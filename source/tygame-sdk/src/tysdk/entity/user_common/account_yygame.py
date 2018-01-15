# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext


######################################################################
# yyduowan登录过程的主要逻辑实现
#
######################################################################
class AccountYYgame():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        accountId = snsId[3:].strip()
        if not accountId:
            return False
        return cls._get_userid(params, accountId)

    @classmethod
    def _get_userid(cls, params, accountId):
        yy_config = TyContext.Configure.get_global_item_json('yy_config', {})
        try:
            appToken = params['snsToken'][3:].split(' ')
            client_sid = appToken[0]
            client_time = appToken[1]
            client_appId = appToken[2]
            appKey = yy_config[client_appId]['appkey']
            if not appKey:
                TyContext.ftlog.error('AccountYYgame _get_userid not yygame apiKey the params=', params)
                return False
        except Exception as e:
            TyContext.ftlog.error('AccountYYgame _get_userid ,exception:', e)
            return False
        server_sid = cls._cal_sign(appKey, client_appId, accountId, client_time)
        if server_sid != client_sid:
            TyContext.ftlog.error('AccountYYgame _get_userid server_sid != client_sid, \
                                  server_sid = ', server_sid, 'client_sid = ', client_sid)
            return False
        return True

    @classmethod
    def _cal_sign(cls, appkey, client_appId, accountId, client_time):
        check_str = appkey + client_appId + accountId + client_time
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        return digest
