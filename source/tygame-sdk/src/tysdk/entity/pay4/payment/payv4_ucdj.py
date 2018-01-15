# -*- coding=utf-8 -*-
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


######################################################################
# UC单机获取订单和支付结果回掉的主要逻辑实现
# Created by Zhangshibo at 2015/09/11
# version: 1.3.0_3.3
######################################################################
class TuYouPayUcDjV4(PayBaseV4):
    @payv4_order('ucdanji')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        type_map = {'chinaunicom': 'liantongwo', 'chinamoblie': 'ydmm', 'chinanet': 'aigame'}
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}
        prodId = chargeinfo.get('buttonId', None)
        paytype = mi.getParamStr('uc_phoneType')
        try:
            paytype = type_map[paytype]
        except Exception as e:
            pass  # 之前需要传入手机类型，用来判断短代类型
        paycode = None
        ucdjPaycodeConfig = TyContext.Configure.get_global_item_json('ucdj_paycode_config', {})
        try:
            paydata = ucdjPaycodeConfig[paytype]['paydata']
        except Exception as e:
            TyContext.ftlog.debug('TuYouPayUcDj->charge_data Get paydata ERROR!', e)
        try:
            paycode = self._from_paydata_get_paycode(paydata, prodId)
        except Exception, e:
            pass  # 之前可能是需要获取运营商短代的计费点的
        TyContext.ftlog.debug('TuYouPayUcDj->charge_data paycode: [%s]' % paycode)
        if paycode:
            chargeinfo['chargeData'] = {'payData': paycode}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @classmethod
    def _from_paydata_get_paycode(cls, paydata, prodId):
        for item in paydata:
            if 0 == cmp(item['prodid'], prodId):
                return item['msgOrderCode']
        else:
            return None

    @payv4_callback('/open/ve/pay/ucdj/callback')
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
            PayHelperV4.callback_error(orderPlatformId, data['failedDesc'], rparam)
            return 'SUCCESS'

        data['third_orderid'] = thirdorderid
        total_fee = float(total_fee)
        ChargeModel.save_third_pay_order_id(orderPlatformId, thirdorderid)
        PayHelperV4.callback_ok(orderPlatformId, total_fee, data)
        return 'SUCCESS'

    @classmethod
    def __verify_sign(cls, rparam, sign):
        ucconfig = TyContext.Configure.get_global_item_json('ucdj_config', {})
        gameid = rparam['gameId']
        apiKey = ""
        try:
            ucgameidconfig = ucconfig[gameid]
            if None != ucgameidconfig:
                apiKey = str(ucgameidconfig['apiKey'])
        except:
            orderPlatformId = rparam['orderId']
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'ucdanji')
            apiKey = config.get('apiKey', "")
        check_str = ''.join([k + '=' + rparam[k] for k in sorted(rparam.keys())]) + apiKey
        digest = md5(check_str).hexdigest().lower()
        TyContext.ftlog.info('TuYouPayUcDj->doUcDjCallback verify sign: expected sign', sign,
                             'calculated', digest, 'rparam', rparam, 'check_str', check_str)
        if digest != sign:
            TyContext.ftlog.error('TuYouPayUcDj->doUcDjCallback verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
