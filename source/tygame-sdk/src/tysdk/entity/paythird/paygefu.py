# -*- coding=utf-8 -*-

import json
import time
from hashlib import md5

from datetime import datetime

from constants import PHONETYPE_INTS
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay_common.clientrevision import ClientRevision


class TuYouPayGeFu(object):
    thirdPartyId = '32'

    @classmethod
    def charge_data(cls, chargeinfo):

        userId = chargeinfo['uid']
        price = int(float(chargeinfo['chargeTotal'])) * 100
        platformOrderId = chargeinfo['platformOrderId']
        productDesc = chargeinfo['buttonName']

        appid = chargeinfo['appId']
        productName = '途游斗地主'

        phoneType = TyContext.UserSession.get_phone_type_name(chargeinfo['phoneType'])
        gefuconfig = TyContext.Configure.get_global_item_json('gefupay_config', {})
        if gefuconfig:
            cls.createorder_url = gefuconfig[cls.thirdPartyId][phoneType]

        response = cls._create_order(phoneType, userId, price, platformOrderId, productName, productDesc)
        status = response['code']
        if int(status) != 200:
            TyContext.ftlog.error('TuYouGeFuPay create_order failed for user', userId,
                                  'reason', response['reason'])
            return

        spnumber, sms_msg = response['sms_port'], response['sms']
        if not ClientRevision(userId).support_type0_smspayinfo:
            payinfo = SmsPayInfo.getSmsPayInfo(1, sms_msg, spnumber)
            chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
            return

        messages = [(spnumber, sms_msg, 0)]
        no_hint = chargeinfo.get('nohint', None)
        payinfo = SmsPayInfo.build_sms_payinfo(messages, nohint=no_hint)
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}

    @classmethod
    def _create_order(cls, phoneType, userId, price, orderPlatformId, productName, productDesc):
        iccid = TyContext.UserSession.get_session_iccid(userId)
        imei = TyContext.UserSession.get_session_imei(userId)
        gefuconfig = TyContext.Configure.get_global_item_json('gefupay_config', {})
        md5key = gefuconfig[cls.thirdPartyId]['md5key']

        params = {}
        params['orderNo'] = orderPlatformId
        params['thirdPartyId'] = cls.thirdPartyId
        params['fee'] = price
        params['spType'] = PHONETYPE_INTS[phoneType] + 1
        datestr = datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
        params['reqTime'] = datestr
        # params['mobileImsi'] = ''

        if not iccid:
            params['mobileICCID'] = 0
        else:

            params['mobileICCID'] = iccid
        # params['deviceModel'] = ''
        params['deviceId'] = imei
        params['productName'] = productName
        params['productDesc'] = productDesc
        params['sign'] = cls._cal_sign(params, md5key)
        response_msg, _ = TyContext.WebPage.webget(cls.createorder_url, params, method_='GET')
        response = json.loads(response_msg)
        return response

    @classmethod
    def doGeFuPayCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doGeFuPayCallback->rparam', rparam)
        try:
            orderPlatformId = rparam['orderno']
            total_fee = float(rparam['fee']) / 100
            reqTime = rparam['reqtime']
            status = rparam['status']
            mobileId = rparam.get('mobilenum')
            sign = rparam['sign']

        except Exception as e:
            TyContext.ftlog.error('doGeFuPayCallback->ERROR, exception', e, 'rparam', rparam)
            return 'error'

        pathType = TyContext.RunHttp.get_request_path()
        chargeType = pathType.find('gefusdk')
        if chargeType != -1:
            thirdPartyId = '43'
            rparam['chargeType'] = 'gefusdk'
        else:
            thirdPartyId = '32'
            rparam['chargeType'] = 'gefu'

        gefuconfig = TyContext.Configure.get_global_item_json('gefupay_config', {})
        md5key = gefuconfig[thirdPartyId]['md5key']
        paramsIn = rparam['fee'] + rparam['orderno'] + rparam['reqtime']
        if not cls._verify_sign(paramsIn, sign, md5key):
            TyContext.ftlog.error('do_gefupay_callback->ERROR  invalid sign', sign)
            return 'error'

        PayHelper.set_order_mobile(orderPlatformId, mobileId)
        if status == 'success':
            PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
            return 'success'

        errinfo = '支付失败'
        PayHelper.callback_error(orderPlatformId, errinfo, rparam)
        return 'failed'

    @classmethod
    def _cal_sign(cls, params, md5key):
        check_str = ''.join([str(params[k]) for k in sorted(params.keys()) if k != 'sign'])
        m = md5()
        m.update(check_str + md5key)
        digest = m.hexdigest().lower()
        return digest

    @classmethod
    def _verify_sign(cls, paramsIn, sign, md5key):
        m = md5()
        m.update(paramsIn + md5key)
        digest = m.hexdigest().upper()
        if digest != sign:
            TyContext.ftlog.error('TuYouGeFuPay verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', paramsIn)
            return False
        return True
