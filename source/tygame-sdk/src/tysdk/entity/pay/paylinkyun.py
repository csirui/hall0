# -*- coding=utf-8 -*-

import json
import random
from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.pay.pay import TuyouPay
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap


class TuYouPayLinkYun():
    # 订单签名验证key
    sign_skey = 'lywuxian'
    union_mobiles = [13010112500, 13010314500, 13010888500, 13010171500, 13010341500, 13010360500, 13010380500,
                     13010811500, 13010831500, 13010180500]
    tel_mobiles = [13800100500, 13800210500, 13800220500, 13800230500, 13800451500, 13800240500, 13800311500,
                   13800351500, 13800531500, 13800250500]

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        appId = params['appId']
        prodId = params['prodId']
        phoneType = params['phoneType']
        # TyContext.ftlog.info("linkyun->params=",params)
        # 判断是移动, 缺省为移动
        # if phoneType == 'chinaMobile':
        payCodeOne = '010'
        payCodeTwo = '020'
        payCodeThree = '050'
        # payCodeFour = '081'
        payCodeFour = '080'
        payCodeFive = '100'
        orderChannel = '98'

        orderPhoneOne = '1065800810025938'
        orderPhoneTwo = '1065800810025938'
        orderPhoneThree = '1065800810025938'
        orderPhoneFour = '1065800810025938'
        orderPhoneFive = '1065800810025938'
        orderVerifyPhone = '1065800810025938'
        orderVerifyPhone2 = '1065800810025938'
        '''
        orderPhoneOne = '1065800810115938'
        orderPhoneTwo = '1065800810115938'
        orderPhoneThree = '1065800810115938'
        orderPhoneFour = '1065800810113130'
        orderVerifyPhone = '1065800810125938'
        orderVerifyPhone2 = '1065800810123130'
        '''
        # 判断是联通
        if phoneType == 'chinaUnion':
            payCodeOne = '3#HJ182'
            payCodeTwo = '4#HJ183'
            payCodeThree = ''
            orderChannel = '98'
            orderPhoneOne = '10655556076'
            orderPhoneTwo = '10655556152'
            orderPhoneThree = ''
            orderVerifyPhone = str(random.choice(TuYouPayLinkYun.union_mobiles))

        # 判断是电信
        if phoneType == 'chinaTelecom':
            payCodeOne = '177#HJ486'
            payCodeTwo = '1048#HJ487'
            payCodeThree = '104#HJ488'
            orderChannel = '98'
            orderPhoneOne = '1066916531'
            orderPhoneTwo = '1066916503'
            orderPhoneThree = '1066916535'
            orderVerifyPhone = str(random.choice(TuYouPayLinkYun.tel_mobiles))

        payCode = payCodeThree
        orderPhone = orderPhoneThree
        if prodId == 'T20K' or prodId == 'CARDMATCH10' or prodId == 'TGBOX1' or prodId == 'T3_NS_COIN_2' or prodId == 'COIN8' or prodId == 'TEXAS_COIN1' or prodId == 'C2':
            payCode = payCodeTwo
            orderPhone = orderPhoneTwo
        if prodId == 'T50K' or prodId == 'TGBOX2' or prodId == 'RAFFLE_5' or prodId == 'T3_NS_COIN_5' or prodId == 'COIN7' or prodId == 'C5' or prodId == 'C5_LUCKY' or prodId == 'TEXAS_COIN6' or prodId == 'diamond5':
            payCode = payCodeThree
            orderPhone = orderPhoneThree
        if prodId == 'MOONKEY':
            payCode = payCodeTwo
            orderPhone = orderPhoneTwo
        if prodId == 'MOONKEY3':
            payCode = payCodeThree
            orderPhone = orderPhoneThree
        if prodId == 'VOICE100':
            payCode = payCodeOne
            orderPhone = orderPhoneOne
        if prodId == 'RAFFLE' and str(appId) == '6':
            payCode = payCodeThree
            orderPhone = orderPhoneThree
        if prodId == 'RAFFLE' and str(appId) != '6':
            payCode = payCodeTwo
            orderPhone = orderPhoneTwo

        if prodId == 'RAFFLE_NEW' or prodId == 'T80K' or prodId == 'ZHUANYUN_MEZZO' or prodId == 'C8' or prodId == 'C8_RAFFLE' or prodId == 'C8_LUCKY' or prodId == 'TEXAS_COIN_R8' or prodId == 'TEXAS_COIN_LUCKY_R8' or prodId == 'TGBOX9' or prodId == 'RAFFLE_8' or prodId == 'ZHUANYUN_8':
            payCode = payCodeFour
            orderPhone = orderPhoneFour
            orderVerifyPhone = orderVerifyPhone2
        if prodId == 'T100K' or prodId == 'C10' or prodId == 'TEXAS_COIN2':
            payCode = payCodeFive
            orderPhone = orderPhoneFive

        payData = {'msgOrderCode': payCode, 'orderChannel': orderChannel, 'orderPhone': orderPhone,
                   'orderVerifyPhone': orderVerifyPhone}
        params['payData'] = payData
        mo.setResult('payData', payData)
        mo.setResult('orderPlatformId', ShortOrderIdMap.get_short_order_id(params['orderPlatformId']))

    @classmethod
    def doBuyStraightLtsdk(self, userId, params, mo):

        mo.setResult('orderPlatformId', ShortOrderIdMap.get_short_order_id(params['orderPlatformId']))

    @classmethod
    def doBuyStraightDx(self, userId, params, mo):
        appId = params['appId']
        prodId = params['prodId']
        phoneType = params['phoneType']

        payCodeOne = 'w01d10c'
        payCodeTwo = 'a02d10c'
        payCodeFive = 'f05d10c'
        payCodeSix = '106d10c'
        payCodeEight = '808d10c'
        payCodeTen = '910d10c'
        orderChannel = '98'
        # 1、2、5元端口
        orderPhoneOne = '10661025'
        # 6元端口
        orderPhoneTwo = '106598725'
        # 8元端口
        orderPhoneThree = '1065987215'
        # 10元端口
        orderPhoneFour = '1065987216'

        payCode = payCodeFive
        if prodId == 'T20K' or prodId == 'CARDMATCH10' or prodId == 'TGBOX1' or prodId == 'T3_NS_COIN_2' or prodId == 'COIN8' or prodId == 'TEXAS_COIN1' or prodId == 'C2':
            payCode = payCodeTwo
            orderPhone = orderPhoneOne
        if prodId == 'T50K' or prodId == 'TGBOX2' or prodId == 'T3_NS_COIN_5' or prodId == 'COIN7' or prodId == 'C5' or prodId == 'C5_LUCKY' or prodId == 'TEXAS_COIN6' or prodId == 'diamond5':
            payCode = payCodeFive
            orderPhone = orderPhoneOne
        if prodId == 'MOONKEY':
            payCode = payCodeTwo
            orderPhone = orderPhoneOne
        if prodId == 'MOONKEY3':
            payCode = payCodeFive
            orderPhone = orderPhoneOne
        if prodId == 'VOICE100':
            payCode = payCodeOne
            orderPhone = orderPhoneOne
        if prodId == 'RAFFLE' and str(appId) == '6':
            payCode = payCodeFive
            orderPhone = orderPhoneOne
        if prodId == 'RAFFLE' and str(appId) != '6':
            payCode = payCodeTwo
            orderPhone = orderPhoneOne

        if prodId == 'T60K' or prodId == 'ZHUANYUN_6' or prodId == 'RAFFLE_6' or prodId == 'TEXAS_COIN_R6' or prodId == 'TEXAS_COIN_LUCKY_R6' or prodId == 'C6' or prodId == 'C6_RAFFLE':
            payCode = payCodeSix
            orderPhone = orderPhoneTwo

        if prodId == 'RAFFLE_NEW' or prodId == 'T80K' or prodId == 'ZHUANYUN_MEZZO' or prodId == 'C8' or prodId == 'C8_RAFFLE' or prodId == 'C8_LUCKY' or prodId == 'TEXAS_COIN_R8' or prodId == 'TEXAS_COIN_LUCKY_R8' or prodId == 'TGBOX9' or prodId == 'RAFFLE_8' or prodId == 'ZHUANYUN_8':
            payCode = payCodeEight
            orderPhone = orderPhoneThree

        if prodId == 'T100K' or prodId == 'C10' or prodId == 'TEXAS_COIN2':
            payCode = payCodeTen
            orderPhone = orderPhoneFour

        payData = {'msgOrderCode': payCode, 'orderChannel': orderChannel, 'orderPhone': orderPhone}
        params['payData'] = payData
        mo.setResult('payData', payData)
        mo.setResult('orderPlatformId', ShortOrderIdMap.get_short_order_id(params['orderPlatformId']))

    @classmethod
    def __get_order_appId__(self, orderPlatformId):
        baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'PAY_STATE_IDEL')
        baseinfo = json.loads(baseinfo)
        appId = baseinfo['appId']
        if appId != None and appId != '':
            return appId
        else:
            return '0'

    @classmethod
    def __set_order_mobile__(self, orderPlatformId, mobile):
        try:
            if mobile != '':
                baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId),
                                                          'PAY_STATE_CHARGE')
                baseinfo = json.loads(baseinfo)
                baseinfo['vouchMobile'] = mobile
                TyContext.RedisPayData.execute('HSET', 'platformOrder:' + str(orderPlatformId), 'PAY_STATE_CHARGE',
                                               json.dumps(baseinfo))
        except:
            TyContext.ftlog.info('linkYunCallback->set mobile error', 'orderPlatformId=', orderPlatformId, 'mobile=',
                                 mobile)

    @classmethod
    def createLinkString(self, rparam):

        sk = rparam.keys()
        ret = ""
        for k in sk:
            ret = ret + str(k) + '=' + str(rparam[k]) + '&'
        return ret[:-1]

    # 凌云移动回调
    @classmethod
    def doLinkYunConfirm(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderId = rparam['orderId']
            mobileId = rparam['mobileId']
            # productCode = rparam['productCode']
            price = rparam['price']
            goodsInf = rparam['goodsInf']
            orderPlatformId = str(goodsInf)[2:]
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLinkYunConfirm->ERROR, param error !! rparam=', rparam)
            return 'N'
        # 效验sign
        tSign = str(orderId) + str(mobileId) + str(price) + str(goodsInf) + TuYouPayLinkYun.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign:
            TyContext.ftlog.info('doLinkYunConfirm->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return 'N'
        else:
            orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
            TyContext.RunMode.get_server_link(orderPlatformId)
            # 新增对订单状态确认，避免玩家重复发同一订单的问题
            # 获取订单状态，如果订单状态大于1，则返回凌云N
            order_state = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'state')
            if order_state != None and int(order_state) > 1:
                return 'N'
            return 'Y'

    # 凌云移动回调
    @classmethod
    def doLinkYunCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = ''
        try:
            orderId = rparam['orderId']
            mobileId = rparam['mobileId']
            # productCode = rparam['productCode']
            price = rparam['price']
            goodsInf = rparam['goodsInf']
            orderPlatformId = str(goodsInf)[2:]
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doLinkYunCallback->ERROR, param error !! rparam=', rparam)
            return '1||param error'

        # 效验sign
        tSign = str(orderId) + str(mobileId) + str(price) + str(goodsInf) + TuYouPayLinkYun.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign:
            TyContext.ftlog.info('doLinkYunCallback->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '1||sign error'
        if orderPlatformId == '':
            TyContext.ftlog.info('doLinkYunCallback->ERROR, orderPlatformId error !! orderPlatformId=', orderPlatformId,
                                 'goodsInf=', goodsInf)
            return '1||orderPlatformId error'

        orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
        TyContext.RunMode.get_server_link(orderPlatformId)

        # 对凌云充值的订单，把手机号补充到订单信息里
        self.__set_order_mobile__(orderPlatformId, mobileId)

        rparam['third_orderid'] = orderId
        total_fee = int(float(price) / 100)
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, 'TRADE_FINISHED', rparam)
        if isOk:
            return '0||'
        else:
            return '1||charge fail'

    # 凌云联通、电信共用的回调
    @classmethod
    def doLinkYunUnionConfirm(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            mobileId = rparam['mobile']
            serviceid = rparam['serviceid']
            orderId = rparam['orderid']
            orderPlatformId = str(rparam['orderid'])[2:]
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLinkYunUnionConfirm->ERROR, param error !! rparam=', rparam)
            return '1'

        # 效验sign=mobile#serviceid#orderid#密钥
        tSign = str(mobileId) + '#' + str(serviceid) + '#' + str(orderId) + '#' + TuYouPayLinkYun.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign:
            TyContext.ftlog.info('doLinkYunUnionConfirm->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '1'
        else:
            # 新增对订单状态确认，避免玩家重复发同一订单的问题
            # 获取订单状态，如果订单状态大于1，则返回凌云N
            orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
            TyContext.RunMode.get_server_link(orderPlatformId)
            order_state = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'state')
            if order_state != None and int(order_state) > 1:
                return '1'

            return '0'

    # 凌云联通、电信共用的回调
    @classmethod
    def doLinkYunUnionCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = ''
        try:
            mobileId = rparam['mobile']
            serviceid = rparam['serviceid']
            orderPlatformId = str(rparam['orderid'])[2:]
            msgcontent = rparam['msgcontent']
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLinkYunUnionCallback->ERROR, param error !! rparam=', rparam)
            return '0'

        # 效验sign
        tSign = str(mobileId) + '#' + str(serviceid) + '#' + str(msgcontent) + '#' + TuYouPayLinkYun.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign:
            TyContext.ftlog.info('doLinkYunUnionCallback->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '0'
        if orderPlatformId == '':
            TyContext.ftlog.info('doLinkYunUnionCallback->ERROR, orderPlatformId error !! orderPlatformId=',
                                 orderPlatformId)
            return '0'

        orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
        TyContext.RunMode.get_server_link(orderPlatformId)

        # 对凌云充值的订单，把手机号补充到订单信息里
        self.__set_order_mobile__(orderPlatformId, mobileId)

        if msgcontent == '0:0':
            TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', rparam)

        return '0'

    @classmethod
    def doLinkYunLtsdkCallback(self, rpath):
        clientIp = TyContext.RunHttp.get_client_ip()
        TyContext.ftlog.info('doLinkYunLtsdkCallback in clientIp=', clientIp)
        '''
        if not clientIp in ('219.238.157.144','125.39.218.102'):
            return '1'
        '''
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = ''
        try:
            mobileId = rparam['mobile']
            transactionId = rparam['transactionId']
            orderPlatformId = rparam['outTradeNo']
            status = rparam['status']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLinkYunLtsdkCallback->ERROR, param error !! rparam=', rparam)
            return '1'

        if orderPlatformId == '':
            TyContext.ftlog.info('doLinkYunLtsdkCallback->ERROR, orderPlatformId error !! orderPlatformId=',
                                 orderPlatformId)
            return '1'

        orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
        TyContext.RunMode.get_server_link(orderPlatformId)

        # 对凌云充值的订单，把手机号补充到订单信息里
        self.__set_order_mobile__(orderPlatformId, mobileId)

        if int(status) == 4:
            TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', rparam)

        return '0'

    @classmethod
    def doLinkYunDxCallback(self, rpath):
        clientIp = TyContext.RunHttp.get_client_ip()
        TyContext.ftlog.info('doLinkYunDxCallback in clientIp=', clientIp)
        '''
        if not clientIp in ('219.238.157.144','125.39.218.102'):
            return '1'
        '''
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = ''
        try:
            mobileId = rparam['mobile']
            orderPlatformId = str(rparam['passwd'])[-6:]
            status = rparam['msg']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLinkYunDxCallback->ERROR, param error !! rparam=', rparam)
            return '1'

        if orderPlatformId == '':
            TyContext.ftlog.info('doLinkYunDxCallback->ERROR, orderPlatformId error !! rparam=', rparam)
            return '1'

        orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
        TyContext.RunMode.get_server_link(orderPlatformId)

        # 对凌云充值的订单，把手机号补充到订单信息里
        self.__set_order_mobile__(orderPlatformId, mobileId)

        if str(status) == 'DELIVRD':
            TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', rparam)
        return '0'
