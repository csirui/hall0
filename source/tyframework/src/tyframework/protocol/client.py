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


# UDP protocol for talk with other server...
class InternalUDPClientProtocol(DatagramProtocol):
    sendCount = 0
    receiveCount = 0

    BUFFERSIZE = 2 * 1024 * 1024

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.serverId = 0
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

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
            if self.__ctx__.ftlog.is_debug_net():
                ukey = '====== RECEIVE INTERAL UDP:' + str(self.gdata.serverId) + ':' + address[0] + ':' + str(
                    address[1]) + ':'
                self.__ctx__.ftlog.debug(ukey + str(len(data)) + ':' + data)
            udpId = self.__ctx__.MsgLine.getUdpId(data)
            if udpId in self.liveMessages:
                self.checkTableCall(data, 0)
                d, c = self.liveMessages[udpId]
                del self.liveMessages[udpId]
                c.cancel()
                d.callback(data)
            else:
                self.__ctx__.ftlog.error('\n' * 5)
                self.__ctx__.ftlog.error('ERROR', ukey, 'msg id not in live table:', data)
                self.__ctx__.ftlog.error('\n' * 5)
        except:
            self.__ctx__.ftlog.error('\n' * 5)
            self.__ctx__.ftlog.error("ERROR", ukey, 'data=', data)
            self.__ctx__.ftlog.exception()
            self.__ctx__.ftlog.error('\n' * 5)

    def getDebugKey(self):
        return '====== SEND_TO UDP:' + str(self.gdata.serverId) + ':' + str(self.host) + ':' + str(
            self.port) + ':' + str(self.serverId) + ':'

    def sendMessage(self, mo):
        message = mo.pack()
        self.sendMessage2(None, message)

    def checkTableCall(self, msg, issend):
        if msg.find('table_call') > 0:
            if issend:
                InternalUDPClientProtocol.sendCount += 1
                if InternalUDPClientProtocol.sendCount % 1000 == 0:
                    self.__ctx__.ftlog.info('InternalUDPClientProtocol table_call_table_call sendCount=',
                                            InternalUDPClientProtocol.sendCount)
            else:
                InternalUDPClientProtocol.receiveCount += 1
                if InternalUDPClientProtocol.receiveCount % 1000 == 0:
                    self.__ctx__.ftlog.info('InternalUDPClientProtocol table_call_table_call receiveCount=',
                                            InternalUDPClientProtocol.receiveCount)

    def sendMessage2(self, targets, message):
        try:
            if self.transport:
                data = self.__ctx__.MsgLine.packstr(0, targets, message)
                if self.__ctx__.ftlog.is_debug_net():
                    self.__ctx__.ftlog.debug(self.getDebugKey() + ':' + str(len(data)) + ':' + repr(data))
                self.checkTableCall(data, 1)
                self.transport.write(data, (self.host, self.port))
            else:
                self.__ctx__.ftlog.error('\n' * 5)
                self.__ctx__.ftlog.error('ERROR ====== INTERNAL UDP SEND: not connected !! self=', self)
                self.__ctx__.ftlog.error('\n' * 5)
        except Exception, e:
            self.__ctx__.ftlog.error('\n' * 5)
            self.__ctx__.ftlog.error('ERROR INTERNAL UDP:', self.getDebugKey(), unicode(e))
            self.__ctx__.ftlog.exception()
            self.__ctx__.ftlog.error('\n' * 5)

    def query(self, data, timeout, userids=None):
        try:
            if self.transport:
                udpId = self.__ctx__.MsgLine.nextUdpId()
                data = self.__ctx__.MsgLine.packstr(udpId, userids, data)
                if self.__ctx__.ftlog.is_debug_net():
                    self.__ctx__.ftlog.debug(self.getDebugKey() + repr(data))
                self.checkTableCall(data, 1)
                self.transport.write(data, (self.host, self.port))
                resultDeferred = defer.Deferred()
                cancelCall = reactor.callLater(timeout, self._clearFailed, resultDeferred, udpId, self.host, self.port,
                                               data)
                self.liveMessages[udpId] = (resultDeferred, cancelCall)
                temp = resultDeferred
                return temp
            else:
                self.__ctx__.ftlog.error('\n' * 5)
                self.__ctx__.ftlog.error('ERROR ====== INTERNAL UDP QUERY : not connected !! self=', self)
                self.__ctx__.ftlog.error('\n' * 5)
        except Exception, e:
            self.__ctx__.ftlog.error('\n' * 5)
            self.__ctx__.ftlog.error('ERROR INTERNAL UDP QUERY:', self.getDebugKey(), unicode(e))
            self.__ctx__.ftlog.exception()
            self.__ctx__.ftlog.error('\n' * 5)
        return None

    def _clearFailed(self, deferred, mid, host, port, data):
        try:
            del self.liveMessages[mid]
        except KeyError:
            pass
        self.__ctx__.ftlog.error('UDP TimeoutException of->', mid, host, port, data)
        deferred.errback(failure.Failure(self.__ctx__.TimeoutException(str(mid))))
