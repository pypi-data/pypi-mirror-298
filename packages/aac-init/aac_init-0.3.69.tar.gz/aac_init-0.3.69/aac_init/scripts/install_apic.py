from cimc_api_tool_new import CIMCTool
from ssh_tool_new import SSHTool
from logging_tool import setup_logging
from datetime import datetime
from time import sleep

# Init
cimc_address = "10.124.145.34"
apic_cimc_username = "admin"
apic_cimc_password = "P@ssw0rd"



# Install - API

hostname = "dlc-aci01-apic1-cimc"
description = "ACI Lab - POD01 - dlc-aci01-apic1"
timezone = "Asia/Shanghai"
ntp_server = "ntp.esl.cisco.com"
aci_image_path = "http://10.124.145.88/Images/ACI/4/4.2/"
apic_image = "aci-apic-dk9.4.2.7f.iso"


device_id = "1"

current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")



iso_url = aci_image_path + apic_image


if __name__ == "__main__":

    # validate APIC
    for apic in apics:
        f1apic1api = CIMCTool(cimc_address, apic_cimc_username, apic_cimc_password)
        f1apic1api.cimc_precheck()

    # install APIC - api
    for apic in apics: #Multi threading
        f1apic1api.cimc_install_apic(hostname, description, timezone,
                        ntp_server, aci_image_path, apic_image)

        f1apic1api.cimc_logout()
        # sleep 180 to wait cimc power-down
        # print("sleep 180 to wait cimc power-down")
        # sleep(180)

        # install APIC - SSH - monitor/post-check
        f1apic1ssh = SSHTool(device_id, hostname, cimc_address,
                    apic_cimc_username, apic_cimc_password,
                    session_log=f"ssh_install_session_{hostname}_{current_datetime}.log")

        f1apic1ssh.ssh_device()
        if not f1apic1ssh.connection:
            print(f"Failed to connect to {hostname}, need to check manually!")

        f1apic1ssh.ssh_cimc_installer(iso_url)
