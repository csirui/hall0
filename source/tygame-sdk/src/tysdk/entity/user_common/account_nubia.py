# -*- coding=utf-8 -*-

import json
import time
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountNubia():
    VALIDATE_URL = "http://niusdk.api.nubia.cn/VerifyAccount/CheckSession"

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        uid = params['nubia_uid']
        session = params['nubia_session']
        app_id = str(params['nubiya_appId'])
        config = TyContext.Configure.get_global_item_json('nubia_keys', {})
        try:
            secret = config[app_id]['secret']
        except KeyError:
            mainChannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('nubia', 'nubia_appId',
                                                                                                 app_id, mainChannel)
            if not config:
                TyContext.ftlog.debug(cls.__name__, 'cannot get nubia sdkconfig!')
                return False
            secret = config.get('secret')
        timestamp = int(time.time())

        rparams = {'uid': uid, 'session_id': session, 'data_timestamp': timestamp}
        text = 'data_timestamp=%s&session_id=%s&uid=%s:%s:%s' % (timestamp, session, uid, app_id, secret)
        sign = md5(text).hexdigest()
        rparams['sign'] = sign

        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, postdata_=rparams, method_='POST')
        TyContext.ftlog.debug('AccountNubia-> response ->', responseMsg)

        response = json.loads(responseMsg)
        # 返回结果0 校验正确3 未登录7 验证参数有为空10 校验失败 uid 与 sessionId 不匹配
        if '0' == str(response['code']):
            return True
        else:
            return False
