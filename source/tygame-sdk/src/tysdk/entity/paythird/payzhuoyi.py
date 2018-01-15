#! encoding=utf-8

__author__ = 'yuejianqiang'

import hashlib

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayZhuoyi(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        zhuoyi_keys = TyContext.Configure.get_global_item_json('zhuoyi_keys', {})
        buttonId = chargeinfo['buttonId']
        buttonName = chargeinfo['buttonName']
        packageName = chargeinfo['packageName']
        payInfo = zhuoyi_keys[packageName]
        codes = payInfo['codes']
        chargeinfo['chargeData'] = {
            'platformOrderId': chargeinfo['platformOrderId'],
            'appId': payInfo['appId'],
            'appKey': payInfo['appKey'],
            'code': codes.get(buttonId, codes.get(buttonName))
        }

    @classmethod
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        platformOrderId = rparams['Extra']
        TyContext.ftlog.debug('TuYouPayZhuoyi->doCallback, rparams=', rparams)
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPayZhuoyi->ERROR, sign error !! rparam=', rparams)
            return 'failure'
        # do charge
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def check_sign(cls, rparams):
        # Recharge_Id = rparams['Recharge_Id']
        App_Id = rparams['App_Id']
        # Uin=rparams['Uin']
        # Urecharge_Id=rparams['Urecharge_Id']
        # Extra=rparams['Extra']
        # Recharge_Money=rparams['Recharge_Money']
        # Recharge_Gold_Count=rparams['Recharge_Gold_Count']
        # Pay_Status=rparams['Pay_Status']
        # Create_Time=rparams['Create_Time']
        Sign = rparams['Sign']
        # find payKey by appId
        zhuoyi_keys = TyContext.Configure.get_global_item_json('zhuoyi_keys', {})
        payKey = ''
        for appInfo in zhuoyi_keys.values():
            if str(appInfo['appId']) == App_Id:
                payKey = appInfo['paySecret']
                break
        params = filter(lambda x: x[0] != '' and x[0] != 'Sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if Sign != hashlib.md5('%s%s' % (text, payKey)).hexdigest():
            return False
        return True
