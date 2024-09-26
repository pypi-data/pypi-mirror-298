# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>

__author__ = "xiawang3, yabian, shlei"


import asyncio
import telnetlib3

from aac_init.scripts.logging_tool import setup_logging


logger = setup_logging()


async def open_connection(host, port):
    try:
        reader, writer = await telnetlib3.open_connection(host, port)
        logger.info(f"{host}:{port} connected successfully.")
        return reader, writer
    except Exception as e:
        logger.error(f"{host}:{port} connected failed!")
        logger.error(f"{host}:{port} exception details: {e}")
        return None, None


class TelnetClient:
    def __init__(
            self,
            telnet_ip,
            telnet_port,
            telnet_username,
            telnet_password
    ):
        self.reader = None
        self.writer = None
        self.host_ip = telnet_ip
        self.port = telnet_port
        self.username = telnet_username
        self.password = telnet_password

    async def read_until(self, match, timeout=20):
        if self.reader:
            try:
                return await asyncio.wait_for(self.reader.readuntil(match), timeout)
            except asyncio.TimeoutError:
                logger.warning(f"{self.host_ip}:{self.port} response timeout!")
                logger.warning(f"Timeout reason: {match.decode()}")
                return False
            except Exception as e:
                logger.error(f"{self.host_ip}:{self.port} response error!")
                logger.error(f"{self.host_ip}:{self.port} exception details: {e}")
                return False

        logger.error(f"{self.host_ip}:{self.port} switch no response!")
        return False

    async def async_login_host(self):
        logger.info(f"Start Telnet connection validation for {self.host_ip}:{self.port}")
        self.reader, self.writer = await open_connection(
            self.host_ip, self.port
        )
        if not self.reader:
            logger.error(f"{self.host_ip}:{self.port} empty reader!")
            return False

        self.writer.write('\n')

        # Login handle: (none) login: , (hostname) login: , (none)#, (hostname)#,

        login_str = await self.read_until(b'login: ')
        if login_str:
            self.writer.write(self.username + '\n')

        pwd_prompt = await self.read_until(b'Password:')
        if pwd_prompt:
            self.writer.write(self.password + '\n')

        prompt_str = await self.read_until(b'#')
        if prompt_str:
            logger.info(f"{self.host_ip}:{self.port} login successfully!")
            return True

        logger.error(f"{self.host_ip}:{self.port} login failed!")
        return False

    async def async_login_host_with_info(self):
        result = await self.async_login_host()
        return result, self.host_ip, self.port

    def login_host(self):
        return asyncio.run(self.async_login_host())


async def batch_check_host(devices, batch_size=10):
    results = []
    if len(devices) <= batch_size:
        tasks = [TelnetClient(host, port, username, password).async_login_host_with_info() for
                 host, port, username, password in devices]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results

    for i in range(0, len(devices), batch_size):
        tasks = [TelnetClient(host, port, username, password).async_login_host_with_info() for
                 host, port, username, password in devices[i: i + batch_size]]
        results += await asyncio.gather(*tasks, return_exceptions=True)
    return results

