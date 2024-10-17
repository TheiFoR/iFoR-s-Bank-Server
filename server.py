import logger
import settings
import socket
from client_handler import ClientHandler

class Server:
    _section = 'server'

    _ip = '127.0.0.1'
    _port = 1310
    _server_socket = None

    _client_list = []

    def __init__(self, ):
        logger.debug("Server has been created")
        self._ip = settings.load(self._section, 'ip', self._ip)
        self._port = settings.load(self._section, 'port', self._port)

    def start(self):
        _server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _server_socket.bind((self._ip, self._port))
        logger.info("The server was started - " + str(self._ip) + ":" + str(self._port))
        _server_socket.listen(1)
        logger.info("The server is waiting for new connections")
        while True:
            client_socket, client_address = _server_socket.accept()
            logger.info("New client connections! " + str(client_address))

            client_handler = ClientHandler(client_socket, client_address)
            client_handler.start()

            self._client_list.append(client_handler)
