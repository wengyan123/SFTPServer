import logging
import json


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
    config = json.load(config_file)
    return config