#! encoding=utf-8
from tysdk.configure.game_item import GameItemConfigure

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
import hashlib
from payv4_helper import PayHelperV4
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.decorator.payv4_order import payv4_order


class TuYouPaySougouV4(PayBaseV4):
    @payv4_order('sogou')
    def charge_data(self, mi):
        return self.handle_order(mi)
        # m4399_keys = TyContext.Configure.get_global_item_json('m4399_keys', {})
        # packageName = chargeinfo['packageName']
        # appInfo = m4399_keys[packageName]
        # appKey = appInfo['appKey']
        # appSecret = appInfo['appSecret']
        # chargeKey = 'sdk.charge:m4399:%s' % chargeinfo['platformOrderId']
        # TyContext.RedisPayData.execute('HMSET', chargeKey, 'appKey', appKey, 'appSecret', appSecret)

    @payv4_callback('/open/ve/pay/sougou/callback')
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPaySougou->doCallback, rparams=', rparams)
        platformOrderId = rparams['appdata']
        amount1 = rparams['amount1']
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPaySougou.doCallback->ERROR, sign error !! rparam=', rparams)
            return 'ERR_200'
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'OK'
        else:
            return 'ERR_500'

    @classmethod
    def check_sign(self, rparams):
        gid = rparams['gid']
        platformOrderId = rparams['appdata']
        sougou_keys = TyContext.Configure.get_global_item_json('sougou_keys', {})
        try:
            paySecret = sougou_keys[gid]['paySecret']
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId, 'sogou')
            paySecret = config.get("sogou_paySecret")
        text = filter(lambda x: x[0] != 'auth', rparams.items())
        text.sort(lambda x, y: cmp(x[0], y[0]))
        text = ['%s=%s' % x for x in text]
        text.append(paySecret)
        myauth = hashlib.md5('&'.join(text)).hexdigest()
        if rparams['auth'] == myauth:
            return True
        return False
