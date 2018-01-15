# -*- coding=utf-8 -*-
import time
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayNubiaV4(PayBaseV4):
    @payv4_order("nubia")
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        app_id = mi.getParamStr('nubia_appId')
        uid = mi.getParamStr('nubia_uid')
        config = TyContext.Configure.get_global_item_json('nubia_keys', {})
        try:
            secret = config[app_id]['secret']
        except KeyError:
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_primarykey('nubia',
                                                                                                     'nubia_appId',
                                                                                                     app_id, chargeinfo[
                                                                                                         'mainChannel'])
            secret = config.get('secret')
        timestamp = int(time.time())
        price = chargeinfo['diamondPrice']
        order_id = chargeinfo['platformOrderId']
        number = chargeinfo['diamondCount']
        goodsname = chargeinfo['diamondName']

        charge_key = 'sdk.charge:nubia:%s' % order_id
        TyContext.RedisPayData.execute('HSET', charge_key, 'appId', app_id)
        TyContext.RedisPayData.execute('EXPIRE', charge_key, 60 * 60)
        text = 'amount=%s&app_id=%s&cp_order_id=%s&data_timestamp=%s&number=%s&product_des=%s&product_name=%s&uid=%s' \
               ':%s:%s' % (price, app_id, order_id, timestamp, number, goodsname, goodsname, uid, app_id, secret)

        sign = md5(text).hexdigest()

        chargeinfo['chargeData'] = {
            'platformOrderId': order_id,
            'timestamp': timestamp,
            'uid': uid,
            'sign': sign
        }
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/nubia/callback")
    def doCallback(self, rpath):
        # convertArgsToDict
        rparams = TyContext.RunHttp.convertArgsToDict()
        order_id = rparams['order_no']
        charge_key = 'sdk.charge:nubia:%s' % order_id
        app_id = TyContext.RedisPayData.execute('HGET', charge_key, 'appId')
        TyContext.ftlog.debug('TuYouPayNubia->doCallback, rparams=', rparams)
        TyContext.ftlog.debug('TuYouPayNubia->doCallback->appId=', app_id)
        if not self.check_sign(rparams, str(app_id)):
            return '{"code":90000,"data":{},"message":"验签失败"}'

        isok = PayHelperV4.callback_ok(order_id, -1, rparams)
        if isok:
            return '{"code":0,"data":{},"message":"成功"}'
        else:
            return '{"code":10000,"data":{},"message":"发货失败"}'

    def check_sign(self, rparams, app_id):
        order_no = rparams['order_no']
        data_timestamp = rparams['data_timestamp']
        config = TyContext.Configure.get_global_item_json('nubia_keys', {})
        try:
            secret = config[app_id]['secret']
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(order_no)
            secret = config.get('secret')
        sign = rparams['sign']

        text = 'data_timestamp=%s&order_no=%s:%s:%s' % (data_timestamp, order_no, app_id, secret)

        if sign != md5(text).hexdigest():
            return False
        else:
            return True
