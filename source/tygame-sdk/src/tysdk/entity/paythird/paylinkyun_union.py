# -*- coding=utf-8 -*-

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay3.constants import PayConst


# 同时包含linkyununion和linkyundx的支持
class TuYouPayLinkYunUnion():
    # 订单签名验证key
    sign_skey = 'lywuxian'

    @classmethod
    def doLinkYunUnionConfirm(cls, rpath):
        rparam = PayHelper.getArgsDict()
        TyContext.ftlog.info(cls.__name__, 'doLinkYunUnionConfirm->args=', rparam)
        try:
            mobileId = rparam['mobile']
            serviceid = rparam['serviceid']
            orderId = rparam['orderid']
            orderPlatformId = str(rparam['orderid'])[2:]
            sign = rparam['sign']
            # 效验sign=mobile#serviceid#orderid#密钥
            isOk = PayHelper.verify_md5(sign, mobileId, '#', serviceid, '#', orderId, '#', cls.sign_skey)
            if isOk:
                orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
                TyContext.RunMode.get_server_link(orderPlatformId)
                order_state = TyContext.RedisPayData.execute('HGET', 'sdk.charge:' + str(orderPlatformId), 'state')
                if order_state is not None and int(order_state) >= PayConst.CHARGE_STATE_BEGIN and int(
                        order_state) < PayConst.CHARGE_STATE_DONE:
                    return '0'
        except:
            TyContext.ftlog.exception()
        TyContext.ftlog.info(cls.__name__, 'doLinkYunUnionConfirm->ERROR, rparam=', rparam)
        return '1'

    @classmethod
    def doLinkYunUnionCallback(cls, rpath):
        rparam = PayHelper.getArgsDict()
        TyContext.ftlog.info(cls.__name__, 'doLinkYunUnionCallback->args=', rparam)
        try:
            mobileId = rparam['mobile']
            serviceid = rparam['serviceid']
            orderPlatformId = str(rparam['orderid'])[2:]
            msgcontent = rparam['msgcontent']
            sign = rparam['sign']

            # 效验sign
            isOk = PayHelper.verify_md5(sign, mobileId, '#', serviceid, '#', msgcontent, '#', cls.sign_skey)
            if isOk:
                # 对凌云充值的订单，把手机号补充到订单信息里
                orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
                TyContext.RunMode.get_server_link(orderPlatformId)
                PayHelper.set_order_mobile(orderPlatformId, mobileId)
                operator = PayHelper.get_mobile_operator(mobileId)
                if operator == 'chinaunicom':
                    rparam['chargeType'] = 'linkyununion'
                elif operator == 'chinatelecom':
                    rparam['chargeType'] = 'linkyundx'
                else:
                    TyContext.ftlog.error(cls.__name__,
                                          'doLinkYunUnionCallback->ERROR get_mobile_operator for',
                                          mobileId)
                if msgcontent == '0:0':
                    PayHelper.callback_ok(orderPlatformId, -1, rparam)
                    return '0'
                else:
                    PayHelper.callback_error(orderPlatformId, '', rparam)
        except:
            TyContext.ftlog.exception()
        TyContext.ftlog.info(cls.__name__, 'doLinkYunUnionCallback->ERROR, rparam=', rparam)
        return '0'
