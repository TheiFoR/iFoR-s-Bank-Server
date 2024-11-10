import sys

from new_types.package import Package

from logger import logger
import threading

from socket import socket
from utils.byteparser import ByteParser


class ClientCore(threading.Thread):
    _socket: socket = None
    _address = None
    message_handler: dict = None
    answer_to_message: dict = None

    def __init__(self, client_socket: socket, address):
        super().__init__()
        self._socket = client_socket
        self._address = address

    def run(self):
        logger.info(f'Client client - {self._address}')
        while True:
            data = self._socket.recv(4096)

            package: Package = ByteParser.parse(data)

            logger.debug(f'Client command id {package.id}, parameters: {package.data}. Raw data: {data}')

            if self.message_handler is None:
                logger.warning("Message handler is None")
                continue

            if not dict(self.message_handler).keys().__contains__(package.id):
                logger.warning("Message handler is not contains command_id: " + str(package.id))
                continue

            code, response = self.message_handler[package.id](self, package.data)

            byte_data = ByteParser.unparse(Package(code, response))
            logger.debug("Message to send: " + str(code) + " " + str(response))
            logger.debug("Message to send raw: " + str(byte_data))
            self.sendBytes(byte_data)

            if code == -1:
                break

        logger.info(f'Client disconnected, job complete')

    def sendBytes(self, data: bytes):
        self._socket.sendall(data)
