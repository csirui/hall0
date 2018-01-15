#! encoding=utf-8
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
import hashlib

from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayPapaV4(PayBaseV4):
    @payv4_order("papa")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
            'notifyUrl': 'http://open.touch4.me/v1/pay/papa/callback'
        }
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/papa/callback")
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        platformOrderId = rparams['app_order_id']
        TyContext.ftlog.debug('TuYouPayPapa->doCallback, rparams=', rparams)
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayPapa->ERROR, sign error !! rparam=', rparams)
            return 'failure'
        # do charge
        ChargeModel.save_third_pay_order_id(platformOrderId, rparams.get('pa_open_order_id', ''))
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def check_sign(cls, rparams):
        app_key = rparams['app_key']
        sign = rparams['sign']
        # find payKey by appId
        papa_keys = TyContext.Configure.get_global_item_json('papa_keys', {})
        try:
            appSecret = papa_keys[app_key]['secretKey']
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(rparams['app_order_id'], 'papa')
            appSecret = config.get('papa_secret', '')
        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if sign != hashlib.md5('%s%s%s' % (app_key, appSecret, text)).hexdigest():
            return False
        return True
