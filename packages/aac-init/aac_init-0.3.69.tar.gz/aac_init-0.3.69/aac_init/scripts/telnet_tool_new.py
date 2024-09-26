# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

__author__ = "xiawang3, yabian, shlei"


from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from datetime import datetime
from time import sleep
import re
import ipaddress
import threading
import queue


class TelnetTool:
    def __init__(
            self,
            device_id: int,
            hostname: str,
            console_host: str,
            console_port: int,
            username: str,
            password: str,
            session_log: str,
            **kwargs
    ):
        self.device_id = device_id
        self.hostname = hostname
        self.console_host = console_host
        self.console_port = console_port
        self.username = username
        self.password = password
        self.session_log = session_log
        self.login_state = False
        self.device = {
            'host': self.console_host,
            'port': self.console_port,
            'username': self.username,
            'password': self.password,
            'session_log': self.session_log,
        }
        self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.disconnect()

        if exc_type:
            print(f"error: {exc_type}, {exc_val}")

    def telnet_device(self):
        DEVICE_TYPES = ["cisco_ios_telnet", "generic_telnet",]
        for device_type in DEVICE_TYPES:
            try:
                print(f"Attempting to connect {self.hostname}:{self.console_port} with {device_type}...")
                self.device["device_type"] = device_type
                self.connection = ConnectHandler(**self.device)
                print(f"Connected to {self.hostname}:{self.console_port} with {device_type} successfully!")
                self.login_state = True
                return True
            # except (NetMikoTimeoutException, NetMikoAuthenticationException) as e:
            #     print(f"Connect to {self.hostname} with {device_type} failed: {e}")
            #     sleep(3)
            except Exception as e:
                print(f"Failed to connect to {self.hostname}:{self.console_port} with {device_type}: {e}")
                sleep(3)
        print(f"Failed to connect to {self.hostname}:{self.console_port} with both methods!")
        return False

    @staticmethod
    def determine_aci_switch_image(aci_switch_image_filename):
        pattern = r"(?:aci-n9000-dk9\.)(\d+\.\d+\.\d+[a-z])\.bin"
        version_match = re.search(pattern, aci_switch_image_filename)

        if version_match:
            print(f"Matched version: {version_match.group(1)}")
            version_part = re.match(r'(\d+)\.(\d+)\.(\d+)([a-z])', version_match.group(1))

            if version_part:
                major, minor, patch, suffix = version_part.groups()
                aci_version = [int(major), int(minor), int(patch)]
                print(f"ACI version: {aci_version}")
                return aci_version

            else:
                print("Failed to parse the version components.")
        else:
            print("Invalid image format.")

        return None

    def validate_aci_switch(self, aci_switch_image_filename):

        switch_prompt = self.connection.find_prompt()
        print(f"switch prompt: {switch_prompt}")

        aci_switch_image = self.determine_aci_switch_image(aci_switch_image_filename)
        if not aci_switch_image:
            print(f"image validate failed: {aci_switch_image_filename}")
            return False

        if "loader >" in switch_prompt:
            loader_output = self.connection.send_command_timing("keyinfo")
            if aci_switch_image >= [16, 0, 2]:
                print("Warning: cannot determine PID for 32/64 image selection, \
                    suggest to fix loader manually or install pre 602.")
                return False
            if "Nexus9k" in loader_output:
                return True
            else:
                print("Not N9K or 'keyinfo' not supported in this loader version, please check manually")
        elif "#" in switch_prompt:
            version_output = self.connection.send_command_timing("show version | grep kickstart")
            inventory_output = self.connection.send_command_timing("show inventory | grep -A1 Chassis")
            if ("aci" in version_output or "nxos" in version_output) and "N9K" in inventory_output:
                return True
            else:
                print("Not N9K")
        else:
            print("Unknown device type")

        return False

    def enter_loader(self, aci_switch_image_filename):
        # TBD: Need to enhance to determine ACI/NXOS running method on modular spine
        current_os_running = self.connection.send_command("show version | grep kickstart", read_timeout=60)
        current_os_running += self.connection.send_command("cat /mnt/cfg/0/boot/grub/menu.lst.local", read_timeout=60)

        # TBD: Always go 32-bit image for less 602, for 602 and above, install 64-bit per pid
        # TBD: Need to determine leaf memory selection..
        if self.determine_aci_switch_image(aci_switch_image_filename) >= [16, 0, 2]:
            SWITCH_602_64BIT = ["N9K-C9408", "N9K-C9504", "N9K-C9508", "N9K-C9516",
                "N9K-C9364D-GX2A", "N9K-C9348D-GX2A", "N9K-C9332D-GX2B",
                "N9K-C93600CD-GX", "N9K-C9316D-GX", "N9K-C9364C",]
            pid_raw = self.connection.send_command("show inventory | grep -A1 Chassis", read_timeout=60)
            pid_pattern = re.compile(r'PID: (N9K-[A-Z0-9\-]+)')

            if pid_raw:
                if not pid_pattern.findall(pid_raw):
                    print("Unable to determine chassis PID!")
                    return None
                if pid_pattern.findall(pid_raw)[0] in SWITCH_602_64BIT:
                    aci_switch_image_filename = aci_switch_image_filename.replace(".bin", "-cs_64.bin")
            else:
                # TBD: Need to enhance to determine modular spine
                aci_switch_image_filename = aci_switch_image_filename.replace(".bin", "-cs_64.bin")

        # ACI handler
        if "aci" in current_os_running:
            self.connection.send_command("rm -f bootflash/*.bin", read_timeout=90)
            self.connection.send_command("setup-clean-config.sh", "Done", read_timeout=90)
            self.connection.send_command("clear-bootvars.sh", "Done", read_timeout=90)

            grub0_output = self.connection.send_command("ls /mnt/cfg/0/boot/grub/")
            grub1_output = self.connection.send_command("ls /mnt/cfg/1/boot/grub/")
            if any([grub0_output, grub1_output]):
                print("grub clear failed!")
                return None

            try:
                self.connection.send_command("reload", "This command will reload the chassis", read_timeout=60)
                self.connection.send_command_timing("y")

                self.connection.read_until_pattern(pattern="loader >",read_timeout=300)
                print("Entered to loader")
                return aci_switch_image_filename
            except Exception as e:
                print(f"Node {self.hostname}: Failed to enter loader: {e}")

        # Nexus handler
        else:
            self.connection.send_command("configure terminal", "config", read_timeout=60)
            self.connection.send_command("delete bootflash:*.bin no-prompt", read_timeout=60)
            self.connection.send_command("no boot nxos", read_timeout=60)
            try:
                self.connection.send_command("copy running-config startup-config", "Copy complete.", read_timeout=60)
                self.connection.send_command("reload", "This command will reboot the system", read_timeout=60)
                self.connection.send_command_timing("y")

                self.connection.read_until_pattern(pattern="loader >",read_timeout=300)
                print("Entered to loader")
                return aci_switch_image_filename
            except Exception as e:
                print(f"Node {self.hostname}: Failed to enter loader: {e}")


        return None

    def loader_installer(self, nodes, aci_image_path, aci_switch_image_filename):
        aci_switch_image_http = aci_image_path + aci_switch_image_filename
        aci_switch_image_tftp = aci_switch_image_http.replace("http", "tftp")

        device_info = [(node.get("oob_address"), node.get("oob_gateway")) for node in nodes if node.get("id") == self.device_id]
        if device_info:
            device_oob, device_gw = device_info[0]
        else:
            print(f"no IP found for {self.hostname}!")

        device_oob_trad = ipaddress.IPv4Interface(device_oob)

        set_tftp_ip = f"set ip {device_oob_trad.ip} {device_oob_trad.netmask}"
        set_tftp_gw = f"set gw {device_gw}"
        tftp_boot_cmd = f"boot {aci_switch_image_tftp}"

        self.connection.send_command_timing("\n")
        self.connection.send_command_timing(set_tftp_ip)
        set_gw_result = self.connection.send_command_timing(set_tftp_gw)

        address_check = f"Address: {device_oob_trad.ip}" in set_gw_result
        netmask_check = f"Netmask: {device_oob_trad.netmask}" in set_gw_result
        gateway_check = f"Gateway: {device_gw}" in set_gw_result

        if all([address_check, netmask_check, gateway_check]):
            self.connection.send_command_timing(tftp_boot_cmd)
            try:
                print(f"Node {self.hostname}: Start to install {aci_switch_image_filename}")
                self.connection.read_until_pattern(pattern="Certificate verification passed",read_timeout=900)
            except Exception as e:
                print(f"Failed to install {self.hostname}: {e}")

        # loader post-installation check
            sleep(180)
            post_check_result = self.connection.send_command_timing("\n")
            version_post_check = re.search(r'aci-n9000-dk9\.\d+\.\d+\.\d+[a-z]',aci_switch_image_filename).group(0)
            for i in range (1,31):
                print(f"post check retry: {i}")
                print(post_check_result)
                if "(none) login:" in self.connection.find_prompt():
                    post_check_result = self.connection.send_command_timing("admin")
                elif "(none)#" in self.connection.find_prompt():
                    try:
                        post_check_result = self.connection.send_command("cat /mnt/cfg/0/boot/grub/menu.lst.local",
                                                                    expect_string=version_post_check, read_timeout=60)
                        self.connection.disconnect()
                        return True
                    except Exception as e:
                        print(f"Post-check failed: {e}")
                else:
                    post_check_result = self.connection.send_command_timing("\n")
                    sleep(1)

            print("Post-check failed")

        else:
            print("set_gw_result check failed")

        self.connection.disconnect()
        return False



