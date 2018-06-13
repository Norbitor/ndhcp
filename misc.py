import logging
import sys

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
    d = {}
    d['op']      = data[0]
    d['htype']   = data[1]
    d['hlen']    = data[2]
    d['hops']    = data[3]
    d['xid']     = int.from_bytes(data[4:8], 'big')
    d['secs']    = int.from_bytes(data[8:10], 'big')
    d['flags']   = int.from_bytes(data[10:12], 'big')
    d['ciaddr']  = int.from_bytes(data[12:16], 'big')
    d['yiaddr']  = int.from_bytes(data[16:20], 'big')
    d['siaddr']  = int.from_bytes(data[20:24], 'big')
    d['giaddr']  = int.from_bytes(data[24:28], 'big')
    d['chaddr']  = ":".join('{:02x}'.format(x) for x in data[28:28+d['hlen']])
    d['gap']     = int.from_bytes(data[44:236], 'big')
    d['options'] = data[240:]
    return d

def resolveOptions(options):
    out = {}
    return out

if __name__ == '__main__':
    print('This file is not intended to run separately. Run main.py file instead.')
