# -*- coding=utf-8 -*-

import hmac
import json
import urllib

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayYouKuV4(PayBaseV4):
    @payv4_order('youku')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        buttonId = chargeinfo['buttonId']
        amount = str(int(float(chargeinfo['chargeTotal']) * 100))
        prodName = chargeinfo['buttonName']
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/youku/callback'
        chargeinfo['chargeData'] = {'amount': amount, 'productId': buttonId,
                                    'productName': prodName, 'notifyUrl': notifyurl}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/youku/callback')
    def doYouKuCallback(cls, rpath):
        cb_rsp = {}
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderPlatformId = rparam['apporderID']
            price = rparam['price']
            uid = rparam['uid']
            sign = rparam['sign']
            youku_appId = rparam['passthrough']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doYouKuCallback->ERROR, param error !! rparam=', rparam)
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '参数错误'
            return json.dumps(cb_rsp)

        paykey_dict = TyContext.Configure.get_global_item_json('youku_paykeys', {})
        try:
            paykey = str(paykey_dict[str(youku_appId)])
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId)
            paykey = config.get('YKGAME_PAYKEY', "")
            if not paykey:
                TyContext.ftlog.error('doYouKuCallback->ERROR,cannot get %s sdkconfig' % youku_appId)

        # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            TyContext.ftlog.error('TuYouPayYouKu.doYouKuCallback sign verify error !!')
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '签名验证失败'
            return json.dumps(cb_rsp)

        try:
            result = int(rparam['result'])
            success_amount = rparam['success_amount']
            if result < 1 or result > 2:
                TyContext.ftlog.error('doYouKuCallback got failed result:', result)
                cb_rsp['status'] = 'failed'
                cb_rsp['desc'] = 'result(%d) is not 1 or 2' % result
                PayHelper.callback_error(orderPlatformId, 'result(%d) is not 1 or 2' % result, rparam)
                return json.dumps(cb_rsp)
            if result == 2:
                TyContext.ftlog.error('doYouKuCallback got partial success result:'
                                      'success_amount is', success_amount)
        except:
            pass

        total_fee = float(price) / 100
        rparam['chargeType'] = 'youku'
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            cb_rsp['status'] = 'success'
            cb_rsp['desc'] = '发货成功'
            return json.dumps(cb_rsp)
        else:
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '发货失败'
            return json.dumps(cb_rsp)

    def __verify_sign(cls, rparam, paykey, sign):
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/youku/callback'
        sorted_args = [('apporderID', rparam['apporderID']),
                       ('price', rparam['price']), ('uid', rparam['uid'])]
        encoded_args = urllib.urlencode(sorted_args)
        check_str = notifyurl + '?' + encoded_args
        check_sign = hmac.new(paykey)
        check_sign.update(check_str)
        digest = check_sign.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayYouKu verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
