# -*- coding=utf-8 -*-

class RunHttpParams(object):
    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _init_singleton_(self):
        self.EXT_KEY_HTTP_REQUEST = '_run_http_request_'
        self.EXT_KEY_HTTP_REQUEST_BODY = '_run_http_request_body_'

    def is_current_http(self):
        exdatas = self.__ctx__.TYRun.get_tasklet_ext_datas()
        return self.EXT_KEY_HTTP_REQUEST in exdatas

    def get_request(self):
        exdatas = self.__ctx__.TYRun.get_tasklet_ext_datas()
        if self.EXT_KEY_HTTP_REQUEST in exdatas:
            return exdatas[self.EXT_KEY_HTTP_REQUEST]

    def getRequestParam(self, key, defaultVal=None):
        request = self.get_request()
        args = request.args
        if key in args:
            vals = args[key]
            return vals[0]
        return defaultVal

    def getRequestParamInt(self, key, defaultVal=0):
        val = self.getRequestParam(key, defaultVal)
        try:
            return int(val)
        except:
            pass
        return defaultVal

    def getRequestParamJs(self, jsons, key, defaultVal=''):
        val = self.getRequestParam(key, defaultVal)
        val = val.replace('\'', '"')
        val = val.decode('UTF-8')
        jsons[key] = val

    def convertToMsgPack(self, keys=None):
        request = self.get_request()
        args = request.args
        msg = self.__ctx__.Cls_MsgPack()
        if keys == None:
            keys = args.keys()
        for key in keys:
            if key in args:
                value = args[key][0]
            else:
                value = ''
            msg.setParam(key, value.strip())
        rpath = request.path.lower().replace('/', '_')
        msg.setCmd(rpath[1:])
        return msg

    def convertArgsToDict(self):
        request = self.get_request()
        args = request.args
        rparam = {}
        for k, v in args.items():
            rparam[k] = v[0].strip()
        return rparam

    def set_request_arg(self, key, val):
        request = self.get_request()
        request.args[key] = [val]

    def get_body_content(self):
        exdatas = self.__ctx__.TYRun.get_tasklet_ext_datas()
        body = exdatas.get(self.EXT_KEY_HTTP_REQUEST_BODY, None)
        if body == None:
            request = self.get_request()
            body = request.content.read().strip()
            exdatas[self.EXT_KEY_HTTP_REQUEST_BODY] = body
        return body

    #     def get_client_ip(self):
    #         # 先取nginx导向中的远程真实IP,取不到，取接入的TCP IP
    #         request = self.get_request()
    #         ip = request.getHeader('x-real-ip')
    #         if ip == None :
    #             ip = request.getClientIP()
    #         return ip

    def get_client_ip(self):
        request = self.__ctx__.RunHttp.get_request()
        ip = request.getHeader('x-forwarded-for')
        if not ip:
            ip = request.getHeader('x-real-ip')
            if not ip:
                ip = request.getClientIP()
        else:
            ips = ip.split(',')
            if len(ips) > 1:
                ip = ips[-2]
            else:
                ip = ips[-1]
            ip = ip.strip()
        self.__ctx__.ftlog.debug('get_client_ip', ip, '|', request.getClientIP(), '|', request.getHeader('x-real-ip'),
                                 '|', request.getHeader('x-forwarded-for'))
        return ip

    def get_request_header(self, headName):
        request = self.get_request()
        val = request.getHeader(headName)
        return val

    def get_request_path(self):
        request = self.get_request()
        return request.path

    def get_request_raw_data(self):
        r = self.get_request()
        if r:
            return ['HEADERS', r.getAllHeaders(),
                    'METHOD', r.method, 'URI', r.uri, 'CLIENTPROTO', r.clientproto,
                    'CONTENT', r.content.getvalue(), ]
        return []
