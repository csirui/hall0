#! encoding=utf-8
import time

from datetime import date

from tyframework.context import TyContext
from tysdk.entity.pay4.decorator.payv4_filter import payv4_filter
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import TuYouPayAliV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4

__author__ = 'yuejianqiang'


class TuYouPayAliBigV4(TuYouPayAliV4):
    @payv4_filter('alibig')
    def filter_alibig(self, payment, prod_info, **kwargs):
        userId = kwargs['userId']
        clientId = kwargs['clientId']
        alibig_config = TyContext.Configure.get_global_item_json('alibig_config', {})
        userList = alibig_config.get('userList', [])
        clientList = alibig_config.get('clientList', [])
        if not int(userId) in userList or not clientId in clientList:
            return False
        timestamp, count = TyContext.RedisPayData.execute('HMGET', 'alibig:%s' % userId, 'timestamp', 'count')
        now = date.fromtimestamp(int(time.time()))
        if not timestamp or now.toordinal() != date.fromtimestamp(int(timestamp)).toordinal():
            count = 0
        if count >= alibig_config.get('limitCount', 0):
            return False
        payment['name'] = alibig_config['paymentName']
        payment['tips'] = alibig_config['paymentTips']
        return True

    @payv4_order('alibig')
    def order_alibig(self, mi):
        userId = mi.getParamInt('userId')
        clientId = mi.getParamStr('clientId')
        alibig_config = TyContext.Configure.get_global_item_json('alibig_config', {})
        userList = alibig_config.get('userList', [])
        clientList = alibig_config.get('clientList', [])
        if not userId in userList or not clientId in clientList:
            raise PayErrorV4(-1, "用户信息错误")
        mi.setParam('prodId', alibig_config['prodId'])
        mi.setParam('prodCount', alibig_config['prodCount'])
        mi.setParam('prodName', alibig_config['prodName'])
        chargeInfo = self.get_charge_info(mi)
        return self.return_mo(0, chargeInfo=chargeInfo)

    def get_consume_info(self, chargeInfo):
        alibig_config = TyContext.Configure.get_global_item_json('alibig_config', {})
        consumeInfo = super(TuYouPayAliBigV4, self).get_consume_info(chargeInfo)
        chargeInfo['chargeCoin'] = int(alibig_config['prodPrice'] * 10)
        consumeInfo['consumeCoin'] = int(alibig_config['prodPrice'] * 10)
        chargeInfo['chargeTotal'] = alibig_config['prodPrice']
        return consumeInfo
