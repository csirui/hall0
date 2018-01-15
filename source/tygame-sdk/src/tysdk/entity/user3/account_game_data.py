#! encoding=utf-8
from tyframework.context import TyContext
from tysdk.entity.report4.report_model import ReportModel

__author__ = 'yuejianqiang'

import datetime
import json
import time


class AccountGameData:
    VIP_EXP_LEVEL = [
        0,  # 0级
        60,  # 1
        350,  # 2
        2000,  # 3
        5000,  # 4
        20000,  # 5
        100000,  # 6
        500000,  # 7
        2000000,  # 8
        5000000,  # 9
        10000000,  # 10
        20000000,  # 11
        50000000,  # 12
        100000000,  # 13
    ]

    @classmethod
    def get_user_vip(cls, appId, userId):
        """
        获取用户vip等级
        :param userId:
        :return:
        """
        vip = 0
        if appId and int(appId) == 9999:
            gameDataKey = 'gamedata:9999:%s' % userId
            vip_exp = TyContext.RedisUser.execute(userId, 'HGET', gameDataKey, 'vip.exp')
            if vip_exp:
                for i, exp in enumerate(cls.VIP_EXP_LEVEL):
                    if int(vip_exp) < exp:
                        break
                    vip = i
        return vip

    @classmethod
    def get_user_total_time(self, appId, userId):
        """
        获取用户累计在线时长
        :param userId:
        :return:
        """
        if appId and int(appId) == 9999:
            gameDataKey = 'gamedata:9999:%s' % userId
            totaltime = TyContext.RedisGame.execute(userId, 'HGET', gameDataKey, 'totaltime')
            if totaltime:
                return max(2, int(totaltime))
        else:
            data = ReportModel().queryOnline(appId, userId)
            if data:
                return max(2, data.get('total', 0))
        return 2

    @classmethod
    def get_user_today_time(self, appId, userId):
        """
        获取用户当日在线时长
        :param userId:
        :return:
        """
        if appId and int(appId) == 9999:
            gameDataKey = 'gamedata:9999:%s' % userId
            todaytime = TyContext.RedisGame.execute(userId, 'HGET', gameDataKey, 'todaytime')
            if todaytime:
                obj = json.loads(todaytime)
                today_time = obj.get(datetime.datetime.now().strftime('%y%m%d'), 0)
                if today_time:
                    return int(today_time)
        else:
            data = ReportModel().queryOnline(appId, userId)
            if data:
                return data.get('daily', 0)
        return 0

    @classmethod
    def get_user_day3_time(self, appId, userId):
        """
        获取用户三日累计在线时长
        :param userId:
        :return:
        """
        if appId and int(appId) == 9999:
            gameDataKey = 'gamedata:9999:%s' % userId
            todaytime = TyContext.RedisGame.execute(userId, 'HGET', gameDataKey, 'todaytime')
            if todaytime:
                obj = json.loads(todaytime)
                time_list = [time.time(), time.time() - 86400, time.time() - 2 * 86400]
                time_list = [datetime.datetime.fromtimestamp(t).strftime('%y%m%d') for t in time_list]
                time_list = [obj.get(t, 0) for t in time_list]
                return sum(time_list)
        return 0

    @classmethod
    def get_user_day7_time(self, appId, userId):
        """
        获取用户7日累计在线时长
        :param userId:
        :return:
        """
        if appId and int(appId) == 9999:
            gameDataKey = 'gamedata:9999:%s' % userId
            todaytime = TyContext.RedisGame.execute(userId, 'HGET', gameDataKey, 'todaytime')
            if todaytime:
                obj = json.loads(todaytime)
                time_list = [time.time(),
                             time.time() - 86400,
                             time.time() - 2 * 86400,
                             time.time() - 3 * 86400,
                             time.time() - 4 * 86400,
                             time.time() - 5 * 86400,
                             time.time() - 6 * 86400]
                time_list = [datetime.datetime.fromtimestamp(t).strftime('%y%m%d') for t in time_list]
                time_list = [obj.get(t, 0) for t in time_list]
                return sum(time_list)
        else:
            data = ReportModel().queryOnline(appId, userId)
            if data:
                return data.get('weekly', 0)
        return 0
