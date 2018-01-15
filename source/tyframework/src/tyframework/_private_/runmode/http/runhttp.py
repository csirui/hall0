# -*- coding=utf-8 -*-
from tyframework._private_.runmode.http.runhttp_action import RunHttpAction
from tyframework._private_.runmode.http.runhttp_params import RunHttpParams
from tyframework._private_.runmode.http.runhttp_register import RunHttpRegister
from tyframework._private_.runmode.http.runhttp_sdk_proxy import RunHttpSdkProxy
from tyframework._private_.runmode.http.runhttp_static import RunHttpStatic


class RunHttp(RunHttpAction, RunHttpParams, RunHttpRegister, RunHttpStatic, RunHttpSdkProxy):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _init_singleton_(self):
        RunHttpAction._init_singleton_(self)
        RunHttpParams._init_singleton_(self)
        RunHttpRegister._init_singleton_(self)
        RunHttpStatic._init_singleton_(self)
        RunHttpSdkProxy._init_singleton_(self)

    def __init__(self):
        pass


RunHttp = RunHttp()
