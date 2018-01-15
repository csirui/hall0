# -*- coding=utf-8 -*-

import os


###########################################################################
# 系统环境变量的取得
###########################################################################
class OsEnv(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.__OSENV__ = None

    def _getEnvs(self):
        if OsEnv.__OSENV__ == None:
            OsEnv.__OSENV__ = {}
            e = os.environ
            for k in e:
                OsEnv.__OSENV__[k] = e[k]
        return OsEnv.__OSENV__

    def get_env(self, key):
        envs = self._getEnvs()
        return envs[key]

    def get_env_val(self, key, defaultValue=None):
        envs = self._getEnvs()
        if key in envs:
            return envs[key]
        return defaultValue


OsEnv = OsEnv()
