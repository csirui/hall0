# -*- coding=utf-8 -*-

import json
import time
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountYsdk(object):
    VALIDATE_URL = {'qq': '/auth/qq_check_token',
                    'wx': '/auth/wx_check_token'}

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        platfrom = params['ysdk_platform']
        appid = params['ysdk_appId']
        openid = params['ysdk_openId']
        openkey = params['ysdk_token']
        ysdk_model = params['ysdk_model']
        timestamp = int(time.time())

        config = TyContext.Configure.get_global_item_json('ysdk_keys', {})
        try:
            appkey = config[appid]['%s_appKey' % platfrom]
            request_url = config['%s_url' % ysdk_model]
        except:
            mainChannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('ysdk', 'ysdk_appId',
                                                                                                 appid, mainChannel)
            appkey = config.get('ysdk_%s_appKey' % platfrom, "")
            request_url = config.get('ysdk_%s_url' % ysdk_model, "")
            if not appkey or not request_url:
                TyContext.ftlog.debug('AccountYsdk,cannot find ysdk sdkconfig %s' % appid)
                return False
        sig = md5('%s%s' % (appkey, timestamp)).hexdigest()
        rparams = {'timestamp': timestamp, 'appid': appid, 'sig': sig, 'openid': openid, 'openkey': openkey}
        _url = 'http://%s%s' % (request_url, cls.VALIDATE_URL[platfrom])

        response_msg, _ = TyContext.WebPage.webget(_url, rparams, method_='GET')
        TyContext.ftlog.debug('AccountYsdk -> response ->', response_msg)
        response = json.loads(response_msg)
        if str(response['ret']) == '0':
            return True
        else:
            return False
