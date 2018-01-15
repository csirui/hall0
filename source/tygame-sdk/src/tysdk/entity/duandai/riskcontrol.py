# -*- coding=utf-8 -*-

import json

from datetime import datetime

from channels import Channels
from tyframework.context import TyContext


class RiskControl(object):
    ''' sms quota limit on user basis and device basis.
    '''

    def __init__(self, userid, devid=None):
        self._uid = userid
        if not devid:
            self._devid = TyContext.UserSession.get_session_deviceid(userid)
        else:
            self._devid = devid
        now = datetime.now()
        self._ts = int((now - datetime(1970, 1, 1)).total_seconds())
        self._month = now.strftime('%Y%m')
        self._day = now.strftime('%Y%m%d')
        self._user_quota, self._clientid, self._user_diamond_quota = TyContext.RedisUser.execute(
            self._uid, 'HMGET', 'user:' + str(self._uid),
            'payquota', 'sessionClientId', 'diamondquota')
        TyContext.ftlog.debug('RiskControl __init__ _user_quota', self._user_quota, self._user_diamond_quota,
                              self._uid, self._devid, self._ts, self._month, self._day)

    def is_limited(self, paytype):
        return self._volume_capped(paytype) or self._pay_too_fast(paytype)

    def _volume_capped(self, paytype):
        limit_month = Channels.get_personal_monthly_cap(paytype)
        limit_day = Channels.get_personal_daily_cap(paytype)
        return self._is_user_volume_capped(paytype, limit_month, limit_day) \
               or self._is_device_volume_capped(paytype, limit_month, limit_day)

    def _is_device_volume_capped(self, paytype, limit_month, limit_day):
        payquota = TyContext.RedisPayData.execute(
            'HGET', 'payquota:' + self._devid, paytype)
        if not payquota:
            return False
        quota = json.loads(payquota)
        return self._is_volume_capped(quota, limit_month, limit_day)

    def _is_user_volume_capped(self, paytype, limit_month, limit_day):
        payquota = self._user_quota
        if not payquota:
            return False
        quota = json.loads(payquota).get(paytype)
        return self._is_volume_capped(quota, limit_month, limit_day)

    def _is_volume_capped(self, quota, limit_month, limit_day):
        if not quota:
            return False
        day, dcount, mcount = quota['yyyymmdd'], quota['dcount'], quota['mcount']
        if day is None:
            return False
        day = str(day)
        month = day[:6]
        if limit_day >= 0 and day == self._day and dcount > limit_day:
            return True
        if limit_month >= 0 and month == self._month and mcount > limit_month:
            return True
        return False

    def _is_in_pay_review(self):
        waived_clientids = TyContext.Configure.get_global_item_json(
            'paytype.msg.speed.limited.waived.clientid.list', [])
        if self._clientid in waived_clientids:
            return True
        return False

    def _pay_too_fast(self, paytype):
        if self._is_in_pay_review():
            return False
        min_interval = Channels.get_min_interval(paytype)
        return self._is_user_pay_too_fast(paytype, min_interval) \
               or self._is_device_pay_too_fast(paytype, min_interval)

    def _is_user_pay_too_fast(self, paytype, min_interval):
        payquota = self._user_quota
        if not payquota:
            return False
        quota = json.loads(payquota).get(paytype)
        if self._is_pay_too_fast(quota, min_interval):
            TyContext.ftlog.info('RiskControl user', self._uid, 'is paying too fast')
            return True
        return False

    def _is_device_pay_too_fast(self, paytype, min_interval):
        payquota = TyContext.RedisPayData.execute(
            'HGET', 'payquota:' + self._devid, paytype)
        if not payquota:
            return False
        quota = json.loads(payquota).get(paytype)
        if self._is_pay_too_fast(quota, min_interval):
            TyContext.ftlog.info('RiskControl user', self._uid,
                                 'devid', self._devid, 'is paying too fast')
            return True
        return False

    def _is_pay_too_fast(self, quota, min_interval):
        if not quota:
            return False
        last_pay_ts = quota.get('last_pay_ts')
        if not last_pay_ts:
            return False
        if self._ts - last_pay_ts < min_interval:
            return True
        return False

    def _update_quota(self, payquota, amount):
        if not payquota:
            quota = {}
        else:
            quota = payquota
        day, dcount, mcount = quota.get('yyyymmdd'), quota.get('dcount'), \
                              quota.get('mcount')
        if not day:
            dcount = amount
            mcount = amount
        else:
            day = str(day)
            month = day[:6]
            TyContext.ftlog.debug('RiskControl _update_quota', day, month, dcount, mcount)
            if month != self._month:
                mcount = amount
            else:
                mcount += amount
            if day != self._day:
                dcount = amount
            else:
                dcount += amount
        quota = {'yyyymmdd': self._day, 'dcount': dcount, 'mcount': mcount, 'last_pay_ts': self._ts}
        return quota

    def _record_device_usage(self, paytype, amount):
        payquota = TyContext.RedisPayData.execute(
            'HGET', 'payquota:' + self._devid, paytype)
        if payquota:
            payquota = json.loads(payquota)
        quota = self._update_quota(payquota, amount)
        TyContext.RedisPayData.execute('HSET', 'payquota:' + self._devid,
                                       paytype, json.dumps(quota))
        TyContext.ftlog.debug('RiskControl _record_device_usage user', self._uid,
                              'payquota:' + self._devid, paytype, quota)

    def _record_user_usage(self, paytype, amount):
        if not self._user_quota:
            userquota = {}
        else:
            userquota = json.loads(self._user_quota)
        payquota = userquota.get(paytype)
        quota = self._update_quota(payquota, amount)
        userquota[paytype] = quota
        TyContext.RedisUser.execute(self._uid, 'HSET', 'user:' + str(self._uid),
                                    'payquota', json.dumps(userquota))
        TyContext.ftlog.debug('RiskControl _record_user_usage', 'user:' + str(self._uid),
                              'payquota', userquota)

    def record_usage(self, paytype, amount):
        self._record_device_usage(paytype, amount)
        self._record_user_usage(paytype, amount)

    def is_diamond_limited(self, diamondId):
        return self._is_user_diamond_limited(diamondId)

    def _is_user_diamond_limited(self, diamondId):
        diamonds_limit_config = TyContext.Configure.get_global_item_json('diamonds_limit_config', {})
        if diamondId not in diamonds_limit_config:
            return False
        diamondquota = self._user_diamond_quota
        if not diamondquota:
            return False
        quota = json.loads(diamondquota).get(diamondId)
        if self._is_buy_diamond_limited(quota, diamonds_limit_config[diamondId]):
            TyContext.ftlog.info('RiskControl user', self._uid, 'diamondId', diamondId, 'quota', quota, 'limit_config',
                                 diamonds_limit_config[diamondId])
            return True
        return False

    def _is_buy_diamond_limited(self, quota, diamonds_limit_config):
        if not quota:
            return False
        buycount, type = diamonds_limit_config.get('buycount'), diamonds_limit_config.get('type')
        day, count = quota['yyyymmdd'], quota['count']
        if day is None:
            return False
        day = str(day)
        month = day[:6]
        if type == 'day' and day == self._day and buycount >= 0 and count >= buycount:
            return True
        if type == 'month' and month == self._month and buycount >= 0 and count >= buycount:
            return True
        return False

    def record_diamond(self, diamondId):
        self._record_user_diamond(diamondId)

    def _record_user_diamond(self, diamondId):
        diamonds_limit_config = TyContext.Configure.get_global_item_json('diamonds_limit_config', {})
        if diamondId not in diamonds_limit_config:
            return

        if not self._user_diamond_quota:
            diamondquota = {}
        else:
            diamondquota = json.loads(self._user_diamond_quota)
        payquota = diamondquota.get(diamondId)
        quota = self._update_diamond_quota(payquota, diamonds_limit_config[diamondId])
        diamondquota[diamondId] = quota
        TyContext.RedisUser.execute(self._uid, 'HSET', 'user:' + str(self._uid),
                                    'diamondquota', json.dumps(diamondquota))
        TyContext.ftlog.debug('RiskControl _record_user_diamond', 'user:' + str(self._uid),
                              'diamondquota', diamondquota)

    def _update_diamond_quota(self, payquota, diamonds_limit_config):
        if not payquota:
            quota = {}
        else:
            quota = payquota
        day, count = quota.get('yyyymmdd'), quota.get('count')

        type = diamonds_limit_config.get('type')
        if type and type == 'day':
            if not day:
                count = 1
            else:
                if day != self._day:
                    count = 1
                else:
                    count += 1
        if type and type == 'month':
            if not day:
                count = 1
            else:
                day = str(day)
                month = day[:6]
                if month != self._month:
                    count = 1
                else:
                    count += 1
        quota = {'yyyymmdd': self._day, 'count': count}
        return quota
