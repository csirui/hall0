# -*- coding=utf-8 -*-

from hashlib import md5

from constants import PHONETYPE_INTS
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class TuYouMaoPao(object):
    @classmethod
    def charge_data(cls, chargeinfo):

        platformOrderId = chargeinfo['platformOrderId']
        prodPrice = int(chargeinfo['chargeTotal']) * 100
        charge = int(chargeinfo['chargeTotal'])
        prodName = chargeinfo['diamondName']
        callbackAddress = PayHelper.getSdkDomain() + '/v1/pay/maopao/callback'

        prodPayMethod = ''
        maopaoConfig = TyContext.Configure.get_global_item_json('maopao_config', {})

        phoneType = TyContext.UserSession.get_phone_type_name(chargeinfo['phoneType'])

        if charge in maopaoConfig['paysms'] and PHONETYPE_INTS[phoneType] != 1:
            prodPayMethod = 'sms'
            payInfo = chargeinfo['payInfo']
            maopaoAppid = payInfo['appid']['maopao_appid']
            typroductId = chargeinfo['buttonId']
            payPointNum = '-1'
            if maopaoAppid in maopaoConfig:
                maopaoAppidPayNum = maopaoConfig[maopaoAppid]
                if typroductId in maopaoAppidPayNum:
                    payPointNum = maopaoAppidPayNum[typroductId]
                    TyContext.ftlog.debug('doMaopaoCallback payInfo', payInfo, 'maopaoAppid', maopaoAppid,
                                          'typroductId', typroductId)
        else:
            prodPayMethod = '3rd'
            payPointNum = '1'

        TyContext.ftlog.debug('doMaopaoCallback payPointNum', payPointNum)

        chargeinfo['chargeData'] = {'platformOrderId': platformOrderId, 'prodPrice': prodPrice,
                                    'prodName': prodName, 'prodPayMethod': prodPayMethod,
                                    'callbackAddress': callbackAddress, 'payPointNum': payPointNum}

    @classmethod
    def doMaopaoPayCallback(cls, rpath):

        rparam = TyContext.RunHttp.convertArgsToDict()

        maopaoInfo = {}
        maopaoInfo['orderId'] = rparam['orderId']
        maopaoInfo['skyId'] = rparam['skyId']
        maopaoInfo['resultCode'] = rparam['resultCode']
        maopaoInfo['payNum'] = rparam['payNum']
        maopaoInfo['cardType'] = rparam['cardType']
        maopaoInfo['realAmount'] = rparam['realAmount']
        maopaoInfo['payTime'] = rparam['payTime']
        maopaoInfo['failure'] = rparam['failure']
        maopaoInfo['signMsg'] = rparam['signMsg']

        rparam['third_orderid'] = maopaoInfo['payNum']
        rparam['chargeType'] = 'maopao'

        maopaoConfig = TyContext.Configure.get_global_item_json('maopao_config', {})
        md5key = maopaoConfig['md5key']

        signParams = rparam['orig_uri']
        signInfo = signParams[signParams.find('?') + 1:signParams.find('signMsg') - 1] + '&' + 'key' + '=' + md5key

        TyContext.ftlog.info('doMaopaoCallback signInfo', signInfo)

        total_fee = int(maopaoInfo['realAmount']) / 100
        orderPlatformId = maopaoInfo['orderId']

        sign = cls._cal_sign(signInfo)
        TyContext.ftlog.debug('doMaopaoCallback  sign', sign, 'signMsg', maopaoInfo['signMsg'], 'signInfo', signInfo)

        if sign == maopaoInfo['signMsg']:
            if int(maopaoInfo['realAmount']) > 0:
                PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
                TyContext.ftlog.info('doMaopaoCallback->SUCCESSFUL rparam', rparam)
                return 'result=0'
            else:
                errinfo = '支付失败'
                PayHelper.callback_error(orderPlatformId, errinfo, rparam)
                TyContext.ftlog.error('doMaopaoCallback->ERROR, failDesc', errinfo, 'rparam', rparam)
        else:
            errinfo = '签名校验失败'
            PayHelper.callback_error(orderPlatformId, errinfo, rparam)
            TyContext.ftlog.error('doMaopaoCallback->ERROR, failDesc', errinfo, 'rparam', rparam)
        return 'result=0'

    @classmethod
    def _cal_sign(cls, signInfo):
        m = md5()
        m.update(signInfo)
        digest = m.hexdigest().upper()
        return digest
