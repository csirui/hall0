# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountCoolpad():
    VALIDATE_URL = 'https://openapi.coolyun.com/oauth2/token'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        client_id = params['client_id']
        code = params['coolpad_code']
        coolpad_keys = TyContext.Configure.get_global_item_json('coolpad_keys', {})
        try:
            client_secret = coolpad_keys[client_id]['appKey']
        except KeyError:
            mainChannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('coolpad',
                                                                                                 'coolpad_appId',
                                                                                                 client_id, mainChannel)
            client_secret = config.get('coolpad_appKey')
            if not client_secret:
                TyContext.ftlog.error(cls.__name__, 'cannot get coolpad sdkconfig,appid:%s' % client_id)
        redirect_uri = client_secret
        rparams = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'code': code,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri}
        # get appSecret by gid
        TyContext.ftlog.debug('AccountCoolpad-> VALIDATE_URL->', cls.VALIDATE_URL, 'rparams', rparams)
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='GET')
        TyContext.ftlog.debug('AccountCoolpad-> response->', responseMsg)
        ret = json.loads(responseMsg)
        if ret.get('openid'):
            params['snsId'] = 'coolpad:%s' % ret['openid']
            params['snsinfo'] = ret['access_token']
            return True
        else:
            return ''

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
