# -*- coding=utf-8 -*-

import json
import uuid

from tyframework.context import TyContext


######################################################################
# 木蚂蚁登录过程的主要逻辑实现
#
######################################################################
class AccountPengyouwan():
    VALIDATE_URL_PRODUCT = 'http://pywsdk.pengyouwan.com/Cpapi/check'
    VALIDATE_URL_TESTING = 'http://xp.yyft.com:8081/Cpapi/check'

    VALIDATE_URL = VALIDATE_URL_PRODUCT

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        return True
        tid = str(uuid.uuid4()).split('-')[-1]
        uid = params['uid']
        token = params['token']
        rparams = {'token': token, 'uid': uid, 'tid': tid}
        TyContext.ftlog.debug('AccountPengyouwan-> VALIDATE_URL->', cls.VALIDATE_URL, 'rparams', rparams)
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='POST')
        TyContext.ftlog.debug('AccountPengyouwan-> response->', responseMsg)
        ret = json.loads(responseMsg)
        if str(ret['ack']) == '200':
            return True
        else:
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
