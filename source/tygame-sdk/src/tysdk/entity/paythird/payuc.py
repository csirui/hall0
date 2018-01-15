# -*- coding=utf-8 -*-
from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayUc(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/uc/callback'
        TyContext.ftlog.debug('TuYouPayUc charge_data callback url=', notifyurl)
        chargeinfo['chargeData'] = {'notifyUrl': notifyurl}

    @classmethod
    def doUcCallback(cls, rpath):
        TyContext.ftlog.debug('doUcCallback start')
        body = TyContext.RunHttp.get_body_content()
        rparam = TyContext.strutil.loads(body, decodeutf8=True)
        data = rparam['data']

        try:
            orderPlatformId = data['cpOrderId']
            state = data['orderStatus']
            total_fee = data['amount']
            sign = rparam['sign']
            thirdorderid = data['orderId']
        except:
            TyContext.ftlog.error('TuYouPayUc.doUcCallback->ERROR, param error !! rparam=', rparam)
            return 'SUCCESS'
        # 签名校验
        if not cls.__verify_sign(data, sign):
            TyContext.ftlog.error('TuYouPayUc.doUcCallback verify error !!')
            return 'FAILURE'
        # 充值状态校验
        if state != 'S':
            TyContext.ftlog.info('TuYouPayUc.doUcCallback, charge failed. fail reason:', data['failedDesc'])
            PayHelper.callback_error(orderPlatformId, data['failedDesc'], rparam)
            return 'SUCCESS'

        rparam['chargeType'] = 'uc'
        rparam['third_orderid'] = thirdorderid
        total_fee = float(total_fee)
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, data)
        return 'SUCCESS'

    @classmethod
    def __verify_sign(cls, rparam, sign):
        ucconfig = TyContext.Configure.get_global_item_json('uc_config', {})
        gameid = rparam['gameId']
        ucgameidconfig = ucconfig[gameid]
        if None != ucgameidconfig:
            apiKey = str(ucgameidconfig['apiKey'])
        else:
            TyContext.ftlog.debug('uc_config error! cannot find gameid:', gameid)
            return False
        check_str = ('accountId=' + rparam['accountId']
                     + 'amount=' + rparam['amount']
                     + 'callbackInfo=' + rparam['callbackInfo']
                     + 'cpOrderId=' + rparam['cpOrderId']
                     + 'creator=' + rparam['creator']
                     + 'failedDesc=' + rparam['failedDesc']
                     + 'gameId=' + rparam['gameId']
                     + 'orderId=' + rparam['orderId']
                     + 'orderStatus=' + rparam['orderStatus']
                     + 'payWay=' + rparam['payWay']
                     + apiKey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayUc.doUcCallback verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
