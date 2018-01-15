# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext


######################################################################
# Letv乐视 登录过程的主要逻辑实现
######################################################################


class AccountLetv():
    VALIDATE_URL = 'https://sso.letv.com/oauthopen/userbasic'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        appid = params['letv_appid']
        uid = params['letv_uid']
        access_token = params['letv_access_token']

        config = TyContext.Configure.get_global_item_json('letv_keys', {})
        app_id = config[appid]['appid']
        tyAppId = params.get('appId')
        if not app_id:
            app_id = appid
        rparams = {'uid': uid, 'client_id': app_id, 'access_token': access_token}
        response_msg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams)
        TyContext.ftlog.debug('AccountLetv-> response ->', response_msg)

        response = json.loads(response_msg)
        if 1 == int(response['status']):
            return True
        else:
            return False
