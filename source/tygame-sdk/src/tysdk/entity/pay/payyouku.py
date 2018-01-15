# -*- coding=utf-8 -*-

import hmac
import json
import urllib

from tyframework.context import TyContext
from tyframework.orderids import orderid


class TuyouPayYouku(object):
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        appId = params['appId']
        prodId = params['prodId']
        prodconfig = TyContext.Configure.get_global_item_json('youku_prodids', {})
        data = prodconfig[str(appId)].get(prodId, None)
        if data is None:
            raise Exception('can not find youku product define of prodId=' + prodId)
        amount = data['price']
        prodName = data['name']
        payData = {'amount': amount, 'productId': prodId, 'productName': prodName}
        params['payData'] = payData
        mo.setResult('payData', payData)
        from tysdk.entity.paythird.helper import PayHelper
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/youku/callback'
        TyContext.ftlog.debug('TuyouPayYouku doBuyStraight callback url=', notifyurl)
        mo.setResult('notifyUrl', notifyurl)

    @classmethod
    def doYoukuCallback(cls, rpath):
        cb_rsp = {}
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderPlatformId = rparam['apporderID']
            appId = orderid.get_appid_frm_order_id(orderPlatformId)
            price = rparam['price']
            uid = rparam['uid']
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doYoukuCallback->ERROR, param error !! rparam=', rparam)
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '参数错误'
            return json.dumps(cb_rsp)

        paykey_dict = TyContext.Configure.get_global_item_json('youku_paykeys', {})
        paykey = str(paykey_dict[str(appId)])
        # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            TyContext.ftlog.error('TuyouPayYouku.doYoukuCallback sign verify error !!')
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '签名验证失败'
            return json.dumps(cb_rsp)

        try:
            result = int(rparam['result'])
            success_amount = rparam['success_amount']
            if result < 1 or result > 2:
                TyContext.ftlog.error('doYoukuCallback got failed result:', result)
                cb_rsp['status'] = 'failed'
                cb_rsp['desc'] = 'result(%d) is not 1 or 2' % result
                return json.dumps(cb_rsp)
            if result == 2:
                TyContext.ftlog.error('doYoukuCallback got partial success result:'
                                      'success_amount is', success_amount)
        except:
            pass

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            cb_rsp['status'] = 'success'
            cb_rsp['desc'] = '发货成功'
            return json.dumps(cb_rsp)
        else:
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '发货失败'
            return json.dumps(cb_rsp)

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        from tysdk.entity.paythird.helper import PayHelper
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/youku/callback'
        sorted_args = [('apporderID', rparam['apporderID']),
                       ('price', rparam['price']), ('uid', rparam['uid'])]
        encoded_args = urllib.urlencode(sorted_args)
        check_str = notifyurl + '?' + encoded_args
        check_sign = hmac.new(paykey)
        check_sign.update(check_str)
        digest = check_sign.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuyouPayYouku verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
