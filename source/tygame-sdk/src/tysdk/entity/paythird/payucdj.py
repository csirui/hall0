# -*- coding=utf-8 -*-
from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


######################################################################
# UC单机获取订单和支付结果回掉的主要逻辑实现
# Created by Zhangshibo at 2015/09/11
# version: 1.3.0_3.3
######################################################################
class TuYouPayUcDj(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        type_map = {'chinaunicom': 'liantongwo', 'chinamoblie': 'ydmm', 'chinanet': 'aigame'}
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}
        prodId = chargeinfo.get('buttonId', None)
        payInfo = chargeinfo.get('payInfo', None)
        TyContext.ftlog.debug('TuYouPayUcDj->charge_data prodId: [%s], payInfo: [%s]' % (prodId, payInfo))
        if not prodId or not payInfo:
            return
        try:
            paytype = payInfo['appid']['ucdanji']
            # 这个版本暂时不用中国电信的计费点，所以不需要做以下的逻辑处理
            if 0 == cmp('chinanet', paytype):
                return
            paytype = type_map[paytype]
        except Exception as e:
            TyContext.ftlog.error('TuYouPayUcDj->charge_data get paytype error! ', e)
            return
        TyContext.ftlog.debug('TuYouPayUcDj->charge_data paytype: [%s]' % paytype)
        ucdjPaycodeConfig = TyContext.Configure.get_global_item_json('ucdj_paycode_config', {})
        if not ucdjPaycodeConfig:
            return
        try:
            paydata = ucdjPaycodeConfig[paytype]['paydata']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayUcDj->charge_data Get paydata ERROR!', e)
            return
        paycode = cls._from_paydata_get_paycode(paydata, prodId)
        TyContext.ftlog.debug('TuYouPayUcDj->charge_data paycode: [%s]' % paycode)
        if paycode:
            chargeinfo['chargeData'] = {'payData': paycode}

    @classmethod
    def _from_paydata_get_paycode(cls, paydata, prodId):
        for item in paydata:
            if 0 == cmp(item['prodid'], prodId):
                return item['msgOrderCode']
        else:
            return None

    @classmethod
    def doUcDjCallback(cls, rpath):
        body = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.debug('TuYouPayUcDj->doUcDjCallback Request data: ', body)
        rparam = TyContext.strutil.loads(body, decodeutf8=True)
        try:
            data = rparam['data']
            orderPlatformId = data['orderId']
            state = data['orderStatus']
            total_fee = data['amount']
            sign = rparam['sign']
            thirdorderid = data['tradeId']
        except:
            TyContext.ftlog.error('TuYouPayUcDj->doUcDjCallback ERROR, param error !! rparam=', rparam)
            return 'FAILURE'
        # 签名校验
        if not cls.__verify_sign(data, sign):
            TyContext.ftlog.error('TuYouPayUcDj->doUcDjCallback verify error !!')
            return 'FAILURE'
        # 充值状态校验
        if state != 'S':
            TyContext.ftlog.info('TuYouPayUcDj->doUcDjCallback charge failed. fail reason:', data['failedDesc'])
            PayHelper.callback_error(orderPlatformId, data['failedDesc'], rparam)
            return 'SUCCESS'

        data['third_orderid'] = thirdorderid
        total_fee = float(total_fee)
        PayHelper.callback_ok(orderPlatformId, total_fee, data)
        return 'SUCCESS'

    @classmethod
    def __verify_sign(cls, rparam, sign):
        ucconfig = TyContext.Configure.get_global_item_json('ucdj_config', {})
        gameid = rparam['gameId']
        ucgameidconfig = ucconfig[gameid]
        if None != ucgameidconfig:
            apiKey = str(ucgameidconfig['apiKey'])
        else:
            TyContext.ftlog.debug('TuYouPayUcDj->doUcDjCallback uc_config error! cannot find gameid:', gameid)
            return False
        check_str = ''.join([k + '=' + rparam[k] for k in sorted(rparam.keys())]) + apiKey
        digest = md5(check_str).hexdigest().lower()
        TyContext.ftlog.info('TuYouPayUcDj->doUcDjCallback verify sign: expected sign', sign,
                             'calculated', digest, 'rparam', rparam, 'check_str', check_str)
        if digest != sign:
            TyContext.ftlog.error('TuYouPayUcDj->doUcDjCallback verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
