from configparser import ConfigParser

_config = ConfigParser()
_config.read('config/config.ini')


def get(option, section='DEFAULT'):
    return _config[section.upper()][option]
