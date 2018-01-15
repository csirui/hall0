# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

from constants import PayConst
from request_conf import TuyouPayRequestConf
from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay_common.orderlog import Order


class TuyouPayRequest(object):
    __request_funs__ = {}

    @classmethod
    def request(cls, mi):
        TyContext.ftlog.debug('---request---mi', mi)
        userId = mi.getParamInt('userId')
        chargeType = mi.getParamStr('chargeType')
        appId = mi.getParamInt('appId', 'na')
        clientId = mi.getParamStr('clientId', 'na')
        platformOrderId = mi.getParamStr('platformOrderId')
        shortId = 'na'
        if ShortOrderIdMap.is_short_order_id_format(platformOrderId):
            shortId, platformOrderId = platformOrderId, ShortOrderIdMap.get_long_order_id(platformOrderId)

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('request')

        chargeKey = 'sdk.charge:' + platformOrderId
        state, chargeInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'state', 'charge')
        TyContext.ftlog.debug('TuyouPayRequest request: order', platformOrderId,
                              'state', state, 'charge', chargeInfo)
        if state is None or not chargeInfo:
            mo.setError(1, '充值错误，请关闭界面重试')
            return mo

        if state >= PayConst.CHARGE_STATE_ERROR_REQUEST:
            mo.setError(1, '充值失败，请关闭界面重试')
            return mo

        chargeInfo = json.loads(chargeInfo)
        if chargeInfo['uid'] != userId:
            mo.setError(1, '充值事务错误')
            return mo

        if 'chargeType' not in chargeInfo or chargeInfo['chargeType'] != chargeType:
            chargeInfo['chargeType'] = chargeType
            TyContext.RedisPayData.execute('HMSET', chargeKey, 'charge', json.dumps(chargeInfo))

        state = cls.__request__(chargeType, chargeInfo, mi, mo)
        if state == PayConst.CHARGE_STATE_REQUEST:
            TyContext.RedisPayData.execute('HSET', chargeKey, 'state', state)
            Order.log(platformOrderId, Order.REQUEST_OK, userId,
                      appId, clientId,
                      diamondid=chargeInfo.get('diamondId', 'na'),
                      charge_price=chargeInfo.get('chargeTotal', 'na'),
                      paytype=chargeType)
        elif state == PayConst.CHARGE_STATE_ERROR_REQUEST:
            # mo.setError(1, '充值请求失败')
            errInfo = mo.getErrorInfo()
            TyContext.RedisPayData.execute('HMSET', chargeKey, 'state', state,
                                           'errorInfo', errInfo)
            Order.log(platformOrderId, Order.REQUEST_ERROR, userId, appId,
                      clientId, info=errInfo,
                      diamondid=chargeInfo.get('diamondId', 'na'),
                      charge_price=chargeInfo.get('chargeTotal', 'na'),
                      paytype=chargeType)
        elif state == PayConst.CHARGE_STATE_REQUEST_RETRY \
                or state == PayConst.CHARGE_STATE_REQUEST_IGNORE:
            Order.log(platformOrderId, Order.REQUEST_RETRY, userId,
                      appId, clientId,
                      diamondid=chargeInfo.get('diamondId', 'na'),
                      charge_price=chargeInfo.get('chargeTotal', 'na'),
                      paytype=chargeType)
        else:
            raise Exception('not known state ' + state)
        mo.setResult('status', state)
        return mo

    @classmethod
    def __request__(cls, chargeType, chargeInfo, mi, mo):

        if chargeType in cls.__request_funs__:
            cfun = cls.__request_funs__[chargeType]
        else:
            cpath = TuyouPayRequestConf.REQUEST_DATA[chargeType]
            tks = cpath.split('.')
            mpackage = '.'.join(tks[0:-2])
            clsName = tks[-2]
            methodName = tks[-1]
            clazz = None
            exec 'from %s import %s as clazz' % (mpackage, clsName)
            cfun = getattr(clazz, methodName)
            cls.__request_funs__[chargeType] = cfun

        return cfun(chargeInfo, mi, mo)
