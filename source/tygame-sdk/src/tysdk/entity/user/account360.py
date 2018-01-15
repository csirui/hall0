# -*- coding=utf-8 -*-

# Author:        zhaoqinghui@hoolai.com
# Company:       Hoolai.Inc
# Created:       2013年01月25日 星期六 00时34分53秒
# FileName:      account.py
# Class:         Account

import json

from tyframework.context import TyContext


######################################################################
# 360登录过程的主要逻辑实现
#
######################################################################
class Account360():
    @classmethod
    def isDefault360Username(cls, username):
        if not isinstance(username, unicode):
            username = str(username)
        return username and username.startswith('360U')

    @classmethod
    def doGetUserInfo(self, snsId, msg):
        code = snsId[4:]
        appId = msg.getParamInt('appId', 0);
        if appId < 0:
            appId = msg.getParamInt('gameId', 0);
        if appId < 0:
            TyContext.ftlog.error('Account360 the appId is not found !')
            return None

        # client_id = ConfigItems.getAppInfo( appId, 'app.360.clientid')
        # client_secret = ConfigItems.getAppInfo( appId, 'app.360.secret')
        clientId = msg.getParamStr('clientId', '')
        client_ids = TyContext.Configure.get_game_item_json(appId, 'account.360.client.version', {})
        clientver = ''
        if clientId in client_ids:
            clientver = str(client_ids[clientId])
        client_id = TyContext.Configure.get_game_item_str(appId, 'account.360.client.id' + clientver)
        client_secret = TyContext.Configure.get_game_item_str(appId, 'account.360.client.secret' + clientver)

        if not client_id or not client_secret:
            TyContext.ftlog.error('Account360 the appinfo of appId %d is not found !' % (appId))
            return None

        tokenurl = 'https://openapi.360.cn/oauth2/access_token?grant_type=authorization_code&' + \
                   'client_id=%s&client_secret=%s&redirect_uri=oob&code=%s' % (client_id, client_secret, code)
        tokenurl = tokenurl.encode('ascii')
        TyContext.ftlog.debug('Account360->access token url->', tokenurl)
        response, tokenurl = TyContext.WebPage.webget(tokenurl)
        TyContext.ftlog.debug('Account360->access token url->', tokenurl, 'return-->', response)
        accessToken = None
        try:
            datas = json.loads(response)
            if 'access_token' in datas:
                accessToken = datas['access_token']
        except:
            TyContext.ftlog.error('Account360->access token url return ERROR, response=', response)
            pass
        infos = None
        if accessToken != None:
            infourl = 'https://openapi.360.cn/user/me.json?fields=id,name,avatar,sex,area&access_token=' + accessToken
            infourl = infourl.encode('ascii')
            TyContext.ftlog.debug('Account360->user info url->', infourl)
            response, infourl = TyContext.WebPage.webget(infourl)
            TyContext.ftlog.debug('Account360->user info url->', infourl, 'response-->', response)
            try:
                infos = json.loads(response)
            except:
                TyContext.ftlog.error('Account360->user info url return ERROR, response=', response)
                pass
        if infos != None:
            msg.setParam('snsId', '360:' + str(infos['id']))
            if appId != 8:
                msg.setParam('name', infos['name'])
            msg.setParam('snsinfo', infos['name'])
            # msg.setParam('purl', infos['avatar'])
            if appId != 8:
                sex360 = repr(infos['sex']).replace('\\', '').replace('\'', '')
                sexMem = repr('男').replace('\\', '').replace('\'', '')
                if sex360.find(sexMem) >= 0:
                    msg.setParam('sex', 1)
                else:
                    msg.setParam('sex', 0)
            msg.setParam('address', infos['area'])
            return True
        return None

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
