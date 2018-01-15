# -*- coding=utf-8 -*-
'''
Created on 2014年12月12日

@author: zhaojiangang
'''


class ChipNotEnoughOpMode(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.NOOP = 0
        self.CLEAR_ZERO = 1


ChipNotEnoughOpMode = ChipNotEnoughOpMode()
