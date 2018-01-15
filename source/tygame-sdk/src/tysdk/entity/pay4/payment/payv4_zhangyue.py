# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayZhangYueV4(PayBaseV4):
    @payv4_order('zhangyue')
    def charge_data(self, mi):
        return self.handle_order(mi)

    @payv4_callback('/open/ve/pay/zhangyue/callback')
    def doZhangYueCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        try:
            appId = rparam['appId']
            transData = json.loads(rparam['transData'])
            orderPlatformId = transData['merOrderId']
            price = transData['payAmt']
            sign = transData['md5SignValue']
        except:
            TyContext.ftlog.info('TuYouPayZhangYueV4 -> ERROR, param error !! rparam=', rparam)
            return 'error'

        config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'zhangyue')
        paykey = config['zhangyue_md5_key']

        # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            TyContext.ftlog.error('TuYouPayZhangYue.doZhangYueCallback sign verify error !!')
            return 'error'

        total_fee = float(price)
        rparam['chargeType'] = 'zhangyue'
        rparam['third_orderid'] = transData['orderId']
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        TyContext.ftlog.info("TuYouPayZhangYueV4 payhelper callback=", isOk)
        if isOk:
            return 'success'
        else:
            return 'error'

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        transData = json.loads(rparam['transData'])
        check_str = (rparam['merId'] + '|' +
                     rparam['appId'] + '|' +
                     transData['orderId'] + '|' +
                     transData['payAmt'] + '|' +
                     paykey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        if digest != sign.lower():
            TyContext.ftlog.error('TuYouPayZhangYue verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
