import configparser
import misc
import sys

class DHCPServer:
    def __init__(self):
        self.log = misc.getLogger(__class__.__name__)
        self.log.info('Starting DHCP server initialization...')
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        if not self.config.sections():
            self.log.critical("Configuration file not found or its invalid. " \
                              "Please provide correct config.ini file.")
            sys.exit(-1)

class DHCPResolver:
    pass

if __name__ == '__main__':
    print('This file is not intended to run separately. Run main.py file instead.')
