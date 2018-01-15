# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

from tyframework.context import TyContext


class TuYouPayWanDouJia(object):
    appkeys = {'100000293': '83d78966187e4bea916552a61927bf62',  # 斗地主
               '100000297': 'f8f8dead01d59e8a19515b517107f182',  # 赢三张
               '100035968': '8baf6cbd68ace4b6b95539a58adf28d2',  # 斗地主
               }

    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'fake': 1}

    @classmethod
    def doWanDouJiaCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doWanDouJiaCallback->rparam=', rparam)
        transdata = rparam['content']
        try:
            datas = json.loads(transdata)
            appId = datas['appKeyId']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doWanDouJiaCallback->ERROR, sign error !! transdata=', transdata)
            return 'Fail'

        appKey = self.appkeys[str(appId)]
        sign = rparam['sign']
        if self.verifySign(transdata, sign, appKey) != True:
            TyContext.ftlog.info('doWanDouJiaCallback->ERROR, sign error !! transdata=', transdata, 'sign=', sign)
            return 'Fail'

        orderPlatformId = datas['out_trade_no']

        trade_status = 'TRADE_FINISHED'
        total_fee = int(float(datas['money']))
        total_fee = total_fee / 100.0

        from tysdk.entity.pay.pay import TuyouPay
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return 'Success'
        else:
            return 'Fail'

    @classmethod
    def verifySign(cls, transdata, sign, appKey):
        # TODO 
        TyContext.ftlog.error('TuYouPayWanDouJia-verifySign->transdata=', transdata, 'sign=', sign, 'appKey=', appKey)
        return True
