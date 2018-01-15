# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayLetvV4(PayBaseV4):
    @payv4_order("letv")
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId']
        }
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/letv/callback')
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayLetv->doCallback, rparams=', rparams)
        order_id = rparams['cooperator_order_no']
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayLetv->ERROR, sign error !! rparam=', rparams)
            return 'fail'
        ChargeModel.save_third_pay_order_id(order_id, rparams.get('lepay_order_no', ''))
        # do charge
        is_ok = PayHelperV4.callback_ok(order_id, -1, rparams)
        if is_ok:
            return 'success'
        else:
            return 'fail'

    @classmethod
    def check_sign(cls, rparams):
        app_id = rparams['app_id']
        sign = rparams['sign']
        config = TyContext.Configure.get_global_item_json('letv_keys', {})
        try:
            app_key = config[app_id]['scrkey']
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(rparams['cooperator_order_no'])
            app_key = config.get('scrkey')
        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if sign != md5('%s&key=%s' % (text, app_key)).hexdigest():
            return False
        else:
            return True
