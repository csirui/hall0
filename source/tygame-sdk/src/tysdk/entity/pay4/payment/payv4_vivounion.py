# -*- coding=utf-8 -*-

import json
from hashlib import md5

import datetime

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYouPayVivounionV4(PayBaseV4):
    @payv4_order('vivo.union')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        orderPlatformId = chargeinfo['platformOrderId']
        vivo_appId = mi.getParamStr('vivo_appId')
        appinfoconfig = TyContext.Configure.get_global_item_json('vivo_appkeys', {})
        appdata = appinfoconfig.get(str(vivo_appId), None)
        if not appdata:
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('vivo', chargeinfo[
                'packageName'],
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])
            appdata = {
                'cpid': config.get('vivo_cpid'),
                'appid': config.get('vivo_appId'),
                'cpkey': config.get('vivo_cpkey'),
            }
        cpkey = appdata['cpkey']

        url = 'https://pay.vivo.com.cn/vcoin/trade'
        params = {
            'version': '1.0.0',
            # 'signature': '',
            'cpId': appdata['cpid'],
            'appId': appdata['appid'],
            'cpOrderNumber': orderPlatformId,
            'notifyUrl': PayHelperV4.getSdkDomain() + '/v1/pay/vivounion/callback',
            'orderTime': datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
            'orderAmount': int(float(chargeinfo['chargeTotal']) * 100),
            'orderTitle': chargeinfo['buttonName'],
            'orderDesc': chargeinfo['buttonName'],
            'extInfo': orderPlatformId
        }

        sign = self.__cal_sign(params, cpkey)
        params['signature'] = sign
        params['signMethod'] = 'MD5'
        response, _ = TyContext.WebPage.webget(url, params)

        TyContext.ftlog.debug('TuYouPayVivounionV4 -> trade response ->', response)

        try:
            datas = json.loads(response)
            if int(datas['respCode']) != 200:
                raise PayErrorV4(1, 'TuYouPayVivo charge_data->order push url response ERROR, rspmsg=',
                                 datas['respMsg'])
            if not self.__verify_sign(datas, cpkey, datas['signature']):
                raise PayErrorV4(1, 'vivo 验签失败！')
            chargeinfo['chargeData'] = {'vivoOrder': datas['orderNumber'],
                                        'vivoSignature': datas['accessKey']}
            return self.return_mo(0, chargeInfo=chargeinfo)
        except:
            raise PayErrorV4(1, 'TuYouPayVivo charge_data->order push url return ERROR, response=', response)

    @payv4_callback('/open/ve/pay/vivounion/callback')
    def doVivoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        TyContext.ftlog.info('doVivoCallback->rparam=', rparam)
        orderPlatformId = rparam['cpOrderNumber']

        try:
            appinfoconfig = TyContext.Configure.get_global_item_json('vivo_appkeys', {})
            cpId = rparam['appId']
            appdata = appinfoconfig[str(cpId)]
            appKey = appdata['cpkey']
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'vivo')
            appKey = config.get('vivo_cpkey')

        sign = rparam['signature']
        if not cls.__verify_sign(rparam, appKey, sign):
            return 'fail'
        total_fee = float(rparam['orderAmount']) / 100
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'success'
        else:
            return 'fail'

    def __cal_sign(self, rparam, appkey):
        TyContext.ftlog.info('__cal_sign->rparam=', rparam)
        check_str = '&'.join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys())) + "&" + md5(
            appkey.encode('utf-8')).hexdigest().lower()
        check_str = check_str.encode('utf-8')
        digest = md5(check_str).hexdigest()
        return digest

    def __verify_sign(cls, rparam, appkey, sign):
        check_str = '&'.join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) if
                             (k != 'signMethod' and k != 'signature')) + "&" + md5(appkey).hexdigest().lower()
        digest = md5(check_str).hexdigest()
        if sign != digest:
            TyContext.ftlog.error('TuYouPayVivo verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
