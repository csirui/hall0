#! encoding=utf-8

import hashlib
from urlparse import parse_qs

from datetime import datetime

from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaUnionPaySign, verifyUnionPayCert
from tysdk.entity.paythird.helper import PayHelper

__author__ = 'yuejianqiang'


class TuYouPayUnionPay(object):
    version = "5.0.0"
    encoding_UTF8 = "UTF-8"
    merId = '777290058124087'
    appTransUrl = 'https://101.231.204.80:5000/gateway/api/appTransReq.do'
    certId = '40220995861346480087409489142384722381'

    @classmethod
    def charge_data(cls, chargeinfo):
        platformOrderId = chargeinfo['platformOrderId']
        txnTime = datetime.now().strftime('%Y%m%d%H%M%S')
        merId = cls.merId
        txnAmt = int(float(chargeinfo['chargeTotal']) * 100)
        backUrl = 'http://open.touch4.me/v1/pay/unionpay/callback'
        contentData = {
            # /***银联全渠道系统，产品参数，除了encoding自行选择外其他不需修改***/
            "version": cls.version,  # 版本号 全渠道默认值
            "encoding": cls.encoding_UTF8,  # 字符集编码 可以使用UTF-8,GBK两种方式
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
            "certId": cls.certId,
        }
        # contentData['encryptCertId'] = '137445581060'
        # contentData['accNo'] = 'FV8j6mVZ67pqQvGm0kYzZXRXoUunT7xNqJRt2VZWBAjsV3LBW0D/bLPJb5Fj9YHWTUL8oIPHnSM7pqVLW0hJpv6D5ohiXm4PRjuN9Goi35aSWJoWRCRWp//4WKgyBr92yMBGSkfAHkkPrlHp8MfK/DE2XCi8vzG7exPjDmuXkuUVlpXAXROwuzpKTV3p7AQf6DBUXtNyTf13qqfUP5piHJfZScenaq9MkBpmM+Iey/ZZ5+vAzp9RqHf/3TMXX98tV5+snWkFNOYNkYjupp67SXJq+i4pWZykR76ACLTmtljhIdLDB2DwlDo9ZMr8N2UgiEg4UdFyMCnUqLwVnkYf0w=='
        # contentData["customerInfo"] = customerInfoStr
        contentData["txnAmt"] = txnAmt  # 交易金额 单位为分，不能带小数点
        contentData["currencyCode"] = "156"  # 境内商户固定 156 人民币
        contentData["reqReserved"] = platformOrderId  # 商户自定义保留域，交易应答时会原样返回
        contentData["backUrl"] = backUrl
        contentData['signature'] = cls.calcSign(**contentData)
        response, purl = TyContext.WebPage.webget(cls.appTransUrl, postdata_=contentData)
        result = parse_qs(response)
        if result.get('respCode')[0] == '00':
            chargeData = {
                'tn': result.get('tn')[0]
            }
        else:
            chargeData = {}
        chargeinfo['chargeData'] = chargeData

    @classmethod
    def calcSign(cls, **args):
        # convert dict to list
        pairs = filter(lambda x: x[1], args.items())
        # sort list
        pairs.sort(lambda x, y: cmp(x[0], y[0]))
        text = '&'.join(['%s=%s' % (k, v) for k, v in pairs])
        code = hashlib.sha1(text).hexdigest()
        return rsaUnionPaySign(code)

    @classmethod
    def doUnionPayCallback(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayYdjd.TuYouPayUnionPay in prams=', '%s' % params)
        if not cls.validateSign(**params):
            return 'sign-error'
        orderId = params['orderId']
        isOk = PayHelper.callback_ok(orderId, -1, params)
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
        return verifyUnionPayCert(stringData, stringSign)
