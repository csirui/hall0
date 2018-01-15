# -*- coding=utf-8 -*-

import json
from hashlib import md5

import datetime

from constants import PHONETYPE_CHINAMOBILE, PHONETYPE_CHINAUNION, PHONETYPE_CHINATELECOM
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay_common.clientrevision import ClientRevision


class TuYouPayLinkYunApi(object):
    apiurl = 'http://121.40.131.189:8080/sdk_command_platform/CommandApiAction'

    @classmethod
    def charge_data(cls, chargeinfo):
        TyContext.ftlog.debug('TuYouPayLinkYunApi charge_data', chargeinfo)

        smsMsg = ''
        smsPort = ''
        smsType = '1'

        userId = chargeinfo['uid']
        appId = chargeinfo['appId']
        phoneType = TyContext.UserSession.get_phone_type_name(chargeinfo['phoneType'])
        prodId = chargeinfo.get("prodId", chargeinfo['diamondId'])
        price = str(chargeinfo['chargeTotal'])
        platformOrderId = chargeinfo['platformOrderId']

        shortOrderPlatformId = ShortOrderIdMap.get_short_order_id(platformOrderId)
        iccid = TyContext.UserSession.get_session_iccid(userId)
        postparams = {}
        postparams['ip_add'] = TyContext.RunHttp.get_client_ip()
        postparams['accessFlag'] = '0001'
        if phoneType == PHONETYPE_CHINAMOBILE:
            postparams['provider'] = 'YD'
            postparams['iccid'] = iccid
            postparams['channelNum'] = 'B2'
            postparams['SHParams'] = '00' + shortOrderPlatformId
            postparams['price'] = price
            if int(price) < 10:
                postparams['price'] = '0' + price
            postparams['sign'] = cls.__cal_mobile_sign(postparams)
            response, final_url = TyContext.WebPage.webget(cls.apiurl, postdata_=postparams)
            response = json.loads(response)
            return cls._get_sms_payinfo(chargeinfo, response)

        elif phoneType == PHONETYPE_CHINAUNION:
            postparams['provider'] = 'LT'
            postparams['appName'] = 'chenjinglong'
            postparams['callbackData'] = 'B2'
            postparams['totalFee'] = price
            postparams['outTradeNo'] = '00' + shortOrderPlatformId
            postparams['subject'] = 'good'
            postparams['timeStamp'] = str(datetime.datetime.now()).replace(' ', '-')
            TyContext.ftlog.debug('doLinkyunapiCallback chinaunion timestamp:', postparams['timeStamp'])
            postparams['appKey'] = str(appId)
            postparams['sign'] = cls.__cal_union_sign(postparams)
            response, final_url = TyContext.WebPage.webget(cls.apiurl, postparams)
            response = json.loads(response)
            return cls._get_sms_payinfo(chargeinfo, response)

        elif phoneType == PHONETYPE_CHINATELECOM:
            postparams['provider'] = 'DX'
            postparams['iccid'] = iccid
            postparams['productID'] = '01'  # XXX
            postparams['SHParams'] = '00' + shortOrderPlatformId
            postparams['price'] = price
            postparams['appKey'] = str(appId)
            postparams['channelNum'] = 'B2'
            postparams['sign'] = cls.__cal_telecom_sign(postparams)
            response, final_url = TyContext.WebPage.webget(cls.apiurl, postparams)
            response = json.loads(response)
            return cls._get_sms_payinfo(chargeinfo, response)
        else:
            TyContext.ftlog.error('TuYouPayLinkYunApi no phoneType=', phoneType)
            return

    @classmethod
    def _get_sms_payinfo(cls, chargeinfo, response):
        TyContext.ftlog.info('TuYouPayLinkYunApi _get_sms_payinfo '
                             'response', response, 'chargeinfo', chargeinfo)
        userId = chargeinfo['uid']
        if int(response['resultCode']) != 0:
            TyContext.ftlog.error('TuYouPayLinkYunApi can not get resultCode in the response=', response)
            return
        sms_count = 1
        spnumbers = {}
        sms_msgs = {}
        spnumbers[0] = str(response['number'])
        sms_msgs[0] = str(response['command'])
        if response['flag']:
            sms_count = 2
            spnumbers[1] = str(response['number'])
            sms_msgs[1] = str(response['command'])
        if response['confirmContent'] != 'N':
            sms_count = 2
            sms_msgs[1] = str(response['confirmContent'])
            spnumbers[1] = str(response['confirmNumber'])
        if not ClientRevision(userId).support_type0_smspayinfo:
            if sms_count == 2:
                payinfo = SmsPayInfo.getSmsPayInfo(5, sms_msgs[0], spnumbers[0],
                                                   sms_msgs[1], spnumbers[1])
            elif sms_count == 1:
                payinfo = SmsPayInfo.getSmsPayInfo(1, sms_msgs[0], spnumbers[0])
            chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
            TyContext.ftlog.info('TuYouPayLinkYunApi _get_sms_payinfo chargeData',
                                 chargeinfo['chargeData'])
            return

        messages = []
        for i in xrange(sms_count):
            messages.append((spnumbers[i], sms_msgs[i], 1000))
        no_hint = chargeinfo.get('nohint', None)
        payinfo = SmsPayInfo.build_sms_payinfo(messages, nohint=no_hint)
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
        TyContext.ftlog.info('TuYouPayLinkYunApi _get_sms_payinfo chargeData',
                             chargeinfo['chargeData'])
        return

    @classmethod
    def doLinkYunApiCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doLinkYunApiCallback rparam', rparam)

        try:
            shortOrderPlatformId = rparam['cpparam'][2:]
            mobile = rparam['mobile']
            orderPlatformId = ShortOrderIdMap.get_long_order_id(shortOrderPlatformId)
            sign = rparam['sign']
        except:
            TyContext.ftlog.error('doLinkYunApiCallback->ERROR, param error !! rparam=', rparam)
            return 'error'

        # 签名校验
        if not cls.__verify_sign(rparam, sign):
            TyContext.ftlog.error('TuYouPayLinkYunApi.doLinkYunApiCallback verify error !!')
            return 'error'

        rparam['chargeType'] = 'linkyun.api'
        rparam['third_orderid'] = rparam['orderId']
        total_fee = float(rparam['price']) / 100
        PayHelper.set_order_mobile(orderPlatformId, mobile)
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return '0||'
        else:
            return 'error'

    @classmethod
    def __cal_mobile_sign(cls, rparam):
        check_str = (rparam['provider']
                     + rparam['channelNum']
                     + rparam['iccid']
                     + rparam['price']
                     + rparam['SHParams']
                     + rparam['ip_add']
                     + rparam['accessFlag'])
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        return digest

    @classmethod
    def __cal_telecom_sign(cls, rparam):
        check_str = (rparam['iccid']
                     + rparam['provider']
                     + rparam['price']
                     + rparam['productID']
                     + rparam['channelNum']
                     + rparam['SHParams']
                     + rparam['appKey']
                     + rparam['ip_add']
                     + rparam['accessFlag'])
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        return digest

    @classmethod
    def __cal_union_sign(cls, rparam):
        check_str = (rparam['appName']
                     + rparam['callbackData']
                     + rparam['totalFee']
                     + rparam['timeStamp']
                     + rparam['subject']
                     + rparam['outTradeNo']
                     + rparam['appKey']
                     + rparam['provider']
                     + rparam['ip_add']
                     + rparam['accessFlag'])
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        return digest

    @classmethod
    def __verify_sign(cls, rparam, sign):
        check_str = (rparam['orderId']
                     + rparam['channelId']
                     + rparam['mobile']
                     + rparam['price']
                     + rparam['cpparam']
                     + rparam['number']
                     + rparam['provider'])
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayLinkYunApi.doLinkYunApiCallback verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
