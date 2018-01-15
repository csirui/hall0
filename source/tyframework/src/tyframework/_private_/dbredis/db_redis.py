# -*- coding=utf-8 -*-

# from tyframework._private_.dbredis import txredisapi
from twisted.internet import reactor

from tyframework.private.servers.protocol.tytasklet.helper import TaskletHelper


class DbRedis(object):
    __CONNREDIS__ = {}
    __LUAALIAS__ = {}

    @classmethod
    def connect(cls, *args):
        from tyframework.context import TyContext
        if len(args) == 1:
            redisConfDict = args[0]
            rhost = redisConfDict['host']
            rport = int(redisConfDict['port'])
            rdbid = int(redisConfDict['dbid'])
        elif len(args) == 3:
            rhost = args[0]
            rport = int(args[1])
            rdbid = int(args[2])
        else:
            raise Exception('args error, connect(ip, port, dbid) or connect({"host":ip, "port":port, "dbid":dbid})')

        TyContext.ftlog.debug('DbRedis.connect->', rhost, rport, rdbid)
        connkey = '%s:%d:%d' % (rhost, rport, rdbid)
        if connkey in DbRedis.__CONNREDIS__:
            return DbRedis.__CONNREDIS__[connkey]
        else:
            rconn = DbRedis(rhost, rport, rdbid)
            DbRedis.__CONNREDIS__[connkey] = rconn
            return rconn

    def __init__(self, rhost, rport, rdbid):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

        self.__ctx__.ftlog.debug('DbRedis.__init__->', rhost, rport, rdbid)
        tasklet = TaskletHelper.getTasklet()
        tips = 'redis-connect' + repr([rhost, rport, rdbid])
        tasklet._report_wait_prep_(tips)

        #         redisPool = txredisapi.ConnectionPool(host=rhost, port=rport, dbid=rdbid, poolsize=TyContext.TYGlobal.redis_pool_size())
        #         self.__redisPool__ = tasklet._wait_for_deferred_(redisPool, tips)

        from tyframework._private_.dbredis.txredis.client import RedisClientFactory
        factory = RedisClientFactory(db=rdbid)
        reactor.connectTCP(rhost, rport, factory)
        tasklet._wait_for_deferred_(factory.deferred, tips)
        self.__redisPool__ = factory

        self.__ctx__.ftlog.debug('DbRedis.__init__->done', self.__redisPool__)
        self.__shamap__ = {}

    def execute(self, *args, **kwargs):
        tasklet = TaskletHelper.getTasklet()
        try:
            tips = 'redis.execute-' + repr(args[0:3])
        except:
            tips = 'redis.execute-errtips'
        tasklet._report_wait_prep_(tips)
        d = self.__redisPool__.execute_command(*args, taskid=tasklet.me._task_id, **kwargs)
        result = tasklet._wait_for_deferred_(d, tips)
        return result

    def sendcmd(self, *args, **kwargs):
        tasklet = TaskletHelper.getTasklet()
        d = self.__redisPool__.execute_command(*args, taskid=tasklet.me._task_id, **kwargs)
        self.__ctx__.TyDeffer.add_default_callback(d, __file__, 'sendcmd', args)
        return d

    def load_lua_script(self, lua_alias, lua_script):
        tasklet = TaskletHelper.getTasklet()
        tips = 'load_lua_script-' + lua_alias
        tasklet._report_wait_prep_(tips)
        d = self.__redisPool__.execute_command('script', 'load', lua_script, taskid=tasklet.me._task_id)
        shaval = tasklet._wait_for_deferred_(d, tips)
        self.__shamap__[lua_alias] = shaval
        DbRedis.__LUAALIAS__[lua_alias] = lua_script
        self.__ctx__.ftlog.info('load_lua_script->', shaval, lua_alias)
        return shaval

    def exec_lua_alias(self, lua_alias, *args, **kwargs):
        tasklet = TaskletHelper.getTasklet()
        tips = 'exec_lua_alias-' + lua_alias
        tasklet._report_wait_prep_(tips)
        if not lua_alias in self.__shamap__:
            lua_script = DbRedis.__LUAALIAS__[lua_alias]
            self.load_lua_script(lua_alias, lua_script)
        shaval = self.__shamap__[lua_alias]
        d = self.__redisPool__.execute_command('evalsha', shaval, *args, taskid=tasklet.me._task_id, **kwargs)
        result = tasklet._wait_for_deferred_(d, tips)
        return result
