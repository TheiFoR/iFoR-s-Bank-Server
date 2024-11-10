import json
import os
from logger import logger

from user import User


def _load() -> dict:
    file_path = "../database.json"

    try:
        # Check if the file exists; if not, create it
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump({}, file)  # Save an empty dictionary to the file
                logger.debug("File database.json created.")
                return {}

        with open(file_path, 'r+', encoding='utf-8') as file:
            try:
                # Read the contents of the file
                data = json.load(file)
                if not data:  # Check if the dictionary is empty
                    logger.debug("File is empty, returning an empty dictionary.")
                    return {}
                return data
            except json.JSONDecodeError:
                logger.error("JSON decoding error.")
                return {}
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Error: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {}


def get_user(login: bytes, password: bytes) -> User:
    user = User()

    database = _load()
    user_js = database.get(login)

    if user_js is None:
        return None

    return user
