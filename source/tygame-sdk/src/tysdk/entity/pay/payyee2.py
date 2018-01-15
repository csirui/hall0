# -*- coding=utf-8 -*-

import time
import urllib

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


# 易宝银联卡支付
class TuYouPayYee2():
    requestSqh = 0
    from tysdk import is_test_sdk_server
    if is_test_sdk_server():
        CALLBACK_TAG = 10
        YEE_ACCOUNT = 'YB01000000144'
        YEE_URL_CARD_0 = 'http://mobiletest.yeepay.com/paymobile/mobile/pay/request'
        YEE_URL_CARD_1 = 'http://mobiletest.yeepay.com/paymobile/mobile/pay/bankcard/debit/request '
        YEE_URL_CARD_2 = 'http://mobiletest.yeepay.com/paymobile/mobile/pay/bankcard/credit/request'
    else:
        CALLBACK_TAG = 20
        YEE_ACCOUNT = 'YB01000000275'
        YEE_URL_CARD_0 = 'https://ok.yeepay.com/paymobile/mobile/pay/request'
        YEE_URL_CARD_1 = 'https://ok.yeepay.com/paymobile/mobile/pay/bankcard/debit/request'
        YEE_URL_CARD_2 = 'https://ok.yeepay.com/paymobile/mobile/pay/bankcard/credit/request'

    @classmethod
    def __make_request_url__(self, cardType, mesdata):
        from rsacrypto_yee2 import get_yee_verify
        yee = get_yee_verify(self.YEE_ACCOUNT)
        values = yee.requestprocess(mesdata)
        if cardType == 1:
            yurl = self.YEE_URL_CARD_1
        elif cardType == 2:
            yurl = self.YEE_URL_CARD_2
        else:
            yurl = self.YEE_URL_CARD_0
        yeeurl = yurl + "?" + urllib.urlencode(values)
        return yeeurl

    @classmethod
    def __verify_callback__(self, yee_channel='tuyoo'):
        try:
            from rsacrypto_yee2 import get_yee_verify
            yee_config = TyContext.Configure.get_global_item_json('yee2_config', {})
            yee_account = yee_config.get(yee_channel)[0]
            self.YEE_ACCOUNT = yee_account
            yee = get_yee_verify(self.YEE_ACCOUNT)
            encryptkey = TyContext.RunHttp.getRequestParam('encryptkey', '')
            data = TyContext.RunHttp.getRequestParam('data', '')
            postData = {'encryptkey': encryptkey, 'data': data}
            TyContext.ftlog.debug('__verify_callback__->', postData)
            rdata = yee.result_decrypt(postData)
            TyContext.ftlog.debug('__verify_callback__->', rdata)
            if rdata:
                if yee.checksign(rdata) == True:
                    return rdata
            TyContext.ftlog.debug('__verify_callback__->checksign false !!', rdata)
        except:
            TyContext.ftlog.exception()
        return None

    @classmethod
    def doPayRequestCard1(self, params):
        mo = TyContext.Cls_MsgPack()
        self.doBuyStraight(params['userId'], params, mo, 1)
        return mo

    @classmethod
    def doPayRequestCard2(self, params):
        mo = TyContext.Cls_MsgPack()
        self.doBuyStraight(params['userId'], params, mo, 2)
        return mo

    @classmethod
    def doBuyStraight(self, userId, params, mo, cardType=0):
        from tysdk import is_test_sdk_server
        if not is_test_sdk_server():
            yee_config = TyContext.Configure.get_global_item_json('yee2_config', {})
            yee_channel = params['yeeChannel']
            yee_account = yee_config.get(str(yee_channel))[0]
            yee_calltag = yee_config.get(str(yee_channel))[1]
            if yee_channel == 'shediao':
                cardType = 3
            if yee_account:
                self.YEE_ACCOUNT = yee_account
                self.CALLBACK_TAG = yee_calltag
            else:
                raise Exception('can not find yee2 account info define of yee_channel=' + str(yee_channel))
        from tysdk.entity.user_common.verify import AccountVerify

        self.requestSqh += 1
        error = ''
        orderPrice = int(params['orderPrice']) * 100
        platformOrderId = params['orderPlatformId'] + '-' + str(self.requestSqh)
        imei = TyContext.RunHttp.getRequestParam('imei', '').strip()
        if len(imei) > 0:
            imei = 'IMEI:' + AccountVerify.decode_item(imei)

        mac = TyContext.RunHttp.getRequestParam('mac', '')
        if len(mac) > 0:
            mac = 'MAC:' + AccountVerify.decode_item(mac)

        if len(imei) > 0:
            other = imei
        elif len(mac) > 0:
            other = mac
        else:
            error = 'params of MAC or IMEI is missing'

        userip = TyContext.RunHttp.getRequestParam('ip', '').strip()
        if len(userip) == 0:
            error = 'params of IP Address is missing'

        userua = TyContext.RunHttp.getRequestParam('user_agent', '').strip()
        if len(userua) == 0:
            error = 'params of User Agent is missing'
        userua = AccountVerify.decode_item(userua)
        if len(userua) == 0:
            error = 'params of User Agent decode error '

        if len(error) > 0:
            mo.setError('code', 1)
            mo.setError('info', error)
            return
        domain = PayHelper.getSdkDomain()
        pname = u'途游-' + unicode(params['orderName'])
        mesdata = {
            'merchantaccount': self.YEE_ACCOUNT,  # 商户账户编号  √  string
            'orderid': platformOrderId,  # 客户订单号  √  string  商户生成的唯一订单号，最长50位
            'transtime': int(time.time()),  # 交易时间  √  int  时间戳，例如:1361324896，精确到秒
            'currency': 156,  # 交易币种   int  默认156人民币(当前仅支持人民币)
            'amount': orderPrice,  # 交易金额  √  int  以"分"为单位的整型，必须大于零
            'productcatalog': '1',  # 商品类别码  √  string  详见商品类别码表   1  虚拟产品
            'productname': pname,  # 商品名称  √  string  最长50位，出于风控考虑，请按下面的格式传递值:应用-商品名称
            'productdesc': '',
            'identityid': str(userId),  # 用户标识  √  string  最长50位，商户生成的用户账号唯一标识
            'identitytype': 2,  # 用户标识类型  √  int 2  用户ID  用户编号
            'other': other,  # 终端硬件标识  √  string  最长50位，手机传IMEI（格式为IMEI:447769804451095），
            'userip': userip,  # 用户IP  √  string  用户支付时使用的网络终端IP
            'userua': userua,  # 终端UA  √  string  用户使用的移动终端的UA信息
            'callbackurl': domain + '/v1/pay/yee2/callback' + str(self.CALLBACK_TAG),
            'fcallbackurl': domain + '/v1/pay/yee2/callback' + str(self.CALLBACK_TAG + 1),
        }
        TyContext.ftlog.debug('TuYouPayYee2.doBuyStraight ', imei, mac, 'mesdata=', mesdata)
        yeeurl = self.__make_request_url__(cardType, mesdata)
        payData = {'openurl': yeeurl}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doTuYouCallback(cls, rpath):
        datas = cls.__verify_callback__('tuyoo')
        return cls.__do_deliver__goods(datas)

    @classmethod
    def doSheDiaoCallback(cls, rpath):
        datas = cls.__verify_callback__('shediao')
        return cls.__do_deliver__goods(datas)

    @classmethod
    def doTestCallback(cls, rpath):
        datas = cls.__verify_callback__('test')
        return cls.__do_deliver__goods(datas)

    @classmethod
    def __do_deliver__goods(cls, datas):
        if datas:
            if 'sign' in datas:
                del datas['sign']
            result = datas.get('status', 0)
            orderPlatformId = datas.get('orderid', '')
            if orderPlatformId.find('-') > 0:
                orderPlatformId = orderPlatformId.split('-')[0]
            datas['third_orderid'] = datas['yborderid']
            from tysdk.entity.pay.pay import TuyouPay
            if result != 1:
                # 长连接通知，客户端支付失败
                TyContext.ftlog.error('doYdMmCallbackMsg error, charge return error !!!')
                TuyouPay.deliveryChargeError(orderPlatformId, datas, u'支付失败', 1)
                return '{"errorcode ":0, "status":0, "callback":1}'

            total_fee = int(float(datas.get('amount', -1)))
            if total_fee > 0:
                total_fee = total_fee / 100
            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, 'TRADE_FINISHED', datas)
            if isOk:
                return '{"errorcode ":0, "status":1, "callback":1}'
            else:
                return '{"errorcode ":200000, "status":1, "callback":1}'
        else:
            return '{"errorcode ":200024, "callback":1}'

    @classmethod
    def doCallback2(cls, rpath):
        return TyContext.CloseWebView.getCloseHtml()
