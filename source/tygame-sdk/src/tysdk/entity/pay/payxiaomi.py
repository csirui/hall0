# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import hmac
from hashlib import sha1

from tyframework.context import TyContext


class TuyouPayXiaomi(object):
    @classmethod
    def doPayRequestXiaomiCommon(self, params):
        mo = TyContext.Cls_MsgPack()
        from tysdk.entity.pay.pay import TuyouPay
        TuyouPay.makeBuyChargeMessage(mo, params)
        return mo

    @classmethod
    def doBuyStraight(cls, userId, params, mo):
        prodId = params['prodId']
        appId = params['appId']

        prodconfig = TyContext.Configure.get_global_item_json('xiaomidanji_prodids', {})
        data = prodconfig[str(appId)].get(prodId, None)
        if data:
            amount = data['price']
            prodName = data['name']
            # payCode = data['feecode']
        else:
            raise Exception('can not find xiaomidanji product define of prodId=' + prodId)

        payData = {'amount': amount, 'productId': prodId, 'productName': prodName}
        params['payData'] = payData
        mo.setResult('payData', payData)

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

        from tysdk.entity.pay.pay import TuyouPay
        if rparam['orderStatus'] != 'TRADE_SUCCESS':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('doXiaomiCallback error, charge return error !!!')
            errorInfo = '小米支付-未知错误'
            TuyouPay.deliveryChargeError(orderPlatformId, rparam, errorInfo, 1)
            return '{"errcode":200}'

        trade_status = 'TRADE_FINISHED'
        total_fee = int(float(rparam['payFee']))
        total_fee = int(total_fee / 100)

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return '{"errcode":200}'
        else:
            return '{"errcode":1506}'
