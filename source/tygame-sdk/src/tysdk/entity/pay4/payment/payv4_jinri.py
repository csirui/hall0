# -*- coding=utf-8 -*-

from tyframework.context import TyContext
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.payment.payv4_yipay_base import TuYouPayYiBase


class TuYouPayJinriV4(TuYouPayYiBase):
    @payv4_order('jinri')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        appId = chargeinfo['appId']
        buttonId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('jinri_prodids', {})
        data = prodconfig[str(appId)].get(str(buttonId), None)

        if data:
            payCode = data['feecode']
        else:
            raise PayErrorV4(1,
                             'can not find jinri product define of buttonId=' + buttonId
                             + ' clientId=' + chargeinfo['clientId'])

        chargeinfo['chargeData'] = {'msgOrderCode': payCode}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/jinri/callback')
    def doJinriCallback(cls, rpath):
        cls.do_yipay_callback('jinri')
