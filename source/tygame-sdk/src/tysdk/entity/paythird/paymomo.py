# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayMomo(object):
    checkorder_url = 'https://game-api.immomo.com/game/2/server/trade/checkorder'

    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        diamondId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('momo_prodids', {})
        data = prodconfig[str(appId)].get(str(diamondId), None)

        if data:
            payCode = data['feecode']
        else:
            raise Exception('can not find momo product define of diamondId=' + diamondId)
        chargeinfo['chargeData'] = {'msgOrderCode': payCode}

    @classmethod
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

        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        return 'success'
