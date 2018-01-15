# -*- coding=utf-8 -*-

import json
import time

import datetime


class Day1st(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def __checkDay1stInstall(self, tasklet, gameId, userId):
        day1stkey = 'day1st:' + str(gameId) + ':' + str(userId)
        # 初始化成一个空字典，各个游戏可以用这个字典纪录每日任务中的局数变量
        ret = self.__ctx__.RedisUser.execute(userId, 'exists', day1stkey)
        if not ret:
            # set expire at next 00:00...
            nt = time.localtime()
            ntsec = 86400 - nt[3] * 3600 + nt[4] * 60 + nt[5]
            nowstr = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.__ctx__.RedisUser.execute(userId, 'HSET', day1stkey, 'now', nowstr)
            self.__ctx__.RedisUser.execute(userId, 'EXPIRE', day1stkey, ntsec)
        return day1stkey

    def getDay1stDatas(self, tasklet, userId, gameId):
        day1stkey = self.__checkDay1stInstall(tasklet, gameId, userId)
        datajson = self.__ctx__.RedisUser.execute(userId, 'HGET', day1stkey, 'data')
        if datajson:
            data = json.loads(datajson)
        else:
            data = {}
        return data

    def setDay1stDatas(self, tasklet, userId, gameId, datas):
        day1stkey = self.__checkDay1stInstall(tasklet, gameId, userId)
        datastr = json.dumps(datas)
        self.__ctx__.RedisUser.execute(userId, 'HSET', day1stkey, 'data', datastr)

    def set_datas(self, userId, gameId, datas):
        tasklet = self.__ctx__.getTasklet()
        return self.setDay1stDatas(tasklet, userId, gameId, datas)

    def get_datas(self, userId, gameId):
        tasklet = self.__ctx__.getTasklet()
        return self.getDay1stDatas(tasklet, userId, gameId)


Day1st = Day1st()
