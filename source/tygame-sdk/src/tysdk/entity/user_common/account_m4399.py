# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext


######################################################################
# 木蚂蚁登录过程的主要逻辑实现
#
######################################################################
class AccountM4399():
    VALIDATE_URL = 'http://m.4399api.com/openapi/oauth-check.html'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        state = params['state']
        uid = params['uid']
        rparams = {'state': state, 'uid': uid, }
        TyContext.ftlog.debug('Account4399-> VALIDATE_URL->', cls.VALIDATE_URL, 'rparams', rparams)
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='GET')
        TyContext.ftlog.debug('Account4399-> response->', responseMsg)
        response = json.loads(responseMsg)
        # 0:成功 1:无效的 token 2:用户不存在 3:会话超时
        if '100' == str(response['code']):
            return True
        else:
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
