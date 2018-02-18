import logging
import json
import os

def createLogger(debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(name)s %(levelname)s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(name)s %(levelname)s %(message)s')
    _logger = logging.getLogger('SFTPServer')
    return _logger


def loadConfig(config_file):
    with open(config_file, 'r') as fp:
        config = json.load(fp)
        return config


def setServerRootDir(value):
    settings = os.path.dirname(os.path.abspath(__file__)) + '/settings.py'
    settings_list = []
    with open(settings, 'r+') as frw:
        for line in frw:
            if line.startswith('SERVER_ROOT_DIR'):
                line = "SERVER_ROOT_DIR = '" + value + "'"
            settings_list.append(line)
        frw.seek(0)
        frw.writelines(settings_list)