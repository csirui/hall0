# -*- coding=utf-8 -*-

from msgtasklet import MsgTasklet


class UdpInnerMsgTasklet(MsgTasklet):
    def __init__(self, msgline, udpProtocol, address):
        self.taskletType = 6
        self.msgline = msgline
        self.udpProtocol = udpProtocol
        self.address = address

    def sendResponse(self, msg, userId=None):
        self.udpProtocol.sendMessage(msg, self.address, userId)
