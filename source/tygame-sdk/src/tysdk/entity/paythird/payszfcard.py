# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import base64
import hashlib

import datetime
from Crypto.Cipher import DES

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay3.constants import PayConst


class TuYouPaySzfCard(object):
    szf_merId = '103545'
    szf_privateKey = 'www.tuyoo.com'
    szf_desKey = 'Cx+ng570B9k='
    szf_callback_url = '/v1/pay/card/callback'
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
                        908: '该笔订单已经处理完成（订单状态已经为确定的状态：成功或者失败）',
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

    reqSeq = 0

    @classmethod
    def doPayRequestCardYd(cls, chargeInfo, mi, mo):
        return cls.__pay_card_request__(chargeInfo, mi, mo, 0)

    @classmethod
    def doPayRequestCardLt(cls, chargeInfo, mi, mo):
        return cls.__pay_card_request__(chargeInfo, mi, mo, 1)

    @classmethod
    def doPayRequestCardDx(cls, chargeInfo, mi, mo):
        return cls.__pay_card_request__(chargeInfo, mi, mo, 2)

    @classmethod
    def __get_card_request_params__(cls, chargeInfo, mi, mo, cardType):
        if not PayHelper.checkCardParam(mi, mo):
            return None

        orderPrice = int(float(chargeInfo['chargeTotal']))
        card_amount = mi.getParamStr('card_amount', '')
        desKey = base64.decodestring(cls.szf_desKey)
        cardInfo = card_amount + '@' + mi.getParamStr('card_number') + '@' + mi.getParamStr('card_pwd')
        TyContext.ftlog.debug('__get_card_request_params__ cardInfo=', cardInfo)
        #        iv = Random.new().read(DES.block_size)
        desobj = DES.new(desKey, DES.MODE_ECB)
        padlen = 8 - len(cardInfo) % 8
        for i in xrange(padlen):
            cardInfo = cardInfo + chr(padlen)
        cipher = desobj.encrypt(cardInfo)
        cardInfo = base64.b64encode(cipher)
        cls.reqSeq += 1
        orderPlatformId = chargeInfo['platformOrderId']
        ct = datetime.datetime.now()
        orderId = ct.strftime('%Y%m%d') + '-' + cls.szf_merId + '-' + orderPlatformId + str(cls.reqSeq % 10000)
        rparam = {}
        rparam['version'] = 3  # 版本号值为：  3
        rparam['merId'] = cls.szf_merId  # 商户在神州付的唯一身份标识
        rparam['payMoney'] = orderPrice * 100  # 支付金额  单位：分
        rparam['orderId'] = orderId  # 订单号的格式：yyyyMMdd-merId-SN
        rparam['returnUrl'] = PayHelper.getSdkDomain() + cls.szf_callback_url
        rparam[
            'cardInfo'] = cardInfo  # DES 加密并做 BASE64 编码后的数据  DES 加密数据格式：充值卡面额[单位:元]@充值卡序列号 @充值卡密码 (请与神州付技术联系配置密钥，然后登录商户平台查看密钥)
        rparam['merUserName'] = ''  # 支付此订单的用户的用户名
        rparam['merUserMail'] = ''  # 支付此订单的用户的邮箱
        rparam['privateField'] = orderPlatformId  # 可以传任意字母数字组成的字符串,回调的时候会传回给商户
        rparam['verifyType'] = 1  # 固定传1
        rparam['cardTypeCombine'] = cardType  # 0：移动；1：联通；2：电信
        md5String = str(rparam['version']) + str(rparam['merId']) + \
                    str(rparam['payMoney']) + str(rparam['orderId']) + \
                    str(rparam['returnUrl']) + str(rparam['cardInfo']) + \
                    str(rparam['privateField']) + str(rparam['verifyType']) + \
                    cls.szf_privateKey
        m = hashlib.md5()
        m.update(md5String)
        md5String = m.hexdigest()
        rparam['md5String'] = md5String  # MD5 校验串
        TyContext.ftlog.debug('__get_card_request_params__->rparam=', rparam)
        return rparam

    @classmethod
    def __pay_card_request__(cls, chargeInfo, mi, mo, cardType):
        rparam = cls.__get_card_request_params__(chargeInfo, mi, mo, cardType)
        if not rparam:
            return PayConst.CHARGE_STATE_REQUEST_RETRY

        cardUrl = cls.szf_url + '?' + PayHelper.createLinkString4Get(rparam)
        TyContext.ftlog.info('TuYouPaySzf->requestUrl=', cardUrl)
        response, cardUrl = TyContext.WebPage.webget(cardUrl, {})
        TyContext.ftlog.info('TuYouPaySzf->requestUrl=', cardUrl, 'response=', response)
        status = 0
        try:
            status = int(response)
        except:
            status = 0
        if status != 200:
            if status in cls.szf_request_code:
                errInfo = cls.szf_request_code[status]
            else:
                errInfo = '充值卡支付失败'
            errInfo = errInfo.decode('utf-8')
            mo.setError(1, errInfo)
            return PayConst.CHARGE_STATE_REQUEST_IGNORE
        else:
            return PayConst.CHARGE_STATE_REQUEST

    @classmethod
    def doCardCallback(cls, rpath):
        rparam = PayHelper.getArgsDict()
        TyContext.ftlog.info('cls.doCardCallback->rparam=', rparam)

        version = rparam['version']
        merId = rparam['merId']
        payMoney = rparam['payMoney']
        orderId = rparam['orderId']
        payResult = rparam['payResult']
        privateField = rparam['privateField']
        payDetails = rparam['payDetails']
        md5String = rparam['md5String']
        # signString = rparam['signString']

        if merId != cls.szf_merId:
            TyContext.ftlog.error('cls.doCardCallback-> its not my merId ! merId=', merId, 'my=', cls.szf_merId)
            return 'error'

        cardMoney = rparam.get('cardMoney')
        if cardMoney:
            combineString = version + "|" + merId + "|" + payMoney + "|" + cardMoney + "|" + orderId + "|" + payResult + "|" + privateField + "|" + payDetails + "|" + cls.szf_privateKey
        else:
            combineString = version + merId + payMoney + orderId + payResult + privateField + payDetails + cls.szf_privateKey

        isOk = PayHelper.verify_md5(md5String, combineString)
        if not isOk:
            TyContext.ftlog.error('cls.doCardCallback-> md5 error ! md5String=', md5String, 'combineString=',
                                  combineString)
            return 'error'

        platformOrderId = privateField
        rparam['chargeType'] = 'shenzhoufu.card'

        if payResult != '1':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('cls.doCardCallback error, charge return error !!!')
            errcode = 0
            if 'errcode' in rparam:
                errcode = int(rparam['errcode'])
            errorInfo = ''
            if errcode in cls.szf_call_back_code:
                errorInfo = cls.szf_call_back_code[errcode]
            else:
                errorInfo = '神州付-未知错误'
            errorInfo = errorInfo.decode('utf-8')
            PayHelper.callback_error(platformOrderId, errorInfo, rparam)
            return orderId

        total_fee = float(payMoney) / 100
        isOK = PayHelper.callback_ok(platformOrderId, total_fee, rparam)
        if isOK:
            return orderId
        else:
            return 'error'
