import logger
import configparser

_file_path = "config.ini"

_config = configparser.ConfigParser()


def save(section: str, key: str, value):
    if not _config.has_section(section):
        _config.add_section(section)
    _config.set(section, key, str(value))

    with open(_file_path, 'w') as config_file:
        _config.write(config_file)


def load(section: str, key: str, value):
    data_type = type(value)
    if section in _config and key in _config[section]:
        result = data_type(_config.get(section, key))
    else:
        result = None

    if result == None:
        result = data_type(value)
        save(section, key, value)

    return result


if __name__ == 'settings':
    global section

    try:
        config_file = open(_file_path, 'x')
        config_file.close()
    except FileExistsError:
        pass

    _config.read(_file_path)
