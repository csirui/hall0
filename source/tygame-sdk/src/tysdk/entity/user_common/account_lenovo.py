# -*- coding=utf-8 -*-

from xml.etree import ElementTree

from tyframework.context import TyContext


class AccountLenovo():
    VALIDATE_URL = "http://passport.lenovo.com/interserver/authen/1.2/getaccountid"

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        rparams = {'lpsust': params['lpsust'], 'realm': params['_appid']}
        response_msg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='GET')
        TyContext.ftlog.debug('AccountLenovo-> response ->', response_msg)
        xmlResponse = ElementTree.fromstring(response_msg)
        uid = xmlResponse.find('AccountID').text
        params['snsId'] = 'lenovo:' + uid
        TyContext.ftlog.debug('AccountLenovo-> uid ->', uid)
        return True
