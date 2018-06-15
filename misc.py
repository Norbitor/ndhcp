import logging
import sys
import ipaddress

def getLogger(name):
    log = logging.getLogger(name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('[%(levelname)s] %(asctime)s '\
                                           '(%(module)s.%(name)s) %(message)s'))
    handler.setLevel(logging.INFO)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    return log

def getGeneralPacket(data):
    packet = {}
    packet['op']      = data[0]
    packet['htype']   = data[1]
    packet['hlen']    = data[2]
    packet['hops']    = data[3]
    packet['xid']     = int.from_bytes(data[4:8], 'big')
    packet['secs']    = int.from_bytes(data[8:10], 'big')
    packet['flags']   = int.from_bytes(data[10:12], 'big')
    packet['ciaddr']  = int.from_bytes(data[12:16], 'big')
    packet['yiaddr']  = int.from_bytes(data[16:20], 'big')
    packet['siaddr']  = int.from_bytes(data[20:24], 'big')
    packet['giaddr']  = int.from_bytes(data[24:28], 'big')
    packet['chaddr']  = ":".join('{:02x}'.format(x) for x in data[28:28+packet['hlen']])
    packet['gap']     = int.from_bytes(data[44:236], 'big')
    packet['cookie']  = int.from_bytes(data[236:240], 'big')
    packet['options'] = resolveOptions(data[240:])
    return packet

def getGeneralOutputPacket(xid, cookie):
    packet = {}
    packet['op']      = 2
    packet['htype']   = 1
    packet['hlen']    = 6
    packet['hops']    = 0
    packet['xid']     = xid
    packet['secs']    = 0
    packet['flags']   = 0
    packet['ciaddr']  = 0
    packet['giaddr']  = 0
    packet['cookie']  = cookie
    packet['options'] = {}
    return packet

def ip2int(addr):
    return int(ipaddress.IPv4Address(addr))

def int2ip(addr):
    return str(ipaddress.IPv4Address(addr))

def resolveOptions(options):
    opts = {}
    opts['other'] = 0
    while len(options) > 0:
        opt = options[0]
        if opt == 0 or opt == 255:
            options = options[1:]
            continue
        length = options[1]
        if length == 1:
            val = options[2]
        else:
            val = int.from_bytes(options[2:2+length], 'big')
        if opt == 53:
            opts['messageType'] = {
                1: 'DISCOVER',
                2: 'OFFER',
                3: 'REQUEST',
                4: 'DECLINE',
                5: 'ACK',
                6: 'NAK',
                7: 'RELEASE',
                8: 'INFORM'
            }[val]
        else:
            opts['other'] += 1

        options = options[1+length:]
    
    return opts


if __name__ == '__main__':
    print('This file is not intended to run separately. Run main.py file instead.')
