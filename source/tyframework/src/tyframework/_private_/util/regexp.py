# -*- coding=utf-8 -*-

import re


class RegExp(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.__buffered_reg__ = {}

    def match(self, regExp, checkStr):
        if regExp == '*':
            return True
        if regExp in self.__buffered_reg__:
            breg = self.__buffered_reg__[regExp]
        else:
            breg = re.compile(regExp)
            self.__buffered_reg__[regExp] = breg
        if breg.match(checkStr):
            return True
        return False

    def matchlist(self, regExpList, checkStr):
        for regExp in regExpList:
            if self.match(regExp, checkStr):
                return True
        return False


RegExp = RegExp()
