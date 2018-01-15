# -*- coding=utf-8 -*-


from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayLiziV4(PayBaseV4):
    @payv4_order("lizi")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
            'notifyUrl': 'http://open.touch4.me/v1/pay/lizi/callback'
        }
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/lizi/callback")
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        platformOrderId = rparams['extend']
        TyContext.ftlog.debug('TuYouPayLizi->doCallback, rparams=', rparams)
        if not cls.verify_sign(rparams):
            return 'failure'
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def verify_sign(cls, rparams):
        sign = rparams['sign']
        appId = rparams['appId']
        platformOrderId = rparams['extend']
        lizi_keys = TyContext.Configure.get_global_item_json('lizi_keys', {})
        try:
            rparams['serverKey'] = lizi_keys[appId]['serverKey']
        except:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId, 'lizi')
            rparams['serverKey'] = config.get('serverKey')
        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s' % x[1], params)

        text = ''.join(params)
        calcSign = md5(text).hexdigest()
        if sign != calcSign:
            return False
        return True
