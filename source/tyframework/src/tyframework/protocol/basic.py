# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 13时57分46秒
# FileName:      server.py
# Class:         PolicyTCPServerProtocol, BasicTCPServerProtocol,
#                GameTCPServerProtocol, LoginTCPServerProtocol,
#                GameServerInfoUDPServerProtocol,
#                ReceiptUDPServerProtocol

import random
import socket
import stackless
import zlib

from twisted.internet import protocol
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.protocols.basic import LineReceiver

from tyframework.context import TyContext


class _PauseableMixinZip:
    paused = False

    def pauseProducing(self):
        self.paused = True
        self.transport.pauseProducing()

    def resumeProducing(self):
        self.paused = False
        self.transport.resumeProducing()
        self.dataReceived('')

    def stopProducing(self):
        self.paused = True
        self.transport.stopProducing()


class ZipLineReceiver(protocol.Protocol, _PauseableMixinZip):
    __buffer = ''

    def __init__(self):
        self._key = ''

    def clearLineBuffer(self):
        b = self.__buffer
        self.__buffer = ""
        return b

    def dataReceived(self, data):
        self.__buffer = self.__buffer + data
        dlen = len(self.__buffer)
        while dlen > 4 and not self.paused:
            mlen = self.__buffer[0:4]
            try:
                mlen = int(mlen, 16)
            except:
                TyContext.ftlog.error('ERROR ZIP HEAD LENGTH !', self, mlen)
                self.transport.loseConnection()
                return

            if dlen < mlen + 4:
                return
            line = self.__buffer[:(mlen + 4)]
            if mlen + 4 == dlen:
                self.__buffer = ''
            else:
                self.__buffer = self.__buffer[(mlen + 4):]
            why = self.lineReceived(line)
            if why or self.transport and self.transport.disconnecting:
                return why
            dlen = len(self.__buffer)
        #         else:
        #             if not self.paused:
        #                 data = self.__buffer
        #                 self.__buffer = ''
        #                 if data:
        #                     return self.rawDataReceived(data)

    def lineReceived(self, line):
        raise NotImplementedError


class TcpProtocolHelper():
    @classmethod
    def connectionMade(cls, protocol):
        protocol.MAX_LENGTH = 65536
        protocol.host = str(protocol.transport.getPeer().host)
        protocol.port = str(protocol.transport.getPeer().port)
        protocol._key = 'TCP:' + str(protocol.gdata.serverId) + ':' + protocol.host + ':' + protocol.port + ':'
        protocol.transport.setTcpNoDelay(1)
        protocol.transport.setTcpKeepAlive(1)
        try:
            protocol.transport.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 180)
            protocol.transport.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 30)
            protocol.transport.socket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 10)
        except Exception, e:
            TyContext.ftlog.debug('not support TCP_KEEPIDLE')
        protocol.isConnected = True
        protocol.userId = 0
        protocol.timeOutCount = 0
        protocol.heart_beat_count = 0
        newps = protocol.gdata.new_protocols
        if not protocol in newps:
            newps[protocol] = protocol
        TyContext.ftlog.info('ConnectionMade key=', protocol._key, 'new_protocols length=', len(newps))

    @classmethod
    def connectionLost(cls, protocol, reason):
        try:
            if protocol.isConnected == True:
                protocol.isConnected = False
                TyContext.ftlog.info('ConnectionLost key=', protocol._key,
                                     'userId=', protocol.userId, 'reason=', reason)
                if protocol.userId > 0:
                    uid = protocol.userId
                    if uid in protocol.gdata.usermap:
                        msg = '{"cmd":"conn_lost","params":{"userId":%d}}\n\0' % (uid)
                        cls.lineReceived(protocol, msg)
                    else:
                        TyContext.ftlog.error('not found userid in UserTable on connection lost event...')
                elif protocol.userId == -1:
                    pass
                else:
                    if TyContext.ftlog.is_debug_net():
                        TyContext.ftlog.debug('empty user connection lost ... ', protocol)

        except Exception, e:
            TyContext.ftlog.error('CONNECTION_LOST_ERROR: ', e)
            TyContext.ftlog.exception()

        if protocol in protocol.gdata.new_protocols:
            del protocol.gdata.new_protocols[protocol]

    @classmethod
    def lineReceived(cls, protocol, data):
        try:
            if TyContext.ftlog.is_debug_net():
                TyContext.ftlog.debug('====== RECEIVE ', protocol._key, protocol.userId, data)
            msgline = TyContext.MsgLine(0, None, data)
            """
            if msgline.cmd == 'heart_beat' :
                uhc = protocol.heart_beat_count + 1
                protocol.heart_beat_count = uhc
                if uhc % HEART_BEAT_RECIVE_MOD == 0 :
                    return
            """
            c = protocol.makeTasklet(msgline)
            stackless.tasklet(c.tasklet)()
        except Exception, e:
            TyContext.ftlog.error('\n' * 5)
            TyContext.ftlog.error("ERROR ====== RECEIVE ", e)
            TyContext.ftlog.exception()
            TyContext.ftlog.error('\n' * 5)
            protocol.transport.write(TyContext.MsgPack.makeErrorString('error pack'))
            protocol.transport.loseConnection()

        reactor.callLater(0.0, stackless.schedule)

    @classmethod
    def sendTcpMessage(cls, protocol, msg, is_heart_beat_reply=False):
        """ @param is_heart_beat_reply
        表示msg是否是对客户端heart_beat消息的回应
        """
        if is_heart_beat_reply:
            msg = '0000'
        try:
            if protocol.transport and protocol.isConnected:
                protocol.transport.write(msg)
                return True
            else:
                TyContext.ftlog.error('\n' * 5)
                TyContext.ftlog.error('ERROR ====== SEND_TO : not connected !! protocol=', protocol)
                TyContext.ftlog.error('\n' * 5)
        except Exception, e:
            TyContext.ftlog.error('\n' * 5)
            TyContext.ftlog.error('ERROR ====== SEND_TO :', e)
            TyContext.ftlog.exception()
            TyContext.ftlog.error('\n' * 5)
        return False


