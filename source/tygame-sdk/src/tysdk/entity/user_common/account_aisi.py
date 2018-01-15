# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext


######################################################################
# AiSi登录过程的主要逻辑实现
#
######################################################################
class AccountAiSi():
    @classmethod
    def doGetUserInfo(cls, params, snsId):

        tokenUrl = 'https://pay.i4.cn/member_third.action'
        rparams = {}
        rparams['token'] = params['snsToken']
        TyContext.ftlog.debug('AccountAiSi-> tokenUrl->', tokenUrl, 'rparams', rparams)

        responseMsg, _ = TyContext.WebPage.webget(tokenUrl, rparams, method_='GET')
        response = json.loads(responseMsg)
        TyContext.ftlog.debug('AccountAiSi-> response->', response)

        # 0:成功 1:无效的 token 2:用户不存在 3:会话超时         
        if 0 == response['status']:
            return True
        else:
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
