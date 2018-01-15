# -*- coding=utf-8 -*-

import platform
import sys
import time

import stackless

from tyframework._private_.util.ftlog import ftlog


class tychannel(object):
    '''
    FAKE of stackless, when eclipse problems notice
    '''

    def receive(self):
        pass


class tybomb(Exception):
    '''
    FAKE of stackless, when eclipse problems notice
    '''

    def __init__(self, ntype, value):
        pass


def tygetcurrent():
    '''
    FAKE of stackless, when eclipse problems notice
    '''
    return 0


def initepollreactor():
    t1 = time.time()
    ftlog.info('initepollreactor begin')
    try:
        if platform.system() == 'Darwin':
            from twisted.internet import reactor
        else:
            from twisted.internet import epollreactor
            epollreactor.install()
    except:
        ftlog.exception('epoll reactor installed fail, not linux?')
    ftlog.info('initepollreactor done, use time ', time.time() - t1)

    ftlog.info(sys.modules['twisted.internet.reactor'])

    global tybomb, tychannel, tygetcurrent
    tybomb = getattr(stackless, 'bomb')
    tychannel = getattr(stackless, 'channel')
    tygetcurrent = getattr(stackless, 'getcurrent')
    ftlog.tygetcurrent = tygetcurrent
