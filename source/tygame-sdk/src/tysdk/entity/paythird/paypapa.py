#! encoding=utf-8

__author__ = 'yuejianqiang'

import hashlib

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayPapa(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
            'notifyUrl': 'http://open.touch4.me/v1/pay/papa/callback'
        }

    @classmethod
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        platformOrderId = rparams['app_order_id']
        TyContext.ftlog.debug('TuYouPayPapa->doCallback, rparams=', rparams)
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayPapa->ERROR, sign error !! rparam=', rparams)
            return 'failure'
        # do charge
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def check_sign(cls, rparams):
        app_key = rparams['app_key']
        sign = rparams['sign']
        # find payKey by appId
        papa_keys = TyContext.Configure.get_global_item_json('papa_keys', {})
        appSecret = papa_keys[app_key]['secretKey']
        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if sign != hashlib.md5('%s%s%s' % (app_key, appSecret, text)).hexdigest():
            return False
        return True
