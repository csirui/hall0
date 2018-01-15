# -*- coding=utf-8 -*-


from tyframework.context import TyContext


class TuYouPayYdMmTy():
    @classmethod
    def doBuyStraight(self, userId, params, mo):

        #         gameId = 6
        #         config redis/config/GenConfigT3Card.py
        #         codemap = ConfigItems.getGameItemJson( gameId, 'pay.code.map',
        #                                               {'DEFAULT': '30000763429602',
        #                                                'T20K' : '30000763429601'})
        prodId = params['prodId']

        #         if prodId in codemap :
        #             payCode = codemap[prodId]
        #         else:
        #             payCode = codemap['DEFAULT']

        payCode = '30000763429602'
        if prodId == 'T20K':
            payCode = '30000763429601'
        if prodId == 'T50K':
            payCode = '30000763429602'
        if prodId == 'T100K':
            payCode = '30000763429603'
        if prodId == 'T300K':
            payCode = '30000763429610'
        if prodId == 'MOONKEY':
            payCode = '30000763429607'
        if prodId == 'MOONKEY3':
            payCode = '30000763429608'
        if prodId == 'VOICE100':
            payCode = '30000763429609'
        if prodId == 'RAFFLE':
            payCode = '30000763429606'
        if prodId == 'ONHOOK':
            payCode = '30000763429601'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doYdMmTyCallbackMsg(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = TyContext.RunHttp.getRequestParam('platformOrderId', '')

        from tysdk.entity.pay.pay import TuyouPay
        result = TyContext.RunHttp.getRequestParam('result', '')
        if result != '1':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('doYdMmTyCallbackMsg error, charge return error !!!')
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
