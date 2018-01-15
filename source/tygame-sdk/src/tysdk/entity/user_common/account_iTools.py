# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext


######################################################################
# iTools登录过程的主要逻辑实现
# Created by Zhangshibo at 2015/09/09
# Version:2.4.1
######################################################################
class AccountiTools():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        TyContext.ftlog.debug('AccountiTools->doGetUserInfo params: %s' % params)
        TyContext.ftlog.debug('AccountiTools->doGetUserInfo snsId: %s' % snsId)
        iTools_userId = snsId[7:]
        TyContext.ftlog.debug('AccountiTools->doGetUserInfo iTools_uid is: %s' % iTools_userId)
        rparam = {}

        # 获取sessionid
        if 'snsToken' in params:
            rparam['sessionid'] = params['snsToken']
        else:
            TyContext.ftlog.error('AccountiTools->doGetUserInfo Get snsToken in parameter ERROR!')
            return False

        # 获取appid
        if 'snsAppId' in params:
            rparam['appid'] = params['snsAppId']
        else:
            TyContext.ftlog.error('AccountiTools->doGetUserInfo Get appid in parameter ERROR!')
            return False
        TyContext.ftlog.debug('AccountiTools->doGetUserInfo rparam is: ', rparam)

        # 生成sign
        rparam['sign'] = md5('&'.join([k + '=' + rparam[k] for k in sorted(rparam.keys())])).hexdigest().lower()
        TyContext.ftlog.debug('AccountiTools->doGetUserInfo sign: %s', rparam['sign'])

        # 请求iToolsSDK
        url = 'https://pay.slooti.com/?r=auth/verify'
        response, requestUrl = TyContext.WebPage.webget(url, querys=rparam)
        TyContext.ftlog.debug('AccountiTools->doGetUserInfo Request url: %s', requestUrl)

        # 判断结果
        try:
            datas = json.loads(response)
            status = datas['status']
            TyContext.ftlog.error('AccountiTools->doGetUserInfo Login Verify %s' % status)
            if 0 != cmp(status, 'success'):
                return False
            else:
                return True
        except:
            TyContext.ftlog.error('AccountiTools->doGetUserInfo Response parameter ERROR, response=%s' % response)
            return False
