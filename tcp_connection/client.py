from data import database

from user import User
from enums.handler import code

from api.client import client
from tcp_connection.client_core import ClientCore


class Client(ClientCore):

    def __init__(self, client_socket, address):
        super(Client, self).__init__(client_socket, address)
        self._user = User()

        self.message_handler = {
            client.login.id: self.login,
            client.signup.id: self.signup
        }

    def login(self, core: ClientCore, parameters: dict) -> (int, dict):
        response = {}

        user = database.get_user(parameters[client.login.phone], parameters[client.login.pin])

        if user is None:
            response['code'] = client.code.error
            response['message'] = 'Invalid phone number or pin code'

        return code.ok, response

    def signup(self, core: ClientCore, parameters: dict):
        response = {}

        database.set_user(parameters[client.signup.phone], parameters[client.signup.pin])

        return code.ok, response
