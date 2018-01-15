# -*- coding=utf-8 -*-
import functools
import inspect
from time import time


class GlobaclLocker(object):
    LUA_LOCK_SCRIPT = '''
if redis.call("get",KEYS[1]) == KEYS[2] then
    return redis.call("del",KEYS[1])
else
    return 0
end
'''

    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _init_singleton_(self):
        self.__ctx__.RedisLocker.load_lua_script('global_locker', self.LUA_LOCK_SCRIPT)

    def __init__(self):
        pass

    def __get_lock_controls__(self):
        tasklet = self.__ctx__.getTasklet()
        controls = getattr(tasklet, '_ty_global_locker_control_dict_', None)
        if controls == None:
            controls = {}
            setattr(tasklet, '_ty_global_locker_control_dict_', controls)
        return controls

    def lock(self, locker_name):
        controls = self.__get_lock_controls__()
        if locker_name in controls:
            raise self.__ctx__.GlobalLockerException(1,
                                                     'the global locker already locked by current tasklet !!' + locker_name)

        tasklet = self.__ctx__.getTasklet()
        isok = 0
        ct = time()
        random_value = self.__ctx__.strutil.uuid()
        self.__ctx__.ftlog.debug('GlobaclLocker.lock', locker_name, random_value)
        while not isok:
            isok = self.__ctx__.RedisLocker.execute('SET', 'global_locker:' + locker_name, random_value, 'NX', 'PX',
                                                    '1000')  # 1秒钟后,自动解锁
            if isok:
                controls[locker_name] = random_value
                self.__ctx__.ftlog.debug('GlobaclLocker.lock', locker_name, random_value, 'lock ok !!')
                return random_value
            else:
                if time() - ct > 1.0:  # 10秒钟还不能锁定, 那么错误返回
                    raise self.__ctx__.GlobalLockerException(1,
                                                             'time out !! can not lock the global resource of : ' + locker_name)
                tasklet._sleep_(0.01)

    def unlock(self, locker_name):
        self.__ctx__.ftlog.debug('GlobaclLocker.unlock', locker_name)
        controls = self.__get_lock_controls__()
        if not locker_name in controls:
            raise self.__ctx__.GlobalLockerException(1, 'the global locker not locked !!' + locker_name)

        random_value = controls[locker_name]
        self.__ctx__.ftlog.debug('GlobaclLocker.unlock', locker_name, random_value)
        isok = self.__ctx__.RedisLocker.exec_lua_alias('global_locker', 2, 'global_locker:' + locker_name, random_value)
        self.__ctx__.ftlog.debug('GlobaclLocker.unlock', locker_name, random_value, isok)
        if locker_name in controls:
            del controls[locker_name]
        if not isok:
            self.__ctx__.ftlog.error('the global locker, unlock error !', locker_name)
            return 0
        else:
            self.__ctx__.ftlog.debug('the global locker, unlock ok !', locker_name)
            return 1


GlobaclLocker = GlobaclLocker()


def global_lock_method(lock_name_head, lock_name_tails=[]):
    assert (isinstance(lock_name_head, (str, unicode)))
    assert (isinstance(lock_name_tails, (list, tuple)))

    def decorating_function(method):

        _lock_name_head = lock_name_head
        _lock_param_indexs = []
        paramkeys, _, __, ___ = inspect.getargspec(method)
        for lname in lock_name_tails:
            i = -1
            for x in xrange(len(paramkeys)):
                if lname == paramkeys[x]:
                    i = x
                    break
            if i >= 0:
                _lock_param_indexs.append(i)
            else:
                raise Exception('can not find the param name of :' + lname)

        @functools.wraps(method)
        def funwarp(*args, **argd):
            from tyframework.context import TyContext
            lockuuid = None
            locker_name = _lock_name_head
            try:
                for i in _lock_param_indexs:
                    locker_name = locker_name + ':' + str(args[i])
                lockuuid = TyContext.GlobaclLocker.lock(locker_name)
                return method(*args, **argd)
            finally:
                try:
                    if lockuuid != None:
                        TyContext.GlobaclLocker.unlock(locker_name)
                except:
                    TyContext.ftlog.error('ERROR, GlobaclLocker.unlock ! locker_name=', locker_name)
                    pass

        return funwarp

    return decorating_function
