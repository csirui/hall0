# -*- coding=utf-8 -*-

import json
import time
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountMeizu():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        accountId = snsId[6:].strip()
        if not accountId:
            return False
        return cls._check_session(params, accountId)

    @classmethod
    def _check_session(cls, params, accountId):
        TyContext.ftlog.debug('AccountMeizu _check_session , params from client'
                              , params)

        try:
            client_sessionId, client_appId = params['snsToken'][6:].split(' ')
        except Exception as e:
            TyContext.ftlog.error('AccountMeizu _check_session ,exception:', e)
            return False
        meizu_config = TyContext.Configure.get_global_item_json('meizu_config', {})
        try:
            appkey = meizu_config[client_appId]['appkey']
        except KeyError:
            mainchannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('meizu', 'mz_appId',
                                                                                                 client_appId,
                                                                                                 mainchannel)
            if not config:
                TyContext.ftlog.debug(cls.__name__, 'meizu,can not get config for appId:%s ' % client_appId)
                return False
            appkey = config.get('mz_appSecret', '')

        server_time = int(time.time())
        md5_str = cls._calc_sign(client_appId, client_sessionId, server_time,
                                 accountId, appkey)
        post_param = 'app_id=%s&session_id=%s&ts=%s&uid=%s&sign_type=md5&sign=%s' % (
            client_appId, client_sessionId, server_time, accountId, md5_str)
        url = 'https://api.game.meizu.com/game/security/checksession'
        try:
            response, _ = TyContext.WebPage.webget(url, postdata_=post_param)
        except Exception as e:
            TyContext.ftlog.error('AccountMeizu _check_session error, exception', e)
            return False
        try:
            infos = json.loads(response)
        except Exception as e:
            TyContext.ftlog.error('AccountMeizu _check_session->infourl json'
                                  ' wrong, response=', response, 'exception', e)
            return False
        TyContext.ftlog.info('AccountMeizu _check_session responseinfo ', infos)
        if int(infos['code']) != 200:
            return False
        return True

    @classmethod
    def _calc_sign(cls, client_appId, client_sessionId, server_time, accountId,
                   appkey):
        check_str = 'app_id=%s&session_id=%s&ts=%s&uid=%s:%s' % (client_appId,
                                                                 client_sessionId, server_time, accountId, appkey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        return digest
