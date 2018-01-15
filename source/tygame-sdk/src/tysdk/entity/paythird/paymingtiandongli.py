# -*- coding=utf-8 -*-

import json
from collections import OrderedDict
from hashlib import md5

from datetime import datetime

from constants import PHONETYPE_CHINAMOBILE, PHONETYPE_CHINAUNION, PHONETYPE_CHINATELECOM
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.duandai.smspayinfo import SmsPayInfo


class TuYouPayMingTianDongLiApi(object):
    createorder_url = ''

    @classmethod
    def charge_data(cls, chargeinfo):
        TyContext.ftlog.info('TuYouPayMingTianDongLiApi->chargeinfo', chargeinfo)

        userId = chargeinfo['uid']
        fee = chargeinfo['chargeTotal']
        orderPlatformId = chargeinfo['platformOrderId']
        ct = datetime.now()
        provider = ''

        phoneType = TyContext.UserSession.get_phone_type_name(chargeinfo['phoneType'])
        if phoneType == PHONETYPE_CHINAMOBILE:
            provider = 'YD'
        elif phoneType == PHONETYPE_CHINAUNION:
            provider = 'LT'
        elif phoneType == PHONETYPE_CHINATELECOM:
            provider = 'DX'
        else:
            provider = ''

        mingtiandongliconfig = TyContext.Configure.get_global_item_json('mingtiandongli_config', {})
        cls.createorder_url = mingtiandongliconfig['createorderUrl']
        rparams = OrderedDict()

        rparams['iccid_params'] = TyContext.UserSession.get_session_iccid(userId)
        rparams['imei_params'] = TyContext.UserSession.get_session_imei(userId)
        rparams['imsi_params'] = TyContext.UserSession.get_session_imsi(userId)
        rparams['ipAddress'] = TyContext.UserSession.get_session_client_ip(userId)
        rparams['channelNum'] = mingtiandongliconfig['channelNum']
        rparams['appID'] = '4944'
        rparams['price_params'] = fee
        rparams['cpParams'] = orderPlatformId
        rparams['provider'] = provider
        rparams['req_date'] = ct.strftime('%Y-%m-%d %H:%M:%S')
        rparams['orderId'] = ''

        # 明天动力,验签暂时关闭.
        # strSign = cls._cal_sign(rparams)
        # rparams['sign'] = strSign
        # TyContext.ftlog.debug('TuYouPayMingTianDongLiApi->rparams', rparams)

        response_msg, _ = TyContext.WebPage.webget(cls.createorder_url, rparams, method_='GET')
        response = json.loads(response_msg)
        TyContext.ftlog.debug('TuYouPayMingTianDongLiApi->response', str(response).strip("u'"))
        param = eval(str(response).strip("u'"))
        TyContext.ftlog.debug('TuYouPayMingTianDongLiApi->response', str(response), 'param', param)

        if 0 != int(param['result']):
            TyContext.ftlog.error('TuYouPayMingTianDongLiApi->create_order failed for user', userId,
                                  'errorCode', param['errorCode'])
            return

        # 当返回的reAccess值为2时,需要重新向服务器发送请求,其他参数为空,运营商标示和上次返回orderId发送即可
        if 2 == int(param['reAccess']):
            secondParams = rparams
            for i in secondParams.key():
                secondParams[i] = ''
            secondParams['provider'] = rparams['provider']
            secondParams['orderId'] = param['orderId']
            response_msg, _ = TyContext.WebPage.webget(cls.createorder_url, rparams, method_='GET')
            response = json.loads(response_msg)
            param = eval(response)
            TyContext.ftlog.debug('TuYouPayMingTianDongLi->response', str(response), 'param', param)

        messages = []

        messages.append((param['port1'], param['command1'], int(param['millons'])))

        # 当返回的order为2时,需要发送两条请求.
        if 2 == int(param['order']):
            messages.append((param['port2'], param['command2'], 0))

        no_hint = chargeinfo.get('nohint', None)
        payinfo = SmsPayInfo.build_sms_payinfo(messages, nohint=no_hint)
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
        TyContext.ftlog.info('TuYouPayMingTianDongLi _get_sms_payinfo chargeData',
                             chargeinfo['chargeData'])
        return

    @classmethod
    def doMingTianDongLiApiCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doMingTianDongLiApiCallback rparam', rparam)

        '''strSoureSign = md.encode(channelNum + appId + price + cpparams + 
        subChannelNum + imei + provider + province + mobile + number'''

        strSoureSign = rparam['channelNum'] + rparam['appId'] + rparam['price'] + \
                       rparam['cpparams'] + rparam['subChannelNum'] + rparam['imei'] + \
                       rparam['provider'] + rparam['province'] + rparam['mobile'] + \
                       rparam['number']

        if not cls._verify_sign(strSoureSign, rparam['sign']):
            TyContext.ftlog.error('doMingTianDongLiApiCallback->ERROR  invalid strSoureSign',
                                  strSoureSign, 'rparam[sign]', rparam['sign'])
            return 'error'

        orderPlatformId = rparam['cpparams']
        total_fee = float(rparam['price']) / 100

        if rparam['mobile']:
            mobileId = rparam['mobile']
            PayHelper.set_order_mobile(orderPlatformId, mobileId)

        PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        return 0

    @classmethod
    def _cal_sign(cls, rparams):
        strSign = ''.join([str(rparams[k]) for k in rparams.keys()])
        TyContext.ftlog.debug('TuYouPayMingTianDongLi->strSign', strSign)
        m = md5()
        m.update(strSign)
        digest = m.hexdigest().lower()
        return digest

    @classmethod
    def _verify_sign(cls, strSource, sign):
        m = md5()
        m.update(strSource)
        digest = m.hexdigest().lower()
        if digest != sign:
            TyContext.ftlog.error('doMingTianDongLiApiCallback verify sign failed: expected sign', sign,
                                  'calculated', digest, 'strSource', strSource)
            return False
        return True
