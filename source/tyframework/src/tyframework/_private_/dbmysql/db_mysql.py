# -*- coding=utf-8 -*-

from twisted.enterprise import adbapi


class DbMySql():
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.__CONNMYSQL__ = {}
        self.__KEEPCOUNT__ = 1
        self.__keep_alive__ = 0

    def keep_alive(self, hc):
        if hc <= 0 or hc % 10 != 0 or self.__keep_alive__ == 1:
            return
        self.__keep_alive__ = 1
        sqlstr = 'select %d' % (self.__KEEPCOUNT__)
        self.__KEEPCOUNT__ = self.__KEEPCOUNT__ + 1
        for dbkey in self.__CONNMYSQL__.keys():
            conn = self.__CONNMYSQL__[dbkey]
            try:
                self.__ctx__.TyDeffer.add_default_callback(conn.runQuery(sqlstr), __file__, 'keep_alive')
            except:
                self.__ctx__.ftlog.error('ERROR MYSQL of', dbkey, 'has connection error ! close !! ')
                try:
                    conn.close()
                except:
                    pass
                try:
                    del self.__CONNMYSQL__[dbkey]
                except:
                    pass
                del conn
        self.__keep_alive__ = 0

    def connect(self, alias_name, *args):
        if alias_name in self.__CONNMYSQL__:
            return self.__CONNMYSQL__[alias_name]

        if len(args) == 1:
            confDict = args[0]

            # noinspection PyPep8Naming
            def PATCH():
                """
                # rname = str(confDict['dbname'])
                默认地址将走intrant而这个地址是指向redis的
                之前的架构全部是本服启动redis与mysql都是127.0.0.1
                所以ok的
                分服部署的时候会有致命问题的
                为了不去摘取所有的相关配置所以在此处加补丁
                """
                return "db.dayun-app.com"

            rname = str(confDict['dbname'])
            ruser = str(confDict['user'])
            rpwd = str(confDict['pwd'])
            rhost = PATCH()
            rport = int(confDict['port'])
        elif len(args) == 5:
            rname = str(args[0])
            rhost = str(args[1])
            rport = int(args[2])
            ruser = str(args[3])
            rpwd = str(args[4])
        else:
            raise Exception(
                'args error, connect(dbname, user, pwd, ip, port) or connect({"dbname":dbname,"user":user,"pwd":pwd, "host":ip, "port":port})',
                args)

        self.__ctx__.ftlog.debug('DbMySql.connect->', alias_name, rname, ruser, rpwd, rhost, rport)
        rconn = adbapi.ConnectionPool('pymysql', db=rname, user=ruser, passwd=rpwd, \
                                      host=rhost, port=rport, charset='utf8', use_unicode=True, cp_reconnect=True)
        self.__ctx__.ftlog.debug('DbMySql.__init__->done', rconn)

        self.__CONNMYSQL__[alias_name] = rconn
        return rconn

    def query(self, alias_name, sqlstr, sql_arg_list=[]):
        mpool = self.__CONNMYSQL__[alias_name]
        self.__ctx__.ftlog.debug('alias_name=', alias_name, 'conn=', mpool, 'sqlstr=', sqlstr, 'sql_arg_list=',
                                 sql_arg_list)
        tasklet = self.__ctx__.getTasklet()
        tasklet._report_wait_prep_(sqlstr)
        d = mpool.runQuery(sqlstr, sql_arg_list)
        self.__ctx__.ftlog.debug('alias_name=', alias_name, 'conn=', mpool, 'd=', d)
        result = tasklet._wait_for_deferred_(d, sqlstr)
        self.__ctx__.ftlog.debug('alias_name=', alias_name, 'conn=', mpool, 'd=', d, 'result=', result)
        return result

    def query_conn(self, mysqlconn, sqlstr, sql_arg_list=[]):
        tasklet = self.__ctx__.getTasklet()
        tasklet._report_wait_prep_(sqlstr)
        d = mysqlconn.runQuery(sqlstr, sql_arg_list)
        result = tasklet._wait_for_deferred_(d, sqlstr)
        return result


DbMySql = DbMySql()
