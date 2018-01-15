# -*- coding=utf-8 -*-

from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap


# paytype: linkyun.ido
class TuYouPayIDO(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        prodId = chargeinfo.get("prodId", chargeinfo['diamondId'])
        prodconfig = TyContext.Configure.get_global_item_json('IDO_prodids', {})
        smscodeconfig = TyContext.Configure.get_global_item_json('IDO_smscodes', {})
        data = prodconfig[str(appId)].get(prodId, None)
        if data:
            amount = data['price']
        else:
            raise Exception('can not find IDO product define of prodId=' + prodId)

        orderPlatformId = chargeinfo['platformOrderId']
        shortOrderPlatformId = ShortOrderIdMap.get_short_order_id(orderPlatformId)
        smsPort = '1065889920'
        smscode = smscodeconfig.get(str(amount), None)
        if smscode:
            smsMsg = smscode.format(
                orderId=shortOrderPlatformId + '00'
            )
        else:
            raise Exception('can not find IDO smscode in the price=' + amount)

        # type是短信支付的方式，1代表的是发一条短信支付
        smsPayinfo = {'type': '1', 'smsMsg': smsMsg, 'smsPort': smsPort}
        chargeinfo['chargeData'] = {'smsPayinfo': smsPayinfo}

    @classmethod
    def doIDOCallback(cls, rpath):
        TyContext.ftlog.info('doIDOCallback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderidconfig = TyContext.Configure.get_global_item_json('IDO_orderid', {})
            start = orderidconfig.get(str(rparam['price']), None)[0]
            end = orderidconfig.get(str(rparam['price']), None)[1]
            shortOrderPlatformId = rparam['order_code'][start:end]
            orderPlatformId = ShortOrderIdMap.get_long_order_id(shortOrderPlatformId)
            sign = rparam['sign']
        except:
            TyContext.ftlog.error('doIDOCallback->ERROR, param error !! rparam=', rparam)
            return 'error'

        # 签名校验
        if not cls.__verify_sign(rparam, sign):
            TyContext.ftlog.error('TuyouPayIDO.doIDOCallbacksign verify error !!')
            return 'error'

        rparam['chargeType'] = 'linkyun.ido'
        rparam['third_orderid'] = rparam['orderID']
        total_fee = float(rparam['price']) / 100
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
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
