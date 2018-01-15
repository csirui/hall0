# -*- coding=utf-8 -*-

from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayLangtian(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        LangtianConfigs = TyContext.Configure.get_global_item_json('Langtian_configs', {})
        price = int(float(chargeinfo['chargeTotal']))
        if not str(price) in LangtianConfigs['smscodes']:
            raise Exception('can not find Langtian price define, price=' + str(price))
        orderPlatformId = chargeinfo['platformOrderId']
        smsPort = LangtianConfigs['smsports'][str(price)]
        smscode = LangtianConfigs['smscodes'][str(price)]
        if smscode:
            smsMsg = smscode.format(
                orderId=orderPlatformId
            )
        else:
            raise Exception('can not find Langtian smscode in the price=' + price)

        # type是短信支付的方式，1代表的是发一条短信支付
        smsPayinfo = {'type': '1', 'smsMsg': smsMsg, 'smsPort': smsPort}
        chargeinfo['chargeData'] = {'smsPayinfo': smsPayinfo}

    @classmethod
    def doLangtianCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('doLangtianCallback start, rparam=', rparam)

        try:
            msg = rparam['msg']
            mobileId = rparam.get('mobile', '')
            msgList = msg.split('#')
            orderPlatformId = msgList[-1]
            sign = rparam['mac']
        except:
            TyContext.ftlog.error('doLangtianCallback->ERROR, param error !! rparam=', rparam)
            return 'error'

        # 签名校验
        if not cls.__verify_sign(rparam, sign):
            TyContext.ftlog.error('TuyouPayLangtian.doLangtianCallback sign verify error !!')
            return 'error'

        total_fee = float(rparam['fee'])
        PayHelper.set_order_mobile(orderPlatformId, mobileId)
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'success'
        else:
            return 'error'

    @classmethod
    def __verify_sign(cls, rparam, sign):
        LangtianConfigs = TyContext.Configure.get_global_item_json('Langtian_configs', {})
        check_str = (rparam['mobile']
                     + rparam['linkId']
                     + rparam['longCode']
                     + rparam['msg']
                     + rparam['status']
                     + rparam['fee']
                     + str(LangtianConfigs['key']))
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().upper()
        if digest != sign:
            TyContext.ftlog.error('TuyouPayLangtian verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
