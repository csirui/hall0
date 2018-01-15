# -*- coding=utf-8 -*-

from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tyframework.orderids import orderid
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPay360payV4(PayBaseV4):
    @payv4_order("360pay")
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        appId = chargeinfo['appId']
        prodId = chargeinfo.get("prodId", chargeinfo['diamondId'])
        notifyurl = PayHelperV4.getSdkDomain() + '/v1/pay/360pay/callback'
        # prodconfig = TyContext.Configure.get_global_item_json('360pay_prodids', {})
        # data = prodconfig[str(appId)].get(prodId, None)
        amount = chargeinfo['chargeTotal'] * 100
        prodName = chargeinfo['buttonName']
        chargeinfo['chargeData'] = {'amount': amount, 'productId': prodId,
                                    'productName': prodName, 'notifyUrl': notifyurl,
                                    'rate': '1000'}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_order("360dj.alipay")
    def charge_data_alipay(self, mi):
        return self.charge_data(mi)

    @payv4_order("360dj.alifree")
    def charge_data_alifree(self, mi):
        return self.charge_data(mi)

    @payv4_order("360dj.weixin")
    def charge_data_weixin(self, mi):
        return self.charge_data(mi)

    @payv4_callback("/open/ve/pay/360pay/callback")
    def do360payCallback(cls, rpath):
        TyContext.ftlog.debug('do360payCallback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderPlatformId = rparam['app_order_id']
            appId = orderid.get_appid_frm_order_id(orderPlatformId)
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('do360payCallback->ERROR, param error !! rparam=', rparam)
            return "error"

        clientId = rparam['app_ext1']
        app_key = rparam['app_key']
        client_ids = TyContext.Configure.get_game_item_json(appId, 'account.360.client.version', {})
        clientver = ''
        if clientId in client_ids:
            clientver = str(client_ids[clientId])
        client_secret = TyContext.Configure.get_game_item_str(appId, 'account.360.client.secret.' + app_key)
        if not client_secret:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, "360")
            client_secret = config.get('QHOPENSDK_APPSECRET')
        if not client_secret:
            TyContext.ftlog.error('Account360 the appinfo of QIHOO(appKey:%s)  is not found !' % app_key)
            return "error"

        # 签名校验
        if not cls.__verify_sign(rparam, client_secret, sign):
            TyContext.ftlog.error('TuyouPay360pay.do360payCallbacksign verify error !!')
            return "error"

        total_fee = float(rparam['amount']) / 100
        ChargeModel.save_third_pay_order_id(orderPlatformId, rparam.get('order_id', ''))
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return "ok"
        else:
            return "error"

    def __verify_sign(cls, rparam, appsecret, signature):
        check_str = '#'.join(
            rparam[k] for k in sorted(rparam.keys()) if k != 'sign' and k != 'sign_return') + '#' + appsecret
        sign = signature
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuyouPay360pay verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
