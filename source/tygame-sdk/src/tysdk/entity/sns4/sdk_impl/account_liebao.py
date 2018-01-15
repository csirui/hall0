# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext
from tysdk.entity.sns4.decorator.snsv4_base import SnsV4Base
from tysdk.entity.sns4.decorator.snsv4_login import snsv4_login


class AccountLiebaoV4(SnsV4Base):
    @snsv4_login('liebao')
    def doGetUserInfo(self, rparams, snsId):
        snsToken = rparams['snsToken']
        if snsToken is None or len(snsToken) == 0:
            TyContext.ftlog.error('snsToken is not found !')
            return None
        openid = snsId[3:]
        token = snsToken
        if not token or not openid:
            TyContext.ftlog.error('AccountWeixin token', token,
                                  'or openid', openid, 'error!')
            return None

        appId = rparams['appId']
        if appId < 0:
            appId = rparams['gameId']
        if appId < 0:
            TyContext.ftlog.error('AccountQtld the appId is not found !')
            return None

        infourl = 'https://api.weixin.qq.com/sns/userinfo?' \
                  'access_token=%s&openid=%s' % (token, openid)
        TyContext.ftlog.debug('AccountWeixin->infourl->', infourl)

        response, infourl = TyContext.WebPage.webget(infourl)
        TyContext.ftlog.info('AccountWeixin->return-->', response)
        infos = response
        try:
            infos = json.loads(response)
        except:
            TyContext.ftlog.error('AccountWeixin->infourl json wrong, response=', response)
            return False

        try:
            unionid = infos['unionid']
        except:
            TyContext.ftlog.error('AccountWeixin->infourl unionid absent, response=', response)
            return False

        TyContext.ftlog.debug('AccountWeixin->infos=', infos)
        rparams['snsId'] = 'wx:' + unionid
        rparams['sex'] = int(infos.get('sex', 1)) ^ 1
        rparams['name'] = infos.get('nickname')
        purl = infos.get('headimgurl')
        if purl:
            purl = purl.replace('\\/', '/') + '.jpg'
            rparams['purl'] = purl
        return True
