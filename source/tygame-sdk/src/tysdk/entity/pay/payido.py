# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap


class TuyouPayIDO(object):
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        appId = params['appId']
        prodId = params['prodId']
        prodconfig = TyContext.Configure.get_global_item_json('IDO_prodids', {})
        smscodeconfig = TyContext.Configure.get_global_item_json('IDO_smscodes', {})
        data = prodconfig[str(appId)].get(prodId, None)
        if data:
            amount = data['price']
        else:
            raise Exception('can not find IDO product define of prodId=' + prodId)

        orderPlatformId = params['orderPlatformId']
        sortOrderPlatformId = ShortOrderIdMap.get_short_order_id(orderPlatformId)
        smsPort = '1065889920'
        smscode = smscodeconfig.get(str(amount), None)
        if smscode:
            smsMsg = smscode.format(
                orderId=sortOrderPlatformId + '00'
            )
        else:
            raise Exception('can not find IDO smscode in the price=' + amount)

        # type是短信支付的方式，1代表的是发一条短信支付
        smsPayinfo = {'type': '1', 'smsMsg': smsMsg, 'smsPort': smsPort}
        mo.setResult('smsPayinfo', smsPayinfo)

    @classmethod
    def doIDOCallback(cls, rpath):
        TyContext.ftlog.info('doIDOCallback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderidconfig = TyContext.Configure.get_global_item_json('IDO_orderid', {})
            start = orderidconfig.get(str(rparam['price']), None)[0]
            end = orderidconfig.get(str(rparam['price']), None)[1]
            sortOrderPlatformId = rparam['order_code'][start:end]
            orderPlatformId = ShortOrderIdMap.get_long_order_id(sortOrderPlatformId)
            sign = rparam['sign']
        except:
            TyContext.ftlog.error('doIDOCallback->ERROR, param error !! rparam=', rparam)
            return 'error'

            # 签名校验
        if not cls.__verify_sign(rparam, sign):
            TyContext.ftlog.error('TuyouPayIDO.doIDOCallbacksign verify error !!')
            return 'error'

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            return 'successful'
        else:
            return 'error'

    @classmethod
    def __verify_sign(cls, rparam, sign):
        check_str = (rparam['order_code']
                     + rparam['channelID']
                     + rparam['price']
                     + rparam['orderID']
                     + rparam['version'])
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuyouPayIDO verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
