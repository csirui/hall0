#! encoding=utf-8
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
import hashlib
import json
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayKuaiwanV4(PayBaseV4):
    @payv4_order("kuaiwan")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
        }
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/kuaiwan/callback")
    def doCallback(cls, rpath):
        data = TyContext.RunHttp.get_body_content()
        rparams = json.loads(data)
        platformOrderId = rparams['orderId']
        TyContext.ftlog.debug('TuYouPayKuaiwan->doCallback, rparams=', rparams)
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayKuaiwan->ERROR, sign error !! rparam=', rparams)
            return 'failure'
        # do charge
        ChargeModel.save_third_pay_order_id(platformOrderId, rparams.get('trade_sn', ''))
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def check_sign(cls, rparams):
        appId = rparams['appId']
        sign = rparams['sign']
        kuaiwan_keys = TyContext.Configure.get_global_item_json('kuaiwan_keys', {})
        try:
            appKey = kuaiwan_keys[appId]['appKey']
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(rparams['orderId'], 'kuaiwan')
            appKey = config.get('kuaiwan_appKey', "")
        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if sign != hashlib.md5('%s%s' % (text, appKey)).hexdigest():
            return False
        return True
