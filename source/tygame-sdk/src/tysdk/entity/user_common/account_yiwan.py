# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountYiwan():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        yiwan_appId = params['yiwan_appId']
        openid = params['yiwan_openid']
        token = params['yiwan_token']
        sign = params['yiwan_sign']

        config = TyContext.Configure.get_global_item_json('yiwan_keys', {})
        appKey = config.get(yiwan_appId)['appKey'] if config.get(yiwan_appId) else ""
        if not appKey:
            appId = params.get('appId', '')
            mainChannel = params['clientId'].split('.')[-2]
            appConfig = GameItemConfigure(appId).get_game_channel_configure_by_primarykey('yiwan', 'yiwan_appId',
                                                                                          yiwan_appId, mainChannel)
            appKey = appConfig.get('appKey')
        text = '%s|%s|%s' % (openid, token, appKey)
        if sign == md5(text).hexdigest():
            return True
        else:
            return False
