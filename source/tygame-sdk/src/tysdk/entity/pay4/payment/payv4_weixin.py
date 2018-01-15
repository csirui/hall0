#! encoding=utf-8
import json
import random
import time
import urllib
from collections import OrderedDict
from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_filter import payv4_filter
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4
from tysdk.entity.pay4.strategy.ios_weixin_strategy import TuYooIOSPayWeixinStrategy

__author__ = 'yuejianqiang'


class PayWeixinV4(PayBaseV4):
    token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    # prepay_url = 'https://api.weixin.qq.com/pay/genprepay'
    prepay_url_new = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    @payv4_order('weixin')
    def handle_order(self, mi):
        chargeInfo = self.get_charge_info(mi)
        ###
        wxappId = mi.getParamStr('wxappId')
        openid = mi.getParamStr('openid')
        tradeType = mi.getParamStr('tradeType', 'APP')
        wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
        config = wxconfig.get(str(wxappId), None)
        if config:
            wxappId = str(config['appId'])
            wxpaySignKey = str(config['paySignKey'])
            wxappSecret = str(config['appSecret'])
            wxpartnerId = str(config['partnerId'])
            wxpartnerKey = str(config['partnerKey'])
        else:
            appId = chargeInfo['appId']
            packageName = chargeInfo['packageName']
            config = GameItemConfigure(appId).get_game_channel_configure_by_package('weixin', packageName)
            if not config:
                raise PayErrorV4(1, 'can not find wxpay config info define of wxappId=' + str(wxappId))
            wxappId = str(config['WXAPPID'])
            wxpaySignKey = ""  # 用不到了
            wxappSecret = str(config['WXAPPKEY'])
            wxpartnerId = str(config['partnerId'])
            wxpartnerKey = str(config['partnerKey'])
        token = self.__get_accesstoken(wxappId, wxappSecret)
        payData = self.__get_prepayid_new(chargeInfo, token, wxappId, wxpaySignKey,
                                          wxpartnerId, wxpartnerKey, tradeType, openid)
        return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)

    @payv4_filter('weixin', 'tuyou.ali', 'alipaywap', 'unionpay', 'wxwap')
    def filter_payment(self, payment, prod_info, **kwargs):
        appId = kwargs['appId']
        userId = kwargs['userId']
        clientId = kwargs['clientId']
        if clientId.startswith('IOS_'):
            strategy_name = payment.get('strategy', 'default_strategy')
            strategy = TuYooIOSPayWeixinStrategy(strategy_name)
            if not strategy(appId=appId, userId=userId, clientId=clientId):
                return False
        return True

    @payv4_order('wxwap')
    def handle_weixinjs(self, mi):
        chargeInfo = self.get_charge_info(mi)
        # 必须采用途游棋牌的wxappId
        wxappId = 'wxb01a635a437adb75'  # mi.getParamStr('wxappId')
        openid = mi.getParamStr('openid', None)
        tradeType = mi.getParamStr('tradeType', 'WAP')
        wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
        config = wxconfig.get(str(wxappId), None)
        if config:
            wxappId = str(config['appId'])
            wxpaySignKey = str(config['paySignKey'])
            wxappSecret = str(config['appSecret'])
            wxpartnerId = str(config['partnerId'])
            wxpartnerKey = str(config['partnerKey'])
        else:
            appId = chargeInfo['appId']
            packageName = chargeInfo['packageName']
            config = GameItemConfigure(appId).get_game_channel_configure_by_package('weixin', packageName)
            if not config:
                raise PayErrorV4(1, 'can not find wxpay config info define of wxappId=' + str(wxappId))
            wxappId = str(config['WXAPPID'])
            wxpaySignKey = ""  # 用不到了
            wxappSecret = str(config['WXAPPKEY'])
            wxpartnerId = str(config['partnerId'])
            wxpartnerKey = str(config['partnerKey'])
        token = self.__get_accesstoken(wxappId, wxappSecret)
        payData = self.__get_prepayid_new(chargeInfo, token, wxappId, wxpaySignKey,
                                          wxpartnerId, wxpartnerKey, tradeType, openid)
        return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)

    @payv4_callback('/open/ve/pay/wxwap/request')
    def handle_wxwap_request(self, rpath):
        args = TyContext.RunHttp.convertArgsToDict()
        deeplink = args['deeplink']

        return """<html><head>
<meta http-equiv="content-type" content="text/html;charset=utf8">
<meta id="viewport" name="viewport" content="width=device-width; initial-scale=1.0; maximum-scale=1; user-scalable=no;">
<title>【微信支付V2.0】WAP支付实例</title>
<!--
/****************************************
本文件是【微信支付V2.0】WAP支付实例
需要用授权接口进入页面
****************************************/
-->
<style type="text/css">
/* 重置 [[*/
body,p,ul,li,h1,h2,form,input{margin:0;padding:0;}
h1,h2{font-size:100%%;}
ul{list-style:none;}
body{-webkit-user-select:none;-webkit-text-size-adjust:none;font-family:Helvetica;background:#ECECEC;}
html,body{height:100%%;}
a,button,input,img{-webkit-touch-callout:none;outline:none;}
a{text-decoration:none;}
/* 重置 ]]*/
/* 功能 [[*/
.hide{display:none!important;}
.cf:after{content:".";display:block;height:0;clear:both;visibility:hidden;}
/* 功能 ]]*/
/* 按钮 [[*/
a[class*="btn"]{display:block;height:42px;line-height:42px;color:#FFFFFF;text-align:center;border-radius:5px;}
.btn-blue{background:#3D87C3;border:1px solid #1C5E93;}
.btn-green{background-image:-webkit-gradient(linear, left top, left bottom, color-stop(0, #43C750), color-stop(1, #31AB40));border:1px solid #2E993C;box-shadow:0 1px 0 0 #69D273 inset;}
/* 按钮 [[*/
/* 充值页 [[*/
.charge{font-family:Helvetica;padding-bottom:10px;-webkit-user-select:none;}
.charge h1{height:44px;line-height:44px;color:#FFFFFF;background:#3D87C3;text-align:center;font-size:20px;-webkit-box-sizing:border-box;box-sizing:border-box;}
.charge h2{font-size:14px;color:#777777;margin:5px 0;text-align:center;}
.charge .content{padding:10px 12px;}
.charge .select li{position:relative;display:block;float:left;width:100%%;margin-right:2%%;height:150px;line-height:150px;text-align:center;border:1px solid #BBBBBB;color:#666666;font-size:16px;margin-bottom:5px;border-radius:3px;background-color:#FFFFFF;-webkit-box-sizing:border-box;box-sizing:border-box;overflow:hidden;}
.charge .price{border-bottom:1px dashed #C9C9C9;padding:10px 10px 15px;margin-bottom:20px;color:#666666;font-size:12px;}
.charge .price strong{font-weight:normal;color:#EE6209;font-size:26px;font-family:Helvetica;}
.charge .showaddr{border:1px dashed #C9C9C9;padding:10px 10px 15px;margin-bottom:20px;color:#666666;font-size:12px;text-align:center;}
.charge .showaddr strong{font-weight:normal;color:#9900FF;font-size:26px;font-family:Helvetica;}
.charge .copy-right{margin:5px 0; font-size:12px;color:#848484;text-align:center;}
/* 充值页 ]]*/
</style>
</head>
<body>
    <article class="charge">
        <h1>微信支付-WAP支付-demo</h1>
        <section class="content">

生成预支付wx20160310185404b0f5689fb10084106757单成功，请点击购买支付
<div class="operation"><a class="btn-blue" id="getBrandWCPayRequest" href="%s">立即购买</a></div>        </section>
    </article>

</body></html>""" % deeplink

    @payv4_callback('/open/ve/pay/wxpay/callback')
    def handle_callback(self, rpath):
        return self.doWXpayCallback(rpath)

    @classmethod
    def __get_accesstoken(cls, wxappId, wxappSecret):
        wxtokenkey = 'wx:token:' + wxappId
        token = TyContext.RedisPayData.execute('GET', wxtokenkey)
        if not token:
            postparams = {}
            postparams['grant_type'] = 'client_credential'
            postparams['appid'] = wxappId
            postparams['secret'] = wxappSecret
            response, _ = TyContext.WebPage.webget(cls.token_url, postdata_=postparams)
            response = json.loads(response)
            if response['access_token']:
                token = str(response['access_token'])
                TyContext.RedisPayData.execute('SET', wxtokenkey, token)
                TyContext.RedisPayData.execute('EXPIRE', wxtokenkey, int(response['expires_in']))
            else:
                raise PayErrorV4(1, 'can not get wxpay access token of appId=' + wxappId)
        return token

    @classmethod
    def __get_prepayid_new(cls, chargeInfo, token, wxappId, wxpaySignKey,
                           partnerId, partnerKey, tradeType='APP', openid=None):
        prepayUrl = cls.prepay_url_new + '?access_token=' + token
        notifyurl = PayHelperV4.getSdkDomain() + '/open/ve/pay/wxpay/callback'

        postparams = {}
        postparams['appid'] = wxappId
        postparams['mch_id'] = partnerId
        postparams['nonce_str'] = md5(str(random.randint(0, 10000))).hexdigest()
        postparams['body'] = chargeInfo['buttonName']
        postparams['out_trade_no'] = chargeInfo['platformOrderId']
        postparams['fee_type'] = 'CNY'  # 货币类型
        postparams['total_fee'] = str(int(float(chargeInfo['chargeTotal']) * 100))
        postparams['spbill_create_ip'] = TyContext.RunHttp.get_client_ip()
        postparams['notify_url'] = notifyurl
        postparams['trade_type'] = tradeType
        if tradeType == 'JSAPI':
            postparams['openid'] = openid

        calStr = '&'.join(k + "=" + postparams[k] for k in sorted(postparams.keys())) + '&key=' + partnerKey
        signValue = md5(calStr).hexdigest().upper()
        postparams['sign'] = signValue
        TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new calStr=', calStr, 'postparams=', postparams)

        rootXml = ElementTree.Element('xml')
        for i in postparams:
            element = ElementTree.SubElement(rootXml, i)
            element.text = postparams[i]
        postXml = ElementTree.tostring(rootXml, encoding='utf-8')
        TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new postXml=', postXml)

        response, _ = TyContext.WebPage.webget(prepayUrl, postdata_=postXml.encode('utf-8'))
        xmlResponse = ElementTree.fromstring(response)
        TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new xmlResponse=', xmlResponse)

        if 'SUCCESS' == xmlResponse.find('return_code').text:
            if 'SUCCESS' == xmlResponse.find('result_code').text:
                payData = OrderedDict()
                prepayid = xmlResponse.find('prepay_id').text

                if tradeType == 'JSAPI':
                    payData['appId'] = wxappId
                    payData['nonceStr'] = postparams['nonce_str']
                    payData['package'] = "prepay_id=" + prepayid
                    payData['timeStamp'] = str(int(time.time()))
                    payData['signType'] = 'MD5'
                elif tradeType == 'WAP':
                    payData['appid'] = wxappId
                    payData['noncestr'] = postparams['nonce_str']
                    payData['package'] = 'WAP'
                    payData['prepayid'] = prepayid
                    payData['timestamp'] = str(int(time.time()))
                else:
                    payData['appid'] = wxappId
                    payData['noncestr'] = postparams['nonce_str']
                    payData['prepayid'] = prepayid
                    payData['package'] = 'Sign=WXpay'
                    payData['partnerid'] = partnerId
                    payData['timestamp'] = str(int(time.time()))
                signStr = '&'.join(k + "=" + payData[k] for k in sorted(payData.keys())) + '&key=' + partnerKey
                sign = md5(signStr).hexdigest().upper()
                payData['sign'] = sign
                if tradeType == 'WAP':
                    payData['deeplink'] = cls.get_deeplink(payData)
                TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new payData=', payData, 'signStr', signStr)
                return payData
            else:
                TyContext.ftlog.error('TuyouPayWXpay.__get_prepayid_new return_msg',
                                      xmlResponse.find('return_msg').text)
        else:
            raise PayErrorV4(1, 'can not get wxpay prepayid  of wxappId=' + wxappId)

    def doWXpayCallback(self, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info('TuyouPayWXpay.doWXpayCallback in xmldata=', xmldata)
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
            total_fee = float(rparam['total_fee']) / 100
            wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
            config = wxconfig.get(str(wxappId), None)
            if not config:
                appConfig = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'weixin')
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

        rparam['third_orderid'] = openId
        rparam['chargeType'] = 'wxpay'
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            returnCode.text = 'SUCCESS'
            returnMsg.text = 'OK'
        else:
            returnCode.text = 'FAIL'
            returnMsg.text = '发货失败'

        responseStr = ElementTree.tostring(responseXml)
        return responseStr

    def __delattr__(self, *args, **kwargs):
        return super(PayWeixinV4, self).__delattr__(*args, **kwargs)

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

    @classmethod
    def get_deeplink(cls, payData):

        str1 = urllib.urlencode(payData)
        str2 = urllib.quote(str1)
        return 'weixin://wap/pay?%s' % str2
