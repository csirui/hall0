# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayDuoKu():
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        buttonId = chargeinfo['buttonId']
        clientId = chargeinfo['clientId']
        packageName = chargeinfo.get('packageName')
        prodconfig = TyContext.Configure.get_global_item_json('duoku_prodids')

        if packageName:
            try:
                appconfig = prodconfig[packageName]
                payData = appconfig[buttonId]
            except:
                TyContext.ftlog.exception()
                raise Exception('can not find duoku product define: buttonId=' + buttonId + ' clientId=' + clientId)
        else:
            try:
                appconfig = prodconfig[str(appId)]
                payData = appconfig[buttonId]
            except Exception as e:
                TyContext.ftlog.exception()
                raise Exception('can not find duoku product define: buttonId='
                                + buttonId + ' clientId=' + clientId)
        orderPlatformId = chargeinfo['platformOrderId']
        shortOrderPlatformId = ShortOrderIdMap.get_short_order_id(orderPlatformId)
        payData['orderPlatformId'] = shortOrderPlatformId
        chargeinfo['chargeData'] = payData

    @classmethod
    def doDuoKuCallback(cls, rpath):
        TyContext.ftlog.info('doDuoKuCallback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            shortOrderPlatformId = rparam['cpdefinepart']
            orderPlatformId = ShortOrderIdMap.get_long_order_id(shortOrderPlatformId)
            appId = rparam['appid']
            sign = rparam['sign']
            unit = rparam['unit']
            amount = rparam['amount']
            status = rparam['status']
            mobileId = rparam.get('phone', '')
        except:
            TyContext.ftlog.info('doDuoKuCallback->ERROR, param error !! rparam=', rparam)
            TyContext.ftlog.exception()
            return 'failure'
        if status != 'success':
            PayHelper.callback_error(orderPlatformId, 'pay fail', rparam)
            return 'failure'

        paykey_dict = TyContext.Configure.get_global_item_json('duoku_paykeys', {})
        paykey = str(paykey_dict[str(appId)])

        # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            return 'failure'

        if unit == 'fen':
            total_fee = float(amount) / 100
        else:
            total_fee = float(amount)

        rparam['chargeType'] = 'duoku'
        rparam['third_orderid'] = rparam['orderid']
        PayHelper.set_order_mobile(orderPlatformId, mobileId)
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        check_str = (rparam['appid']
                     + rparam['orderid']
                     + rparam['amount']
                     + rparam['unit']
                     + rparam['status']
                     + rparam['paychannel']
                     + paykey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayDuoKu verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
