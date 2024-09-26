# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>, Rudy Lei <shlei@cisco.com>

import os
import re
import sys
import click
import shutil
import errorhandler
# import aac_init.validator

from .. import __version__ #
from . import options, selections, cli_validators
from aac_init.conf import settings #
from aac_init.logging import setup_logger #

# from aac_init.yaml_conf import yaml_writer
# from aac_init.scripts.thread_tool import MyThread
# from aac_init.scripts.ansible_tool import ansible_deploy_function


error_handler = errorhandler.ErrorHandler()


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
@options.yaml_dir_path
@options.log_level
def main(
        data: str,
        log_level: str
) -> None:
    """
    A CLI tool to bootstrap and configure ACI fabric using ACI as Code.
    """
    # Setup working dir
    output_path = settings.OUTPUT_BASE_DIR

    if os.path.exists(output_path) and os.path.isdir(output_path):
        shutil.rmtree(output_path)

    settings.DEFAULT_LOG_LEVEL = log_level

    logger = setup_logger("main.log")

    cli_validator = cli_validators.CLI_Validator(data, output_path)
    logger.debug("CLI Validator initialized.\n")

    # Type single number or multiple numbers (1,2... or *)
    selection_prompt = "Select single or multiple choice(s) " \
            "to init ACI Fabric:\n{}\nExample: (1,2,.. or *)"\
        .format("\n".join([f"[{i + 1}]  {selection}" for i, selection
                in enumerate(settings.DEFAULT_USER_SELECTIONS)]))
    selection_choices = click.prompt(
        click.style(selection_prompt, fg='green'),
        type=cli_validator.validate_selections)
    logger.debug("Selections validated successfully.")
    if not selection_choices:
        logger.debug("Selections validated failed. Exiting...")
        exit()

    # Type "yes" or "no" to confirm
    confirm_prompt = (
    "\nAre you sure to proceed with the following choice(s)?\n"
    + "\n".join(
        f"[{i}] {settings.DEFAULT_USER_SELECTIONS[int(i) - 1]}"
        for i in selection_choices
    )
    + "\n")

    selections_confirm = click.prompt(
    click.style(confirm_prompt, fg='green'),
    type=click.Choice(['yes', 'no'], case_sensitive=False),
    default='yes',
    show_default=True,
    show_choices=True)

    if not re.match(r"yes", selections_confirm, re.IGNORECASE):
        logger.error("Process aborted, exiting aac-init tool...")
        exit()

    logger.info("Start to process aac-init tool!")
    logger.info("Validating data file...")
    if cli_validator.validate_cli_input():
        logger.info("Input data files validated successfully.")
    else:
        logger.error("input data files validated failed!")
        logger.error("Error details:\n")
        formatted_errors = "\n".join(
            [f"{i + 1}. {error}" for i, error in enumerate(cli_validator.errors)])
        logger.error(f"Errors:\n{formatted_errors}")
        exit()

    # selections handling
    cli_selection = selections.Selections(data, output_path)
    for selection in selection_choices:
        logger.info(f"Start to process selection: {selection}")
        match selection:
            case "1":
                if cli_selection.fabric_bootstrap():
                    logger.info("ACI fabric bootstrap successfully.")
                else:
                    logger.error("ACI fabric bootstrap failed!")
                    exit()
            case "2":
                if cli_selection.apic_init_setup():
                    logger.info("APIC initial setup successfully.")
                else:
                    logger.error("APIC initial setup failed!")
                    exit()
            case "3":
                exit()
            case _:
                logger.error(f"Unknown selection: {selection}")
                exit()

    ######
#     for option in option_choice:
#         logger.info("Start processing step {}.".format(option))
#         if int(option) in [1]:
#             error = validator.validate_ssh_telnet_connection()
#             if error:
#                 exit()
#             yaml_path = validator.validate_yaml_exist(
#                 settings.DEFAULT_DATA_PATH
#             )
#             if not yaml_path:
#                 exit()
#             error = validator.validate_cimc_precheck()
#             if error:
#                 exit()
#             try:
#                 if 'apic_nodes_connection' in settings.global_policy['fabric']:
#                     apics = settings.global_policy['fabric']['apic_nodes_connection']

