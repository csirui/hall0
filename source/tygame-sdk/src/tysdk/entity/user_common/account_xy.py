# -*- coding=utf-8 -*-

import json
from urllib import urlencode

from tyframework.context import TyContext


######################################################################
# XY苹果助手登录过程的主要逻辑实现
# Created by Zhangshibo at 2015/08/12
######################################################################
class AccountXY():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        rparam = {}
        rparam['uid'] = params["snsId"][3:]
        rparam['appid'] = params["snsAppId"]
        rparam['token'] = params["snsToken"]
        paramStr = urlencode(rparam)

        # 访问XY助手的接口，查询用户的登录状态
        getidurl = 'http://passport.xyzs.com/checkLogin.php'
        TyContext.ftlog.debug('AccountXY->access url->', getidurl)
        response, tokenurl = TyContext.WebPage.webget(getidurl, postdata_=paramStr)
        TyContext.ftlog.debug('AccountXY->access response=', response)

        try:
            datas = json.loads(response)
            ret = datas['ret']
            errormsg = datas['error']
            if 0 != ret:
                TyContext.ftlog.error('AccountXY->access url return ERROR:', errormsg)
                return False
        except:
            TyContext.ftlog.error('AccountXY->get userid url return ERROR, response=', response)
            return False
        return True