# Basic tcp protocol...
class BasicTCPZipServerProtocol(ZipLineReceiver):
    def tycode(self, seed, datas):
        return TyContext.strutil.tycode(seed, datas)

    def ty_encode(self, srcstr):
        #         if srcstr.find('"gameId"') < 0 :
        #             TyContext.ftlog.error('')
        #             TyContext.ftlog.error('ERRRRRRRRR !!! this message has no gameId !', srcstr)
        #             TyContext.ftlog.error('')
        zstr = zlib.compress(srcstr)
        dlen = len(zstr)
        tstr = '%04X' % dlen
        czstr = self.tycode(self.session_seed + dlen, zstr)
        return tstr + czstr

    def ty_decode(self, dststr):
        ddstr = self.tycode(self.session_seed + int(dststr[:4], 16), dststr[4:])
        return ddstr

    def connectionLost(self, reason):
        TcpProtocolHelper.connectionLost(self, reason)

    def connectionMade(self):
        TcpProtocolHelper.connectionMade(self)
        self.session_seed = random.randint(100, 0xfffE)
        self.myrand = 0
        self.transport.write('%04x' % self.session_seed)
        if TyContext.ftlog.is_debug_net():
            TyContext.ftlog.debug('ziptcp->session_seed=', self.session_seed)

    def lineReceived(self, data):
        try:
            if TyContext.ftlog.is_debug_net():
                TyContext.ftlog.debug('ziptcp <<<', repr(data))
            data = self.ty_decode(data)
            if len(data) < 11:  # {"cmd":"a"}
                raise Exception('lineReceived, ty_decode data too short ! [' + repr(data) + ']')
            if data[0] != '{':
                raise Exception('lineReceived, ty_decode data not start with { ! [' + repr(data[0:10]) + ']')
            c1, c2, c3, c4, c5 = data[-1], data[-2], data[-3], data[-4], data[-5]  # 后3位可能是  }\n\0 或 }\n 或 }\0 或 }
            if not (c1 == '}' or c2 == '}' or c3 == '}' or c4 == '}' or c5 == '}'):
                raise Exception('lineReceived, ty_decode data not end with } ! [' + repr(data[-10:]) + ']')

        except Exception, e:
            TyContext.ftlog.error('\n' * 5)
            TyContext.ftlog.error("ERROR ====== key=", self._key, "ZIP RECEIVE ", e)
            TyContext.ftlog.exception()
            TyContext.ftlog.error('\n' * 5)
            self.transport.loseConnection()
            return
        TcpProtocolHelper.lineReceived(self, data)

    def sendTcpMessageList(self, msgs):
        if TyContext.ftlog.is_debug_net():
            for x in xrange(len(msgs)):
                TyContext.ftlog.debug('====== SEND_TO2 ', self._key, self.userId, repr(msgs[x]))
        msgstr = ''
        for x in xrange(len(msgs)):
            msgstr = msgstr + self.ty_encode(msgs[x])
            if TyContext.ftlog.is_debug_net():
                TyContext.ftlog.debug('ziptcp >>>', repr(msgstr))

        return TcpProtocolHelper.sendTcpMessage(self, msgstr)

    def sendTcpMessage(self, msg, is_heart_beat_reply=False):
        if TyContext.ftlog.is_debug_net():
            TyContext.ftlog.debug('====== SEND_TO ', self._key, self.userId, repr(msg))

        if is_heart_beat_reply:
            zinfo = ''
        else:
            zinfo = self.ty_encode(msg)
        if TyContext.ftlog.is_debug_net():
            TyContext.ftlog.debug('ziptcp >>>', repr(zinfo))
        return TcpProtocolHelper.sendTcpMessage(self, zinfo, is_heart_beat_reply)

    def makeTasklet(self, reqmsg):
        pass


