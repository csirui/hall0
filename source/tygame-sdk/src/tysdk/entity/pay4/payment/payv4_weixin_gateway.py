#! encoding=utf-8
import json
from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.payment.payv4_gateway import PayGatewayV4
from tysdk.entity.pay4.payment.payv4_weixin import PayWeixinV4
from tysdk.entity.pay_common.orderlog import Order
from tysdk.entity.paythird.helper import PayHelper

__author__ = 'yuejianqiang'


class PayWeixinV4Gateway(PayGatewayV4):
    @payv4_callback('/open/gateway/wxpay/order')
    def doPay(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('PayWeixinV4Gateway.doPay rparams=', rparams)
        if not self.checkGatewaySign(rparams):
            return '{"code":1,"msg":"signature error"}'
        appId = rparams['appId']
        prodName = rparams['prodName']
        prodPrice = rparams['prodPrice']
        orderId = rparams['orderId']
        notifyUrl = rparams['notifyUrl']
        ###
        chargeInfo = {
            'buttonName': prodName,
            'platformOrderId': orderId,
            'chargeTotal': float(prodPrice),
        }
        wxappId = 'wxb01a635a437adb75'  # mi.getParamStr('wxappId')
        openid = None  # mi.getParamStr('openid')
        tradeType = 'WAP'
        wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
        config = wxconfig.get(str(wxappId), None)
        if config:
            wxappId = str(config['appId'])
            wxpaySignKey = str(config['paySignKey'])
            wxappSecret = str(config['appSecret'])
            wxpartnerId = str(config['partnerId'])
            wxpartnerKey = str(config['partnerKey'])
        else:
            raise PayErrorV4(1, 'can not find wxpay config info define of wxappId=' + str(wxappId))
        token = PayWeixinV4.get_accesstoken(wxappId, wxappSecret)
        callbackUrl = PayHelper.getSdkDomain() + '/open/gateway/wxpay/callback'
        payData = PayWeixinV4.get_prepayid_new(chargeInfo, token, wxappId, wxpaySignKey,
                                               wxpartnerId, wxpartnerKey, tradeType, openid, callbackUrl)
        ###
        chargeData = {
            'appId': appId,
            'prodName': prodName,
            'prodPrice': prodPrice,
            'orderId': orderId,
            'notifyUrl': notifyUrl,
            'payData': payData
        }
        TyContext.RedisPayData.execute('SET', 'sdk.charge.gateway:' + orderId, json.dumps(chargeData))
        return json.dumps({'code': 0, 'payData': payData})

    @payv4_callback('/open/gateway/wxpay/callback')
    def doCallback(self, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info('PayWeixinV4Gateway.doWXpayCallback in xmldata=', xmldata)
        xmlroot = ElementTree.fromstring(xmldata)
        wxappId = xmlroot.find('appid').text
        openId = xmlroot.find('openid').text

        rparam = {}
        for node in xmlroot.iter():
            if 'xml' != node.tag:
                rparam[node.tag] = node.text
        TyContext.ftlog.debug('TuyouPayWXpay.doWXpayCallback in rparam=', rparam)

        responseXml = ElementTree.Element('xml')
        returnCode = ElementTree.SubElement(responseXml, 'return_code')
        returnMsg = ElementTree.SubElement(responseXml, 'return_msg')

        try:
            orderPlatformId = rparam['out_trade_no']
            transaction_id = rparam['transaction_id']
            total_fee = float(rparam['total_fee']) / 100
            wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
            config = wxconfig.get(str(wxappId), None)
            wxpartnerKey = str(config['partnerKey'])
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doWXpayCallback->ERROR, param error !! rparam=', rparam)
            returnCode.text = 'FAIL'
            returnMsg.text = '参数格式校验错误'
            responseStr = ElementTree.tostring(responseXml)
            return responseStr

        # 签名校验
        if not self.__verify_sign(rparam, wxpartnerKey, sign):
            TyContext.ftlog.error('TuyouPayWXpay.doWXpayCallback verify error !!')
            returnCode.text = 'FAIL'
            returnMsg.text = '签名失败'
            responseStr = ElementTree.tostring(responseXml)
            return responseStr

        chargeData = TyContext.RedisPayData.execute('GET', 'sdk.charge.gateway:' + orderPlatformId)
        chargeData = json.loads(chargeData)
        appId = chargeData['appId']
        notifyUrl = chargeData['notifyUrl']
        params = {
            'appId': appId,
            'prodName': chargeData['prodName'],
            'prodPrice': chargeData['prodPrice'],
            'orderId': orderPlatformId,
            'total_fee': total_fee,
            'transaction_id': transaction_id,
            'status': 'success',
        }
        params['sign'] = self.calcGatewaySign(params)
        result = TyContext.WebPage.webget(notifyUrl, params, method_='GET')
        if result == 'success' or result == 'ok':
            returnCode.text = 'SUCCESS'
            returnMsg.text = 'OK'
        else:
            returnCode.text = 'FAIL'
            returnMsg.text = '发货失败'
        responseStr = ElementTree.tostring(responseXml)

        # report bi data
        try:
            TyContext.BiReport.report_bi_sdk_buy(Order.CALLBACK_OK,
                                                 0,  # userId
                                                 appId,  # appId
                                                 '',  # clientId,
                                                 '',  # orderId
                                                 charge_price=chargeData['prodPrice'],
                                                 succ_price=chargeData['prodPrice'],
                                                 paytype=114)  # wxwap
        except:
            TyContext.ftlog.exception()

        return responseStr

    @classmethod
    def __verify_sign(cls, rparam, partnerKey, sign):
        check_str = '&'.join(k + "=" + rparam[k] for k in sorted(rparam.keys()) if k != 'sign') \
                    + '&key=' + partnerKey
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().upper()
        if digest != sign:
            TyContext.ftlog.error('TuyouPayWXpay verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
