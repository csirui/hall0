#! encoding=utf-8
from tysdk.entity.pay4.charge_model import ChargeModel

__author__ = 'yuejianqiang'

from hashlib import md5

from tyframework.context import TyContext
from payv4_helper import PayHelperV4
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.decorator.payv4_order import payv4_order


class TuYouIIAppleV4(PayBaseV4):
    @payv4_order('iiApple')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/iiapple/callback')
    def doCallback(cls, rpath):
        iiapple_paykeys = TyContext.Configure.get_global_item_json('iiapple_paykeys', {})
        secretKey = iiapple_paykeys['secretKey']
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouIIApple callback with: %s' % rparam)
        ## verify sign
        keys = filter(lambda x: x != '_sign', rparam.keys())
        keys.sort()
        text = '&'.join(['%s=%s' % (x, rparam[x]) for x in keys])
        m = md5()
        m.update(text)
        m2 = md5()
        m2.update('%s%s' % (m.hexdigest().lower(), secretKey))
        if rparam['_sign'] != m2.hexdigest().lower():
            TyContext.ftlog.error('doIDOCallback->ERROR, sign error !! rparam=', rparam)
            return 'error'
        # do charge

        # from tysdk.entity.pay.pay import TuyouPay
        trade_status = rparam['status']
        orderPlatformId = rparam['gameExtend']
        # isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        ChargeModel.save_third_pay_order_id(orderPlatformId, rparam.get('transaction', ''))
        isOk = PayHelperV4.callback_ok(orderPlatformId, -1, rparam)
        if isOk:
            return '{"status":0, "transIDO":"%s"}' % orderPlatformId
        else:
            return '{"status":1, "transIDO":"%s"}' % orderPlatformId
