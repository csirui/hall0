# -*- coding=utf-8 -*-

from tyframework.context import TyContext
from tyframework.tasklet.basic import BasicTasklet


class ManagerTasklet(BasicTasklet):
    def __init__(self, gdata, msgline, udpprotocol, udpaddress):
        self.gdata = gdata
        self.msgline = msgline
        self.msg = None
        self.redis_conn = gdata.redis_pool
        self.protocol = udpprotocol
        self.transport = udpprotocol.transport
        self.udpaddress = udpaddress

    def handle(self, cmd):
        self.msg = self.getMsg()
        userId = self.msg.getParamInt('userId')
        gameId = self.msg.getParamInt('gameId')
        TyContext.ftlog.debug('QuickStartTasklet->cmd=', cmd, 'gameId=', gameId, 'userId=', userId)
        if cmd == 'server_ready':
            self.doServiceReady()
            return

        TyContext.ftlog.error('HANDLE_ERROR, not in case cmd=', cmd)

    def doServerHeartBeat(self, hc):
        pass
