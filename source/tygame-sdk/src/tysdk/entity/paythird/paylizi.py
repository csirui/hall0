# -*- coding=utf-8 -*-


from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayLizi(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
            'notifyUrl': 'http://open.touch4.me/v1/pay/lizi/callback'
        }

    @classmethod
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        platformOrderId = rparams['extend']
        TyContext.ftlog.debug('TuYouPayLizi->doCallback, rparams=', rparams)
        if not cls.verify_sign(rparams):
            return 'failure'
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def verify_sign(cls, rparams):
        sign = rparams['sign']
        appId = rparams['appId']

        lizi_keys = TyContext.Configure.get_global_item_json('lizi_keys', {})
        rparams['serverKey'] = lizi_keys[appId]['serverKey']

        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s' % x[1], params)

        text = ''.join(params)
        calcSign = md5(text).hexdigest()
        if sign != calcSign:
            return False
        return True
