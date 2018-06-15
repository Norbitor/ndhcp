import misc

class DHCPResolver:
    def __init__(self, packet, config, db):
        self.packet = packet
        self.config = config
        self.db = db
        self.outpacket = misc.getGeneralOutputPacket(packet['xid'], packet['cookie'])
        self.outpacket['siaddr'] = misc.ip2int(config['zone']['server'])
        self.outpacket['chaddr'] = packet['chaddr']
        self.outpacket['options']['netmask'] = misc.ip2int(config['zone']['netmask'])
        self.outpacket['options']['router']  = misc.ip2int(config['zone']['gateway'])
        self.outpacket['options']['lease'] = config['zone']['lease']
        self.outpacket['options']['dhcpsrv'] = misc.ip2int(config['zone']['server'])
        self.outpacket['options']['dnssrvs'] = config['zone']['dns']

    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')

    def toBytes(self):
        raise NotImplementedError('not, yet')

class DHCPDiscoverResolver(DHCPResolver): # DISCOVER -> OFFER
    def resolve(self):
        self.outpacket['options']['messageType'] = 2
        print(self.outpacket)


class DHCPRequestResolver(DHCPResolver): # REQUEST -> ACK
    def resolve(self):
        self.outpacket['options']['messageType'] = 5
        print(self.outpacket)


class DHCPDeclineResolver(DHCPResolver):
    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')


class DHCPReleaseResolver(DHCPResolver):
    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')


class DHCPInformResolver(DHCPResolver):
    def resolve(self):
        self.outpacket['options']['messageType'] = 5
        print(self.outpacket)
        
