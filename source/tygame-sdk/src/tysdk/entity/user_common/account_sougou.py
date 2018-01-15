# -*- coding=utf-8 -*-

import hashlib
import json

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountSougou():
    VALIDATE_URL_PRODUCT = 'http://api.app.wan.sogou.com/api/v1/login/verify'
    VALIDATE_URL_TESTING = 'http://dev.app.wan.sogou.com/api/v1/login/verify'

    VALIDATE_URL = VALIDATE_URL_TESTING

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        gid = params['gid']
        session_key = params['session_key']
        user_id = params['user_id']
        rparams = {'gid': gid, 'session_key': session_key, 'user_id': user_id}
        # get appSecret by gid
        sougou_keys = TyContext.Configure.get_global_item_json('sougou_keys', {})
        try:
            appSecret = sougou_keys[gid]['appSecret']
        except KeyError:
            mainchannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('sogou', 'sogou_gid',
                                                                                                 gid, mainchannel)
            appSecret = config.get('sogou_appSecret', '')
            if not appSecret:
                TyContext.ftlog.error(cls.__name__, 'can not find %s sdkconfig' % gid)
                return False
        text = rparams.items()
        text.sort(lambda x, y: cmp(x[0], y[0]))
        text = ['%s=%s' % x for x in text]
        text.append(appSecret)
        rparams['auth'] = hashlib.md5('&'.join(text)).hexdigest()
        TyContext.ftlog.debug('AccountSougou-> VALIDATE_URL->', cls.VALIDATE_URL, 'rparams', rparams)
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='POST')
        TyContext.ftlog.debug('AccountSougou-> response->', responseMsg)
        ret = json.loads(responseMsg)
        if ret.get('result') == 'true' or ret['result'] is True:
            return True
        else:
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
