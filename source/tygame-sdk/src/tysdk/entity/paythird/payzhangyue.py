# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayZhangYue(object):
    @classmethod
    def charge_data(self, chargeinfo):
        chargeinfo['chargeData'] = {}

    @classmethod
    def doZhangYueCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        try:
            appId = rparam['appId']
            transData = json.loads(rparam['transData'])
            orderPlatformId = transData['merOrderId']
            price = transData['payAmt']
            sign = transData['md5SignValue']
        except:
            TyContext.ftlog.info('doZhangYueCallback->ERROR, param error !! rparam=', rparam)
            return 'error'

        paykey_dict = TyContext.Configure.get_global_item_json('zhangyue_paykeys', {})
        paykey = str(paykey_dict[str(appId)])

        # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            TyContext.ftlog.error('TuYouPayZhangYue.doZhangYueCallback sign verify error !!')
            return 'error'

        total_fee = float(price)
        rparam['chargeType'] = 'zhangyue'
        rparam['third_orderid'] = transData['orderId']
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'success'
        else:
            return 'error'

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        transData = json.loads(rparam['transData'])
        check_str = (rparam['merId'] + '|' +
                     rparam['appId'] + '|' +
                     transData['orderId'] + '|' +
                     transData['payAmt'] + '|' +
                     paykey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        if digest != sign.lower():
            TyContext.ftlog.error('TuYouPayZhangYue verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
