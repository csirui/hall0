#! encoding=utf-8
import json
import time
from hashlib import md5

from datetime import datetime

from tyframework.context import TyContext
from tysdk.entity.pay3.diamondlist import TuyouPayDiamondList
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4
from tysdk.entity.user3.account_check import AccountCheck
from tysdk.entity.user3.account_game_data import AccountGameData


def is_sandbox_receipt(receipt):
    try:
        import re
        import base64
        receiptstr = base64.b64decode(receipt)
        line = re.compile(r'("[^"]*")\s*=\s*("[^"]*");')
        result = line.sub(r'\1: \2,', receiptstr)
        trailingcomma = re.compile(r',(\s*})')
        receiptstr = trailingcomma.sub(r'\1', result)
        receipt = json.loads(receiptstr)
        if receipt['environment'] == 'Sandbox':
            return True
    except:
        return False


__author__ = 'yuejianqiang'


class TuYouPayIOSV4(PayBaseV4):
    @classmethod
    def get_pay_ios_product(cls, appId, prodId, clientId, checkIdKey):
        products = TuyouPayDiamondList._get_pay_products_list_(appId, clientId, 'ios-products-v2', clientId)
        if products is None:
            TyContext.ftlog.error('get_pay_ios_product products not found ! appId=', appId, 'prodId=', prodId,
                                  'clientId=', clientId, 'checkIdKey=', checkIdKey)
            return None
        for x in xrange(len(products)):
            if products[x][checkIdKey] == prodId:
                TyContext.ftlog.debug('get_pay_ios_product the ios pay product appId=', appId, 'prodId=', prodId,
                                      'clientId=', clientId, 'checkIdKey=', checkIdKey, 'product=', products[x])
                return products[x]
        TyContext.ftlog.error('get_pay_ios_product the ios pay product not found ! appId=', appId, 'prodId=', prodId,
                              'clientId=', clientId, 'checkIdKey=', checkIdKey)
        return None

    @classmethod
    def check_match(cls, regExpList, checkStr):
        import re
        for regExp in regExpList:
            if regExp == '*':
                return True
            breg = re.compile(regExp)
            if breg.match(checkStr):
                return True
        return False

    @classmethod
    def get_ios_product_by_packageName(cls, appId, packageName, clientId, buttonId):
        rediskey = 'ios-products-v4:%s' % packageName
        configList = TyContext.Configure.get_game_item_json(appId, rediskey, [])
        if not configList:
            return None, None
        products = None
        for config in configList:
            regExpList = config.get('clientIds')
            if cls.check_match(regExpList, clientId):
                products = config.get('products')
        if not products:
            return None, None
        for product in products:
            if product.get('tyid') == buttonId:
                return product, products
        return None, None

    def check_charge_info(self, mi, chargeInfo):
        appId = chargeInfo['appId']
        clientId = chargeInfo['clientId']
        diamondId = chargeInfo['diamondId']
        diamondPrice = chargeInfo['diamondPrice']
        packageName = chargeInfo.get('packageName', '')
        products = []
        if packageName:
            _, products = self.get_ios_product_by_packageName(appId, packageName, clientId, diamondId)
        if not products:
            products = TuyouPayDiamondList._get_pay_products_list_(appId, clientId, 'ios-products-v2', clientId)
        # 没有计费点商品
        if not filter(lambda x: x['tyid'] == diamondId, products):
            prodDict = ChargeConfigure.get_prod_dict(appId, clientId=clientId)
            diamondList = []
            for diamond in products:
                tyid = diamond['tyid']
                prodInfo = prodDict.get(tyid, {})
                if prodInfo.get('is_diamond') and prodInfo['price'] >= diamondPrice:
                    diamondList.append(prodInfo)
            if diamondList:
                diamondList.sort(lambda x, y: cmp(x['price'], y['price']))
                prodInfo = diamondList[0]
                chargeInfo['diamondId'] = prodInfo['id']
                chargeInfo['buttonId'] = prodInfo['id']
                chargeInfo['diamondName'] = prodInfo['name']
                chargeInfo['diamondPrice'] = prodInfo['price']
                chargeInfo['chargeTotal'] = prodInfo['price'] * chargeInfo['diamondCount']
                chargeInfo['chargeCoin'] = prodInfo['diamondPrice'] * chargeInfo['diamondCount']

    @payv4_order('tuyooios')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        TyContext.ftlog.debug('TuYouPayIOSV4', 'charge_data->chargeinfo', chargeinfo)
        buttonId = chargeinfo['buttonId']
        clientId = chargeinfo['clientId']
        appId = chargeinfo['appId']
        userId = chargeinfo['uid']
        product = self.get_pay_ios_product(appId, buttonId, clientId, 'tyid')
        if not product:
            raise Exception('the ios pay code not found ! userId=' + str(userId)
                            + ' appId=' + str(appId) + ' buttonId=' + str(buttonId)
                            + ' clientId=' + str(clientId))
        payCode = product['iosid']
        orderProdName = product['name']
        chargeinfo['chargeData'] = {'orderIosCode': payCode, 'orderProdName': orderProdName}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/ios/callback')
    def doIosCallback(cls, rpath):

        platformOrderId = TyContext.RunHttp.getRequestParam('iosOrderId', '')
        TyContext.RunMode.get_server_link(platformOrderId)

        isReturn, params = AccountCheck.normal_check(rpath, True)
        if isReturn:
            return params
        userId = params['userId']
        appId = params['appId']
        clientId = params['clientId']
        appInfo = TyContext.RunHttp.getRequestParam('appInfo', '')

        isMock = bool(TyContext.RunHttp.getRequestParam('isMock'))

        receipt = TyContext.RunHttp.getRequestParam('receipt', '')
        receiptData = {'receiptJsonStr': '{"receipt-data" : "' + receipt + '"}',
                       'platformOrder': platformOrderId, 'userId': userId}

        TyContext.ftlog.info('IOS->doIosCallback->userId', userId, 'appId', appId,
                             'clientId', clientId, 'appInfo', appInfo,
                             'platformOrderId', platformOrderId, 'receipt', receipt,
                             'isMock', isMock)

        rparam = PayHelperV4.getArgsDict()
        rparam['chargeType'] = 'tuyooios'
        rparam['userId'] = params['userId']
        rparam['appId'] = params['appId']
        rparam['clientId'] = params['clientId']

        isSandbox = is_sandbox_receipt(receipt)
        ret = cls.doIosCallbackVerify(receiptData, isSandbox, isMock)
        TyContext.ftlog.debug('IOS->doIosCallback->doIosCallbackVerify ret=', ret)

        if ret != 'ok' and ret != 'uuid_prohibit':
            PayHelperV4.callback_error(platformOrderId, ret, rparam)
            return ret
        # 如果是被封禁的uuid，不进行发货处理
        if ret == 'uuid_prohibit':
            return 'success'

        transaction_id = receiptData['original_transaction_id']
        rparam['third_orderid'] = transaction_id
        rparam['third_prodid'] = receiptData.get('product_id', 'na')
        rparam['isTestOrder'] = receiptData.get('sandbox', False)

        if cls._is_ios_transaction_delivered(transaction_id):
            PayHelperV4.callback_error(platformOrderId, 'error-transaction-already-delivered', rparam)
            TyContext.ftlog.info('IOS->doIosCallback error-transaction-already-delivered '
                                 'userId', userId, 'platformOrder', platformOrderId)
            return 'error-transaction-already-delivered'

        if not platformOrderId:
            ret = cls._deliver_missing_order(rparam)
            if not ret:
                return 'error-platform-order-missing'
            else:
                platformOrderId = ret
        # 根据商品Id过滤刷单的订单---------------start
        try:
            chargeKey = 'sdk.charge:' + platformOrderId
            chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
            if chargeInfo == None:
                TyContext.ftlog.info('IOS->doIosCallback error-platformOrderId-not-found '
                                     'userId', userId, 'platformOrder', platformOrderId)
                return 'error-platform-order-missing'

            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
            if 'chargeData' in chargeInfo and 'orderIosCode' in chargeInfo['chargeData'] and chargeInfo['chargeData'][
                'orderIosCode'] != rparam['third_prodid']:
                TyContext.ftlog.info('IOS->doIosCallback error-product_id '
                                     'userId', userId, 'platformOrder', platformOrderId, 'orderIosCode',
                                     chargeInfo['chargeData']['orderIosCode'], 'receipt_product_id',
                                     rparam['third_prodid'])
                return 'error-product_id'
        except:
            pass

        product = cls.get_pay_ios_product(appId, rparam['third_prodid'], clientId, 'iosid')
        if not product:
            TyContext.ftlog.error('get_pay_ios_product products not found!'
                                  ' appId=', appId, 'iosId=', rparam['third_prodid'],
                                  'clientId=', clientId, 'checkIdKey=iosid')
            return 'error-product_id'
        # 根据商品Id过滤刷单的订单---------------end

        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparam)
        if isOk:
            cls._mark_ios_transaction_as_delivered(transaction_id)
            try:
                # 328 & 628 第一次购买后只能使用微信支付
                ios_control = TyContext.Configure.get_global_item_json('ios_weinxin_pay_control', {})
                if product['tyid'] in ios_control.get('weixin_products', []):
                    wxpay_count = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'wxpay_flag')
                    if not wxpay_count:
                        wxpay_count = 0
                    TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'wxpay_flag',
                                                int(wxpay_count) + 1)
            except:
                TyContext.ftlog.exception()
            return 'success'
        else:
            return 'error-handle-callback'

    @classmethod
    def doIosCallbackVerify(cls, paydata, isSandBox, isMock=False):
        platformOrderId = paydata['platformOrder']
        userId = paydata['userId']
        receiptJsonStr = paydata['receiptJsonStr']
        if not receiptJsonStr or len(receiptJsonStr) < 200:
            return 'error-receipt'

        # documentation link: https://developer.apple.com/library/ios/releasenotes/General/ValidateAppStoreReceipt/Chapters/ValidateRemotely.html
        if isMock:
            vrurl = PayHelperV4.getSdkDomain() + '/open/v3/mockios/verifyReceipt'
        elif isSandBox:
            vrurl = 'https://sandbox.itunes.apple.com/verifyReceipt'
        else:
            vrurl = 'https://buy.itunes.apple.com/verifyReceipt'

        TyContext.ftlog.debug('IOS->doIosCallbackVerify isSandBox=', isSandBox, 'url=', vrurl, 'datas=', paydata)

        paydata['iosurl'] = vrurl
        paydata['sandbox'] = isSandBox
        # verifying order can get errors like, "503 Service Unavailable",
        # TCPTimedOutError, etc. so retry 3 times. client will timeout after 8s,
        # so it is useless to retry longer. If sdk service restarts during the
        # process, client will get no response, in which case the client will
        # retry the callback.
        retries = 3
        while retries > 0:
            try:
                response, vrurl = TyContext.WebPage.webget(
                    vrurl, {}, None, receiptJsonStr, 'POST',
                    {'Content-type': 'text/json'})
                return cls.doIosCallbackVerifyDone(response, paydata)
            except Exception, e:
                TyContext.ftlog.error('IOS->doIosCallbackVerify webget failed.'
                                      ' exception', e, 'userId', userId,
                                      'platformOrder', platformOrderId)
                retries -= 1
        TyContext.ftlog.error('IOS->doIosCallbackVerify webget failed 3 times in a row, datas=', paydata)
        return 'error-system'

    @classmethod
    def doIosCallbackVerifyDone(cls, response, paydata):
        TyContext.ftlog.info('doIosCallbackVerifyDone response=', response, 'request=', paydata)
        try:
            status = None
            receipt = None
            product_id = None
            original_transaction_id = None
            user_uuid = None
            ht = json.loads(response)
            for i in ht:
                TyContext.ftlog.debug('doIosCallbackVerifyDone item:', str(i) + ' ' + str(ht[i]))
            if ht.has_key('status'):
                status = int(ht['status'])
            if ht.has_key('receipt'):
                receipt = ht['receipt']
                # 判断uuid是否被列入黑名单中
                if receipt.has_key('unique_identifier') and receipt['unique_identifier'] != '':
                    user_uuid = receipt['unique_identifier']

                # 兼容新AppStore IAP，增加in_app参数:
                if receipt.has_key('in_app'):
                    in_app_list = receipt['in_app']
                    if isinstance(in_app_list, list):
                        ln = len(in_app_list)
                        if ln > 1:
                            in_app_list = sorted(receipt["in_app"], key=lambda info: info['original_purchase_date'])
                        if in_app_list[ln - 1].has_key('product_id'):
                            product_id = in_app_list[ln - 1]['product_id']
                        if in_app_list[ln - 1].has_key('original_transaction_id'):
                            original_transaction_id = in_app_list[ln - 1]['original_transaction_id']
                else:
                    if receipt.has_key('product_id'):
                        product_id = receipt['product_id']
                    if receipt.has_key('original_transaction_id'):
                        original_transaction_id = receipt['original_transaction_id']
            if status == 0:
                if receipt is not None and product_id is not None and original_transaction_id is not None:
                    paydata['product_id'] = product_id
                    paydata['original_transaction_id'] = original_transaction_id
                    paydata['iosreceipt'] = ht
                    if user_uuid != None:
                        if cls._is_ios_backlist_uid(user_uuid):
                            TyContext.ftlog.info('iosPayProhibitedByUuid', 'userId=', paydata['userId'],
                                                 'platformOrderId=', paydata['platformOrder'], 'uuid=', user_uuid)
                            return 'uuid_prohibit'

                        # 判断uuid是否超过充值限制
                        checkret, payiosquota, ios_pay_total, ios_uuid_pay_amount = cls._check_uuid_ios_pay(user_uuid,
                                                                                                            paydata[
                                                                                                                'userId'])
                        if checkret:
                            TyContext.ftlog.info('iosPayLimitedByUuid', 'userId=', paydata['userId'],
                                                 'platformOrderId=', paydata['platformOrder'], 'uuid=', user_uuid,
                                                 'payiosquota=', payiosquota, 'ios_pay_total=', ios_pay_total,
                                                 'ios_uuid_pay_amount=', ios_uuid_pay_amount)
                            ios_limited_config = TyContext.Configure.get_global_item_json('ios_limited_config', {})
                            ios_uuid_pay_total_open = ios_limited_config.get('ios_uuid_pay_total_open', 1)
                            if ios_uuid_pay_total_open:
                                return 'uuid_prohibit'
                        # 更新充值uuid的次数及金额
                        chargeKey = 'sdk.charge:' + paydata['platformOrder']
                        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
                        if chargeInfo != None:
                            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
                            cls._update_ios_uuid_quota(user_uuid, int(chargeInfo['chargeTotal']))
                    return 'ok'
                else:
                    return 'error-product_id'
            # elif status == 21005 :  # The receipt server is not currently available, retry
            #    return cls.doIosCallbackVerify(paydata, False)
            elif status == 21007:  # This receipt is a sandbox receipt, but it was sent to the production service for verification.
                return cls.doIosCallbackVerify(paydata, True)
            elif status == 21008:  # This receipt is a production receipt, but it was sent to the sandbox service for verification.
                return cls.doIosCallbackVerify(paydata, False)
            else:
                return 'error-status-' + str(status)
        except:
            TyContext.ftlog.exception()
            return 'error-system'

    @classmethod
    def _mark_ios_transaction_as_delivered(cls, transaction_id):
        ttl = TyContext.RedisMix.execute('TTL', 'delivered_ios_transactions')
        TyContext.RedisMix.execute('SADD', 'delivered_ios_transactions',
                                   transaction_id)
        TyContext.ftlog.info('_mark_ios_transaction_as_delivered add transaction_id:',
                             transaction_id, 'ttl:', ttl)
        if ttl < 0:
            TyContext.RedisMix.execute('EXPIRE', 'delivered_ios_transactions',
                                       60 * 60 * 24 * 30)

    @classmethod
    def _is_ios_transaction_delivered(cls, transaction_id):
        return 1 == TyContext.RedisMix.execute('SISMEMBER', 'delivered_ios_transactions', transaction_id)

    @classmethod
    def _deliver_missing_order(cls, rparam):

        # fake platform order, for gdss' sake
        ts = int(time.time())
        seqNum = int(TyContext.RedisMix.execute('INCR', 'global.orderid.seq.a'))
        fake_order = 'fakeo' + TyContext.strutil.tostr62(ts, 6) + \
                     TyContext.strutil.tostr62(seqNum, 3)

        platformOrderId = fake_order
        appId = rparam['appId']
        iosId = rparam['third_prodid']
        clientId = rparam['clientId']
        userId = rparam['userId']
        appInfo = TyContext.RunHttp.getRequestParam('appInfo', '')
        product = cls.get_pay_ios_product(appId, iosId, clientId, 'iosid')
        if not product:
            TyContext.ftlog.error('get_pay_ios_product products not found!'
                                  ' appId=', appId, 'iosId=', iosId,
                                  'clientId=', clientId, 'checkIdKey=iosid')
            return None

        state = 0
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        charge = {}
        prodId = product['tyid']
        prodPrice = product['price']
        prodName = product['name']
        charge['diamondId'] = prodId
        charge['uid'] = userId
        charge['diamondName'] = prodName
        charge['buttonId'] = prodId
        charge['appInfo'] = appInfo
        charge['clientId'] = clientId
        charge['chargeTotal'] = int(prodPrice / 10)
        charge['phoneType'] = 0
        charge['chargeType'] = 'tuyooios'
        charge['appId'] = appId
        charge['diamondsPerUnit'] = int(prodPrice)
        charge['buttonName'] = prodName
        charge['diamondCount'] = 1
        charge['diamondPrice'] = int(prodPrice / 10)
        charge['platformOrderId'] = platformOrderId

        consume = {}
        consume['appInfo'] = appInfo
        # consume['mustcharge'] = 1
        consume['userId'] = userId
        consume['prodCount'] = 1
        consume['clientId'] = clientId
        consume['prodPrice'] = prodPrice
        consume['prodId'] = prodId
        consume['appId'] = appId
        consume['prodName'] = prodName
        consume['prodOrderId'] = 'ios_compensate'
        consume['consumeCoin'] = prodPrice

        # 伪造chargeKey中的内容
        chargeKey = 'sdk.charge:' + platformOrderId
        # 当不是直接购买钻石时,需要加上商品信息
        if product['tyid'][6] == 'D':
            TyContext.RedisPayData.execute('HMSET', chargeKey, 'state', state,
                                           'cbTime', timestamp,
                                           'createTime', timestamp,
                                           'charge', json.dumps(charge),
                                           'consume', json.dumps(consume))
        else:
            TyContext.RedisPayData.execute('HMSET', chargeKey, 'state', state,
                                           'cbTime', timestamp,
                                           'createTime', timestamp,
                                           'charge', json.dumps(charge))

        return platformOrderId

    @classmethod
    def _check_user_ios_pay(cls, userId):
        if userId == None or int(userId) <= 10000:
            return False, None
        # 'ios_gametime_limit_today': 600, # 每日时长10分钟
        # 'ios_gametime_limit_day7': 3*3600, # 7天时长超过3小时
        # 'ios_gametime_limit_total': 10*3600, # 累计超过10小时
        ios_limited_config = TyContext.Configure.get_global_item_json('ios_limited_config', {})
        if cls._check_ios_pay_time(userId, ios_limited_config):
            return False, None
        try:
            ios_pay_total = ios_limited_config.get('ios_pay_total', 2000)
            ios_pay_waived_uids = ios_limited_config.get('ios_pay_waived_uids', [])
            pay_limit_msg = ios_limited_config.get('pay_limit_msg', '对不起，您的充值已达上限')
            if userId in ios_pay_waived_uids:
                return False, None

            payiosquota = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'payiosquota')
            if payiosquota:
                payiosquota = json.loads(payiosquota)
            else:
                payiosquota = {}

            if cls._is_ios_volume_capped(payiosquota, ios_pay_total):
                TyContext.ftlog.info('_check_user_ios_pay ios pay limited:'
                                     ' userId', userId, 'payiosquota', payiosquota, 'ios_pay_total', ios_pay_total)
                return True, pay_limit_msg

        except Exception as e:
            TyContext.ftlog.error('_check_user_ios_pay failed:', ' userId', userId)

        return False, None

    @classmethod
    def _is_ios_volume_capped(cls, quota, limit_day):
        if not quota:
            return False
        day, dcount = quota['yyyymmdd'], quota['dcount']
        if day is None:
            return False
        day = str(day)
        now = datetime.now()
        now_day = now.strftime('%Y%m%d')
        if limit_day >= 0 and day == now_day and dcount > limit_day:
            return True
        return False

    @classmethod
    def _update_ios_quota(cls, userId, amount):
        quota = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'payiosquota')
        if quota:
            quota = json.loads(quota)
        else:
            quota = {}

        now = datetime.now()
        now_day = now.strftime('%Y%m%d')
        day, dcount = quota.get('yyyymmdd'), quota.get('dcount')
        if not day:
            dcount = amount
        else:
            day = str(day)
            if day != now_day:
                dcount = amount
            else:
                dcount += amount
        quota = {'yyyymmdd': now_day, 'dcount': dcount}
        TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'payiosquota', json.dumps(quota))
        TyContext.ftlog.info('_check_user_ios_pay _record_user_iospay', 'user:' + str(userId), 'payiosquota', quota)

    @classmethod
    def _check_ios_pay_time(cls, userId, ios_limited_config):
        ios_gametime_limit_today = ios_limited_config.get('ios_gametime_limit_today', 600)  # 当天10分钟
        ios_gametime_limit_day7 = ios_limited_config.get('ios_gametime_limit_day7', 3 * 3600)  # 7天累计3小时
        ios_gametime_limit_total = ios_limited_config.get('ios_gametime_limit_total', 10 * 3600)  # 累计10小时以上
        today_time = AccountGameData.get_user_today_time(9999, userId)
        TyContext.ftlog.info('_check_ios_pay_time:',
                             'today=%s/%s' % (
                             ios_gametime_limit_today, AccountGameData.get_user_today_time(9999, userId)),
                             'day7=%s/%s' % (AccountGameData.get_user_day7_time(9999, userId), ios_gametime_limit_day7),
                             'total=%s/%s' % (
                             AccountGameData.get_user_total_time(9999, userId), ios_gametime_limit_total))
        if today_time > ios_gametime_limit_today:
            day7_time = AccountGameData.get_user_day7_time(9999, userId)
            total_time = AccountGameData.get_user_total_time(9999, userId)
            if day7_time > ios_gametime_limit_day7 or total_time > ios_gametime_limit_total:
                TyContext.ftlog.info('_check_ios_pay_time:'
                                     ' userId', userId,
                                     'today_time=%s/%s' % (today_time, ios_gametime_limit_today),
                                     'total_time=%s/%s' % (total_time, ios_gametime_limit_total),
                                     'day7_time=%s/%s' % (day7_time, ios_gametime_limit_day7))
                return True
        return False

    @classmethod
    def _check_uuid_ios_pay(cls, uuid, userId):
        if not uuid:
            return False, None, None, None
        # uuid = cls.uuidTomd5(uuid)
        ios_limited_config = TyContext.Configure.get_global_item_json('ios_limited_config', {})
        if cls._check_ios_pay_time(userId, ios_limited_config):
            return False, None, None, None
        try:
            ios_pay_total = ios_limited_config.get('ios_uuid_pay_total', 10)
            ios_uuid_pay_amount = ios_limited_config.get('ios_uuid_pay_amount', 3000)
            pay_limit_msg = ios_limited_config.get('ios_uuid_limit_msg', '单日充值次数达到上限')
            ios_pay_waived_uids = ios_limited_config.get('ios_pay_waived_uids', [])
            # 判断是否在白名单里
            if userId != None and userId in ios_pay_waived_uids:
                return False, None, None, None

            payiosquota = TyContext.RedisPayData.execute('GET', 'payiosquota:' + uuid)
            if payiosquota:
                payiosquota = json.loads(payiosquota)
            else:
                payiosquota = {}
            if cls._is_ios_uuid_capped(payiosquota, ios_pay_total, ios_uuid_pay_amount):
                TyContext.ftlog.debug('_check_uuid_ios_pay limited: uuid', uuid, 'payiosquota', payiosquota,
                                      'ios_uuid_pay_total', ios_pay_total)
                return True, payiosquota, ios_pay_total, ios_uuid_pay_amount

        except Exception as e:
            TyContext.ftlog.error('_check_uuid_ios_pay failed:', ' uuid', uuid)

        return False, None, None, None

    @classmethod
    def _is_ios_uuid_capped(cls, quota, limit_count, limit_amount):
        TyContext.ftlog.debug('_is_ios_uuid_capped', 'quota', quota, 'limit_count', limit_count, 'limit_amount',
                              limit_amount)
        if not quota:
            return False
        if not 'damount' in quota:
            quota['damount'] = 0
        day, dcount, damount = quota['yyyymmdd'], quota['dcount'], quota['damount']
        if day is None:
            return False
        day = str(day)
        now = datetime.now()
        now_day = now.strftime('%Y%m%d')
        if limit_count >= 0 and day == now_day and (dcount > limit_count or damount > limit_amount):
            return True
        return False

    @classmethod
    def _update_ios_uuid_quota(cls, uuid, amount):
        # uuid = cls.uuidTomd5(uuid)
        quota = TyContext.RedisPayData.execute('GET', 'payiosquota:' + uuid)
        if quota:
            quota = json.loads(quota)
        else:
            quota = {}

        if not 'damount' in quota:
            quota['damount'] = int(amount)

        now = datetime.now()
        now_day = now.strftime('%Y%m%d')
        day, dcount, damount = quota.get('yyyymmdd'), quota.get('dcount'), quota['damount']
        if not day:
            dcount = 1
            damount = amount
        else:
            day = str(day)
            if day != now_day:
                dcount = 1
                damount = amount
            else:
                dcount += 1
                damount += amount
        quota = {'yyyymmdd': now_day, 'dcount': dcount, 'damount': damount}
        TyContext.RedisPayData.execute('SET', 'payiosquota:' + uuid, json.dumps(quota))
        TyContext.ftlog.debug('_update_ios_uuid_quota', 'payiosquota:' + uuid, quota)

    @classmethod
    def _is_ios_backlist_uid(cls, user_uuid):
        # user_uuid = cls.uuidTomd5(user_uuid)
        return 1 == TyContext.RedisPayData.execute('SISMEMBER', 'ios_pay_uuid_backlist', user_uuid)

    @classmethod
    def uuidTomd5(cls, uuid):
        mstr = uuid = uuid.lower()
        if len(mstr) > 0:
            m = md5()
            m.update(mstr)
            md5str = m.hexdigest()
            return md5str
        return ''

    @classmethod
    def _zadd_user_ios_pay(cls, uid, amount):
        if int(uid) <= 0 or int(amount) <= 0:
            return
        ts = int(time.time())
        TyContext.RedisUser.execute(uid, 'ZADD', 'ios_pay_user:%d' % int(uid), ts, amount)
        TyContext.ftlog.debug('_zadd_user_ios_pay', 'userId', uid, 'amount', amount)
        # maxtime = ts - 86400
        # 清除掉历史充值数据
        # TyContext.RedisUser.execute(uid,'zremrangebyscore', 'ios_pay_user:%d' % int(uid),0, maxtime)
        # 判断5分钟内的充值
        min5ret, amount_total, limit_amount = cls._check_ios_pay_5mins(uid)
        if min5ret:
            TyContext.ftlog.info('iosPayLimitedBy5mins', 'userId=', uid, 'amount_total=', amount_total, 'limit_amount=',
                                 limit_amount)

    @classmethod
    def _check_ios_pay_5mins(cls, uid):
        if uid == None or int(uid) <= 0:
            return False, None, None
        etime = int(time.time())
        stime = etime - 300
        ios_limited_config = TyContext.Configure.get_global_item_json('ios_limited_config', {})
        limit_amount = ios_limited_config.get('ios_5mins_pay_total', 195)
        amount_total = 0.0
        amountList = TyContext.RedisUser.execute(uid, 'zrangebyscore', 'ios_pay_user:%d' % int(uid), stime, etime)
        if amountList and len(amountList) > 0:
            TyContext.ftlog.debug('_check_ios_pay_5mins', 'userId', uid, 'amountList', amountList)
            for amount in amountList:
                amount_total += amount
        if amount_total >= limit_amount:
            TyContext.ftlog.debug('_check_ios_pay_5mins', 'userId=', uid, 'amount_total=', amount_total,
                                  'limit_amount=', limit_amount)
            return True, amount_total, limit_amount

        return False, None, None

    @classmethod
    def _check_user_gametime(cls, userId):
        if userId == None or int(userId) <= 0:
            return False
        ios_limited_config = TyContext.Configure.get_global_item_json('ios_limited_config', {})
        gametimes_limited = ios_limited_config.get('ios_gametimes_limited', 3600)
        is_open_gametimes = ios_limited_config.get('ios_gametimes_limited_open', 1)
        if not is_open_gametimes:
            return False
        gametime = TyContext.RedisUser.execute(userId, 'HGET', 'gamedata:9999:' + str(userId), 'totaltime')
        TyContext.ftlog.debug('_check_user_gametime', 'userId=', userId, 'gametime=', gametime, 'gametimes_limited=',
                              gametimes_limited)
        if gametime == None:
            return False

        if gametime <= gametimes_limited:
            TyContext.ftlog.info('iosPayLimitedByGametimes', 'userId=', userId, 'gametime=', gametime,
                                 'gametimes_limited=', gametimes_limited)
            return True
        return False
