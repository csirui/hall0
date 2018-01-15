# -*- coding=utf-8 -*-

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPay360Msg():
    # 订单回调签名验证key
    sign_skey = 'TUYOU!Qaz2wsx360msg'

    # 第三方支付初始化数据
    CHARGE_DATA = {
        'D20': {'issms': 1, 'msgOrderCode': '001'},
        'D50': {'issms': 1, 'msgOrderCode': '005'}
    }

    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = cls.CHARGE_DATA[chargeinfo['diamondId']]

    @classmethod
    def callback(cls, rpath):
        success = 0
        try:
            rparam = PayHelper.getArgsDict()
            TyContext.ftlog.info(cls.__name__, 'callback rparam=', rparam)

            platformOrderId = rparam['platformOrderId']
            sign = rparam['sign']
            result = rparam['result']

            isOK = PayHelper.verify_md5(sign, platformOrderId, result, cls.sign_skey)
            if isOK:
                if result == '1':
                    isBackOk = PayHelper.callback_ok(platformOrderId, -1, rparam)
                    if isBackOk:
                        success = 1
                else:
                    PayHelper.callback_error(platformOrderId, '', rparam)
        except:
            TyContext.ftlog.exception()

        return '{"result":{"success":%d,"platformOrderId":"%s"}}' % (success, platformOrderId)
