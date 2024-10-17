import client_commands

from user import User

from api.client import client
from TCPConnection.Server.client_handler import BaseClientHandler


class ClientHandler(BaseClientHandler):

    def __init__(self, client_socket, address):
        super(ClientHandler, self).__init__(client_socket, address)
        self._user = User()

        self.message_handler = {
            client.login.id: client_commands.login,
            client.signup.id: client_commands.signup
        }
