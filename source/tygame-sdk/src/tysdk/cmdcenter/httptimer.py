# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class HttpSdkTimer(object):
    def get_interval(self):
        return 1

    def execute(self, second):
        TyContext.ftlog.debug('HttpSdkTimer execute', second)
        pass
