# -*- coding=utf-8 -*-
import time
from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayNubia(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        payInfo = chargeinfo['payInfo']
        app_id = payInfo['appid']['nubia_appid']
        uid = payInfo['appid']['nubia_uid']
        config = TyContext.Configure.get_global_item_json('nubia_keys', {})
        secret = config[app_id]['secret']
        timestamp = int(time.time())
        price = chargeinfo['diamondPrice']
        order_id = chargeinfo['platformOrderId']
        number = chargeinfo['diamondCount']
        goodsname = chargeinfo['diamondName']

        charge_key = 'sdk.charge:nubia:%s' % order_id
        TyContext.RedisPayData.execute('HSET', charge_key, 'appId', app_id)
        text = 'amount=%s&app_id=%s&cp_order_id=%s&data_timestamp=%s&number=%s&product_des=%s&product_name=%s&uid=%s' \
               ':%s:%s' % (price, app_id, order_id, timestamp, number, goodsname, goodsname, uid, app_id, secret)

        sign = md5(text).hexdigest()

        chargeinfo['chargeData'] = {
            'platformOrderId': order_id,
            'timestamp': timestamp,
            'uid': uid,
            'sign': sign
        }

    @classmethod
    def doCallback(cls, rpath):
        # convertArgsToDict
        rparams = TyContext.RunHttp.convertArgsToDict()
        order_id = rparams['order_no']

        charge_key = 'sdk.charge:nubia:%s' % order_id
        app_id = TyContext.RedisPayData.execute('HGET', charge_key, 'appId')

        TyContext.ftlog.debug('TuYouPayNubia->doCallback, rparams=', rparams)
        if not cls.check_sign(rparams, str(app_id)):
            return '{"code":90000,"data":{},"message":"验签失败"}'

        isok = PayHelper.callback_ok(order_id, -1, rparams, app_id)
        if isok:
            return '{"code":0,"data":{},"message":"成功"}'
        else:
            return '{"code":10000,"data":{},"message":"发货失败"}'

    @classmethod
    def check_sign(cls, rparams, app_id):
        order_no = rparams['order_no']
        data_timestamp = rparams['data_timestamp']
        config = TyContext.Configure.get_global_item_json('nubia_keys', {})
        secret = config[app_id]['secret']
        sign = rparams['sign']

        text = 'data_timestamp=%s&order_no=%s:%s:%s' % (data_timestamp, order_no, app_id, secret)

        if sign != md5(text).hexdigest():
            return False
        else:
            return True
