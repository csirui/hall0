# -*- coding=utf-8 -*-

import json

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaVerify


class TuYouPayChangba(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
        }

    @classmethod
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
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def verify_sign(cls, rparams):
        sign = rparams['sign']
        transdata = rparams['transdata']
        return rsaVerify(transdata, sign, 'changba')
