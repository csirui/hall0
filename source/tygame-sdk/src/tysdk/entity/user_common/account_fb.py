# -*- coding=utf-8 -*-

import json
import urllib2

from tyframework.context import TyContext


class AccountFaceBook():
    @classmethod
    def doGetUserInfo(self, rparams, snsId):
        snsToken = rparams['snsToken']
        if snsToken is None or len(snsToken) == 0:
            TyContext.ftlog.error('snsToken is not found !')
            return None
        openid = snsId[3:]
        token = snsToken
        if not token or not openid:
            TyContext.ftlog.error('AccountFaceBook token', token,
                                  'or openid', openid, 'error!')
            return None

        appId = rparams['appId']
        if appId < 0:
            appId = rparams['gameId']
        if appId < 0:
            TyContext.ftlog.error('AccountFaceBook the appId is not found !')
            return None

        infourl = 'https://graph.facebook.com/me?fields=id,name,picture,gender&access_token=%s' % token
        TyContext.ftlog.debug('AccountFaceBook->infourl->', infourl)

        # response, infourl = TyContext.WebPage.webget(infourl)
        try:
            f = urllib2.urlopen(infourl)
            response = f.read()
            f.close()
            TyContext.ftlog.info('AccountFaceBook->return-->', response)
            infos = json.loads(response)
        except:
            TyContext.ftlog.error('AccountFaceBook->infourl wrong, response=', response)
            return False

        try:
            unionid = infos['id']
        except:
            TyContext.ftlog.error('AccountFaceBook->infourl id absent, response=', response)
            return False

        TyContext.ftlog.debug('AccountFaceBook->infos=', infos)
        rparams['snsId'] = 'fb:' + unionid
        sex = infos.get("gender", "male")
        rparams['sex'] = 0 if sex == "male" else 1
        name = infos.get('name', "")
        rparams['name'] = name.strip()[0:16]
        picture = infos.get('picture')
        if picture:
            data = picture.get('data')
            if data:
                purl = data.get('url')
                if purl:
                    purl = purl.replace('\\/', '/')
                    rparams['purl'] = purl
        return True
