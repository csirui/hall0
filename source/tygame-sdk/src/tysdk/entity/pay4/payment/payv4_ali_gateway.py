import hashlib
import json
import urllib
from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import _sign_with_privatekey_pycrypto, \
    _verify_with_publickey_pycrypto
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.payment.payv4_gateway import PayGatewayV4
from tysdk.entity.pay_common.orderlog import Order
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayAliV4Gateway(PayGatewayV4):
    PARTNER = "2088901481292394"

    SELLER = "2088901481292394"

    SELLER_ID = SELLER

    RSA_PRIVATE = "MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAOIc0bKk2wj6nA2Fzd59LDfhXJGlurRs+GzYPKtKKjyMLVxq/PDLOahkiYNzaOBeWFa4smtdFZdd39sgHCyqoMkVTSR1KGZHiiPrlUEoIdwYI+iS7vRvwPk4RkN7C/gL1OKZ1P6/EhCb/R5wJ1zfymiRd1iv3ztDL+0dLOlOcbklAgMBAAECgYEAtSPNQkYbSugpmBO3RyQUBng+Blg0aFJb+iaJA9gYWgUaWc1D8Ut9V0+jcnFEdWpfbqnsFWKu52JG8W6Z45aV0sADvoMHe0DzB+OD4nqgObG/lFZif3vSWEyN+UIxmW+Eu+nOyR/PHUD6W0Etg5B47W2rqzpXEzU2zfknwM7uWsECQQDytNtBxeMg2Y5w82WU+GuMtaFNIAe6g+YreEKEn6TmbU266x8HCktXsSP1jKSt4GpvkLDUB5zOa+HZobnuVkmZAkEA7n9J+iP7JcMPU+X8O1nxzsMe103gfzQaGyiIVtPLoHHkZU/2kJ8O3WBAcS4glJ8ZBoqQJs3yel+GNSar2MNbbQJBAKondVgFXhjXrW8ulNb92pjJdY5WmFSAyEtNgoTsT3VkyAv1bslGxE90Vxt9QK7OGJCixfXAaISnSa2EHpAjWnECQGzeNgq1OgO20txdc5I0MKlNcFqf9gaa5f/XtMTN0XngA34rzkWeFc8ADOqdP8oYBfhyb/MGt9UcncrNaEx+gNECQQDXYEhXZEptZMm3nb2tj0u//kOEgfnVqu18/pfFbJOyXjRqoIya46hMvzEcEvq0dND5bdhP8mIud7No5ZelmAPn"

    RSA_ALIPAY_PUBLIC = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCStnZ2gtxZW8GdetfCxwiz7jkdXF9RFaEV7GyUuXEvC9ss5di6SWHkieKccJhBCOULujkADKDXO2uEurjIRIQMufAjaBbNNSIoMa+u72R252BQrocvhILmd2hUur9P+s4dPg3lFqAEPiJtrEJQo/AnxnhFqm7scnl+BuMfYA0nwwIDAQAB"

    ALIPAY_GATEWAY_NEW = "https://mapi.alipay.com/gateway.do"

    ALIPAY_APP_ID = '2016012101112179'

    ALIPAY_MD5_KEY = 'p6pyopwqnt3589w9w0ycbcmu1swmuu4u'

    # ALIPAY_SIGN_CALLBACK_URL = 'http://open.touch4.me/open/gateway/alifree/sign_callback'

    # ALIPAY_ORDER_CALLBACK_URL = 'http://open.touch4.me/open/gateway/alifree/order_callback'


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

    @payv4_callback("/open/gateway/alifree/signandpay")
    def handle_alipay_free_signandpay(self, rpath):
        """
        调用签约并支付接口，需要传入的参数: appId, orderId, prodName, prodPrice, userId, returnUrl, notifyUrl
        :param rpath:
        :return:
        """
        rparams = TyContext.RunHttp.convertArgsToDict()
        requiredParams = ['appId', 'userId', 'prodName', 'prodPrice', 'orderId', 'notifyUrl', 'returnUrl']
        for name in requiredParams:
            if not name in rparams:
                return '{"code":3, "msg":"缺少参数%s"}' % name
        if not self.checkGatewaySign(rparams):
            return '{"code":1, "msg":"signature error"}'
        sParaTemp = {}
        sParaTemp["partner"] = self.PARTNER
        sParaTemp["seller_id"] = self.SELLER_ID
        #  已经签约则直接扣钱
        chargeInfo = {
            'appId': rparams['appId'],
            'buttonName': rparams['prodName'],
            'chargeTotal': rparams['prodPrice'],
            'platformOrderId': rparams['orderId'],
            'return_url': rparams['returnUrl'],
            'userId': rparams['userId'],
        }
        ##
        deeplink = '%s?%s' % (self.ALIPAY_GATEWAY_NEW, urllib.urlencode(self.get_sign_and_pay_params(chargeInfo)))
        payData = {
            'deeplink': 'alipays://platformapi/startapp?appId=20000067&url=%s' % (urllib.quote_plus(deeplink),)
        }
        chargeData = {
            'code': 0,
            'appId': rparams['appId'],
            'prodName': rparams['prodName'],
            'prodPrice': rparams['prodPrice'],
            'userId': rparams['userId'],
            'orderId': rparams['orderId'],
            'notifyUrl': rparams['notifyUrl'],
            'payData': payData,
        }
        chargeKey = 'sdk.charge.gateway:' + chargeData['orderId']
        TyContext.RedisPayData.execute('SET', chargeKey, json.dumps(chargeData))
        TyContext.RedisPayData.execute('EXPIRE', chargeKey, 86400 * 7)
        return json.dumps(chargeData)

    @payv4_callback("/open/gateway/alifree/pay")
    def handle_alipay_free_pay(self, rpath):
        """
        支付宝免密直接扣款,需要传入的参数有：appId, sign, orderId, prodName, prodPrice, userId
        :param rpath:
        :return:
        """
        rparams = TyContext.RunHttp.convertArgsToDict()
        requiredParams = ['appId', 'userId', 'prodName', 'prodPrice', 'orderId', 'notifyUrl']
        for name in requiredParams:
            if not name in rparams:
                return '{"code":3, "msg":"缺少参数%s"}' % name
        if not self.checkGatewaySign(rparams):
            return '{"code":1, "msg":"signature error"}'
        appId = rparams['appId']
        userId = rparams['userId']
        hashUserId = '%s@%s' % (userId, appId)
        alipay_agreement_no = TyContext.RedisUser.execute(abs(hash(hashUserId)), 'HGET',
                                                          'universal_user:%s' % hashUserId,
                                                          'alipay_agreement_no')
        if not alipay_agreement_no:
            return '{"code":2, "msg":"还未签署免密协议"}'
        sParaTemp = {}
        sParaTemp["partner"] = self.PARTNER
        sParaTemp["seller_id"] = self.SELLER_ID
        sParaTemp["service"] = "alipay.acquire.createandpay"
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["product_code"] = "GENERAL_WITHHOLDING"
        sParaTemp['out_trade_no'] = rparams['orderId']
        sParaTemp['subject'] = rparams['prodName']
        sParaTemp['total_fee'] = rparams['prodPrice']
        sParaTemp['it_b_pay'] = '30m'
        ###
        sParaTemp['agreement_info'] = '{"agreement_no":"%s"}' % alipay_agreement_no
        sParaTemp["notify_url"] = PayHelper.getSdkDomain() + '/open/gateway/alifree/order_callback'
        sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
        sParaTemp['sign_type'] = 'MD5'
        # save order
        chargeData = {
            'code': 0,
            'appId': rparams['appId'],
            'prodName': rparams['prodName'],
            'prodPrice': rparams['prodPrice'],
            'userId': rparams['userId'],
            'orderId': rparams['orderId'],
            'notifyUrl': rparams['notifyUrl'],
        }
        TyContext.RedisPayData.execute('SET', 'sdk.charge.gateway:' + chargeData['orderId'], json.dumps(chargeData))
        # trade_no = xmlResponse.find('response').find('alipay').find('trade_no').text
        response, _ = TyContext.WebPage.webget(self.ALIPAY_GATEWAY_NEW, sParaTemp)
        xmlResponse = ElementTree.fromstring(response)
        if xmlResponse.find('is_success').text == 'T':
            status = 'success'
        else:
            status = 'failed'
        return json.dumps({'code': 0,
                           'status': status,
                           'prodName': rparams['prodName'],
                           'prodPrice': rparams['prodPrice'],
                           'orderId': rparams['orderId'],
                           # 'trade_no': trade_no,
                           })

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
        external_user_id = '%s@%s' % (chargeInfo['userId'], chargeInfo['appId'])
        # sParaTemp["seller_id"] =  self.SELLER_ID
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp['out_trade_no'] = chargeInfo['platformOrderId']
        sParaTemp['subject'] = chargeInfo['buttonName']
        sParaTemp['product_code'] = 'GENERAL_WITHHOLDING'
        sParaTemp['integration_type'] = 'ALIAPP'
        sParaTemp[
            'agreement_sign_parameters'] = '{"productCode":"GENERAL_WITHHOLDING_P","signValidityPeriod":"12m","externalUserId":"%s", "notifyUrl":"%s"}' % (
            external_user_id,
            PayHelper.getSdkDomain() + '/open/gateway/alifree/sign_callback')
        sParaTemp['total_fee'] = chargeInfo['chargeTotal']
        ### 签约参数
        ###
        sParaTemp["return_url"] = chargeInfo['return_url']
        sParaTemp["request_from_url"] = chargeInfo['return_url']
        sParaTemp["notify_url"] = PayHelper.getSdkDomain() + '/open/gateway/alifree/order_callback'
        sParaTemp['external_user_id'] = external_user_id
        sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
        sParaTemp['sign_type'] = 'MD5'
        return sParaTemp

    # 只有sellerId
    @payv4_callback('/open/gateway/alifree/order_callback')
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
        ###
        buyer_id = rparams.get('buyer_id')
        platformOrderId = rparams['out_trade_no']
        chargeKey = 'sdk.charge.gateway:' + platformOrderId
        chargeData = TyContext.RedisPayData.execute('GET', chargeKey)
        chargeData = json.loads(chargeData)
        appId = chargeData['appId']
        userId = chargeData['userId']
        params = {
            'appId': appId,
            'userId': userId,
            'prodName': chargeData['prodName'],
            'prodPrice': chargeData['prodPrice'],
            'orderId': chargeData['orderId'],
            'total_fee': rparams['total_fee'],
            'trade_no': rparams['trade_no'],
            'status': 'success',
        }
        # 检查用户有没有完成绑定
        if buyer_id:
            alipay_agreement_no, alipay_invalid_time, alipay_user_id = TyContext.RedisUser.execute(
                abs(hash(buyer_id)), 'HMGET', 'universal_user:%s@alipay' % buyer_id,
                'alipay_agreement_no',
                'alipay_invalid_time',
                'alipay_user_id')
            if alipay_agreement_no:
                external_user_id = '%s@%s' % (userId, appId)
                TyContext.RedisUser.execute(abs(hash(external_user_id)), 'HMSET',
                                            'universal_user:%s' % external_user_id,
                                            'alipay_agreement_no', alipay_agreement_no,
                                            'alipay_invalid_time', alipay_invalid_time,
                                            'alipay_user_id', alipay_user_id)

        params['sign'] = self.calcGatewaySign(params)
        try:
            result = TyContext.WebPage.webget(chargeData['notifyUrl'], params, method_='GET')
        except:
            TyContext.ftlog.exception()
        # report bi data
        try:
            TyContext.BiReport.report_bi_sdk_buy(Order.CALLBACK_OK,
                                                 0,  # userId
                                                 appId,  # appId
                                                 '',  # clientId,
                                                 platformOrderId,  # orderId
                                                 charge_price=chargeData['prodPrice'],
                                                 succ_price=chargeData['prodPrice'],
                                                 paytype=116)  # alipay
        except:
            TyContext.ftlog.exception()

        if True or result == 'success' or result == 'ok':
            return 'success'
        else:
            return 'error'

    @payv4_callback('/open/gateway/alifree/unsign')
    def handle_alifree_unsign(self, rpath):
        """
        解约接口，需要传入的参数：
            appId
            userId
            returnUrl
        :param rpath:
        :return:
        """
        rparams = TyContext.RunHttp.convertArgsToDict()
        requiredParams = ['appId', 'userId', 'returnUrl']
        for name in requiredParams:
            if not name in rparams:
                return '{"code":3, "msg":"缺少参数%s"}' % name
        TyContext.ftlog.info('TuYouPayAliGatewayV4.unsign rparams=', rparams)
        if not self.checkGatewaySign(rparams):
            return '{"code":1, "msg":"signature error"}'
        appId = rparams['appId']
        userId = rparams['userId']
        hashUserId = '%s@%s' % (userId, appId)
        alipay_agreement_no, alipay_user_id = TyContext.RedisUser.execute(abs(hash(hashUserId)), 'HMGET',
                                                                          'universal_user:%s' % hashUserId,
                                                                          'alipay_agreement_no',
                                                                          'alipay_user_id')
        if not alipay_agreement_no or not alipay_user_id:
            return '{"code":2, "msg":"还未签署免密协议"}'
        sParaTemp = {}
        sParaTemp["service"] = "alipay.dut.customer.agreement.unsign"
        sParaTemp["_input_charset"] = 'utf-8'
        sParaTemp["product_code"] = "GENERAL_WITHHOLDING_P"
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
        sParaTemp['external_user_id'] = hashUserId
        # 上线修改正式服
        sParaTemp["return_url"] = rparams['returnUrl']
        # sParaTemp["notify_url"] =  'http://open.touch4.me/open/v4/pay/alifree/sign_callback'
        sParaTemp['sign'] = self.calcSignMD5(**sParaTemp)
        sParaTemp['sign_type'] = 'MD5'
        response, _ = TyContext.WebPage.webget(self.ALIPAY_GATEWAY_NEW, sParaTemp)
        xmlResponse = ElementTree.fromstring(response)
        TyContext.ftlog.info('TuYouPayAliV4.handle_alifree_unsign response', response)
        if True or xmlResponse.find('is_success').text == 'T':
            TyContext.RedisUser.execute(abs(hash(hashUserId)), 'DEL', 'universal_user:%s' % hashUserId)
        return '{"code":0, "info":"success"}'

    @payv4_callback('/open/gateway/alifree/sign_callback')
    def handle_alifree_sign_callback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouPayAliGatewayV4.sign_callback rparams=', rparams)
        status = rparams['status']
        sign = rparams['sign']
        # 签名校验
        if not self.verifySignMD5(sign, rparams):
            TyContext.ftlog.error('TuyouPayTuyou.doAliCallback md5 verify error !!')
            return 'error'
        # 此处userId为签约时传入的userId，格式为userId@appId
        external_user_id = rparams['external_user_id']
        if status == 'NORMAL':
            alipay_user_id = rparams['alipay_user_id']
            agreement_no = rparams['agreement_no']
            TyContext.RedisUser.execute(abs(hash(external_user_id)), 'HMSET',
                                        'universal_user:%s' % external_user_id,
                                        'alipay_agreement_no', agreement_no,
                                        'alipay_invalid_time', rparams['invalid_time'],
                                        'alipay_user_id', alipay_user_id)
            ####
            TyContext.RedisUser.execute(abs(hash(alipay_user_id)), 'HMSET',
                                        'universal_user:%s@alipay' % alipay_user_id,
                                        'alipay_agreement_no', agreement_no,
                                        'alipay_invalid_time', rparams['invalid_time'],
                                        'alipay_user_id', alipay_user_id)
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
