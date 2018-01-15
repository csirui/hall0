# -*- coding=utf-8 -*-

# Author:        zhaoqinghui@hoolai.com
# Company:       Hoolai.Inc
# Created:       2013年01月25日 星期六 00时34分53秒
# FileName:      account.py
# Class:         Account


from tyframework.context import TyContext


######################################################################
# qtld登录过程的主要逻辑实现
#
######################################################################
class AccountQtld():
    @classmethod
    def doGetUserInfo(self, rparams, snsId):
        # clientVersion = msg.getParamStr('clientVersion')
        # if clientVersion <= '2.8':
        #     TyContext.ftlog.debug('clientVersion:', clientVersion)
        #     return True
        snsToken = rparams['snsToken']
        if snsToken is None or len(snsToken) == 0:
            TyContext.ftlog.error('snsToken is not found !')
            return None
        code = snsId[5:]
        session_id = snsToken
        pid = 1
        if code == '' or len(session_id) < 20:
            TyContext.ftlog.error('snsToken error !')
            return None

        appId = rparams['appId'];
        if appId < 0:
            appId = rparams['gameId'];
        if appId < 0:
            TyContext.ftlog.error('AccountQtld the appId is not found !')
            return None

        tokenurl = 'http://www.44755.com/notify-login'
        tokenurl = tokenurl.encode('ascii')
        TyContext.ftlog.debug('AccountQtld->check url->', tokenurl)

        postdata = "uid=%s&session_id=%s&pid=%s" % (code, session_id, pid)
        response, tokenurl = TyContext.WebPage.webget(tokenurl, postdata_=postdata)
        TyContext.ftlog.debug('AccountQtld->check url->', tokenurl, 'postdata-->', str(postdata), 'return-->', response)
        infos = response
        # try:
        #     infos = json.loads(response)
        # except :
        #     TyContext.ftlog.error('AccountQtld->check url return ERROR, response=', response)
        #     pass
        if not infos is None:
            retcode = str(infos)
            if retcode == '1':
                return True
            else:
                return False
        return None

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
