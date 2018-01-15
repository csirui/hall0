# -*- coding=utf-8 -*-

from tyframework.context import TyContext
from tyframework.tasklet.basic import BasicTasklet


class HttpUdpTasklet(BasicTasklet):
    _extend_heartbeat_callable = []

    def __init__(self, gdata, msgline, udpprotocol, udpaddress):
        self.gdata = gdata
        self.msgline = msgline
        self.msg = None
        self.redis_conn = gdata.redis_pool
        self.protocol = udpprotocol
        self.transport = udpprotocol.transport
        self.udpaddress = udpaddress

    def handle(self, cmd):
        TyContext.ftlog.info('HttpUdpTasklet cmd=', cmd)
        pass

    @classmethod
    def add_heartbeat_handler(cls, handler):
        cls._extend_heartbeat_callable.append(handler)

    def doServerHeartBeat(self, hc):
        TyContext.ftlog.debug('HttpUdpTasklet Server Heart Beat !!', hc)
        if HttpUdpTasklet._extend_heartbeat_callable:
            for call in HttpUdpTasklet._extend_heartbeat_callable:
                try:
                    call(hc)
                except:
                    TyContext.ftlog.exception()
