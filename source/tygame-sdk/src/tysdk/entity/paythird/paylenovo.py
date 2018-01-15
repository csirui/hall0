# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayLenovo(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        if 'payInfo' in chargeinfo and chargeinfo['payInfo']:
            payInfo = chargeinfo['payInfo']
            if 'appid' in payInfo and payInfo['appid']['lenovo']:
                appId = payInfo['appid']['lenovo']
        diamondId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('lenovo_prodids', {})
        data = prodconfig[str(appId)].get(str(diamondId), None)

        if data:
            payCode = data['feecode']
        else:
            raise Exception('can not find lenovo product define of buttonId='
                            + diamondId + ' for clientId=' + chargeinfo['clientId'])

        chargeinfo['chargeData'] = {'msgOrderCode': payCode}

    @classmethod
    def doLenovoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        TyContext.ftlog.info('doLenovoCallback->rparam=', rparam)
        transdata = rparam['transdata']

        try:
            datas = json.loads(transdata)
            appId = datas['appid']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLenovoCallback->ERROR, sign error !! transdata=', transdata)
            return 'ERROR'

        appkeyconfig = TyContext.Configure.get_global_item_json('lenovo_appkeys', {})
        appKey = appkeyconfig[str(appId)]
        sign = rparam['sign']
        if cls.verifySign(transdata, sign, appKey) != True:
            TyContext.ftlog.info('doLenovoCallback->ERROR, sign error !! transdata=', transdata, 'sign=', sign)
            return 'ERROR'

        orderPlatformId = datas['exorderno']

        total_fee = float(datas['money']) / 100
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)

        if isOk:
            return 'SUCCESS'
        else:
            return 'ERROR'

    @classmethod
    def verifySign(cls, transdata, sign, appKey):
        # TODO 
        TyContext.ftlog.error('TuyouPayLenovo-verifySign->transdata=', transdata, 'sign=', sign, 'appKey=', appKey)
        return True
