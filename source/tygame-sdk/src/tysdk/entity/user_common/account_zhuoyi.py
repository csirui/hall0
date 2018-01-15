# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountZhuoyi():
    VALIDATE_URL = 'http://open.zhuoyi.com/phone/index.php/ILoginAuth/auth'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        uid = params['uid']
        access_token = params['access_token']
        app_id = params['app_id']
        rparams = {'uid': uid, 'access_token': access_token, 'app_id': app_id}
        config = TyContext.Configure.get_global_item_json('zhuoyi_keys', {})
        for keys in config.values():
            if keys['appId'] == app_id:
                appKey = keys['paySecret']
                break
        else:
            mainChannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('zhuoyi',
                                                                                                 'zhuoyi_appId',
                                                                                                 app_id, mainChannel)
            appKey = config.get('zhuoyi_paySecret', "")
            if not appKey:
                return False
                # return False
        text = 'uid=%s&access_token=%s&app_id=%s&key=%s' % (uid, access_token, app_id, appKey)
        sign = md5(text).hexdigest()
        rparams['sign'] = sign
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='GET')
        TyContext.ftlog.debug('AccountZhuoyi-> response->', responseMsg)
        response = json.loads(responseMsg)
        # 0:成功 1:无效的 token 2:用户不存在 3:会话超时
        if '0' == str(response['code']):
            return True
        else:
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
