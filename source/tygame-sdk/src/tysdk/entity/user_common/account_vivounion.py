# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext


class AccountVivounion():
    VALIDATE_URL = "https://usrsys.vivo.com.cn/sdk/user/auth.do"

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        authtoken = params['authtoken']
        openid = params['openid']

        rparams = {'authtoken': authtoken, 'from': '在线途游'}
        response_msg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, postdata_=rparams, method_='POST')
        TyContext.ftlog.debug('AccountVivo-> response ->', response_msg)
        # {"retcode":0,"data":{"success":true,"openid":"bddb4ed37c3d7220"}}
        response = json.loads(response_msg)

        if int(response['retcode'] == 0):
            if response['data']['openid'] == openid:
                return True

        return False