####### Test datas

nodes = [
    {
        "id": 101,
        "pod": 1,
        "role": "leaf",
        "serial_number": "FDO20430UXX",
        "name": "dlc-aci01-leaf101",
        "oob_address": "10.124.145.25/24",
        "oob_gateway": "10.124.145.1"
    },
    {
        "id": 102,
        "pod": 1,
        "role": "leaf",
        "serial_number": "FDO23321AYC",
        "name": "dlc-aci01-leaf102",
        "oob_address": "10.124.145.26/24",
        "oob_gateway": "10.124.145.1"
    },
    {
        "id": 211,
        "pod": 1,
        "role": "spine",
        "serial_number": "FDO21461ZCD",
        "name": "dlc-aci01-spine201",
        "oob_address": "10.124.145.29/24",
        "oob_gateway": "10.124.145.1"
    },
]

switches = [
    {
        "id": 101,
        "hostname": "dlc-aci01-leaf101",
        "console_address": "10.124.120.176",
        "console_port": 2112
    },
    # {
    #     "id": 102,
    #     "hostname": "dlc-aci01-leaf102",
    #     "console_address": "10.124.120.176",
    #     "console_port": 2111
    # },
    # {
    #     "id": 211,
    #     "hostname": "dlc-aci01-spine211",
    #     "console_address": "10.124.120.176",
    #     "console_port": 2108,
    #     "console_address_standby": "10.124.120.176",
    #     "console_port_standby": 2107
    # },
    # {
    #     "id": 211,
    #     "hostname": "dlc-aci01-spine211",
    #     "console_address": "10.124.120.176",
    #     "console_port": 2098,
    #     "console_address_standby": "10.124.120.176",
    #     "console_port_standby": 2099
    # },
]

