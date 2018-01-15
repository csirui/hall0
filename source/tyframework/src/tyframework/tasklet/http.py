# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 16时55分58秒
# FileName:      http91.py
# Class:         Http91Tasklet
from tyframework.context import TyContext
from tyframework.tasklet.basic import SimpleTasklet


class HttpTasklet(SimpleTasklet):
    def __init__(self, gdata, request, redispool, wwwroot):
        self.gdata = gdata
        self.request = request
        if request:
            self.args = request.args
        else:
            self.args = {}

        self.wwwroot = wwwroot + '/'
        self.canSendMainUdpMsg = True

    def doServerHeartBeat(self, hc):
        TyContext.ftlog.debug('HttpTasklet doServerHeartBeat', hc)

    def handle(self):

        if not self.request:
            try:
                hc = self.gdata.heartCounter
                self.doServerHeartBeat(hc)
                #                 TyContext.Configure.reload(hc, True) # 由热更新命令直接带动, 不再循环检查变化
                if hc > 31536000:  # 1年
                    self.gdata.heartCounter = 0
                else:
                    self.gdata.heartCounter = hc + 1
            except Exception, e:
                TyContext.ftlog.error('HANDLE_ERROR', e)
                TyContext.ftlog.exception()
            self.gdata.service.scheduleHeartBeat()
            return

        TyContext.RunHttp.handler_http_request(self.request)

    def doRequestFinish(self, content, fheads, rpath, debugContent=True):
        if debugContent:
            TyContext.ftlog.debug('doRequestFinish', rpath, content)
        try:
            for k, v in fheads.items():
                self.request.setHeader(k, v)
            self.request.setHeader('Content-Length', len(content))
        except:
            TyContext.ftlog.exception()
        try:
            self.request.write(content)
        except:
            try:
                self.request.write(content.encode('utf8'))
            except:
                TyContext.ftlog.exception()
            pass
        try:
            self.request.channel.persistent = 0
        except:
            pass
        try:
            self.request.finish()
        except:
            TyContext.ftlog.exception()

    def getRequestParam(self, key, defaultVal=None):
        if key in self.args:
            vals = self.args[key]
            return vals[0]
        return defaultVal

    def getRequestParamInt(self, key, defaultVal=0):
        try:
            return int(self.args[key][0])
        except:
            pass
        return defaultVal

    def getRequestParamJs(self, jsons, key, defaultVal):
        val = defaultVal
        if key in self.args:
            vals = self.args[key]
            val = vals[0]
        val = val.replace('\'', '"')
        val = val.decode('UTF-8')
        jsons[key] = val

    def convertToMsgPack(self, keys):
        msg = TyContext.MsgPack()
        for key in keys:
            value = self.getRequestParam(key)
            if value != None:
                msg.setParam(key, value)
        return msg

    def convertToDict(self):
        datas = {}
        for key in self.args:
            value = self.getRequestParam(key)
            if value != None:
                datas[key] = value
        return datas

    def notifyItemListChange(self, gameId, userId):
        mo = TyContext.MsgPack()
        mo.setCmd('item_list')
        mo.setParam('userId', userId)
        mo.setParam('gameId', gameId)
        self.msg = mo
        self.sendUdpToServerType(mo, userId, 3)

    def notifyUserInfoChange(self, gameId, userId):
        mo = TyContext.MsgPack()
        mo.setCmd('user_info')
        mo.setParam('userId', userId)
        mo.setParam('gameId', gameId)
        clientId = TyContext.UserSession.get_session_clientid(userId)
        if clientId != None:
            mo.setParam('clientId', clientId)
            self.msg = mo
            self.sendUdpToServerType(mo, userId, 2)
        else:
            TyContext.ftlog.error('the user sessionClientId is none', userId)
