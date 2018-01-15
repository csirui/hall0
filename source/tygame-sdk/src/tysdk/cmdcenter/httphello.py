# -*- coding=utf-8 -*-
'''
Created on 2015年6月10日

@author: zqh
'''
from tyframework.context import TyContext
from tyframework.orderids import gamereg


class HttpHello(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/hello': cls.doProxyHello,
            }
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
            }
        return cls.HTMLPATHS

    def __init__(self):
        pass

    @classmethod
    def doProxyHello(self, rpath):
        datas = TyContext.RunHttp.convertArgsToDict()
        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        http_game = gamereg.findHttpGameByClientId(clientId)
        http_game = TyContext.strutil.decode_objs_utf8(http_game)
        TyContext.RunHttp.doHttpProxy(http_game + rpath, datas)
        return ''
