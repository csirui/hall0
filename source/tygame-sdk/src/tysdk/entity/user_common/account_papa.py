# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountPapa():
    VALIDATE_URL = 'http://sdkapi.papa91.com/auth/check_token'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        uid = params['uid']
        app_key = params['app_key']
        token = params['token']
        rparams = {'uid': uid, 'app_key': app_key, 'token': token}
        config = TyContext.Configure.get_global_item_json('papa_keys', {})
        try:
            secretKey = config[app_key]['secretKey']
        except KeyError:
            mainChannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey("papa", 'papa_app_key',
                                                                                                 app_key, mainChannel)
            secretKey = config.get('papa_secret', "")
            if not secretKey:
                TyContext.ftlog.debug(cls.__name__, 'cannot get sdkconfig papa')
                return False
        sign = md5('%s%sapp_key=%s&token=%s&uid=%s' % (app_key, secretKey, app_key, token, uid)).hexdigest()
        rparams['sign'] = sign
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, postdata_=rparams, method_='POST')
        TyContext.ftlog.debug('AccountPapa-> response->', responseMsg)
        response = json.loads(responseMsg)
        # 0:成功 1:无效的 token 2:用户不存在 3:会话超时
        if '0' == str(response['error']) and response['data']['is_success']:
            return True
        else:
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
