# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

from tyframework.context import TyContext


class TuYouPayLenovo(object):
    appkeys = {
        '20017200000001200172': 'RDNCMjAyOTlFQkU1NzdCMDI1NDRBRUIwMTc0NjlCNjM0NkZDNzM5QU1UQTJORFExTVRjeU9ERTNPRFl5T1RjNE5ERXJNVFUwTnpNek9EVTNNekV6TkRNd01UZzRORFkzTWpZeE5EZzVOamcyTnpBNE9UQTNPVFF6'
        }

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        payCode = '3'
        if prodId == 'T20K':
            payCode = '1'
        if prodId == 'T50K':
            payCode = '2'
        if prodId == 'T100K':
            payCode = '3'
        if prodId == 'T300K':
            payCode = '4'
        if prodId == 'RAFFLE':
            payCode = '1'
        if prodId == 'RAFFLE_NEW':
            payCode = '9'
        if prodId == 'VOICE100':
            payCode = '6'
        if prodId == 'ONHOOK':
            payCode = '7'
        if prodId == 'MOONKEY':
            payCode = '1'
        if prodId == 'MOONKEY3':
            payCode = '2'

        prodName = params['orderName']
        if prodName == u'幸运礼包':
            payCode = '1'
        if prodName == u'旺财礼包':
            payCode = '2'
        if prodName == u'黄钻礼包':
            payCode = '3'
        if prodName == u'至尊礼包':
            payCode = '4'
        if prodName == u'翻倍抽奖':
            payCode = '1'
        if prodName == u'语音喇叭礼包':
            payCode = '6'
        if prodName == u'挂机礼包':
            payCode = '7'
        if prodName == u'月光之钥':
            payCode = '1'
        if prodName == u'月光之钥x3':
            payCode = '2'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doLenovoCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        TyContext.ftlog.info('doLenovoCallback->rparam=', rparam)
        transdata = rparam['transdata']

        try:
            datas = json.loads(transdata)
            appId = datas['appid']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLenovoCallback->ERROR, sign error !! transdata=', transdata)
            return 'ERROR'

        appKey = self.appkeys[appId]
        sign = rparam['sign']
        if self.verifySign(transdata, sign, appKey) != True:
            TyContext.ftlog.info('doLenovoCallback->ERROR, sign error !! transdata=', transdata, 'sign=', sign)
            return 'ERROR'

        orderPlatformId = datas['exorderno']

        from tysdk.entity.pay.pay import TuyouPay
        if datas['result'] != 0:
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('doLenovoCallback error, charge return error !!!')
            errorInfo = '联想-未知错误'
            TuyouPay.deliveryChargeError(orderPlatformId, rparam, errorInfo, 1)
            return 'ERROR'

        trade_status = 'TRADE_FINISHED'
        total_fee = float(datas['money'])
        total_fee = int(total_fee / 100)

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return 'SUCCESS'
        else:
            return 'ERROR'

    @classmethod
    def verifySign(cls, transdata, sign, appKey):
        # TODO 
        TyContext.ftlog.error('TuyouPayLenovo-verifySign->transdata=', transdata, 'sign=', sign, 'appKey=', appKey)
        return True
