# -*- coding=utf-8 -*-

import json
import random
import time
import urllib
from hashlib import md5
from hashlib import sha1
from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class TuyouPayWXpay(object):
    token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    prepay_url = 'https://api.weixin.qq.com/pay/genprepay'

    @classmethod
    def doPayRequestWx(cls, params):
        mo = TyContext.Cls_MsgPack()
        appId = params['appId']
        wxappId = params['wxappId']
        prodId = params['prodId']
        wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
        config = wxconfig.get(str(wxappId), None)
        if config:
            wxappId = str(config['appId'])
            wxpaySignKey = str(config['paySignKey'])
            wxappSecret = str(config['appSecret'])
            wxpartnerId = str(config['partnerId'])
            wxpartnerKey = str(config['partnerKey'])
        else:
            raise Exception('can not find wxpay config info define of appId=' + str(appId))
        token = cls._get_accesstoken(wxappId, wxappSecret)
        payData = cls._get_prepayid(params, token, wxappId, wxpaySignKey, wxpartnerId, wxpartnerKey)

        mo.setResult('code', 0)
        mo.setResult('payData', payData)
        return mo

    @classmethod
    def _get_accesstoken(cls, wxappId, wxappSecret):
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

    @classmethod
    def _get_prepayid(cls, params, token, wxappId, wxpaySignKey, partnerId, partnerKey):
        prepayUrl = cls.prepay_url + '?access_token=' + token
        orderPlatformId = params['orderPlatformId']
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/wxpay/callback'
        rparam = {}
        rparam['bank_type'] = 'WX'
        rparam['body'] = params['orderName']
        rparam['partner'] = partnerId
        rparam['out_trade_no'] = orderPlatformId
        rparam['total_fee'] = str(int(params['orderPrice']) * 100)
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
            payData['noncestr'] = postparams['noncestr']
            payData['package'] = 'Sign=WXpay'
            payData['partnerid'] = partnerId
            payData['timestamp'] = postparams['timestamp']
            sign_str = '&'.join(k + "=" + payData[k] for k in sorted(payData.keys()))
            sign = sha1(sign_str).hexdigest()
            payData['sign'] = sign
            return payData
        else:
            raise Exception('can not get wxpay prepayid  of wxappId=' + wxappId)

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

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'
        rparam['OpenId'] = OpenId

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            return "ok"
        else:
            return "error"

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
