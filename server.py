import configparser
import misc
import sys
import db
from resolver import DHCPDeclineResolver, DHCPDiscoverResolver, \
                     DHCPInformResolver, DHCPReleaseResolver, \
                     DHCPReleaseResolver, DHCPRequestResolver
from socket import socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, \
                   SO_REUSEPORT, SOL_IP, IP_MULTICAST_TTL, IP_MULTICAST_LOOP, \
                   IP_MULTICAST_IF, inet_aton, SHUT_RD, gethostbyname, gethostname, \
                   SO_BROADCAST

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
        self.db = db.InMemoryDHCPDatabase()
        self._setup()

    def _setup(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.socket.setsockopt(SOL_IP, IP_MULTICAST_TTL, 20)
        self.socket.setsockopt(SOL_IP, IP_MULTICAST_LOOP, 1)
    
    def _dispatch(self, data, addr):
        pack = misc.getGeneralPacket(data)
        resolver = {}
        print(pack)
        if pack['options']['messageType'] == 'DISCOVER':
            self.log.info('Processing DISCOVER message.')
            resolver = DHCPDiscoverResolver(pack, self.config, self.db)
            resolver.resolve()
        elif pack['options']['messageType'] == 'REQUEST':
            self.log.info('Processing REQUEST message.')
            resolver = DHCPRequestResolver(pack, self.config, self.db)
            resolver.resolve()
        elif pack['options']['messageType'] == 'DECLINE':
            self.log.info('Processing DECLINE message.')
            resolver = DHCPDeclineResolver(pack, self.config, self.db)
            resolver.resolve()
        elif pack['options']['messageType'] == 'RELEASE':
            self.log.info('Processing RELEASE message.')
            resolver = DHCPReleaseResolver(pack, self.config, self.db)
            resolver.resolve()
            return
        elif pack['options']['messageType'] == 'INFORM':
            self.log.info('Processing INFORM message.')
            resolver = DHCPInformResolver(pack, self.config, self.db)
            resolver.resolve()
        self._sendPacket(resolver.toBytes(), addr)
    
    def _sendPacket(self, data, addr):
        sendsock = socket(AF_INET, SOCK_DGRAM)
        sendsock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        sendsock.bind((self.config['zone']['server'], 0))
        sendsock.sendto(data, ('<broadcast>', 68))
        sendsock.close()

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

if __name__ == '__main__':
    print('This file is not intended to run separately. Run main.py file instead.')
