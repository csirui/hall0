#! encoding=utf-8
from tysdk.entity.user3.account_login import AccountLogin

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
from helper import PayHelper
import hashlib
import base64
import json


class TuYouPayMumayi(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId'], }
        mumayi_keys = TyContext.Configure.get_global_item_json('mumayi_keys', {})
        packageName = chargeinfo['packageName']
        appKey = mumayi_keys[packageName]
        userId = chargeinfo['uid']
        chargeKey = 'sdk.charge:mumayi:%s' % userId
        TyContext.RedisPayData.execute('HMSET', chargeKey, 'platformOrderId', chargeinfo['platformOrderId'], 'appKey',
                                       appKey)

    @classmethod
    def doCallback(cls, rpath):
        postData = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.debug('TuYouPayMumayi->doCallback, postData=', postData)
        try:
            rparams = json.loads(postData)
        except:
            TyContext.ftlog.error('TuYouPayMumayi->callback, json error !! postData=', postData)
            return 'error'
        # orderPlatformId = rparams['orderID']
        uid = rparams['uid']
        userId = AccountLogin.__find_userid_by_snsid__('mumayi:%s' % uid)
        chargeKey = 'sdk.charge:mumayi:%s' % userId
        platformOrderId, appKey = TyContext.RedisPayData.execute('HMGET', chargeKey, 'platformOrderId', 'appKey')
        TyContext.ftlog.debug('TuYouPayMumayi->get order info:',
                              'userId=%s platformOrderId=%s appKey=%s' % (userId, platformOrderId, appKey))
        # payType = rparams['payType']
        # productName = rparams['productName']
        # productPrice = rparams['productPrice']
        # productDesc = rparams['productDesc']
        # orderTime = rparams['orderTime']
        # tradeSign = rparams['tradeSign']
        # tradeState = rparams['tradeState']
        if not cls.check_pay(rparams, appKey):
            TyContext.ftlog.error('doIDOCallback->ERROR, sign error !! rparam=', rparams)
            return 'error'
        # do charge
        # from tysdk.entity.pay.pay import TuyouPay
        # trade_status = rparams['status']
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'error'

    @classmethod
    def check_pay(cls, data, appKey):
        sign = data.get("tradeSign")
        orderID = data.get("orderID")
        if sign < 14:
            return False
        vstr = sign[0:8]
        dvstr = sign[8:]
        mds = hashlib.md5(dvstr).hexdigest()
        if vstr != mds[0:8]:
            return False

        key_b = dvstr[0:6]
        randkey = "%s%s" % (key_b, appKey)
        randkey = hashlib.md5(randkey).hexdigest()
        dv = cls._check_b64(dvstr[6:])
        dvlen = len(dv)
        st = ""
        for i in range(dvlen):
            st += chr(ord(dv[i]) ^ ord(randkey[i % 32]))
        if st == orderID:
            return True
        return False

    @classmethod
    def _check_b64(cls, strg):
        missing_padding = 4 - len(strg) % 4
        if missing_padding:
            strg += b'=' * missing_padding
        result = base64.b64decode(strg)
        return result
