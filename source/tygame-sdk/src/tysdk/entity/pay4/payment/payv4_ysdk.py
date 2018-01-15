# -*- coding=utf-8 -*-

import json
import time
import urllib
from base64 import b64encode
from hashlib import md5

from Crypto.Hash import SHA, HMAC

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay3.consume import tasklet_sleep
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayYsdkV4(PayBaseV4):
    session = {
        'qq': {
            'session_id': 'openid',
            'session_type': 'kp_actoken'
        },
        'wx': {
            'session_id': 'hy_gameid',
            'session_type': 'wc_actoken'
        }
    }

    @payv4_order("ysdk")
    def charge_data(self, mi):
        chargeInfo = self.get_charge_info(mi)
        chargeInfo['chargeData'] = {
            'platformOrderId': chargeInfo['platformOrderId'],
            'notifyUrl': PayHelperV4.getSdkDomain() + '/v1/pay/ysdk/callback'
        }

        return self.return_mo(0, chargeInfo=chargeInfo)

    def getPaymentUrl(cls, mi, chageInfo):
        ysdk_paydata = mi.getParamStr('ysdk_pay_data', '{}')
        paydata = json.loads(ysdk_paydata)
        ysdk_platform = paydata.get('ysdk_platform')
        cookies = cls.session.get(ysdk_platform)
        cookies['org_loc'] = '/v3/r/mpay/buy_goods_m'
        requestParams = {
            'openid': paydata.get('ysdk_openid'),
            'openkey': paydata.get('ysdk_openkey'),
            'appid': paydata.get('ysdk_appid'),
            'ts': int(time.time()),
            'payitem': '%s*%s*%s' % (chageInfo['buttonId'], int(float(chageInfo['chargeTotal']) * 10), 1),
            'goodsmeta': '%s*%s' % (chageInfo['buttonName'], chageInfo['buttonName']),
            'goodsurl': '',
            'pf': paydata.get('ysdk_pf'),
            'pfkey': paydata.get('ysdk_pfkey'),
            'zoneid': '1',
        }
        ysdk_model = paydata.get('ysdk_model')
        platformOrderId = chageInfo['platformOrderId']
        config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId, 'ysdk')
        app_key = config.get('ysdk_%s_appKey' % ysdk_model, "")
        cls.gen_sign('/mpay/buy_goods_m', app_key, requestParams)
        if ysdk_model == 'sandbox':
            pay_url = 'https://ysdktest.qq.com/mpay/buy_goods_m'
        else:
            pay_url = 'https://ysdk.qq.com/mpay/buy_goods_m'

        request_url = pay_url + '?' + urllib.urlencode(requestParams)
        try:
            response, purl = TyContext.WebPage.webget(request_url, {}, method_='GET',
                                                      cookies=cookies)
            response = json.loads(response)
            ret = response.get('ret')
            if ret == 0:
                return response.get('url_params')
        except:
            print 'request ysdk error!!'
        paymenturl = ''
        return paymenturl

    @payv4_order('ysdk.direct')
    def charge_data_direct(self, mi):
        chargeInfo = self.get_charge_info(mi)
        chargeInfo['chargeData'] = {
            'platformOrderId': chargeInfo['platformOrderId'],
            'notifyUrl': PayHelperV4.getSdkDomain() + '/v1/pay/ysdk/callback',
            'paymentUrl': self.getPaymentUrl(mi, chargeInfo)
        }
        return self.return_mo(0, chargeInfo=chargeInfo)

    @payv4_callback("/open/ve/pay/ysdk/callback")
    def doCallback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        order_id = rparams['orderId']
        price_coin = rparams['price']
        config = TyContext.Configure.get_global_item_json('ysdk_keys', {})
        app_id = rparams['ysdk_appid']
        ysdk_model = rparams['ysdk_model']
        ysdk_openId = rparams.get('ysdk_openid', '')
        ChargeModel.save_third_pay_order_id(order_id, 'openId:%s' % ysdk_openId)
        try:
            self.request_url = 'https://' + config['%s_url' % ysdk_model]
            app_key = config[app_id]['%s_appKey' % ysdk_model]
        except:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(order_id, 'ysdk')
            self.request_url = 'https://' + config.get('ysdk_%s_url' % ysdk_model, "")
            app_key = config.get('ysdk_%s_appKey' % ysdk_model, "")
            if not self.request_url or not app_key:
                return 'check sign fail'
        # 验签
        if not self.check_sign(rparams):
            return 'check sign fail'

        # 轮询金币是否到账
        has_balance = self.get_balance_m('/mpay/get_balance_m', app_key, rparams)

        if not has_balance:
            return '充值金币未到账'

        # 尝试扣除金币
        pay_response = self.pay_m('/mpay/pay_m', app_key, rparams)
        if 0 == int(pay_response['ret']) and order_id == pay_response['billno']:
            # 尝试发货
            isOk = PayHelperV4.callback_ok(order_id, -1, rparams)
            if isOk:
                return '发货成功'
            else:
                # 发货失败尝试取消扣费
                return self.cancel_pay_m('/mpay/cancel_pay_m', app_key, rparams)
        elif 1004 == int(pay_response['ret']):
            return '余额不足'
        elif 1018 == int(pay_response['ret']):
            return '登录校验失败'
        else:
            return '扣费失败'

    def get_balance_m(self, org_loc, appKey, rparams):
        price_coin = int(rparams['price'])
        request_url = '%s%s' % (self.request_url, org_loc)
        # 2分钟内间隔15秒钟多次轮询
        cookies, requests = self.build_request(org_loc, rparams)
        i = 4

        # 如果重发订单,只查询一次,防止垃圾重发超时.
        if '1' == str(rparams.get('ysdk_retry', '0')):
            TyContext.ftlog.debug('TuYouPayYsdkV4 -> get_balance_m -> is retry!')
            i = 1

        while i > 0:
            i -= 1
            ts = int(time.time())
            requests['ts'] = ts
            self.gen_sign(org_loc, appKey, requests)
            response_msg, _ = TyContext.WebPage.webget(request_url, querys=requests, cookies=cookies, method_='GET')
            TyContext.ftlog.debug('TuYouPayYsdkV4 -> get_balance_m -> response:', i, ': -> ', response_msg)
            response = json.loads(response_msg)
            if 0 == int(response['ret']):
                if int(response['balance']) >= price_coin:
                    # 全部金币准备扣除
                    rparams['pay_amt'] = response['balance']
                    return True
                else:
                    if i > 0:
                        tasklet_sleep(14)
            else:
                break
        return False

    def pay_m(self, org_loc, appKey, rparams):
        request_url = '%s%s' % (self.request_url, org_loc)
        cookies, requests = self.build_request(org_loc, rparams)

        requests['amt'] = rparams['pay_amt']
        requests['billno'] = rparams['orderId']

        self.gen_sign(org_loc, appKey, requests)
        response_msg, _ = TyContext.WebPage.webget(request_url, querys=requests, cookies=cookies, method_='GET')
        TyContext.ftlog.debug('TuYouPayYsdkV4 -> pay_m -> response ->', response_msg)
        response = json.loads(response_msg)
        return response

    def cancel_pay_m(self, org_loc, appKey, rparams):
        request_url = '%s%s' % (self.request_url, org_loc)
        cookies, requests = self.build_request(org_loc, rparams)

        requests['amt'] = rparams['pay_amt']
        requests['billno'] = rparams['orderId']

        self.gen_sign(org_loc, appKey, requests)
        response_msg, _ = TyContext.WebPage.webget(request_url, querys=requests, cookies=cookies, method_='GET')
        TyContext.ftlog.debug('TuYouPayYsdkV4 -> cancel_pay_m -> response ->', response_msg)
        response = json.loads(response_msg)
        # ret=0成功, 1018登录校验失败, 其他失败
        if 0 == int(response['ret']):
            return '发货失败, 取消支付成功'
        elif 1018 == int(response['ret']):
            return '登录校验失败'
        else:
            return '取消支付失败'

    def build_request(self, org_loc, rparams):
        _org_loc = urllib.quote(org_loc)
        order_id = rparams['orderId']
        platform = rparams['ysdk_platform']

        cookies = {
            'org_loc': _org_loc,
            'session_id': self.session[platform]['session_id'],
            'session_type': self.session[platform]['session_type']
        }

        ts = int(time.time())

        requests = {
            'openid': rparams['ysdk_openid'],
            'openkey': rparams['ysdk_openkey'],
            'appid': rparams['ysdk_appid'],
            'ts': ts,
            'pf': rparams['ysdk_pf'],
            'pfkey': rparams['ysdk_pfkey'],
            'zoneid': '1',
            'format': 'json'
        }
        TyContext.ftlog.debug('TuYouPayYsdkV4 -> build request -> cookies ->', cookies)
        return cookies, requests

    def check_sign(self, rparams):
        sign = rparams['sign']
        order_id = rparams['orderId']
        price = rparams['price']
        text = '%s%s' % (order_id, price)
        if sign != md5(text).hexdigest():
            return False
        else:
            return True

    def gen_sign(self, org_loc, appKey, requests):
        params = filter(lambda x: x[0] != '' and x[0] != 'sig', requests.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        query_text = '&'.join(params)

        v3uri = '/v3/r%s' % org_loc
        hmac_text = 'GET&%s&%s' % (urllib.quote_plus(v3uri), urllib.quote_plus(str(query_text)))

        hmac_key = '%s&' % appKey
        TyContext.ftlog.debug('TuYouPayYsdkV4 -> gen_hmac_sign ->', hmac_key, hmac_text)
        hmac_sign = HMAC.new(str(hmac_key), str(hmac_text), SHA)
        # 二进制而不是hexdigest()
        sign = b64encode(hmac_sign.digest())
        TyContext.ftlog.debug('TuYouPayYsdkV4 -> gen_hmac_sign ->', sign)
        # sign = urllib.quote_plus(sign)
        # TyContext.ftlog.debug('TuYouPayYsdkV4 -> gen_hmac_sign ->', sign)
        requests['sig'] = sign
