class DHCPResolver:
    def __init__(self, packet):
        self.packet = packet
        self.outpacket = {}

    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')

    def toBytes(self):
        raise NotImplementedError('not, yet')

class DHCPDiscoverResolver(DHCPResolver):
    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')


class DHCPRequestResolver(DHCPResolver):
    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')


class DHCPDeclineResolver(DHCPResolver):
    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')


class DHCPReleaseResolver(DHCPResolver):
    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')


class DHCPInformResolver(DHCPResolver):
    def resolve(self):
        raise NotImplementedError('This method has to be overrided.')
