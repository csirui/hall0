#! encoding=utf-8
import datetime

from tyframework.context import TyContext
from tysdk.entity.huiyuan.alipay_huiyuan import datetime_offset_by_month

__author__ = 'yuejianqiang'


class WeixinHuiyuan:
    def __init__(self, appId, userId):
        self.appId = appId
        self.userId = userId

    def handle_sign(self):
        nextMonth = datetime_offset_by_month(datetime.datetime.now()).toordinal()
        TyContext.RedisUserKeys.execute("ZADD", "huiyuan:weixin:%d:members" % self.appId, nextMonth, self.userId)
        TyContext.RedisUser.execute(self.userId, 'HSET', 'user:%d' % self.userId, 'isWeixinHuiyuan', '1')

    def handle_unsign(self):
        TyContext.RedisUserKeys.execute("ZREM", "huiyuan:weixin:%d:members" % self.appId, self.userId)
        TyContext.RedisUser.execute(self.userId, 'HSET', 'user:%d' % self.userId, 'isWeixinHuiyuan', '0')

    def handle_order(self, chargeInfo):
        TyContext.RedisUserKeys.execute("HMSET", "huiyuan:weixin:%d:%d" % self.appId, self.userId,
                                        'chargeTotal', chargeInfo['chargeTotal'],
                                        'prodId', chargeInfo['prodId'],
                                        'platformOrderId', chargeInfo['platformOrderId'],
                                        'clientId', chargeInfo['clientId'])

    def get_renew_info(self):
        prodId, clientId = TyContext.RedisUserKeys.execute("HMGET", "huiyuan:weixin:%d:%d" % self.appId, self.userId,
                                                           'prodId', 'clientId')
        return {
            'appId': self.appId,
            'clientId': clientId,
            'userId': self.userId,
            'prodId': prodId,
        }
