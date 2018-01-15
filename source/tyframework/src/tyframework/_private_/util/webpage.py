# -*- coding=utf-8 -*-

import urllib

from twisted.web import client

# add this to suppressing "Starting/Stopping HTTPClientFactory" log by twisted
client.HTTPClientFactory.noisy = False


class WebPage(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def webget_json(self, httpurl, datas={}, appKey=None):
        response, httpurl = self.webget(httpurl, datas, appKey)
        datas = None
        try:
            datas = self.__ctx__.strutil.loads(response)
        except:
            self.__ctx__.ftlog.exception()
        return datas, httpurl

    def webget(self, httpurl, querys={}, appKey=None, postdata_='', method_='POST', headers_={}, cookies={}):
        params = []
        if isinstance(querys, (list, tuple)):
            params.extend(querys)
        elif isinstance(querys, dict):
            keys = querys.keys()
            keys.sort()
            for k in keys:
                params.append(k)
                params.append(querys[k])

        for x in xrange(len(params)):
            param = params[x]
            if isinstance(param, unicode):
                param = param.encode('utf8')
            else:
                param = str(param)
            params[x] = param

        query2 = []
        query = []
        for x in xrange(len(params) / 2):
            k = params[x * 2]
            v = params[x * 2 + 1]
            query.append(k + '=' + v)
            if k == 'authInfo':
                query2.append(k + '=' + v)
            else:
                query2.append(k + '=' + urllib.quote(v))
        query = '&'.join(query)
        query2 = '&'.join(query2)
        if appKey:
            md5str = str(appKey) + query + str(appKey)
            md5code = self.__ctx__.strutil.md5digest(md5str)
            query2 = query2 + '&code=' + md5code

        if isinstance(httpurl, unicode):
            httpurl = httpurl.encode('utf8')

        if len(query2) > 0:
            if httpurl.find('?') > 0:
                httpurl = httpurl + '&' + query2
            else:
                httpurl = httpurl + '?' + query2

        if isinstance(httpurl, unicode):
            httpurl = httpurl.encode('utf8')

        if postdata_ and isinstance(postdata_, dict):
            postdata_ = urllib.urlencode(postdata_)

        if headers_ == None or len(headers_) == 0:
            headers_ = {'Content-type': 'application/x-www-form-urlencoded'}

        self.__ctx__.ftlog.info('webget httpurl=', httpurl, method_, postdata_)
        tasklet = self.__ctx__.getTasklet()
        tasklet._report_wait_prep_(httpurl)
        d = client.getPage(httpurl, method=method_, headers=headers_, postdata=postdata_, cookies=cookies)
        response = tasklet._wait_for_deferred_(d, httpurl[:60])
        self.__ctx__.ftlog.info('webget httpurl return=', response, 'httpurl=', httpurl)

        return response, httpurl


WebPage = WebPage()
