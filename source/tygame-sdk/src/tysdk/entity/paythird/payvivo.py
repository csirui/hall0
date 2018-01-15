# -*- coding=utf-8 -*-
'''
Created on 2014-11-3

@author: Administrator
'''
import json
from hashlib import md5

import datetime

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayVivo(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        diamondId = chargeinfo['buttonId']
        orderPlatformId = chargeinfo['platformOrderId']
        clientId = chargeinfo['clientId']
        if 'payInfo' in chargeinfo and chargeinfo['payInfo']:
            payInfo = chargeinfo['payInfo']
            if 'appid' in payInfo and payInfo['appid']['vivo']:
                clientId = payInfo['appid']['vivo']

        pramas = {}
        pramas['version'] = '1.0.0'
        pramas['orderTitle'] = chargeinfo['buttonName']
        pramas['orderDesc'] = chargeinfo['buttonName']
        pramas['orderAmount'] = '%.2f' % chargeinfo['chargeTotal']

        appinfoconfig = TyContext.Configure.get_global_item_json('vivo_appkeys', {})
        appdata = appinfoconfig.get(str(clientId), None)
        if not appdata:
            raise Exception('can not find app info define of clientId=' + clientId)

        pramas['storeId'] = appdata['cpid']
        pramas['appId'] = appdata['appid']
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/vivo/callback'
        pramas['notifyUrl'] = notifyurl
        pramas['storeOrder'] = orderPlatformId

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        pramas['orderTime'] = timestamp
        cpkey = appdata['cpkey']
        sign = cls.__cal_sign(pramas, cpkey)
        pramas['signature'] = sign
        pramas['signMethod'] = 'MD5'

        orderpushurl = 'https://pay.vivo.com.cn/vivoPay/getVivoOrderNum'
        TyContext.ftlog.debug('TuYouPayVivo->order push url->', orderpushurl)
        response, orderpushurl = TyContext.WebPage.webget(orderpushurl, pramas)
        try:
            datas = json.loads(response)
            if int(datas['respCode']) != 200:
                TyContext.ftlog.error('TuYouPayVivo charge_data->order push url response ERROR, rspmsg=',
                                      datas['respMsg'])
                return
            if not cls.__verify_sign(datas, cpkey, datas['signature']):
                return
            chargeinfo['chargeData'] = {'vivoOrder': datas['vivoOrder'],
                                        'vivoSignature': datas['vivoSignature']}
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.error('TuYouPayVivo charge_data->order push url return ERROR, response=', response)

    @classmethod
    def doVivoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        TyContext.ftlog.info('doVivoCallback->rparam=', rparam)
        orderPlatformId = rparam['storeOrder']

        appinfoconfig = TyContext.Configure.get_global_item_json('vivo_appkeys', {})
        cpId = rparam['storeId']
        appdata = appinfoconfig.get(str(cpId), None)
        appKey = appdata['cpkey']
        sign = rparam['signature']
        if not cls.__verify_sign(rparam, appKey, sign):
            return 'ERROR'
        total_fee = float(rparam['orderAmount'])
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'SUCCESS'
        else:
            return 'ERROR'

    @classmethod
    def __cal_sign(cls, rparam, appkey):
        check_str = '&'.join(k + "=" + rparam[k] for k in sorted(rparam.keys())) + "&" + md5(
            appkey.encode('utf-8')).hexdigest().lower()
        check_str = check_str.encode('utf-8')
        digest = md5(check_str).hexdigest()
        return digest

    @classmethod
    def __verify_sign(cls, rparam, appkey, sign):
        check_str = '&'.join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) if
                             (k != 'signMethod' and k != 'signature')) + "&" + md5(appkey).hexdigest().lower()
        digest = md5(check_str).hexdigest()
        if sign != digest:
            TyContext.ftlog.error('TuYouPayVivo verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
