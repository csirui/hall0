# -*- coding=utf-8 -*-


from hashlib import md5

from tyframework.context import TyContext
from tyframework.orderids import orderid


class TuYouPayDuoKu():
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        appId = params['appId']
        prodId = params['prodId']
        prodconfig = TyContext.Configure.get_global_item_json('duoku_prodids', {})
        data = prodconfig[str(appId)].get(prodId, None)
        if data:
            data['payData']['amount'] = data['price']
            data['payData']['prodName'] = data['name']
            payData = data['payData']
        else:
            raise Exception('can not find duoku product define of prodId=' + prodId)

        mo.setResult('payData', payData)
        pass

    @classmethod
    def doDuoKuCallbackMsg(self, rpath):
        TyContext.ftlog.info('doDuoKuCallback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderPlatformId = rparam['cpdefinepart']
            appId = orderid.get_appid_frm_order_id(orderPlatformId)
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doDuoKuCallback->ERROR, param error !! rparam=', rparam)
            return "failure"

        paykey_dict = TyContext.Configure.get_global_item_json('duoku_paykeys', {})
        paykey = str(paykey_dict[str(appId)])
        # 签名校验
        if not self.__verify_sign(rparam, paykey, sign):
            TyContext.ftlog.error('TuYouPayDuoKu.doDuoKuCallbacksign verify error !!')
            return "failure"

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            return "success"
        else:
            return "failure"

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        check_str = (rparam['appid']
                     + rparam['orderid']
                     + rparam['amount']
                     + rparam['unit']
                     + rparam['status']
                     + rparam['paychannel']
                     + paykey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayDuoKu verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
