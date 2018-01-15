# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import datetime

from tyframework.context import TyContext


class TuyouPayCheck(object):
    @classmethod
    def updateMsgPayByDev(cls, coin, userId):
        sDevId = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sessionDevId')
        if sDevId == None or len(sDevId) <= 0:
            #             TyContext.ftlog.error('ERROR, TuyouPayCheck->updateMsgPayByDev the user sessionDevId is empty ! userId=', userId)
            return 0, 0

        yyyymmdd, yyyymm, dcount, mcount = TyContext.RedisPayData.execute('HMGET', 'pay:' + sDevId, 'yyyymmdd',
                                                                          'yyyymm', 'dcount', 'mcount')
        if coin <= 0:
            if dcount == None or mcount == None:
                return 0, 0

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
        #         TyContext.ftlog.debug('TuyouPayCheck->updateMsgPayByDev datas=', yyyymmdd, yyyymm, dcount, mcount, 'userId=', userId, 'coin=', coin)

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

        if coin > 0:
            change = True
        mcount += coin
        dcount += coin

        if change:
            TyContext.RedisPayData.execute('HMSET', 'pay:' + sDevId, 'yyyymmdd', yyyymmdd, 'yyyymm', yyyymm, 'dcount',
                                           dcount, 'mcount', mcount)
            TyContext.RedisPayData.execute('EXPIRE', 'pay:' + sDevId, 86400 * 32)
        #         TyContext.ftlog.debug('TuyouPayCheck->updateMsgPayByDev done datas=', yyyymmdd, yyyymm, dcount, mcount, 'userId=', userId, 'coin=', coin, 'change=', change)
        return dcount, mcount

    @classmethod
    def updateMsgPayLimit(cls, coin, payType, userId):
        TyContext.ftlog.debug('TuyouPayCheck->updateMsgPayLimit payType=', payType, 'coin=', coin, 'userId=', userId)
        msgpayttpes = ['linkyun', 'linkyununion', 'ydmm', 'huafubao', 'liantong.wo', 'newYinHe', '360.ydmm',
                       '360.liantong.wo']
        msgpayttpes = TyContext.Configure.get_global_item_json('paytype.msg.limited.list', msgpayttpes)
        if coin > 0 and payType in msgpayttpes:
            cls.updateMsgPayByDev(coin, userId)

    @classmethod
    def appendMsgPayLimitInfo(cls, userId, datas):
        datas['msgpaylimit'] = 0
        dcount, mcount = cls.updateMsgPayByDev(0, userId)
        TyContext.ftlog.debug('appendMsgPayLimitInfo->msg->dcount, mcount=', dcount, mcount, 'userId=', userId)
        if dcount >= 50 or mcount > 290:
            datas['msgpaylimit'] = 1

    @classmethod
    def getMsgPayLimit(cls, userId):
        dcount, mcount = cls.updateMsgPayByDev(0, userId)
        if dcount >= 50 or mcount > 290:
            return 1
        return 0
