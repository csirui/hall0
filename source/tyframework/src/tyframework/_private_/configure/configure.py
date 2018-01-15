# -*- coding=utf-8 -*-
from operator import isCallable

from tyframework._private_.configure.cache_lfu import CacheLfu

DATA_TYPE_UNKNOW = -1  # 数据类型:未知,即直接返回redis的数据结构,不做处理
DATA_TYPE_STR = 0  # 数据类型: ASCII字符串
DATA_TYPE_UNICODE = 1  # 数据类型:UNICODE字符串
DATA_TYPE_JSON = 2  # 数据类型: JSON对象, list或dict
DATA_TYPE_INT = 3  # 数据类型: 整形数字
DATA_TYPE_FLOAT = 4  # 数据类型 : 浮点数字
DATA_TYPE_FUNCTION = 5  # 数据类型: python函数, 代码格式请参考 get_configure_function 说明
DATA_TYPE_HASH_SET = 6  # 数据类型: JSON对象, 将数据转换为python的set对象


class Configure(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.__is_reload__ = 0
        self._cache_ = CacheLfu(self._get_redis_data_)

    def reload_cache_keys(self, keylist):
        self._cache_._clear_keys_(keylist)
        self.__is_reload__ += 1
        if self.__is_reload__ > 1:
            return

        while self.__is_reload__ > 0:
            self.__ctx__.ftlog.info('Configure->reload_cache_keys start, uuid=', self.get_configure_uuid())
            self.__ctx__.ftlog._init_singleton_()
            tasklet = self.__ctx__.getTasklet()
            tasklet.gdata.updateConfig(tasklet)
            self.__ctx__.ftlog.info('Configure->reload_cache_keys done')
            self.__is_reload__ -= 1

    '''
    再进程内设定一个配置信息, 通知其他进程进行同步更新? 这个业务逻辑不稳妥, 放弃所有的set方法
    '''

    #     def set_configure(self, redisfullkey, redisvalue, clientid=None):
    #         '''
    #         设定配置数据库中的一个键值数据
    #         设定后, 将清除对应键值redisfullkey的缓存
    #         注意: 此方法设定的键值数据只影响到当前进程的配置数据,不进行"配置变更事件的广播",
    #               其他进程将无法及时收到该键值数据已经变化的事件, 不会重新加载此键值,
    #               其他进程只有当重新启动时,才会重新加载此键值数据
    #         参数: redisfullkey 再REDIS中存取的键值
    #              redisvalue 存入REDIS的数据的值,直接使用json的序列化功能转换为字符串后,再进行存储
    #         '''
    #         if isinstance(redisvalue, (list, dict)) :
    #             redisvalue = self.__ctx__.strutil.dumps(redisvalue)
    #         if not isinstance(redisvalue, (int, float, bool, str, unicode)) :
    #             raise Exception('configureitems value type error !! must simple type in (int, float, bool, str, unicode)')
    #         if clientid != None and len(clientid) > 0 :
    #             redisfullkey = redisfullkey + ':' + clientid
    #         self.__ctx__.RedisConfig.execute('SET', redisfullkey, redisvalue)
    #         self._cache_._clear_keys_([redisfullkey])

    def _get_redis_data_(self, redisfullkey, datatype, decodeutf8):
        '''
        取得配置系统的一个键值的数据
        配置系统的数据,单独存放在配置数据库中,全部使用GET/SET命令进行数据的读取和写入
        当前使用lru缓存机制,进行缓存
        参数: redisfullkey REDIS中对应的数据的键值名称
        参数: datatype 获取的数据的类型, 参考:DATA_TYPE_XXXX
        '''
        value = self.__ctx__.RedisConfig.execute('GET', redisfullkey)
        if value == None:
            return None

        if datatype == DATA_TYPE_JSON:
            value = self.__ctx__.strutil.loads(value, decodeutf8)
        elif datatype == DATA_TYPE_INT:
            value = int(value)
        elif datatype == DATA_TYPE_FLOAT:
            value = float(value)
        elif datatype == DATA_TYPE_STR:
            if not isinstance(value, unicode):  # 所有的字符串都应该是unicode
                value = unicode(value)
            #             if not isinstance(value, str) :
            #                 value = unicode(value).encode('utf-8')
        elif datatype == DATA_TYPE_UNICODE:
            if not isinstance(value, unicode):
                value = unicode(value)
        elif datatype == DATA_TYPE_HASH_SET:
            value = self.__ctx__.strutil.loads(value, decodeutf8)
            value = set(value)
        elif datatype == DATA_TYPE_FUNCTION:
            myglobals = {}
            mylocals = {}
            co = compile(value, 'load_dynamic_func', 'exec')
            exec co in myglobals, mylocals
            value = mylocals[mylocals.keys()[0]]
            value.__myglobals__ = myglobals
            value.__mylocals__ = mylocals
        return value

    def _get_configure_(self, redisfullkey, defaultvalue=None, datatype=DATA_TYPE_STR, clientid=None, decodeutf8=False):
        isclientid = 0
        if clientid == None or len(clientid) <= 0:
            rkey = redisfullkey
        else:
            isclientid = 1
            rkey = redisfullkey + ':' + clientid
        value = self._cache_._get_cache_data_(rkey, datatype, decodeutf8)
        if value == None and isclientid == 1:
            rkey = redisfullkey + ':default'
            value = self._cache_._get_cache_data_(rkey, datatype, decodeutf8)
        if value == None:
            value = defaultvalue

        if value != None:
            if datatype == DATA_TYPE_JSON:
                assert (isinstance(value, (list, dict)))
            elif datatype == DATA_TYPE_INT:
                assert (isinstance(value, int))
            elif datatype == DATA_TYPE_FLOAT:
                assert (isinstance(value, float))
            elif datatype == DATA_TYPE_STR:
                assert (isinstance(value, (unicode, str)))
            elif datatype == DATA_TYPE_UNICODE:
                assert (isinstance(value, (unicode, str)))
            elif datatype == DATA_TYPE_HASH_SET:
                assert (isinstance(value, set))
            elif datatype == DATA_TYPE_FUNCTION:
                assert (isCallable(value))
            else:
                assert (isinstance(value, (str, unicode, int, float)))
            #         self.__ctx__.ftlog.debug('_get_configure_->', rkey, '=', value)
        return value

    def get_configure_uuid(self):
        '''
        取得配置内容的更新的标记, 即配置内容每发生一次变化(由配置脚本或配置界面更新), 此标记变化一次
        其值为一个UUID字符串
        '''
        return self._get_configure_('configitems:__uuid__', 'none', DATA_TYPE_STR, None)

    def get_configure_int(self, redisfullkey, defaultVal=None, clientid=None):
        '''
        取得配置系统的一个键值的int值
        '''
        return self._get_configure_(redisfullkey, defaultVal, DATA_TYPE_INT, clientid)

    def get_configure_float(self, redisfullkey, defaultVal=None, clientid=None):
        '''
        取得配置系统的一个键值的float值
        '''
        return self._get_configure_(redisfullkey, defaultVal, DATA_TYPE_FLOAT, clientid)

    def get_configure_str(self, redisfullkey, defaultVal=None, clientid=None):
        '''
        取得配置系统的一个键值的str值
        '''
        return self._get_configure_(redisfullkey, defaultVal, DATA_TYPE_STR, clientid)

    def get_configure_unicode(self, redisfullkey, defaultVal=None, clientid=None):
        '''
        取得配置系统的一个键值的unicode值
        '''
        return self._get_configure_(redisfullkey, defaultVal, DATA_TYPE_UNICODE, clientid)

    def get_configure_json(self, redisfullkey, defaultVal=None, clientid=None, decodeutf8=False):
        '''
        取得配置系统的一个键值的json对象值(list或dict类型)
        '''
        return self._get_configure_(redisfullkey, defaultVal, DATA_TYPE_JSON, clientid, decodeutf8)

    def get_configure_hashset(self, redisfullkey, defaultVal=None, clientid=None, decodeutf8=False):
        '''
        取得配置系统的一个键值的json对象值(set类型)
        '''
        return self._get_configure_(redisfullkey, defaultVal, DATA_TYPE_HASH_SET, clientid, decodeutf8)

    def get_configure_function(self, redisfullkey, defaultVal=None, clientid=None):
        '''
        取得配置系统的一个键值的可调用函数,即改对应键值再REDIS中,为一个函数定义
        函数定义说明:
            1. 仅仅支持对外一个函数的定义
            2. 函数的参数不要求完全一致,需要使用者和定义者进行协商
            3. 定义的函数的字符串, 第一行必定为 def xxxx(...), 
               且在同一代码级别上不能再有其他的函数变量,import等定义
        示例:
def test_func1(arg1, arg2) :
    from tyframework.context import TyContext
    TyContext.ftlog.debug('测试')
    return 1
        '''
        return self._get_configure_(redisfullkey, defaultVal, DATA_TYPE_FUNCTION, clientid)

        ###############################################################################################
        # configitems:global: 全局定义系列方法
        ###############################################################################################

    #     def set_global_item(self, key, value, clientid=None):
    #         return self.set_configure('configitems:global:' + key, value, clientid)

    def get_global_item_int(self, key, defaultVal=0, clientid=None):
        return self._get_configure_('configitems:global:' + key, defaultVal, DATA_TYPE_INT, clientid)

    def get_global_item_float(self, key, defaultVal=0.0, clientid=None):
        return self._get_configure_('configitems:global:' + key, defaultVal, DATA_TYPE_FLOAT, clientid)

    def get_global_item_str(self, key, defaultVal='', clientid=None):
        return self._get_configure_('configitems:global:' + key, defaultVal, DATA_TYPE_STR, clientid)

    def get_global_item_unicode(self, key, defaultVal=u'', clientid=None):
        return self._get_configure_('configitems:global:' + key, defaultVal, DATA_TYPE_UNICODE, clientid)

    def get_global_item_json(self, key, defaultVal=None, clientid=None, decodeutf8=False):
        return self._get_configure_('configitems:global:' + key, defaultVal, DATA_TYPE_JSON, clientid, decodeutf8)

    def get_global_item_hashset(self, key, defaultVal=None, clientid=None, decodeutf8=False):
        return self._get_configure_('configitems:global:' + key, defaultVal, DATA_TYPE_HASH_SET, clientid, decodeutf8)

    def get_global_item_function(self, key, defaultVal=None, clientid=None):
        return self._get_configure_('configitems:global:' + key, defaultVal, DATA_TYPE_FUNCTION, clientid)

        ###############################################################################################
        # configitems:game: 游戏级别定义系列方法
        ###############################################################################################

    #     def set_game_item(self, gid, key, value, clientid=None):
    #         return self.set_configure('configitems:game:' + str(gid) + ':' + key, value, clientid)

    def get_game_item(self, gid, key, defaultVal=None, datatype=DATA_TYPE_UNKNOW, clientid=None):
        '''
        deprecated 保留项目, 一定时机后删除
        '''
        return self._get_configure_('configitems:game:' + str(gid) + ':' + key, defaultVal, datatype, clientid)

    def get_game_item_int(self, gid, key, defaultVal=0, clientid=None):
        return self._get_configure_('configitems:game:' + str(gid) + ':' + key, defaultVal, DATA_TYPE_INT, clientid)

    def get_game_item_float(self, gid, key, defaultVal=0.0, clientid=None):
        return self._get_configure_('configitems:game:' + str(gid) + ':' + key, defaultVal, DATA_TYPE_FLOAT, clientid)

    def get_game_item_str(self, gid, key, defaultVal='', clientid=None):
        return self._get_configure_('configitems:game:' + str(gid) + ':' + key, defaultVal, DATA_TYPE_STR, clientid)

    def get_game_item_unicode(self, gid, key, defaultVal=u'', clientid=None):
        return self._get_configure_('configitems:game:' + str(gid) + ':' + key, defaultVal, DATA_TYPE_UNICODE, clientid)

    def get_game_item_json(self, gid, key, defaultVal=None, clientid=None, decodeutf8=False):
        return self._get_configure_('configitems:game:' + str(gid) + ':' + key, defaultVal, DATA_TYPE_JSON, clientid,
                                    decodeutf8)

    def get_game_item_hashset(self, gid, key, defaultVal=None, clientid=None, decodeutf8=False):
        return self._get_configure_('configitems:game:' + str(gid) + ':' + key, defaultVal, DATA_TYPE_HASH_SET,
                                    clientid, decodeutf8)

    def get_game_item_function(self, gid, key, defaultVal=None, clientid=None):
        return self._get_configure_('configitems:game:' + str(gid) + ':' + key, defaultVal, DATA_TYPE_FUNCTION,
                                    clientid)

        ###############################################################################################
        # configitems:room: 游戏级别定义系列方法
        ###############################################################################################

    #     def set_room_item(self, gid, rid, key, value, clientid=None):
    #         return self.set_configure('configitems:room:' + str(gid) + ':' + str(rid) + ':' + key, value, clientid)

    def get_room_item_int(self, gid, rid, key, defaultVal=0, clientid=None):
        return self._get_configure_('configitems:room:' + str(gid) + ':' + str(rid) + ':' + key, defaultVal,
                                    DATA_TYPE_INT, clientid)

    def get_room_item_float(self, gid, rid, key, defaultVal=0.0, clientid=None):
        return self._get_configure_('configitems:room:' + str(gid) + ':' + str(rid) + ':' + key, defaultVal,
                                    DATA_TYPE_FLOAT, clientid)

    def get_room_item_str(self, gid, rid, key, defaultVal='', clientid=None):
        return self._get_configure_('configitems:room:' + str(gid) + ':' + str(rid) + ':' + key, defaultVal,
                                    DATA_TYPE_STR, clientid)

    def get_room_item_unicode(self, gid, rid, key, defaultVal=u'', clientid=None):
        return self._get_configure_('configitems:room:' + str(gid) + ':' + str(rid) + ':' + key, defaultVal,
                                    DATA_TYPE_UNICODE, clientid)

    def get_room_item_json(self, gid, rid, key, defaultVal=None, clientid=None, decodeutf8=False):
        return self._get_configure_('configitems:room:' + str(gid) + ':' + str(rid) + ':' + key, defaultVal,
                                    DATA_TYPE_JSON, clientid, decodeutf8)

    def get_room_item_hashset(self, gid, rid, key, defaultVal=None, clientid=None, decodeutf8=False):
        return self._get_configure_('configitems:room:' + str(gid) + ':' + str(rid) + ':' + key, defaultVal,
                                    DATA_TYPE_HASH_SET, clientid, decodeutf8)

    def get_room_item_function(self, gid, rid, key, defaultVal=None, clientid=None):
        return self._get_configure_('configitems:room:' + str(gid) + ':' + str(rid) + ':' + key, defaultVal,
                                    DATA_TYPE_FUNCTION, clientid)

        ###############################################################################################
        # template: 模板级别定义系列方法
        ###############################################################################################

    #     def set_template_item(self, templateid, value, clientid=None):
    #         return self.set_configure('configitems:template:' + templateid, value, clientid)

    def get_template_item_int(self, templateid, defaultVal=0, clientid=None):
        return self._get_configure_('configitems:template:' + templateid, defaultVal, DATA_TYPE_INT, clientid)

    def get_template_item_float(self, templateid, defaultVal=0.0, clientid=None):
        return self._get_configure_('configitems:template:' + templateid, defaultVal, DATA_TYPE_FLOAT, clientid)

    def get_template_item_str(self, templateid, defaultVal='', clientid=None):
        return self._get_configure_('configitems:template:' + templateid, defaultVal, DATA_TYPE_STR, clientid)

    def get_template_item_unicode(self, templateid, defaultVal=u'', clientid=None):
        return self._get_configure_('configitems:template:' + templateid, defaultVal, DATA_TYPE_UNICODE, clientid)

    def get_template_item_json(self, templateid, defaultVal=None, clientid=None, decodeutf8=False):
        return self._get_configure_('configitems:template:' + templateid, defaultVal, DATA_TYPE_JSON, clientid,
                                    decodeutf8)

    def get_template_item_hashset(self, templateid, defaultVal=None, clientid=None, decodeutf8=False):
        return self._get_configure_('configitems:template:' + templateid, defaultVal, DATA_TYPE_HASH_SET, clientid,
                                    decodeutf8)

    def get_template_item_function(self, templateid, defaultVal=None, clientid=None):
        return self._get_configure_('configitems:template:' + templateid, defaultVal, DATA_TYPE_FUNCTION, clientid)


Configure = Configure()
