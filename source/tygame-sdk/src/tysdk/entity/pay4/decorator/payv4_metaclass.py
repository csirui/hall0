#! encoding=utf-8
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback_map
from tysdk.entity.pay4.decorator.payv4_filter import payv4_filter_map
from tysdk.entity.pay4.decorator.payv4_order import payv4_order_map

__author__ = 'yuejianqiang'

import types
import functools


class payv4_metaclass(type):
    def __new__(cls, name, bases, dct):
        newcls = type.__new__(cls, name, bases, dct)
        instance = newcls()
        for k, v in dct.items():
            if isinstance(v, types.FunctionType):
                try:
                    for filter_type in v.__filter_type__:
                        payv4_filter_map[filter_type] = functools.partial(v, instance)
                except AttributeError:
                    pass
                try:
                    for charge_type in v.__charge_type__:
                        payv4_order_map[charge_type] = functools.partial(v, instance)
                except AttributeError:
                    pass
                try:
                    for path in v.__callback_path__:
                        payv4_callback_map[path] = functools.partial(v, instance)
                except AttributeError:
                    pass
        return newcls
