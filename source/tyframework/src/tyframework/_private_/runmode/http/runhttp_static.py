# -*- coding=utf-8 -*-

import datetime
import os


class RunHttpStatic(object):
    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _init_singleton_(self):
        self.__path_webroots__ = []
        self.__STATIC_POOL__ = {}
        self.add_webroot(os.environ['PATH_WEBROOT'])

    def add_webroot(self, webroot):
        self.__ctx__.ftlog.info('RunHttp Add WEBROOT ->', webroot)
        if not webroot in self.__path_webroots__:
            self.__path_webroots__.append(webroot)

    def __handler_http_static__(self, httprequest):

        rpath = httprequest.path

        if self.__ctx__.TYGlobal.mode() == 1:  # 正式服务, 不允许使用py进程提供静态资源下载
            httprequest.setResponseCode(404, 'Not Found')
            self.doRequestFinish('', {}, rpath, False)
            return

        fvalue = None
        for wpath in self.__path_webroots__:
            fpath = wpath + rpath
            fpath = os.path.abspath(fpath)
            if fpath.find(wpath) == 0 and os.path.isfile(fpath):
                fvalue = self.__load_resource__(fpath)
                if fvalue != None:
                    break

        if fvalue == None:
            httprequest.setResponseCode(404, 'Not Found')
            self.doRequestFinish('', {}, rpath, False)
        elif httprequest.getHeader('If-Modified-Since') == fvalue[0]:
            httprequest.setResponseCode(304, 'Not Modified')
            self.doRequestFinish('', fvalue[2], rpath, False)
        elif httprequest.getHeader('If-None-Match') == fvalue[0]:
            httprequest.setResponseCode(304, 'Not Modified')
            self.doRequestFinish('', fvalue[2], rpath, False)
        else:
            self.doRequestFinish(fvalue[1], fvalue[2], rpath, False)

    def __load_resource__(self, fpath):
        fheads = None
        if fpath in self.__STATIC_POOL__:
            fvalue = self.__STATIC_POOL__[fpath]
        else:
            fvalue = ['', '', {}]
            self.__STATIC_POOL__[fpath] = fvalue

        filemt = os.path.getmtime(fpath)
        fdt = datetime.datetime.fromtimestamp(filemt)
        GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
        fkey = fdt.strftime(GMT_FORMAT)
        if fvalue[0] != fkey:
            self.__ctx__.ftlog.debug('load file->', fpath)
            ffile = file(fpath, 'r')
            fcontent = ffile.read()
            fvalue[0] = fkey
            fvalue[1] = fcontent

            fheads = {}
            fvalue[2] = fheads
            if fpath.endswith('.html') or fpath.endswith('.ty'):
                fheads['Content-Type'] = 'text/html;charset=UTF-8'
            elif fpath.endswith('.css'):
                fheads['Content-Type'] = 'text/css;charset=UTF-8'
            elif fpath.endswith('.js'):
                fheads['Content-Type'] = 'application/x-javascript;charset=UTF-8'
            elif fpath.endswith('.jpeg') or fpath.endswith('.jpg'):
                fheads['Content-Type'] = 'image/jpeg'
            elif fpath.endswith('.png'):
                fheads['Content-Type'] = 'image/png'
            elif fpath.endswith('.zip'):
                fheads['Content-Type'] = 'application/zip'
            elif fpath.endswith('.apk'):
                fheads['Content-Type'] = 'application/vnd.android.package-archive'

            fgmt = fkey
            fheads['Date'] = fgmt
            fheads['Etag'] = fgmt
            fheads['Last-Modified'] = fgmt

            fdt = fdt.replace(year=3000)
            fgmt = fdt.strftime(GMT_FORMAT)
            # fheads['Expires'] = fgmt
            # fheads['Cache-Control'] = 'max-age=99999999'
            fheads['Cache-Control'] = 'no-cache'
        return fvalue
