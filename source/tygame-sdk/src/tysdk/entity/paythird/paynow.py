#! encoding=utf-8

__author__ = 'yuejianqiang'

import hashlib
import urllib

from datetime import datetime

from helper import PayHelper
from tyframework.context import TyContext


class TuYouNow(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        borui_paykeys = TyContext.Configure.get_global_item_json('borui_paykeys', {})
        clientId = chargeinfo['clientId']
        payNowAppId = borui_paykeys.get(clientId, '')
        try:
            payNowInfo = borui_paykeys[payNowAppId]
        except KeyError:
            payNowInfo = borui_paykeys
        appSecret = payNowInfo['appSecret']
        chargeData = {
            # 'platformOrderId' : chargeinfo['platformOrderId'],
            'appId': payNowInfo['appId'],  #
            'mhtOrderNo': chargeinfo['platformOrderId'],
            'mhtOrderName': chargeinfo['buttonName'],
            'mhtOrderType': '01',  # 普通消费
            'mhtCurrencyType': '156',  # 人民币
            'mhtOrderAmt': int(float(chargeinfo['chargeTotal']) * 100),  # 单位分
            'mhtOrderDetail': chargeinfo['buttonName'],
            'mhtOrderTimeOut': 3600,
            'mhtOrderStartTime': datetime.now().strftime('%Y%m%d%H%M%S'),
            'notifyUrl': payNowInfo['notifyUrl'],
            'mhtCharset': 'UTF-8',
            'payChannelType': chargeinfo.get('payChannelType', None),  # 支付宝
            'mhtReserved': payNowInfo['mhtReserved'],
        }
        keys = chargeData.keys()
        keys.sort()
        keys = filter(lambda x: chargeData[x], keys)
        text = '&'.join(['%s=%s' % (k, chargeData[k]) for k in keys])
        sign1 = hashlib.md5(appSecret).hexdigest()
        sign2 = hashlib.md5('%s&%s' % (text.encode('utf-8'), sign1)).hexdigest()
        chargeData['mhtSignature'] = sign2
        chargeData['mhtSignType'] = 'MD5'
        chargeData['consumerId'] = chargeinfo['uid']
        chargeData['consumerName'] = chargeinfo['uid']
        chargeinfo['chargeData'] = chargeData

    @classmethod
    def doCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouNow callback with: %s' % rparam)
        payNowAppId = rparam['appId']
        borui_paykeys = TyContext.Configure.get_global_item_json('borui_paykeys', {})
        try:
            payNowInfo = borui_paykeys[payNowAppId]
        except KeyError:
            payNowInfo = borui_paykeys
        appSecret = payNowInfo['appSecret']
        ## check signature
        keys = filter(lambda k: k not in ['signType', 'signature', ], rparam.keys())
        keys.sort()
        text = '&'.join(['%s=%s' % (k, rparam[k]) for k in keys])
        text = urllib.unquote(text)  # 转为utf－8编码
        s1 = hashlib.md5(appSecret).hexdigest()
        s2 = hashlib.md5('%s&%s' % (text, s1)).hexdigest()
        if rparam['signature'] != s2:
            TyContext.ftlog.error('TuYouNow->ERROR, sign error !! rparam=', rparam)
            return 'N'
        # do charge
        tradeStatus = rparam['tradeStatus']
        orderPlatformId = rparam['mhtOrderNo']
        if tradeStatus == 'A001':
            if PayHelper.callback_ok(orderPlatformId, -1, rparam):
                return 'Y'
        return 'N'
