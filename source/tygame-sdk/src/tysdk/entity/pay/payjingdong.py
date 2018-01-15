# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import base64
import json
from hashlib import md5

from tyframework.context import TyContext


class TuYouPayJingDong(object):
    appkeys = {'100000293': '83d78966187e4bea916552a61927bf62',  # 斗地主
               '100000297': 'f8f8dead01d59e8a19515b517107f182'  # 赢三张
               }

    @classmethod
    def createLinkString(self, rparam):
        print rparam
        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            ret = ret + str(k) + '=' + str(rparam[k]) + '&'
        return ret[:-1]

    @classmethod
    def buildMySign(self, rparam, appId):
        appKey = TuYouPayJingDong.appkeys[str(appId)]
        rstr = self.createLinkString(rparam) + '&' + appKey
        m = md5()
        m.update(rstr)
        ret = m.hexdigest()
        return ret

    @classmethod
    def doJingDongGetRole(self, rpath):
        appId = 0
        userId = 0
        jsondata = None
        try:
            jsondata = TyContext.RunHttp.getRequestParam('data')
            jsondata = base64.decodestring(jsondata)
            TyContext.ftlog.info('doJingDongCallback->jsondata=', jsondata)
            jsondata = json.loads(jsondata)
            appId = int(jsondata['gameId'])
            userId = int(jsondata['userId'])
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doJingDongGetRole->ERROR, param error !! jsondata=', jsondata)
            return '{"retCode": "103","retMessage": "param error","data": ""}'

        rparam = TyContext.RunHttp.convertArgsToDict()
        if not 'sign' in rparam:
            TyContext.ftlog.error('doJingDongGetRole error, no sign !!!')
            return '{"retCode": "103","retMessage": "param error","data": ""}'

        sign = rparam['sign']
        del rparam['sign']
        vSign = self.buildMySign(rparam, appId)
        if sign != vSign:
            TyContext.ftlog.info('doJingDongGetRole->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '{"retCode": "105","retMessage": "sign error","data": ""}'

        data_base64 = base64.b64encode('{"roleInfos": [{"roleId": "' + str(userId) + '","roleName": ""}]}')
        return '{"retCode": "100","retMessage": "success","data": "' + data_base64 + '"}'

    @classmethod
    def doJingDongGetOrder(self, rpath):
        # appId = 0
        jsondata = None
        try:
            jsondata = TyContext.RunHttp.getRequestParam('data')
            jsondata = base64.decodestring(jsondata)
            TyContext.ftlog.info('doJingDongCallback->jsondata=', jsondata)
            jsondata = json.loads(jsondata)
            # appId = int(jsondata['gameId'])
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doJingDongGetOrder->ERROR, param error !! jsondata=', jsondata)
            return '{"retCode": "103","retMessage": "param error","data": ""}'

        # base64.b64encode('{"orderStatus": "0"}') == eyJvcmRlclN0YXR1cyI6ICIwIn0=
        return '{"retCode": "100","retMessage": "success","data": "eyJvcmRlclN0YXR1cyI6ICIwIn0="}'

    @classmethod
    def doJingDongCallback(self, rpath):
        appId = 0
        jsondata = None
        try:
            jsondata = TyContext.RunHttp.getRequestParam('data')
            jsondata = base64.decodestring(jsondata)
            TyContext.ftlog.info('doJingDongCallback->jsondata=', jsondata)
            jsondata = json.loads(jsondata)
            appId = int(jsondata['gameId'])
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doWanDouJiaCallback->ERROR, param error !! jsondata=', jsondata)
            return '{"retCode": "103","retMessage": "param error","data": ""}'

        rparam = TyContext.RunHttp.convertArgsToDict()
        if not 'sign' in rparam:
            TyContext.ftlog.error('doWanDouJiaCallback error, no sign !!!')
            return 'error'

        sign = rparam['sign']
        del rparam['sign']
        vSign = self.buildMySign(rparam, appId)
        if sign != vSign:
            TyContext.ftlog.info('doJingDongCallback->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '{"retCode": "105","retMessage": "sign error","data": ""}'

        orderPlatformId = jsondata['orderId']

        trade_status = 'TRADE_FINISHED'
        total_fee = int(float(jsondata['chargeMoney']))

        from tysdk.entity.pay.pay import TuyouPay
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            # base64.b64encode('{"orderStatus": "0"}') == eyJvcmRlclN0YXR1cyI6ICIwIn0=
            return '{"retCode": "100","retMessage": "success","data": "eyJvcmRlclN0YXR1cyI6ICIwIn0="}'
        else:
            return '{"retCode": "999","retMessage": "param error","data": ""}'
