# -*- coding=utf-8 -*-

import random
from hashlib import md5

from tyframework.context import TyContext


class TuYouPayLinkYunApp():
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
        # ftlog.info("linkyun->params=",params)
        # 判断是移动
        if phoneType == 'chinaMobile':
            payCodeOne = '010'
            payCodeTwo = '020'
            payCodeThree = '050'
            orderChannel = '98'
            orderPhoneOne = '1065800810115938'
            orderPhoneTwo = '1065800810115938'
            orderPhoneThree = '1065800810115938'
            orderVerifyPhone = '1065800810125938'

        # 判断是联通
        if phoneType == 'chinaUnion':
            payCodeOne = '3#HJ182'
            payCodeTwo = '4#HJ183'
            payCodeThree = ''
            orderChannel = '98'
            orderPhoneOne = '10655556076'
            orderPhoneTwo = '10655556152'
            orderPhoneThree = ''
            orderVerifyPhone = str(random.choice(TuYouPayLinkYunApp.union_mobiles))

        # 判断是电信
        if phoneType == 'chinaTelecom':
            payCodeOne = '177#HJ486'
            payCodeTwo = '1048#HJ487'
            payCodeThree = '104#HJ488'
            orderChannel = '98'
            orderPhoneOne = '1066916531'
            orderPhoneTwo = '1066916503'
            orderPhoneThree = '1066916535'
            orderVerifyPhone = str(random.choice(TuYouPayLinkYunApp.tel_mobiles))

        if prodId == 'T20K' or prodId == 'TGBOX1' or prodId == 'COIN8':
            payCode = payCodeTwo
            orderPhone = orderPhoneTwo
        if prodId == 'T50K' or prodId == 'TGBOX2' or prodId == 'TGBOX5' or prodId == 'TGBOX6' or prodId == 'COIN7':
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

        payData = {'msgOrderCode': payCode, 'orderChannel': orderChannel, 'orderPhone': orderPhone,
                   'orderVerifyPhone': orderVerifyPhone}
        params['payData'] = payData
        mo.setResult('payData', payData)

        pass

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
        tSign = str(orderId) + str(mobileId) + str(price) + str(goodsInf) + TuYouPayLinkYunApp.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign:
            TyContext.ftlog.info('doLinkYunConfirm->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return 'N'
        else:
            # 新增对订单状态确认，避免玩家重复发同一订单的问题
            # 获取订单状态，如果订单状态大于1，则返回凌云N
            order_state = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'state')
            if order_state != None and int(order_state) > 1:
                return 'N'

            return 'Y'

        pass

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
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLinkYunCallback->ERROR, param error !! rparam=', rparam)
            return 'N'

        # 效验sign
        tSign = str(orderId) + str(mobileId) + str(price) + str(goodsInf) + TuYouPayLinkYunApp.sign_skey
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

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'
        total_fee = int(float(price) / 100)

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return '0||'
        else:
            return '1||charge fail'

        pass

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
        tSign = str(mobileId) + '#' + str(serviceid) + '#' + str(orderId) + '#' + TuYouPayLinkYunApp.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign:
            TyContext.ftlog.info('doLinkYunUnionConfirm->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return '1'
        else:
            # 新增对订单状态确认，避免玩家重复发同一订单的问题
            # 获取订单状态，如果订单状态大于1，则返回凌云N
            order_state = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'state')
            if order_state != None and int(order_state) > 1:
                return '1'

            return '0'

        pass

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
        tSign = str(mobileId) + '#' + str(serviceid) + '#' + str(msgcontent) + '#' + TuYouPayLinkYunApp.sign_skey
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

        if msgcontent == '0:0':
            from tysdk.entity.pay.pay import TuyouPay
            trade_status = 'TRADE_FINISHED'
            TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)

        return '0'

        pass
