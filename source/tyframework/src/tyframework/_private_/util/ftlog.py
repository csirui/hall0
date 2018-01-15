# -*- coding=utf-8 -*-

import os
import traceback

from datetime import datetime


class ftlog(object):
    def __call__(self, *argl, **argd):
        return self

    def __init__(self):
        self.LOG_DEBUG = 1
        self.LOG_DEBUG_METHOD = 1
        self.LOG_DEBUG_FUN = 1
        self.LOG_DEBUG_NET = 1
        self.__LOG_BUFFER__ = []
        self.flogger = None
        self.stdf = None

    def _init_singleton_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext
        debuglog = 0
        if self.__ctx__.TYGlobal.mode() == 1:
            if self.__ctx__.TYGlobal.simulation():
                debuglog = 1
            else:
                debuglog = 0
        elif self.__ctx__.TYGlobal.mode() == 2:
            debuglog = 0
        else:
            debuglog = 1
        if debuglog:
            self.set_debug(1)
            self.set_debug_net(1)
        else:
            self.set_debug(0)
            self.set_debug_net(0)
        self.info('Configure->reload debuglog=', debuglog)

    def tygetcurrent(self):
        return 0

    def is_debug(self):
        return self.LOG_DEBUG

    def is_debug_net(self):
        return self.LOG_DEBUG_NET

    def is_debug_method(self):
        return self.LOG_DEBUG_METHOD

    def is_debug_fun(self):
        return self.LOG_DEBUG_FUN

    def set_debug(self, isenable):
        if isenable:
            self.LOG_DEBUG = 1
        else:
            self.LOG_DEBUG = 0
        return self.LOG_DEBUG

    def set_debug_net(self, isenable):
        if isenable:
            self.LOG_DEBUG_NET = 1
        else:
            self.LOG_DEBUG_NET = 0
        return self.LOG_DEBUG_NET

    def set_debug_method(self, isenable):
        if isenable:
            self.LOG_DEBUG_METHOD = 1
        else:
            self.LOG_DEBUG_METHOD = 0
        return self.LOG_DEBUG_METHOD

    def set_debug_fun(self, isenable):
        if isenable:
            self.LOG_DEBUG_FUN = 1
        else:
            self.LOG_DEBUG_FUN = 0
        return self.LOG_DEBUG_FUN

    def open_normal_logfile(self, log_file_fullpath):
        import logging.handlers
        my_logger = logging.getLogger(log_file_fullpath)
        my_logger.setLevel(logging.DEBUG)
        handler = logging.handlers.TimedRotatingFileHandler(log_file_fullpath, when='MIDNIGHT')
        my_logger.addHandler(handler)
        return my_logger

    def open_stdout_logfile(self, log_file_fullpath):
        if self.__LOG_BUFFER__ != None:
            outpath = os.path.dirname(log_file_fullpath)
            outfile = os.path.basename(log_file_fullpath)
            from twisted.python import logfile
            from twisted.python import log as twisted_log
            class __TyFileLogObserver__(twisted_log.FileLogObserver):
                twisted_log.FileLogObserver.timeFormat = '%m-%d %H:%M:%S.%f'

                def emit(self, eventDict):
                    eventDict['system'] = '-'
                    twisted_log.FileLogObserver.emit(self, eventDict)

            logf = logfile.DailyLogFile(outfile, outpath)
            for line in self.__LOG_BUFFER__:
                logf.write(line)
                logf.write('\n')
            flo = __TyFileLogObserver__(logf)
            twisted_log.startLoggingWithObserver(flo.emit)
            self.__LOG_BUFFER__ = None

    def __convert__(self, value):
        if isinstance(value, str):
            return value
        if isinstance(value, (int, long, bool, float)):
            return str(value)
        if isinstance(value, unicode):
            try:
                return unicode(value).encode('utf-8')
            except:
                return repr(value)
        return self.to_string(value)

    def __write__(self, tag, args):
        if self.__LOG_BUFFER__ == None:
            lines = [tag, str(id(self.tygetcurrent())), '|']
        else:
            lines = [datetime.now().strftime('%m-%d %H:%M:%S.%f'), '[-]',
                     tag, str(id(self.tygetcurrent())), '|']

        for x in args:
            lines.append(self.__convert__(x))
        line = ' '.join(lines)

        print line
        if self.__LOG_BUFFER__ != None:
            if len(self.__LOG_BUFFER__) < 10000:
                self.__LOG_BUFFER__.append(line)

    maxlen_config = 2048

    def to_string(self, obj, maxlen=maxlen_config, needeascp=False):
        datas = []
        self.__makelines__(obj, datas, maxlen, 1)
        str1 = ''.join(datas)
        if needeascp:
            str1 = str1.replace('\n', '\\n')
            str1 = str1.replace('\d', '\\\\d')
            str1 = str1.replace('\r', '')
        return str1

    def __makelines__(self, obj, datas, maxlen, flg=0):
        dtype = type(obj)
        if dtype == unicode:
            obj = obj.encode('utf-8')
            if maxlen > 0 and len(obj) > maxlen:
                obj = obj[0:maxlen] + '......'
            if flg:
                datas.append(obj)
            else:
                datas.append('"')
                datas.append(obj)
                datas.append('"')

        elif dtype == str:
            if maxlen > 0 and len(obj) > maxlen:
                obj = obj[0:maxlen] + '......'
            if flg:
                datas.append(obj)
            else:
                datas.append('"')
                datas.append(obj)
                datas.append('"')

        elif dtype == int or dtype == long or dtype == bool or dtype == float:
            datas.append(str(obj))

        elif dtype == list:
            datas.append('[')
            i = 0
            for sobj in obj:
                if i > 0:
                    datas.append(', ')
                self.__makelines__(sobj, datas, maxlen)
                i = 1
            datas.append(']')

        elif dtype == tuple:
            datas.append('(')
            i = 0
            for sobj in obj:
                if i > 0:
                    datas.append(', ')
                self.__makelines__(sobj, datas, maxlen)
                i = 1
            datas.append(')')

        elif dtype == dict:
            datas.append('{')
            i = 0
            for k, v in obj.items():
                if i > 0:
                    datas.append(', ')
                if isinstance(k, unicode):
                    k = k.encode('utf-8')
                else:
                    k = str(k)
                datas.append('"')
                datas.append(k)
                datas.append('":')
                self.__makelines__(v, datas, maxlen)
                i = 1
            datas.append('}')

        else:
            obj = str(obj)
            if maxlen > 0 and len(obj) > maxlen:
                obj = obj[0:maxlen] + '......'
            if flg:
                datas.append(obj)
            else:
                datas.append('"')
                datas.append(obj)
                datas.append('"')

    def info(self, *args):
        self.__write__('I', args)

    def error(self, *args):
        try:
            self.__write__('E', args)
        except:
            pass

    def warn(self, *args):
        self.__write__('W', args)

    def fatal(self, *args):
        self.__write__('F', args)

    def exception(self, *args):
        self.__write__('E', ['************************************************************'])
        self.__write__('E', args)
        traceback.print_exc(file=self.stdf)
        self.__write__('E', ['------------------------ Call Stack ------------------------'])
        traceback.print_stack(file=self.stdf)
        self.__write__('E', ['************************************************************'])

    def format_exc(self, limit=None):
        return traceback.format_exc(limit)

    def print_stack(self, limit=None, *args):
        self.__write__('E', ['************************************************************'])
        self.__write__('E', args)
        traceback.print_stack(limit=limit, file=self.stdf)
        self.__write__('E', ['************************************************************'])

    def client(self, *args):
        self.__write__('C', args)

    def debug(self, *args):
        if self.LOG_DEBUG:
            try:
                self.__write__('D', args)
            except:
                pass

    def debug_net(self, *args):
        if self.LOG_DEBUG_NET:
            self.__write__('N', args)

    def debug_methods(self, tag, mdict):
        if self.LOG_DEBUG_METHOD:
            paths = mdict.keys()
            paths.sort()
            for path in paths:
                strm = self.to_string(mdict[path])
                if strm.find('bound method classobj') > 0:
                    strm = strm.split(' ')
                    strm = strm[5] + '.' + strm[2].split('.')[-1] + '()'
                self.__write__('M', [tag, '>>', path, '>>', strm])

    def funin(self, obj, funname, *args):
        if self.LOG_DEBUG_FUN and getattr(obj, '_debug', 0):
            nlist = ['*****', funname, '*****']
            nlist.extend(args)
            self.__write__('FI', [])
            self.__write__('FI', [])
            self.__write__('FI', nlist)
            if hasattr(obj, 'dump'):
                obj.dump(funname + ' in')

    def funout(self, obj, funname, *args):
        if self.LOG_DEBUG_FUN and getattr(obj, '_debug', 0):
            nlist = ['*****', funname, '*****']
            nlist.extend(args)
            self.__write__('FO', nlist)
            if hasattr(obj, 'dump'):
                obj.dump(funname + ' out')
            self.__write__('FO', [])
            self.__write__('FO', [])
            self.__write__('FO', [])

    def chipUpdate(self, uid, loc, event, delta, final, gameId=-1):
        self.info('CHIPUPDATE:<gameid=', gameId, '><userid=', uid, '><loc=', loc, '><event=', event, '><delta=', delta,
                  '><final=', final, '>')

    def couponUpdate(self, uid, loc, event, delta, final, gameId=-1):
        self.info('COUPONUPDATE:<gameid=', gameId, '><userid=', uid, '><loc=', loc, '><event=', event, '><delta=',
                  delta, '><final=', final, '>')


ftlog = ftlog()
