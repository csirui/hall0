# -*- coding=utf-8 -*-

from simpletasklet import SimpleTasklet
from tyframework.context import TyContext


class TimerTasklet(SimpleTasklet):
    heartcount = 0

    def __init__(self, server):
        self.server = server

    def handle(self):
        hc = TimerTasklet.heartcount + 1
        if hc > 31536000:  # 1年
            TimerTasklet.heartcount = 1
        else:
            TimerTasklet.heartcount = hc

        for fun in self.getCommands():
            try:
                fun(hc)
            except Exception, e:
                TyContext.ftlog.exception('HANDLE TIMER ERROR', e)

        self.server.scheduleHeartBeat()

    def getCommands(self):
        raise NotImplementedError
