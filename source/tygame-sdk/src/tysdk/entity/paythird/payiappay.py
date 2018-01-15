# -*- coding=utf-8 -*-

import json

from Crypto.PublicKey import RSA

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto_md5


class TuYooIappay(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appid = chargeinfo['payInfo']['appid']['iappay']
        iappayConfig = TyContext.Configure.get_global_item_json('iappay_config', {})
        appKey = iappayConfig[appid]['appkey']
        try:

            if 'diamondId' in chargeinfo:
                waresid = iappayConfig[appid]['payConfig'][chargeinfo['diamondId']]
            elif 'buttonId' in chargeinfo:
                waresid = iappayConfig[appid]['payConfig'][chargeinfo['buttonId']]
            elif 'prodId' in chargeinfo:
                waresid = iappayConfig[appid]['payConfig'][chargeinfo['prodId']]
            else:
                waresid = None
        except:
            waresid = None
        if not appKey:
            TyContext.ftlog.error('TuYooIappay this id has no key , id ', appid)

        if not waresid:
            TyContext.ftlog.error('TuYooIappay this prodId has no waresid , chargeinfo ', chargeinfo)
        chargeinfo['chargeData'] = {'waresid': waresid, 'appKey': appKey}

    @classmethod
    def doIappayPayCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        transdata = rparam['transdata']
        transdata = json.loads(transdata)
        sign = rparam['sign']
        appid = transdata['appid']
        signtype = rparam['signtype']
        iappayConfig = TyContext.Configure.get_global_item_json('iappay_config', {})
        try:
            pubkey = iappayConfig[appid]['pubkey']
            orderPlatformId = transdata['cporderid']
            total_fee = transdata['money']
            result = transdata['result']
        except Exception as e:
            TyContext.ftlog.error('doIappayPayCallback->ERROR, exception', e, 'rparam', transdata)
            return 'error'
        if not cls._verify_sign(rparam, sign, pubkey):
            errinfo = '支付失败'
            PayHelper.callback_error(orderPlatformId, errinfo, rparam)
            return 'failed'

        if result != 0:
            errinfo = '支付失败'
            TyContext.ftlog.error('doIappayPayCallback->ERROR, exception, result not 0')
            PayHelper.callback_error(orderPlatformId, errinfo, rparam)
            return 'failed'
        PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        return 'success'

    @classmethod
    def _verify_sign(cls, rparam, sign, pubkey):
        # data = "&".join(k + "=" + str(rparam[k]) for k in rparam.keys())
        data = str(rparam['transdata'])
        key = RSA.importKey(pubkey)
        TyContext.ftlog.error('doIappayPayCallback->ERROR, exception', data, sign, key)
        return _verify_with_publickey_pycrypto_md5(data, sign, key)
