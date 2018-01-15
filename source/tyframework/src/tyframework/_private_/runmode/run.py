# -*- coding=utf-8 -*-

import stackless
from stackless import bomb


class __NW_Channel__(stackless.channel):
    def send_nowait(self, v):
        if self.balance == 0:
            self.value = v
        else:
            self.send(v)

    def send_exception_nowait(self, ntype, value):
        if self.balance == 0:
            self.exc = (ntype, value)
        else:
            if isinstance(value, ntype):
                self.send(bomb(ntype, value))
            else:
                self.send_exception(ntype, value)

    def receive(self):
        if hasattr(self, 'value'):
            v = self.value
            del self.value
            return v
        if hasattr(self, 'exc'):
            ntype, value = self.exc
            del self.exc
            raise ntype, value
        return stackless.channel.receive(self)


class __TYTasklet__(object):
    def __init__(self, target, *argl, **argd):
        self._target_ = target
        self._target_argl_ = argl
        self._target_argd_ = argd
        self._channel_ = __NW_Channel__()
        self._timer_id_ = 0
        self._ty_ext_datas_ = {}

    def _run_(self):
        t = stackless.getcurrent()
        try:
            timerid = self._timer_id_
            if timerid <= 0:
                self._target_(*self._target_argl_, **self._target_argd_)
            else:
                if timerid in TYRun.__timer_control__:
                    del TYRun.__timer_control__[timerid]
                    self._target_(*self._target_argl_, **self._target_argd_)
        finally:
            t._tyTasklet = None

    def _wait_for_deferred_(self, d, tips):
        d.addCallback(self.__successful_deferred__)
        d.addErrback(self.__error_deferred__)
        return self._channel_.receive()

    def __successful_deferred__(self, resmsg):
        self._channel_.send_nowait(resmsg)

    def __error_deferred__(self, fault):
        self._channel_.send_exception_nowait(fault.type, fault.value)


class TYRun(object):
    def __call__(self, *args, **argd):
        return self

    def __init__(self):
        self.__reactor__ = None
        self.__timer_id__ = 0
        self.__timer_control__ = {}

    def install(self):
        try:
            from twisted.internet import epollreactor
            epollreactor.install()
        except:
            pass
        from twisted.internet import reactor
        self.__reactor__ = reactor

    def main_loop(self):
        self.tasklet_schedule(self.__run_reactor__)
        stackless.run()

    def __run_reactor__(self, r=None):
        r = self.__reactor__
        r.startRunning()
        while r.running:
            try:
                t2 = r.timeout()
                t = r.running and t2
                r.iterate(t)
            except:
                from tyframework.context import TyContext
                TyContext.ftlog.exception()
                print "TYReactor Unexpected error in main loop."
            finally:
                if stackless.getruncount() > 1:
                    stackless.schedule()
        print 'TYReactor Main loop terminated.'

    def get_tasklet_current(self):
        t = stackless.getcurrent()
        return t._tyTasklet

    def get_tasklet_ext_datas(self):
        tasklet = self.get_tasklet_current()
        _ty_ext_datas_ = getattr(tasklet, '_ty_ext_datas_', None)
        if _ty_ext_datas_ == None:
            _ty_ext_datas_ = {}
            setattr(tasklet, '_ty_ext_datas_', _ty_ext_datas_)
        return _ty_ext_datas_

    def _wait_for_deferred_(self, d, tips):
        tasklet = self.get_tasklet_current()
        result = tasklet._wait_for_deferred_(d, tips)
        return result

    def tasklet_schedule(self, target, *argl, **argd):
        tasklet = __TYTasklet__(target, *argl, **argd)
        t = stackless.tasklet(tasklet._run_)()
        t._tyTasklet = tasklet
        return tasklet

    def __callLater_schedule__(self, datas):
        tasklet = __TYTasklet__(datas[0])
        tasklet._target_argl_ = datas[1]
        tasklet._target_argd_ = datas[2]
        tasklet._timer_id_ = datas[3]
        t = stackless.tasklet(tasklet._run_)()
        t._tyTasklet = tasklet
        return tasklet

    def calllater(self, interval, target, *argl, **argd):
        timerobj = self.__reactor__.callLater(interval, target, *argl, **argd)
        return timerobj

    def setup_timer(self, interval, target, *argl, **argd):
        self.__timer_id__ += 1
        timerargs = (target, argl, argd, self.__timer_id__)
        timerobj = self.__reactor__.callLater(interval, self.__callLater_schedule__, timerargs)
        self.__timer_control__[self.__timer_id__] = timerobj
        return self.__timer_id__

    def cancel_timer(self, timerid):
        timerobj = self.__timer_control__.get(timerid, None)
        if timerobj:
            del self.__timer_control__[timerid]
            try:
                timerobj.cancel()
                return True
            except:
                pass
        return False

    def get_timer_timeout(self, timerid):
        timerobj = self.__timer_control__.get(timerid, None)
        if timerobj:
            try:
                return timerobj.getTime()
            except:
                pass
        return -1

    def reset_timer(self, timerid, interval):
        timerobj = self.__timer_control__.get(timerid, None)
        if timerobj:
            try:
                timerobj.reset(interval)
                return True
            except:
                pass
        return False


TYRun = TYRun()
