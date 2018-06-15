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
        bpacket = bytearray()
        bpacket.append(self.packet['op'])
        bpacket.append(self.packet['htype'])
        bpacket.append(self.packet['hlen'])
        bpacket.append(self.packet['hops'])
        print(type(self.packet['xid']))
        bpacket += self.packet['xid'].to_bytes(4, 'big')
        bpacket += self.packet['secs'].to_bytes(2, 'big')
        bpacket += self.packet['flags'].to_bytes(2, 'big')
        bpacket += self.packet['ciaddr'].to_bytes(4, 'big')
        bpacket += self.packet['yiaddr'].to_bytes(4, 'big')
        bpacket += self.packet['siaddr'].to_bytes(4, 'big')
        bpacket += self.packet['giaddr'].to_bytes(4, 'big')
        #bpacket += self.packet['chaddr'].to_bytes(16, 'big')
        bpacket += (0).to_bytes(16, 'big')
        bpacket += (0).to_bytes(192, 'big') # gap
        bpacket += self.packet['cookie'].to_bytes(4, 'big')
        # options
        print(bpacket)
        raise NotImplementedError('not, yet')

class DHCPDiscoverResolver(DHCPResolver): # DISCOVER -> OFFER
    def resolve(self):
        self.outpacket['options']['messageType'] = 2
        if self.db.isEmpty():
            self.outpacket['yiaddr'] = misc.ip2int(self.config['zone']['start'])
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
