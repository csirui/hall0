# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext


######################################################################
# 唱吧 登录过程的主要逻辑实现
#
######################################################################
class AccountChangba():
    VALIDATE_URL = 'http://openapi.changba.com/user/getuserinfo.php'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        appid = params['cb_appid']
        userid = params['cb_userid']
        accessToken = params['cb_accesstoken']
        secret = params['cb_secret']
        secretMd5 = md5(secret).hexdigest()
        rparams = {'ver': '1.0', 'id': appid, 'accesstoken': accessToken, 'userid': userid, 'format': 'json'}
        text = 'accesstoken=%s&format=json&id=%s&userid=%s&ver=1.0%s' % (accessToken, appid, userid, secretMd5)
        sign = md5(text).hexdigest()
        rparams['sig'] = sign
        responseMsg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='GET')
        TyContext.ftlog.debug('AccountChangba-> response ->', responseMsg)

        response = json.loads(responseMsg)
        if '0' == str(response['errno']):
            data = response['data']
            nickname = data['nickname']
            headphoto = data['headphoto']
            sex = data['gender']

            params['sex'] = int(sex) ^ 1
            params['deviceName'] = nickname
            params['name'] = nickname
            if headphoto:
                headphoto = headphoto.replace('\\/', '/')
                params['headurl'] = headphoto
                params['purl'] = headphoto

            TyContext.ftlog.debug('AccountChangba-> rparam=', params)
            return True
        else:
            return False
