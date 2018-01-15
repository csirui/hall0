# -*- coding=utf-8 -*-


from tyframework.context import TyContext


class TuYouPayYingYongHui():
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        payCode = '11111997'
        if prodId == 'T20K':
            payCode = '11111997'
        if prodId == 'T50K':
            payCode = '11111998'
        if prodId == 'RAFFLE':
            payCode = '11111999'
        if prodId == 'VOICE100':
            payCode = '11112000'
        if prodId == 'ONHOOK':
            payCode = '11112001'

        prodName = params['orderName']
        if prodName == u'幸运礼包':
            payCode = '11111997'
        if prodName == u'旺财礼包':
            payCode = '11111998'
        if prodName == u'翻倍抽奖':
            payCode = '11111999'
        if prodName == u'语音喇叭礼包':
            payCode = '11112000'
        if prodName == u'挂机礼包':
            payCode = '11112001'
        if prodName == u'黄钻礼包':
            payCode = '11112002'
        if prodName == u'金钻礼包':
            payCode = '11112003'
        if prodName == u'至尊礼包':
            payCode = '11112004'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doYyhCallbackMsg(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = TyContext.RunHttp.getRequestParam('platformOrderId', '')

        from tysdk.entity.pay.pay import TuyouPay
        result = TyContext.RunHttp.getRequestParam('result', '')
        if result != '1':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('doYyhCallbackMsg error, charge return error !!!')
            TuyouPay.deliveryChargeError(orderPlatformId, rparam, u'短信支付失败', 1)
            return '{result:{success:1,orderPlatformId:"' + orderPlatformId + '"}}'

        trade_status = 'TRADE_FINISHED'
        total_fee = -1
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return '{result:{success:1,orderPlatformId:"' + orderPlatformId + '"}}'
        else:
            return '{result:{success:0,orderPlatformId:"' + orderPlatformId + '"}}'
        pass