#                     parent_dir = os.path.dirname(settings.TEMPLATE_DIR[int(option) - 1][0])
#                     folder_name = os.path.basename(parent_dir)

#                     for apic in apics:
#                         writer = yaml_writer.YamlWriter([yaml_path])
#                         writer.write_1(settings.TEMPLATE_DIR[int(option) - 1][0], output, apic['hostname'])
#                         logger.info(f"Generate step {option} apic {apic['hostname']} working directory"
#                                     f"in {output} successfully.")

#                         dir_path = os.path.join(
#                             output,
#                             folder_name,
#                             apic['hostname'],
#                             'apic_reimage',
#                             'vars'
#                         )

#                         if os.path.exists(dir_path) and os.path.isdir(dir_path):
#                             yaml_cp_output_path = os.path.join(
#                                 dir_path,
#                                 'main.yaml'
#                             )
#                             result = validator.write_output(
#                                 yaml_path,
#                                 yaml_cp_output_path,
#                                 apic,
#                                 'apic'
#                             )
#                             if not result:
#                                 exit()

#                         settings.STEP_1_YAML_LIST.append(os.path.join(output, folder_name, apic['hostname'], settings.YAML_NAME[0][0]))
#                 else:
#                     logger.warning("No APIC configuration provided.")

#                 if 'switch_nodes_connection' in settings.global_policy['fabric']:
#                     switches = settings.global_policy['fabric']['switch_nodes_connection']
#                     parent_dir = os.path.dirname(settings.TEMPLATE_DIR[int(option) - 1][1])
#                     folder_name = os.path.basename(parent_dir)

#                     for switch in switches:
#                         writer = yaml_writer.YamlWriter([yaml_path])
#                         writer.write_1(settings.TEMPLATE_DIR[int(option) - 1][1], output, switch['hostname'])
#                         logger.info(f"Generate step {option} switch {switch['hostname']} working directory"
#                                     f"in {output} successfully.")

#                         dir_path = os.path.join(
#                             output,
#                             folder_name,
#                             switch['hostname'],
#                             'aci_switch_reimage',
#                             'vars'
#                         )

#                         if os.path.exists(dir_path) and os.path.isdir(dir_path):
#                             yaml_cp_output_path = os.path.join(
#                                 dir_path,
#                                 'main.yaml'
#                             )
#                             result = validator.write_output(
#                                 yaml_path,
#                                 yaml_cp_output_path,
#                                 switch,
#                                 'switch'
#                             )
#                             if not result:
#                                 exit()

#                         settings.STEP_1_YAML_LIST.append(os.path.join(output, folder_name, switch['hostname'], settings.YAML_NAME[0][1]))
#                 else:
#                     logger.warning("No Switch configuration provided.")
#                 if 'apic_nodes_connection' not in settings.global_policy['fabric'] and 'switch_nodes_connection' not in settings.global_policy['fabric']:
#                     logger.error("No APIC/Switch configuration provided.")
#                     exit()

#             except Exception as e:
#                 msg = f"Generate working directory failed.\nDetail: {e}"
#                 logger.error(msg)
#                 exit()
#             try:
#                 if 'apic_nodes_connection' in settings.global_policy['fabric'] or 'switch_nodes_connection' in settings.global_policy['fabric']:
#                     logger.info("ACI fabric bootstrap in progress, "
#                             "check APIC/switch logs for detail.")
#                     step_1_threads = []
#                     for step1_yaml_path in settings.STEP_1_YAML_LIST:
#                         thread = MyThread(
#                                     target=ansible_deploy_function,
#                                     args=(
#                                         step1_yaml_path,
#                                         os.path.basename(os.path.dirname(step1_yaml_path)),
#                                         option,
#                                         None,
#                                         True)
#                                 )
#                         step_1_threads.append(thread)

