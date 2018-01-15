# -*- coding=utf-8 -*-

from urllib import unquote

from Crypto.PublicKey import RSA

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto, _jinli_pubkey_py
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayJinliV4(PayBaseV4):
    @payv4_order('jinli')
    def charge_data(self, mi):
        return self.handle_order(mi)

    @payv4_callback('/open/ve/pay/jinli/callback')
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
        PayHelperV4.callback_ok(orderPlatformId, float(total_fee), rparam)
        return 'success'

    def _check_sign(self, rparam):
        sigdata = "&".join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) \
                           if k != 'sign')
        si = unquote(rparam['sign'])
        TyContext.ftlog.info('doJinliCallback  ,param err,exception si', si)
        appkeyconfig = TyContext.Configure.get_global_item_json('jinli_config', {})
        jinli_pubkey_py = ""
        if 'api_key' in rparam and appkeyconfig:
            for item in appkeyconfig:
                if 0 == cmp(rparam['api_key'], item['appKey']):
                    jinli_pubkey_py = RSA.importKey(item['publicKey'])
                    break
        if not jinli_pubkey_py:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(rparam['out_order_no'])
            TyContext.ftlog.debug('jinli getsdkconfig -->', config)
            jinli_pubkey_py = config.get('jinli_publicKey', "")
            if jinli_pubkey_py:
                jinli_pubkey_py = self.loadRsaPublicKey(jinli_pubkey_py)
                jinli_pubkey_py = RSA.importKey(jinli_pubkey_py)
            else:
                jinli_pubkey_py = _jinli_pubkey_py
        return _verify_with_publickey_pycrypto(sigdata, si, jinli_pubkey_py)
