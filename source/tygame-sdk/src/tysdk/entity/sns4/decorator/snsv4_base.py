from tysdk.entity.sns4.decorator.snsv4_login import snsv4_login_map

__author__ = 'tuyou'
import types
from functools import partial


class MetaClass(type):
    def __new__(cls, name, bases, dct):
        newcls = type.__new__(cls, name, bases, dct)
        instance = newcls()
        for v in dct.values():
            if isinstance(v, types.FunctionType):
                try:
                    for sdk in v.__sdks__:
                        snsv4_login_map[sdk] = partial(v, instance)
                except:
                    pass
        return newcls


class SnsV4Base:
    __metaclass__ = MetaClass
