import datetime
import json
import logging
import os
from utils import settings

_log_level_map = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "fatal": logging.FATAL,
}

_log_format = '%(asctime)s %(levelname)s %(message)s'
_log_level_str = settings.load('logger', 'log_level', 'info')
_log_level = logging.INFO

if _log_level_str in _log_level_map:
    _log_level = _log_level_map[_log_level_str]

logging.basicConfig(format=_log_format,
                    level=_log_level)

_log_path = settings.load('logger', 'logs_path_folder', 'logs')
_log_full_path = ''

os.makedirs(_log_path, exist_ok=True)
_time_now_str = datetime.datetime.now().strftime('%d-%m-%Y_%I-%M-%S %p')
_log_full_path = _log_path + '/log_' + '0' + '.json'


# try:
#     _log_file = open(_log_full_path, 'r+b')
#     _log_file.close()
# except:
#     _log_file = open(_log_full_path, 'w')
#     _log_file.write("")
#     _log_file.close()


def debug(msg, *args, **kwargs):
    _write_log(msg, "Debug")
    logging.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _write_log(msg, "Information")
    logging.info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    _write_log(msg, "Warning")
    logging.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _write_log(msg, "Error")
    logging.error(msg, *args, **kwargs)


def fatal(msg, *args, **kwargs):
    _write_log(msg, "Fatal")
    logging.fatal(msg, *args, **kwargs)


def _write_log(msg: str, level: str):
    data = {
        "@t": datetime.datetime.now().isoformat(),
        "@m": msg,
        "@l": level
    }
    with open(_log_full_path, 'a') as log_file:
        json.dump(data, log_file)
        log_file.write('\n')


if __name__ == 'logger.logger':
    info("Start a log file at the path: " + _log_full_path)
