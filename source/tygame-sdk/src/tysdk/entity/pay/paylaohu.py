# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext


class TuYouPayLaoHu():
    # 订单签名验证key
    sign_skey = 'TUYOU!Qaz2wsxLaoHu'

    @classmethod
    def doLaoHuCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = TyContext.RunHttp.getRequestParam('platformOrderId', '')

        result = TyContext.RunHttp.getRequestParam('result', '')
        sign = TyContext.RunHttp.getRequestParam('sign', '')

        # tSign = 'orderid='+orderPlatformId+'&result='+result+'&key='+TuYouPayLaoHu.sign_skey
        tSign = orderPlatformId + result + TuYouPayLaoHu.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign.upper():
            TyContext.ftlog.info('doLaoHuCallback->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '{result:{success:0,orderPlatformId:"' + orderPlatformId + '"}}'

        from tysdk.entity.pay.pay import TuyouPay

        if result != '1':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('doLaoHuCallback error, charge return error !!!')
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
