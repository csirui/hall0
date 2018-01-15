# -*- coding=utf-8 -*-

from hashlib import md5

from constants import PHONETYPE_CHINAMOBILE, PHONETYPE_CHINAUNION
from tyframework.context import TyContext
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay_common.clientrevision import ClientRevision


class TuYouPayEftApi(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        userId = chargeinfo['uid']
        appId = chargeinfo['appId']
        phoneType = TyContext.UserSession.get_phone_type_name(chargeinfo['phoneType'])
        price = int(float(chargeinfo['chargeTotal']))
        platformOrderId = chargeinfo['platformOrderId']

        response = cls.__create_order(phoneType, userId, price, platformOrderId)
        if not response:
            return
        if str(response[0]) != '000':
            TyContext.ftlog.error('TuYouPayEftApi create_order failed for user', userId,
                                  'orderid', platformOrderId, 'response', response)
            return
        spnumber = str(response[2])
        sms_msg = str(response[3])

        if not ClientRevision(userId).support_type0_smspayinfo:
            payinfo = SmsPayInfo.getSmsPayInfo(1, sms_msg, spnumber)
            chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
            return

        messages = []
        messages.append((spnumber, sms_msg, 0))
        payinfo = SmsPayInfo.build_sms_payinfo(messages)
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}

    @classmethod
    def __create_order(cls, phoneType, userId, amount, orderPlatformId):
        eft_config = TyContext.Configure.get_global_item_json('eftapi_config', {})
        keywords = str(eft_config['KeyWords'])
        paykey = str(eft_config['paykey'])
        createorder_url = str(eft_config['createorder_url'])
        paykey = str(eft_config['paykey'])
        yd_support_fee = eft_config['yd_support_fee']
        lt_support_fee = eft_config['lt_support_fee']
        dx_support_fee = eft_config['dx_support_fee']
        params = {}
        if phoneType == PHONETYPE_CHINAMOBILE:
            params['MobileType'] = 'YD'
            if amount not in yd_support_fee:
                return None
        elif phoneType == PHONETYPE_CHINAUNION:
            params['MobileType'] = 'LT'
            if amount not in lt_support_fee:
                return None
        else:
            params['MobileType'] = 'DX'
            if amount not in dx_support_fee:
                return None

        params['OrderId'] = keywords + orderPlatformId
        params['Fee'] = str(amount)
        params['UserId'] = str(userId)
        params['KeyWords'] = keywords
        params['sign'] = cls.__cal_sign(params, paykey)
        response_msg, final_url = TyContext.WebPage.webget(createorder_url, params)

        response = response_msg.split('~')
        return response

    @classmethod
    def doEftApiCallback(cls, rpath):

        return None

    @classmethod
    def __cal_sign(cls, rparam, paykey):
        check_str = (rparam['OrderId']
                     + rparam['KeyWords']
                     + rparam['Fee']
                     + rparam['MobileType']
                     + rparam['UserId']
                     + paykey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        return digest
