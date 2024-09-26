# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

__author__ = "shlei"


from netmiko import ConnectHandler, NetMikoTimeoutException, NetMikoAuthenticationException
from datetime import datetime
from time import sleep
from logging_tool import setup_logging

import re
import ipaddress
import threading
import queue

logger = setup_logging("cimc_ssh")

class SSHTool:
    def __init__(
            self,
            device_id: int,
            hostname: str,
            host: str,
            username: str,
            password: str,
            session_log: str,
            fast_cli: bool = False, # Disable fast CLI to mimic human-like sending
            **kwargs
    ):
        self.device_id = device_id
        self.hostname = hostname
        self.host = host
        self.username = username
        self.password = password
        self.fast_cli = fast_cli
        self.session_log = session_log
        self.device = {
            'host': self.host,
            'username': self.username,
            'password': self.password,
            "fast_cli" : self.fast_cli,
            'session_log': self.session_log,
        }
        self.connection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.disconnect()

        if exc_type:
            logger.error(f"error: {exc_type}, {exc_val}")

    def ssh_device(self):
        DEVICE_TYPES = ["generic", "linux",]
        for device_type in DEVICE_TYPES:
            try:
                logger.info(f"Attempting to connect {self.hostname} with {device_type}...")
                self.device["device_type"] = device_type
                self.connection = ConnectHandler(**self.device)
                logger.info(f"Connected to {self.hostname}: with {device_type} successfully!")
                return True
            except Exception as e:
                logger.error(f"Failed to connect to {self.hostname} with {device_type}: {e}")
                sleep(3)
        logger.error(f"Failed to connect to {self.hostname} with both methods!")
        return False

    def ssh_cimc_installer(self, iso_url):
        # Speed up APIC install process

        # V4: To speed up the install, enter iso url in next ten minutes:
        # V5: To speed up the install, enter iso url in next ten minutes:
        # V6: To speed up the install, enter iso url
        self.connection.send_command("connect host", "To speed up the install, enter iso url", read_timeout=900)

        # V4: type static, dhcp, bash for a shell to configure networking, or url to re-enter the url
        # V5: type static, dhcp, bash for a shell to configure networking, or url to re-enter the url
        # V6: type static, dhcp, bash for a shell to configure networking, or url to re-enter the url
        self.connection.send_command(iso_url, "type static, dhcp, bash for a shell to configure networking", read_timeout=90)

        return True

