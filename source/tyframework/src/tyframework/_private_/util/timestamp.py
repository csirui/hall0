# -*- coding=utf-8 -*-

import time

from datetime import datetime
from dateutil import relativedelta


class TimeStamp(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def get_delta_month_start_timestamp(self, timestamp=None, deltamonth=0):
        '''
        获取timestamp所在时间nmonth前后个月的开始时间，nmonth=0表示当前月, -1表示前一个月, 1表示下一个月
        '''
        timestamp = timestamp or int(time.time())
        dt = datetime.fromtimestamp(timestamp)
        delta = relativedelta(months=deltamonth)
        dt = dt + delta
        dt = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return time.mktime(dt.timetuple())

    def get_week_start_timestamp(self, timestamp=None):
        '''
        获取timestamp这个时间所在周的开始时间
        '''
        timestamp = timestamp or int(time.time())
        dt = datetime.fromtimestamp(timestamp)
        return (timestamp - dt.date().weekday() * 86400 -
                dt.hour * 3600 - dt.minute * 60 - dt.second)

    def get_day_left_seconds(self, timestamp=None):
        '''
        获取timestamp这个时间到timestamp所在的天结束时的秒数
        '''
        timestamp = timestamp or int(time.time())
        nt = time.localtime(timestamp)
        ntsec = 86400 - nt[3] * 3600 + nt[4] * 60 + nt[5]
        return ntsec

    def get_day_past_seconds(self, timestamp=None):
        '''
        获取timestamp这个时间到timestamp所在的天结束时的秒数
        '''
        timestamp = timestamp or int(time.time())
        nt = time.localtime(timestamp)
        return nt[3] * 3600 + nt[4] * 60 + nt[5]

    def get_day_start_timestamp(self, timestamp=None):
        '''
        获取timestamp这个时间戳
        '''
        timestamp = timestamp or int(time.time())
        return int(timestamp) - self.get_day_past_seconds(timestamp)

    def get_current_week_start_timestamp(self):
        ''' 
        获取本周开始的时间戳，本周开始的时间点，到当前时间的秒数
        '''
        td = datetime.today()
        now_ts = int(time.time())
        return (now_ts - td.weekday() * 86400 -
                td.hour * 3600 - td.minute * 60 - td.second)

    def get_current_day_left_seconds(self):
        '''
        获取当前时间开始，到本天结束时的秒数
        '''
        nt = time.localtime()
        ntsec = 86400 - nt[3] * 3600 + nt[4] * 60 + nt[5]
        return ntsec

    def get_current_timestamp(self):
        '''
        获取当前时间戳 int (unit: second)
        '''
        return int(time.time())

    def get_current_timestamp_f(self):
        '''
        获取当前时间戳 float (unit: second)
        '''
        return time.time()

    def get_time_str_f_diff(self, start, end):
        ''' 
        获取两个时间字符串的时间差，end-start，单位为秒
        时间字符串格式:%Y-%m-%d %H:%M:%S.%f
        '''
        t1 = datetime.strptime(start, '%Y-%m-%d %H:%M:%S.%f')
        t2 = datetime.strptime(end, '%Y-%m-%d %H:%M:%S.%f')
        diff = t2 - t1
        return diff.days * 86400 + diff.seconds

    def format_time_ms(self, ct=None):
        '''
        获取当前时间字符串:%Y-%m-%d %H:%M:%S.%f
        '''
        if ct == None:
            ct = datetime.now()
        ctfull = ct.strftime('%Y-%m-%d %H:%M:%S.%f')
        return ctfull

    def parse_time_ms(self, timestr):
        '''
        解析当前时间字符串:%Y-%m-%d %H:%M:%S.%f
        '''
        return datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S.%f')

    def format_time_second(self, ct=None):
        '''
        获取当前时间字符串:%Y-%m-%d %H:%M:%S
        '''
        if ct == None:
            ct = datetime.now()
        ctfull = ct.strftime('%Y-%m-%d %H:%M:%S')
        return ctfull

    def parse_time_second(self, timestr):
        '''
        解析当前时间字符串:%Y-%m-%d %H:%M:%S
        '''
        return datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')

    def format_time_minute(self, ct=None):
        '''
        获取当前时间字符串:%Y-%m-%d %H:%M
        '''
        if ct == None:
            ct = datetime.now()
        ctfull = ct.strftime('%Y-%m-%d %H:%M')
        return ctfull

    def parse_time_minute(self, timestr):
        '''
        解析当前时间字符串:%Y-%m-%d %H:%M
        '''
        return datetime.strptime(timestr, '%Y-%m-%d %H:%M')

    def format_time_hour(self, ct=None):
        '''
        获取当前时间字符串:%Y-%m-%d %H
        '''
        if ct == None:
            ct = datetime.now()
        ctfull = ct.strftime('%Y-%m-%d %H')
        return ctfull

    def parse_time_hour(self, timestr):
        '''
        解析当前时间字符串:%Y-%m-%d %H
        '''
        return datetime.strptime(timestr, '%Y-%m-%d %H')

    def format_time_day(self, ct=None):
        '''
        获取当前时间字符串:%Y-%m-%d
        '''
        if ct == None:
            ct = datetime.now()
        ctfull = ct.strftime('%Y-%m-%d')
        return ctfull

    def parse_time_day(self, timestr):
        '''
        解析当前时间字符串:%Y-%m-%d
        '''
        return datetime.strptime(timestr, '%Y-%m-%d')

    def format_time_day_short(self, ct=None):
        '''
        获取当前时间字符串:%Y%m%d
        '''
        if ct == None:
            ct = datetime.now()
        ctfull = ct.strftime('%Y%m%d')
        return ctfull

    def parse_time_day_short(self, timestr):
        '''
        解析当前时间字符串:%Y%m%d
        '''
        return datetime.strptime(timestr, '%Y%m%d')

    def format_time_month_short(self, ct=None):
        '''
        获取当前时间字符串:%Y%m
        '''
        if ct == None:
            ct = datetime.now()
        ctfull = ct.strftime('%Y%m')
        return ctfull

    def parse_time_month_short(self, timestr):
        '''
        解析当前时间字符串:%Y%m
        '''
        return datetime.strptime(timestr, '%Y%m')


TimeStamp = TimeStamp()
