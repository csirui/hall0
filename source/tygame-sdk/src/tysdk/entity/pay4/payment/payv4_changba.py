# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaVerify
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayChangbaV4(PayBaseV4):
    @payv4_order("changba")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
        }
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/changba/callback")
    def doCallback(cls, rpath):
        # convertArgsToDict
        rparams = TyContext.RunHttp.convertArgsToDict()
        transdata = rparams['transdata']
        transdata = json.loads(transdata)
        platformOrderId = transdata['cporderid']
        TyContext.ftlog.debug('TuYouPayChangba->doCallback,rparams=', rparams)
        if not cls.verify_sign(rparams):
            return 'failure'
        # do charge
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def verify_sign(cls, rparams):
        sign = rparams['sign']
        transdata = rparams['transdata']
        return rsaVerify(transdata, sign, 'changba')
