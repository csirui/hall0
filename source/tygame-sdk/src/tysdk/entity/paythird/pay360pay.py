# -*- coding=utf-8 -*-

from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext
from tyframework.orderids import orderid


class TuYouPay360pay(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        prodId = chargeinfo.get("prodId", chargeinfo['diamondId'])
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/360pay/callback'
        # prodconfig = TyContext.Configure.get_global_item_json('360pay_prodids', {})
        # data = prodconfig[str(appId)].get(prodId, None)
        amount = chargeinfo['chargeTotal'] * 100
        prodName = chargeinfo['buttonName']
        chargeinfo['chargeData'] = {'amount': amount, 'productId': prodId,
                                    'productName': prodName, 'notifyUrl': notifyurl,
                                    'rate': '1000'}

    @classmethod
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
        client_id = TyContext.Configure.get_game_item_str(appId, 'account.360.client.id' + clientver)
        client_secret = TyContext.Configure.get_game_item_str(appId, 'account.360.client.secret.' + app_key)

        if client_id == None or client_secret == None:
            TyContext.ftlog.error('Account360 the appinfo of appId %d is not found !' % (appId))
            return "error"

        # 签名校验
        if not cls.__verify_sign(rparam, client_secret, sign):
            TyContext.ftlog.error('TuyouPay360pay.do360payCallbacksign verify error !!')
            return "error"

        total_fee = float(rparam['amount']) / 100
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)

        if isOk:
            return "ok"
        else:
            return "error"

    @classmethod
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
