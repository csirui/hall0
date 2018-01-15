# -*- coding=utf-8 -*-
from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayJiuxiu(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {}

    @classmethod
    def doJiuxiuCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doJiuxiuCallback start rparam=', rparam)

        try:
            orderPlatformId = rparam['orderPlatformId']
            total_fee = rparam['amount']
            sign = rparam['sign']
            thirdorderid = rparam['orderId']
        except:
            TyContext.ftlog.error('doJiuxiuCallback->ERROR, param error !! rparam=', rparam)
            return 'fail'
        # 签名校验
        if not cls.__verify_sign(rparam, sign):
            TyContext.ftlog.error('TuYouPayJiuxiu.doJiuxiuCallback verify error !!')
            return 'fail'

        rparam['chargeType'] = '9xiu'
        rparam['third_orderid'] = thirdorderid
        total_fee = float(total_fee)
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'success'
        else:
            return 'fail'

    @classmethod
    def __verify_sign(cls, rparam, sign):
        ucconfig = TyContext.Configure.get_global_item_json('9xiu_config', {})
        gameid = rparam['gameId']
        apiKey = ucconfig[gameid]
        if not apiKey:
            TyContext.ftlog.debug('9xiu_config error! cannot find gameid:', gameid)
            return False
        check_str = (rparam['orderPlatformId']
                     + '_' + rparam['gameId']
                     + '_' + apiKey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest.lower() != sign.lower():
            TyContext.ftlog.error('TuYouPayJiuxiu.doJiuxiuCallback verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
