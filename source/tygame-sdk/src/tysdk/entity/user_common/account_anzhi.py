# -*- coding=utf-8 -*-

######################################################################
# 安智登录过程的主要逻辑实现
# Created by Zhangshibo at 2015/10/12
# Version: 3.2
######################################################################
import json
from base64 import b64encode, b64decode
from urllib import urlencode

import datetime

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure


class AccountAnZhi():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        TyContext.ftlog.info('AccountAnZhi->doGetUserInfo Params is: ', params)
        rparam = {}
        rparam['time'] = str(datetime.datetime.now()).replace('-', '').replace(' ', '') \
                             .replace(':', '').replace('.', '')[:-3]
        if 'snsToken' in params:
            rparam['sid'], rparam['appkey'] = params["snsToken"].split(' ')
        else:
            TyContext.ftlog.error('AccountAnZhi->doGetUserInfo ERROR Cann\'t find snsToken.')
            return False

        anzhiconfig = TyContext.Configure.get_global_item_json('anzhi_config', {})
        appSecret = ""
        if anzhiconfig:
            for item in anzhiconfig:
                if 0 == cmp(item['appId'], rparam['appkey']):
                    appSecret = item['appsecret']
                    break
            else:
                TyContext.ftlog.error('AccountAnZhi->doGetUserInfo ERROR Cann\'t find appsecert, appId is: ',
                                      rparam['appkey'])
        else:
            TyContext.ftlog.error('AccountAnZhi->doGetUserInfo ERROR cann\'t find anzhi_config.')
        if not appSecret:
            mainchannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('anzhi',
                                                                                                 'anzhi_appKey',
                                                                                                 rparam['appkey'],
                                                                                                 mainchannel)
            if not config:
                return False
            appSecret = config.get('anzhi_appSecret')
        rparam['sign'] = b64encode(rparam['appkey'] + rparam['sid'] + appSecret)
        requestBody = urlencode(rparam)

        # 访问安智的接口，查询用户的登录状态
        getidurl = 'http://user.anzhi.com/web/api/sdk/third/1/queryislogin'
        TyContext.ftlog.debug('AccountAnZhi->doGetUserInfo url->', getidurl)
        response, tokenurl = TyContext.WebPage.webget(getidurl, postdata_=requestBody)
        TyContext.ftlog.debug('AccountAnZhi->doGetUserInfo response=', response)

        try:
            response = response.replace("'", "\"")
            datas = json.loads(response)
            ret = int(datas['sc'])
            errormsg = datas['st']
            uid = json.loads(b64decode(datas['msg']).replace("'", "\""))['uid']
            if 1 != ret:
                TyContext.ftlog.error('AccountAnZhi->doGetUserInfo url return ERROR:', errormsg)
                return False
        except Exception as e:
            TyContext.ftlog.error('AccountAnZhi->doGetUserInfo get userid url return ERROR, response=', response, e)
            return False

        params['snsId'] = 'anzhi:' + uid
        return True
