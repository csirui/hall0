# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYouPayMomoV4(PayBaseV4):
    checkorder_url = 'https://game-api.immomo.com/game/2/server/trade/checkorder'

    @payv4_order('momo')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        appId = chargeinfo['appId']
        diamondId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('momo_prodids', {})
        data = prodconfig['6'].get(str(diamondId), None)
        if data:
            payCode = data['feecode']
        else:
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('momo',
                                                                                                  chargeinfo[
                                                                                                      'packageName'],
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])
            if not config:
                package = 'com.wemomo.game.ddz'
                channel = 'momo'
                config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('momo',
                                                                                                      package,
                                                                                                      channel)
            products = config.get('products', {})
            productConfig = filter(lambda x: x['diamondId'].strip() == diamondId, products)
            payCode = productConfig[0].get('feecode', '') if len(productConfig) > 0 else ''
            if not payCode:
                raise PayErrorV4(1, 'can not find momo product define of diamondId=' + diamondId)
        chargeinfo['chargeData'] = {'msgOrderCode': payCode}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_order('momo.jailbreak')
    def charge_date_jailbreak(self, mi):
        return self.charge_data(mi)

    @payv4_order('momo.ios')
    def charge_data_ios(self, mi):
        return self.charge_data(mi)

    @payv4_callback('/open/ve/pay/momo/callback')
    def doMomoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        momo_paykeys = TyContext.Configure.get_global_item_json('momo_paykeys', {})
        TyContext.ftlog.debug('doMomoCallback->rparam=', rparam)
        try:
            orderPlatformId = rparam['app_trade_no']
            trade_no = rparam['trade_no']
            appid = rparam['appid']
            postparams = {}
            postparams['appid'] = appid
            postparams['sign'] = rparam['sign']
            postparams['trade_no'] = trade_no
            postparams['app_secret'] = momo_paykeys[str(appid)]
            response, _ = TyContext.WebPage.webget(cls.checkorder_url, postdata_=postparams)
            response = json.loads(response)
            if int(response['ec']) != 0:
                TyContext.ftlog.error('doMomoCallback->ERROR, check momo order fail, response=', response)
                return 'fail'
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.error('doMomoCallback->ERROR, rparam=', rparam)
            return 'fail'

        if int(rparam['currency_type']) == 0:
            total_fee = float(rparam['total_fee'])
        else:
            total_fee = float(rparam['total_fee']) / 10
        rparam['third_orderid'] = trade_no
        rparam['chargeType'] = 'momo'
        # channel_type   string 支付渠道 0-苹果 1-支付宝 2-短信 3-陌陌币 4-网页版
        rparam['sub_paytype'] = rparam['channel_type']
        try:
            chargeKey = 'sdk.charge:' + orderPlatformId
            chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
            if chargeInfo == None:
                chargeInfo = {}
            else:
                chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
            chargeInfo['sub_paytype'] = rparam['channel_type']
            TyContext.RedisPayData.execute('HSET', chargeKey, 'charge', json.dumps(chargeInfo))
        except:
            TyContext.ftlog.error()

        ChargeModel.save_third_pay_order_id(orderPlatformId, trade_no)
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        return 'success'
