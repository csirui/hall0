# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import hmac
from hashlib import sha1

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayXiaomiV4(PayBaseV4):
    @payv4_order('xiaomi.common')
    def charge_data(self, mi):
        return self.get_charge_data(mi)

    @payv4_order('xiaomi.danji')
    def handle_order_danji(self, mi):
        return self.get_charge_data(mi)

    @payv4_order("xiaomi.weixin")
    def handle_order_weixin(self, mi):
        return self.get_charge_data(mi)

    @payv4_order("xiaomi.alipay")
    def handle_order_alipay(self, mi):
        return self.get_charge_data(mi)

    @payv4_order("xioami.qq")
    def handle_order_qq(self, mi):
        return self.get_charge_data(mi)

    def get_charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        chargeinfo['chargeData'] = {
            'amount': str(chargeinfo['chargeTotal']),
            'productId': chargeinfo['buttonId'],
            'productName': chargeinfo['buttonName'],
        }
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/xiaomi/callback')
    def doXiaomiCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doXiaomiCallback->rparam=', rparam)
        appkeys = TyContext.Configure.get_global_item_json('xiaomi_paykeys', {})
        try:
            appKey = str(appkeys[rparam['appId']])
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(rparam['cpOrderId'], 'xiaomi')
            appKey = str(config.get('xiaomi_payKey'))
            if not appKey:
                TyContext.ftlog.error('xiaomidanji callback , cannot get  %s config' % rparam['appId'])
                return '{"errcode":1515}'
        return cls.__check_callback(rparam, appKey)

    @payv4_callback('/open/ve/pay/xiaomidanji/callback')
    def doXiaomiDanJiCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doXiaomiDanJiCallback->rparam=', rparam)
        appkeys = TyContext.Configure.get_global_item_json('xiaomidanji_paykeys', {})
        try:
            appKey = str(appkeys[rparam['appId']])
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(rparam['cpOrderId'], 'midanji')
            appKey = str(config.get('xiaomidanji_payKey', ""))
            if not appKey:
                TyContext.ftlog.error('xiaomidanji callback , cannot get  %s config' % rparam['appId'])
                return '{"errcode":1515}'
        return cls.__check_callback(rparam, appKey)

    def __check_callback(cls, rparam, appKey):
        signQuery = rparam['signature']
        del rparam['signature']

        sk = rparam.keys()
        sk.sort()
        queryStr = ""
        for k in sk:
            queryStr = queryStr + str(k) + '=' + str(rparam[k]) + '&'
        signData = queryStr[:-1]
        TyContext.ftlog.info('doXiaomiCallback->queryStr=', queryStr, 'signData=', signData)

        a = hmac.new(appKey, signData, sha1)
        sign = a.digest().encode('hex').upper()
        if signQuery.upper() != sign:
            TyContext.ftlog.info('doXiaomiCallback->ERROR, sign error !! signQuery=', signQuery, 'sign=', sign)
            return '{"errcode":1525}'

        orderPlatformId = rparam['cpOrderId']

        total_fee = float(rparam['payFee']) / 100
        ChargeModel.save_third_pay_order_id(orderPlatformId, rparam.get('orderId'))
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return '{"errcode":200}'
        else:
            return '{"errcode":1506}'
