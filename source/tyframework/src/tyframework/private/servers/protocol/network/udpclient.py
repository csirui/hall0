# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 13时56分15秒
# FileName:      client.py
# Class:         InternalUDPClientProtocol

import socket

from twisted.internet import defer, reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.python import failure

from tyframework.context import TyContext


# UDP protocol for talk with other server...
class InternalUDPClientProtocol(DatagramProtocol):
    sendCount = 0
    receiveCount = 0

    BUFFERSIZE = 2 * 1024 * 1024

    def __init__(self):
        pass

    def startProtocol(self):
        self.liveMessages = {}
        sock = self.transport.getHandle()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFFERSIZE)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.BUFFERSIZE)

    def stopProtocol(self):
        self.liveMessages = {}

    def datagramReceived(self, data, address):
        ukey = ''
        try:
            if TyContext.ftlog.is_debug_net():
                ukey = '====== RECEIVE INTERAL UDP:' + address[0] + ':' + str(address[1]) + ':'
                TyContext.ftlog.debug(ukey + str(len(data)) + ':' + data)
            udpId = TyContext.MsgLine.getUdpId(data)
            if udpId in self.liveMessages:
                self.checkTableCall(data, 0)
                d, c = self.liveMessages[udpId]
                del self.liveMessages[udpId]
                c.cancel()
                d.callback(data)
            else:
                TyContext.ftlog.error('\n' * 5)
                TyContext.ftlog.error('ERROR', ukey, 'msg id not in live table:', data)
                TyContext.ftlog.error('\n' * 5)
        except:
            TyContext.ftlog.error('\n' * 5)
            TyContext.ftlog.error("ERROR", ukey, address, 'data=', data)
            TyContext.ftlog.exception()
            TyContext.ftlog.error('\n' * 5)

    def getDebugKey(self, serverId, toaddress):
        return '====== SEND_TO UDP:' + str(serverId) + ':' + str(toaddress[0]) + ':' + str(toaddress[1]) + ':'

    def checkTableCall(self, msg, issend):
        if msg.find('table_call') > 0:
            if issend:
                InternalUDPClientProtocol.sendCount += 1
                if InternalUDPClientProtocol.sendCount % 1000 == 0:
                    TyContext.ftlog.info('InternalUDPClientProtocol table_call_table_call sendCount=',
                                         InternalUDPClientProtocol.sendCount)
            else:
                InternalUDPClientProtocol.receiveCount += 1
                if InternalUDPClientProtocol.receiveCount % 1000 == 0:
                    TyContext.ftlog.info('InternalUDPClientProtocol table_call_table_call receiveCount=',
                                         InternalUDPClientProtocol.receiveCount)

    def sendMessage2(self, targets, message, serverId, toaddress):
        try:
            if self.transport:
                data = TyContext.MsgLine.packstr(0, targets, message)
                if TyContext.ftlog.is_debug_net():
                    TyContext.ftlog.debug(
                        self.getDebugKey(serverId, toaddress) + ':' + str(len(data)) + ':' + repr(data))
                self.checkTableCall(data, 1)
                self.transport.write(data, toaddress)
            else:
                TyContext.ftlog.error('\n' * 5)
                TyContext.ftlog.error('ERROR ====== INTERNAL UDP SEND: not connected !! self=', self)
                TyContext.ftlog.error('\n' * 5)
        except Exception, e:
            TyContext.ftlog.error('\n' * 5)
            TyContext.ftlog.error('ERROR INTERNAL UDP:', self.getDebugKey(serverId, toaddress), unicode(e))
            TyContext.ftlog.exception()
            TyContext.ftlog.error('\n' * 5)

    def query(self, data, timeout, serverId, toaddress, userids=None):
        try:
            if self.transport:
                udpId = TyContext.MsgLine.nextUdpId()
                data = TyContext.MsgLine.packstr(udpId, userids, data)
                if TyContext.ftlog.is_debug_net():
                    TyContext.ftlog.debug(self.getDebugKey(serverId, toaddress) + repr(data))
                self.checkTableCall(data, 1)
                self.transport.write(data, toaddress)
                resultDeferred = defer.Deferred()
                cancelCall = reactor.callLater(timeout, self._clearFailed, resultDeferred, udpId, toaddress, data)
                self.liveMessages[udpId] = (resultDeferred, cancelCall)
                temp = resultDeferred
                return temp
            else:
                TyContext.ftlog.error('\n' * 5)
                TyContext.ftlog.error('ERROR ====== INTERNAL UDP QUERY : not connected !! self=', self)
                TyContext.ftlog.error('\n' * 5)
        except Exception, e:
            TyContext.ftlog.error('\n' * 5)
            TyContext.ftlog.error('ERROR INTERNAL UDP QUERY:', self.getDebugKey(serverId, toaddress), unicode(e))
            TyContext.ftlog.exception()
            TyContext.ftlog.error('\n' * 5)
        return None

    def _clearFailed(self, deferred, mid, toaddress, data):
        try:
            del self.liveMessages[mid]
        except KeyError:
            pass
        TyContext.ftlog.error('UDP TimeoutException of->', mid, toaddress, data)
        deferred.errback(failure.Failure(TyContext.TimeoutException(str(mid))))


class UDPClientProxy():
    def __init__(self, serverId, host, port, udpClient):
        self.serverId = serverId
        self.toaddress = (host, port)
        self.udpClient = udpClient

    def sendMessage(self, mo):
        message = mo.pack()
        self.udpClient.sendMessage2(None, message, self.serverId, self.toaddress)

    def sendMessage2(self, targets, message):
        return self.udpClient.sendMessage2(targets, message, self.serverId, self.toaddress)

    def query(self, data, timeout, userids=None):
        return self.udpClient.query(data, timeout, self.serverId, self.toaddress, userids)
