import sys

from tcp_connection.client_core import ClientCore

from logger import logger
import socket


class Server:
    _ip = '127.0.0.1'
    _port = 1310

    _client_list = []

    _server_socket = None

    client: ClientCore = None

    def __init__(self, ip, port, client):
        self._ip = ip
        self._port = port
        self.client = client

    def start(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._ip, self._port))
        logger.info("The server was started - " + str(self._ip) + ":" + str(self._port))
        self._server_socket.listen(1)
        logger.info("The server is waiting for new connections")
        while True:
            client_socket, client_address = self._server_socket.accept()
            logger.info("New client connections! " + str(client_address))

            client = self.client(client_socket, client_address)
            client.start()

            self._client_list.append(client)
