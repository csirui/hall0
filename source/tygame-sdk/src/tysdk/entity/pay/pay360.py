# -*- coding=utf-8 -*-

import json
from hashlib import md5
from urllib import quote

from constants import CHARGE_RATE_RMB
from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class TuYouPay360():
    DEBUG360 = True
    # 商户id和密钥，由360提供
    merchant_code = "3337100050";
    merchant_security_code = "53c3985592a0dced717c014092d7718b";

    # 360支付url
    pay_request_url = "https://mpay.360.cn/gateway/do?";
    query_request_url = "http://query.mpay.360.cn/trans/get?";
    no_notify_url = "http://mpay.360.cn/noReturn/notify";

    notify_url = "/v1/pay/360/callback";

    bank_code = ['MOBILE_ZFB', 'SZX_CARD', 'LT_CARD', 'DX_CARD', 'JCARD', 'QIHU_CARD']
    trans_service = 'direct_pay'
    input_cha = 'UTF-8'
    sign_type = 'MD5'

    # 订单回调签名验证key
    sign_skey = 'TUYOU!Qaz2wsx360msg'

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
    def createLinkString4Get(self, rparam):
        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            ret = ret + str(k) + '=' + quote(str(rparam[k]), '') + '&'
        return ret[:-1]

    @classmethod
    def buildMySign(self, rparam):
        rstr = self.createLinkString(rparam) + TuYouPay360.merchant_security_code
        m = md5()
        m.update(rstr)
        ret = m.hexdigest()
        return ret

    @classmethod
    def getPayUrl(self, rparam):
        return TuYouPay360.pay_request_url + self.createLinkString4Get(rparam)

    @classmethod
    def payRequest(self, rparam, datas, bankIndex):
        purl = self.getPayUrl(rparam)
        TyContext.ftlog.info('TuYouPay360->requestUrl=', purl)
        response, purl = TyContext.WebPage.webget(purl)
        return self.getStatus(response, rparam, datas, bankIndex)

    @classmethod
    def getStatus(self, page, rparam, datas, bankIndex):
        TyContext.ftlog.info('TuYouPay360->request->return bankIndex=', bankIndex, 'page=', page)
        if bankIndex == 0:
            return self.doPayRequestAliDone(page, rparam, datas)
        elif bankIndex == 1:
            return self.doPayRequestCardDone(page, rparam, datas)
        elif bankIndex == 2:
            return self.doPayRequestCardDone(page, rparam, datas)
        elif bankIndex == 3:
            return self.doPayRequestCardDone(page, rparam, datas)

    @classmethod
    def _getPayRequsetParams(self, datas, bankIndex):
        httpdomain = PayHelper.getSdkDomain()
        rparam = {}
        # 游戏分配的订单号,这个必须是没用到过的，如果用过的trade_code，会返回-1004错误
        rparam['mer_trade_code'] = datas['orderPlatformId']
        # 商户发送的支付金额
        rparam['rec_amount'] = int(datas['orderPrice'])
        #         if TuYouPay360.DEBUG360 :
        #             rparam['rec_amount'] = 0.01

        rparam['product_name'] = 'TYB' + str(rparam['rec_amount'] * CHARGE_RATE_RMB)
        # 商户ID
        rparam['mer_code'] = TuYouPay360.merchant_code
        rparam['trans_service'] = TuYouPay360.trans_service
        rparam['input_cha'] = TuYouPay360.input_cha
        rparam['sign_type'] = TuYouPay360.sign_type
        rparam['notify_url'] = httpdomain + TuYouPay360.notify_url
        rparam['return_url'] = TuYouPay360.no_notify_url
        rparam['bank_code'] = TuYouPay360.bank_code[bankIndex]  # "MOBILE_ZFB",子支付的区分 MOBILE_ZFB 支付宝
        if bankIndex in (1, 2, 3):
            rparam['card_amount'] = datas['card_amount']
            rparam['card_number'] = datas['card_number']
            rparam['card_pwd'] = datas['card_pwd']
        rparam['sign'] = self.buildMySign(rparam)

        TyContext.ftlog.info('TuYouPay360->params=', rparam)
        return rparam

    @classmethod
    def doPayRequestAli(self, datas):
        rparam = self._getPayRequsetParams(datas, 0)
        return self.payRequest(rparam, datas, 0)

    @classmethod
    def doPayRequestAliDone(self, page, rparam, datas):
        # 成功的返回如下，可以发回客户端，由客户端调用支付宝
        # {"code":"success","paydata":"partner=\"2088701816336850\"&seller=\"mobilepay@360.cn\"&out_trade_no=\"0830120418153417112\"&subject=\"360Coin\"&body=\"360Coin\"&total_fee=\"10\"&notify_url=\"https%3A%2F%2Fapi.360pay.cn%2Freturn%2Fnotify%2FchannelId%2F10005\"&sign=\"IPYiJda%2Br%2BLqTLBwJ%2FJKlj8EPzy6k%2Bxhv4DDxRsQOvV81StDZHuro%2Fgl2UlAUidskqSVgwsJ6jEd1uw4maLQ72N65EZ6KIzObvI7rzXxFhQV%2BY0ReyCcxqp7DvdWUGT1T8O32ckpgXHi1N41Nv%2FbMQB1hTp3Xr%2Bw6zLgIckuLBE%3D\"&sign_type=\"RSA\""}
        jsons = None
        try:
            jsons = json.loads(page)
            if 'code' in jsons:
                if not jsons['code'] == 'success':
                    jsons = {'code': 'error', 'info': 'net work error'}
            else:
                jsons = {'code': 'error', 'info': 'net work error'}
        except:
            jsons = {'code': 'error', 'info': 'net work error'}

        mo = TyContext.Cls_MsgPack()
        from tysdk.entity.pay.pay import TuyouPay
        TuyouPay.makeBuyChargeMessage(mo, datas)
        if jsons['code'] == 'success':
            mo.setResult('payData', jsons['paydata'])
        else:
            mo.setResult('payData', '')
            mo.setResult('code', 1)
            if 'info' in jsons:
                mo.setResult('info', jsons['info'])
            else:
                mo.setResult('info', 'net work error')
        return mo

    @classmethod
    def doPayRequestCardYd(self, datas):
        rparam = self._getPayRequsetParams(datas, 1)
        return self.payRequest(rparam, datas, 1)

    @classmethod
    def doPayRequestCardLt(self, datas):
        rparam = self._getPayRequsetParams(datas, 2)
        return self.payRequest(rparam, datas, 2)

    @classmethod
    def doPayRequestCardDx(self, datas):
        rparam = self._getPayRequsetParams(datas, 3)
        return self.payRequest(rparam, datas, 3)

    @classmethod
    def doPayRequestCardDone(self, page, rparam, datas):
        mo = TyContext.Cls_MsgPack()
        from tysdk.entity.pay.pay import TuyouPay
        if page[0:7] == 'success':
            TuyouPay.makeBuyChargeMessage(mo, datas)
        else:
            mo.setResult('code', 1)
            # mo.setResult('info', 'pay/charge/360/card error')
            mo.setResult('info', '卡号和密码验证失败')
        return mo

    @classmethod
    def __get_order_appId__(self, orderPlatformId):
        baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'PAY_STATE_IDEL')
        baseinfo = json.loads(baseinfo)
        appId = baseinfo['appId']
        if appId != None and appId != '':
            return appId
        else:
            return '0'

    @classmethod
    def do360Callback(self, rpath):
        # args= {'mer_trade_code': ['3ed16f18-aae9-45f9-ae58-2df2a4034fe3'], 'input_cha': ['UTF-8'
        # ], 'bank_pay_flag': ['failed:81007:\xe6\x97\xa0\xe6\x95\x88\xe7\x9a\x84\xe5\x8d\xa1\xe5\x8f\xb7\xe5\xaf\x86\xe7\xa0\x81'], 'mer_code': [
        # '3337100050'], 'gateway_trade_code': ['1AA0000A94CA82013041912123982027'], 'rec_amount': ['10'], 'inner_trade_code': ['08301204191212398
        # 20'], 'sign': ['4c2ea11a263c9ec2ef9f545b85ec4186'], 'sign_type': ['MD5'], 'product_name': ['360Coin']}

        # {'bank_trade_code': ['GWR13041912144816935'], 'input_cha': ['UTF-8'], 'sign_type':
        # ['MD5'], 'bank_pay_flag': ['success'], 'mer_code': ['3337100050'], 'rec_amount': ['10'], 'bank_code': ['DX_CARD'], 'inner_trade_code': ['
        # 0830130419121425414'], 'product_name': ['360Coin'], 'pay_amount': ['20'], 'mer_trade_code': ['3ed16f18-aae9-48f9-ae58-2df2a4034fe3'], 'si
        # gn': ['19b64607388cfe14eee99073ed9d6b44'], 'gateway_trade_code': ['1AA0000FE33C52013041912142541410']}

        orderPlatformId = TyContext.RunHttp.getRequestParam('mer_trade_code')

        rparam = TyContext.RunHttp.convertArgsToDict()
        if not 'sign' in rparam:
            TyContext.ftlog.error('do360Callback error, no sign !!!')
            return 'error'

        sign = rparam['sign']
        del rparam['sign']
        vSign = self.buildMySign(rparam)
        if sign != vSign:
            TyContext.ftlog.error('do360Callback error, sign error !!!')
            return 'error'
        rparam['sign'] = sign

        mer_code = TyContext.RunHttp.getRequestParam('mer_code')
        if mer_code != TuYouPay360.merchant_code:
            TyContext.ftlog.error('do360Callback error, mer_code is not me !!!')
            return 'error'

        from tysdk.entity.pay.pay import TuyouPay
        bank_pay_flag = TyContext.RunHttp.getRequestParam('bank_pay_flag')
        if bank_pay_flag != 'success':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('do360Callback error, charge return error !!!')
            bank_pay_flag = bank_pay_flag.decode('utf-8')
            TuyouPay.deliveryChargeError(orderPlatformId, rparam, bank_pay_flag, 1)

            return 'success'

        trade_status = 'TRADE_FINISHED'
        total_fee = TyContext.RunHttp.getRequestParam('pay_amount')
        if total_fee == None:
            total_fee = TyContext.RunHttp.getRequestParam('rec_amount')

        #         if TuYouPay360.DEBUG360 :
        #             total_fee = float(total_fee)
        #             if total_fee == 0.01 :
        #                 total_fee = 10

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return 'success'
        else:
            return 'error'

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        payCode = '001'
        if prodId == 'T20K':
            payCode = '001'
            # if random.randint(0, 1) == 0 :
            #    payCode = '003'
        if prodId == 'T50K':
            payCode = '002'
            # if random.randint(0, 1) == 0 :
            #    payCode = '004'
        if prodId == 'T100K':
            payCode = '003'
        if prodId == 'RAFFLE' or prodId == 'RAFFLE_NEW' or prodId == 'RAFFLE_10':
            payCode = '004'
        if prodId == 'VOICE100':
            payCode = '005'
        if prodId == 'MOONKEY3':
            payCode = '006'
        if prodId == 'MOONKEY':
            payCode = '007'
        if prodId == 'CARDMATCH10':
            payCode = '008'

        prodName = params['orderName']
        if prodName == u'2元金币':
            payCode = '001'
        if prodName == u'5元金币':
            payCode = '002'
        if prodName == u'10元金币':
            payCode = '003'
        if prodName == u'抽奖':
            payCode = '004'
        if prodName == u'语音小喇叭x100':
            payCode = '005'
        if prodName == u'月光之钥x3':
            payCode = '006'
        if prodName == u'月光之钥':
            payCode = '007'
        if prodName == u'参赛券10张':
            payCode = '008'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def do360CallbackMsg(self, rpath):

        orderPlatformId = TyContext.RunHttp.getRequestParam('platformOrderId', '')

        rparam = TyContext.RunHttp.convertArgsToDict()

        sign = TyContext.RunHttp.getRequestParam('sign', '')
        result = TyContext.RunHttp.getRequestParam('result', '')
        # tSign = 'orderid='+orderPlatformId+'&result='+result+'&key='+TuYouPayLaoHu.sign_skey
        tSign = orderPlatformId + result + TuYouPay360.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign.upper():
            TyContext.ftlog.info('do360CallbackMsg->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '{result:{success:0,orderPlatformId:"' + orderPlatformId + '"}}'

        from tysdk.entity.pay.pay import TuyouPay
        if result != '1':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('do360CallbackMsg error, charge return error !!!')
            TuyouPay.deliveryChargeError(orderPlatformId, rparam, u'短信支付失败', 1)
            return '{result:{success:1,orderPlatformId:"' + orderPlatformId + '"}}'

        trade_status = 'TRADE_FINISHED'
        total_fee = -1
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return '{result:{success:1,orderPlatformId:"' + orderPlatformId + '"}}'
        else:
            return '{result:{success:0,orderPlatformId:"' + orderPlatformId + '"}}'
        pass