#                     for thread in step_1_threads:
#                         thread.start()

#                     for thread in step_1_threads:
#                         thread.join()

#                     for thread in step_1_threads:
#                         if not thread.get_result():
#                             logger.error(
#                                 "ACI fabric bootstrap failed, "
#                                 "check APIC/switch logs for detail."
#                             )
#                             exit()

#                     logger.info("ACI fabric bootstrap is successfully.")
#                     logger.info("Processing step {} completed.".format(option))

#             except Exception as e:
#                 msg = "Run Step 1 ACI fabric bootstrap ansible-playbook" \
#                       " failed.\nDetail: {}".format(e)
#                 logger.error(msg)
#                 exit()


#         elif int(option) in [2]:
#             yaml_path = validator.validate_yaml_exist(
#                 settings.DEFAULT_DATA_PATH
#             )
#             if not yaml_path:
#                 exit()
#             error = validator.validate_cimc_precheck()
#             if error:
#                 exit()
#             try:
#                 if 'apic_nodes_connection' in settings.global_policy['fabric']:
#                     apics = settings.global_policy['fabric']['apic_nodes_connection']

#                     folder_name = os.path.basename(settings.TEMPLATE_DIR[int(option) - 1])

#                     for apic in apics:
#                         writer = yaml_writer.YamlWriter([yaml_path])
#                         writer.write_2(settings.TEMPLATE_DIR[int(option) - 1], output, apic['hostname'])
#                         logger.info(f"Generate step {option} apic {apic['hostname']} working directory"
#                                     f"in {output} successfully.")

#                         dir_path = os.path.join(
#                             output,
#                             folder_name,
#                             apic['hostname'],
#                             'apic_setup',
#                             'vars'
#                         )

#                         if os.path.exists(dir_path) and os.path.isdir(dir_path):
#                             yaml_cp_output_path = os.path.join(
#                                 dir_path,
#                                 'main.yaml'
#                             )
#                             result = validator.write_output(
#                                 yaml_path,
#                                 yaml_cp_output_path,
#                                 apic,
#                                 'apic'
#                             )
#                             if not result:
#                                 exit()

#                         settings.STEP_2_YAML_LIST.append(os.path.join(output, folder_name, apic['hostname'], settings.YAML_NAME[1]))
#                 else:
#                     logger.warning("No APIC configuration provided.")

#             except Exception as e:
#                 msg = f"Generate working directory failed.\nDetail: {e}"
#                 logger.error(msg)
#                 exit()

#             try:
#                 if 'apic_nodes_connection' in settings.global_policy['fabric']:
#                     logger.info("APIC setup in progress, "
#                             "check APIC setup logs for detail.")
#                     step_2_threads = []
#                     for step2_yaml_path in settings.STEP_2_YAML_LIST:
#                         thread = MyThread(
#                                     target=ansible_deploy_function,
#                                     args=(
#                                         step2_yaml_path,
#                                         os.path.basename(os.path.dirname(step2_yaml_path)),
#                                         option,
#                                         None,
#                                         True)
#                                 )
#                         step_2_threads.append(thread)

#                     for thread in step_2_threads:
#                         thread.start()

#                     for thread in step_2_threads:
#                         thread.join()

#                     for thread in step_2_threads:
#                         if not thread.get_result():
#                             logger.error(
#                                 "APIC setup failed, "
#                                 "check APIC setup logs for detail."
#                             )
#                             exit()

#                     logger.info("APIC setup is successfully.")
#                     logger.info("Processing step {} completed.".format(option))

#             except Exception as e:
#                 msg = "Run Step 2 APIC setup ansible-playbook" \
#                       " failed.\nDetail: {}".format(e)
#                 logger.error(msg)
#                 exit()

