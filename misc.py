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

if __name__ == '__main__':
    print('This file is not intended to run separately. Run main.py file instead.')
