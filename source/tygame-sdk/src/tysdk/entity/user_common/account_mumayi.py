# -*- coding=utf-8 -*-

from tyframework.context import TyContext


######################################################################
# 木蚂蚁登录过程的主要逻辑实现
#
######################################################################
class AccountMumayi():
    VALIDATE_URL = 'http://pay.mumayi.com/user/index/validation'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        token = params['token']
        uid = params['uid']
        rparams = {'token': token, 'uid': uid, }
        TyContext.ftlog.debug('Mumayi-> VALIDATE_URL->', cls.VALIDATE_URL, 'rparams', rparams)
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='POST')
        TyContext.ftlog.debug('AccountMumayi-> response->', responseMsg)
        if responseMsg.strip() == 'success':
            return True
        else:
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
