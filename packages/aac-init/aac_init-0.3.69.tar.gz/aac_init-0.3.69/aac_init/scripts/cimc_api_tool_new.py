# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

import re
import urllib3
import requests
import xml.etree.ElementTree as ET

from logging_tool import setup_logging

logger = setup_logging("apic_cimc_pre_check")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CIMCTool:
    def __init__(self, cimc_ip, cimc_username, cimc_password):
        self.cimc_ip = cimc_ip
        self.cimc_username = cimc_username
        self.cimc_password = cimc_password
        self.token = None

    def cimc_api(self, data):
        try:
            cimc_url = f"https://{self.cimc_ip}/nuova"
            headers = {
                'accept': '*/*',
                'Content-Type': 'text/html',
            }

            response = requests.post(
                url=cimc_url,
                headers=headers,
                data=data,
                verify=False
            )

            if response.status_code == 200:
                return response
            else:
                msg = f"APIC CIMC {self.cimc_ip} connection failed!"
                logger.error(msg)
                return False
        except Exception as e:
            msg = "{}".format(e)
            logger.error(msg)
            return False

    def cimc_login(self):
        try:
            data = (
                f"<aaaLogin inName='{self.cimc_username}' "
                f"inPassword='{self.cimc_password}'>"
                f"</aaaLogin>"
            )
            response = self.cimc_api(data)
            self.token = ET.fromstring(response.text).attrib.get('outCookie')
            if self.token:
                logger.info(f"CIMC Login token: {self.token}")
                return self.token
            else:
                msg = f"CIMC {self.cimc_ip} Login failed!"
                logger.error(msg)
                return False

        except Exception as e:
            msg = "{}".format(e)
            logger.error(msg)
            return False

    def cimc_logout(self):
        try:
            data = f"<aaaLogout cookie='{self.token}' inCookie='{self.token}'></aaaLogout>"
            self.cimc_api(data)
            logger.info(f"Logout CIMC {self.cimc_ip} with token {self.token} successfully.")
        except Exception as e:
            msg = "{}".format(e)
            logger.error(msg)
            return False

    def cimc_health_check(self):
        try:
            firmware_data = f'''
            <!-- firmware version -->
            <configResolveDn cookie="{self.token}" inHierarchical='false'
            dn="sys/rack-unit-1/mgmt/fw-system"/>
            '''
            firmware_response = self.cimc_api(firmware_data)
            firmware_version = ET.fromstring(firmware_response.text).find(
                './/firmwareRunning').attrib['version']
            logger.info(f"Current Firmware version is: {firmware_version}")

            fault_data = f'''
            <!-- fault info -->
            <configResolveClass cookie="{self.token}"
            inHierarchical='false' classId='faultInst'/>
            '''
            logger.info("Logging CIMC fault info:")
            fault_response = self.cimc_api(fault_data)
            logger.info(fault_response.text)

            tpm_data = f'''
            <!-- TPM status -->
            <configResolveClass cookie="{self.token}"
            inHierarchical='false' classId='equipmentTpm'/>
            '''
            tpm_response = self.cimc_api(tpm_data)
            tpm_status = ET.fromstring(tpm_response.text).find(
                './/equipmentTpm').attrib['enabledStatus']
            logger.info(f"Current TPM status is: {tpm_status}")

            if "enable" not in tpm_status:
                logger.error(f"CIMC {self.cimc_ip}: TPM is not enabled!")
                return False

            return True

        except Exception as e:
            msg = "{}".format(e)
            logger.error(msg)
            return False

    def cimc_clear_mapping(self):
        try:
            cimc_mapping_data = f'''
            <!-- Retrieve CIMC mapping -->
            <configResolveClass cookie="{self.token}"
            inHierarchical='false' classId='commVMediaMap'/>
            '''
            cimc_mapping_response = self.cimc_api(cimc_mapping_data)
            if re.search(r'commVMediaMap volumeName', cimc_mapping_response.text):
                existing_mapping = ET.fromstring(
                    cimc_mapping_response.text).find(
                    './/commVMediaMap').attrib['volumeName']
                logger.info(f"Removing existing mapping: {existing_mapping}")
                cimc_mapping_clear_data = f'''
                <!-- CIMC mapping clear -->
                <configConfMo cookie="{self.token}"><inConfig>
                    <commVMediaMap
                    dn="sys/svc-ext/vmedia-svc/vmmap-{existing_mapping}"
                    volumeName="{existing_mapping}"
                    status='removed' ></commVMediaMap>
                </inConfig></configConfMo>
                '''
                cimc_mapping_clear_response = self.cimc_api(cimc_mapping_clear_data)
                if cimc_mapping_clear_response:
                    logger.info(f"Removed existing mapping: {existing_mapping}")
                else:
                    return False

            cimc_boot_data = f'''
            <!-- Retrieve CIMC boot order -->
            <configResolveClass cookie="{self.token}"
            inHierarchical='false' classId='lsbootVMedia'/>
            '''
            cimc_boot_data_response = self.cimc_api(cimc_boot_data)
            if re.search(r'lsbootVMedia name', cimc_boot_data_response.text):
                existing_bootorder = ET.fromstring(
                    cimc_boot_data_response.text).find(
                    './/lsbootVMedia').attrib['name']
                logger.info(f"Removing existing boot order: {existing_bootorder}")
                cimc_bootorder_clear_data = f'''
                <!-- CIMC boot order clear -->
                <configConfMo cookie="{self.token}"><inConfig>
                    <lsbootVMedia
                    dn="sys/rack-unit-1/boot-precision/vm-{existing_bootorder}"
                    name="{existing_bootorder}" status='removed' ></lsbootVMedia>
                </inConfig></configConfMo>
                '''
                cimc_bootorder_clear_response = self.cimc_api(cimc_bootorder_clear_data)
                if cimc_bootorder_clear_response:
                    logger.info(f"Removed existing boot order: {existing_bootorder}")
                else:
                    return False

            return True

        except Exception as e:
            msg = "{}".format(e)
            logger.error(msg)
            return False

    def power_down_cimc(self):
        try:
            cimc_power_down_data = f'''
            <!-- CIMC Power Off -->
            <configConfMo cookie="{self.token}"><inConfig>
                <computeRackUnit dn="sys/rack-unit-1" adminPower="down" />
            </inConfig></configConfMo>
            '''
            cimc_power_down_response = self.cimc_api(cimc_power_down_data)
            if cimc_power_down_response:
                logger.info("CIMC is powered down.")
            else:
                return False

            return True

        except Exception as e:
            msg = "{}".format(e)
            logger.error(msg)
            return False

    def cimc_precheck(self):
        try:
            self.cimc_login()
            health_check_result = self.cimc_health_check()
            if not health_check_result:
                logger.error("CIMC health check failed!")
                return False

            logger.info("CIMC health check pass!")

            cimc_clear_mapping_result = self.cimc_clear_mapping()
            if not cimc_clear_mapping_result:
                logger.error("CIMC mapping clean failed!")
                return False

            logger.info("CIMC mapping clean successfully.")
            logger.info("Powering down CIMC...")
            self.power_down_cimc()
            return True

        except Exception as e:
            msg = "{}".format(e)
            logger.error(msg)
            return False

    def cimc_install_apic(self, hostname, description, timezone,
                        ntp_server, aci_image_path, apic_image):

        self.cimc_login()

        cimc_install_data = {
            "Configure hostname": f"""
                <configConfMo cookie="{self.token}"><inConfig>
                    <mgmtIf dn="sys/rack-unit-1/mgmt/if-1" hostname="{hostname}"/>
                </inConfig></configConfMo>
            """,

            "Configure description": f"""
                <configConfMo cookie="{self.token}"><inConfig>
                    <computeRackUnit dn="sys/rack-unit-1" usrLbl="{description}"/>
                </inConfig></configConfMo>
            """,

            "Configure timeZone": f"""
                <configConfMo cookie="{self.token}"><inConfig>
                    <topSystem dn="sys" timeZone="{timezone}"/>
                </inConfig></configConfMo>
            """,

            "Configure NTP": f"""
                <configConfMo cookie="{self.token}"><inConfig>
                    <commNtpProvider dn="sys/svc-ext/ntp-svc" ntpServer1="{ntp_server}"/>
                </inConfig></configConfMo>
            """,

            "Configure SOL": f"""
                <configConfMo cookie="{self.token}"><inConfig>
                    <solIf dn="sys/rack-unit-1/sol-if" adminState="enable" speed="115200"
                        comport="com0" sshPort="2400"/>
                </inConfig></configConfMo>
            """,

            "Configure CIMC mapping": f"""
                <configConfMo cookie="{self.token}"><inConfig>
                    <commVMediaMap volumeName="aci-automation" map="www"
                                remoteShare="{aci_image_path}" remoteFile="{apic_image}"
                                dn="sys/svc-ext/vmedia-svc/vmmap-aci-automation"/>
                </inConfig></configConfMo>
            """,

            "IMC change boot order to CIMC-map": f"""
                <configConfMo cookie="{self.token}"><inConfig>
                    <lsbootVMedia dn="sys/rack-unit-1/boot-precision/vm-cimc-map"
                                name="cimc-map" type="VMEDIA" subtype="cimc-mapped-dvd"
                                order="1" state="Enabled"/>
                </inConfig></configConfMo>
            """,

            "CIMC power up": f"""
                <configConfMo cookie="{self.token}"><inConfig>
                    <computeRackUnit dn="sys/rack-unit-1" adminPower="up"/>
                </inConfig></configConfMo>
            """,
        }

        for key,value in cimc_install_data.items():
            cimc_install_apic_response = self.cimc_api(value)
            if cimc_install_apic_response:
                logger.info(cimc_install_apic_response)
                logger.info(f"CIMC APIC installer triggered: {key}")
            else:
                return False

        return True



