#! encoding=utf-8

__author__ = 'yuejianqiang'

import json
from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


class TuYouIIApple(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}

    @classmethod
    def doCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouIIApple callback with: %s' % rparam)
        iiapple_paykeys_new = TyContext.Configure.get_global_item_json('iiapple_paykeys_new', {})
        iiapple_paykeys = TyContext.Configure.get_global_item_json('iiapple_paykeys', {})

        orderPlatformId = rparam['gameExtend']
        chargeKey = 'sdk.charge:' + orderPlatformId
        state, chargeInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'state', 'charge')
        if state is None or not chargeInfo:
            secretKey = iiapple_paykeys['secretKey']

        chargeInfo = json.loads(chargeInfo)
        clientId = chargeInfo.get('clientId', '')
        for sub_clientid in iiapple_paykeys_new.keys():
            if clientId.find(sub_clientid) > 0:
                secretKey = iiapple_paykeys_new[sub_clientid]['secretKey']
                break
        else:
            secretKey = iiapple_paykeys['secretKey']

        ## verify sign
        keys = filter(lambda x: x != '_sign', rparam.keys())
        keys.sort()
        text = '&'.join(['%s=%s' % (x, rparam[x]) for x in keys])
        m = md5()
        m.update(text)
        m2 = md5()
        m2.update('%s%s' % (m.hexdigest().lower(), secretKey))
        if rparam['_sign'] != m2.hexdigest().lower():
            TyContext.ftlog.error('doIDOCallback->ERROR, sign error !! rparam=', rparam)
            return 'error'
        # do charge

        # from tysdk.entity.pay.pay import TuyouPay
        trade_status = rparam['status']
        # isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        isOk = PayHelper.callback_ok(orderPlatformId, -1, rparam)
        if isOk:
            return '{"status":0, "transIDO":"%s"}' % orderPlatformId
        else:
            return '{"status":1, "transIDO":"%s"}' % orderPlatformId
