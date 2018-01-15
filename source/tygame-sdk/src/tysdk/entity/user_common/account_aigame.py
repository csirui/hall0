# -*- coding=utf-8 -*-

import json

import datetime

from tyframework.context import TyContext


######################################################################
# 爱游戏登录过程的主要逻辑实现
#
######################################################################
class AccountAigame():
    sexMem = repr('男').replace('\\', '').replace('\'', '')

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        ret = cls.__doGetUserInfo__(params, snsId)
        TyContext.ftlog.info('doGetUserInfoAigame', ret, snsId)
        return ret

    @classmethod
    def __doGetUserInfo__(cls, params, snsId):
        code = snsId[11:].strip()
        if code == 'null' or code == 'undefined' or len(code) <= 0:
            return False

        aigameuserid = cls.__get_userid(params, code)
        params['snsId'] = 'aigame:' + aigameuserid
        return aigameuserid

    @classmethod
    def __get_userid(cls, params, code):
        aigameConfigs = TyContext.Configure.get_global_item_json('aigame_configs', {})
        appId = params['appId'];
        clientId = params['clientId']
        postparam = {}
        postparam['client_id'] = aigameConfigs['client_id']
        postparam['code'] = code
        postparam['grant_type'] = 'authorization_code'
        postparam['ClientSecret'] = aigameConfigs['ClientSecret']
        postparam['sign_method'] = 'MD5'
        postparam['version'] = '1.0'
        postparam['timestamp'] = str(datetime.datetime.now())
        postparam['sign_sort'] = 'client_id&sign_method&version&timestamp&client_secret'
        postparam['signature'] = cls.__cal_sign(postparam)

        tokenurl = 'https://open.play.cn/oauth/token'
        TyContext.ftlog.debug('AccountAigame->access token url->', tokenurl, 'param:', postparam)
        response, tokenurl = TyContext.WebPage.webget(tokenurl, {}, None, postparam)

        try:
            datas = json.loads(response)
            # accessToken = datas['access_token']
            aigameuserid = datas['user_id']
        except:
            TyContext.ftlog.error('AccountAigame->userid url return ERROR, response=', response)
            return False
        return True

    @classmethod
    def __cal_sign(cls, rparam):
        check_str = (rparam['client_id']
                     + rparam['sign_method']
                     + rparam['version']
                     + rparam['timestamp']
                     + rparam['client_secret'])
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        return digest
