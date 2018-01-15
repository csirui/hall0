# -*- coding=utf-8 -*-

import stackless

from tyframework.context import TyContext


class SimpleTasklet():
    def tasklet(self):
        self.taskletType = 0
        self.__me__ = stackless.getcurrent()
        self.__me__._tyTasklet = self
        self.__return_channel__ = TyContext.NWChannel()
        try:
            self.handle()
        except:
            TyContext.ftlog.exception('TASKLET HANDLE ERROR')

    def handle(self):
        pass

    def _wait_for_deferred_(self, d, tips):
        try:
            d.addCallback(self.__successful_deferred__)
            d.addErrback(self.__error_deferred__)
            return self.__return_channel__.receive()
        except Exception, e:
            TyContext.ftlog.exception(tips, e)
            raise e

    def __successful_deferred__(self, resmsg):
        self.__return_channel__.send_nowait(resmsg)
        if stackless.getcurrent() != self.__me__:
            stackless.schedule()

    def __error_deferred__(self, fault):
        self.__return_channel__.send_exception_nowait(fault.type, fault.value)
        if stackless.getcurrent() != self.__me__:
            stackless.schedule()
