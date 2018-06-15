import misc

class DHCPResolver:
    def __init__(self, packet, config, db):
        self.packet = packet
        self.config = config
        self.db = db
        self.outpacket = misc.getGeneralOutputPacket(packet['xid'], packet['cookie'])
        self.outpacket['siaddr'] = misc.ip2int(config['zone']['server'])
        # tmp yet
        self.outpacket['yiaddr'] = 0
        self.outpacket['ciaddr'] = 0
        self.outpacket['giaddr'] = 0

        self.outpacket['chaddr'] = packet['chaddr']
        self.outpacket['options']['netmask'] = misc.ip2int(config['zone']['netmask'])
        self.outpacket['options']['router']  = misc.ip2int(config['zone']['gateway'])
        self.outpacket['options']['lease'] = int(config['zone']['lease'])
        self.outpacket['options']['dhcpsrv'] = misc.ip2int(config['zone']['server'])
        self.outpacket['options']['dnssrvs'] = config['zone']['dns']

    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')

    def toBytes(self):
        bpacket = bytearray()
        bpacket.append(self.outpacket['op'])
        bpacket.append(self.outpacket['htype'])
        bpacket.append(self.outpacket['hlen'])
        bpacket.append(self.outpacket['hops'])
        bpacket += self.outpacket['xid'].to_bytes(4, 'big')
        bpacket += self.outpacket['secs'].to_bytes(2, 'big')
        bpacket += self.outpacket['flags'].to_bytes(2, 'big')
        bpacket += self.outpacket['ciaddr'].to_bytes(4, 'big')
        bpacket += self.outpacket['yiaddr'].to_bytes(4, 'big')
        bpacket += self.outpacket['siaddr'].to_bytes(4, 'big')
        bpacket += self.outpacket['giaddr'].to_bytes(4, 'big')
        bpacket += self.outpacket['chaddr'].replace(':', '').encode('ascii')
        bpacket += (0).to_bytes(10, 'big') # mac gap
        bpacket += (0).to_bytes(192, 'big') # gap
        bpacket += self.outpacket['cookie'].to_bytes(4, 'big')
        # options
        bpacket += self._optionsBytes()
        print(bpacket)
        return bpacket
    
    def _optionsBytes(self):
        bopts = bytearray()
        for key, val in self.outpacket['options'].items():
            print(key)
            print(val)
            print(type(val))
            if key == 'messageType':
                bopts.append(53)
                bopts.append(1)
                bopts.append(val)
            if key == 'netmask':
                bopts.append(1)
                bopts.append(4)
                val.to_bytes(4, 'big')
            if key == 'router':
                bopts.append(1)
                bopts.append(4)
                val.to_bytes(4, 'big')
            if key == 'lease':
                bopts.append(51)
                bopts.append(4)
                val.to_bytes(4, 'big')
            if key == 'dns':
                ips = val.split(',')
                bopts.append(6)
                bopts.append(len(ips)*4)
                for dns in ips:
                    bopts.append(misc.ip2int(dns))
                
        return bopts

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
