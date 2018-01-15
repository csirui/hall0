# -*- coding=utf-8 -*-
import json
import re
import urllib

from tyframework.context import TyContext
from tysdk.entity.user3.account_check import AccountCheck

'''
  推送

'''


class HttpPushV3(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v3/push/submitPushToken': cls.submitPushToken,
            }
            AccountCheck.__init_checker__()
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                # '/open/vc/user/smsCallback': cls.doSmsBindCallBack,
            }
            AccountCheck.__init_checker__()
        return cls.HTMLPATHS

    @classmethod
    def checkAccount(cls, rpath):
        # return AccountCheck.normal_check(rpath, False)
        return AccountCheck.normal_check(rpath)

    @classmethod
    def submitPushToken(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        clientId = rparams.get('clientId', '')
        clientVersion = TyContext.ClientUtils.getVersionFromClientId(clientId);
        if clientVersion < 3.77:
            url = TyContext.Configure.get_global_item_str('push.server', '')
        else:
            url = TyContext.Configure.get_global_item_str('push.server.new', '')

        mo = TyContext.Cls_MsgPack()
        if url == '':
            mo.setResult('code', 0)
            mo.setResult('info', 'push server is null')
            return mo

        if clientVersion >= 3.77:
            # 都从SDK发出来，校验HTTP数据的安全性，校验code
            isReturn, params = AccountCheck.normal_check(rpath, False)
            if isReturn:
                return params

            url += '/push_register'
            postdata = urllib.urlencode(rparams)
            TyContext.ftlog.debug('updateToken 1 url=', url, 'rparams:', rparams, 'postdata:', postdata)
            response, url = TyContext.WebPage.webget(url, {}, None, postdata)
            code = 1
            try:
                datas = json.loads(response)
                code = datas['code']
            except:
                TyContext.ftlog.error('updateToken 1 return ERROR, response=', response)
            if code == 200:
                mo.setResult('code', 0)
                mo.setResult('info', 'success')
            else:
                mo.setResult('code', 1)
                mo.setResult('info', 'fail')
            return mo
        else:
            # url = 'http://127.0.0.1:8080/token/update'
            # url = 'http://125.39.218.101:8080/push/updateToken'
            m = re.search('0\-hall(\d+)', clientId)
            if m:
                appId = m.group(1)
            else:
                appId = '9999'
            TyContext.RunHttp.set_request_arg("appId", appId)
            TyContext.RunHttp.set_request_arg("imei", 'null')
            isReturn, params = AccountCheck.normal_check(rpath, False)
            if isReturn:
                return params

            url += '/push/updateToken'
            params = TyContext.RunHttp.convertArgsToDict()
            postdata = urllib.urlencode(params)
            TyContext.ftlog.debug('updateToken url=', url, 'postdata:', postdata)
            response, url = TyContext.WebPage.webget(url, {}, None, postdata)
            ec = 1
            try:
                datas = json.loads(response)
                ec = datas['ec']
            except:
                TyContext.ftlog.error('updateToken return ERROR, response=', response)
            if ec == 0:
                mo.setResult('code', 0)
                mo.setResult('info', 'success')
            else:
                mo.setResult('code', 1)
                mo.setResult('info', 'fail')
            return mo
