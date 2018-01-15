# -*- coding=utf-8 -*-

import random

from constants import PHONETYPE_CHINAUNION, PHONETYPE_CHINATELECOM
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay3.constants import PayConst


class TuYouPayLinkYun():
    # 订单签名验证key
    sign_skey = 'lywuxian'

    union_mobiles = [13010112500, 13010314500, 13010888500, 13010171500, 13010341500, 13010360500, 13010380500,
                     13010811500, 13010831500, 13010180500]
    tel_mobiles = [13800100500, 13800210500, 13800220500, 13800230500, 13800451500, 13800240500, 13800311500,
                   13800351500, 13800531500, 13800250500]

    @classmethod
    def charge_data(cls, chargeinfo):
        diamondId = chargeinfo['buttonId']
        orderPlatformId = chargeinfo['platformOrderId']

        payCodeOne = '010'
        payCodeTwo = '020'
        payCodeFive = '050'
        payCodeEight = '080'
        payCodeTen = '100'

        orderChannel = '98'

        orderPhoneOne = '1065800810025938'
        orderPhoneTwo = '1065800810025938'
        orderPhoneFive = '1065800810025938'
        orderPhoneEight = '1065800810025938'
        orderPhoneTen = '1065800810025938'

        orderVerifyPhone = '1065800810025938'
        orderVerifyPhone2 = '1065800810025938'

        # 判断是联通
        phoneType = chargeinfo['phoneType']
        if phoneType == PHONETYPE_CHINAUNION:
            payCodeOne = '3#HJ182'
            payCodeTwo = '4#HJ183'
            payCodeFive = ''
            orderChannel = '98'
            orderPhoneOne = '10655556076'
            orderPhoneTwo = '10655556152'
            orderPhoneFive = ''
            orderVerifyPhone = str(random.choice(cls.union_mobiles))

        # 判断是电信
        if phoneType == PHONETYPE_CHINATELECOM:
            payCodeOne = '177#HJ486'
            payCodeTwo = '1048#HJ487'
            payCodeFive = '104#HJ488'
            orderChannel = '98'
            orderPhoneOne = '1066916531'
            orderPhoneTwo = '1066916503'
            orderPhoneFive = '1066916535'
            orderVerifyPhone = str(random.choice(cls.tel_mobiles))

        if diamondId == 'D20' or diamondId == 'TY0006D0000202':
            payCode = payCodeTwo
            orderPhone = orderPhoneTwo
        if diamondId == 'D50':
            payCode = payCodeFive
            orderPhone = orderPhoneFive
        if diamondId == 'TY9999R0008001':
            payCode = payCodeEight
            orderPhone = orderPhoneEight
            orderVerifyPhone = orderVerifyPhone2

        smsMsg = payCode + '#' + orderChannel + orderPlatformId
        smsPayinfo = cls.__get_smspayinfo(3, smsMsg, orderPhone, orderVerifyPhone)
        chargeinfo['chargeData'] = {
            'need_short_order_id': 1, 'issms': 1, 'msgOrderCode': payCode,
            'orderChannel': orderChannel, 'orderPhone': orderPhone,
            'orderVerifyPhone': orderVerifyPhone, 'smsNewPay': smsPayinfo}

    @classmethod
    def __get_smspayinfo(cls, smsType, smsMsg, smsPort, smsVerifyPort):
        # type是短信支付的方式，2代表的是发两条同样短信内容发不同端口号支付
        smsPayinfo = {'type': str(smsType), 'smsMsg': smsMsg, 'smsPort': str(smsPort),
                      'smsVerifyPort': str(smsVerifyPort)}
        return smsPayinfo

    @classmethod
    def doLinkYunConfirm(cls, rpath):
        rparam = PayHelper.getArgsDict()
        TyContext.ftlog.info('doLinkYunConfirm->args=', rparam)
        try:
            orderId = rparam['orderId']
            mobileId = rparam['mobileId']
            price = rparam['price']
            goodsInf = rparam['goodsInf']
            sign = rparam['sign']
            # 效验sign
            isOk = PayHelper.verify_md5(sign, orderId, mobileId, price, goodsInf, cls.sign_skey)
            if isOk:
                orderPlatformId = str(goodsInf)[2:]
                orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
                TyContext.RunMode.get_server_link(orderPlatformId)
                order_state = TyContext.RedisPayData.execute('HGET', 'sdk.charge:' + str(orderPlatformId), 'state')
                if order_state != None and int(order_state) >= PayConst.CHARGE_STATE_BEGIN and int(
                        order_state) < PayConst.CHARGE_STATE_DONE:
                    return 'Y'
                return 'N'
            else:
                TyContext.ftlog.error('doLinkYunConfirm->ERROR, sign error !! ')
                return 'N'
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.error('doLinkYunConfirm->ERROR, exception error !! ', rparam)
            return 'N'

    @classmethod
    def doLinkYunCallback(cls, rpath):
        rparam = PayHelper.getArgsDict()
        TyContext.ftlog.info('doLinkYunCallback->args=', rparam)
        try:
            orderId = rparam['orderId']
            mobileId = rparam['mobileId']
            price = rparam['price']
            goodsInf = rparam['goodsInf']
            sign = rparam['sign']
            isOk = PayHelper.verify_md5(sign, orderId, mobileId, price, goodsInf, cls.sign_skey)
            # 效验sign
            if not isOk:
                TyContext.ftlog.info('doLinkYunCallback->ERROR, sign error !!')
                return '1||sign error'

            platformOrderId = str(goodsInf)[2:]
            if not platformOrderId:
                TyContext.ftlog.info('doLinkYunCallback->ERROR, platformOrderId error !!')
                return '1||orderPlatformId error'

            # 对凌云充值的订单，把手机号补充到订单信息里
            platformOrderId = ShortOrderIdMap.get_long_order_id(platformOrderId)
            TyContext.RunMode.get_server_link(platformOrderId)
            PayHelper.set_order_mobile(platformOrderId, mobileId)

            rparam['chargeType'] = 'linkyun'
            rparam['third_orderid'] = orderId
            total_fee = float(price) / 100
            isOk = PayHelper.callback_ok(platformOrderId, total_fee, rparam)
            if isOk:
                return '0||'
            else:
                return '1||charge fail'
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLinkYunCallback->ERROR, param error !! rparam=', rparam)
            return '1||charge exception'
