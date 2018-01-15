# -*- coding=utf-8 -*-
'''
Created on 2015年6月10日

@author: zqh
'''
from tyframework._private_.msg.msg import MsgPack
from tyframework.context import TyContext
from tyframework.orderids import gamereg


class HttpGameRegister(object):
    JSONPATHS = None
    HTMLPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/_game_server_online_': cls.doGameServerOnline,
                '/_game_server_offline_': cls.doGameServerOffline,
                '/_game_server_list_': cls.doGameServerList
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
    def _check_param_params(self):
        jstr = TyContext.RunHttp.getRequestParam('params', '')
        if len(jstr) > 0:
            try:
                data = TyContext.strutil.loadsbase64(jstr)
                return data
            except:
                pass
        return 'param params error'

    @classmethod
    def doGameServerOnline(self, rpath):
        params = self._check_param_params()
        TyContext.ftlog.info('doGameServerOnline', params)
        if not isinstance(params, dict):
            mo = MsgPack()
            mo.setError(1, params)
            return
        http_game = params['http_game']
        conns = params['conns']
        mode = params['mode']
        name = params['name']
        rtime = params['time']
        ok, games = gamereg.registerServer(http_game, mode, name, conns, rtime)
        mo = MsgPack()
        mo.setResult('ok', ok)
        mo.setResult('games', games)
        return mo

    @classmethod
    def doGameServerOffline(self, rpath):
        params = self._check_param_params()
        TyContext.ftlog.info('doGameServerOffline', params)
        if not isinstance(params, dict):
            mo = MsgPack()
            mo.setError(1, params)
            return
        http_game = params['http_game']
        ok, games = gamereg.unRegisterServer(http_game)
        mo = MsgPack()
        mo.setResult('ok', ok)
        mo.setResult('games', games)
        return mo

    @classmethod
    def doGameServerList(self, rpath):
        TyContext.ftlog.info('doGameServerList')
        gamesBuff, gamesDb = gamereg.listRegisterServer()
        mo = MsgPack()
        mo.setResult('gamesBuff', gamesBuff)
        mo.setResult('gamesDb', gamesDb)
        return mo
