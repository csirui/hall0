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
from tysdk.entity.huiyuan.weixin_huiyuan import WeixinHuiyuan
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_filter import payv4_filter
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.paythird.helper import PayHelper

__author__ = 'yuejianqiang'


class PayWeixinPapV4(PayBaseV4):
    token_url = 'https://api.weixin.qq.com/cgi-bin/token'
    # prepay_url = 'https://api.weixin.qq.com/pay/genprepay'
    prepay_url_new = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    @payv4_filter('wxpap')
    def filter_payment(self, payment, prod_info, **kwargs):
        """
        支付方式列表中过滤检查，没有计费点得商品就不要显示此支付方式
        :param prodInfo:
        :param chargeInfo:
        :param kwargs:
        :return:
        """
        appId = kwargs['appId']
        clientId = kwargs['clientId']
        userId = kwargs['userId']
        wxpap_config = GameItemConfigure(appId).get_game_channel_configure('wxpap_config')
        wxpap_contract_id, wxpap_contract_code = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%s' % userId,
                                                                             'wxpap_contract_id', 'wxpap_contract_code')
        if wxpap_contract_id and wxpap_contract_code:
            payment['options'] = {
                'wxpap_sign': 1,
            }
        else:
            payment['options'] = {
                'wxpap_sign': 0,
            }
        return True

    @payv4_order('wxpap')
    def handle_order(self, mi):
        chargeInfo = self.get_charge_info(mi)
        ###
        wxpap_config = GameItemConfigure(chargeInfo['appId']).get_game_channel_configure('wxpap_config')
        wxappId = wxpap_config['wxappId']
        plan_id = wxpap_config['plan_id']
        ## get pay config
        wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
        config = wxconfig.get(str(wxappId), None)
        wxappId = str(config['appId'])
        wxpaySignKey = str(config['paySignKey'])
        wxappSecret = str(config['appSecret'])
        wxpartnerId = str(config['partnerId'])
        wxpartnerKey = str(config['partnerKey'])
        userId = int(chargeInfo['userId'])

        wxpap_contract_id, wxpap_contract_code = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%s' % userId,
                                                                             'wxpap_contract_id', 'wxpap_contract_code')
        # 已经签约
        if wxpap_contract_id and wxpap_contract_code:
            postparams = {
                'appid': wxappId,
                'mch_id': wxpartnerId,
                'nonce_str': md5(str(random.randint(0, 10000))).hexdigest(),
                'body': chargeInfo['buttonName'],
                'out_trade_no': chargeInfo['platformOrderId'],
                'total_fee': str(int(float(chargeInfo['chargeTotal']) * 100)),
                'fee_type': 'CNY',  # 货币类型
                'spbill_create_ip': TyContext.RunHttp.get_client_ip(),
                'notify_url': PayHelper.getSdkDomain() + '/open/ve/pay/wxpap/order_callback',
                'trade_type': 'PAP',
                'contract_id': str(wxpap_contract_id),
            }
            calStr = '&'.join(k + "=" + postparams[k] for k in sorted(postparams.keys())) + '&key=' + wxpartnerKey
            signValue = md5(calStr).hexdigest().upper()
            postparams['sign'] = signValue
            TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new calStr=', calStr, 'postparams=', postparams)

            rootXml = ElementTree.Element('xml')
            for i in postparams:
                element = ElementTree.SubElement(rootXml, i)
                element.text = postparams[i]
            postXml = ElementTree.tostring(rootXml, encoding='utf-8')
            TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new postXml=', postXml)
            papUrl = 'https://api.mch.weixin.qq.com/pay/pappayapply'
            response, _ = TyContext.WebPage.webget(papUrl, postdata_=postXml.encode('utf-8'))
            xmlResponse = ElementTree.fromstring(response)
            TyContext.ftlog.debug('TuyouPayWXpay.__get_prepayid_new xmlResponse=', response)
            return_code = xmlResponse.find('return_code').text
            return_msg = xmlResponse.find('return_msg').text
            err_code = xmlResponse.find('err_code').text if xmlResponse.find('err_code') is not None else ''
            err_code_des = xmlResponse.find('err_code_des').text if xmlResponse.find('err_code_des') is not None else ''
            if err_code != 'CONTRACTERROR':
                payData = {
                    'status': 'signed',
                    'return_code': return_code,
                    'return_msg': return_msg or err_code_des,
                }
                # 更新会员
                if err_code == 'SUCCESS':
                    WeixinHuiyuan(chargeInfo['appId'], userId).handle_order(chargeInfo)
                return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)
        # 需要重新签约
        # get userInfo
        userEmail, userName, coin, userPurl, userSex, userSnsId, bindMobile = \
            TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId),
                                        'email', 'name', 'diamond', 'purl', 'sex', 'snsId', 'bindMobile')
        request_serial = int(TyContext.RedisMix.execute('INCR', 'global.orderid.seq.a'))
        rparams = {
            'appid': wxappId,
            'mch_id': wxpartnerId,
            'plan_id': plan_id,
            'contract_code': chargeInfo['platformOrderId'],
            'request_serial': request_serial,
            'contract_display_account': userName,
            'notify_url': PayHelper.getSdkDomain() + '/open/ve/pay/wxpap/sign_callback',
            'version': '1.0',
            'timestamp': str(int(time.time())),
        }
        # save sign
        calStr = '&'.join(k + "=" + str(rparams[k]) for k in sorted(rparams.keys())) + '&key=' + wxpartnerKey
        signValue = md5(calStr).hexdigest().upper()
        rparams['sign'] = signValue
        payData = {
            'status': 'unsign',
            'err_code': '',
            'sign_url': 'https://api.mch.weixin.qq.com/papay/entrustweb?%s' % urllib.urlencode(rparams)
        }
        ## unsigned
        WeixinHuiyuan(9999, userId).handle_unsign()
        return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)

    @payv4_callback('/open/ve/pay/wxpap/sign_callback')
    def handle_sign_callback(self, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info('PayWeixinPapV4.sign_callback in xmldata=', xmldata)
        xmlroot = ElementTree.fromstring(xmldata)
        rparams = {}
        for node in xmlroot.iter():
            if 'xml' != node.tag:
                rparams[node.tag] = node.text
        # response
        responseXml = ElementTree.Element('xml')
        returnCode = ElementTree.SubElement(responseXml, 'return_code')
        returnMsg = ElementTree.SubElement(responseXml, 'return_msg')
        # configure
        wxpap_config = GameItemConfigure(9999).get_game_channel_configure('wxpap_config')
        wxappId = wxpap_config['wxappId']
        plan_id = wxpap_config['plan_id']
        ## get pay config
        wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
        config = wxconfig.get(str(wxappId), None)
        wxappId = str(config['appId'])
        wxpaySignKey = str(config['paySignKey'])
        wxappSecret = str(config['appSecret'])
        wxpartnerId = str(config['partnerId'])
        wxpartnerKey = str(config['partnerKey'])
        if not self.__verify_sign(rparams, wxpartnerKey, rparams['sign']):
            TyContext.ftlog.error('TuyouPayWXpay.doWXpayCallback verify error !!')
            returnCode.text = 'FAIL'
            returnMsg.text = '签名失败'
            responseStr = ElementTree.tostring(responseXml)
            return responseStr
        #
        result_code = rparams['result_code']
        if result_code == 'SUCCESS':
            change_type = rparams['change_type']
            contract_code = rparams['contract_code']
            contract_id = rparams['contract_id']
            ###
            # 解约
            if change_type == 'DELETE':
                userId = TyContext.RedisUserKeys.execute('HGET', 'wxpap_contract_code', contract_code)
                if userId:
                    TyContext.RedisUser.execute(userId, 'HDEL', 'user:%s' % userId,
                                                'wxpap_contract_id'
                                                'wxpap_contract_code',
                                                'wxpap_plan_id')
            # 签约
            else:
                chargeInfo = self.load_order_charge_info(contract_code)
                userId = chargeInfo['userId']
                TyContext.RedisUser.execute(userId, 'HMSET', 'user:%s' % userId,
                                            'wxpap_contract_id', contract_id,
                                            'wxpap_contract_code', contract_code,
                                            'wxpap_plan_id', rparams['plan_id'])

                TyContext.RedisUserKeys.execute('HSET', 'wxpap_contract_code', contract_code, userId)
                ### 签约成功
                WeixinHuiyuan(9999, userId).handle_sign()
        returnCode.text = 'SUCCESS'
        returnMsg.text = 'OK'
        responseStr = ElementTree.tostring(responseXml)
        return responseStr

    @payv4_callback('/open/ve/pay/wxpap/order_callback')
    def handle_order_callback(self, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info('PayWeixinPapV4.order_callback in xmldata=', xmldata)
        xmlroot = ElementTree.fromstring(xmldata)
        rparams = {}
        for node in xmlroot.iter():
            if 'xml' != node.tag:
                rparams[node.tag] = node.text
        # configure
        wxpap_config = GameItemConfigure(9999).get_game_channel_configure('wxpap_config')
        wxappId = wxpap_config['wxappId']
        plan_id = wxpap_config['plan_id']
        ## get pay config
        wxconfig = TyContext.Configure.get_global_item_json('wx_config', {})
        config = wxconfig.get(str(wxappId), None)
        wxappId = str(config['appId'])
        wxpaySignKey = str(config['paySignKey'])
        wxappSecret = str(config['appSecret'])
        wxpartnerId = str(config['partnerId'])
        wxpartnerKey = str(config['partnerKey'])
        # response
        responseXml = ElementTree.Element('xml')
        returnCode = ElementTree.SubElement(responseXml, 'return_code')
        returnMsg = ElementTree.SubElement(responseXml, 'return_msg')
        ### check sign
        if not self.__verify_sign(rparams, wxpartnerKey, rparams['sign']):
            TyContext.ftlog.error('TuyouPayWXpay.doWXpayCallback verify error !!')
            returnCode.text = 'FAIL'
            returnMsg.text = '签名失败'
            responseStr = ElementTree.tostring(responseXml)
            return responseStr
        result_code = rparams['result_code']
        out_trade_no = rparams['out_trade_no']
        chargeInfo = self.load_order_charge_info(out_trade_no)
        if result_code == 'SUCCESS':
            ## huiyuan
            WeixinHuiyuan(chargeInfo['appId'], chargeInfo['userId']).handle_order(chargeInfo)
            isOk = PayHelper.callback_ok(out_trade_no, -1, rparams)
            if isOk:
                returnCode.text = 'SUCCESS'
                returnMsg.text = 'OK'
                return ElementTree.tostring(responseXml)
        returnCode.text = 'FAIL'
        returnMsg.text = '发货失败'
        return ElementTree.tostring(responseXml)

    @classmethod
    def get_accesstoken(cls, wxappId, wxappSecret):
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
    def get_prepayid_new(cls, chargeInfo, token, wxappId, wxpaySignKey,
                         partnerId, partnerKey, tradeType='APP', openid=None, notifyurl=None):

        if not notifyurl:
            notifyurl = PayHelper.getSdkDomain() + '/open/ve/pay/wxpap/callback'
        prepayUrl = cls.prepay_url_new + '?access_token=' + token
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
        try:
            chargeInfo = cls.load_order_charge_info(orderPlatformId)
            appId, userId = chargeInfo['appId'], chargeInfo['userId']
            WeixinHuiyuan(appId, userId).handle_order(chargeInfo['buttodId'], orderPlatformId,
                                                      chargeInfo['chargeTotal'])
        except:
            TyContext.ftlog.exception()
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

    @classmethod
    def get_deeplink(cls, payData):

        str1 = urllib.urlencode(payData)
        str2 = urllib.quote(str1)
        return 'weixin://wap/pay?%s' % str2
