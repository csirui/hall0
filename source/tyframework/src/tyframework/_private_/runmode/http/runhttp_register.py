# -*- coding=utf-8 -*-

import functools
import inspect
from operator import isCallable


def http_request_entry(httppath=None, jsonp=False, ip_filter=False, extend_tag=None, response='json'):
    if jsonp:
        jsonp = 1
    else:
        jsonp = 0

    if ip_filter:
        ip_filter = 1
    else:
        ip_filter = 0

    if not response in ('json', 'html'):
        response = 'json'

    entry = {
        'registed': 0,
        'jsonp': jsonp,
        'need_ip_filter': ip_filter,
        'extend_tag': extend_tag,
        'response': response,
        'httppath': httppath
    }

    def decorating_function(method):

        paramkeys, _, __, ___ = inspect.getargspec(method)
        if len(paramkeys) > 0:  # 去除self和cls关键字
            if paramkeys[0] in ('self', 'cls'):
                paramkeys = paramkeys[1:]
        entry['paramkeys'] = paramkeys

        @functools.wraps(method)
        def funwarp(*args, **argd):
            from tyframework.context import TyContext
            return TyContext.RunHttp._http_rquest_entry_wrap_call_(entry, method, *args, **argd)

        setattr(funwarp, '_http_request_entry_', entry)

        return funwarp

    return decorating_function


