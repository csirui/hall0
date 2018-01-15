# -*- coding=utf-8 -*-

from tyframework.context import TyContext

######################################################################
# 木蚂蚁登录过程的主要逻辑实现
#
######################################################################
from tysdk.entity.pay.rsacrypto import rsaVerify


class AccountJolo():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        uid = params['userId']
        session = params['session']
        account = params['account']
        accountSign = params['accountSign']
        TyContext.ftlog.debug('AccountJolo-> getUserInfo', 'account=%s' % account, 'accountSign=%s' % accountSign)
        if not rsaVerify(account, accountSign, 'jolo'):
            return False
        params['snsinfo'] = session
        return True
        # rparams = {'uid': uid, 'access_token':access_token, 'app_id':app_id}
        # config = TyContext.Configure.get_global_item_json('zhuoyi_keys', {})
        # for keys in config.values():
        #    if keys['appId'] == app_id:
        #        appKey = keys['paySecret']
        #        break
        # else:
        #    return False
        #
        # 0:成功 1:无效的 token 2:用户不存在 3:会话超时
        # if '0' == str(response['code']):
        #    return True
        # else:
        #    return False

# ------------------------------------------------------------------------------
# End of File
# ------------------------------------------------------------------------------
