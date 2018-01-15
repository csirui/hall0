# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

import datetime

from constants import PAY_STATE_CHARGE
from tyframework.context import TyContext
from tysdk.entity.paythird.payios import is_sandbox_receipt

_IOS_CALL_COUNT_ = 0


class TuYouPayIos(object):
    @classmethod
    def doIosCallback(cls, rpath):
        global _IOS_CALL_COUNT_
        _IOS_CALL_COUNT_ = _IOS_CALL_COUNT_ + 1
        ct = datetime.datetime.now()
        ioskey = ct.strftime('ios-%Y%m%d%H%M%S-') + str(_IOS_CALL_COUNT_)

        iosOrderId = TyContext.RunHttp.getRequestParam('iosOrderId', '')
        TyContext.RunMode.get_server_link(iosOrderId)

        authInfo = TyContext.RunHttp.getRequestParam('authInfo')
        userId, userName, userTime = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        if userId <= 0:
            TyContext.ftlog.error('IOS->doIosCallback authInfo error')
            return 'error-authInfo'

        TyContext.ftlog.info('IOS->doIosCallback ioskey=', ioskey, 'userId=', userId, 'userName=', userName,
                             'userTime=', userTime)
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        if appId < 0:
            TyContext.ftlog.error('IOS->doIosCallback appId error')
            return 'error-appId'

        receipt = TyContext.RunHttp.getRequestParam('receipt', '')
        TyContext.ftlog.info('IOS->doIosCallback ioskey=', ioskey, 'receipt=', receipt)
        if not receipt or len(receipt) < 200:
            TyContext.ftlog.error('IOS->doIosCallback receipt error')
            return 'error-receipt'

        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        if clientId == '':
            clientId = TyContext.RunHttp.getRequestParam('clientID', '')

        appInfo = TyContext.RunHttp.getRequestParam('appInfo', '')
        raffle = TyContext.RunHttp.getRequestParamInt('raffle', 0)
        paydata = {}
        paydata['receiptJsonStr'] = '{"receipt-data" : "' + receipt + '"}'
        paydata['iosOrderId'] = iosOrderId
        isSandbox = is_sandbox_receipt(receipt)
        ret = cls.doIosCallbackVerify(paydata, isSandbox)
        productsStr = ''
        #         ret = 'ok'
        #         paydata['product_id'] = '10003005'
        #         paydata['original_transaction_id'] = '10003005SSSS'
        #         paydata['iosreceipt'] = {}
        if ret != 'ok':
            return ret

        transaction_id = paydata['original_transaction_id']
        if cls.__is_ios_transaction_delivered(transaction_id):
            return 'error-transaction-already-delivered'

        products = []
        # 由于ios多个版本会用冲突，这里增加根据clientId来获取商品信息
        if clientId != '':
            products = TyContext.Configure.get_game_item_json(str(appId) + ':' + str(clientId), 'products')
        if products == None:
            products = TyContext.Configure.get_game_item_json(appId, 'products')
        if products == None:
            products = []

        TyContext.ftlog.info('IOS->doIosCallback products=', products)
        total_fee = 0
        orderName = ''
        prodId = ''
        pid = paydata['product_id']
        for x in xrange(len(products)):
            if products[x][0] == pid:
                orderName = products[x][1]
                total_fee = int(float(products[x][2]))
                if len(products[x]) > 3:
                    prodId = products[x][3]
                else:
                    prodId = pid
                break
        if total_fee == 0:
            TyContext.ftlog.error('IOS->doIosCallback cannot find product of ', pid)
            return 'error-receipt2'

        # paydata['orderId'] = ioskey
        paydata['orderId'] = iosOrderId
        paydata['appId'] = appId
        paydata['userId'] = userId
        paydata['clientId'] = clientId
        paydata['payType'] = 'ios'
        paydata['orderPrice'] = total_fee
        paydata['orderName'] = orderName
        paydata['authInfo'] = authInfo
        paydata['appInfo'] = appInfo
        paydata['raffle'] = raffle
        paydata['prodId'] = prodId

        from tysdk.entity.pay.pay import TuyouPay
        TyContext.ftlog.info('IOS->doIosCallback->paydata=', paydata)
        platformOrderId = iosOrderId
        # 只对自有游戏做防刷。对第三方没有buy_prod流程，没有GO订单
        if appId < 10000:
            dbUserId, game_order_id = TyContext.RedisPayData.execute('HMGET', 'platformOrder:' + platformOrderId,
                                                                     'userId', 'orderId')
            if dbUserId and isinstance(dbUserId, int) and dbUserId > 10000:
                game_db_prodid = TyContext.RedisPayData.execute('HGET', 'gameOrder:' + game_order_id, 'prodId')
                if game_db_prodid != prodId:
                    TyContext.ftlog.error('IOS->doIosCallback the receipt prodid is not equal to the pay request 1 !',
                                          pid, platformOrderId, game_db_prodid, game_order_id)
                    return 'error-prodid'
            else:
                game_db_prodid = TyContext.RedisPayData.execute('HGET', 'gameOrder:' + platformOrderId, 'prodId')
                if game_db_prodid != prodId:
                    TyContext.ftlog.error('IOS->doIosCallback the receipt prodid is not equal to the pay request 2 !',
                                          pid, platformOrderId, game_db_prodid)
                    return 'error-prodid'

                platformOrderId = TuyouPay.createTransaction(userId, paydata)

        TuyouPay.changeTransState(platformOrderId, PAY_STATE_CHARGE, 'PAY_STATE_CHARGE', paydata)

        paydata['third_orderid'] = transaction_id
        paydata['third_prodid'] = pid
        isOk = TuyouPay.doBuyChargeCallback(platformOrderId, total_fee, 'TRADE_FINISHED', paydata)
        if isOk:
            cls.__mark_ios_transaction_as_delivered(transaction_id)
            try:
                # 328 & 628 第一次购买后只能使用微信支付
                ios_control = TyContext.Configure.get_global_item_json('ios_weinxin_pay_control', {})
                if prodId in ios_control.get('weixin_products', []):
                    TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'wxpay_flag', 1)
            except:
                TyContext.ftlog.exception()
            return 'success'
        else:
            return 'error-delivery'

    # @classmethod
    # def __parse_ios_receipt(cls, receipt):


    @classmethod
    def __mark_ios_transaction_as_delivered(cls, transaction_id):
        ttl = TyContext.RedisMix.execute('TTL', 'delivered_ios_transactions')
        TyContext.RedisMix.execute('SADD', 'delivered_ios_transactions',
                                   transaction_id)
        TyContext.ftlog.info('__mark_ios_transaction_as_delivered add transaction_id:',
                             transaction_id, 'ttl:', ttl)
        if ttl < 0:
            TyContext.RedisMix.execute('EXPIRE', 'delivered_ios_transactions',
                                       60 * 60 * 24 * 30)

    @classmethod
    def __is_ios_transaction_delivered(cls, transaction_id):
        return 1 == TyContext.RedisMix.execute('SISMEMBER', 'delivered_ios_transactions', transaction_id)

    @classmethod
    def doIosCallbackVerify(cls, paydata, isSandBox):
        if isSandBox:
            vrurl = 'https://sandbox.itunes.apple.com/verifyReceipt'
        else:
            vrurl = 'https://buy.itunes.apple.com/verifyReceipt'

        TyContext.ftlog.debug('IOS->doIosCallbackVerify isSandBox=', isSandBox, 'url=', vrurl, 'datas=', paydata)

        paydata['iosurl'] = vrurl
        paydata['sandbox'] = isSandBox
        receiptJsonStr = paydata['receiptJsonStr']
        response, vrurl = TyContext.WebPage.webget(vrurl, {}, None, receiptJsonStr, 'POST',
                                                   {'Content-type': 'text/json'})
        return cls.doIosCallbackVerifyDone(response, paydata)

    @classmethod
    def doIosCallbackVerifyDone(cls, response, paydata):
        TyContext.ftlog.info('doIosCallbackVerifyDone response=', response, 'request=', paydata)
        try:
            status = None
            receipt = None
            product_id = None
            original_transaction_id = None
            ht = json.loads(response)
            for i in ht:
                TyContext.ftlog.debug('doIosCallbackVerifyDone item:', str(i) + ' ' + str(ht[i]))
            if ht.has_key('status'):
                status = int(ht['status'])
            if ht.has_key('receipt'):
                receipt = ht['receipt']
                if receipt.has_key('product_id'):
                    product_id = receipt['product_id']
                if receipt.has_key('original_transaction_id'):
                    original_transaction_id = receipt['original_transaction_id']
            if status == 0:
                if receipt != None and product_id != None and original_transaction_id != None:
                    paydata['product_id'] = product_id
                    paydata['original_transaction_id'] = original_transaction_id
                    paydata['iosreceipt'] = ht
                    return 'ok'
                else:
                    return 'error-product_id'
            elif status == 21007:  # This receipt is a sandbox receipt, but it was sent to the production service for verification.
                return cls.doIosCallbackVerify(paydata, True)
            elif status == 21008:  # This receipt is a production receipt, but it was sent to the sandbox service for verification.
                return cls.doIosCallbackVerify(paydata, False)
            else:
                return 'error-status-' + str(status)
        except:
            TyContext.ftlog.exception()
            return 'error-system'
