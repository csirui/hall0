# -*- coding=utf-8 -*-

'''
Created on 2013年12月17日

@author: zhaojiangang
'''


class ClientUtils(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def getMomoClientVerBefore337(self, clientId):
        if clientId in ('Android_3.2_momo', 'Android_3.1_momo', 'IOS_3.1_momo', 'IOS_3.2_momo'):
            return 2.8
        return 0

    def getVersionFromClientId(self, clientId):
        clientVer = self.getMomoClientVerBefore337(clientId)
        self.__ctx__.ftlog.debug('getVersionFromClientId->', clientVer, clientId)
        if clientVer > 0:
            return clientVer
        if isinstance(clientId, (str, unicode)):
            infos = clientId.split('_')
            if len(infos) > 2:
                try:
                    clientVer = float(infos[1])
                except:
                    pass
        return clientVer

    def getVersionFromMsg(self, msg):
        clientId = msg.getParamStr('clientId', '')
        return self.getVersionFromClientId(clientId)

    def getVersionFromUserSession(self, tasklet, uid):
        sessionClientId = self.__ctx__.UserSession.get_session_clientid(uid)
        return self.getVersionFromClientId(sessionClientId)

    def getUserSessionClientId(self, tasklet, uid):
        sessionClientId = self.__ctx__.UserSession.get_session_clientid(uid)
        return sessionClientId

    def isIOSClient(self, clientId):
        if not isinstance(clientId, basestring):
            return False
        clientId = clientId.lower()
        if clientId.find('ios_') == 0:
            return True
        return False

    def isWinPcClient(self, clientId):
        return isinstance(clientId, basestring) and clientId.startswith('Winpc')

    def isBindMobile(self, tasklet, userId):
        bindMobile = self.__ctx__.UserProps.get_attr(userId, 'bindMobile', False)
        return True if bindMobile else False

    def getGameId(self, clientId, gameId):
        for i in clientId.split('.'):
            index = i.find('hall')
            if index >= 0:
                return i[index + 4:]
        return gameId

    def getGameIdFromUserSession(self, tasklet, uid, gameId):
        sessionClientId = self.__ctx__.UserSession.get_session_clientid(uid)
        return self.getGameId(sessionClientId, gameId)


ClientUtils = ClientUtils()
