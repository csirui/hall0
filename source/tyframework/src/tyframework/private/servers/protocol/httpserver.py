# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月13日 星期五 15时06分10秒
# FileName:      HttpServer.py
# Class:         LogRequestHandler, LogHttp, LogHttpFactory
import stackless
from twisted.internet import reactor
from twisted.web import http

from tyframework.context import TyContext
from tyframework.tasklet.http import HttpTasklet


class LogRequestHandler(http.Request):
    def process(self):
        try:
            gdata = LogHttpFactory.gdata
            c = HttpTasklet(gdata, self, gdata.redis_pool, gdata.webroot)
            stackless.tasklet(c.tasklet)()
            reactor.callLater(0.0, stackless.schedule)
        except:
            TyContext.ftlog.exception()
            self.finish()


class LogHttp(http.HTTPChannel):
    requestFactory = LogRequestHandler


class LogHttpFactory(http.HTTPFactory):
    protocol = LogHttp

    def __init__(self, gdata):
        LogHttpFactory.gdata = gdata

    def startFactory(self):
        pass

    def stopFactory(self):
        pass

    def log(self, request):
        pass

    def _logFormatter(self, datas, request):
        return ''

    @classmethod
    def makeHeartBeatTasklet(cls):
        gdata = LogHttpFactory.gdata
        c = HttpTasklet(gdata, None, gdata.redis_pool, gdata.webroot)
        return c
