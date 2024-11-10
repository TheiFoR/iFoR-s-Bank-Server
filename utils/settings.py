import configparser

_file_path = "config.ini"

_config = configparser.ConfigParser()


def save(section: str, key: str, value):
    if not _config.has_section(section):
        _config.add_section(section)
    _config.set(section, key, str(value))

    with open(_file_path, 'w') as config_file:
        _config.write(config_file)


def load(section: str, key: str, default_value):
    data_type = type(default_value)
    if section in _config and key in _config[section]:
        result = data_type(_config.get(section, key))
    else:
        result = None

    if result == None:
        result = data_type(default_value)
        save(section, key, default_value)

    return result


if __name__ == 'utils.settings':
    global section

    try:
        config_file = open(_file_path, 'x')
        config_file.close()
    except FileExistsError:
        pass

    _config.read(_file_path)
