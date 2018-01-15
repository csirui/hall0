# -*- coding=utf-8 -*-


from tyframework.context import TyContext


class TuYouPayYdMm():
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        payCode = '30000552202602'
        if prodId == 'T20K':
            payCode = '30000552202601'
        if prodId == 'T50K':
            payCode = '30000552202602'
        if prodId == 'T100K':
            payCode = '30000552202603'
        if prodId == 'T300K':
            payCode = '30000552202604'
        if prodId == 'MOONKEY':
            payCode = '30000552202605'
        if prodId == 'MOONKEY3':
            payCode = '30000552202606'
        if prodId == 'VOICE100':
            payCode = '30000552202607'
        if prodId == 'RAFFLE':
            payCode = '30000552202608'
        if prodId == 'ONHOOK':
            payCode = '30000552202601'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doYdMmCallbackMsg(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = TyContext.RunHttp.getRequestParam('platformOrderId', '')

        from tysdk.entity.pay.pay import TuyouPay
        result = TyContext.RunHttp.getRequestParam('result', '')
        if result != '1':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('doYdMmCallbackMsg return error: result(%d)' % result, 'is not 1 !!!')
            if orderPlatformId:
                TuyouPay.deliveryChargeError(orderPlatformId, rparam, u'支付失败', 1)
            return '{result:{success:1,orderPlatformId:"' + orderPlatformId + '"}}'

        trade_status = 'TRADE_FINISHED'
        total_fee = -1
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return '{result:{success:1,orderPlatformId:"' + orderPlatformId + '"}}'
        else:
            return '{result:{success:0,orderPlatformId:"' + orderPlatformId + '"}}'
        pass