# switch_images = ["aci-n9000-dk9.14.2.7f.bin", "aci-n9000-dk9.16.0.2h.bin", "aci-n9000-dk9.16.0.5j.bin",]
switch_images = ["aci-n9000-dk9.14.2.7f.bin"]

aci_local_username = "admin"
aci_local_password = "Cisco123"

aci_image_path = "http://10.124.145.88/Images/ACI/4/4.2/"
aci_switch_image = "aci-n9000-dk9.14.2.5k.bin"

# aci_image_path = "http://10.124.145.88/Images/ACI/5/5.2/"
# aci_switch_image = "aci-n9000-dk9.15.2.8g.bin"

# aci_image_path = "http://10.124.145.88/Images/ACI/6/6.0/"
# aci_switch_image = "aci-n9000-dk9.16.0.5h.bin"

####### Test datas


def validation(switches, switch_image):
    print("Validation starts")

    for switch in switches:
        current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
        hostname = switch.get("hostname")
        with TelnetTool(
            device_id=switch.get("id"),
            hostname=hostname,
            console_host=switch.get("console_address"),
            console_port=switch.get("console_port"),
            username=aci_local_username,
            password=aci_local_password,
            session_log=f"validation_{hostname}_{current_datetime}.log"
        ) as tt:
            tt.telnet_device()
            if not tt.connection:
                print(f"Failed to connect to {hostname}, need to check manually!")
                return False
            validation_result = tt.validate_aci_switch(aci_switch_image_filename=switch_image)
            print(f"Validate {hostname}, result: {validation_result}")

        if "console_address_standby" in switch.keys():
            hostname_standby = f"{hostname}_standby"
            with TelnetTool(
                device_id=switch.get("id"),
                hostname=hostname_standby,
                console_host=switch.get("console_address_standby"),
                console_port=switch.get("console_port_standby"),
                username=aci_local_username,
                password=aci_local_password,
                session_log=f"validation_{hostname_standby}_{current_datetime}.log"
            ) as tt_standby:
                tt_standby.telnet_device()
                if not tt_standby.connection:
                    print(f"Failed to connect to {hostname_standby}, need to check manually!")
                    return False
                validation_result = tt_standby.validate_aci_switch(aci_switch_image_filename=switch_image)
                print(f"Validate {hostname_standby}, result: {validation_result}")


    print("Validation ends")

