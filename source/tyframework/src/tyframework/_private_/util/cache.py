# -*- coding=utf-8 -*-

from datetime import datetime


###########################################################################
# 用于系统的数据缓存
###########################################################################
class Cache:
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.__CACHE__ = {}

    def getCache(self, key, live=0):
        cache = self.__CACHE__
        if key in cache:
            item = cache[key]
            if live > 0:
                ctime = item['ctime']
                s = (datetime.now() - ctime).total_seconds()
                if s > live:
                    del cache[key]
                    return None
            return item['data']
        return None

    def setCache(self, key, value):
        ctime = datetime.now()
        self.__CACHE__[key] = {'ctime': ctime, 'data': value}

    def rmCache(self, key):
        if key in self.__CACHE__:
            del self.__CACHE__[key]


Cache = Cache()
