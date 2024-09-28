# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>, Rudy Lei <shlei@cisco.com>

import os
import re

from typing import Any, Dict, List, Optional
from aac_init.logging import setup_logger
from aac_init.conf import settings
from aac_init.utils.aac_yaml import load_yaml_files
from aac_init.utils.yaml_writer import YamlWriter
from ruamel import yaml
from ansible_runner import run


class Ansible_Tool:
    """Ansible Toolkits, include validation and deployment"""

    def __init__(self, output_path: str):
        self.logger = setup_logger("ansible_tool.log")

        self.data: Optional[Dict[str, Any]] = None
        self.output_path = output_path
        self.aac_inventory_path = None
        self.errors: List[str] = []

        self.logger.debug("Ansible Tool initialized successfully.")

    def _load_aac_data(self):
        """Load global policy and AAC data"""

        self.logger.debug("Loading global policy and AAC data...")

        try:
            global_policy_writer = YamlWriter([settings.DEFAULT_DATA_PATH])
            global_policy_writer.write_3(settings.TEMPLATE_DIR[0], self.output_path)
            self.logger.debug(
                f"Generate AAC working directory: '{self.output_path}' successfully."
            )

            aac_path = os.path.join(
                self.output_path,
                os.path.basename(settings.TEMPLATE_DIR[0]),
                "host_vars",
                "apic1",
            )
            aac_data_path = os.path.join(aac_path, "data.yaml")

            aac_data = load_yaml_files(settings.DATA_PATH)
            self.logger.debug("Load AAC data successfully.")

            with open(aac_data_path, "w") as aac:
                y = yaml.YAML()
                y.default_flow_style = False
                y.dump(aac_data, aac)

            self.logger.debug(
                f"Copy AAC data to working directory: '{self.output_path}' successfully."
            )

            self.aac_inventory_path = os.path.join(
                os.getcwd(),
                self.output_path,
                os.path.basename(settings.TEMPLATE_DIR[0]),
                "inventory.yaml",
            )

            self.logger.debug("Set AAC inventory successfully.")
            return True

        except Exception as e:
            msg = f"Exception occurred during loading AAC data: {str(e)}"
            self.logger.error(msg)
            self.errors.append(msg)

        return False

    def ansible_runner(
        self, ansible_phase, playbook_dir, inventory_path=None, quiet=True
    ):
        """Ansible runner"""

        logger = setup_logger(f"ansible_tool_{ansible_phase}.log")

        def _callback(res):
            if not quiet and "stdout" in res:
                print(res["stdout"])
            output = re.compile(r"\x1b\[\[?(?:\d{1,2}(?:;\d{0,2})*)?[m|K]").sub(
                "", res["stdout"]
            )
            logger.debug(output)

        runner = run(
            playbook=playbook_dir,
            inventory=inventory_path,
            verbosity=5,
            quiet=True,
            event_handler=_callback,
        )

        if runner.status == "successful":
            logger.debug(
                f"Complete Network as Code Ansible phase: '{ansible_phase}' successfully."
            )
            return True

        else:
            msg = f"Error on Network as Code Ansible phase: '{ansible_phase}'!"
            logger.error(msg)
            self.errors.append(msg)
            return False

    def aac_ansible(self, ansible_phase, playbook_dir):
        """perform AAC ansible"""

        if not self._load_aac_data():
            msg = "Failed to load AAC data!"
            self.logger.error(msg)
            self.errors.append(msg)
            return False

        return self.ansible_runner(
            ansible_phase,
            playbook_dir,
            inventory_path=self.aac_inventory_path,
            quiet=True,
        )
