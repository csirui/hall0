# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import rsaVerify
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayWanDouJiaV4(PayBaseV4):
    appkeys = {'100000293': '83d78966187e4bea916552a61927bf62',  # 斗地主
               '100000297': 'f8f8dead01d59e8a19515b517107f182',  # 赢三张
               '100035968': '8baf6cbd68ace4b6b95539a58adf28d2',  # 斗地主
               '100036122': '7a59015533375bef3807c3183e84940e',  # 天天德州
               }

    # @payv4_filter('wandoujia')
    # def filter_wandoujia(self, payment, prod_info, **kwargs):
    #     if prod_info['price'] >= 100:
    #         return False
    #     return True

    @payv4_order("wandoujia")
    def charge_data(cls, mi):
        return cls.handle_order(mi)

    @payv4_callback("/open/ve/pay/wandoujia/callback")
    def doWanDouJiaCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doWanDouJiaCallback->rparam=', rparam)
        transdata = rparam['content']
        datas = json.loads(transdata)
        appId = datas['appKeyId']
        orderPlatformId = datas['out_trade_no']
        try:
            appkeyconfig = TyContext.Configure.get_global_item_json('wannew_appkeys', {})
            appKey = appkeyconfig[str(appId)]
        except:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'wannew')
            TyContext.ftlog.debug('wandoujia,get sdk config -->', config)
            if not config:
                TyContext.ftlog.exception()
                TyContext.ftlog.info('doWanDouJiaCallback->ERROR, sign error !! transdata=', transdata)
                return 'Fail'
            appKey = config.get('wannew_secretKey')
            # appKey = self.appkeys[str(appId)]
        sign = rparam['sign']
        if self.verifySign(transdata, sign, appKey) != True:
            TyContext.ftlog.info('doWanDouJiaCallback->ERROR, sign error !! transdata=', transdata, 'sign=', sign)
            return 'Fail'
        trade_status = 'TRADE_FINISHED'
        total_fee = int(float(datas['money']))
        total_fee = int(total_fee / 100)
        ChargeModel.save_third_pay_order_id(orderPlatformId, datas.get('orderId', ''))
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'Success'
        else:
            return 'Fail'

    @classmethod
    def verifySign(cls, transdata, sign, appKey):
        TyContext.ftlog.error('TuYouPayWanDouJia-verifySign->transdata=', transdata, 'sign=', sign, 'appKey=', appKey)
        if rsaVerify(transdata, sign, 'wandoujia'):
            return True
        return False
