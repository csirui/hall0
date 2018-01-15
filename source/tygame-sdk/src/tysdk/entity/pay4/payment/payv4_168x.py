# -*- coding=utf-8 -*-
from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPay168XV4(PayBaseV4):
    @payv4_order('168x')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)

        config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('168x',
                                                                                              chargeinfo['packageName'],
                                                                                              chargeinfo['mainChannel'])
        if not config:
            appId = '9999'
            sdk = '168x'
            mainChannel = '168x'
            packageName = 'com.sdk.168x.default'
            config = GameItemConfigure(appId).get_game_channel_configure_by_package(sdk, packageName, mainChannel)
            import string
            import random
            salt = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        payData = {'randomstr': salt}
        chargeinfo['chargeData'] = payData
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/168x/callback')
    def do168xCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        signKey = ['game_key', 'game_orderno', 'nonce', 'subject', 'timestamp', 'total_fee']
        platformOrderId = rparam.get('game_orderno')
        signStr = '&'.join(k + '=' + str(rparam.get(k)) for k in signKey)
        config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId)
        if not config:
            appId = '9999'
            sdk = '168x'
            mainChannel = '168x'
            packageName = 'com.sdk.168x.default'
            config = GameItemConfigure(appId).get_game_channel_configure_by_package(sdk, packageName, mainChannel)
        secret = config.get('game_sceret')
        signStr = signStr + '&' + secret
        from hashlib import md5
        m = md5(signStr)
        if m.hexdigest().lower() != rparam.get('signature'):
            return 1
        PayHelperV4.callback_ok(platformOrderId, rparam.get('total_fee'), rparam)
        return 0
