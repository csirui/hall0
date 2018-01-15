# -*- coding=utf-8 -*-

# Author:        zhaoqinghui@hoolai.com
# Company:       Hoolai.Inc
# Created:       2013年01月25日 星期六 00时34分53秒
# FileName:      account.py
# Class:         Account

import json

from tyframework.context import TyContext


######################################################################
# momo登录过程的主要逻辑实现
#
######################################################################
class AccountMomo():
    # appId = 'ex_ddz_8nTFeiGK'
    # appSecret = 'EDE4378B-B0AD-09FA-8941-356DF6D90342'

    @classmethod
    def doGetUserInfo(self, snsId, msg):
        clientVersion = msg.getParamStr('clientVersion')
        if clientVersion <= '2.8':
            TyContext.ftlog.debug('clientVersion:', clientVersion)
            return True
        snsToken = msg.getParamStr('snsToken')
        if snsToken is None or len(snsToken) == 0:
            TyContext.ftlog.error('snsToken is not found !')
            return None
        code = snsId[5:]
        appId = msg.getParamInt('appId', 0);
        if appId < 0:
            appId = msg.getParamInt('gameId', 0);
        if appId < 0:
            TyContext.ftlog.error('AccountMomo the appId is not found !')
            return None

        # clientId = msg.getParamStr('clientId', '')
        # client_ids = ConfigItems.getGameItemJson( appId, 'account.360.client.version', {})
        # clientver = ''
        # if clientId in client_ids:
        #     clientver = str(client_ids[clientId])
        client_id = TyContext.Configure.get_game_item_str(appId, 'account.momo.client.id' + '')
        client_secret = TyContext.Configure.get_game_item(appId, 'account.momo.client.secret' + '')

        if not client_id or not client_secret:
            TyContext.ftlog.error('AccountMomo the appinfo of appId %d is not found !' % (appId))
            return None

        tokenurl = 'https://game-api.immomo.com/game/2/server/app/check?appid=%s&' + \
                   'app_secret=%s&vtoken=%s&userid=%s' % (client_id, client_secret, snsToken, code)
        tokenurl = tokenurl.encode('ascii')
        TyContext.ftlog.debug('AccountMomo->check url->', tokenurl)
        response, tokenurl = TyContext.WebPage.webget(tokenurl)
        TyContext.ftlog.debug('AccountMomo->check url->', tokenurl, 'return-->', response)
        infos = None
        try:
            infos = json.loads(response)
        except:
            TyContext.ftlog.error('AccountMomo->check url return ERROR, response=', response)
            pass
        if not infos is None:
            ec = int(infos['ec'])
            if ec > 0:
                msg.setParam('code', ec)
                return False
            if not infos.has_key('data'):
                return False
            datas = infos['data']
            msg.setParam('snsId', snsId)
            msg.setParam('name', datas['name'])
            msg.setParam('snsinfo', datas['name'])
            # msg.setParam('purl', infos['avatar'])
            if datas['sex'] == 'M':
                msg.setParam('sex', 0)
            else:
                msg.setParam('sex', 1)
            # msg.setParam('address', infos['area'])
            return True
        return None

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
