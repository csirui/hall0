'''
Created on 2013-3-8

@author: Administrator
'''
import stackless
from twisted.internet import reactor


class GameTimer(object):
    def __init__(self, timerCount):
        self._timer = [None] * timerCount
        self._intervals = [0] * timerCount

    def onTimeUp(self, msg, gdata, timerid):
        from freetime.tasklet.game import GameTasklet
        c = GameTasklet(gdata, None, None, None, msg)
        stackless.tasklet(c.tasklet)()
        reactor.callLater(0, stackless.schedule)

        self._timer[timerid] = None
        self._intervals[timerid] = 0

    def has_timer(self, timerId):
        return not self._timer[timerId] is None

    def setupTimer(self, timerid, interval, msg, gdata):
        self.cancelTimer(timerid)
        if (interval < 0):
            interval = 0
        msg.setParam('debug_timer_tid', timerid)
        msg.setParam('debug_timer_int', interval)
        self._timer[timerid] = reactor.callLater(interval, self.onTimeUp, msg, gdata, timerid)
        self._intervals[timerid] = interval

    def getTimeOut(self, timerid):
        ts = self._timer[timerid]
        if not ts:
            return 0.0
        try:
            return ts.getTime()
        except:
            pass
        return 0.0

    def getTimerInterval(self, timerid):
        return self._intervals[timerid]

    def resetTimer(self, timerid, interval):
        ts = self._timer[timerid]
        if ts:
            try:
                ts.reset(interval)
                self._intervals[timerid] = interval
                return True
            except:
                pass
        return False

    def cancelTimer(self, timerid):
        ts = self._timer[timerid]
        if not ts:
            return False
        try:
            ts.cancel()
        except:
            pass
        self._timer[timerid] = None;
        self._intervals[timerid] = 0
        return True

    def cancelTimerAll(self):
        for i in xrange(len(self._timer)):
            self.cancelTimer(i)
