# -*- coding=utf-8 -*-

import datetime

from tyframework.context import TyContext

stats = {'all': 0, 'na': 0, }
start_time = datetime.datetime.now()


def monitor(execute):
    global stats

    def count(obj, rpath):
        stats['all'] += 1
        try:
            stats[rpath] += 1
        except:
            stats[rpath] = 1

    from functools import wraps
    @wraps(execute)
    def wrapper(obj, rpath):
        count(obj, rpath)
        return execute(obj, rpath)

    return wrapper


class HttpExecuter(object):
    '''
    de
    '''

    def getJsonPaths(self):
        return getattr(self, 'JSONPATHS', {})

    def getHtmlPaths(self):
        return getattr(self, 'HTMLPATHS', {})

    def jsonApiIntercept(self, rpath):
        return False, None

    @monitor
    def execute(self, rpath):
        TyContext.ftlog.debug(self, 'execute', rpath)
        paths = self.getJsonPaths()
        if rpath in paths:
            fun = paths[rpath]
            self.execJsonApi(rpath, fun)
            return True

        paths = self.getHtmlPaths()
        if rpath in paths:
            fun = paths[rpath]
            self.execHtml(rpath, fun)
            return True

        return False

    def execJsonApi(self, rpath, fun):
        mo = None
        try:
            isReturn, mo = self.jsonApiIntercept(rpath)
            if not isReturn:
                mo = fun(rpath)
        except TyContext.MySqlSwapException, e:
            TyContext.ftlog.error('execJsonApi', rpath,
                                  'failed get cold data for userid', e.userid)
            mo = TyContext.Cls_MsgPack()
            mo.setCmd(rpath)
            mo.setError(1, 'you user id not on this server, please delete the'
                           ' user info file on you mobile and try again.')
        except:
            TyContext.ftlog.exception()

        try:
            if mo == None:
                mo = TyContext.Cls_MsgPack()
                mo.setCmd(rpath)
                mo.setError(1, 'system error')
            if isinstance(mo, (str, unicode)):
                jsonstr = mo
            elif isinstance(mo, (list, tuple, dict, set)):
                jsonstr = TyContext.strutil.dumps(mo)
            elif isinstance(mo, (int, float, bool)):
                jsonstr = str(mo)
            else:
                jsonstr = mo.packJson()
        except:
            TyContext.ftlog.exception()
            jsonstr = 'system error 2'

        TyContext.RunHttp.doRequestFinish(jsonstr, {'Content-Type': 'application/json;charset=UTF-8'}, rpath)

    def execHtml(self, rpath, fun):
        html = None
        try:
            html = fun(rpath)
        except:
            TyContext.ftlog.exception(rpath)
        if not html:
            html = 'system error'
        elif html == 'redirected':
            return
        TyContext.RunHttp.doRequestFinish(html, {'Content-Type': 'text/html;charset=UTF-8'}, rpath)

    @classmethod
    def get_stats(cls, rpath):
        global stats
        return stats

    @classmethod
    def get_service_start_time(cls):
        global start_time
        return start_time
