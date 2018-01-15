# -*- coding=utf-8 -*-
from tyframework.context import TyContext


class AccountLizi():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        uid = params['lizi_uid']
        appId = params['lizi_appid']

        TyContext.ftlog.debug('AccountLizi->', 'uid=%s,appId=%s' % (uid, appId))

        return True
