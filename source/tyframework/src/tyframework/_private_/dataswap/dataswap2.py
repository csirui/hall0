# -*- coding=utf-8 -*-

import json
import time

from datetime import datetime

from tyframework._private_.lua_scripts.dataswap_scripts import DATA_SWAP_LUA_SCRIPT, \
    CHECK_USER_DATA_LUA_SCRIPT
from tyframework.decorator.globallocker import global_lock_method


class MySqlSwap2(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _init_singleton_(self):
        self.__lua_check_data = 'mysqlswap2.checkdata'
        self.__lua_load_data = 'mysqlswap2.loaddata'
        self.__ctx__.RedisUser.load_lua_script(self.__lua_check_data, CHECK_USER_DATA_LUA_SCRIPT)
        self.__ctx__.RedisUser.load_lua_script(self.__lua_load_data, DATA_SWAP_LUA_SCRIPT)

        msize = 0
        for k in self.__ctx__.TYGlobal.all_service()['mysql'].keys():
            if k.find('tydata') == 0:
                msize += 1
        self.mysqlsize = msize
        self.__ctx__.ftlog.info('_init_singleton_ mysqlsize', self.mysqlsize)

    def __init__(self):
        pass

    def updateUserDataAuthorTime(self, userId, lastAuthorTime=None):
        '''
        不推荐使用, 需要修改现有的业务逻辑进行改进
        '''
        if lastAuthorTime:
            self.__ctx__.UserProps.set_attr(userId, 'lastAuthorTime', lastAuthorTime)
        ctfull = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.__ctx__.UserProps.set_attr(userId, 'authorTime', ctfull)
        return ctfull

    def updateUserGameDataAuthorTime(self, userId, gameId):
        '''
        不推荐使用, 需要修改现有的业务逻辑进行改进
        '''
        ctfull = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.__ctx__.UserProps.set_game_attr(userId, gameId, 'authorTime', ctfull)
        return ctfull

    def updateUserDataAliveTime(self, userId):
        '''
        更新当前用户的数据生命时间
        更新的时机为: 用户登录,注册, 用户TCP连接的心跳(每小时,更新一次即可)
        冷数据导出的时机: 7天的时间间隔以上
        '''
        userId = int(userId)
        ctfull = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.__ctx__.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'aliveTime', ctfull)
        return ctfull

    def isUserDataExists(self, userId):
        self.__ctx__.ftlog.debug('MySqlSwap isUserDataExists->userId=', userId)
        userId = int(userId)
        ctfull = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        isok = self.__ctx__.RedisUser.exec_lua_alias(userId, self.__lua_check_data, 2, userId, ctfull)
        return isok == 1

    def checkUserDate(self, userId, throwEx=True, clientId=0, appId=9999, rparams=None):
        '''
        检查当前用户的数据是否是热数据(即存储在REDIS), 
        如果不是热数据, 那么重MYSQL中读取冷数据导入至热数据中
        同时更新当前用户的数据生命时间
        导入导出的用户数据包括user和个个游戏的所有数据
        返回:
            如果用户数据的最终状态为热数据,返回1
            如果用户数据不存在,返回0
        '''
        self.__ctx__.ftlog.debug('MySqlSwap checkUserData->userId=', userId, 'clientId=', clientId, 'appId=', appId)
        userId = int(userId)
        ctfull = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        isok = self.__ctx__.RedisUser.exec_lua_alias(userId, self.__lua_check_data, 2, userId, ctfull)
        if isok == 1:
            return 1
        if isinstance(clientId, basestring):
            intClientId = self.__ctx__.BiUtils.clientIdToNumber(appId, clientId)
        else:
            intClientId = int(clientId)
        appId = int(appId)
        return self.__tryReadDataFromMySql(userId, intClientId, appId, ctfull, rparams=rparams)

    def __getInt(self, v):
        if v != None:
            try:
                return int(v)
            except:
                self.__ctx__.ftlog.exception('__getInt', v)
                pass
        return 0

    @global_lock_method(lock_name_head="global.dataswap", lock_name_tails=["userId"])
    def __tryReadDataFromMySql(self, userId, intClientId, appId, ctfull, rparams=None):
        # 再次检查，避免二次进入时，又装在一次
        ctfull = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        isok = self.__ctx__.RedisUser.exec_lua_alias(userId, self.__lua_check_data, 2, userId, ctfull)
        if isok == 1:
            return 1
        # 得到MySQL中的数据
        csize = self.mysqlsize
        dbname = 'tydata' + str(userId % csize)
        tablename = 't' + str(userId / csize % 200)
        sqlstr = 'select data from %s where userid=%d limit 1' % (tablename, userId)
        self.__ctx__.ftlog.info('__tryReadDataFromMySql', userId, intClientId, appId, dbname, sqlstr)
        mysqldef = self.__ctx__.TYGlobal.mysql(dbname)
        self.__ctx__.DbMySql.connect(dbname, mysqldef)
        tabledata = self.__ctx__.DbMySql.query(dbname, sqlstr)
        jsonstr = self.__get_table_data(tabledata, 0, 0)
        self.__ctx__.ftlog.info('__tryReadDataFromMySql before', userId, jsonstr)
        if not jsonstr:
            self.__ctx__.ftlog.info('__tryReadDataFromMySql', userId, 'the user mysql data not found !')
            return 0
        loaddatas = json.loads(jsonstr)
        try:
            if 'user:' in loaddatas:
                userdata = loaddatas['user:']
            else:
                userdata = loaddatas['user:%s']
            jsondata = dict(zip(userdata[::2], userdata[1::2]))
            authorTime = jsondata.get('authorTime')
            chip = int(jsondata.get('chip', 0))
            chargeTotal = float(jsondata.get('chargeTotal', 0))
            # changePwdCount = int(jsondata.get('changePwdCount', 0))
            # 3000w and 60day
            if authorTime:
                try:
                    diff = time.time() - time.mktime(time.strptime(authorTime, '%Y-%m-%d %H:%M:%S.%f'))
                    if diff >= 6 * 30 * 86400 and int(chip) > 30000000:  # and float(chargeTotal) < 10:
                        forbid_data = self.__ctx__.Configure.get_global_item_json("forbid_device_whitelist", {})
                        forbid_userList = forbid_data.get('userList', [])
                        if not userId in forbid_userList:
                            self.__ctx__.ftlog.info('__tryReadDataFromMySql check failed->', userId,
                                                    'writtime=', authorTime,
                                                    'chip=', chip,
                                                    'chargeTotal=', chargeTotal,
                                                    'jsonstr=', jsonstr)
                            return 0
                except:
                    self.__ctx__.ftlog.error("load authorTime exception", "authorTime=", authorTime)
            # 100w and devid
            if chip >= 1000000 and rparams:
                result = []
                deviceId = rparams.get('deviceId', '')
                iccid = rparams.get('iccid')
                idfa = rparams.get('idfa')
                uuid = rparams.get('uuid')
                mac = rparams.get('mac')
                result.append(deviceId and deviceId == jsondata.get('mdevid'))
                result.append(deviceId and deviceId == jsondata.get('sessionDevId'))
                result.append(iccid and iccid == jsondata.get('sessionIccid'))
                result.append(idfa and idfa == jsondata.get('sessionIdfa'))
                result.append(uuid and uuid == jsondata.get('uuid'))
                result.append(mac and mac == jsondata.get('mac'))
                if not reduce(lambda x, y: x or y, result):
                    self.__ctx__.ftlog.error("AccountLogin->checkLoginDevice failed userId=", userId,
                                             'rparams=', rparams,
                                             'jsondata=', jsondata)
                    return 0
        except:
            self.__ctx__.ftlog.info("__tryReadDataFromMySql check exception", jsonstr)
            return 0

        # 拆解执行数据装载，避免redis的slowlog, 避免挤压redis
        isok, chip, diamond, coin, coupon = 1, 0, 0, 0, 0
        rkeys = loaddatas.keys()
        while (len(rkeys)) > 0:
            subrkeys = rkeys[0:4]
            rkeys = rkeys[4:]
            subdata = {}
            for subkey in subrkeys:
                subdata[subkey] = loaddatas[subkey]
            jsonstr1 = json.dumps(subdata)
            isok1, chip1, diamond1, coin1, coupon1 = self.__ctx__.RedisUser.exec_lua_alias(userId,
                                                                                           self.__lua_load_data, 3,
                                                                                           userId, ctfull, jsonstr1)
            self.__ctx__.ftlog.debug('__tryReadDataFromMySql save to redis->', userId, isok, jsonstr1)
            isok = min(isok, isok1)
            chip = max(chip, chip1)
            diamond = max(diamond, diamond1)
            coin = max(coin, coin1)
            coupon = max(coupon, coupon1)

        self.__ctx__.ftlog.info('__tryReadDataFromMySql save to redis->', userId,
                                'isok=', isok, 'chip=', chip if chip else 0, 'diamond=', diamond if diamond else 0,
                                'coin=', coin if coin else 0, 'coupon=', coupon if coupon else 0)
        chip = self.__getInt(chip)
        diamond = self.__getInt(diamond)
        coin = self.__getInt(coin)
        coupon = self.__getInt(coupon)
        if isok == 1:
            self.__ctx__.BiReport.report_bi_chip_update(userId, chip, chip, chip,
                                                        self.__ctx__.BIEventId.DATA_FROM_MYSQL_2_REDIS_CHIP,
                                                        intClientId, appId, appId, 0,
                                                        self.__ctx__.BiReport.CHIP_TYPE_CHIP)
            self.__ctx__.BiReport.report_bi_chip_update(userId, coin, coin, coin,
                                                        self.__ctx__.BIEventId.DATA_FROM_MYSQL_2_REDIS_COIN,
                                                        intClientId, appId, appId, 0,
                                                        self.__ctx__.BiReport.CHIP_TYPE_COIN)
            self.__ctx__.BiReport.report_bi_chip_update(userId, diamond, diamond, diamond,
                                                        self.__ctx__.BIEventId.DATA_FROM_MYSQL_2_REDIS_DIAMOND,
                                                        intClientId, appId, appId, 0,
                                                        self.__ctx__.BiReport.CHIP_TYPE_DIAMOND)
            self.__ctx__.BiReport.report_bi_chip_update(userId, coupon, coupon, coupon,
                                                        self.__ctx__.BIEventId.DATA_FROM_MYSQL_2_REDIS_COUPON,
                                                        intClientId, appId, appId, 0,
                                                        self.__ctx__.BiReport.CHIP_TYPE_COUPON)
            return 1
        return 0

    def __get_table_data(self, datas, row, col):
        try:
            if datas and len(datas) > 0:
                dstr = datas[row][col]
                if dstr[0] == '{' and dstr[-1] == '}':
                    return dstr
            self.__ctx__.ftlog.error('ERROR, the mysql data error !!', datas)
        except:
            self.__ctx__.ftlog.error('ERROR, the mysql data not found !!', datas)
        return None


MySqlSwap2 = MySqlSwap2()
