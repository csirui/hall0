# -*- coding=utf-8 -*-

import datetime
import json

from rsacrypto import rsaSign, rsaVerify
from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class TuyouPayHuafubao():
    RET_MSG = '''<META NAME="MobilePayPlatform" CONTENT ="%s">'''
    notify_url = "/v1/pay/huafubao/callback";

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        payCode = '060'
        if prodId == 'MOONKEY':
            payCode = '021'
        if prodId == 'T60K':
            payCode = '060'
        if prodId == 'ZHUANYUN_6':
            payCode = '061'
        if prodId == 'RAFFLE_NEW':
            payCode = '080'
        if prodId == 'T100K':
            payCode = '100'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)

        pass

    @classmethod
    def __get_order_info__(self, orderPlatformId):
        orderinfo = None
        try:
            if orderPlatformId != '':
                baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId),
                                                          'PAY_STATE_IDEL')
                if baseinfo != None:
                    orderinfo = json.loads(baseinfo)
        except:
            TyContext.ftlog.exception()

        return orderinfo

    @classmethod
    def doHuafubaoGetOrder(self, rpath):
        httpdomain = PayHelper.getSdkDomain()
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = ''
        notify_url = httpdomain + TuyouPayHuafubao.notify_url
        merId = ''
        goodsId = ''
        amout = 0
        merDate = datetime.datetime.now().strftime('%Y%m%d')
        version = ''
        sign = ''
        try:
            merId = rparam['merId']
            goodsId = rparam['goodsId']
            goodsInf = rparam['goodsInf']
            orderPlatformId = str(goodsInf).split('#')[2]
            amtType = rparam['amtType']
            bankType = rparam['bankType']
            mobileId = rparam['mobileId']
            version = rparam['version']
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doHuafubaoGetOrder->ERROR, param error !! rparam=', rparam)
            retContent = merId + '|' + goodsId + '|' + orderPlatformId + '|' + merDate + '|' + str(
                amout) + '||||' + '0002|fail|' + version
            ret_sign = rsaSign(retContent, 'huafubao')
            retContent = retContent + '|' + ret_sign
            retMsg = TuyouPayHuafubao.RET_MSG % (retContent)
            return retMsg

        TyContext.RunMode.get_server_link(orderPlatformId)
        orderinfo = self.__get_order_info__(orderPlatformId)
        # ftlog.info('doHuafubaoGetOrder->orderinfo=',orderinfo,'orderPlatformId=',orderPlatformId)
        if orderinfo != None:
            amout = int(orderinfo['orderPrice']) * 100
        else:
            TyContext.ftlog.info('doHuafubaoGetOrder->ERROR, param error !! rparam=', rparam)
            retContent = merId + '|' + goodsId + '|' + orderPlatformId + '|' + merDate + '|' + str(
                amout) + '||||' + '0002|fail|' + version
            ret_sign = rsaSign(retContent, 'huafubao')
            retContent = retContent + '|' + ret_sign
            retMsg = TuyouPayHuafubao.RET_MSG % (retContent)
            return retMsg

        # merId=9996&goodsId=100&orderId=133819&merDate=20090402&payDate=20090402&amount=1000&amtType=02&bankType=3&mobileId=13426399070&transType=0&settleDate=20090403&merPriv=&retCode=0000&version=3.0

        baseString = 'merId=' + merId + '&goodsId=' + goodsId + '&goodsInf=' + goodsInf + '&mobileId=' + mobileId + \
                     '&amtType=' + amtType + '&bankType=' + bankType + '&version=' + version

        # python 底层有BUG，将+号转换为空格了
        sign = sign.replace(' ', '+')
        # 签名校验
        if rsaVerify(baseString, sign, 'huafubao') != True:
            TyContext.ftlog.info('doHuafubaoGetOrder->ERROR, sign error !! sign=', sign)
            retContent = merId + '|' + goodsId + '|' + orderPlatformId + '|' + merDate + '|' + str(
                amout) + '||||' + '0002|fail|' + version
        else:
            retContent = merId + '|' + goodsId + '|' + orderPlatformId + '|' + merDate + '|' + str(
                amout) + '||||' + '0000|success|' + version

        ret_sign = rsaSign(retContent, 'huafubao')
        retContent = retContent + '|' + ret_sign
        retMsg = TuyouPayHuafubao.RET_MSG % (retContent)

        return retMsg

    @classmethod
    def doHuafubaoCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = ''
        try:
            merId = rparam['merId']
            goodsId = rparam['goodsId']
            orderPlatformId = rparam['orderId']
            merDate = rparam['merDate']
            payDate = rparam['payDate']
            amount = rparam['amount']
            amtType = rparam['amtType']
            bankType = rparam['bankType']
            mobileId = rparam['mobileId']
            transType = rparam['transType']
            settleDate = rparam['settleDate']
            merPriv = rparam['merPriv']
            retCode = rparam['retCode']
            version = rparam['version']
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doHuafubaoCallback->ERROR, param error !! rparam=', rparam)
            retContent = merId + '|' + goodsId + '|' + orderPlatformId + '|' + merDate + '|' + '1111|fail|' + version
            ret_sign = rsaSign(retContent, 'huafubao')
            retContent = retContent + '|' + ret_sign
            retMsg = TuyouPayHuafubao.RET_MSG % (retContent)
            return retMsg

        # merId=9996&goodsId=100&orderId=133819&merDate=20090402&payDate=20090402&amount=1000&amtType=02&bankType=3&mobileId=13426399070&transType=0&settleDate=20090403&merPriv=&retCode=0000&version=3.0

        baseString = 'merId=' + merId + '&goodsId=' + goodsId + '&orderId=' + orderPlatformId + '&merDate=' + merDate + '&payDate=' + payDate + '&amount=' + str(
            amount) + \
                     '&amtType=' + amtType + '&bankType=' + bankType + '&mobileId=' + mobileId + '&transType=' + transType + '&settleDate=' + settleDate + '&merPriv=' + merPriv + '&retCode=' + retCode + '&version=' + version

        # 签名校验
        if rsaVerify(baseString, sign, 'huafubao') != True:
            TyContext.ftlog.info('doHuafubaoCallback->ERROR, sign error !! sign=', sign)
            retContent = merId + '|' + goodsId + '|' + orderPlatformId + '|' + merDate + '|' + '1111|fail|' + version
            ret_sign = rsaSign(retContent, 'huafubao')
            retContent = retContent + '|' + ret_sign
            retMsg = TuyouPayHuafubao.RET_MSG % (retContent)
            return retMsg

        from tysdk.entity.pay.pay import TuyouPay
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', rparam)
        if isOk:
            retContent = merId + '|' + goodsId + '|' + orderPlatformId + '|' + merDate + '|' + '0000|success|' + version
        else:
            retContent = merId + '|' + goodsId + '|' + orderPlatformId + '|' + merDate + '|' + '1111|fail|' + version

        ret_sign = rsaSign(retContent, 'huafubao')
        retContent = retContent + '|' + ret_sign
        retMsg = TuyouPayHuafubao.RET_MSG % (retContent)
        # ftlog.info('doHuafubaoCallback->retMsg, retMsg=', retMsg)
        return retMsg
