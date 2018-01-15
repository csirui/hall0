# -*- coding=utf-8 -*-
import json

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaVerify
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayWandoujiadanji(PayBaseV4):
    @payv4_order("wandoujiadanji")
    def charge_data(cls, mi):
        charge_info = cls.get_charge_info(mi)
        return cls.return_mo(0, chargeInfo=charge_info)

    @payv4_callback("/open/ve/pay/wandoujiadanji/callback")
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()

        content = rparams['content']
        content_json = json.loads(content)
        orderId = content_json['out_trade_no']

        if not cls.verify_sign(rparams):
            TyContext.ftlog.info('TuYouPayWandoujiadanji->sign verify ERROR')
            return "fail"

        total_fee = int(float(content_json['money']))
        total_fee = int(total_fee / 100)
        ChargeModel.save_third_pay_order_id(orderId, content_json.get('orderId', ''))
        is_ok = PayHelperV4.callback_ok(orderId, total_fee, rparams)
        if is_ok:
            return 'success'
        else:
            return 'fail'

    @classmethod
    def verify_sign(cls, rparams):
        sign = rparams['sign']
        data = rparams['content']
        # wandoujiadanji跟wandoujia使用的是同一个公钥
        if rsaVerify(data, sign, 'wandoujia'):
            return True
        return False
