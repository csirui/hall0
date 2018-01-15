#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'

"""
DB: TyContext.RedisPayData
TYPE: hash
KEY: online:appId:userId
PROPERTIES: {'timestamp':timePoint, 'daily':duration, 'weekly':duration, 'monthly':duration, 'total':duration}


if day(timestamp) != day(now): today = 0
if week(timestamp) != week(now): weekly = 0
if month(timestamp) != month(now): monthly = 0

"""

import time
from datetime import date


class ReportModel(object):
    def getLastTimestamp(self, appId, userId):
        assert appId > 0
        assert userId > 0
        key = 'online:%s:%s' % (appId, userId)
        timestamp = TyContext.RedisPayData.execute('HGET', key, 'timestamp')
        if not timestamp:
            timestamp = int(time.time())
            TyContext.RedisPayData.execute('HMSET', key,
                                           'timestamp', timestamp,
                                           'daily', 0,
                                           'weekly', 0,
                                           'monthly', 0,
                                           'total', 0)
        return int(timestamp)

    def checkOnline(self, appId, userId):
        timestamp = int(time.time())
        lastTimestamp = self.getLastTimestamp(appId, userId)
        key = 'online:%s:%s' % (appId, userId)
        now = date.fromtimestamp(timestamp)
        last = date.fromtimestamp(lastTimestamp)
        delta = timestamp - lastTimestamp
        # 5 minutes offline
        if delta > 5 * 60:
            delta = 0
        # day change
        if now.toordinal() != last.toordinal():
            daily = int(TyContext.RedisPayData.execute('HGET', key, 'daily'))
            TyContext.RedisPayData.execute('HSET', key, 'daily', 0)
            # week change
            if now.weekday() <= last.weekday() or now.toordinal() - last.toordinal() >= 7:
                TyContext.RedisPayData.execute('HSET', key, 'weekly', 0)
            else:
                weekly = TyContext.RedisPayData.execute('HGET', key, 'weekly')
                TyContext.RedisPayData.execute('HSET', key, 'weekly', weekly + daily)
            # month change
            if now.year != last.year or now.month != last.month:
                TyContext.RedisPayData.execute('HSET', key, 'monthly', 0)
            else:
                monthly = TyContext.RedisPayData.execute('HGET', key, 'monthly')
                TyContext.RedisPayData.execute('HSET', key, 'monthly', monthly + daily)
        # 累计在线时间
        elif delta > 0:
            daily = int(TyContext.RedisPayData.execute('HGET', key, 'daily'))
            TyContext.RedisPayData.execute('HSET', key, 'daily', daily + delta)
        # set timestamp
        TyContext.RedisPayData.execute('HSET', key, 'timestamp', timestamp)

    def queryOnline(self, appId, userId):
        key = 'online:%s:%s' % (appId, userId)
        timestamp, daily, weekly, monthly, total = TyContext.RedisPayData.execute('HMGET', key, 'timestamp', 'daily',
                                                                                  'weekly', 'monthly', 'total')
        now = date.fromtimestamp(int(time.time()))
        last = date.fromtimestamp(timestamp)
        if now.toordinal() != last.toordinal():
            self.checkOnline(appId, userId)
        if not timestamp:
            daily, weekly, monthly, total = 0, 0, 0, 0
        return {"daily": daily,
                "weekly": weekly + daily,
                "monthly": monthly + daily,
                "total": total + daily}
