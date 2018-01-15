# -*- coding=utf-8 -*-
from tyframework.context import TyContext


class AccountLiebao():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        token = snsId[7:]
        verify_url = 'https://xopen.ksmobile.com/1/api/oauth2/me?access_token=%s' % token
        response, _ = TyContext.WebPage.webget(verify_url, method_="GET")
        open_id = ''
        import json
        try:
            response = json.loads(response)
            open_id = response.get('open_id_str', '')
        except:
            return False
        if not open_id:
            return False
        params['snsId'] = 'liebao:%s' % open_id
        return True
