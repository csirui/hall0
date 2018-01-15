# -*- coding=utf-8 -*-

import base64
import json
import traceback

from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as pk

from tyframework.context import TyContext
from tysdk.entity.pay3.diamondlist import TuyouPayDiamondList
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.paythird.helper import PayHelper
from tysdk.entity.user3.account_check import AccountCheck


class TuyouPayGoogleIABV4(PayBaseV4):
    __name__ = 'googleiab'

    @payv4_order('googleiab')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        buttonId = chargeinfo.get('prodId', chargeinfo['diamondId'])
        clientId = chargeinfo['clientId']
        phoneType = chargeinfo['phoneType']
        appId = chargeinfo['appId']
        userId = chargeinfo['uid']
        TyContext.ftlog.debug(cls.__name__, 'charge_data->', userId, appId, buttonId, phoneType, clientId)
        product = cls.get_pay_googleiab_product(appId, buttonId, clientId, 'tyid')
        if product == None:
            raise Exception('the googleiab pay code not found ! userId=' + str(userId) + ' appId=' + str(
                appId) + ' buttonId=' + str(buttonId) + ' phoneType=' + str(phoneType) + ' clientId=' + str(clientId))
        payCode = product['googleiabid']
        # 是否是支付测试 在global_paytype中配置
        purchase_test = cls._is_googleiab_test_(appId, clientId)
        if purchase_test == True:
            payCode = 'android.test.purchased'  # Google play测试商品 android.test.purchased
        TyContext.ftlog.info('isTest', purchase_test, ' payCode', payCode)
        orderProdName = product['name']
        publicKey = cls._get_google_public_key(appId, clientId, 'google_publickeys', clientId)
        chargeinfo['chargeData'] = {'orderGoogleIABCode': payCode,
                                    'orderProdName': orderProdName,
                                    'publicKey': publicKey,
                                    'platformOrderId': chargeinfo['platformOrderId']}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @classmethod
    def get_pay_googleiab_product(cls, appId, prodId, clientId, checkIdKey):
        products = TuyouPayDiamondList._get_pay_products_list_(appId, clientId, 'googleiab-products-v2', clientId)
        if products is None:
            TyContext.ftlog.error('get_pay_googleiab_product products not found ! appId=', appId, 'prodId=', prodId,
                                  'clientId=', clientId, 'checkIdKey=', checkIdKey)
            return None
        for x in xrange(len(products)):
            if products[x][checkIdKey] == prodId:
                TyContext.ftlog.debug('get_pay_googleiab_product the googleiab pay product appId=', appId, 'prodId=',
                                      prodId, 'clientId=', clientId, 'checkIdKey=', checkIdKey, 'product=', products[x])
                return products[x]
        TyContext.ftlog.error('get_pay_googleiab_product the googleiab pay product not found ! appId=', appId,
                              'prodId=', prodId, 'clientId=', clientId, 'checkIdKey=', checkIdKey)
        return None

    @payv4_callback('/open/ve/pay/googleiab/callback')
    def doGoogleIABCallback(cls, rpath):
        action = TyContext.RunHttp.getRequestParam('action', '')
        appId = TyContext.RunHttp.getRequestParam('appId')
        clientId = TyContext.RunHttp.getRequestParam('clientId')
        # google支付需要向客户端返回公钥
        publicKey = cls._get_google_public_key(appId, clientId, 'google_publickeys', clientId)
        TyContext.ftlog.debug('doGoogleIABCallback->action=', action, 'appId=', appId)

        result = {}
        if not action or action == '':
            result['action'] = ''
            result['state'] = 'error'
            result['info'] = 'error-action is null'
            return cls._dict2string(result)
        elif action == 'getKey':
            result['action'] = 'getKey'
            if publicKey == '':
                result['state'] = 'error'
                result['info'] = 'error-get publickey failed'
                return cls._dict2string(result)
            else:
                result['state'] = 'success'
                result['publicKey'] = publicKey
                result['info'] = 'get publickey success'
                return cls._dict2string(result)
        else:
            platformOrderId = TyContext.RunHttp.getRequestParam('platformOrderId', '')
            if not platformOrderId or platformOrderId is '':
                result['state'] = 'error'
                result['info'] = 'error-null platformOrderId'
                TyContext.ftlog.error('doGoogleIABCallback error platformOrderId is null')
                return cls._dict2string(result)

            result['platformOrderId'] = platformOrderId

            if action == 'redelivery':
                result['action'] = 'redilivery'
            elif action == 'verify':
                result['action'] = 'verify'

            isReturn, params = AccountCheck.normal_check(rpath, True)
            if isReturn:
                result['state'] = 'error'
                result['info'] = 'error-accountcheck failed'
                TyContext.ftlog.error('doGoogleIABCallback->accountcheck failed：', params)
                return cls._dict2string(result)

            signData = TyContext.RunHttp.getRequestParam('purchaseData', '')
            signature = TyContext.RunHttp.getRequestParam('dataSignature', '')

            TyContext.ftlog.info('TuyouPayGoogleIAB.doGoogleIABCallback->action=', action, 'platformOrderId=',
                                 platformOrderId, 'appId=', appId, 'signData=', signData, 'signature=', signature)

            base64PublicKey = '-----BEGIN PUBLIC KEY-----' + '\n' + publicKey + '\n' + '-----END PUBLIC KEY-----'

            if cls.doGoogleIABCallbackVerify(base64PublicKey, signData, signature) != True:
                result['state'] = 'error'
                result['info'] = 'error-verify failed'
                return cls._dict2string(result)

            try:
                signDataObj = json.loads(signData)
            except:
                result['state'] = 'error'
                result['info'] = 'error-load-signData failed'
                TyContext.ftlog.error('doGoogleIABCallback load-signData failed', signData)
                return cls._dict2string(result)

            googleOrderId = signDataObj.get("orderId", "")
            if not googleOrderId:
                result['state'] = 'success'
                result['info'] = 'transaction-already-delivered'
                TyContext.ftlog.error('doGoogleIABCallback, orderId error', googleOrderId)
                return cls._dict2string(result)

            if cls._is_google_transaction_delivered(googleOrderId):
                result['state'] = 'success'
                result['info'] = 'transaction-already-delivered'
                TyContext.ftlog.error('doGoogleIABCallback->order is already-delivered:', googleOrderId)
                return cls._dict2string(result)

            rparam = PayHelper.getArgsDict()
            rparam['chargeType'] = 'googleiab'
            isOk = PayHelper.callback_ok(platformOrderId, -1, rparam)
            if isOk:
                cls._mark_google_transaction_as_delivered(googleOrderId)
                result['state'] = 'success'
                result['info'] = 'googleiab callback success'
                return cls._dict2string(result)
            else:
                result['state'] = 'error'
                result['info'] = 'error-delivery'
                TyContext.ftlog.error('doGoogleIABCallback error delivery')
                return cls._dict2string(result)

    @classmethod
    def doGoogleIABCallbackVerify(cls, base64PublicKey, signedData, signature):
        if not base64PublicKey or not signedData or not signature:
            TyContext.ftlog.error('TuyouPayGoogleIAB.doGoogleIABCallbackVerify->param error.')
            return False

        verified = False
        # 生成公钥实例
        key = RSA.importKey(base64PublicKey)
        # 验签
        verified = cls._verify(key, signedData, signature)
        if verified != True:
            TyContext.ftlog.debug('TuyouPayGoogleIAB.doGoogleIABCallbackVerify->signature does not match data.')
            return False

        return True

    @classmethod
    def _verify(cls, publicKey, signedData, signature):
        try:
            verifier = pk.new(publicKey)
            sd = SHA.new(signedData)
            if verifier.verify(sd, base64.b64decode(signature)):
                TyContext.ftlog.info('TuyouPayGoogleIAB.doGoogleIABCallbackVerify->Signature verification succeded.')
                return True
        except:
            traceback.print_exc()
            TyContext.ftlog.error('TuyouPayGoogleIAB.doGoogleIABCallbackVerify->Signature verification failed.')
            return False

    @classmethod
    def _mark_google_transaction_as_delivered(cls, transaction_id):
        ttl = TyContext.RedisMix.execute('TTL', 'delivered_google_transactions')
        TyContext.RedisMix.execute('SADD', 'delivered_google_transactions',
                                   transaction_id)
        TyContext.ftlog.info('_mark_google_transaction_as_delivered add transaction_id:',
                             transaction_id, 'ttl:', ttl)
        if ttl < 0:
            TyContext.RedisMix.execute('EXPIRE', 'delivered_google_transactions',
                                       60 * 60 * 24 * 60)

    @classmethod
    def _is_google_transaction_delivered(cls, transaction_id):
        return 1 == TyContext.RedisMix.execute('SISMEMBER', 'delivered_google_transactions', transaction_id)

    @classmethod
    def _dict2string(cls, dict):
        rs = '{'
        for key, value in dict.items():
            rs += "\"%s\":\"%s\"" % (key, value) + ','

        str = rs[:-1] + '}'
        return str

    # 获取GooglePlay上应用的公钥
    @classmethod
    def _get_google_public_key(cls, appId, clientId, rediskey, matchStr):
        publickeyconfs = TyContext.Configure.get_game_item_json(appId, rediskey, [])
        publickey = ''
        if publickeyconfs:
            for x in xrange(len(publickeyconfs) - 1, -1, -1):
                publickeyconf = publickeyconfs[x]
                clientIds = publickeyconf['clientIds']
                if TyContext.strutil.reg_matchlist(clientIds, matchStr):
                    publickey = publickeyconf['publickey']
                    if not publickey:
                        publickey = ''
                    break
        TyContext.ftlog.debug('_get_google_public_key->', appId, clientId, rediskey, matchStr, publickey)
        return publickey

    # Google支付是否是购买测试商品
    @classmethod
    def _is_googleiab_test_(cls, appId, clientId):
        clientids = TyContext.Configure.get_game_item_json(appId, 'googleiab.test.clientids', [])
        TyContext.ftlog.info('_is_googleiab_test_->clientids ', clientids)
        if TyContext.strutil.reg_matchlist(clientids, clientId):
            return True
        else:
            return False
