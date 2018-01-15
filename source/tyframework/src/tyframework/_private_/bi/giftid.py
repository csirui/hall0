# -*- coding=utf-8 -*-
'''
Created on 2014年12月12日

@author: zhaojiangang
'''

'''
TODO 将这些定义移动到配置文件中, 使用 __get_attr__进行替换封装
'''


class GiftId(object):
    def __setattr__(self, *args, **kwargs):
        if len(args) == 2 and len(kwargs) == 0:
            name = args[0]
            val = args[1]
            if isinstance(val, int):
                if not hasattr(self, '__all_eventids'):
                    self.__all_eventids = set()
                    self.__all_eventnames = set()
                if name in self.__all_eventnames:
                    raise Exception('the gift name already exits ! ' + name)
                self.__all_eventnames.add(name)

                if val in self.__all_eventids:
                    raise Exception('the gift id already exits ! ' + name + '=' + str(val))
                self.__all_eventids.add(name)

                return object.__setattr__(self, name, val)
        return object.__setattr__(self, *args, **kwargs)

    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.UNKNOWN = 0
        self.FLOWER = 10001
        self.CAKE = 10002
        self.CAR = 10003
        self.PLANE = 10004
        self.VILLA = 10005


GiftId = GiftId()
