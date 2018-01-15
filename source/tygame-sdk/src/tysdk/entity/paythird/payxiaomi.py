# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import hmac
from hashlib import sha1

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayXiaomi(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {
            'amount': str(chargeinfo['chargeTotal']),
            'productId': chargeinfo['buttonId'],
            'productName': chargeinfo['buttonName'],
        }

    @classmethod
    def doXiaomiCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doXiaomiCallback->rparam=', rparam)
        appkeys = TyContext.Configure.get_global_item_json('xiaomi_paykeys', {})
        if rparam['appId'] not in appkeys:
            TyContext.ftlog.error('doXiaomiCallback->ERROR, appId error !! appId=', rparam['appId'])
            return '{"errcode":1515}'

        appKey = str(appkeys[rparam['appId']])
        return cls.__check_callback(rparam, appKey)

    @classmethod
    def doXiaomiDanJiCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doXiaomiDanJiCallback->rparam=', rparam)
        appkeys = TyContext.Configure.get_global_item_json('xiaomidanji_paykeys', {})
        if rparam['appId'] not in appkeys:
            TyContext.ftlog.error('doXiaomiCallback->ERROR, appId error !! appId=', rparam['appId'])
            return '{"errcode":1515}'

        appKey = str(appkeys[rparam['appId']])
        return cls.__check_callback(rparam, appKey)

    @classmethod
    def __check_callback(cls, rparam, appKey):
        signQuery = rparam['signature']
        del rparam['signature']

        sk = rparam.keys()
        sk.sort()
        queryStr = ""
        for k in sk:
            queryStr = queryStr + str(k) + '=' + str(rparam[k]) + '&'
        signData = queryStr[:-1]
        TyContext.ftlog.info('doXiaomiCallback->queryStr=', queryStr, 'signData=', signData)

        a = hmac.new(appKey, signData, sha1)
        sign = a.digest().encode('hex').upper()
        if signQuery.upper() != sign:
            TyContext.ftlog.info('doXiaomiCallback->ERROR, sign error !! signQuery=', signQuery, 'sign=', sign)
            return '{"errcode":1525}'

        orderPlatformId = rparam['cpOrderId']

        total_fee = float(rparam['payFee']) / 100

        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return '{"errcode":200}'
        else:
            return '{"errcode":1506}'
