# -*- coding=utf-8 -*-

import binascii
import hashlib
import hmac
import json
import time
import urllib

from helper import PayHelper
from tyframework.context import TyContext

get_balance_org_loc = '/mpay/get_balance_m'
pay_org_loc = '/mpay/pay_m'
cancel_pay_org_loc = '/mpay/cancel_pay_m'
pay_server = {'test': 'http://opensdktest.tencent.com',
              'release': 'http://opensdk.tencent.com',
              }
get_balance_url = ''
pay_url = ''
cancel_pay_url = ''


def set_pay_urls(mode):
    global get_balance_url, pay_url, cancel_pay_url
    get_balance_url = pay_server[mode] + get_balance_org_loc
    pay_url = pay_server[mode] + pay_org_loc
    cancel_pay_url = pay_server[mode] + cancel_pay_org_loc


class ErrorWithInfo(Exception):
    @property
    def info(self):
        return self.__info

    def __init__(self, info):
        self.__info = info


class TuyouPayTencent(object):
    @staticmethod
    def __mk_source(method, url_path, params):
        str_params = urllib.quote(
            "&".join(k + "=" + str(params[k]) for k in sorted(params.keys())),
            '')
        source = '%s&%s&%s' % (method.upper(), urllib.quote(url_path, ''),
                               str_params)
        return str(source)

    @staticmethod
    def _hmac_sha1_sig(method, url_path, params, secret):
        source = TuyouPayTencent.__mk_source(method, url_path, params)
        hashed = hmac.new(str(secret), source, hashlib.sha1)
        return binascii.b2a_base64(hashed.digest())[:-1]

    @staticmethod
    def __get_balance(openid, appid, appkey, accesstoken, paytoken,
                      pf, pfkey, sessionId, sessionType):
        org_loc = get_balance_org_loc
        # POST should do either
        method = 'GET'
        params = {}
        params['appid'] = appid
        params['openid'] = openid
        params['openkey'] = accesstoken
        params['pay_token'] = paytoken
        params['ts'] = int(time.time())
        params['zoneid'] = 1
        params['pf'] = pf
        params['pfkey'] = pfkey

        secret = appkey + '&'
        sig = TuyouPayTencent._hmac_sha1_sig(method, org_loc, params, secret)
        params['sig'] = sig
        _cookies = {'session_id': sessionId,
                    'session_type': sessionType,
                    'org_loc': urllib.quote(org_loc, '')}
        purl = get_balance_url + '?' + urllib.urlencode(params)
        TyContext.ftlog.debug('PayTencent __get_balance: get_balance_url:', purl,
                              'method:', method, 'params:', params, 'cookies:', _cookies)
        response, purl = TyContext.WebPage.webget(purl, {}, method_=method,
                                                  cookies=_cookies)
        TyContext.ftlog.info('PayTencent __get_balance: response:', response)

        jsons = None
        url_params = None
        try:
            jsons = json.loads(response)
            if 'ret' not in jsons:
                raise ErrorWithInfo('tencent payserver error: '
                                    'no ret param in response')
            else:
                ret = int(jsons['ret'])
                if ret == 0:
                    balance = jsons['balance']
                    # gen_balance = jsons['gen_balance']
                else:
                    raise ErrorWithInfo('get_balance_m error ret %d msg %s'
                                        % (ret, jsons['msg']))
        except:
            raise ErrorWithInfo('network error')

        return int(balance)

    @staticmethod
    def __pay(openid, appid, appkey, accesstoken, paytoken,
              pf, pfkey, diamonds, sessionId, sessionType):
        org_loc = pay_org_loc
        # POST should do either
        method = 'GET'
        params = {}
        params['appid'] = appid
        params['openid'] = openid
        params['openkey'] = accesstoken
        params['pay_token'] = paytoken
        params['ts'] = int(time.time())
        params['zoneid'] = 1
        params['pf'] = pf
        params['pfkey'] = pfkey
        params['amt'] = diamonds

        secret = appkey + '&'
        TyContext.ftlog.debug('PayTencent __pay: params:', params)
        TyContext.ftlog.debug('PayTencent __pay: org_loc:', org_loc)
        sig = TuyouPayTencent._hmac_sha1_sig(method, org_loc, params, secret)
        params['sig'] = sig
        _cookies = {'session_id': sessionId,
                    'session_type': sessionType,
                    'org_loc': urllib.quote(org_loc, '')}
        purl = pay_url + '?' + urllib.urlencode(params)
        TyContext.ftlog.debug('PayTencent __pay: pay_url:', purl, 'method:', method,
                              'params:', params, 'cookies:', _cookies)
        response, purl = TyContext.WebPage.webget(purl, {}, method_=method,
                                                  cookies=_cookies)
        TyContext.ftlog.debug('PayTencent __pay: response:', response)

        billno = None
        try:
            resp = json.loads(response)
            if 'ret' not in resp:
                raise ErrorWithInfo('tencent payserver error: '
                                    'no ret param in response')
            else:
                ret = resp['ret']
                if ret == 0:
                    billno = resp['billno']
                else:
                    raise ErrorWithInfo('pay_m error ret %d msg %s'
                                        % (ret, resp['msg']))
        except:
            raise ErrorWithInfo('network error')

        return billno

    @staticmethod
    def __cancel_pay(openid, appid, appkey, accesstoken, paytoken,
                     pf, pfkey, diamonds, billno, sessionId, sessionType):
        org_loc = cancel_pay_org_loc
        # POST should do either
        method = 'GET'
        params = {}
        params['appid'] = appid
        params['openid'] = openid
        params['openkey'] = accesstoken
        params['pay_token'] = paytoken
        params['ts'] = int(time.time())
        params['zoneid'] = 1
        params['pf'] = pf
        params['pfkey'] = pfkey
        params['amt'] = diamonds
        params['billno'] = billno

        secret = appkey + '&'
        sig = TuyouPayTencent._hmac_sha1_sig(method, org_loc, params, secret)
        params['sig'] = sig
        _cookies = {'session_id': sessionId,
                    'session_type': sessionType,
                    'org_loc': urllib.quote(org_loc, '')}
        purl = cancel_pay_url + '?' + urllib.urlencode(params)
        TyContext.ftlog.debug('PayTencent __cancel_pay: cancel_pay_url:', purl, 'method:',
                              method, 'params:', params, 'cookies:', _cookies)
        response, purl = TyContext.WebPage.webget(purl, {}, method_=method,
                                                  cookies=_cookies)
        TyContext.ftlog.debug('PayTencent __cancel_pay: response:', response)

        try:
            resp = json.loads(response)
            if 'ret' not in resp:
                raise ErrorWithInfo('tencent payserver error: '
                                    'no ret param in response')
            else:
                ret = resp['ret']
                if ret != 0:
                    raise ErrorWithInfo('cancel_pay_m error ret %d msg %s'
                                        % (ret, resp['msg']))
        except:
            raise ErrorWithInfo('network error')

    @classmethod
    def consume_ext_diamond(cls, params, iscancel):
        if iscancel:
            return cls.__cancel_consume_ext_diamond(params)
        else:
            return cls.__consume_ext_diamond(params)

    @classmethod
    def __consume_ext_diamond(cls, params):
        prodPrice = params['prodPrice']
        prodCount = params['prodCount']
        numDiamonds = prodPrice * prodCount

        appInfo = json.loads(params['appInfo'])
        mode = appInfo['mode']
        set_pay_urls(mode)
        appid = appInfo['appid']
        appkey = appInfo['appkey']
        openid = appInfo['openid']
        openkey = appInfo['openkey']
        pay_token = appInfo['pay_token']
        pf = appInfo['pf']
        pfkey = appInfo['pfkey']
        sessionId = appInfo.get('sessionId', 'openid')
        sessionType = appInfo.get('sessionType', 'kp_actoken')

        try:
            billno = TuyouPayTencent.__pay(openid, appid, appkey, openkey,
                                           pay_token, pf, pfkey, numDiamonds,
                                           sessionId, sessionType)
            if billno is None:
                TyContext.ftlog.error("PayTencent __consume_ext_diamond: "
                                      "billno is None")
                return False
        except ErrorWithInfo, e:
            TyContext.ftlog.error("PayTencent __consume_ext_diamond: ", e.info)
            return False

        params['billno'] = billno
        return True

    @classmethod
    def __cancel_consume_ext_diamond(cls, params):
        numDiamonds = params['prodPrice']
        billno = params['billno']

        appInfo = json.loads(params['appInfo'])
        mode = appInfo['mode']
        set_pay_urls(mode)
        appid = appInfo['appid']
        appkey = appInfo['appkey']
        openid = appInfo['openid']
        openkey = appInfo['openkey']
        pay_token = appInfo['pay_token']
        pf = appInfo['pf']
        pfkey = appInfo['pfkey']
        sessionId = appInfo.get('sessionId', 'openid')
        sessionType = appInfo.get('sessionType', 'kp_actoken')

        try:
            TuyouPayTencent.__cancel_pay(
                openid, appid, appkey, openkey, pay_token, pf, pfkey,
                numDiamonds, billno, sessionId, sessionType)
        except ErrorWithInfo, e:
            TyContext.ftlog.error("PayTencent __cancel_consume_ext_diamond: ", e.info)
            return False

        return True

    @classmethod
    def query_ext_status(cls, chargInfo):
        ''' check tencent pay delivery status '''
        userId = chargInfo['uid']
        orderPlatformId = chargInfo['platformOrderId']
        rparam = {}
        diamondCount = int(chargInfo['diamondCount'])
        diamondsPerUnit = int(chargInfo['diamondsPerUnit'])
        num_diamonds = diamondCount * diamondsPerUnit
        mi = TyContext.RunHttp.convertToMsgPack(
            ['mode', 'openid', 'appid', 'appkey', 'openkey', 'pay_token',
             'pf', 'pfkey', 'sessionId', 'sessionType'])
        TyContext.ftlog.debug('PayTencent query_ext_status mi:', mi.packJson())
        try:
            mode = mi.getParamStr('mode')
            set_pay_urls(mode)
            openid = mi.getParamStr('openid')
            appid = mi.getParamStr('appid')
            appkey = mi.getParamStr('appkey')
            openkey = mi.getParamStr('openkey')
            pay_token = mi.getParamStr('pay_token')
            pf = mi.getParamStr('pf')
            pfkey = mi.getParamStr('pfkey')
            sessionId = mi.getParamStr('sessionId')
            sessionType = mi.getParamStr('sessionType')
            if not sessionId:
                sessionId = 'openid'
                sessionType = 'kp_actoken'
            balance = TuyouPayTencent.__get_balance(
                openid, appid, appkey, openkey, pay_token, pf, pfkey, sessionId, sessionType)
        except ErrorWithInfo, e:
            TyContext.ftlog.error('PayTencent get_balance_m error:', e.info)
            return False

        userCoin = TyContext.RedisUser.execute(
            userId, 'HGET', 'user:' + str(userId), 'diamond')
        if isinstance(userCoin, (int, float)):
            userCoin = int(userCoin)
        else:
            userCoin = 0
        expected = userCoin + num_diamonds
        added = balance - userCoin
        if added > 0:
            if added != num_diamonds:
                TyContext.ftlog.error('PayTencent get_balance_m unexpected: added',
                                      added, 'expected', num_diamonds)
            # TODO RMB to diamond ratio is 1:10 now. hard-code 10.0 here.
            # refactor in the future to calculate the ratio from diamond list
            isOk = PayHelper.callback_ok(orderPlatformId, added / 10.0, rparam)
            return True
        elif added < 0:
            # isOk = PayHelper.callback_error(orderPlatformId,
            # 'diamond out-of-sync', rparam)
            TyContext.ftlog.error('PayTencent get_balance_m diamond out-of-sync: '
                                  'remote:', balance, 'local:', userCoin)
            return False
        else:
            TyContext.ftlog.debug('PayTencent get_balance_m diamond not changed:',
                                  balance)
            return False

    ##################################################################
    ######     UNUSED CODE, LEAVE FOR LATER USE      #################
    ##################################################################
    @classmethod
    def doTencentCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doTencentCallback->rparam=', rparam)
        # XXX callback should include this parameter

        sig = rparam['sig']
        if not self.verifySign(sig):
            TyContext.ftlog.info('doTencentCallback->ERROR, sig error !! sig=', sig)
            return '{"ret":0,"msg":"sig NOT OK"}'

        orderPlatformId = rparam['app_metadata']

        # if datas['result'] != 0:
        # 长连接通知，客户端支付失败
        # TyContext.ftlog.error('doTencentCallback error, charge return error !!!')
        # errorInfo = '腾讯-未知错误'
        # from tysdk.entity.pay.pay import TuyouPay
        # TuyouPay.deliveryChargeError(orderPlatformId, rparam, errorInfo, 1)
        # return 'ERROR'

        trade_status = 'TRADE_FINISHED'
        total_fee = float(rparam['amt'])
        total_fee = int(total_fee / 100)

        from tysdk.entity.pay.pay import TuyouPay
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee,
                                            trade_status, rparam)
        if isOk:
            return '{"ret":0,"msg":"OK"}'
        else:
            return '{"ret":0,"msg":"prod delivery NOT OK"}'

    @classmethod
    def verifySign(cls, sig):
        TyContext.ftlog.error('TuyouPayTencent-verifySign->transdata=', 'sign=', sig)
        return True
