import hashlib
import time
import urllib
from xml.etree import ElementTree

from datetime import date
from datetime import datetime

from tyframework.context import TyContext
from tysdk.entity.huiyuan.alipay_huiyuan import AlipayHuiyuan
from tysdk.entity.pay.rsacrypto import _sign_with_privatekey_pycrypto, \
    _verify_with_publickey_pycrypto
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_filter import payv4_filter
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayAliV4(PayBaseV4):
    PARTNER = "2088901481292394"

    SELLER = "2088901481292394"

    SELLER_ID = SELLER

    RSA_PRIVATE = "MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAOIc0bKk2wj6nA2Fzd59LDfhXJGlurRs+GzYPKtKKjyMLVxq/PDLOahkiYNzaOBeWFa4smtdFZdd39sgHCyqoMkVTSR1KGZHiiPrlUEoIdwYI+iS7vRvwPk4RkN7C/gL1OKZ1P6/EhCb/R5wJ1zfymiRd1iv3ztDL+0dLOlOcbklAgMBAAECgYEAtSPNQkYbSugpmBO3RyQUBng+Blg0aFJb+iaJA9gYWgUaWc1D8Ut9V0+jcnFEdWpfbqnsFWKu52JG8W6Z45aV0sADvoMHe0DzB+OD4nqgObG/lFZif3vSWEyN+UIxmW+Eu+nOyR/PHUD6W0Etg5B47W2rqzpXEzU2zfknwM7uWsECQQDytNtBxeMg2Y5w82WU+GuMtaFNIAe6g+YreEKEn6TmbU266x8HCktXsSP1jKSt4GpvkLDUB5zOa+HZobnuVkmZAkEA7n9J+iP7JcMPU+X8O1nxzsMe103gfzQaGyiIVtPLoHHkZU/2kJ8O3WBAcS4glJ8ZBoqQJs3yel+GNSar2MNbbQJBAKondVgFXhjXrW8ulNb92pjJdY5WmFSAyEtNgoTsT3VkyAv1bslGxE90Vxt9QK7OGJCixfXAaISnSa2EHpAjWnECQGzeNgq1OgO20txdc5I0MKlNcFqf9gaa5f/XtMTN0XngA34rzkWeFc8ADOqdP8oYBfhyb/MGt9UcncrNaEx+gNECQQDXYEhXZEptZMm3nb2tj0u//kOEgfnVqu18/pfFbJOyXjRqoIya46hMvzEcEvq0dND5bdhP8mIud7No5ZelmAPn"

    RSA_ALIPAY_PUBLIC = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCStnZ2gtxZW8GdetfCxwiz7jkdXF9RFaEV7GyUuXEvC9ss5di6SWHkieKccJhBCOULujkADKDXO2uEurjIRIQMufAjaBbNNSIoMa+u72R252BQrocvhILmd2hUur9P+s4dPg3lFqAEPiJtrEJQo/AnxnhFqm7scnl+BuMfYA0nwwIDAQAB"

    ALIPAY_GATEWAY_NEW = "https://mapi.alipay.com/gateway.do"

    NOTIFY_URL = "http://open.touch4.me/v1/pay/alinewpay/callback"

    ALIPAY_APP_ID = '2016012101112179'

    ALIPAY_MD5_KEY = 'p6pyopwqnt3589w9w0ycbcmu1swmuu4u'

    ALIPAY_SIGN_CALLBACK_URL = 'http://125.39.218.101:8002/open/v4/pay/alifree/sign_callback'

    ALIPAY_ORDER_CALLBACK_URL = 'http://125.39.218.101:8002/open/v4/pay/alifree/order_callback'

    paytype_map = {
        'tuyou': '2088901481292394',  # 在线途游
        'shediao': '2088211680098179',  # 北京射雕
        'pingxiang': '2088011439630081',  # 萍乡射雕
        'teyoutu': '2088121857137870',  # 广州特游兔,
        'wannianli': '2088502710358739',  # 万年历
    }

    @payv4_order("tuyou.ali")
    def handle_order_tuyoo(self, mi):
        chargeInfo = self.get_charge_info(mi)
        out_trade_no = chargeInfo['platformOrderId']
        subject = chargeInfo['buttonName']
        total_fee = chargeInfo['chargeTotal']
        packageName = mi.getParamStr('packageName', "")
        appId = chargeInfo['appId']
        alipay_config = self.getPartnerParam(appId=appId, packageName=packageName, chargeType=chargeInfo['chargeType'])
        sParaTemp = {}
        if not alipay_config:
            sParaTemp["partner"] = self.PARTNER
            sParaTemp["seller_id"] = self.SELLER_ID
        else:
            sParaTemp["partner"] = alipay_config['partnerId']
            sParaTemp["seller_id"] = alipay_config['sellerId']
        sParaTemp["out_trade_no"] = out_trade_no
        sParaTemp["subject"] = subject
        sParaTemp["body"] = subject
        sParaTemp["total_fee"] = total_fee
        sParaTemp["notify_url"] = PayHelperV4.getSdkDomain() + "/v1/pay/alinewpay/callback"
        sParaTemp["service"] = "mobile.securitypay.pay"
        sParaTemp["payment_type"] = 1
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["it_b_pay"] = "30m"
        sParaTemp["return_url"] = "m.alipay.com"
        for k, v in sParaTemp.iteritems():
            sParaTemp[k] = '"' + str(v) + '"'
        pairs = filter(lambda x: x[1], sParaTemp.items())
        pairs.sort(lambda x, y: cmp(x[0], y[0]))
        text = '&'.join(['%s=%s' % (k, v) for k, v in pairs])
        otherData = {}
        otherData['sign'] = urllib.quote(self.rsaAliSign(text, alipay_config['partnerId']))
        otherData['sign_type'] = 'RSA'
        otherText = '&'.join(['%s="%s"' % (k, v) for k, v in otherData.iteritems()])
        text = text + '&' + otherText
        payData = {}
        payData['ali_config'] = text
        return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)

    @payv4_order("wannianli.ali")
    def handle_order_wannianli(self, mi):
        return self.handle_order_tuyoo(mi)

    @payv4_order("shediao.ali")
    def handle_order_shedioa(self, mi):
        return self.handle_order_tuyoo(mi)

    @payv4_order("shediao.aliwap")
    def handle_order_aliwap_shediao(self, mi):
        return self.handle_order_alipaywap(mi)

    @payv4_order("wannianli.aliwap")
    def handle_order_aliwap_wannianli(self, mi):
        return self.handle_order_alipaywap(mi)

    @payv4_order("pingxiang.ali")
    def handle_order_app_pingxiang(self, mi):
        return self.handle_order_tuyoo(mi)

    @payv4_order('pingxiang.aliwap')
    def handle_order_alipaywap_pingxiang(self, mi):
        return self.handle_order_alipaywap(mi)

    @payv4_order('teyoutu.ali')
    def handle_order_app_teyoutu(self, mi):
        return self.handle_order_tuyoo(mi)

    @payv4_order('teyoutu.aliwap')
    def handle_order_wap_teyoutu(self, mi):
        return self.handle_order_alipaywap(mi)

    @payv4_order("alipaywap")
    def handle_order_alipaywap(self, mi):
        return super(TuYouPayAliV4, self).handle_order(mi)

    @payv4_callback('/open/ve/pay/alinewpady/callback')
    def handle_tuyoo_callback(self, rpath):
        return self.doAliCallback(rpath)

    @payv4_callback('/open/ve/pay/shediao/alinewpay/callback')
    def handle_shediao_callback(self, rpath):
        return self.doAliCallback(rpath)

    def doAliCallback(self, rpath):
        rparam = PayHelperV4.getArgsDict()
        TyContext.ftlog.info('doAliCallbackNew->args=', rparam)

        sign = rparam['sign']
        notify_data = self.createLinkString(rparam)
        # TyContext.ftlog.info('doAliCallbackNew->notify_data=', notify_data)
        # TyContext.ftlog.info('doAliCallbackNew->sign=', sign)
        # 签名校验
        if not self.rsaVerify(notify_data, **rparam):
            TyContext.ftlog.error('TuyouPayTuyou.doAliCallback rsa verify error !!')
            return 'error'

        trade_status = rparam['trade_status']
        total_fee = rparam['total_fee']
        subject = rparam['subject']
        out_trade_no = rparam['out_trade_no']
        trade_no = rparam['trade_no']

        platformOrderId = out_trade_no
        chargeKey = 'sdk.charge:' + platformOrderId
        oldState, chargeInfo, consumeInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'state', 'charge',
                                                                           'consume')
        chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True) if chargeInfo else {}
        appId = int(chargeInfo.get('appId', 9999))
        chargeType = chargeInfo.get('chargeType', 'tuyou.ali')
        notifys = {'status': trade_status, 'total_fee': total_fee,
                   'subject': subject, 'out_trade_no': out_trade_no,
                   'trade_no': trade_no, 'sign': sign, 'notify_data': notify_data,
                   'chargeType': chargeType, 'third_orderid': trade_no}

        if trade_status == 'TRADE_CLOSED':
            PayHelperV4.callback_error(platformOrderId, 'TRADE_CLOSED', notifys)
            return 'success'
        if trade_status != 'TRADE_SUCCESS' and trade_status != 'TRADE_FINISHED':
            if chargeInfo.get('chargeType') == 'alibig':
                userId = chargeInfo['userId']
                timestamp, count = TyContext.RedisPayData.execute('HMGET', 'alibig:%s' % userId, 'timestamp', 'count')
                now = date.fromtimestamp(int(time.time()))
                if timestamp and now.toordinal() == date.fromtimestamp(int(timestamp)).toordinal():
                    count = int(count) + 1
                else:
                    timestamp = int(time.time())
                    count = 1
                TyContext.RedisPayData.execute('HMSET', 'alibig:%s' % userId,
                                               'timestamp', timestamp,
                                               'count', count)
            return 'success'

        isOK = PayHelperV4.callback_ok(platformOrderId, -1, notifys)
        if isOK:
            return 'success'
        else:
            return 'error'

    @classmethod
    def createLinkString(self, rparam):
        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            # 去掉空值与签名参数后的新签名参数组
            if k != 'sign' and k != 'sign_type' and str(rparam[k]) != '':
                ret = ret + str(k) + '=' + str(rparam[k]) + '&'

        return ret[:-1]

    @payv4_callback('/open/v4/pay/alipayweb')
    def handle_ali_web(self, rpath):
        """
        支付宝PC支付
        :param rpath:
        :return:
        """
        mi = TyContext.RunHttp.convertToMsgPack()
        mi.setParam('chargeType', 'alipay')
        chargeinfo = self.get_charge_info(mi)
        platformOrderId = chargeinfo['platformOrderId']
        txnTime = datetime.now().strftime('%Y%m%d%H%M%S')
        txnAmt = float(chargeinfo['chargeTotal'])
        backUrl = mi.getParamStr('backUrl', '')

        payment_type = "1"
        # //必填，不能修改
        # //服务器异步通知页面路径
        # notify_url = "http://125.39.218.101/v1/pay/alinewpay/callback"
        # //需http://格式的完整路径，不能加?id=123这类自定义参数

        # //页面跳转同步通知页面路径
        return_url = "http://www.tuyoo.com/"
        # //需http://格式的完整路径，不能加?id=123这类自定义参数，不能写成http://localhost/

        # //商户订单号
        out_trade_no = platformOrderId
        # //商户网站订单系统中唯一订单号，必填

        # //订单名称
        subject = chargeinfo['buttonName']
        # //必填

        # //付款金额
        total_fee = txnAmt
        # //必填

        # //商品展示地址
        show_url = 'http://www.tuyoo.com/'
        # //必填，需以http://开头的完整路径，例如：http://www.商户网址.com/myorder.html

        # //订单描述
        body = chargeinfo['buttonName']
        # //选填

        # //超时时间
        it_b_pay = '60m'
        # //选填

        # //钱包token
        extern_token = ''
        # //选填

        # //////////////////////////////////////////////////////////////////////////////////
        # //把请求参数打包成数组
        sParaTemp = {}
        sParaTemp["service"] = "create_direct_pay_by_user"
        appId = chargeinfo.get('appId')
        packageName = chargeinfo.get('packageName')
        partnerParam = self.getPartnerParam(appId=appId, packageName=packageName)
        if not partnerParam:
            sParaTemp["partner"] = self.PARTNER
            sParaTemp["seller_id"] = self.SELLER_ID
        else:
            sParaTemp["partner"] = partnerParam['partnerId']
            sParaTemp["seller_id"] = partnerParam['sellerId']
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["payment_type"] = payment_type
        sParaTemp["notify_url"] = self.NOTIFY_URL
        sParaTemp["return_url"] = return_url
        sParaTemp["out_trade_no"] = out_trade_no
        sParaTemp["subject"] = subject
        sParaTemp["total_fee"] = total_fee
        sParaTemp["show_url"] = show_url
        sParaTemp["body"] = body
        sParaTemp["it_b_pay"] = it_b_pay
        sParaTemp["extern_token"] = extern_token
        sParaTemp['sign'] = self.calcSign(**sParaTemp)
        sParaTemp['sign_type'] = 'RSA'
        return self.buildRequest(sParaTemp, 'get', '确认')

    @payv4_callback('/open/v4/pay/alipaywap')
    def handle_ali_wap(self, rpath):
        """
        支付宝wap支付
        :param rpath:
        :return:
        """
        mi = TyContext.RunHttp.convertToMsgPack()
        # 根据已有订单号查询实际请求的chargeType
        preOrderId = mi.getParamStr('platformOrderId')
        chargeKey = 'sdk.charge:' + preOrderId
        oldState, chargeInfo, consumeInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'state', 'charge',
                                                                           'consume')
        chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True) if chargeInfo else {}
        mi.setParam('chargeType', chargeInfo.get('chargeType', 'alipaywap'))
        chargeinfo = self.get_charge_info(mi)
        platformOrderId = chargeinfo['platformOrderId']
        txnTime = datetime.now().strftime('%Y%m%d%H%M%S')
        txnAmt = float(chargeinfo['chargeTotal'])
        backUrl = mi.getParamStr('backUrl', '')

        payment_type = "1"
        # //必填，不能修改
        # //服务器异步通知页面路径
        # notify_url = "http://125.39.218.101/v1/pay/alinewpay/callback"
        # //需http://格式的完整路径，不能加?id=123这类自定义参数

        # //页面跳转同步通知页面路径
        return_url = "http://www.tuyoo.com/"
        # //需http://格式的完整路径，不能加?id=123这类自定义参数，不能写成http://localhost/

        # //商户订单号
        out_trade_no = platformOrderId
        # //商户网站订单系统中唯一订单号，必填

        # //订单名称
        subject = chargeinfo['buttonName']
        # //必填

        # //付款金额
        total_fee = txnAmt
        # //必填

        # //商品展示地址
        show_url = 'http://www.tuyoo.com/'
        # //必填，需以http://开头的完整路径，例如：http://www.商户网址.com/myorder.html

        # //订单描述
        body = chargeinfo['buttonName']
        # //选填

        # //超时时间
        it_b_pay = '60m'
        # //选填

        # //钱包token
        extern_token = ''
        # //选填

        # //////////////////////////////////////////////////////////////////////////////////
        # //把请求参数打包成数组
        sParaTemp = {}
        appId = chargeinfo.get('appId')
        packageName = chargeinfo.get('packageName')
        partnerParam = self.getPartnerParam(appId=appId, packageName=packageName, chargeType=chargeinfo['chargeType'])
        if not partnerParam:
            sParaTemp["partner"] = self.PARTNER
            sParaTemp["seller_id"] = self.SELLER_ID
        else:
            sParaTemp["partner"] = partnerParam['partnerId']
            sParaTemp["seller_id"] = partnerParam['sellerId']
        sParaTemp["service"] = "alipay.wap.create.direct.pay.by.user"
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["payment_type"] = payment_type
        sParaTemp["notify_url"] = self.NOTIFY_URL
        sParaTemp["return_url"] = return_url
        sParaTemp["out_trade_no"] = out_trade_no
        sParaTemp["subject"] = subject
        sParaTemp["total_fee"] = total_fee
        sParaTemp["show_url"] = show_url
        sParaTemp["body"] = body
        sParaTemp["it_b_pay"] = it_b_pay
        sParaTemp["extern_token"] = extern_token
        sParaTemp['sign'] = self.calcSign(**sParaTemp)
        sParaTemp['sign_type'] = 'RSA'
        TyContext.ftlog.debug('aliwap pay --->', sParaTemp)
        return self.buildRequest(sParaTemp, 'get', '确认')

    @classmethod
    def calcSign(cls, **args):
        # convert dict to list
        pairs = filter(lambda x: x[1], args.items())
        # sort list
        pairs.sort(lambda x, y: cmp(x[0], y[0]))
        text = '&'.join(['%s=%s' % (k, v) for k, v in pairs])
        return cls.rsaAliSign(text, args['partner'])

    @classmethod
    def calcSignMD5(cls, **args):
        pairs = filter(lambda x: x[1], args.items())
        # sort list
        pairs.sort(lambda x, y: cmp(x[0], y[0]))
        text = '&'.join(['%s=%s' % (k, v) for k, v in pairs])
        partnerId = args['partner']
        partnerParam = cls.getPartnerParam(partnerId=partnerId)
        if not partnerParam:
            aliMD5key = cls.ALIPAY_MD5_KEY
        else:
            aliMD5key = partnerParam['alipayMD5']
        return hashlib.md5(text + aliMD5key).hexdigest()

    @classmethod
    def verifySignMD5(cls, sign, rparams):
        pairs = filter(lambda x: x[1] and x[0] != 'sign' and x[0] != 'sign_type', rparams.items())
        pairs.sort(lambda x, y: cmp(x[0], y[0]))
        text = '&'.join(['%s=%s' % (k, v) for k, v in pairs])
        partnerId = rparams.get('partner_id', "")
        sellerId = rparams.get('seller_id', "")
        partnerParam = cls.getPartnerParam(partnerId=partnerId, sellerId=sellerId)
        if not partnerParam:
            aliMD5key = cls.ALIPAY_MD5_KEY
        else:
            aliMD5key = partnerParam['alipayMD5']
        return sign == hashlib.md5(text + aliMD5key).hexdigest()

    @classmethod
    def buildRequest(cls, sParaTemp, strMethod, strButtonName):
        sb = '<form id="alipaysubmit" name="alipaysubmit" enctype="multipart/form-data" action="' + cls.ALIPAY_GATEWAY_NEW + '?_input_charset=' + 'utf-8' + '" method="' + strMethod + '">'
        for name, value in sParaTemp.items():
            sb += '<input type="hidden" name="' + name + '" value="' + str(value) + '"/>'
        sb += '<input type="submit" value="' + strButtonName + '" style="display:none;"></form>'
        sb += "<script>document.forms['alipaysubmit'].submit();</script>"
        return sb

    @classmethod
    def paraFilter(cls, params):
        d = {}
        for k, v in params.items():
            if not v:
                continue
            v = str(v)
            if v.find('"') >= 0:
                v = v.replace('"', '&quot;')
            d[k] = v
        return d

    @payv4_filter("alifree")
    def filter_alipay_free(self, payment, prod_info, **kwargs):
        # 小于50元商品才能使用
        if prod_info['price'] > 50:
            return False

        userId = kwargs['userId']
        # payment['alipay_appid'] = self.ALIPAY_APP_ID
        alipay_sign_flag, alipay_user_id = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%s' % userId,
                                                                       'alipay_sign_flag',
                                                                       'alipay_user_id')
        payment['options'] = {
            'alipay_appid': self.ALIPAY_APP_ID,
            'alipay_sign_flag': alipay_sign_flag if alipay_sign_flag else 0,
            'alipay_user_id': alipay_user_id if alipay_user_id else 0,
        }

        if alipay_user_id:
            payment['isDefault'] = 5
        # if not alipay_user_id:
        #    payment['options']['deeplink'] = self.handle_alifree_sign('/open/v4/pay/alifree/sign')
        # payment['alipay_sign_flag'] = alipay_sign_flag if alipay_sign_flag else 0
        # payment['alipay_user_id'] = alipay_user_id if alipay_user_id else 0
        return True

    @payv4_order("alifree")
    def handle_alipay_free(self, mi):
        chargeInfo = self.get_charge_info(mi)
        userId = chargeInfo['userId']
        alipay_sign_flag, alipay_user_id, alipay_agreement_no = TyContext.RedisUser.execute(userId, 'HMGET',
                                                                                            'user:%s' % userId,
                                                                                            'alipay_sign_flag',
                                                                                            'alipay_user_id',
                                                                                            'alipay_agreement_no')
        sParaTemp = {}
        appId = chargeInfo['appId']
        packageName = mi.getParamStr('tyPackageName', "")
        chargeInfo['packageName'] = packageName
        partnerParam = self.getPartnerParam(appId=appId, packageName=packageName)
        if not partnerParam:
            sParaTemp["partner"] = self.PARTNER
            sParaTemp["seller_id"] = self.SELLER_ID
        else:
            sParaTemp["partner"] = partnerParam['partnerId']
            sParaTemp["seller_id"] = partnerParam['sellerId']
        # 已经签约则直接扣钱
        if alipay_sign_flag:
            sParaTemp["service"] = "alipay.acquire.createandpay"
            sParaTemp["_input_charset"] = 'utf-8'
            sParaTemp["product_code"] = "GENERAL_WITHHOLDING"
            sParaTemp['out_trade_no'] = chargeInfo['platformOrderId']
            sParaTemp['subject'] = chargeInfo['buttonName']
            sParaTemp['total_fee'] = chargeInfo['chargeTotal']
            sParaTemp['it_b_pay'] = '30m'
            ###
            sParaTemp['agreement_info'] = '{"agreement_no":"%s"}' % alipay_agreement_no
            sParaTemp["notify_url"] = self.ALIPAY_ORDER_CALLBACK_URL
            sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
            sParaTemp['sign_type'] = 'MD5'
            response, _ = TyContext.WebPage.webget(self.ALIPAY_GATEWAY_NEW, sParaTemp)
            xmlResponse = ElementTree.fromstring(response)
            if xmlResponse.find('is_success').text == 'T':
                payData = {'status': 'success'}
            else:
                try:
                    AlipayHuiyuan(9999, userId).handle_unsign()
                except:
                    TyContext.ftlog.exception()
                payData = {'status': 'failed'}
            return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)
        # 未签约，通知客户端转跳到createandpay页面执行签约并支付
        else:
            params = TyContext.RunHttp.convertArgsToDict()
            params['platformOrderId'] = chargeInfo['platformOrderId']
            ##
            deeplink = '%s?%s' % (self.ALIPAY_GATEWAY_NEW, urllib.urlencode(self.get_sign_and_pay_params(chargeInfo)))
            payData = {
                'status': 'unsign',
                # 'url':'http://open.touch4.me/open/v4/pay/alifree/createandpay?%s' % urllib.urlencode(params),
                'deeplink': 'alipays://platformapi/startapp?appId=20000067&url=%s' % (urllib.quote_plus(deeplink),)
            }
            return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)

    def get_sign_and_pay_params(self, chargeInfo):
        sParaTemp = {}
        sParaTemp["service"] = "alipay.acquire.page.createandpay"
        appId = chargeInfo['appId']
        packageName = chargeInfo.get('packageName')
        partnerParam = self.getPartnerParam(appId=appId, packageName=packageName)
        if not partnerParam:
            sParaTemp["partner"] = self.PARTNER
        else:
            sParaTemp["partner"] = partnerParam['partnerId']
        # sParaTemp["seller_id"] =  self.SELLER_ID
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp['out_trade_no'] = chargeInfo['platformOrderId']
        sParaTemp['subject'] = chargeInfo['buttonName']
        sParaTemp['product_code'] = 'GENERAL_WITHHOLDING'
        sParaTemp['integration_type'] = 'ALIAPP'
        sParaTemp[
            'agreement_sign_parameters'] = '{"productCode":"GENERAL_WITHHOLDING_P","signValidityPeriod":"12m","externalUserId":"%s", "notifyUrl":"%s"}' % (
            chargeInfo['userId'],
            self.ALIPAY_SIGN_CALLBACK_URL)
        sParaTemp['total_fee'] = chargeInfo['chargeTotal']
        ### 签约参数
        ###
        sParaTemp["return_url"] = "tuyooalifree://signandpay"
        sParaTemp["request_from_url"] = "tuyooalifree://signandpay"
        sParaTemp["notify_url"] = self.ALIPAY_ORDER_CALLBACK_URL
        sParaTemp['external_user_id'] = chargeInfo['userId']
        sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
        sParaTemp['sign_type'] = 'MD5'
        return sParaTemp

    @payv4_callback('/open/v4/pay/alifree/createandpay')
    def handle_sign_and_pay(self, rpath):
        mi = TyContext.RunHttp.convertToMsgPack()
        mi.setParam('chargeType', 'alipay')
        chargeInfo = self.get_charge_info(mi)
        sParaTemp = self.get_sign_and_pay_params(chargeInfo)
        return self.buildRequest(self.paraFilter(sParaTemp), "get", "确定")

    # 只有sellerId
    @payv4_callback('/open/v4/pay/alifree/order_callback')
    def handle_alifree_order_callback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        sign = rparams['sign']
        # 签名校验
        if not self.verifySignMD5(sign, rparams):
            TyContext.ftlog.error('TuyouPayTuyou.doAliCallback md5 verify error !!')
            return 'error'
        trade_status = rparams['trade_status']
        if trade_status != 'TRADE_SUCCESS' and trade_status != 'TRADE_FINISHED':
            return 'success'
        buyer_id = rparams.get('buyer_id')
        platformOrderId = rparams['out_trade_no']
        chargeInfo = None
        if buyer_id:
            chargeKey = 'sdk.charge:' + platformOrderId
            chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
            if chargeInfo:
                chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
                userId = int(chargeInfo['userId'])
                TyContext.RedisUser.execute(userId, 'HMSET', 'user:%s' % userId,
                                            'alipay_sign_flag', 1,
                                            'alipay_user_id', buyer_id)
        try:
            AlipayHuiyuan(9999, userId).handle_order(chargeInfo)
        except:
            TyContext.ftlog.exception()
        isOK = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOK:
            return 'success'
        else:
            return 'error'

    @payv4_callback('/open/v4/pay/alifree/sign')
    def handle_alifree_sign(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        userId = rparams['userId']
        channel = rparams.get('channel', 'WAP')
        ###
        sParaTemp = {}
        appId = rparams.get('appId', "")
        packageName = rparams.get('packageName')
        partnerParam = self.getPartnerParam(appId=appId, packageName=packageName)
        if not partnerParam:
            sParaTemp["partner"] = self.PARTNER
        else:
            sParaTemp["partner"] = partnerParam['partnerId']
        sParaTemp["service"] = "alipay.dut.customer.agreement.page.sign"
        # sParaTemp["seller_id"] =  self.SELLER_ID
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["product_code"] = "GENERAL_WITHHOLDING_P"
        sParaTemp["access_info"] = '{"channel":"%s"}' % channel
        ###
        sParaTemp["return_url"] = "http://www.tuyoo.com/"
        sParaTemp["notify_url"] = self.ALIPAY_SIGN_CALLBACK_URL
        sParaTemp['external_user_id'] = userId
        sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
        sParaTemp['sign_type'] = 'MD5'
        url = '%s?%s' % (self.ALIPAY_GATEWAY_NEW, urllib.urlencode(sParaTemp))
        # return url
        return 'alipays://platformapi/startapp?appId=20000067&url=%s' % (urllib.quote_plus(url),)
        # return self.buildRequest(self.paraFilter(sParaTemp), "get", '确定')

    @payv4_callback('/open/v4/pay/alifree/sign/modify')
    def handle_alifree_modify_sign(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        userId = rparams['userId']
        channel = rparams.get('channel', 'WAP')
        ###
        sParaTemp = {}
        appId = rparams.get('appId', "")
        packageName = rparams.get('packageName')
        partnerParam = self.getPartnerParam(appId=appId, packageName=packageName)
        if not partnerParam:
            sParaTemp["partner"] = self.PARTNER
            sParaTemp["seller_id"] = self.SELLER_ID
        else:
            sParaTemp["partner"] = partnerParam['partnerId']
            sParaTemp["seller_id"] = partnerParam['sellerId']
        sParaTemp["service"] = "alipay.dut.customer.agreement.page.sign.modify"
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["product_code"] = "GENERAL_WITHHOLDING_P"
        sParaTemp["access_info"] = '{"channel":"%s"}' % channel
        ###
        sParaTemp["return_url"] = "http://www.tuyoo.com/"
        # sParaTemp["notify_url"] = 'http://open.touch4.me/open/v4/pay/alifree/sign_callback'
        sParaTemp['external_user_id'] = userId
        sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
        sParaTemp['sign_type'] = 'MD5'
        url = '%s?%s' % (self.ALIPAY_GATEWAY_NEW, urllib.urlencode(sParaTemp))
        # return url
        # return 'alipays://platformapi/startapp?appId=%s&url=%s' % (self.ALIPAY_APP_ID, urllib.quote_plus(url))
        return self.buildRequest(self.paraFilter(sParaTemp), "get", '确定')

    @payv4_callback('/open/v4/pay/alifree/sign/query')
    def handle_alifree_query_sign(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        # userId = rparams['userId']
        channel = rparams.get('channel', 'WAP')
        alipay_logon_id = rparams['alipay_logon_id']
        ###
        sParaTemp = {}
        appId = rparams.get('appId', "")
        packageName = rparams.get('packageName')
        partnerParam = self.getPartnerParam(appId=appId, packageName=packageName)
        if not partnerParam:
            sParaTemp["partner"] = self.PARTNER
        else:
            sParaTemp["partner"] = partnerParam['partnerId']
        sParaTemp["service"] = "alipay.dut.customer.agreement.query"
        # sParaTemp["seller_id"] =  self.SELLER_ID
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["product_code"] = "GENERAL_WITHHOLDING_P"
        # sParaTemp["access_info"] = '{"channel":"%s"}' % channel
        ###
        # sParaTemp["return_url"] = "http://www.tuyoo.com/"
        # sParaTemp["notify_url"] = 'http://open.touch4.me/open/v4/pay/alifree/sign_callback'
        # sParaTemp['external_user_id'] = userId
        sParaTemp['alipay_logon_id'] = alipay_logon_id
        sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
        sParaTemp['sign_type'] = 'MD5'
        response, _ = TyContext.WebPage.webget(self.ALIPAY_GATEWAY_NEW, sParaTemp)
        return response
        #

    @payv4_callback('/open/v4/pay/alifree/unsign')
    def handle_alifree_unsign(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        userId = rparams['userId']
        TyContext.ftlog.info('TuYouPayAliV4.handle_alifree_unsign', userId)
        alipay_logon_id = rparams.get('alipay_logon_id')
        alipay_sign_flag, alipay_user_id = TyContext.RedisUser.execute(int(userId), 'HMGET', 'user:%s' % userId,
                                                                       'alipay_sign_flag',
                                                                       'alipay_user_id')
        if not alipay_logon_id and not alipay_user_id:
            return '{"code":-1, "info":"no user info"}'
        sParaTemp = {}

        sParaTemp["service"] = "alipay.dut.customer.agreement.unsign"

        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["product_code"] = "GENERAL_WITHHOLDING_P"
        if alipay_logon_id:
            sParaTemp['alipay_logon_id'] = alipay_logon_id
            sParaTemp['app_id'] = self.ALIPAY_APP_ID
        else:
            sParaTemp["alipay_user_id"] = alipay_user_id
            sParaTemp['app_id'] = self.ALIPAY_APP_ID
        appId = rparams.get('appId', "")
        packageName = rparams.get('packageName')
        partnerParam = self.getPartnerParam(appId=appId, packageName=packageName)
        if not partnerParam:
            sParaTemp["partner"] = self.PARTNER
            sParaTemp["seller_id"] = self.SELLER_ID
            sParaTemp['app_id'] = self.ALIPAY_APP_ID
        else:
            sParaTemp["partner"] = partnerParam['partnerId']
            sParaTemp["seller_id"] = partnerParam['sellerId']
            sParaTemp['app_id'] = partnerParam['alipayAppId']
        sParaTemp['external_user_id'] = userId
        # 上线修改正式服
        sParaTemp["return_url"] = "http://www.tuyoo.com/"
        # sParaTemp["notify_url"] =  'http://open.touch4.me/open/v4/pay/alifree/sign_callback'
        sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
        sParaTemp['sign_type'] = 'MD5'
        response, _ = TyContext.WebPage.webget(self.ALIPAY_GATEWAY_NEW, sParaTemp)
        xmlResponse = ElementTree.fromstring(response)
        TyContext.ftlog.info('TuYouPayAliV4.handle_alifree_unsign response', response)
        if True or xmlResponse.find('is_success').text == 'T':
            TyContext.RedisUser.execute(int(userId), 'HDEL', 'user:%s' % userId,
                                        'alipay_sign_flag',
                                        'alipay_invalid_time',
                                        'alipay_user_id')
        return '{"code":0, "info":"success"}'

    @payv4_callback('/open/v4/pay/alifree/sign_callback')
    def handle_alifree_sign_callback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        status = rparams['status']
        sign = rparams['sign']
        # 签名校验
        if not self.verifySignMD5(sign, rparams):
            TyContext.ftlog.error('TuyouPayTuyou.doAliCallback md5 verify error !!')
            return 'error'
        userId = int(rparams['external_user_id'])
        if status == 'NORMAL':
            alipay_user_id = rparams['alipay_user_id']
            agreement_no = rparams['agreement_no']
            TyContext.RedisUser.execute(userId, 'HMSET', 'user:%s' % userId,
                                        'alipay_sign_flag', 1,
                                        'alipay_agreement_no', agreement_no,
                                        'alipay_invalid_time', rparams['invalid_time'],
                                        'alipay_user_id', alipay_user_id)

            ####
            TyContext.RedisUserKeys.execute('HMSET', 'alipay_agreement_no:%s' % agreement_no,
                                            'alipay_user_id', alipay_user_id,
                                            'external_user_id', userId,
                                            'alipay_invalid_time', rparams['invalid_time'], )

            AlipayHuiyuan(9999, userId).handle_sign()
        return 'success'

    @classmethod
    def rsaVerify(cls, data, **kwargs):
        sign = kwargs['sign']
        partnerId = kwargs.get('partner_id', "")
        sellerId = kwargs.get('seller_id', "")
        partnerParam = cls.getPartnerParam(partnerId=partnerId, sellerId=sellerId)
        from Crypto.PublicKey import RSA
        public_key = RSA.importKey(partnerParam['rsaPubKey'])
        return _verify_with_publickey_pycrypto(data, sign, public_key)

    @classmethod
    def getPartnerParam(cls, **kwargs):
        '''
        获取 一组partner 参数
        :param kwargs:
        :return:
        '''
        alipay_config = TyContext.Configure.get_global_item_json('alipay_config', {})
        partnerId = kwargs.get('partnerId', "")
        if not partnerId:
            for k, v in kwargs.iteritems():
                partnerId = alipay_config['partnerId'].get(str(v), "")
                if partnerId:
                    break
        # 继续如果,没有找到对应的配置，按照支付方式索引对应的商户号
        if not partnerId:
            chargeType = kwargs.get('chargeType', 'tuyou')
            map_key = chargeType.split('.')[0]
            partnerId = cls.paytype_map.get(map_key)
        if not partnerId:
            partnerId = cls.PARTNER
        partnerParam = alipay_config['partnerParam'].get(partnerId, None)
        if partnerParam:
            return partnerParam
        sellerId = kwargs.get("sellerId", "")
        if sellerId:
            for k, v in alipay_config['partnerParam'].iteritems():
                if v['sellerId'] == sellerId:
                    return v
        TyContext.ftlog.debug("TuYouPayUnionPayV4 unionpay_config not exist ,appId")
        return None

    @classmethod
    def rsaAliSign(cls, data, parterId):
        partnerParam = cls.getPartnerParam(partnerId=parterId)
        privateKey = partnerParam['rsaPrivateKey']
        from Crypto.PublicKey import RSA
        priv_key = RSA.importKey(privateKey)
        return _sign_with_privatekey_pycrypto(data, priv_key)
