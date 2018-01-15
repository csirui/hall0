# -*- coding=utf-8 -*-
from tyframework._private_.dbredis.db_redis import DbRedis


class RedisSingle(object):
    def __init__(self, params=None, dbname=None):
        if params == None:
            return
        from tyframework.context import TyContext
        self.__ctx__ = TyContext
        self.address = params
        self.dbname = dbname
        self.__ctx__.ftlog.info('RedisSingle.__init__->', params)
        self.__db__ = DbRedis.connect(params)
        self.__ctx__.ftlog.info('RedisSingle.__init__->done')

    def __get_db__(self):
        if self.dbname:
            rdb = self.__ctx__.RunMode.get_redis_conn(self.dbname)
            if rdb:
                return rdb
        return self.__db__

    def execute(self, *args, **kwargs):
        rdb = self.__get_db__()
        return rdb.execute(*args, **kwargs)

    def sendcmd(self, *args, **kwargs):
        rdb = self.__get_db__()
        return rdb.sendcmd(*args, **kwargs)

    def load_lua_script(self, lua_alias, lua_script):
        rdb = self.__get_db__()
        return rdb.load_lua_script(lua_alias, lua_script)

    def exec_lua_alias(self, lua_alias, *args, **kwargs):
        rdb = self.__get_db__()
        return rdb.exec_lua_alias(lua_alias, *args, **kwargs)
