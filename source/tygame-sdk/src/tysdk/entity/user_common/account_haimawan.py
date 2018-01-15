# -*- coding=utf-8 -*-

from urllib import urlencode

from tyframework.context import TyContext


######################################################################
# 海马玩登录过程的主要逻辑实现
# Created by Zhangshibo at 2015/08/18
######################################################################
class AccountHaiMaWan():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        # 获取参数appid和validateToken
        rparam = {}
        try:
            rparam['appid'] = params['snsAppId']
            rparam['t'] = params['snsToken']
            rparam['uid'] = snsId[len('haimawan:'):]
        except Exception as e:
            TyContext.ftlog.error('AccountHaiMaWan->doGetUserInfo get appid|token ERROR!', e)
            return False

        # 向海马玩服务器发验证请求
        strRequestUrl = 'http://api.haimawan.com/index.php?m=api&a=validate_token'
        strParam = urlencode(rparam)
        strReponse, strHttpUrl = TyContext.WebPage.webget(strRequestUrl, postdata_=strParam, method_='POST')
        TyContext.ftlog.debug('AccountHaiMaWan->doGetUserInfo Request is: [', strHttpUrl,
                              '] params is: [', strParam, '] Reponse is: [', strReponse, ']')

        # 判断结果
        if strReponse and strReponse.startswith('success'):  # 0 == cmp(strReponse, 'success'):
            return True
        else:
            del rparam['uid']
            strRequestUrl = 'http://api.haimawan.com/index.php?m=api&a=validate_token'
            strParam = urlencode(rparam)
            strReponse, strHttpUrl = TyContext.WebPage.webget(strRequestUrl, postdata_=strParam, method_='POST')
            TyContext.ftlog.debug('AccountHaiMaWan->doGetUserInfo2 response is: [', strReponse)
            if 0 == cmp(strReponse, 'success'):
                return True
            return False
