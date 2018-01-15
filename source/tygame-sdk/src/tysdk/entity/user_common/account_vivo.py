# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext


class AccountVivo():
    VALIDATE_URL = "https://usrsys.inner.bbk.com/auth/user/info"

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        access_token = params['authtoken']
        rparams = {'access_token': access_token}
        response_msg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, postdata_=rparams, method_='POST')
        TyContext.ftlog.debug('AccountVivo-> response ->', response_msg)
        # {"code":0,"msg":"", "data":{"guid":"s1234567890"}}
        response = json.loads(response_msg)
        uid = response['uid']
        params['snsId'] = 'vivo:' + uid
        TyContext.ftlog.debug('AccountVivo-> uid ->', uid)
        return True
