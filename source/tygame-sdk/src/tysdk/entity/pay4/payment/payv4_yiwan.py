# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayYiwanV4(PayBaseV4):
    @payv4_order("yiwan")
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        order_id = chargeinfo['platformOrderId']
        app_id = mi.getParamStr('yiwan_appId')
        charge_key = 'sdk.charge:yiwan:%s' % order_id
        TyContext.RedisPayData.execute('HSET', charge_key, 'appId', app_id)

        chargeinfo['chargeData'] = {
            'platformOrderId': order_id
        }
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/yiwan/callback')
    def doCallback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayYiwanV4->doCallback, rparams=', rparams)
        order_id = rparams['custominfo']
        charge_key = 'sdk.charge:yiwan:%s' % order_id
        app_id = TyContext.RedisPayData.execute('HGET', charge_key, 'appId')
        if not self._check_sign(rparams, app_id):
            TyContext.ftlog.error('TuYouPayYiwanV4 check sign error')
            return '100'

        status = rparams['status']
        if 1 != int(status):
            return '100'

        is_ok = PayHelperV4.callback_ok(order_id, -1, rparams)
        if is_ok:
            return '1'
        else:
            return '103'

    def _check_sign(self, rparams, app_id):
        serverid = rparams['serverid']
        custominfo = rparams['custominfo']
        openid = rparams['openid']
        ordernum = rparams['ordernum']
        status = rparams['status']
        paytype = rparams['paytype']
        amount = rparams['amount']
        errdesc = rparams['errdesc']
        paytime = rparams['paytime']
        sign = rparams['sign']

        config = TyContext.Configure.get_global_item_json('yiwan_keys', {})
        try:
            appKey = config[str(app_id)]['appKey']
        except KeyError:
            appConfig = GameItemConfigure.get_game_channel_configure_by_orderId(custominfo)
            appKey = appConfig.get('appKey')

        text = '%s|%s|%s|%s|%s|%s|%s|%s|%s|%s' % (
        serverid, custominfo, openid, ordernum, status, paytype, amount, errdesc, paytime, appKey)

        if sign == md5(text).hexdigest():
            return True
        else:
            return False
