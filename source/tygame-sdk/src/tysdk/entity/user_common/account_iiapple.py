# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext


######################################################################
# 爱苹果登录过程的主要逻辑实现
#
######################################################################
class AccountIIApple():
    @classmethod
    def doGetUserInfo(cls, params, snsId):

        iiapple_paykeys = TyContext.Configure.get_global_item_json('iiapple_paykeys', {})
        iiapple_paykeys_new = TyContext.Configure.get_global_item_json('iiapple_paykeys_new', {})

        for sub_clientid in iiapple_paykeys_new.keys():
            if params['clientId'].find(sub_clientid) > 0:
                gameKey = iiapple_paykeys_new[sub_clientid]['gameKey']
                secretKey = iiapple_paykeys_new[sub_clientid]['secretKey']
                tokenUrl = iiapple_paykeys_new[sub_clientid]['tokenUrl']
                break
        else:
            secretKey = iiapple_paykeys['secretKey']
            gameKey = iiapple_paykeys['gameKey']
            secretKey = iiapple_paykeys['secretKey']
            tokenUrl = iiapple_paykeys['tokenUrl']
        rparams = {
            'game_id': gameKey,
            'user_id': params['userid'],
            'session': params['session']
        }
        ###
        m = md5()
        m.update('game_id=%s&session=%s&user_id=%s' % (rparams['game_id'], rparams['session'], rparams['user_id']))
        m2 = md5()
        m2.update('%s%s' % (m.hexdigest().lower(), secretKey))
        rparams['_sign'] = m2.hexdigest().lower()

        TyContext.ftlog.debug('AccountIIApple-> tokenUrl->', tokenUrl, 'rparams', rparams)

        responseMsg, _ = TyContext.WebPage.webget(tokenUrl, rparams, method_='GET')
        response = json.loads(responseMsg)
        TyContext.ftlog.debug('AccountIIApple-> response->', response)

        # 1:成功 其他失败
        if 1 == int(response['status']):
            TyContext.ftlog.debug('AccountIIApple ', responseMsg)
            return True
        else:
            TyContext.ftlog.error('AccountIIApple ', responseMsg)
            return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
