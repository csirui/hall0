# -*- coding=utf-8 -*-
'''
Created on 2014-11-3

@author: Administrator
'''
import json
from hashlib import md5

import datetime

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYouPayVivoV4(PayBaseV4):
    @payv4_order('vivo')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        appId = chargeinfo['appId']
        diamondId = chargeinfo['buttonId']
        orderPlatformId = chargeinfo['platformOrderId']
        vivo_appId = mi.getParamStr('vivo_appId')
        if not vivo_appId:
            raise PayErrorV4(1, '沒有找到参数vivo_appId！')

        pramas = {}
        pramas['version'] = '1.0.0'
        pramas['orderTitle'] = chargeinfo['buttonName']
        pramas['orderDesc'] = chargeinfo['buttonName']
        pramas['orderAmount'] = '%.2f' % chargeinfo['chargeTotal']

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
        pramas['storeId'] = appdata['cpid']
        pramas['appId'] = appdata['appid']
        notifyurl = PayHelperV4.getSdkDomain() + '/v1/pay/vivo/callback'
        pramas['notifyUrl'] = notifyurl
        pramas['storeOrder'] = orderPlatformId

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        pramas['orderTime'] = timestamp
        cpkey = appdata['cpkey']
        sign = self.__cal_sign(pramas, cpkey)
        pramas['signature'] = sign
        pramas['signMethod'] = 'MD5'

        orderpushurl = 'https://pay.vivo.com.cn/vivoPay/getVivoOrderNum'
        TyContext.ftlog.debug('TuYouPayVivo->order push url->', orderpushurl)
        response, orderpushurl = TyContext.WebPage.webget(orderpushurl, pramas)
        try:
            datas = json.loads(response)
            if int(datas['respCode']) != 200:
                raise PayErrorV4(1, 'TuYouPayVivo charge_data->order push url response ERROR, rspmsg=',
                                 datas['respMsg'])
            if not self.__verify_sign(datas, cpkey, datas['signature']):
                raise PayErrorV4(1, 'vivo 验签失败！')
            chargeinfo['chargeData'] = {'vivoOrder': datas['vivoOrder'],
                                        'vivoSignature': datas['vivoSignature']}
            return self.return_mo(0, chargeInfo=chargeinfo)
        except:
            raise PayErrorV4(1, 'TuYouPayVivo charge_data->order push url return ERROR, response=', response)

    @payv4_order('vivo.alipay')
    def charge_date_alipay(self, mi):
        return self.charge_data(mi)

    @payv4_order('vivo.weixin')
    def charge_data_weixin(self, mi):
        return self.charge_data(mi)

    @payv4_callback('/open/ve/pay/vivo/callback')
    def doVivoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        TyContext.ftlog.info('doVivoCallback->rparam=', rparam)
        orderPlatformId = rparam['storeOrder']

        try:
            appinfoconfig = TyContext.Configure.get_global_item_json('vivo_appkeys', {})
            cpId = rparam['storeId']
            appdata = appinfoconfig[str(cpId)]
            appKey = appdata['cpkey']
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'vivo')
            appKey = config.get('vivo_cpkey')
        sign = rparam['signature']
        if not cls.__verify_sign(rparam, appKey, sign):
            return 'ERROR'
        total_fee = float(rparam['orderAmount'])
        ChargeModel.save_third_pay_order_id(rparam.get('vivoOrder', ''))
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'SUCCESS'
        else:
            return 'ERROR'

    def __cal_sign(self, rparam, appkey):
        check_str = '&'.join(k + "=" + rparam[k] for k in sorted(rparam.keys())) + "&" + md5(
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
