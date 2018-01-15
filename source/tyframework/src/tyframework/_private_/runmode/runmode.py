# -*- coding=utf-8 -*-

# from tyframework._private_.dbredis.db_redis import DbRedis


'''
接入服务器的运行模式检查器
'''


class RunMode(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.__MODE_KEY__ = '_ty_test_server_'

    def check_game_server_mode(self):
        '''
        检查当前接入的http或udp的服务器的运行模式
        '''

    #         tasklet = self.__ctx__.getTasklet()
    #         jstr = ''
    #         try:
    #             args = getattr(tasklet, 'args', None)
    #             if isinstance(args, dict) and self.__MODE_KEY__ in args :
    #                 jstr = args[self.__MODE_KEY__][0]
    #             else:
    #                 return
    #
    #             del args[self.__MODE_KEY__]
    #             request = getattr(tasklet, 'request', None)
    #             if request != None and self.__MODE_KEY__ in request.args:
    #                 del request.args[self.__MODE_KEY__]
    #
    #             test_server = self.__ctx__.strutil.loadsbase64(jstr)
    #             test_server['__conns__'] = {}
    #             appId = test_server['appId']
    #             httpgame = test_server.get('http.game', '')
    #
    #             if httpgame == '' :
    #                 serverip = test_server['internet']
    #                 httpport = test_server['http.port']
    #                 if httpport > 80 :
    #                     httpgame = 'http://' + serverip + ':' + str(httpport)
    #                 else:
    #                     httpgame = 'http://' + serverip
    #
    #                 minp = test_server['tcp.port.min']
    #                 maxp = test_server['tcp.port.max']
    #                 ports = []
    #                 while minp <= maxp :
    #                     ports.append(minp)
    #                     minp = minp + 1
    #                 test_server['_tcp.ports_'] = ports
    #
    #             hcount = 0
    #             controlall = self.__ctx__.ServerControl.get_control_all(appId)
    #             if controlall :
    #                 for x in xrange(len(controlall) - 1, -1, -1):
    #                     control = controlall[x]
    #                     if httpgame == control['http'] :
    #                         test_server['_server.control_'] = control
    #                         hcount += 1
    #             if hcount <= 0 :
    #                 raise Exception('the test server of ' + str(appId) + ' ' + httpgame + ' not report online !')
    #             if hcount > 1 :
    #                 raise Exception('the test server of ' + str(appId) + ' ' + httpgame + ' double report online !')
    #             setattr(tasklet, self.__MODE_KEY__, test_server)
    #             self.__ctx__.ftlog.debug('RunMode.check_game_server_mode test_server=', test_server)
    #         except:
    #             self.__ctx__.ftlog.exception('RunMode.check_game_server_mode ERROR jstr=', jstr)

    #     def __get_test_game_server__(self):
    #         tasklet = self.__ctx__.getTasklet()
    #         test_server = getattr(tasklet, self.__MODE_KEY__, None)
    #         return test_server

    def get_server_control(self):
        #         '''
        #         取得接入的服务器的服务控制定义
        #         '''
        #         server = self.__get_test_game_server__()
        #         if server :
        #             return server['_server.control_']
        return None

    #     def get_user_tcp_address(self, userId):
    #         '''
    #         取得当前接入的服务器的TCP链接地址
    #         '''
    #         server = self.__get_test_game_server__()
    #         if server :
    #             try:
    #                 ports = server['conn.list']
    #                 port = ports[userId % len(ports)]
    #                 return port[0], port[1]
    #             except:
    #                 ports = server['_tcp.ports_']
    #                 port = ports[userId % len(ports)]
    #                 return server['internet'], port
    #         return None, None

    #     def __get_redis_conn__(self, redisKey):
    #         rdbs = None
    #         server = self.__get_test_game_server__()
    #         if server :
    #             conns = server['__conns__']
    #             keyconn = redisKey + '._conn_'
    #             if not keyconn in conns :
    #                 if redisKey in server :
    #                     dbconfs = server[redisKey]
    #                     if isinstance(dbconfs, dict) :
    #                         rdbs = DbRedis.connect(dbconfs)
    #                     else:
    #                         rdbs = []
    #                         for dbconf in dbconfs :
    #                             rdbs.append(DbRedis.connect(dbconf))
    #                     conns[keyconn] = rdbs
    #                 else:
    #                     conns[keyconn] = None
    #             else:
    #                 rdbs = conns[keyconn]
    # #         self.__ctx__.ftlog.debug('RunMode.__get_redis_conn__->', redisKey, rdbs)
    #         return rdbs

    def get_redis_conn(self, dbname):
        return None

    #         '''
    #         取得当前接入服务器的REDIS定义
    #         '''
    #         return self.__get_redis_conn__(dbname)

    def set_server_link(self, key):
        pass

    #         '''
    #         绑定一个关键值和当前的接入服务，后期当发现这个关键值时，可以使用get_server_link找到原始的接入服务
    #         '''
    #         try:
    #             server = self.__get_test_game_server__()
    #             if server :
    #                 datas = dict(server)
    #                 del datas['__conns__']
    #                 datas = self.__ctx__.strutil.dumps(datas)
    #                 self.__ctx__.RedisConfig.execute('HSET', 'sdk.orderid.server.links', key, datas)
    #                 self.__ctx__.ftlog.debug('RunMode.set_server_link->', key, datas)
    #                 return
    #             self.__ctx__.ftlog.debug('RunMode.set_server_link no link->', key)
    #         except:
    #             self.__ctx__.ftlog.exception()

    def get_server_link(self, key):
        pass

    #         '''
    #         找到并恢复关键值和其对应的原始的接入服务
    #         '''
    #         try:
    #             server = self.__get_test_game_server__()
    #             if server == None :
    #                 datas = self.__ctx__.RedisConfig.execute('HGET', 'sdk.orderid.server.links', key)
    #                 if datas :
    #                     server = self.__ctx__.strutil.loads(datas)
    #                     tasklet = self.__ctx__.getTasklet()
    #                     setattr(tasklet, self.__MODE_KEY__, server)
    #                     server['__conns__'] = {}
    #                     self.__ctx__.ftlog.debug('RunMode.get_server_link load->', key, server)
    #                     return
    #                 self.__ctx__.ftlog.debug('RunMode.get_server_link not found->', key)
    #             else:
    #                 self.__ctx__.ftlog.debug('RunMode.get_server_link old->', key, server)
    #         except:
    #             self.__ctx__.ftlog.exception()

    def del_server_link(self, key):
        pass


# '''
#         删除关键值和其对应的原始的接入服务定义
#         '''
#         try:
#             self.__ctx__.RedisConfig.execute('HDEL', 'sdk.orderid.server.links', key)
#             self.__ctx__.ftlog.debug('RunMode.del_server_link->', key)
#         except:
#             self.__ctx__.ftlog.exception()

RunMode = RunMode()
