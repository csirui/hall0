# -*- coding=utf-8 -*-
'''
Created on 2014-11-3

@author: Administrator
'''

from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPay16WifiV4(PayBaseV4):
    @payv4_order('16wifi')
    def charge_data(self, mi):
        return self.handle_order(mi)

    @payv4_callback('/open/ve/pay/16game/callback')
    def doVivoCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        appId = rparams.get('verdorCode')
        platformOrderId = rparams.get('orderId')
        config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId, '16wifi')

        md5key = config.get('16wifi_key')

        signStr = '&'.join(k + '=' + rparams[k] for k in sorted(rparams.keys()) if rparams[k] and k != 'sign')

        signStr += '&key=%s' % md5key
        m = md5(signStr)
        if m.hexdigest().upper() != rparams['sign']:
            return {
                'ReturnCode': 1
            }
        total_fee = rparams.get('cashAmount')
        ChargeModel.save_third_pay_order_id(platformOrderId, rparams.get('payCode'))
        PayHelperV4.callback_ok(platformOrderId, total_fee, rparams)
        return {
            'ReturnCode': 200
        }
