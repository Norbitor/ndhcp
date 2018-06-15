import time
import misc

class DHCPDatabase:
    def getClient(self, mac):
        raise NotImplementedError("The getClient method has to be overrided.")
    def addClient(self, mac, ip, lease_time=None):
        raise NotImplementedError("The addClient method has to be overrided.")
    def deleteClient(self, mac):
        raise NotImplementedError("The deleteClient method has to be overrided.")
    def cleanup(self):
        raise NotImplementedError("The cleanup method has to be overrided.")

class InMemoryDHCPDatabase(DHCPDatabase):
    def __init__(self):
        self.client_list = []
        self.log = misc.getLogger(__class__.__name__)
    
    def getClient(self, mac):
        try:
            client = next(filter(lambda cli: cli[0] == mac, self.client_list))
            return client
        except StopIteration:
            return None

    def addClient(self, mac, ip, lease_time=None):
        self.client_list.append((mac, ip, lease_time))
    
    def deleteClient(self, mac):
        client = self.getClient(mac)
        if client:
            self.client_list.remove(client)
        else:
            self.log.warning("Entry for MAC " + mac + " not found")

    def isEmpty(self):
        return True if len(self.client_list) == 0 else False
    
    def cleanup(self):
        curtime = time.time()
        self.client_list = filter(lambda cli: cli[2] == None or cli[2] > curtime, self.client_list)

if __name__ == '__main__':
    print('This file is not intended to run separately. Run main.py file instead.')
