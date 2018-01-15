#! encoding=utf-8
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.pay_common.orderlog import Order
from tysdk.entity.user4.universal_user import UniversalUser

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
import hashlib
from payv4_helper import PayHelperV4
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.decorator.payv4_order import payv4_order


class TuYouPayLudashiV4(PayBaseV4):
    @payv4_order('ludashi')
    def charge_data(self, mi):
        return self.handle_order(mi)

    @payv4_callback('/open/ve/pay/ludashi/callback')
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayLudashi->doCallback, rparams=', rparams)
        platformOrderId = rparams['orderId']
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayLudashi.doCallback->ERROR, sign error !! rparam=', rparams)
            return {"code": 1, "info": "signature error"}
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return {"code": 0, "info": "success"}
        else:
            return {"code": 2, "info": "error"}

    @classmethod
    def check_sign(self, rparams):
        all_sign_keys = TyContext.Configure.get_global_item_json('kaiping_sign_keys', {})
        pay_key = all_sign_keys['ludashi']['payKey']
        text = filter(lambda x: x[0] != 'sign', rparams.items())
        text.sort(lambda x, y: cmp(x[0], y[0]))
        text = ['%s=%s' % x for x in text]
        text.append(pay_key)
        myauth = hashlib.md5('&'.join(text)).hexdigest()
        if rparams['sign'] == myauth:
            return True
        return False

    @classmethod
    def handle_random_charge_callback(cls, platformOrderId, amount, rparams):
        pass
        chargeKey = 'sdk.charge:' + platformOrderId

        # 1、防重复回调检查
        def is_orderId_valid(orderId, rparam, amount):
            chargeKey = 'sdk.charge:' + platformOrderId
            oldState, chargeInfo, consumeInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'state', 'charge',
                                                                               'consume')
            if oldState != PayConst.CHARGE_STATE_ERROR_CALLBACK:
                return True
            else:
                chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
                paytype = rparam.get('chargeType', chargeInfo.get('chargeType', 'na'))
                Order.log(platformOrderId, Order.INTERNAL_ERR, chargeInfo['uid'],
                          chargeInfo['appId'], chargeInfo['clientId'],
                          paytype=paytype,
                          prodid=chargeInfo.get('prodId', 'na'),
                          diamondid=chargeInfo['diamondId'],
                          charge_price=chargeInfo['chargeTotal'],
                          succ_price=amount,
                          sub_paytype=rparam.get('sub_paytype', 'na'),
                          third_prodid=rparam.get('third_prodid', 'na'),
                          third_orderid=rparam.get('third_orderid', 'na'),
                          third_provid=rparam.get('third_provid', 'na'),
                          third_userid=rparam.get('third_userid', 'na'),
                          pay_appid=rparam.get('pay_appid', 'na'),
                          info='order state charged',
                          )
                TyContext.ftlog.info('callback platformOrderId=', platformOrderId,
                                     'old state is done, oldState=', oldState,
                                     'newState=', PayConst.CHARGE_STATE_CALLBACK_OK)
                return False

        # 2、增加钻石
        def incr_user_diamond(orderId, amount):
            chargeKey = 'sdk.charge:' + platformOrderId
            chargeInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'charge')
            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
            userId = chargeInfo['uid']
            appId = chargeInfo.get('appId', "")
            UniversalUser().increase_user_charge_data(chargeInfo['uid'],
                                                      chargeInfo['appId'],
                                                      chargeInfo['clientId'],
                                                      amount,
                                                      chargeInfo.get('chargeType', 'na'))

            userKey = 'user:' + str(userId)
            diamondCount = float(amount) * 10
            _, coin = TyContext.UserProps.incr_diamond(
                int(userId), int(appId), diamondCount,
                TyContext.ChipNotEnoughOpMode.NOOP, TyContext.BIEventId.UNKNOWN)
            TyContext.BiReport.diamond_update(appId, userId, diamondCount, coin,
                                              'charge.callback')

            # 增加用户的充值次数
            PayHelperV4.incr_paycount(userId)

            # 增加用户总体支付的数量
            TyContext.RedisUser.execute(userId, 'HINCRBYFLOAT', userKey, 'chargeTotal', amount)

            # 增加用户的钻石购买的数据
            # RiskControlV4(userId).record_diamond(diamondId)

            if not is_orderId_valid(orderId, rparams, amount):
                return False
            incr_user_diamond(orderId, amount)
            PayHelperV4.notify_game_server_on_diamond_change(
                {'appId': chargeInfo['appId'], 'clientId': chargeInfo['clientId'],
                 'userId': chargeInfo['uid'], 'buttonId': chargeInfo['diamondId'],
                 'diamonds': chargeInfo['chargedDiamonds'],
                 'rmbs': amount})
            return True
