#! encoding=utf-8
from Crypto.PublicKey import RSA

from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto_md5

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
from helper import PayHelper
import json


class TuYouPayCoolpad(object):
    ORDER_URL = 'http://pay.coolyun.com:6988/payapi/order'

    @classmethod
    def charge_data(cls, chargeinfo):
        packageName = chargeinfo['packageName']
        userId = int(chargeinfo['uid'])
        snsId, snsinfo = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%s' % userId, 'snsId', 'snsinfo')
        coolpad_keys = TyContext.Configure.get_global_item_json('coolpad_keys', {})
        for appId, appInfo in coolpad_keys.items():
            if appId == 'publicKey':
                continue
            if isinstance(appInfo, dict) and appInfo.get('package') == packageName:
                break
        else:
            TyContext.ftlog.error('TuYouPayCoolpad package not found ', packageName)
            return
        appId = appInfo['appId']
        appKey = appInfo['appKey']
        try:
            if 'diamondId' in chargeinfo:
                waresid = chargeinfo['diamondId']
            elif 'buttonId' in chargeinfo:
                waresid = chargeinfo['buttonId']
            elif 'prodId' in chargeinfo:
                waresid = chargeinfo['prodId']
            else:
                waresid = None
            waresid = appInfo['products'][waresid]
        except:
            TyContext.ftlog.error('TuYouPayCoolpad product not found ', chargeinfo)
            return
        if not appKey:
            TyContext.ftlog.error('TuYooIappay this id has no key , id ', appId)

        if not waresid:
            TyContext.ftlog.error('TuYooIappay this prodId has no waresid , chargeinfo ', chargeinfo)
            return
        chargeinfo['chargeData'] = {'callback': 'http://open.touch4.me/v1/pay/coolpad/callback', 'waresid': waresid,
                                    'appKey': appKey, 'openID': snsId[len('coolpad:'):], 'authToken': snsinfo}

    @classmethod
    def doCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        transdata = rparam['transdata']
        transdata = json.loads(transdata)
        sign = rparam['sign']
        appid = transdata['appid']
        signtype = rparam['signtype']
        coolpad_keys = TyContext.Configure.get_global_item_json('coolpad_keys', {})
        pubkey = coolpad_keys[appid]['publicKey']
        try:
            orderPlatformId = transdata['cporderid']
            # total_fee = transdata['money']
            result = transdata['result']
        except Exception as e:
            TyContext.ftlog.error('doCoolpadPayCallback->ERROR, exception', e, 'rparam', transdata)
            return 'error'
        if not cls._verify_sign(rparam, sign, pubkey):
            errinfo = '支付失败'
            PayHelper.callback_error(orderPlatformId, errinfo, rparam)
            return 'failed'

        if result != 0:
            errinfo = '支付失败'
            TyContext.ftlog.error('doCoolpadPayCallback->ERROR, exception, result not 0')
            PayHelper.callback_error(orderPlatformId, errinfo, rparam)
            return 'failed'
        PayHelper.callback_ok(orderPlatformId, -1, rparam)
        return 'success'

    @classmethod
    def _verify_sign(cls, rparam, sign, pubkey):
        # data = "&".join(k + "=" + str(rparam[k]) for k in rparam.keys())
        data = str(rparam['transdata'])
        key = RSA.importKey(pubkey)
        TyContext.ftlog.error('doCoolpadPayCallback->ERROR, exception', data, sign, key)
        return _verify_with_publickey_pycrypto_md5(data, sign, key)
