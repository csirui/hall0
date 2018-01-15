#! encoding=utf-8

import hashlib
from urlparse import parse_qs

from datetime import datetime

from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import _verify_with_cert_openssl, _sign_with_privatekey_pycrypto
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4

__author__ = 'yuejianqiang'

"""
pfx文件提取private key：
    openssl pkcs12 -in acp_test_sign.pfx -nocerts -out test.pem -nodes
获取serial number
    openssl pkcs12 -nokeys -in 700000000000001_acp-4.pfx | openssl x509 -serial -noout
"""


class PayUnionPayV4(PayBaseV4):
    version = "5.0.0"
    encoding_UTF8 = "UTF-8"
    merId = '802130059620501'
    certId = '69812453430'
    appTransUrl = 'https://gateway.95516.com/gateway/api/appTransReq.do'
    frontTransUrl = 'https://gateway.95516.com/gateway/api/frontTransReq.do'
    backUrl = 'http://open.touch4.me/v1/pay/unionpay/callback'

    @payv4_order('unionpay')
    def handle_order(self, mi):
        """
        v4版本银联手机支付创建订单接口
        :param mi:
        :return:
        """
        chargeinfo = self.get_charge_info(mi)
        platformOrderId = chargeinfo['platformOrderId']
        txnTime = datetime.now().strftime('%Y%m%d%H%M%S')
        appId = chargeinfo['appId']
        merParam = self.getMerParam(appId=appId)
        if not merParam:
            merId = self.merId
        else:
            merId = merParam['merId']
        txnAmt = int(float(chargeinfo['chargeTotal']) * 100)
        contentData = {
            # /***银联全渠道系统，产品参数，除了encoding自行选择外其他不需修改***/
            "version": self.version,  # 版本号 全渠道默认值
            "encoding": self.encoding_UTF8,  # 字符集编码 可以使用UTF-8,GBK两种方式
            "signMethod": "01",  # 签名方法 目前只支持01：RSA方式证书加密
            "txnType": "01",  # 交易类型 01:消费
            "txnSubType": "01",  # 交易子类 01：消费
            "bizType": "000201",  # 填写000201
            "channelType": "07",  # 渠道类型
            # /***商户接入参数***/
            "merId": merId,  # 商户号码，请改成自己申请的商户号或者open上注册得来的777商户号测试
            "accessType": "0",  # 接入类型，商户接入填0 ，不需修改（0：直连商户， 1： 收单机构 2：平台商户）
            "orderId": platformOrderId,  # 商户订单号，8-40位数字字母，不能含“-”或“_”，可以自行定制规则
            "txnTime": txnTime,  # 订单发送时间，取系统时间，格式为YYYYMMDDhhmmss，必须取当前时间，否则会报txnTime无效
            "accType": "01",  # 账号类型 01：银行卡02：存折03：IC卡帐号类型(卡介质)
            "certId": self.certId,
        }
        # contentData['encryptCertId'] = '137445581060'
        # contentData['accNo'] = 'FV8j6mVZ67pqQvGm0kYzZXRXoUunT7xNqJRt2VZWBAjsV3LBW0D/bLPJb5Fj9YHWTUL8oIPHnSM7pqVLW0hJpv6D5ohiXm4PRjuN9Goi35aSWJoWRCRWp//4WKgyBr92yMBGSkfAHkkPrlHp8MfK/DE2XCi8vzG7exPjDmuXkuUVlpXAXROwuzpKTV3p7AQf6DBUXtNyTf13qqfUP5piHJfZScenaq9MkBpmM+Iey/ZZ5+vAzp9RqHf/3TMXX98tV5+snWkFNOYNkYjupp67SXJq+i4pWZykR76ACLTmtljhIdLDB2DwlDo9ZMr8N2UgiEg4UdFyMCnUqLwVnkYf0w=='
        # contentData["customerInfo"] = customerInfoStr
        contentData["txnAmt"] = txnAmt  # 交易金额 单位为分，不能带小数点
        contentData["currencyCode"] = "156"  # 境内商户固定 156 人民币
        contentData["reqReserved"] = platformOrderId  # 商户自定义保留域，交易应答时会原样返回
        contentData["backUrl"] = self.backUrl
        contentData['signature'] = self.calcSign(**contentData)
        response, purl = TyContext.WebPage.webget(self.appTransUrl, postdata_=contentData)
        result = parse_qs(response)
        if result.get('respCode')[0] == '00':
            chargeData = {
                'tn': result.get('tn')[0]
            }
        else:
            chargeData = {}
        chargeinfo['chargeData'] = chargeData
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/v4/pay/unionpay')
    def handle_union_gateway(self, rpath):
        """
        v4版本银联wap支付接口
        :param rpath:
        :return:
        """

        mi = TyContext.RunHttp.convertToMsgPack()
        mi.setParam('chargeType', 'unionpay')
        chargeinfo = self.get_charge_info(mi)
        platformOrderId = chargeinfo['platformOrderId']
        txnTime = datetime.now().strftime('%Y%m%d%H%M%S')
        appId = chargeinfo['appId']
        merParam = self.getMerParam(appId=appId)
        if not merParam:
            merId = self.merId
        else:
            merId = merParam['merId']
        txnAmt = int(float(chargeinfo['chargeTotal']) * 100)
        backUrl = mi.getParamStr('backUrl', '')
        contentData = {}
        # /***银联全渠道系统，产品参数，除了encoding自行选择外其他不需修改***/
        contentData["version"] = self.version  # 版本号，全渠道默认值
        contentData["encoding"] = self.encoding_UTF8  # 字符集编码，可以使用UTF-8,GBK两种方式
        contentData["signMethod"] = "01"  # 签名方法，只支持 01：RSA方式证书加密
        contentData["txnType"] = "01"  # 交易类型 ，01：消费
        contentData["txnSubType"] = "01"  # 交易子类型， 01：自助消费
        contentData["bizType"] = "000201"  # 业务类型，B2C网关支付，手机wap支付
        contentData["channelType"] = "07"  # 渠道类型，这个字段区分B2C网关支付和手机wap支付；07：PC,平板  08：手机
        # /***商户接入参数***/
        contentData["merId"] = merId  # 商户号码，请改成自己申请的正式商户号或者open上注册得来的777测试商户号
        contentData["accessType"] = "0"  # 接入类型，0：直连商户
        contentData["orderId"] = platformOrderId  # 商户订单号，8-40位数字字母，不能含“-”或“_”，可以自行定制规则
        contentData["txnTime"] = txnTime  # 订单发送时间，取系统时间，格式为YYYYMMDDhhmmss，必须取当前时间，否则会报txnTime无效
        contentData["currencyCode"] = "156"  # 交易币种（境内商户一般是156 人民币）
        contentData["txnAmt"] = txnAmt  # 交易金额，单位分，不要带小数点
        contentData[
            "reqReserved"] = platformOrderId  # 请求方保留域，透传字段（可以实现商户自定义参数的追踪）本交易的后台通知,对本交易的交易状态查询交易、对账文件中均会原样返回，商户可以按需上传，长度为1-1024个字节
        contentData["certId"] = self.certId
        # contentData['encryptCertId'] = '137445581060'
        # contentData['accNo'] = 'FV8j6mVZ67pqQvGm0kYzZXRXoUunT7xNqJRt2VZWBAjsV3LBW0D/bLPJb5Fj9YHWTUL8oIPHnSM7pqVLW0hJpv6D5ohiXm4PRjuN9Goi35aSWJoWRCRWp//4WKgyBr92yMBGSkfAHkkPrlHp8MfK/DE2XCi8vzG7exPjDmuXkuUVlpXAXROwuzpKTV3p7AQf6DBUXtNyTf13qqfUP5piHJfZScenaq9MkBpmM+Iey/ZZ5+vAzp9RqHf/3TMXX98tV5+snWkFNOYNkYjupp67SXJq+i4pWZykR76ACLTmtljhIdLDB2DwlDo9ZMr8N2UgiEg4UdFyMCnUqLwVnkYf0w=='
        # contentData["customerInfo"] = customerInfoStr
        # contentData["txnAmt"] = txnAmt                             #交易金额 单位为分，不能带小数点
        # contentData["currencyCode"] = "156"                     #境内商户固定 156 人民币
        # contentData["reqReserved"] = platformOrderId            #商户自定义保留域，交易应答时会原样返回
        contentData["backUrl"] = self.backUrl
        contentData["frontUrl"] = backUrl
        contentData['signature'] = self.calcSign(**contentData)
        return self.createAutoFormHtml(self.frontTransUrl, contentData, 'UTF-8')

    @classmethod
    def createAutoFormHtml(cls, action, hiddens, encoding):
        sf = "<html><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=" + encoding + "\"/></head><body>"
        sf += "<form id = \"pay_form\" action=\"" + action + "\" method=\"post\">"
        for key, value in hiddens.items():
            sf += "<input type=\"hidden\" name=\"" + str(key) + "\" id=\"" + str(key) + "\" value=\"" + str(
                value) + "\"/>\n"
        sf += "</form>"
        sf += "</body>"
        sf += "<script type=\"text/javascript\">"
        sf += "document.all.pay_form.submit();"
        sf += "</script>"
        sf += "</html>"
        return sf

    @classmethod
    def calcSign(cls, **args):
        # convert dict to list
        pairs = filter(lambda x: x[1], args.items())
        # sort list
        pairs.sort(lambda x, y: cmp(x[0], y[0]))
        text = '&'.join(['%s=%s' % (k, v) for k, v in pairs])
        code = hashlib.sha1(text).hexdigest()
        merId = args['merId']
        return cls.rsaUnionPaySign(code, merId)

    @payv4_callback('/open/ve/pay/unionpay/callback')
    def doUnionPayCallback(self, rpath):
        """
        银联v4版本支付回调
        :param rpath:
        :return:
        """
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayUnionPayV4 in prams=', '%s' % params)
        if not self.validateSign(**params):
            return 'sign-error'
        orderId = params['orderId']
        isOk = PayHelperV4.callback_ok(orderId, -1, params)
        if isOk:
            return 'ok'
        else:
            return 'error'

    @classmethod
    def validateSign(cls, **resData):
        stringSign = resData.get('signature')
        # 从返回报文中获取certId ，然后去证书静态Map中查询对应验签证书对象
        # certId = resData.get('certId');
        pairs = filter(lambda x: x[1] and x[0] != 'signature', resData.items())
        pairs.sort(lambda x, y: cmp(x[0], y[0]))
        text = '&'.join(['%s=%s' % (k, v) for k, v in pairs])
        # 验证签名需要用银联发给商户的公钥证书.
        stringData = hashlib.sha1(text).hexdigest()
        merId = resData.get('merId')
        return cls.verifyUnionPayCert(stringData, stringSign, merId)

    @classmethod
    def getMerParam(cls, **params):
        merId = params.get("merId", "")
        unionpayConfig = TyContext.Configure.get_global_item_json('unionpay_config', {})

        if not merId:
            for k, v in params.iteritems():
                merId = unionpayConfig['merId'].get(str(v), "")
                if merId:
                    break
        if merId:
            merParam = unionpayConfig['merParam'].get(merId, None)
            if merParam:
                return merParam
        TyContext.ftlog.debug("TuYouPayUnionPayV4 unionpay_config not exist ")
        return None

    @classmethod
    def verifyUnionPayCert(cls, strData, strSign, merId):

        from OpenSSL.crypto import load_certificate, FILETYPE_PEM
        merParam = cls.getMerParam(merId=merId)
        if not merParam:
            TyContext.ftlog.error("TuYouPayUnionPayV4 unionpay_config not exist,merId", merId)
            return False
        UNIONPAY_CERT_KEY = merParam['certKey']
        _unionpay_certkey = load_certificate(FILETYPE_PEM, UNIONPAY_CERT_KEY)
        return _verify_with_cert_openssl(strData, strSign, _unionpay_certkey)

    @classmethod
    def rsaUnionPaySign(cls, data, merId):
        from Crypto.PublicKey import RSA
        merParam = cls.getMerParam(merId=merId)
        if not merParam:
            TyContext.ftlog.error("TuYouPayUnionPayV4 unionpay_config not exist,merId", merId)
            return False
        strKey = merParam['privateKey']
        _unionpay_private_key = RSA.importKey(strKey)
        return _sign_with_privatekey_pycrypto(data, _unionpay_private_key)
