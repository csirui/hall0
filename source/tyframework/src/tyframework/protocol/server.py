# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 13时57分46秒
# FileName:      server.py
# Class:         PolicyTCPServerProtocol, BasicTCPServerProtocol, 
#                GameTCPServerProtocol, LoginTCPServerProtocol,
#                GameServerInfoUDPServerProtocol,
#                ReceiptUDPServerProtocol

import stackless
from twisted.internet import reactor

from tyframework.protocol.basic import BasicTCPServerProtocol
from tyframework.protocol.basic import BasicTCPZipServerProtocol
from tyframework.protocol.basic import BasicUDPServerProtocol
from tyframework.tasklet.httpudp import HttpUdpTasklet
from tyframework.tasklet.manager import ManagerTasklet

ConnTasklet = None
AccountTasklet = None
EntityTasklet = None
GameTasklet = None
HeartBeatTasklet = None
QuickStartTasklet = None
ConnBridgeTasklet = None


def _init_game_tasklets_():
    '''
    再framework结构过渡期,SDK工程无法引用游戏工程的内容,
    后期framework的机构将与目前HTTP服务的结构类似, 即可避免跨工程引用的问题
    '''
    global ConnTasklet
    global AccountTasklet
    global EntityTasklet
    global GameTasklet
    global HeartBeatTasklet
    global QuickStartTasklet
    global ConnBridgeTasklet
    from freetime.tasklet.conn import ConnTasklet as ConnTasklet_
    from freetime.tasklet.conn_bridge import ConnBridgeTasklet as ConnBridgeTasklet_
    from freetime.tasklet.account import AccountTasklet as AccountTasklet_
    from freetime.tasklet.entity import EntityTasklet as EntityTasklet_
    from freetime.tasklet.game import GameTasklet as GameTasklet_
    from freetime.tasklet.heartbeat import HeartBeatTasklet as HeartBeatTasklet_
    from freetime.tasklet.quickstart import QuickStartTasklet as QuickStartTasklet_
    ConnTasklet = ConnTasklet_
    AccountTasklet = AccountTasklet_
    EntityTasklet = EntityTasklet_
    GameTasklet = GameTasklet_
    HeartBeatTasklet = HeartBeatTasklet_
    QuickStartTasklet = QuickStartTasklet_
    ConnBridgeTasklet = ConnBridgeTasklet_


class ConnTCPSrvProtocol(BasicTCPServerProtocol):
    def makeTasklet(self, reqmsg):
        return ConnTasklet(self.gdata, reqmsg, self, None, None)


class ConnTCPSrvZipProtocol(BasicTCPZipServerProtocol):
    def makeTasklet(self, reqmsg):
        return ConnTasklet(self.gdata, reqmsg, self, None, None)


class ConnTCPSrvBridgeProtocol(BasicTCPServerProtocol):
    def makeTasklet(self, reqmsg):
        return ConnBridgeTasklet(self.gdata, reqmsg, self, None, None)

    def connectionLost(self, reason):
        from tyframework.protocol.basic import TcpProtocolHelper
        TcpProtocolHelper.connectionLost(self, reason)
        from freetime.tasklet.conn_bridge import delBridgeProtocols
        delBridgeProtocols(self)

    def lineReceived(self, data):
        from tyframework.context import TyContext
        try:
            if TyContext.ftlog.is_debug_net():
                TyContext.ftlog.debug('====== BRIDGE RECEIVE ', self._key, self.userId, data)
            msgline = TyContext.MsgLine(0, None, data)
            c = self.makeTasklet(msgline)
            stackless.tasklet(c.tasklet)()
        except Exception, e:
            TyContext.ftlog.error('\n' * 5)
            TyContext.ftlog.error("ERROR ======BRIDGE RECEIVE ", e)
            TyContext.ftlog.exception()
            TyContext.ftlog.error('\n' * 5)
            self.transport.write(TyContext.MsgPack.makeErrorString('error pack'))
            self.transport.loseConnection()

        reactor.callLater(0.0, stackless.schedule)


class ConnUDPSrvProtocol(BasicUDPServerProtocol):
    def makeTasklet(self, reqmsg, protocol, address):
        return ConnTasklet(self.gdata, reqmsg, None, self, address)


class AccountUDPSrvProtocol(BasicUDPServerProtocol):
    def makeTasklet(self, reqmsg, protocol, address):
        return AccountTasklet(self.gdata, reqmsg, self, address)


class EntityUdpSvrProtocol(BasicUDPServerProtocol):
    def makeTasklet(self, reqmsg, protocol, address):
        return EntityTasklet(self.gdata, reqmsg, self, address)


class GameUdpSvrProtocol(BasicUDPServerProtocol):
    def makeTasklet(self, reqmsg, protocol, address):
        return GameTasklet(self.gdata, reqmsg, self, address)


class HeartBeatUdpSvrProtocol(BasicUDPServerProtocol):
    def makeTasklet(self, reqmsg, protocol, address):
        return HeartBeatTasklet(self.gdata, reqmsg, self, address)


class QuickStartUdpSvrProtocol(BasicUDPServerProtocol):
    def makeTasklet(self, reqmsg, protocol, address):
        return QuickStartTasklet(self.gdata, reqmsg, self, address)


class ManagerUdpSvrProtocol(BasicUDPServerProtocol):
    def makeTasklet(self, reqmsg, protocol, address):
        return ManagerTasklet(self.gdata, reqmsg, self, address)


class HttpUdpSvrProtocol(BasicUDPServerProtocol):
    def makeTasklet(self, reqmsg, protocol, address):
        return HttpUdpTasklet(self.gdata, reqmsg, self, address)
