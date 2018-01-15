# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountJusdk():
    VALIDATE_URL = "http://api.jusdk.com/user/get"

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        app_id = params['jusdk_appId']
        token_key = params['jusdk_token']

        config = TyContext.Configure.get_global_item_json("jusdk_keys", {})
        try:
            appkey = config[app_id]['appKey']
        except:
            mainChannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('jusdk', 'jusdk_appId',
                                                                                                 app_id, mainChannel)
            appkey = config.get('jusdk_appKey', "")
            if not appkey:
                TyContext.ftlog.debug("AccountJusdk,cannot find jusdk config for", app_id)
                return False
        sign_text = '%s%s' % (appkey, token_key)
        sign = md5(sign_text).hexdigest()
        rparams = {'tokenKey': token_key, 'sign': sign}
        response_msg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, postdata_=rparams, method_='POST')
        TyContext.ftlog.debug('AccountJusdk-> response ->', response_msg)
        # {"code":0,"msg":"", "data":{"guid":"s1234567890"}}
        response = json.loads(response_msg)
        if 0 == int(response['code']):
            jusdk_guid = response['data']['guid']
            params['snsId'] = 'jusdk:' + jusdk_guid
            TyContext.ftlog.debug('AccountJusdk-> guid ->', jusdk_guid)
            return True
        else:
            return False
