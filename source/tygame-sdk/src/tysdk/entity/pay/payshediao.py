# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import base64
import hashlib
from urllib import quote, urlencode
from xml.etree import ElementTree

import datetime
from Crypto.Cipher import DES

from constants import CHARGE_RATE_RMB
from rsacrypto import rsaVerify
from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper

_IOS_CALL_COUNT_ = 0


class TuyouPayShediao(object):
    cft_merId = '1215766201'  # '1215766301'
    cft_key = 'b07ac870c296e86e7d52da034efcb3e3'  # 'c6133fa99f3d9a5c3e58256913a8ede1'
    cft_init_url = 'https://wap.tenpay.com/cgi-bin/wappayv2.0/wappay_init.cgi'
    cft_pay_url = 'https://wap.tenpay.com/cgi-bin/wappayv2.0/wappay_gate.cgi'
    cft_callback_url = '/v1/pay/shediao/caifutong/callback'
    cft_notify_url = '/v1/pay/shediao/caifutong/notify'

    szf_merId = '174988'
    szf_privateKey = 'www.shediao.com'
    szf_desKey = 'VAR6j3n+he8='
    szf_callback_url = '/v1/pay/shediao/card/callback'
    szf_url = 'http://pay3.shenzhoufu.com/interface/version3/serverconnszx/entry-noxml.aspx'
    szf_request_code = {101: 'md5 验证失败 ',
                        102: '订单号重复 ',
                        103: '恶意用户 ',
                        104: '序列号，密码简单验证失败或之前曾提交过的卡密已验证失败',
                        105: '密码正在处理中 ',
                        106: '系统繁忙，暂停提交',
                        107: '多次支付时卡内余额不足',
                        109: 'des 解密失败 ',
                        201: '证书验证失败 ',
                        501: '插入数据库失败',
                        502: '插入数据库失败 ',
                        200: '请求成功，神州付收单（非订单支付成功）',
                        902: '商户参数不全 ',
                        903: '商户 ID 不存在 ',
                        904: '商户没有激活 ',
                        905: '商户没有使用该接口的权限',
                        906: '商户没有设置  密钥（privateKey）',
                        907: '商户没有设置  DES 密钥 ',
                        908: '该笔订单已经处理完成（订单状态已经为确定的状态:成功或者失败）',
                        909: '该笔订单不符合重复支付的条件 ',
                        910: '服务器返回地址，不符合规范 ',
                        911: '订单号，不符合规范 ',
                        912: '非法订单 ',
                        913: '该地方卡暂时不支持',
                        914: '支付金额非法 ',
                        915: '卡面额非法 ',
                        916: '商户不支持该充值卡的支付',
                        917: '参数格式不正确 ',
                        0: '网络连接失败'
                        }
    szf_call_back_code = {200: '支付成功',
                          201: '您输入的充值卡密码错误或充值卡余额不足以支付本次订单',
                          202: '您输入的充值卡已被使用 ',
                          203: '您输入的充值卡密码非法 ',
                          204: '您输入的卡号或密码错误次数过多',
                          205: '卡号密码正则不匹配或者被禁止',
                          206: '本卡之前被提交过，本次订单失败，不再继续处理',
                          207: '暂不支持该充值卡的支付 ',
                          208: '您输入的充值卡卡号错误 ',
                          209: '您输入的充值卡未激活（生成卡）',
                          210: '您输入的充值卡已经作废（能查到有该卡，但是没卡的信息）',
                          211: '您输入的充值卡已过期 ',
                          212: '您选择的卡面额不正确 ',
                          213: '该卡为特殊本地业务卡，系统不支持',
                          214: '该卡为增值业务卡，系统不支持 ',
                          215: '新生卡 ',
                          216: '系统维护 ',
                          217: '接口维护 ',
                          218: '运营商系统维护',
                          219: '系统忙，请稍后再试',
                          220: '未知错误 ',
                          221: '本卡之前被处理完毕，本次订单失败，不再继续处理',
                          0: '未知错误'
                          }

    @classmethod
    def doPayRequestAli(self, datas):
        mo = TyContext.Cls_MsgPack()
        from tysdk.entity.pay.pay import TuyouPay
        TuyouPay.makeBuyChargeMessage(mo, datas)
        return mo

    @classmethod
    def createLinkString(self, rparam):
        print rparam
        if rparam.has_key('sign'):
            del rparam['sign']
        if rparam.has_key('sign_type'):
            del rparam['sign_type']

        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            ret = ret + str(k) + '=' + str(rparam[k]) + '&'
        return ret[:-1]

    @classmethod
    def doAliCallback(self, rpath):
        from tysdk.entity.pay.pay import TuyouPay
        # tuYouId = '2088901481292394'
        sign = TyContext.RunHttp.getRequestParam('sign', '')

        rparam = TyContext.RunHttp.convertArgsToDict()

        notify_data = self.createLinkString(rparam)
        TyContext.ftlog.info('notify_data=', notify_data)
        # 签名校验
        if rsaVerify(notify_data, sign, 'shediao') != True:
            TyContext.ftlog.error('TuyouPayShediao.doAliCallback rsa verify error !!')
            return 'error'

        trade_status = TyContext.RunHttp.getRequestParam('trade_status', '')
        total_fee = int(float(TyContext.RunHttp.getRequestParam('total_fee', '0')))
        subject = TyContext.RunHttp.getRequestParam('subject', '')
        out_trade_no = TyContext.RunHttp.getRequestParam('out_trade_no', '')
        trade_no = TyContext.RunHttp.getRequestParam('trade_no', '')
        nodeTime = TyContext.RunHttp.getRequestParam('notify_reg_time', '')
        if nodeTime == '':
            nodeTime = TyContext.RunHttp.getRequestParam('gmt_create', '')
        if nodeTime != '':
            notify_reg_time = nodeTime
        else:
            notify_reg_time = 'not know'

        notifys = {'status': trade_status, 'total_fee': total_fee, 'subject': subject, 'out_trade_no': out_trade_no, \
                   'notify_reg_time': notify_reg_time, 'trade_no': trade_no, 'sign': sign, 'notify_data': notify_data}
        orderPlatformId = out_trade_no

        isOK = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, notifys)
        if isOK:
            return 'success'
        else:
            return 'error'

    @classmethod
    def doPayRequestCardYd(self, datas):
        rparam = self._getCardRequsetParams(datas, 0)
        return self.payCardRequest(rparam, datas)

    @classmethod
    def doPayRequestCardLt(self, datas):
        rparam = self._getCardRequsetParams(datas, 1)
        return self.payCardRequest(rparam, datas)

    @classmethod
    def doPayRequestCardDx(self, datas):
        rparam = self._getCardRequsetParams(datas, 2)
        return self.payCardRequest(rparam, datas)

    @classmethod
    def _getCardRequsetParams(self, datas, cardType):
        httpdomain = PayHelper.getSdkDomain()
        orderPrice = int(float(datas['orderPrice']))
        card_amount = int(float(datas['card_amount']))
        desKey = base64.decodestring(TuyouPayShediao.szf_desKey)
        cardInfo = str(card_amount) + '@' + str(datas['card_number']) + '@' + str(datas['card_pwd'])
        #        iv = Random.new().read(DES.block_size)
        desobj = DES.new(desKey, DES.MODE_ECB)
        padlen = 8 - len(cardInfo) % 8
        for i in xrange(padlen):
            cardInfo = cardInfo + chr(padlen)
        cipher = desobj.encrypt(cardInfo)
        cardInfo = base64.b64encode(cipher)
        orderPlatformId = datas['orderPlatformId']
        ct = datetime.datetime.now()
        orderId = ct.strftime('%Y%m%d') + '-' + TuyouPayShediao.szf_merId + '-' + orderPlatformId
        rparam = {}
        rparam['version'] = 3  # 版本号值为:  3
        rparam['merId'] = TuyouPayShediao.szf_merId  # 商户在神州付的唯一身份标识
        rparam['payMoney'] = orderPrice * 100  # 支付金额  单位:分
        rparam['orderId'] = orderId  # 订单号的格式:yyyyMMdd-merId-SN 
        rparam['returnUrl'] = httpdomain + TuyouPayShediao.szf_callback_url
        rparam[
            'cardInfo'] = cardInfo  # DES 加密并做 BASE64 编码后的数据  DES 加密数据格式:充值卡面额[单位:元]@充值卡序列号 @充值卡密码 (请与神州付技术联系配置密钥，然后登录商户平台查看密钥)
        rparam['merUserName'] = ''  # 支付此订单的用户的用户名
        rparam['merUserMail'] = ''  # 支付此订单的用户的邮箱
        rparam['privateField'] = orderPlatformId  # 可以传任意字母数字组成的字符串,回调的时候会传回给商户
        rparam['verifyType'] = 1  # 固定传1 
        rparam['cardTypeCombine'] = cardType  # 0:移动；1:联通；2:电信 
        md5String = str(rparam['version']) + str(rparam['merId']) + \
                    str(rparam['payMoney']) + str(rparam['orderId']) + \
                    str(rparam['returnUrl']) + str(rparam['cardInfo']) + \
                    str(rparam['privateField']) + str(rparam['verifyType']) + \
                    TuyouPayShediao.szf_privateKey
        m = hashlib.md5()
        m.update(md5String)
        md5String = m.hexdigest()
        rparam['md5String'] = md5String  # MD5 校验串 
        TyContext.ftlog.debug('_getCardRequsetParams->rparam=', rparam)
        return rparam

    @classmethod
    def createLinkString4Get(self, rparam):
        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            ret = ret + str(k) + '=' + quote(str(rparam[k]), '') + '&'
        return ret[:-1]

    @classmethod
    def payCardRequest(self, rparam, datas):
        cardUrl = TuyouPayShediao.szf_url + '?' + self.createLinkString4Get(rparam)
        TyContext.ftlog.info('TuyouPayShediao->requestUrl=', cardUrl)
        response, cardUrl = TyContext.WebPage.webget(cardUrl)
        TyContext.ftlog.info('TuyouPayShediao->requestUrl=', cardUrl, 'response=', response)
        status = 0
        try:
            status = int(response)
        except:
            status = 0
        mo = TyContext.Cls_MsgPack()
        from tysdk.entity.pay.pay import TuyouPay
        if status == 200:
            TuyouPay.makeBuyChargeMessage(mo, datas)
        else:
            mo.setResult('code', 1)
            mo.setResult('shediao.card.code', status)
            info = ''
            if status in TuyouPayShediao.szf_request_code:
                info = TuyouPayShediao.szf_request_code[status]
            else:
                info = '充值卡支付失败'
            info = info.decode('utf-8')
            mo.setResult('info', info)
        return mo

    @classmethod
    def doCardCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuyouPayShediao.doCardCallback->rparam=', rparam)

        version = rparam['version']
        merId = rparam['merId']
        payMoney = rparam['payMoney']
        orderId = rparam['orderId']
        payResult = rparam['payResult']
        privateField = rparam['privateField']
        payDetails = rparam['payDetails']
        md5String = rparam['md5String']
        # signString = rparam['signString']
        cardMoney = None
        if 'cardMoney' in rparam:
            cardMoney = rparam['cardMoney']

        if merId != TuyouPayShediao.szf_merId:
            TyContext.ftlog.error('TuyouPayShediao.doCardCallback-> its not my merId ! merId=', merId, 'my=',
                                  TuyouPayShediao.szf_merId)
            return 'error'

        combineString = ''
        if cardMoney != None:
            combineString = version + "|" + merId + "|" + payMoney + "|" + cardMoney + "|" + orderId + "|" + payResult + "|" + privateField + "|" + payDetails + "|" + TuyouPayShediao.szf_privateKey;
        else:
            combineString = version + merId + payMoney + orderId + payResult + privateField + payDetails + TuyouPayShediao.szf_privateKey;

        m = hashlib.md5()
        m.update(combineString)
        combineString = m.hexdigest()
        if md5String != combineString:
            TyContext.ftlog.error('TuyouPayShediao.doCardCallback-> md5 error ! md5String=', md5String,
                                  'combineString=', combineString)
            return 'error'

        from tysdk.entity.pay.pay import TuyouPay
        orderPlatformId = privateField

        if payResult != '1':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('TuyouPayShediao.doCardCallback error, charge return error !!!')
            errcode = 0
            if 'errcode' in rparam:
                errcode = int(rparam['errcode'])
            errorInfo = ''
            if errcode in TuyouPayShediao.szf_call_back_code:
                errorInfo = TuyouPayShediao.szf_call_back_code[errcode]
            else:
                errorInfo = '神州付-未知错误'
            errorInfo = errorInfo.decode('utf-8')
            TuyouPay.deliveryChargeError(orderPlatformId, rparam, errorInfo, 1)
            return orderId

        trade_status = 'TRADE_FINISHED'
        total_fee = int(float(payMoney) / 100)

        isOK = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOK:
            return orderId
        else:
            return 'error'

    @classmethod
    def doPayRequestCaiFuTong(self, datas):
        TyContext.ftlog.info('TuyouPayShediao.doPayRequestCaiFuTong->datas=', datas)
        httpdomain = PayHelper.getSdkDomain()
        charge = int(float(datas['orderPrice'])) * CHARGE_RATE_RMB
        rparam = {'ver': '2.0',  # 版本号，ver默认值是1.0，目前版本ver取值应为2.0
                  'charset': '1',  # 1 UTF-8, 2 GB2312， 默认为1
                  'bank_type': '0',  # 银行类型:财付通支付填0
                  'desc': 'TYB' + str(charge),  # 商品描述，32个字符以内
                  # 'purchaser_id' :'', # 用户(买方)的财付通帐户(QQ )。若商户没有传该参数，则在财付通支付页面，买家需要输入其财付通帐户
                  'bargainor_id': TuyouPayShediao.cft_merId,  # 商户号
                  'sp_billno': datas['orderPlatformId'],  # 商户系统内部的定单号，32个字符内、可包含字母
                  'total_fee': charge * 100,  # 总金额，以分为单位，不允许包含任何字、符号
                  'fee_type': '1',  # 现金支付币种，目前只支持人民币，默认值是1:人民币
                  'notify_url': httpdomain + TuyouPayShediao.cft_notify_url,  # 接收财付通通知的URL，需给绝对路径
                  'callback_url': httpdomain + TuyouPayShediao.cft_callback_url,  # 交易完成后跳转的URL，需给绝对路径
                  # 'attach': datas['orderPlatformId'] # 商户附加信息，可做扩展参数，255字符内
                  # 'time_start' : '' # 订单生成时间
                  # 'time_expire' : '' # 订单失效时间
                  # 'sign':'' # MD5签名结果
                  }
        sk = rparam.keys()
        sk.sort()
        queryStr = ""
        for k in sk:
            queryStr = queryStr + str(k) + '=' + str(rparam[k]) + '&'
        signData = queryStr + 'key=' + TuyouPayShediao.cft_key
        m = hashlib.md5()
        m.update(signData)
        sign = m.hexdigest().upper()
        rparam['sign'] = sign
        initUrl = TuyouPayShediao.cft_init_url + '?' + urlencode(rparam)
        TyContext.ftlog.info('TuyouPayShediao.doPayRequestCaiFuTong->initUrl=', initUrl)
        response, initUrl = TyContext.WebPage.webget(initUrl, {}, None, '', 'GET', {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0',
            'Accept-Encoding': 'deflate',
            'Connection': 'keep-alive',
            'Host': 'wap.tenpay.com',
            })
        TyContext.ftlog.info('TuyouPayShediao.doPayRequestCaiFuTong->initUrl=', initUrl, 'response=', response)
        if response.find('gb2312') > 0:
            response = response.replace('gb2312', 'utf-8')
            response = unicode(response, encoding='gb2312').encode('utf-8')

        err_info = '财付通初始化失败'
        token_id = None
        xmlroot = ElementTree.fromstring(response)
        xmlnode = xmlroot.find('token_id')
        if xmlnode != None:
            token_id = xmlnode.text

        errnode = xmlroot.find('err_info')
        if errnode != None:
            err_info = errnode.text

        mo = TyContext.Cls_MsgPack()
        if token_id != None:
            from tysdk.entity.pay.pay import TuyouPay
            TuyouPay.makeBuyChargeMessage(mo, datas)
            mo.setResult('payUrl', TuyouPayShediao.cft_pay_url + '?token_id=' + token_id)
        else:
            mo.setResult('code', 1)
            mo.setResult('info', err_info)
        return mo

    @classmethod
    def doCaiFuTongCallback(self, rpath):
        htmlpath = '/sdk/pay/pay.callback.ty'
        pay_result = int(self.getRequestParam('pay_result', 1))
        datas = {}
        if pay_result == 0:
            datas['message'] = '您的充值已经成功，请等候后续处理...<p style="color:green">您可以关闭此页面，继续游戏</p>'
        else:
            datas['message'] = '<p style="color:red">您的充值操作失败，请重新进行充值</p>'
        raise Exception('doTemplate not defined !')
        # return doTemplate(htmlpath, datas)

    @classmethod
    def doCaiFuTongNotify(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        signQuery = rparam['sign']
        del rparam['sign']

        sk = rparam.keys()
        sk.sort()
        queryStr = ""
        for k in sk:
            queryStr = queryStr + str(k) + '=' + str(rparam[k]) + '&'
        signData = queryStr + 'key=' + TuyouPayShediao.cft_key
        m = hashlib.md5()
        m.update(signData)
        sign = m.hexdigest().upper()
        if signQuery.upper() != sign:
            TyContext.ftlog.info('TuyouPayShediao.doCaiFuTongNotify->ERROR, sign error !! signQuery=', signQuery,
                                 'sign=', sign)
            return 'error'

        orderPlatformId = rparam['sp_billno']

        from tysdk.entity.pay.pay import TuyouPay
        if rparam['pay_result'] != '0':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('TuyouPayShediao.doCaiFuTongNotify error, charge return error !!!')
            errorInfo = ''
            if 'pay_info' in rparam:
                errorInfo = rparam['pay_info']
                errorInfo = errorInfo.decode('utf-8')
            else:
                errorInfo = '财付通-未知错误'
            TuyouPay.deliveryChargeError(orderPlatformId, rparam, errorInfo, 1)
            return 'success'

        trade_status = 'TRADE_FINISHED'
        total_fee = int(float(rparam['total_fee']))
        total_fee = int(total_fee / 100)

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return 'success'
        else:
            return 'error'
