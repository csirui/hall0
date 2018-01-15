# -*- coding=utf-8 -*-


class TyDeffer:
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def add_default_callback(self, deffer_, filename, func_name, *params):
        deffer_.addCallback(self.__successful_default_callback__)
        deffer_.addErrback(self.__error_default_callback__, filename, func_name, params)

    def __successful_default_callback__(self, *argl, **argd):
        pass

    # noinspection PyMethodMayBeStatic
    def __error_default_callback__(self, fault, filename, func_name, params):
        from tyframework.context import TyContext
        TyContext.ftlog.error('Traceback ERROR, File ' + str(filename) + ', in ' + str(func_name)
                              + ' Fault=' + str(fault) + ' Params=', params)
        TyContext.ftlog.exception()


TyDeffer = TyDeffer()
