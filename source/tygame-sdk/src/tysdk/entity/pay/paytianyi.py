# -*- coding=utf-8 -*-

from hashlib import sha1
from urllib import urlencode

from tyframework.context import TyContext


class TuYouPayTianYi():
    # 订单签名验证key
    sign_sha_key = 'cab1c89c19ebb56f'

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        payCode = 'E85CBFBF6BD0FD49E040640A041E48FB'
        if prodId == 'T20K':
            payCode = 'E85CBFBF6BCEFD49E040640A041E48FB'
        if prodId == 'T50K':
            payCode = 'E85CBFBF6BCFFD49E040640A041E48FB'
        if prodId == 'T100K':
            payCode = 'E85CBFBF6BD0FD49E040640A041E48FB'
        if prodId == 'MOONKEY':
            payCode = 'E85CBFBF6BD1FD49E040640A041E48FB'
        if prodId == 'MOONKEY3':
            payCode = 'E85CBFBF6BD2FD49E040640A041E48FB'
        if prodId == 'VOICE100':
            payCode = 'E85CBFBF6BD3FD49E040640A041E48FB'
        if prodId == 'RAFFLE':
            payCode = 'E85CBFBF6BCEFD49E040640A041E48FB'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def createLinkString(self, rparam):
        print rparam
        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            ret = ret + str(k) + str(rparam[k])
        return ret

    @classmethod
    def buildMySign(self, rparam):
        rstr = urlencode(self.createLinkString(rparam)) + TuYouPayTianYi.sign_sha_key
        m = sha1()
        m.update(rstr)
        ret = m.hexdigest()
        return ret

    @classmethod
    def doTianyiCallbackMsg(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        if not 'sig' in rparam:
            TyContext.ftlog.error('doTianyiCallbackMsg error, no sign !!!')
            return '{"resultCode":"1111","resultDesc":"参数错误"}'

        sign = rparam['sig']
        del rparam['sig']
        vSign = self.buildMySign(rparam)
        if sign != vSign:
            TyContext.ftlog.info('doTianyiCallbackMsg->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '{"resultCode":"2222","resultDesc":"sig不正确"}'
        # 原始游戏订单号
        orderPlatformId = rparam['txId']
        TyContext.ftlog.info('TuYouPayTianYi.doTianyiCallbackMsg orderPlatformId=', orderPlatformId)

        from tysdk.entity.pay.pay import TuyouPay

        if int(rparam['chargeResult']) == 0:
            trade_status = 'TRADE_FINISHED'
            total_fee = -1
            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
            if isOk:
                return '{"resultCode":"0000","resultDesc":"通知成功"}'
            else:
                return '{"resultCode":"3333","resultDesc":"失败"}'
        pass
