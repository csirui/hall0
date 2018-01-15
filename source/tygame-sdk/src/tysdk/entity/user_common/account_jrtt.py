# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext


######################################################################
# JinRiTouTiaoSDK登录过程的主要逻辑实现
#
######################################################################
class AccountJRTT():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        accountId = snsId.strip()[5:]
        if not accountId:
            return False
        return cls._check_token(params, accountId)

    @classmethod
    def _check_token(cls, params, accountId):
        TyContext.ftlog.debug('AccountJRTT _check_token , params from client',
                              params)
        access_token, appid = params['snsToken'][5:].split(' ')
        toutiao_config = TyContext.Configure.get_global_item_json('jinritoutiao_config', {})
        url = toutiao_config[appid]['url']
        if not url:
            TyContext.ftlog.error('AccountJRTT _check_token not url ',
                                  url);
            return False
        url = url + 'client_key=' + appid + '&uid=' + accountId + '&access_token=' \
              + access_token
        try:
            response, _ = TyContext.WebPage.webget(url, method_='GET')
        except Exception as e:
            TyContext.ftlog.error('AccountJRTT _check_token error, exception', e)
            return False
        try:
            infos = json.loads(response)
        except Exception as e:
            TyContext.ftlog.error('AccountJRTT _check_token-> json wrong, '
                                  'response=', response, 'exception', e)
            return False
        TyContext.ftlog.info('AccountJRTT _check_token responseinfo ', infos)
        if not infos['message']:
            return False
        if infos['message'] != 'success':
            TyContext.ftlog.error('AccountJRTT _check_token message err,'
                                  'info', infos['data']['description'])
            return False
        if infos['data']['verify_result'] != 1:
            TyContext.ftlog.error('AccountJRTT _check_token message return ,'
                                  'with exception ,code', infos['data']['verify_result'])
            return False
        return True
