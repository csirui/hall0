# -*- coding=utf-8 -*-
import json
from urllib import unquote

from OpenSSL.crypto import load_privatekey, FILETYPE_PEM
from datetime import datetime

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto, _sign_with_privatekey_openssl
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayJinliOnlineV4(PayBaseV4):
    @payv4_order('jinlionline')
    def charge_data(self, mi):
        chargeInfo = self.get_charge_info(mi)
        appId = chargeInfo['appId']
        # check config
        packageName = chargeInfo['packageName']
        changeName = chargeInfo['channelName']
        config = GameItemConfigure(appId).get_sdk_configure(changeName, packageName, 'jinli')
        jinli_privateKey = config['jinli_privateKey']
        ###
        rparams = {
            'player_id': mi.getParamStr('player_id'),
            'api_key': mi.getParamStr('api_key'),
            'deal_price': str(chargeInfo['chargeTotal']),
            'deliver_type': '1',
            'notify_url': PayHelper.getSdkDomain() + '/open/ve/pay/jinlionline/callback',
            'out_order_no': chargeInfo['platformOrderId'],
            'subject': chargeInfo['buttonName'],
            'submit_time': datetime.now().strftime('%Y%m%d%H%M%S'),
            'total_fee': str(chargeInfo['chargeTotal']),
        }
        pairs = filter(lambda x: x[0] not in ['player_id'], rparams.items())
        pairs.sort()
        data = ''.join(['%s' % x[1] for x in pairs])
        # calc sign
        privateKey = load_privatekey(FILETYPE_PEM, self.loadRsaPrivateKey(jinli_privateKey))
        sign = _sign_with_privatekey_openssl(data, privateKey)
        rparams['sign'] = sign
        # create order
        url = 'https://pay.gionee.com/order/create'
        response, purl = TyContext.WebPage.webget(url, postdata_=json.dumps(rparams), method_="POST");
        chargeInfo['chargeData'] = json.loads(response)
        return self.return_mo(0, chargeInfo=chargeInfo)

    @payv4_callback('/open/ve/pay/jinlionline/callback')
    def doJinliCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doJinliOnlineCallback', rparam)

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
        platformOrderId = rparam['out_order_no']
        chargeInfo = self.load_order_charge_info(platformOrderId)
        appId = chargeInfo['appId']
        packageName = chargeInfo['packageName']
        changeName = chargeInfo['channelName']
        config = GameItemConfigure(appId).get_sdk_configure(changeName, packageName, 'jinli')
        jinli_publicKey = config['jinli_publicKey']
        return _verify_with_publickey_pycrypto(sigdata, si, self.loadRsaPublicKey(jinli_publicKey))
