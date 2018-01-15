# -*- coding=utf-8 -*-

import socket

from twisted.internet.protocol import DatagramProtocol

from tyframework.context import TyContext
from tyframework.private.servers.protocol.tytasklet.helper import TaskletHelper


class UDPLineServerProtocol(DatagramProtocol):
    BUFFERSIZE = 2 * 1024 * 1024

    def startProtocol(self):
        sock = self.transport.getHandle()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFFERSIZE)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.BUFFERSIZE)

    def datagramReceived(self, data, address):
        try:
            TyContext.ftlog.debug_net('====== RECEIVE UDP:<--', address, data)
            msgline = TyContext.MsgLine.unpack(data)
            tasklet = self.makeTasklet(msgline, address)
            TaskletHelper.asyncTasklet(tasklet)
        except Exception, e:
            TyContext.ftlog.exception('====== ERROR RECEIVE UDP:', address, e, data)

    def sendMessage(self, msg, address, userId=None):
        try:
            data = TyContext.MsgLine.packstr(0, userId, msg)
            TyContext.ftlog.debug_net('====== SEND', address, data)
            self.transport.write(data, address)
        except Exception, e:
            TyContext.ftlog.exception('====== ERROR SEND', address, e, msg)

    def makeTasklet(self, msgline, address):
        raise NotImplementedError
