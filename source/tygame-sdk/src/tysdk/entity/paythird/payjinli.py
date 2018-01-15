# -*- coding=utf-8 -*-

from urllib import unquote

from Crypto.PublicKey import RSA

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto, _jinli_pubkey_py


class TuYouPayJinli(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {}

    @classmethod
    def doJinliCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doJinliCallback', rparam)
        try:
            orderPlatformId = rparam['out_order_no']
            total_fee = rparam['deal_price']
        except Exception as e:
            TyContext.ftlog.error('doJinliCallback  ,param err,exception ', e)
            return 'exception in params'
        if not cls._check_sign(rparam):
            TyContext.ftlog.error('doJinliCallback ,check sign error!')
            return 'check sign error!'
        PayHelper.callback_ok(orderPlatformId, float(total_fee), rparam)
        return 'success'

    @classmethod
    def _check_sign(cls, rparam):
        sigdata = "&".join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) \
                           if k != 'sign')
        si = unquote(rparam['sign'])
        TyContext.ftlog.info('doJinliCallback  ,param err,exception si', si)
        appkeyconfig = TyContext.Configure.get_global_item_json('jinli_config', {})
        if 'api_key' in rparam and appkeyconfig:
            for item in appkeyconfig:
                if 0 == cmp(rparam['api_key'], item['appKey']):
                    jinli_pubkey_py = RSA.importKey(item['publicKey'])
                    break
        else:
            jinli_pubkey_py = _jinli_pubkey_py
        return _verify_with_publickey_pycrypto(sigdata, si, jinli_pubkey_py)
