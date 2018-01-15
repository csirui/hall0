#! encoding=utf-8

__author__ = 'yuejianqiang'

import hashlib
import json

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayKuaiwan(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
        }

    @classmethod
    def doCallback(cls, rpath):
        data = TyContext.RunHttp.get_body_content()
        rparams = json.loads(data)
        platformOrderId = rparams['orderId']
        TyContext.ftlog.debug('TuYouPayKuaiwan->doCallback, rparams=', rparams)
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayKuaiwan->ERROR, sign error !! rparam=', rparams)
            return 'failure'
        # do charge
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def check_sign(cls, rparams):
        appId = rparams['appId']
        sign = rparams['sign']
        kuaiwan_keys = TyContext.Configure.get_global_item_json('kuaiwan_keys', {})
        appKey = kuaiwan_keys[appId]['appKey']
        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if sign != hashlib.md5('%s%s' % (text, appKey)).hexdigest():
            return False
        return True
