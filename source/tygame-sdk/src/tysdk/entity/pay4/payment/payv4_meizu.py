# -*- coding=utf-8 -*-
'''
Created on 2015-5-21

@author: tiancz
'''
import json
import time
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYouPayMeizuV4(PayBaseV4):
    @payv4_order("meizu")
    def charge_data(cls, mi):
        chargedata = {}
        chargeinfo = cls.get_charge_info(mi)
        mz_appId = mi.getParamStr('mz_appId')
        if not mz_appId:
            raise PayErrorV4(1, '【魅族】mz_appId没有找到！')
        chargedata['app_id'] = mz_appId
        chargedata['cp_order_id'] = chargeinfo['platformOrderId']
        mz_uid = mi.getParamStr('mz_uid')
        if not mz_uid:
            raise PayErrorV4(1, '【魅族】没有找到mz_uid参数!')
        chargedata['uid'] = mi.getParamStr('mz_uid')
        chargedata['product_id'] = chargeinfo['buttonId']
        chargedata['product_subject'] = chargeinfo['diamondName']
        chargedata['product_body'] = chargeinfo['diamondName']
        chargedata['product_unit'] = ''
        chargedata['buy_amount'] = chargeinfo['diamondCount']
        chargedata['product_per_price'] = chargeinfo['diamondPrice']
        chargedata['total_price'] = chargeinfo['chargeTotal']
        chargedata['create_time'] = int(time.time())
        chargedata['pay_type'] = '0'
        chargedata['user_info'] = chargeinfo['clientId']
        chargedata['sign_type'] = 'md5'
        sign = cls._calc_sign(chargedata)
        chargedata['sign'] = sign
        chargeinfo['chargeData'] = chargedata
        TyContext.ftlog.info('TuYouPayMeizu charge_data chargeinfo ', chargeinfo)
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/meizu/callback")
    def doMeizuPayCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doMeizuPayCallback rparam', rparam)
        cp_order_id = None
        try:
            cp_order_id = rparam['cp_order_id']
            total_price = float(rparam['total_price'])
            trade_status = rparam['trade_status']
            ChargeModel.save_third_pay_order_id(cp_order_id, rparam.get('order_id', ''))
        except Exception as e:
            TyContext.ftlog.error('doMeizuCallback param error, exception',
                                  e, 'cp_order_id', cp_order_id)
            return json.dumps({'code': 900000, 'message': '参数不匹配',
                               'redirect': '', 'value': None})
        if not cls._check_sign(rparam):
            TyContext.ftlog.error('TuYouPayMeizu _check_sign failed', cp_order_id)
            return json.dumps({'code': 900000, 'message': '签名错误',
                               'redirect': '', 'value': None})
        if trade_status == '3':
            PayHelperV4.callback_ok(cp_order_id, total_price, rparam)
            return json.dumps({'code': 200, 'message': '充值成功',
                               'redirect': '', 'value': None})
        elif trade_status == '4':
            PayHelperV4.callback_error(cp_order_id, '订单取消', rparam)
            return json.dumps({'code': 900000, 'message': '',
                               'redirect': '', 'value': None})
        elif trade_status == '1' or trade_status == '2':
            return json.dumps({'code': 90000, 'message': '订单处理中',
                               'redirect': '', 'value': None})
        elif trade_status == '5':
            return json.dumps({'code': 90000, 'message': '订单异常取消',
                               'redirect': '', 'value': None})

    def _check_sign(cls, rparam):
        return rparam['sign'] == cls._calc_sign(rparam)

    def _calc_sign(cls, rparam):
        meizu_config = TyContext.Configure.get_global_item_json('meizu_config', {})
        try:
            app_key = meizu_config[rparam['app_id']]['appkey']
        except KeyError:
            orderId = rparam['cp_order_id']
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderId, 'meizu')
            app_key = config.get('mz_appSecret')
        query = "&".join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) \
                         if k != 'sign' and k != 'sign_type')
        TyContext.ftlog.debug('TuYouMeizuPay _calc_sign ,query', query)
        m = md5()
        m.update(query + ':' + app_key)
        return m.hexdigest().lower()
