#! encoding=utf-8

__author__ = 'yuejianqiang'

import hashlib
import json

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayPengyouwan(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId'], }

    @classmethod
    def doCallback(cls, rpath):
        postData = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.debug('TuYouPayPengyouwan->doCallback, postData=', postData)
        try:
            rparams = json.loads(postData)
        except:
            TyContext.ftlog.error('TuYouPayPengyouwan->callback, json error !! postData=', postData)
            return 'error'
        platformOrderId = rparams['cp_orderid']
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('doIDOCallback->ERROR, sign error !! rparam=', rparams)
            return 'error'
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return '{"ack":200, "msg":"Ok"}'
        else:
            return '{"ack":500, "msg":"Error"}'

    @classmethod
    def check_sign(cls, rparams):
        cp_orderid = rparams['cp_orderid']
        ch_orderid = rparams['ch_orderid']
        amount = rparams['amount']
        gameKey = rparams['gamekey']
        pengyouwan_keys = TyContext.Configure.get_global_item_json('pengyouwan_keys', {})
        apiSecret = pengyouwan_keys[gameKey]
        sign = rparams['sign']
        if sign != hashlib.md5('%s%s%s%s' % (apiSecret, cp_orderid, ch_orderid, amount)).hexdigest():
            return False
        return True
