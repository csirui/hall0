#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'

# coding=utf-8
# from: http://blog.ipattern.org/archives/417

import datetime


# input datetime1, and an month offset
# return the result datetime
def datetime_offset_by_month(datetime1, n=1):
    # create a shortcut object for one day
    one_day = datetime.timedelta(days=1)

    # first use div and mod to determine year cycle
    q, r = divmod(datetime1.month + n, 12)

    # create a datetime2
    # to be the last day of the target month
    datetime2 = datetime.datetime(
        datetime1.year + q, r + 1, 1) - one_day

    # if input date is the last day of this month
    # then the output date should also be the last
    # day of the target month, although the day
    # may be different.
    # for example:
    # datetime1 = 8.31
    # datetime2 = 9.30
    if datetime1.month != (datetime1 + one_day).month:
        return datetime2

    # if datetime1 day is bigger than last day of
    # target month, then, use datetime2
    # for example:
    # datetime1 = 10.31
    # datetime2 = 11.30
    if datetime1.day >= datetime2.day:
        return datetime2

    # then, here, we just replace datetime2's day
    # with the same of datetime1, that's ok.
    return datetime2.replace(day=datetime1.day)


class AlipayHuiyuan:
    def __init__(self, appId, userId):
        self.appId = appId
        self.userId = userId

    def handle_sign(self):
        nextMonth = datetime_offset_by_month(datetime.datetime.now()).toordinal()
        TyContext.RedisUserKeys.execute("ZADD", "huiyuan:alipay:%d:members" % self.appId, nextMonth, self.userId)
        TyContext.RedisUser.execute(self.userId, 'HSET', 'user:%d' % self.userId, 'isAlipayHuiyuan', '1')

    def handle_unsign(self):
        TyContext.RedisUserKeys.execute("ZREM", "huiyuan:alipay:%d:members" % self.appId, self.userId)
        TyContext.RedisUser.execute(self.userId, 'HSET', 'user:%d' % self.userId, 'isAlipayHuiyuan', '0')

    def handle_order(self, chargeInfo):
        TyContext.RedisUserKeys.execute("HMSET", "huiyuan:alipay:%d:%d" % self.appId, self.userId,
                                        'chargeTotal', chargeInfo['chargeTotal'],
                                        'prodId', chargeInfo['prodId'],
                                        'platformOrderId', chargeInfo['platformOrderId'],
                                        'clientId', chargeInfo['clientId'],
                                        )

    def get_renew_info(self):
        pass
