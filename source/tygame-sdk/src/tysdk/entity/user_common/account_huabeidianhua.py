# -*- coding=utf-8 -*-

import json
from hashlib import md5

import datetime

from tyframework.context import TyContext


######################################################################
# 华北电话登录过程的主要逻辑实现
# modify at 2015-09-07
# version:4.1.2
######################################################################
class AccountHuabeidianhua():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        TyContext.ftlog.debug('AccountHuabeidianhua->doGetUserInfo params: ', params)
        ret = cls.__doGetUserInfo__(params, snsId)
        TyContext.ftlog.info('AccountHuabeidianhua->doGetUserInfo', ret, snsId)
        return ret

    @classmethod
    def __doGetUserInfo__(cls, params, snsId):
        code = snsId[14:].strip()
        if code == 'null' or code == 'undefined' or len(code) <= 0:
            TyContext.ftlog.error('AccountHuabeidianhua->__doGetUserInfo__ Get code ERROR!')
            return False
        TyContext.ftlog.debug('AccountHuabeidianhua->doGetUserInfo code is: ', code)
        result, aigameuserid = cls.__get_userid(code)
        params['snsId'] = 'huabeidianhua:' + aigameuserid
        return result

    @classmethod
    def __get_userid(cls, code):
        # 目前只有单机斗地主(欢乐版)接入了登录，如果有其他的版本接入，需要另配client_id和client_secret.
        aigameConfigs = TyContext.Configure.get_global_item_json('huabeidianhua_configs', {})
        aigameuserid = ''
        postparam = {}
        try:
            postparam['client_id'] = aigameConfigs['client_id']
            postparam['client_secret'] = aigameConfigs['client_secret']
        except:
            TyContext.ftlog.error(
                'AccountHuabeidianhua->__get_userid Get client_id or client_secret failed, check aigame_configs.')
            return False, aigameuserid
        postparam['code'] = code
        postparam['grant_type'] = 'authorization_code'
        postparam['sign_method'] = 'MD5'
        postparam['version'] = '1.0'
        postparam['timestamp'] = str(datetime.datetime.now())
        postparam['sign_sort'] = 'client_id&sign_method&version&timestamp&client_secret'
        postparam['signature'] = cls.__cal_sign(postparam)
        TyContext.ftlog.debug('AccountHuabeidianhua->__get_userid signature is: %s' % postparam['signature'])

        # 用授权码换取令牌+user_id,这里只用到了user_id
        tokenurl = 'https://open.play.cn/oauth/token'
        TyContext.ftlog.debug('AccountHuabeidianhua->access token url->', tokenurl, 'param:', postparam)
        response, tokenurl = TyContext.WebPage.webget(tokenurl, {}, None, postparam)

        try:
            datas = json.loads(response)
            aigameuserid = datas['user_id']
        except:
            TyContext.ftlog.error('AccountHuabeidianhua->userid url return ERROR, response=', response)
            return False, aigameuserid
        return True, aigameuserid

    @classmethod
    def __cal_sign(cls, rparam):
        check_str = (rparam['client_id']
                     + rparam['sign_method']
                     + rparam['version']
                     + rparam['timestamp']
                     + rparam['client_secret'])
        m = md5()
        m.update(check_str)
        return m.hexdigest()
