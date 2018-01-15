# -*- coding=utf-8 -*-
from tyframework._private_.util.ftlog import ftlog
from tyframework._private_.util.initreactor import tychannel, tygetcurrent


class Locker(tychannel):
    def lockInit(self, lockkey):
        self.lockkey = lockkey
        self._islock = False
        self.tasklet = None
        self.relock = 0
        self.debug = 0

    def lock(self):
        if self._islock == True:
            if self.tasklet == tygetcurrent():
                self.relock += 1
                if self.debug: ftlog.info('locker', self.lockkey, 'lock relock', self.relock)
                return
            if self.debug: ftlog.info('locker', self.lockkey, ', lock receive start')
            self.receive()

        if self.debug: ftlog.info('locker', self.lockkey, 'lock succ')
        self._islock = True
        self.tasklet = tygetcurrent()

    def unlock(self):
        if self.relock > 0:
            self.relock -= 1
            if self.debug: ftlog.info('locker', self.lockkey, 'unlock, relock', self.relock)
            return

        self.tasklet = None
        self._islock = False
        if self.debug: ftlog.info('locker', self.lockkey, 'unlock, send')
        if self.balance < 0:
            self.send(0)


def syncobjectmethod(func):
    def syncfunc(*args, **argkw):
        objself = args[0]
        if not hasattr(objself, '__object_locker__'):
            objself.__object_locker__ = Locker()
            objself.__object_locker__.lockInit(objself)

        objself.__object_locker__.lock()
        ret = None
        error = None
        try:
            ret = func(*args, **argkw)
        except Exception, error:
            ftlog.exception(error, 'ERROR func=', func.__name__, 'args=', args, 'argkw=', argkw)
            ret = None
        objself.__object_locker__.unlock()
        if error != None:
            raise error
        return ret

    return syncfunc
