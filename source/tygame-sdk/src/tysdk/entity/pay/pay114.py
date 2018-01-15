# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tyframework.orderids import orderid


class TuyouPay114(object):
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        appId = params['appId']
        prodId = params['prodId']
        prodconfig = TyContext.Configure.get_global_item_json('114_prodids', {})
        data = prodconfig[str(appId)].get(prodId, None)
        if data:
            amount = data['price']
            prodName = data['name']
        else:
            raise Exception('can not find 114 product define of prodId=' + prodId)
        payData = {'amount': amount, 'productId': prodId, 'productName': prodName}
        params['payData'] = payData
        mo.setResult('payData', payData)

    @classmethod
    def do114Callback(cls, rpath):
        TyContext.ftlog.info('do114Callback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderPlatformId = rparam['cpOrderId']
            appId = orderid.get_appid_frm_order_id(orderPlatformId)
            sign = rparam['signature']
        except:
            TyContext.ftlog.info('do114Callback->ERROR, param error !! rparam=', rparam)
            return "failure"

        paykey_dict = TyContext.Configure.get_global_item_json('114_paykeys', {})
        appkey = str(paykey_dict[str(appId)]['appkey'])
        appsecret = str(paykey_dict[str(appId)]['appsecret'])
        # 签名校验
        if not cls.__verify_sign(rparam, appkey, appsecret, sign):
            TyContext.ftlog.error('TuyouPay114.do114Callbacksign verify error !!')
            return "failure"

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            return "success"
        else:
            return "failure"

    @classmethod
    def __verify_sign(cls, rparam, appkey, appsecret, signature):
        check_str = ('amount=' + rparam['amount']
                     + '&appKey=' + appkey
                     + '&appSecret=' + appsecret
                     + '&cpOrderId=' + rparam['cpOrderId']
                     + '&orderId=' + rparam['orderId']
                     + '&paymethod=' + rparam['paymethod']
                     + '&status=' + rparam['status'])
        sign = signature.lower()
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        if digest != sign:
            TyContext.ftlog.error('TuyouPay114 verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
