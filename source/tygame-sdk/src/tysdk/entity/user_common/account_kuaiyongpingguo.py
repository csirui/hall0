# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext


######################################################################
# 快用苹果登录过程的主要逻辑实现
#
######################################################################
class AccountKuaiYongPingGuo():
    @classmethod
    def doGetUserInfo(cls, params, snsId):

        tokenUrl = 'http://f_signin.bppstore.com/loginCheck.php'
        rparams = {}
        rparams['tokenKey'] = params['snsToken']

        kuaiyongpingguo_config = TyContext.Configure.get_global_item_json('kuaiyongpingguo_config', {})
        if kuaiyongpingguo_config:
            appKey = kuaiyongpingguo_config['appKey']

        m = md5()
        m.update(appKey + rparams['tokenKey'])
        digest = m.hexdigest().lower()
        rparams['sign'] = digest

        TyContext.ftlog.debug('AccountKuaiYongPingGuo-> tokenUrl->', tokenUrl, 'rparams', rparams)

        responseMsg, _ = TyContext.WebPage.webget(tokenUrl, rparams, method_='GET')
        response = json.loads(responseMsg)
        TyContext.ftlog.debug('AccountKuaiYongPingGuo-> response->', response)

        # 0:成功 其他失败   
        if 0 == int(response['code']):
            params['snsId'] = params['snsId'] + response['data']['guid']
            TyContext.ftlog.debug('AccountKuaiYongPingGuo ', response['msg'])
            return True
        else:
            TyContext.ftlog.error('AccountKuaiYongPingGuo ', response['msg'])
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
