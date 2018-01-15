# -*- coding=utf-8 -*-

from hashlib import md5

from constants import PHONETYPE_INTS
from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYouMaoPaoV4(PayBaseV4):
    @payv4_order('maopao')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        platformOrderId = chargeinfo['platformOrderId']
        prodPrice = int(chargeinfo['chargeTotal']) * 100
        charge = int(chargeinfo['chargeTotal'])
        prodName = chargeinfo['diamondName']
        callbackAddress = PayHelperV4.getSdkDomain() + '/v1/pay/maopao/callback'

        prodPayMethod = ''
        maopaoConfig = TyContext.Configure.get_global_item_json('maopao_config', {})

        phoneType = TyContext.UserSession.get_phone_type_name(chargeinfo['phoneType'])
        maopaoAppid = mi.getParamStr('maopao_appId')
        if not maopaoAppid:
            raise PayErrorV4(1, '【冒泡】maopao_appId参数 没有！')
        if charge in maopaoConfig['paysms'] and PHONETYPE_INTS[phoneType] != 1:
            prodPayMethod = 'sms'
            typroductId = chargeinfo['buttonId']
            payPointNum = '-1'
            if maopaoAppid in maopaoConfig:
                maopaoAppidPayNum = maopaoConfig[maopaoAppid]
                if typroductId in maopaoAppidPayNum:
                    payPointNum = maopaoAppidPayNum[typroductId]
                    TyContext.ftlog.debug('doMaopaoCallback payInfo', 'maopaoAppid', maopaoAppid, 'typroductId',
                                          typroductId)
            else:
                raise PayErrorV4(1, '【冒泡】ID [%s] 没有[%s]计费点配置！', maopaoAppid, typroductId)
        else:
            prodPayMethod = '3rd'
            payPointNum = '1'

        TyContext.ftlog.debug('doMaopaoCallback payPointNum', payPointNum)

        chargeinfo['chargeData'] = {'platformOrderId': platformOrderId, 'prodPrice': prodPrice,
                                    'prodName': prodName, 'prodPayMethod': prodPayMethod,
                                    'callbackAddress': callbackAddress, 'payPointNum': payPointNum}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/maopao/callback')
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
                ChargeModel.save_third_pay_order_id(orderPlatformId, maopaoInfo['payNum'])
                PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
                TyContext.ftlog.info('doMaopaoCallback->SUCCESSFUL rparam', rparam)
                return 'result=0'
            else:
                errinfo = '支付失败'
                PayHelperV4.callback_error(orderPlatformId, errinfo, rparam)
                TyContext.ftlog.error('doMaopaoCallback->ERROR, failDesc', errinfo, 'rparam', rparam)
        else:
            errinfo = '签名校验失败'
            PayHelperV4.callback_error(orderPlatformId, errinfo, rparam)
            TyContext.ftlog.error('doMaopaoCallback->ERROR, failDesc', errinfo, 'rparam', rparam)
        return 'result=0'

    @classmethod
    def _cal_sign(cls, signInfo):
        m = md5()
        m.update(signInfo)
        digest = m.hexdigest().upper()
        return digest
