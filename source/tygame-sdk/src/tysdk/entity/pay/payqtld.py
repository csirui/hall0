# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tyframework.orderids import orderid


class TuyouPayQtld(object):
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        appId = params['appId']
        prodId = params['prodId']
        prodconfig = TyContext.Configure.get_global_item_json('qtld_prodids', {})
        data = prodconfig[str(appId)].get(prodId, None)
        if data:
            amount = data['price']
            prodName = data['name']
        else:
            raise Exception('can not find qtld product define of prodId=' + prodId)
        payData = {'amount': amount, 'productId': prodId, 'productName': prodName}
        params['payData'] = payData
        mo.setResult('payData', payData)

    @classmethod
    def doQtldCallback(cls, rpath):
        TyContext.ftlog.info('doQtldCallback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderPlatformId = rparam['extra']
            appId = orderid.get_appid_frm_order_id(orderPlatformId)
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doQtldCallback->ERROR, param error !! rparam=', rparam)
            return "0"

        paykey_dict = TyContext.Configure.get_global_item_json('qtld_paykeys', {})
        paykey = str(paykey_dict[str(appId)])
        # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            TyContext.ftlog.error('TuyouPayQltd.doQltdCallbacksign verify error !!')
            return "0"

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            return "1"
        else:
            return "0"

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        check_str = ''.join(k + "=" + rparam[k] for k in sorted(rparam.keys()) if k != 'sign') + paykey
        digest = md5(check_str).hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuyouPayQltd verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