#         elif int(option) in [3]:
#             error = validator.validate_apic_aaa_connection()
#             if error:
#                 exit()
#             yaml_path = validator.validate_yaml_exist(
#                 settings.DEFAULT_DATA_PATH
#             )
#             if not yaml_path:
#                 exit()
#             option_yaml_path = validator.validate_yaml_dir_exist(
#                 settings.DATA_PATH
#             )
#             if not option_yaml_path:
#                 exit()
#             try:
#                 writer = yaml_writer.YamlWriter([yaml_path])
#                 writer.write_3(
#                     settings.TEMPLATE_DIR[int(option)-1],
#                     output
#                 )
#                 logger.info(
#                     "Generate step {} working directory in {} successfully."
#                     .format(option, output)
#                 )
#                 dir_path = os.path.join(
#                     output,
#                     os.path.basename(settings.TEMPLATE_DIR[int(option)-1]),
#                     'host_vars',
#                     'apic1'
#                 )
#                 if os.path.exists(dir_path) and os.path.isdir(dir_path):
#                     yaml_cp_output_path = os.path.join(
#                         dir_path,
#                         'data.yaml'
#                     )
#                     result = validator.write_output(
#                         option_yaml_path,
#                         yaml_cp_output_path
#                     )
#                     if not result:
#                         exit()

#             except Exception as e:
#                 msg = "Generate working directory failed.\nDetail: {}"\
#                     .format(e)
#                 logger.error(msg)
#                 exit()

#             try:
#                 inventory_path = os.path.join(
#                     os.getcwd(),
#                     output,
#                     os.path.basename(settings.TEMPLATE_DIR[int(option)-1]),
#                     'inventory.yaml'
#                 )
#                 playbook_dir_validate = os.path.join(
#                     os.getcwd(),
#                     output,
#                     os.path.basename(settings.TEMPLATE_DIR[int(option)-1]),
#                     'aac_ansible',
#                     "apic_validate.yaml"
#                 )

#                 playbook_dir_deploy = os.path.join(
#                     os.getcwd(),
#                     output,
#                     os.path.basename(settings.TEMPLATE_DIR[int(option)-1]),
#                     'aac_ansible',
#                     "apic_deploy.yaml"
#                 )

#                 playbook_dir_test = os.path.join(
#                     os.getcwd(),
#                     output,
#                     os.path.basename(settings.TEMPLATE_DIR[int(option)-1]),
#                     'aac_ansible',
#                     "apic_test.yaml"
#                 )

#                 validate_result = ansible_deploy_function(
#                     playbook_dir=playbook_dir_validate,
#                     step_name=settings.ANSIBLE_STEP[3],
#                     inventory_path=inventory_path,
#                     option=option,
#                     quiet=False)

#                 if not validate_result:
#                     logger.error("NaC validated failed!")
#                     exit()

#                 deploy_result = ansible_deploy_function(
#                     playbook_dir=playbook_dir_deploy,
#                     step_name=settings.ANSIBLE_STEP[4],
#                     inventory_path=inventory_path,
#                     option=option,
#                     quiet=False
#                 )

#                 if not deploy_result:
#                     logger.error("NaC deployed failed!")
#                     exit()

#                 test_result = ansible_deploy_function(
#                     playbook_dir=playbook_dir_test,
#                     step_name=settings.ANSIBLE_STEP[5],
#                     inventory_path=inventory_path,
#                     option=option,
#                     quiet=False
#                 )

#                 if not test_result:
#                     logger.error("NaC tested failed!")
#                     exit()

#             except Exception as e:
#                 msg = "Run Step 3 NaC ansible-playbook" \
#                         " failed.\nDetail: {}".format(e)
#                 logger.error(msg)
#                 exit()

#             logger.info("Processing step {} completed.".format(option))

#     logger.info(f"Option(s): {option_choice} had been completed!")


def exit() -> None:
    if error_handler.fired:
        sys.exit(1)
    else:
        sys.exit(0)
