# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountKuaiwan():
    VALIDATE_URL = 'http://api.9665.com/sdk/ucCheck.html'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        userid = params['kw_userid']
        appId = params['kw_appId']
        rparams = {'userid': userid, 'specialid': appId}
        config = TyContext.Configure.get_global_item_json('kuaiwan_keys', {})
        try:
            appKey = config[appId]['appKey']
        except KeyError:
            mainChannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('kuaiwan',
                                                                                                 'kuaiwan_appId',
                                                                                                 appId, mainChannel)
            appKey = config.get('kuaiwan_appKey', '')
        text = 'specialid=%s&userid=%s%s' % (appId, userid, appKey)
        sign = md5(text).hexdigest()
        rparams['sign'] = sign
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, postdata_=rparams, method_='POST')
        TyContext.ftlog.debug('AccountKuaiwan-> response->', responseMsg)
        response = json.loads(responseMsg)
        if '1' == str(response['result']):
            return True
        else:
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
