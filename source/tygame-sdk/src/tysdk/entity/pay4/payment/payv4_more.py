# -*- coding=utf-8 -*-
from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayMoreV4(PayBaseV4):
    @payv4_order('more')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        cporderid = chargeinfo.get('platformOrderId', '')
        config = GameItemConfigure.get_game_channel_configure_by_orderId(cporderid, 'more')
        appkey = config.get('more_appkey', '')
        chargeinfo['chargeData'] = {'callbackUrl': PayHelperV4.getSdkDomain() + '/v1/pay/more/callback'}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/more/callback')
    def doMomoCallback(cls, rpath):
        rparam = TyContext.RunHttp.get_body_content()
        import json
        rparam = json.loads(rparam)
        orderinfo = rparam.get('orderinfo', {})
        statusMsg = rparam.get('statusMsg', '')
        sign = rparam.get('sign')
        signKey = ['cporderid', 'payorderid', 'ordertime', 'status', 'amount', 'currency', 'pname', 'appid', 'cid']
        cporderid = orderinfo.get('cporderid', '')
        config = GameItemConfigure.get_game_channel_configure_by_orderId(cporderid, 'more')
        appkey = config.get('more_appkey', '')
        # 读取默认参数配置
        if not appkey:
            packageName = 'com.sdk.more.default'
            channel = 'kuyuoka'
            appId = '9999'
            config = GameItemConfigure(appId).get_game_channel_configure_by_package('more', packageName, channel)
        appkey = config.get('more_appkey', '')
        signStr = appkey + ''.join(str(orderinfo[k]) for k in signKey)
        from hashlib import md5
        m = md5(signStr)
        if m.hexdigest().lower() != sign:
            PayHelperV4.callback_error(cporderid, '验签失败', rparam)
            return {'returnCode': 0, 'returnMsg': '失败'}
        total_fee = float(orderinfo.get('amount')) / 100
        PayHelperV4.callback_ok(cporderid, total_fee, rparam)
        return {'returnCode': 1, 'returnMsg': ''}
