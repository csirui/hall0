# -*- coding=utf-8 -*-
'''
Created on 2014年12月12日

@author: zhaojiangang
'''


class BiUtils(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def clientIdToNumber(self, gameId, clientId):
        '''
        '''
        numDict = self.__ctx__.Configure.get_configure_json('clientid.number.map', {})
        if not numDict:
            self.__ctx__.ftlog.error('BiUtils.clientIdToNumber gameId=', gameId,
                                     'clientId=', clientId, 'NotConfig')
            return 0
        num = numDict.get(clientId)
        if num is None:
            self.__ctx__.ftlog.error('BiUtils.clientIdToNumber gameId=', gameId,
                                     'clientId=', clientId, 'UnknownClientId')
            return 0
        return num

    def productIdToNumber(self, gameId, productId):
        '''
        '''
        numDict = self.__ctx__.Configure.get_global_item_json('productid.number.map', {})
        if not numDict:
            self.__ctx__.ftlog.error('BiUtils.productIdToNumber gameId=', gameId,
                                     'productId=', productId, 'NotConfig')
            return 0
        num = numDict.get(productId)
        if num is None:
            self.__ctx__.ftlog.error('BiUtils.productIdToNumber gameId=', gameId,
                                     'productId=', productId, 'UnknownProductId')
            return 0
        return num

    def giftIdToNumber(self, gameId, giftId):
        numDict = {
            'GIFT1': self.__ctx__.GiftId.FLOWER,
            'GIFT2': self.__ctx__.GiftId.CAKE,
            'GIFT3': self.__ctx__.GiftId.CAR,
            'GIFT4': self.__ctx__.GiftId.PLANE,
            'GIFT5': self.__ctx__.GiftId.VILLA
        }
        num = numDict.get(giftId, self.__ctx__.GiftId.UNKNOWN)
        if num == self.__ctx__.GiftId.UNKNOWN:
            self.__ctx__.ftlog.error('BiUtils.giftIdToNumber gameId=', gameId,
                                     'giftId=', giftId, 'UnknownGiftId')
        return num

    def consumeEmoticonNameToBIEventId(self, gameId, ename):
        numDict = {
            'egg': self.__ctx__.BIEventId.EMOTICON_EGG_CONSUME,
            'bomb': self.__ctx__.BIEventId.EMOTICON_BOMB_CONSUME,
            'flower': self.__ctx__.BIEventId.EMOTICON_FLOWER_CONSUME,
            'diamond': self.__ctx__.BIEventId.EMOTICON_DIAMOND_CONSUME,

            'eggs': self.__ctx__.BIEventId.EMOTICON_EGG_CONSUME,  # for texas
            'rose': self.__ctx__.BIEventId.EMOTICON_FLOWER_CONSUME,  # for texas
            'ring': self.__ctx__.BIEventId.EMOTICON_DIAMOND_CONSUME,  # for texas
        }
        num = numDict.get(ename, self.__ctx__.BIEventId.UNKNOWN)
        if num == self.__ctx__.BIEventId.UNKNOWN:
            self.__ctx__.ftlog.error('BiUtils.consumeEmoticonNameToBIEventId gameId=', gameId,
                                     'ename=', ename, 'UnknownEmoticonId')
        return num

    def _getClientIdNumInt(self, gameid, clientId):
        if clientId:
            if isinstance(clientId, (int, float)):
                return int(clientId)
            if isinstance(clientId, (str, unicode)):
                numberClientId = self.clientIdToNumber(gameid, clientId)
                if numberClientId:
                    return numberClientId
        return 0

    def getClientIdNum(self, clientId, argdict, gameid, uid, check_msg=1):
        # 先看原始输入
        i = self._getClientIdNumInt(gameid, clientId)
        if i:
            return clientId, i
        # 再看可变参数集合
        if isinstance(argdict, dict):
            clientId0 = argdict.get('clientId', None)
            i = self._getClientIdNumInt(gameid, clientId0)
            if i:
                return clientId0, i
        # 再看消息中的值
        if check_msg:
            clientId3 = None
            try:
                if self.__ctx__.RunHttp.is_current_http():
                    clientId3 = self.__ctx__.RunHttp.getRequestParam('clientId')
                else:
                    msg = self.__ctx__.getTasklet().getMsg()
                    clientId3 = msg.getParam('clientId')
            except:
                pass
            i = self._getClientIdNumInt(gameid, clientId3)
            if i:
                return clientId3, i
        # 再看session中的值和创建用户时的值
        clientId1, clientId2 = None, None
        try:
            clientId1, clientId2 = self.__ctx__.RedisUser.execute(uid, 'HMGET', 'user:' + str(uid), 'sessionClientId',
                                                                  'clientId')
        except:
            pass
        i = self._getClientIdNumInt(gameid, clientId1)
        if i:
            return clientId1, i

        i = self._getClientIdNumInt(gameid, clientId2)
        if i:
            return clientId2, i
        self.__ctx__.ftlog.error('BiUtils.clientIdToNumber gameId=', gameid,
                                 'clientId=', clientId, 'UnknownClientId Final')
        return clientId, 0


BiUtils = BiUtils()
