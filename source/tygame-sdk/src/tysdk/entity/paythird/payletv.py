# -*- coding=utf-8 -*-

from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayLetv(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId']
        }

    @classmethod
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayLetv->doCallback, rparams=', rparams)
        order_id = rparams['cooperator_order_no']
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayLetv->ERROR, sign error !! rparam=', rparams)
            return 'fail'

        # do charge
        is_ok = PayHelper.callback_ok(order_id, -1, rparams)
        if is_ok:
            return 'success'
        else:
            return 'fail'

    @classmethod
    def check_sign(cls, rparams):
        app_id = rparams['app_id']
        sign = rparams['sign']
        config = TyContext.Configure.get_global_item_json('letv_keys', {})
        app_key = config[app_id]['scrkey']

        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if sign != md5('%s&key=%s' % (text, app_key)).hexdigest():
            return False
        else:
            return True