def loader_switch(switch, console_address, console_port, hostname,
                    current_datetime, aci_switch_image, result_queue):
    with TelnetTool(
            device_id=switch.get("id"),
            hostname=hostname,
            console_host=switch.get(console_address),
            console_port=switch.get(console_port),
            username=aci_local_username,
            password=aci_local_password,
            session_log=f"install_session_{hostname}_{current_datetime}.log"
        ) as tt:
            tt.telnet_device()
            if not tt.connection:
                print(f"NODE {hostname}:{console_port}: Failed to connect to {hostname}, need to check manually!")
                result_queue.put(None)
                return
            switch_target_image = aci_switch_image
            switch_prompt = tt.connection.find_prompt()
            print(f"NODE {hostname}:{console_port}: switch prompt: {switch_prompt}")

            if "loader >" not in switch_prompt:
                switch_target_image = tt.enter_loader(aci_switch_image)

    sleep(5)  # release console
    result_queue.put(switch_target_image)


def installation(switch):
    print("installation starts")

    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
    hostname = switch.get("hostname")
    hostname_standby = f"{hostname}_standby" if "console_address_standby" in switch.keys() else None

    # Queues to store results
    result_queue_active = queue.Queue()
    result_queue_standby = queue.Queue() if hostname_standby else None

    # Enter Console
    thread_active = threading.Thread(target=loader_switch, args=(
        switch, "console_address", "console_port", hostname, current_datetime, aci_switch_image, result_queue_active
    ))
    if hostname_standby:
        thread_standby = threading.Thread(target=loader_switch, args=(
            switch, "console_address_standby", "console_port_standby",
            hostname_standby, current_datetime, aci_switch_image, result_queue_standby
        ))

    # Start the threads
    thread_active.start()
    if hostname_standby:
        thread_standby.start()

    # Wait for both threads to complete
    thread_active.join()
    if hostname_standby:
        thread_standby.join()

    # Retrieve results
    switch_target_image = result_queue_active.get()
    device_standby_target_image = result_queue_standby.get() if hostname_standby else None

    # Check results
    if switch_target_image is None:
        print(f"Failed to get the target image for active device {hostname}")
        return False
    if hostname_standby and device_standby_target_image is None:
        print(f"Failed to get the target image for standby device {hostname_standby}")
        return False

    # Install active
    with TelnetTool(
            device_id=switch.get("id"),
            hostname=hostname,
            console_host=switch.get("console_address"),
            console_port=switch.get("console_port"),
            username=aci_local_username,
            password=aci_local_password,
            session_log=f"install_session_{hostname}_{current_datetime}.log"
        ) as tt:
            tt.telnet_device()
            if not tt.connection:
                print(f"Failed to connect to {hostname}, need to check manually!")
                return False
            install_result = tt.loader_installer(nodes, aci_image_path, switch_target_image)
            if install_result:
                print(f"Node {tt.hostname}: Install {switch_target_image} successfully!")
            else:
                print(f"Node {tt.hostname}: Install {switch_target_image} failed!")
                return False

    # Install standby
    if "console_address_standby" in switch.keys():
        with TelnetTool(
                    device_id=switch.get("id"),
                    hostname=hostname_standby,
                    console_host=switch.get("console_address_standby"),
                    console_port=switch.get("console_port_standby"),
                    username=aci_local_username,
                    password=aci_local_password,
                    session_log=f"install_session_{hostname_standby}_{current_datetime}.log"
                ) as tt_standby:
                    tt_standby.telnet_device()
                    if not tt_standby.connection:
                        print(f"Failed to connect to {hostname_standby}, need to check manually!")
                        return False
                    install_result_standby = tt_standby.loader_installer(nodes, aci_image_path, device_standby_target_image)
                    if install_result_standby:
                        print(f"Node {tt_standby.hostname}_standby: Install {device_standby_target_image} successfully!")
                    else:
                        print(f"Node {tt_standby.hostname}_standby: Install {device_standby_target_image} failed!")
                        return False

    return True




if __name__ == "__main__":

    # validation
    for switch in switches:
        validation(switches, aci_switch_image)

    # installation
    switch_threads = []

    for switch in switches:
        switch_thread = threading.Thread(target=installation, args=(switch,))
        switch_threads.append(switch_thread)

    for switch_thread in switch_threads:
        switch_thread.start()

    for switch_thread in switch_threads:
        switch_thread.join()
