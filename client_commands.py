import client_handler
import database

from api.client import client
from user import User
from enums import code


def login(self: client_handler, parameters: dict):
    response = {}

    user = database.get_user(parameters[client.login.phone], parameters[client.login.pin])

    if user is None:
        response['code'] = client.enums.error
        response['message'] = 'Invalid phone number or pin code'

    return code.ok, response


def signup(self: client_handler, parameters: dict):
    response = {}

    database.set_user(parameters[client.signup.phone], parameters[client.signup.pin])

    return code.ok, response
