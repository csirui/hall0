# -*- coding=utf-8 -*-
import json

from constants import PHONETYPE_INTS
from tyframework.context import TyContext
from tysdk.entity.pay.paycheck import TuyouPayCheck


class TuYooPayType(object):
    @classmethod
    def __bug_paytypeinfo_patch__(cls, datas):
        if datas:
            if 'paytype' in datas:
                datas['payType'] = datas['paytype']
            elif 'payType' in datas:
                datas['paytype'] = datas['payType']
        return datas

    @classmethod
    def __get_pay_info__(cls, appId, clientId, buttonId, unlimit, phonetype):
        rkey = "paytype:" + str(appId) + ":" + clientId
        rsubkey = str(buttonId) + '_' + str(unlimit) + '_' + str(phonetype)
        TyContext.ftlog.info('__get_pay_info__ ->HGET', "rkey:", rkey, 'rsubkey', rsubkey)

        # TODO 过渡期代码，线上的paytype存放于mix库，新的策略为存放于configer库 
        paytypeinfo = TyContext.RedisMix.execute('HGET', rkey, rsubkey)
        if paytypeinfo == None:
            paytypeinfo = TyContext.RedisConfig.execute('HGET', rkey, rsubkey)
        try:
            data = json.loads(paytypeinfo)
            return cls.__bug_paytypeinfo_patch__(data)
        except:
            TyContext.ftlog.exception()
        TyContext.ftlog.info('__get_pay_info__ ERROR ->HGET', "paytype:" + str(appId) + ":" + clientId,
                             str(buttonId) + '_' + str(unlimit) + '_' + str(phonetype), paytypeinfo)
        return None

    @classmethod
    def getPayType(self, appId, clientId, buttonId, unlimit, phonetype, mo):
        #         TyContext.ftlog.info('getPayType->', appId, clientId, buttonId, unlimit, phonetype)
        if appId == None or clientId == None or buttonId == None or unlimit == None or phonetype == None:
            mo.setResult('code', '1')
            mo.setResult('info', 'param error!')
            return
        data = self.__get_pay_info__(appId, clientId, buttonId, unlimit, phonetype)
        try:
            mo.setResult('code', '0')
            mo.setResult('payType', data['paytype'])
            mo.setResult('price', data['price'])
            return
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('TuYooPayType.getPayType->ERROR,  paytypeinfo=', data, appId, clientId, buttonId,
                                 unlimit, phonetype)
        mo.setResult('code', '2')
        mo.setResult('info', 'system error!')
        return

    @classmethod
    def getPayTypeByUser(self, userId, appId, buttonId):
        #         TyContext.ftlog.info('getPayTypeByUser->', appId, userId, appId, buttonId)
        phoneType, clientId = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'sessionPhoneType',
                                                          'sessionClientId')
        if clientId == None:
            clientId = 'none_1_none'
        if phoneType in PHONETYPE_INTS:
            phoneType = PHONETYPE_INTS[phoneType]
        else:
            phoneType = PHONETYPE_INTS['other']

        udata = {}
        TuyouPayCheck.appendMsgPayLimitInfo(userId, udata)
        if (int(udata['msgpaylimit']) != 0):
            unlimit = 1
        else:
            unlimit = 0

        data = self.__get_pay_info__(appId, clientId, buttonId, unlimit, phoneType)
        if data:
            return data['paytype']
        else:
            return '360'

    @classmethod
    def getChargeTypeByUser(self, userId, appId, diamondId, clientId):
        #         TyContext.ftlog.info('getChargeTypeByUser->', userId, appId, diamondId, clientId)
        paytypeinfo = None
        rkey = None
        rsubkey = None
        phoneType = ''
        try:
            phoneType = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sessionPhoneType')
            if phoneType in PHONETYPE_INTS:
                phoneTypeInt = PHONETYPE_INTS[phoneType]
            else:
                phoneTypeInt = PHONETYPE_INTS['other']

            unlimit = TuyouPayCheck.getMsgPayLimit(userId)

            rkey = "paytype:" + str(appId) + ":" + clientId
            rsubkey = str(diamondId) + '_' + str(unlimit) + '_' + str(phoneTypeInt)

            # TODO 过渡期代码，线上的paytype存放于mix库，新的策略为存放于configer库 
            paytypeinfo = TyContext.RedisMix.execute('HGET', rkey, rsubkey)
            if paytypeinfo == None:
                paytypeinfo = TyContext.RedisConfig.execute('HGET', rkey, rsubkey)

            data = json.loads(paytypeinfo)
            data = self.__bug_paytypeinfo_patch__(data)
            if data and 'paytype' in data:
                return data['paytype'], phoneType
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.error('TuYooPayType.getChargeTypeByUser->ERROR, params=', userId, appId, diamondId,
                                  clientId, rkey, rsubkey, paytypeinfo)
        return '360', phoneType
