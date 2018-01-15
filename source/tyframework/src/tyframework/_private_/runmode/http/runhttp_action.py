# -*- coding=utf-8 -*-

class RunHttpAction(object):
    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _init_singleton_(self):
        pass

    def doRequestFinish(self, content, fheads, rpath, debugreturn=True):

        #         if content == 'redirected' :
        #             self.__ctx__.ftlog.debug('HTTPRESPONSE', rpath, 'redirected !!')
        #             return

        if debugreturn:
            debugcontent = content
            if len(debugcontent) > 128 and debugcontent[0] != '{':
                debugcontent = repr(debugcontent[0:128]) + '......'
            if self.TRACE_RESPONSE:
                self.__ctx__.ftlog.info('HTTPRESPONSE', rpath, debugcontent)
        else:
            if self.TRACE_RESPONSE:
                self.__ctx__.ftlog.info('HTTPRESPONSE', rpath)

        request = self.get_request()
        if getattr(request, 'finished', 0) == 1:
            self.__ctx__.ftlog.error('HTTPRESPONSE already finished !!', rpath)
            return

        try:
            for k, v in fheads.items():
                request.setHeader(k, v)
        except:
            self.__ctx__.ftlog.exception(rpath)

        try:
            request.write(content)
        except:
            try:
                request.write(content.encode('utf8'))
            except:
                self.__ctx__.ftlog.exception(rpath)

        try:
            request.channel.persistent = 0
        except:
            pass

        try:
            request.finish()
        except:
            if self.TRACE_RESPONSE:
                self.__ctx__.ftlog.exception(rpath)

        setattr(request, 'finished', 1)

    def redirect(self, redirectUrl):
        request = self.get_request()
        request.redirect(redirectUrl)
        self.doRequestFinish('', {}, '', False)
