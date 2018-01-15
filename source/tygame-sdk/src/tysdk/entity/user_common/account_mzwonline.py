# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext


######################################################################
# Letv乐视 登录过程的主要逻辑实现
######################################################################


class AccountMZWOnline():
    VALIDATE_URL = 'http://sdk.muzhiwan.com/oauth2/getuser.php'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        appkey = params['mzw_appKey']
        token = params['mzw_token']
        rparams = {'token': token, 'appkey': appkey, }
        response_msg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams)
        TyContext.ftlog.debug('AccountMZWOnline-> response ->', response_msg)
        response = json.loads(response_msg)
        if 1 == int(response['code']):
            uid = response['user']['uid']
            params['snsId'] = 'muzhiwan:%s' % uid
            params['name'] = response['user']['username']
            return True
        else:
            return False
