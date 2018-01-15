# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayPPSV4(PayBaseV4):
    @payv4_order('pps')
    def charge_data(self, mi):
        return self.handle_order(mi)

    @payv4_callback('/open/ve/pay/pps/callback')
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
        try:
            paykey = str(paykey_dict[str(appId)])
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'pps')
            paykey = config.get('pps_payKey', "")
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
