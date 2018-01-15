# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayXYZSV4(PayBaseV4):
    @payv4_order('xyzs')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/xyzs/callback")
    def doXYZSPayCallback(cls, rpath):
        # 获取XY助手途游斗地主的appkey和paykey
        rparam = TyContext.RunHttp.convertArgsToDict()
        orderPlatformId = rparam["extra"]
        try:
            appid = rparam['orderid'].split('_')[0]
            keyvalue = TyContext.Configure.get_global_item_json('XYSdk_config', {})
            if keyvalue and appid in keyvalue:
                appkey = keyvalue[appid]['appkey']
                paykey = keyvalue[appid]['paykey']
            else:
                config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId)
                appkey = config.get('appkey', "")
                paykey = config.get('paykey', "")
                if not appkey or not paykey:
                    TyContext.ftlog.error('TuYouPayXYZS->doXYZSPayCallback get appkey and paykey ERROR')
                    return cls._response_result(8)
        except:
            TyContext.ftlog.error('TuYouPayXYZS->doXYZSPayCallback get appkey and paykey ERROR')
            return cls._response_result(8)
        TyContext.ftlog.debug(
            'TuYouPayXYZS->doXYZSPayCallback rparam: [%s], appid: [%s], appkey: [%s], paykey: [%s]' % (
            rparam, appid, appkey, paykey))
        return cls._docallback(appkey, paykey)

    @payv4_callback('/open/ve/pay/xyzsdj/callback')
    def doXYZSDJPayCallback(cls, rpath):
        # 获取XY助手单机斗地主的appkey和paykey
        rparam = TyContext.RunHttp.convertArgsToDict()
        orderPlatformId = rparam["extra"]
        try:
            appid = rparam['orderid'].split('_')[0]
            keyvalue = TyContext.Configure.get_global_item_json('XYDJSdk_config', {})
            if keyvalue and appid in keyvalue:
                appkey = keyvalue[appid]['appkey']
                paykey = keyvalue[appid]['paykey']
            else:
                config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId)
                appkey = config.get('appkey', "")
                paykey = config.get('paykey', "")
                if not appkey or not paykey:
                    TyContext.ftlog.error('TuYouPayXYZS->doXYZSDJPayCallback get appkey and paykey ERROR')
                    return cls._response_result(8)
        except:
            TyContext.ftlog.error('TuYouPayXYZS->doXYZSDJPayCallback get appkey and paykey ERROR')
            return cls._response_result(8)
        TyContext.ftlog.debug(
            'TuYouPayXYZS->doXYZSDJPayCallback rparam: [%s], appid: [%s], appkey: [%s], paykey: [%s]' % (
            rparam, appid, appkey, paykey))
        ChargeModel.save_third_pay_order_id(orderPlatformId, rparam.get('orderid', ''))
        return cls._docallback(appkey, paykey)

    @classmethod
    def _docallback(cls, appkey, paykey):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayXYZS->_docallback rparam is : ', rparam)

        # 验签
        safeSign = cls._gen_safe_sign(rparam, appkey)
        if safeSign != rparam['sign']:
            TyContext.ftlog.error('TuYouPayXYZS->_docallback sign verify failed, '
                                  'sign is [', safeSign, '],  rparam["sign"] is [', rparam['sign'], ']')
            return cls._response_result(6)
        if rparam['sig']:
            safeSign = cls._gen_safe_sign(rparam, paykey)
            if safeSign != rparam['sig']:
                TyContext.ftlog.error('TuYouPayXYZS->_docallback sign verify failed.'
                                      'sig is [', safeSign, '],  rparam["sig"] is [', rparam['sig'], ']')
                return cls._response_result(6)

        # 开始发货
        orderPlatformId = rparam["extra"]
        total_fee = float(rparam["amount"])
        PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        TyContext.ftlog.debug('TuYouPayXYZS->_docallback deliver goods successed.')

        return cls._response_result(0)

    # 签名方法
    @classmethod
    def _gen_safe_sign(cls, rparam, appkey):
        queryStr = appkey + '&'.join([k + '=' + rparam[k] for k in sorted(rparam.keys()) if k != 'sign' and k != 'sig'])
        TyContext.ftlog.debug('TuYouPayXYZS->_gen_safe_sign queryStr befor sign is : ', queryStr)
        sign = md5(queryStr).hexdigest()
        TyContext.ftlog.debug('TuYouPayXYZS->_gen_safe_sign queryStr after sign is : ', sign)
        return sign

    # 相应结果
    @classmethod
    def _response_result(cls, code):
        message = {
            0: '回调成功',
            1: '参数错误',
            2: '玩家不存在',
            3: '游戏服不存在',
            4: '订单已存在',
            5: '透传信息错误',
            6: '签名校验错误',
            7: '数据库错误',
            8: '其它错误'
        }
        return json.dumps({'ret': code, 'msg': message[code]})