class RunHttpRegister(object):
    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext
        self.TRACE_RESPONSE = 1

    def _init_singleton_(self):
        self.TRACE_RESPONSE = 1
        self.RESPONSE_CONTENT_TYPE_JSON = {'Content-Type': 'application/json;charset=UTF-8'}
        self.RESPONSE_CONTENT_TYPE_HTML = {'Content-Type': 'text/html;charset=UTF-8'}
        self.__path_methods__ = {}

    def _http_rquest_entry_wrap_call_(self, entry, method, *args, **argd):

        if entry.get('registed', 0) != 1:
            # 未使用add_handler方法进行注册
            return method(*args, **argd)

        apiobj = args[0]  # 第0个为self或cls
        msg, values = self.__check_request_params__(apiobj, entry['paramkeys'], entry['extend_tag'])
        if msg:
            return self.__stringify_http_response__(entry['jsonp'], msg)

        msg = method(apiobj, *values)
        return self.__stringify_http_response__(entry['jsonp'], msg)

    def _dummy_json_api_intercept_(self, rpath):
        return False, None

    def _dummy_fun_ip_filter_(self, ip):
        return None

    def __register_http_entry__(self, handler, method, entry, api_style_ver=3):
        # 设置注册标记
        entry['registed'] = 1
        entry['api_style_ver'] = api_style_ver

        # 确定HTTP的API路径
        httppath = entry.get('httppath', None)
        if not isinstance(httppath, (str, unicode)) or len(httppath) <= 0:
            httppath = method.__name__.replace('_', '/')
            if httppath.find('do/http/') == 0:
                httppath = httppath[7:]
            if httppath[0] != '/':
                httppath = '/' + httppath
            while httppath.find('//') >= 0:
                httppath = httppath.replace('//', '/')
            entry['httppath'] = httppath

        # 确定是否需要IP过滤
        entry['ip_filter'] = self._dummy_fun_ip_filter_
        if entry['need_ip_filter']:
            ip_filter = getattr(handler, 'ip_filter', None)
            if isCallable(ip_filter):
                entry['ip_filter'] = ip_filter

        # 确定是否有JSON API切面方法
        entry['json_api_intercept'] = self._dummy_json_api_intercept_
        if entry['response'] == 'json':
            jsonApiIntercept = getattr(handler, 'jsonApiIntercept', None)
            if jsonApiIntercept != None and isCallable(jsonApiIntercept):
                entry['json_api_intercept'] = jsonApiIntercept

        # 确定返回的ContentType
        if entry['response'] == 'json' or entry['jsonp'] == 1:
            entry['content_type'] = self.RESPONSE_CONTENT_TYPE_JSON
        else:
            entry['content_type'] = self.RESPONSE_CONTENT_TYPE_HTML

        if httppath in self.__path_methods__:
            raise Exception('the http path already defined !! httppath=' + str(httppath))
        self.__path_methods__[httppath] = (method, entry)
        self.__ctx__.ftlog.info('RunHttp Add Path ->', httppath, 'method=', method)
        return httppath

    def __stringify_http_response__(self, isjsonp, content):
        if (isinstance(content, (str, unicode))):
            pass
        elif (isinstance(content, self.__ctx__.MsgPack)):
            content = content.packJson()
        elif (isinstance(content, (list, tuple, dict, set))):
            content = self.__ctx__.strutil.dumps(content)
        elif (isinstance(content, (int, float, bool))):
            content = str(content)
        else:
            content = repr(content)
        content = content.encode('utf-8')
        if isjsonp:
            callback = self.getRequestParam('callback', '').strip()
            if len(callback) > 0:
                content = '%s(%s);' % (callback, content)
        return content

    def __check_request_params__(self, apiobj, paramkeys, extend_tag):
        values = []
        params = {}
        if not paramkeys:
            return None, values
        key, funname = None, None
        for key in paramkeys:
            funname = '_check_param_' + key
            func = getattr(apiobj, funname, None)
            error, value = func(key, params, extend_tag)
            if error:
                return error, None
            values.append(value)
            params[key] = value
        return None, values

    def add_handler(self, handler):
        '''
        添加一个HTTP请求处理的入口实例
        参数: handler HTTP请求的类或实例, 其定义的HTTP方法必须使用: @http_request_entry 进行修饰
        '''
        self.__ctx__.ftlog.info('RunHttp Add Handler ->', handler)

        for key in dir(handler):
            method = getattr(handler, key)
            if isCallable(method):
                entry = getattr(method, '_http_request_entry_', None)
                if isinstance(entry, dict):
                    self.__register_http_entry__(handler, method, entry, 3)

    def add_router(self, router):
        '''
        @deprecate
        此方法已经不提倡使用, 请使用 @http_request_entry 和 add_handler 方法
        '''
        self.__ctx__.ftlog.error('RunHttp.add_router is deprecate !!!!')
        self.__add_handler__(router, 1)

    def add_executer(self, router):
        '''
        @deprecate
        此方法已经不提倡使用, 请使用 @http_request_entry 和 add_handler 方法
        '''
        self.__ctx__.ftlog.error('RunHttp.add_executer is deprecate !!!!')
        self.__add_handler__(router, 2)

    def __add_handler__(self, router, api_style_ver):
        '''
        @deprecate
        此方法已经不提倡使用, 请使用 @http_request_entry 和 add_handler 方法
        '''
        self.__ctx__.ftlog.info('RunHttp Add Handler ->', router)

        if isCallable(getattr(router, 'getJsonPaths', None)):
            jsons = router.getJsonPaths()
            if jsons:
                for httppath, httpfun in jsons.items():
                    entry = {
                        'registed': 0,
                        'jsonp': 0,
                        'need_ip_filter': 0,
                        'extend_tag': None,
                        'response': 'json',
                        'httppath': httppath
                    }
                    self.__register_http_entry__(router, httpfun, entry, api_style_ver)

        if isCallable(getattr(router, 'getHtmlPaths', None)):
            htmls = router.getHtmlPaths()
            if htmls:
                for httppath, httpfun in htmls.items():
                    entry = {
                        'registed': 0,
                        'jsonp': 0,
                        'need_ip_filter': 0,
                        'extend_tag': None,
                        'response': 'html',
                        'httppath': httppath
                    }
                    self.__register_http_entry__(router, httpfun, entry, api_style_ver)

    def handler_http_request(self, httprequest):
        mo = None
        try:
            rpath = httprequest.path
            if self.TRACE_RESPONSE:
                self.__ctx__.ftlog.info('HTTPREQUEST', rpath, httprequest.args)

            extdatas = self.__ctx__.TYRun.get_tasklet_ext_datas()
            extdatas[self.EXT_KEY_HTTP_REQUEST] = httprequest

            # 游戏服务SDK代理处理
            if self._handler_http_sdk_proxy_(httprequest):
                return

            # 当前服务处理
            funhttp, entry = self.__path_methods__.get(rpath, (None, None))
            if funhttp == None or entry == None:
                self.__handler_http_static__(httprequest)
                return  # 查找静态资源返回

            # IP 地址过滤
            if entry['need_ip_filter']:
                ip = self.get_client_ip()
                mo = entry['ip_filter'](ip)
                if mo:
                    mo = self.__stringify_http_response__(entry['jsonp'], mo)
                    self.doRequestFinish(mo, entry['content_type'], rpath)
                    return  # IP 过滤失败, 返回

            # 代理的SDK API检查
            self.__ctx__.RunMode.check_game_server_mode()

            # 执行动态调用
            try:
                isReturn, mo = entry['json_api_intercept'](rpath)
                if not isReturn:
                    apiver = entry['api_style_ver']
                    if apiver == 1:
                        tasklet = self.__ctx__.getTasklet()
                        mo = funhttp(tasklet, rpath)  # 老版本的带tasklet和rpath的定义方法
                    elif apiver == 2:
                        mo = funhttp(rpath)  # 老版本的带rpath的定义方法
                    else:  # apiver == 3 :
                        mo = funhttp()  # 最新版本的 @http_request_entry 方法
                    if mo == None:
                        mo = self.__ctx__.Cls_MsgPack()
                        mo.setCmd(rpath)
                        mo.setError(1, 'http api return None')
                else:
                    if mo == None:
                        mo = self.__ctx__.Cls_MsgPack()
                        mo.setCmd(rpath)
                        mo.setError(1, 'json_api_intercept return None')
            except self.__ctx__.MySqlSwapException, e:
                self.__ctx__.ftlog.error('handler_http_request', rpath,
                                         'failed get cold data for userid', e.userid)
                mo = self.__ctx__.MsgPack()
                mo.setCmd(rpath)
                mo.setError(1, 'you user id not on this server, please delete the'
                               ' user info file on you mobile and try again.')
            except self.__ctx__.FreetimeException, e:
                mo = self.__ctx__.MsgPack()
                mo.setCmd(rpath)
                mo.setResult('code', e.errorCode)
                mo.setResult('info', e.message)
                mo.setError(e.errorCode, e.message)
            except:
                self.__ctx__.ftlog.exception()
                mo = self.__ctx__.Cls_MsgPack()
                mo.setCmd(rpath)
                mo.setError(1, 'http api exception')

            mo = self.__stringify_http_response__(entry['jsonp'], mo)
            self.doRequestFinish(mo, entry['content_type'], rpath)
        except:
            self.__ctx__.ftlog.exception()
            mo = self.__ctx__.Cls_MsgPack()
            mo.setCmd(rpath)
            mo.setError(1, 'system exception return')
            mo = self.__stringify_http_response__(0, mo)
            self.doRequestFinish(mo, self.RESPONSE_CONTENT_TYPE_HTML, rpath)
