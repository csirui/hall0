# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import datetime


class SmsPayCheck(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def __update_sms_pay_info_cal__(self, rmb, yyyymmdd, yyyymm, dcount, mcount):

        if rmb <= 0:
            if dcount == None or mcount == None:
                return '', '', 0, 0, False

        if yyyymmdd == None:
            yyyymmdd = ''
        else:
            yyyymmdd = str(yyyymmdd)
        if yyyymm == None:
            yyyymm = ''
        else:
            yyyymm = str(yyyymm)
        if dcount == None:
            dcount = 0
        if mcount == None:
            mcount = 0

        change = False
        mnow = datetime.datetime.now()
        mnowstr = mnow.strftime('%Y%m')
        if mnowstr != yyyymm:
            yyyymm = mnowstr
            mcount = 0
            change = True

        mnowstr = mnow.strftime('%Y%m%d')
        if mnowstr != yyyymmdd:
            yyyymmdd = mnowstr
            dcount = 0
            change = True

        if rmb > 0:
            change = True
        mcount += rmb
        dcount += rmb
        return yyyymmdd, yyyymm, dcount, mcount, change

    def update_sms_pay_info(self, userId, rmb):
        self.__ctx__.ftlog.debug('update_sms_pay_info userId=', userId, 'rmb=', rmb)
        sms_pay_limit = self.__ctx__.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sms_pay_limit')
        yyyymmdd, yyyymm, dcount1, mcount1 = None, None, None, None
        if sms_pay_limit:
            try:
                sms_pay_limit = self.__ctx__.strutil.loads(sms_pay_limit)
                yyyymmdd, yyyymm, dcount1, mcount1 = sms_pay_limit['yyyymmdd'], sms_pay_limit['yyyymm'], sms_pay_limit[
                    'dcount'], sms_pay_limit['mcount']
            except:
                yyyymmdd, yyyymm, dcount1, mcount1 = None, None, None, None
        yyyymmdd, yyyymm, dcount1, mcount1, change1 = self.__update_sms_pay_info_cal__(rmb, yyyymmdd, yyyymm, dcount1,
                                                                                       mcount1)
        if change1:
            sms_pay_limit = {'yyyymmdd': yyyymmdd, 'yyyymm': yyyymm, 'dcount': dcount1, 'mcount': mcount1}
            sms_pay_limit = self.__ctx__.strutil.dumps(sms_pay_limit)
            self.__ctx__.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'sms_pay_limit', sms_pay_limit)

        dcount2, mcount2 = 0, 0
        sDevId = self.__ctx__.UserSession.get_session_deviceid(userId)
        if sDevId != None and len(sDevId) > 0:
            yyyymmdd, yyyymm, dcount2, mcount2 = self.__ctx__.RedisPayData.execute('HMGET', 'pay:' + sDevId, 'yyyymmdd',
                                                                                   'yyyymm', 'dcount', 'mcount')
            yyyymmdd, yyyymm, dcount2, mcount2, change2 = self.__update_sms_pay_info_cal__(rmb, yyyymmdd, yyyymm,
                                                                                           dcount2, mcount2)
            if change2:
                self.__ctx__.RedisPayData.execute('HMSET', 'pay:' + sDevId, 'yyyymmdd', yyyymmdd, 'yyyymm', yyyymm,
                                                  'dcount', dcount2, 'mcount', mcount2)
                self.__ctx__.RedisPayData.execute('EXPIRE', 'pay:' + sDevId, 86400 * 32)

        dcount = max(dcount1, dcount2)
        mcount = max(mcount1, mcount2)
        return dcount, mcount

    def update_sms_pay_info_by_type(self, userId, rmb, payType):
        self.__ctx__.ftlog.debug('update_sms_pay_info_by_type payType=', payType, 'coin=', rmb, 'userId=', userId)
        msgpayttpes = ['linkyun', 'linkyununion', 'ydmm', 'huafubao', 'liantong.wo', 'newYinHe', '360.ydmm',
                       '360.liantong.wo']
        msgpayttpes = self.__ctx__.Configure.get_global_item_json('paytype.msg.limited.list', msgpayttpes)
        if rmb > 0 and payType in msgpayttpes:
            self.update_sms_pay_info(userId, rmb)

    def append_sms_pay_limit_info(self, userId, datas):
        datas['msgpaylimit'] = 0
        dcount, mcount = self.update_sms_pay_info(userId, 0)
        self.__ctx__.ftlog.debug('append_sms_pay_limit_info->msg->dcount, mcount=', dcount, mcount, 'userId=', userId)
        limit_month = self.__ctx__.Configure.get_global_item_int('paytype.msg.limited.month', 290)
        limit_day = self.__ctx__.Configure.get_global_item_int('paytype.msg.limited.day', 50)
        if dcount >= limit_day or mcount > limit_month:
            datas['msgpaylimit'] = 1

    def is_sms_pay_limited(self, userId):
        dcount, mcount = self.update_sms_pay_info(userId, 0)
        limit_month = self.__ctx__.Configure.get_global_item_int('paytype.msg.limited.month', 290)
        limit_day = self.__ctx__.Configure.get_global_item_int('paytype.msg.limited.day', 50)
        self.__ctx__.ftlog.debug('is_sms_pay_limited userId=', userId,
                                 'dcount', dcount, 'mcount', mcount,
                                 'limit_month', limit_month, 'limit_day', limit_day)
        if dcount >= limit_day or mcount > limit_month:
            return 1
        return 0

    def update_sms_pay_timestamp(self, userId, paytype):
        msgpayttpes = self.__ctx__.Configure.get_global_item_json(
            'paytype.msg.speed.limited.list', [])
        if paytype not in msgpayttpes:
            return
        ts = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
        self.__ctx__.RedisUser.execute(userId, 'HSET', 'user:' + str(userId),
                                       'last_smspay_ts', ts)
        self.__ctx__.ftlog.debug('update_sms_pay_timestamp userId', userId, 'last_smspay_ts', ts)

    def is_sms_pay_speed_limited(self, userId, paytype):
        clientId = self.__ctx__.UserSession.get_session_clientid(userId)
        waived_clientids = self.__ctx__.Configure.get_global_item_json(
            'paytype.msg.speed.limited.waived.clientid.list', [])
        if clientId in waived_clientids:
            return 0
        msgpayttpes = self.__ctx__.Configure.get_global_item_json(
            'paytype.msg.speed.limited.list', [])
        if paytype not in msgpayttpes:
            return 0
        last_ts = self.__ctx__.RedisUser.execute(
            userId, 'HGET', 'user:' + str(userId), 'last_smspay_ts')
        if not last_ts:
            return 0
        min_interval = self.__ctx__.Configure.get_global_item_int(
            'paytype.msg.speed.min.interval', 90)
        ts = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
        if ts - last_ts > min_interval:
            return 0
        self.__ctx__.ftlog.info('is_sms_pay_speed_limited userId=', userId,
                                'paytype', paytype)
        return 1


SmsPayCheck = SmsPayCheck()
