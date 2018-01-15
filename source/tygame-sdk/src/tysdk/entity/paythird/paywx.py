# -*- coding=utf-8 -*-

import json
import random
import time
from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayWXpay(object):
    token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    # prepay_url = 'https://api.weixin.qq.com/pay/genprepay'
    prepay_url_new = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'fake': 'data'}

    @classmethod
    def doPayRequestWx(cls, chargeInfo, mi, mo):
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
            raise Exception('can not find wxpay config info define of wxappId=' + str(wxappId))
        token = cls.__get_accesstoken(wxappId, wxappSecret)
        # payData = cls.__get_prepayid(chargeInfo, token, wxappId, wxpaySignKey, wxpartnerId, wxpartnerKey)
        payData = cls.__get_prepayid_new(chargeInfo, token, wxappId, wxpaySignKey,
                                         wxpartnerId, wxpartnerKey, tradeType, openid)

        mo.setResult('payData', payData)
        return PayConst.CHARGE_STATE_REQUEST

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
                raise Exception('can not get wxpay access token of appId=' + wxappId)
        return token

    '''
    @classmethod
    def __get_prepayid(cls, chargeInfo, token, wxappId, wxpaySignKey, partnerId, partnerKey):
        prepayUrl = cls.prepay_url + '?access_token=' + token
        orderPlatformId = chargeInfo['platformOrderId']
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/wxpay/callback'
        rparam = {}
        rparam['bank_type'] = 'WX'
        rparam['body'] = chargeInfo['diamondName']
        rparam['partner'] = partnerId
        rparam['out_trade_no'] = orderPlatformId
        rparam['total_fee'] = str(int(float(chargeInfo['chargeTotal']) * 100))
        rparam['fee_type'] = '1'
        rparam['notify_url'] = notifyurl
        rparam['spbill_create_ip'] = TyContext.RunHttp.get_client_ip()
        rparam['input_charset'] = 'UTF-8'
        cal_str = '&'.join(k + "=" + rparam[k] for k in sorted(rparam.keys())) + '&key=' + partnerKey
        signValue = md5(cal_str.encode('utf-8')).hexdigest().upper()
        packageValue = '&'.join(k + "=" + urllib.quote(rparam[k].encode('utf-8')) for k in sorted(rparam.keys())) \
                       + "&sign=" + signValue

        postparams = {}
        postparams['appid'] = wxappId
        postparams['appkey'] = wxpaySignKey
        postparams['traceid'] = orderPlatformId
        postparams['noncestr'] = md5(str(random.randint(0, 10000))).hexdigest()
        postparams['package'] = packageValue
        postparams['timestamp'] = str(int(time.time()))
        sign_str = '&'.join(k + "=" + postparams[k] for k in sorted(postparams.keys()))
        app_signature = sha1(sign_str).hexdigest()
        postparams['app_signature'] = app_signature
        postparams['sign_method'] = 'sha1'
        del postparams['appkey']
        postjson = json.dumps(postparams, ensure_ascii=False)
        response, _ = TyContext.WebPage.webget(prepayUrl, postdata_=postjson)
        response = json.loads(response)
        if 'prepayid' in response.keys() and response['prepayid']:
            payData = {}
            payData['appid'] = wxappId
            payData['appkey'] = wxpaySignKey
            payData['prepayid'] = response['prepayid']
            payData['noncestr'] =  postparams['noncestr']
            payData['package'] = 'Sign=WXpay'
            payData['partnerid'] = partnerId
            payData['timestamp'] = postparams['timestamp']
            sign_str = '&'.join(k + "=" + payData[k] for k in sorted(payData.keys()))
            sign = sha1(sign_str).hexdigest()
            payData['sign'] = sign
            return payData
        else:
            raise Exception('can not get wxpay prepayid  of wxappId=' + wxappId)
    '''

    @classmethod
    def __get_prepayid_new(cls, chargeInfo, token, wxappId, wxpaySignKey,
                           partnerId, partnerKey, tradeType='APP', openid=None):
        prepayUrl = cls.prepay_url_new + '?access_token=' + token
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/wxpay/callback'

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

        xml = ['<xml>', ]
        for k, v in postparams.items():
            if isinstance(v, int):
                xml.append('<%s>%s</%s>' % (k, v, k))
            else:
                xml.append('<%s><![CDATA[%s]]></%s>' % (k, v, k))
        xml.append('</xml>')
        postXml = ''.join(xml)
        TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new postXml=', postXml)

        response, _ = TyContext.WebPage.webget(prepayUrl, postdata_=postXml.encode('utf-8'))
        xmlResponse = ElementTree.fromstring(response)
        TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new xmlResponse=', xmlResponse)

        if 'SUCCESS' == xmlResponse.find('return_code').text:
            if 'SUCCESS' == xmlResponse.find('result_code').text:
                payData = {}
                prepayid = xmlResponse.find('prepay_id').text

                if tradeType == 'JSAPI':
                    payData['appId'] = wxappId
                    payData['nonceStr'] = postparams['nonce_str']
                    payData['package'] = "prepay_id=" + prepayid
                    payData['timeStamp'] = str(int(time.time()))
                    payData['signType'] = 'MD5'
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
                TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new payData=', payData, 'signStr', signStr)
                return payData
            else:
                TyContext.ftlog.error('TuyouPayWXpay.__get_prepayid_new return_msg',
                                      xmlResponse.find('return_msg').text)
        else:
            raise Exception('can not get wxpay prepayid  of wxappId=' + wxappId)

    '''
    @classmethod
    def doWXpayCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info('TuyouPayWXpay.doWXpayCallback in xmldata=', xmldata)
        xmlroot = ElementTree.fromstring(xmldata)
        wxappId = xmlroot.find('AppId').text
        OpenId = xmlroot.find('OpenId').text

        try:
            orderPlatformId = rparam['out_trade_no']
            total_fee = float(rparam['total_fee']) / 100
            wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
            config = wxconfig.get(str(wxappId), None)
            wxpartnerKey = str(config['partnerKey'])
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doWXpayCallback->ERROR, param error !! rparam=', rparam)
            return "error"

        # 签名校验
        if not cls.__verify_sign(rparam, wxpartnerKey, sign):
            TyContext.ftlog.error('TuyouPayWXpay.doWXpayCallback verify error !!')
            return "error"

        rparam['third_orderid'] = OpenId
        rparam['chargeType'] = 'wxpay'
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk :
            return "ok"
        else:
            return "error"
    '''

    @classmethod
    def doWXpayCallback(cls, rpath):
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
            wxpartnerKey = str(config['partnerKey'])
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doWXpayCallback->ERROR, param error !! rparam=', rparam)
            returnCode.text = 'FAIL'
            returnMsg.text = '参数格式校验错误'
            responseStr = ElementTree.tostring(responseXml)
            return responseStr

        # 签名校验
        if not cls.__verify_sign(rparam, wxpartnerKey, sign):
            TyContext.ftlog.error('TuyouPayWXpay.doWXpayCallback verify error !!')
            returnCode.text = 'FAIL'
            returnMsg.text = '签名失败'
            responseStr = ElementTree.tostring(responseXml)
            return responseStr

        rparam['third_orderid'] = openId
        rparam['chargeType'] = 'wxpay'
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            returnCode.text = 'SUCCESS'
            returnMsg.text = 'OK'
        else:
            returnCode.text = 'FAIL'
            returnMsg.text = '发货失败'

        responseStr = ElementTree.tostring(responseXml)
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
