# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayPPS(object):
    @classmethod
    def charge_data(self, chargeinfo):
        chargeinfo['chargeData'] = {'fake': 'data'}

    @classmethod
    def doPPSCallback(cls, rpath):
        cb_rsp = {}
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderPlatformId = rparam['userData'].split(',')[0]
            appId = rparam['userData'].split(',')[1]
            price = rparam['money']
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doPPSCallback->ERROR, param error !! rparam=', rparam)
            cb_rsp['result'] = '-2'
            cb_rsp['message'] = 'Parameters error'
            return json.dumps(cb_rsp)

        paykey_dict = TyContext.Configure.get_global_item_json('pps_paykeys', {})
        paykey = str(paykey_dict[str(appId)])

        # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            TyContext.ftlog.error('TuYouPayPPS.doPPSCallback sign verify error !!')
            cb_rsp['result'] = '-1'
            cb_rsp['message'] = 'Sign error'
            return json.dumps(cb_rsp)

        total_fee = float(price)
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            cb_rsp['result'] = '0'
            cb_rsp['message'] = 'success'
            return json.dumps(cb_rsp)
        else:
            cb_rsp['result'] = '-6'
            cb_rsp['message'] = 'Other errors'
            return json.dumps(cb_rsp)

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        check_str = (rparam['user_id'] +
                     rparam['role_id'] +
                     rparam['order_id'] +
                     rparam['money'] +
                     rparam['time'] +
                     paykey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        if digest != sign.lower():
            TyContext.ftlog.error('TuYouPayPPS verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