# Basic tcp protocol...
class BasicTCPServerProtocol(LineReceiver):
    def connectionMade(self):
        TcpProtocolHelper.connectionMade(self)

    def connectionLost(self, reason):
        TcpProtocolHelper.connectionLost(self, reason)

    def lineReceived(self, data):
        TcpProtocolHelper.lineReceived(self, data)

    def sendTcpMessageList(self, msgs):
        if TyContext.ftlog.is_debug_net():
            for x in xrange(len(msgs)):
                TyContext.ftlog.debug('====== SEND_TO2 ', self._key, self.userId, repr(msgs[x]))
        msgstr = ''.join(msgs)
        return TcpProtocolHelper.sendTcpMessage(self, msgstr)

    def sendTcpMessage(self, msg, is_heart_beat_reply=False):
        if TyContext.ftlog.is_debug_net():
            TyContext.ftlog.debug('====== SEND_TO ', self._key, self.userId, repr(msg))
        return TcpProtocolHelper.sendTcpMessage(self, msg, is_heart_beat_reply)

    def makeTasklet(self, reqmsg):
        pass


class BasicUDPServerProtocol(DatagramProtocol):
    sendCount = 0
    receiveCount = 0
    BUFFERSIZE = 2 * 1024 * 1024

    def startProtocol(self):
        sock = self.transport.getHandle()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFFERSIZE)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, self.BUFFERSIZE)

    def checkTableCall(self, msg, issend):
        if msg.find('table_call') > 0:
            if issend:
                BasicUDPServerProtocol.sendCount += 1
                if BasicUDPServerProtocol.sendCount % 1000 == 0:
                    TyContext.ftlog.info('BasicUDPServerProtocol table_call_table_call sendCount=',
                                         BasicUDPServerProtocol.sendCount)
            else:
                BasicUDPServerProtocol.receiveCount += 1
                if BasicUDPServerProtocol.receiveCount % 1000 == 0:
                    TyContext.ftlog.info('BasicUDPServerProtocol table_call_table_call receiveCount=',
                                         BasicUDPServerProtocol.receiveCount)

    def writeMessage(self, data, address):
        if TyContext.ftlog.is_debug_net():
            TyContext.ftlog.debug('====== SEND_TO UDP: ' + str(self.gdata.serverId) + ':' + address[0] + ':' + str(
                address[1]) + ':' + data)
        self.checkTableCall(data, 1)
        self.transport.write(data, address)

    def datagramReceived(self, data, address):
        ukey = ''
        try:
            if TyContext.ftlog.is_debug_net():
                ukey = '====== RECEIVE UDP: ' + str(self.gdata.serverId) + ':' + address[0] + ':' + str(
                    address[1]) + ':'
                TyContext.ftlog.debug(ukey + ':' + str(len(data)) + ':' + data)
            self.checkTableCall(data, 0)
            msgline = TyContext.MsgLine.unpack(data)
            c = self.makeTasklet(msgline, self, address)
            stackless.tasklet(c.tasklet)()
        except:
            TyContext.ftlog.error('\n' * 5)
            TyContext.ftlog.error("ERROR", ukey, address, data)
            TyContext.ftlog.exception()
            TyContext.ftlog.error('\n' * 5)
        #             self.transport.write(MsgPack.makeErrorString('error udp pack'), address)

        reactor.callLater(0.0, stackless.schedule)

    def makeTasklet(self, reqmsg, protocol, address):
        pass
