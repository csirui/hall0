# -*- coding=utf-8 -*-

from tyframework._private_.dbredis.db_redis import DbRedis
from tyframework._private_.util.datanotify import notify_game_server_on_data_change


class RedisCluster(object):
    def __init__(self, paramList=None, dbname=None):
        if paramList == None:
            return
        if not isinstance(paramList, list):
            paramList = [paramList]
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

        if len(paramList) == 1:
            if not 'useridmod' in paramList[0]:
                paramList[0]['useridmod'] = 0
        paramList.sort(key=lambda x: x['useridmod'])
        self.__ctx__.ftlog.info('RedisCluster.__init__->', paramList)

        if paramList[0]['useridmod'] != 0:
            raise Exception('redis cluster useridmods error !! 0 is missing')
        if paramList[-1]['useridmod'] != len(paramList) - 1:
            raise Exception('redis cluster useridmods error !! mod is off and on !!')

        self.notifycahnged = 0
        self.dbname = dbname
        self.address = []
        self.__dbs__ = []
        for param in paramList:
            self.__ctx__.ftlog.info('RedisCluster.__init__->', param)
            rdb = DbRedis.connect(param)
            self.__dbs__.append(rdb)
            self.address.append(param)
        self.__cluseter_size = len(self.__dbs__)
        self.__ctx__.ftlog.info('RedisCluster.__init__->done', len(self.__dbs__))

    def get_cluster_size(self):
        return self.__cluseter_size

    def __get_db__(self):
        if self.dbname:
            rdbs = self.__ctx__.RunMode.get_redis_conn(self.dbname)
            if rdbs:
                return rdbs
        return self.__dbs__

    def get_db_conn(self, userId):
        userId = int(userId)
        if userId <= 0:
            raise Exception('userId value error !! ' + str(userId))
        rdbs = self.__get_db__()
        rdb = rdbs[userId % len(rdbs)]
        return rdb

    def execute(self, userId, *args, **kwargs):
        if self.notifycahnged:
            notify_game_server_on_data_change(userId, args)
        rdb = self.get_db_conn(userId)
        return rdb.execute(*args, **kwargs)

    def sendcmd(self, userId, *args, **kwargs):
        if self.notifycahnged:
            notify_game_server_on_data_change(userId, args)
        rdb = self.get_db_conn(userId)
        return rdb.sendcmd(*args, **kwargs)

    def load_lua_script(self, lua_alias, lua_script):
        rdbs = self.__get_db__()
        shaval = ''
        for rdb in rdbs:
            shaval = rdb.load_lua_script(lua_alias, lua_script)
        return shaval

    def exec_lua_alias(self, userId, lua_alias, *args, **kwargs):
        if self.notifycahnged:
            notify_game_server_on_data_change(userId, None)
        rdb = self.get_db_conn(userId)
        return rdb.exec_lua_alias(lua_alias, *args, **kwargs)
