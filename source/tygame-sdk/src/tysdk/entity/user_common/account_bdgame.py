# -*- coding=utf-8 -*-

import json
from base64 import b64decode
from hashlib import md5
from urllib import unquote

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountBDGame():
    VALIDATE_URL = 'http://querysdkapi.baidu.com/query/cploginstatequery'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        appId = params['bdgame_appId']
        uid = params['bdgame_uid']
        accessToken = params['bdgame_accessToken']

        config = TyContext.Configure.get_global_item_json('bdgame_keys', {})
        try:
            secretKey = config[appId]['secretKey']
        except:
            mainChannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('bdgame',
                                                                                                 'bdgame_appId',
                                                                                                 appId, mainChannel)
            secretKey = config.get('bdgame_secretKey', "")
            if not secretKey:
                TyContext.ftlog.debug("AccountBDgame,cannot find sdkconfig for ", appId)
                return False
        sign = md5('%s%s%s' % (appId, accessToken, secretKey)).hexdigest()

        rparams = {'AppID': appId, 'AccessToken': accessToken, 'Sign': sign}
        response_msg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, postdata_=rparams, method_='POST')
        TyContext.ftlog.debug('AccountBDGame-> response ->', response_msg)

        response = json.loads(response_msg)

        check_sign = response['Sign']
        check_text = '%s%s%s%s' % (response['AppID'], response['ResultCode'], response['Content'], secretKey)
        if check_sign != md5(check_text).hexdigest():
            return False
        # content是一个json字符串,先urldeconde,再base64解码
        content = b64decode(unquote(response['Content']))
        item = json.loads(content)
        if str(item['UID']) == uid:
            return True
        else:
            return False
