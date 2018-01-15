# -*- coding=utf-8 -*-
''' 管理接口 '''

from tyframework.context import TyContext


class HttpManagement(object):
    JSONPATHS = None
    HTMLPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
            }
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                '/mgt/test': cls.__test,
                '/mgt/stats': cls.__stats,
                '/mgt/execfile': cls.__execfile,
            }
        return cls.HTMLPATHS

    @classmethod
    def __test(cls, rpath):
        return 'it works like a charm'

    @classmethod
    def __stats(cls, rpath):
        import datetime
        uptime = str(datetime.datetime.now() - cls.get_service_start_time())
        stats = cls.get_stats(rpath)
        lines = list()
        for s in stats:
            lines.append((stats[s], s))
        from operator import itemgetter
        return 'uptime: ' + uptime + '<p/>' + \
               '<p/>'.join(['%d %s' % (line[0], line[1]) for line in sorted(lines, key=itemgetter(0), reverse=True)])

    @classmethod
    def __execfile(self, rpath):
        """ 用 execfile 动态执行消息中指定的脚本文件，来实现动态的调试、
        更新、 bug修复、数据调整等

        e.g. http://125.39.218.101:8100/mgt/execfile?f=/home/test1/tysdk/webroot/11.py&p=22,33,abc
        e.g 11.py source:
            c = exec_context
            params = exec_params
            result = exec_result
            def parameterize(param):
                return tuple(param.split(','))

            argv = parameterize(params)
            result['argv'] = argv
        """

        TyContext.ftlog.debug("__execfile", rpath)
        fname = TyContext.RunHttp.getRequestParam('f')
        params = TyContext.RunHttp.getRequestParam('p')
        execfile_result = {}
        execfile_globals = {
            'exec_fname': fname,
            'exec_params': params,
            'exec_context': TyContext,
            'exec_result': execfile_result,
        }
        try:
            execfile(fname, execfile_globals)
            return TyContext.strutil.dumps(execfile_result)
        except:
            import traceback
            result_json = traceback.format_exc()
            TyContext.ftlog.exception('__execfile', execfile_globals)
            return result_json
