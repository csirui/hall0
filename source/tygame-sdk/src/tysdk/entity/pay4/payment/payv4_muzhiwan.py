# -*- coding=utf-8 -*-

from tyframework.context import TyContext
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayMuzhiwanV4(PayBaseV4):
    @payv4_order("muzhiwan")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        appId = chargeinfo['appId']
        buttonId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('muzhiwan_prodids', {})
        data = prodconfig[str(appId)].get(str(buttonId), None)

        if data:
            payCode = data['feecode']
        else:
            raise Exception('can not find muzhiwan product define of buttonId=' + buttonId)

        chargeinfo['chargeData'] = {'msgOrderCode': payCode}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/muzhiwan/callback")
    def doMuzhiwanCallback(cls, rpath):
        from payyi import TuYouPayYi
        return TuYouPayYi.do_yipay_callback('muzhiwan')
