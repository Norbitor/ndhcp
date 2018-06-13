import configparser
import misc
import sys
from socket import *

class DHCPServer:
    def __init__(self):
        self.log = misc.getLogger(__class__.__name__)
        self.log.info('Starting DHCP server initialization...')
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        if not self.config.sections():
            self.log.critical('Configuration file not found or its invalid. ' \
                              'Please provide correct config.ini file.')
            sys.exit(-1)
        self.log.info('Configuration loaded successfully')
        self.process = True
        self._setup()

    def _setup(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.socket.setsockopt(SOL_IP, IP_MULTICAST_TTL, 20)
        self.socket.setsockopt(SOL_IP, IP_MULTICAST_LOOP, 1)
        self.socket.setsockopt(SOL_IP, IP_MULTICAST_IF, inet_aton(gethostbyname(gethostname())))
    
    def _dispatch(self, data, addr):
        pack = misc.getGeneralPacket(data)
        print(pack)

    def listen(self):
        self.socket.bind(('', 67))
        self.log.info('Sever started. Waiting for connections...')
        while self.process:
            data, client_addr = self.socket.recvfrom(1024)
            self.log.info("Received broadcast message on port 67")
            self._dispatch(data, client_addr)
        self.socket.close()

    def shutdown(self):
        self.log.info("Gracefully stopping listening...")
        try:
            self.socket.shutdown(SHUT_RD)
        except OSError:
            pass
        self.log.info("Server stopped.")

class DHCPResolver:
    pass

if __name__ == '__main__':
    print('This file is not intended to run separately. Run main.py file instead.')
