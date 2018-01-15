# -*- coding=utf-8 -*-

import urllib

from twisted.internet import defer, reactor
from twisted.internet.defer import succeed
from twisted.web.client import Agent, readBody
from twisted.web.http_headers import Headers
from twisted.web.iweb import IBodyProducer
from zope.interface import implements


class StringProducer(object):
    implements(IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


class RunHttpSdkProxy(object):
    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _init_singleton_(self):
        self.__ty_sdk_server_proxy__ = None

    #         self.__init_ty_sdk_server_proxy__()

    #     def __get_redis_info__(self, datas, redisdb):
    #         dbname = getattr(redisdb, 'dbname')
    #         if dbname :
    #             address = getattr(redisdb, 'address')
    #             datas[dbname] = address

    #     def __init_ty_sdk_server_proxy__(self):
    #         appId = self.__ctx__.TYGlobal.gameid()
    #         runmode = self.__ctx__.TYGlobal.mode()
    #         if runmode == self.__ctx__.TYGlobal.RUN_MODE_ONLINE \
    #             or runmode == self.__ctx__.TYGlobal.RUN_MODE_ONLINE_AUDIT \
    #             or appId == self.__ctx__.Const.SDK_GAMEID :  # 正式服,审核服, SDK不进行代理处理
    #             return
    #         datas = {}
    #         datas['mode'] = runmode
    #         datas['appId'] = appId
    #         datas['http.game'] = self.__ctx__.TYGlobal.http_game()
    #         datas['conn.list'] = self.__ctx__.TYGlobal.conn_ip_port_list()
    #         self.__get_redis_info__(datas, self.__ctx__.RedisUser)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisMix)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisAvatar)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisPayData)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisUserKeys)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisBiCount)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisOnline)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisOnlineGeo)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisFriendMix)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisLocker)
    #         self.__get_redis_info__(datas, self.__ctx__.RedisTableData)
    #
    #         # 旧形式代码, 需要整理 start
    #         datas['http.port'] = 65536
    #         datas['tcp.port.min'] = 65536
    #         datas['tcp.port.max'] = 0
    #
    #         for sdef in self.__ctx__.TYGlobal.all_process():
    #             internet = sdef['internet']
    #             tcport = sdef.get('tcp', 0)
    #             httpport = sdef.get('http', 0)
    #
    #             intrant = sdef['intrant']
    #             tcptype = sdef['type']
    #             if tcptype == 'conn' and tcport > 0:  # ZIP
    #                 datas['tcp.port.min'] = min(tcport, datas['tcp.port.min'])
    #                 datas['tcp.port.max'] = max(tcport, datas['tcp.port.max'])
    #             elif tcptype == 'http' and 'http.port' in datas and httpport > 0 :  # HTTP
    #                 datas['http.port'] = min(httpport, datas['http.port'])
    #             else:
    #                 continue
    #             if 'internet' in datas :
    #                 if datas['internet'] != internet :
    #                     raise Exception('the test service tcp internet address not same !', datas['internet'], internet)
    #             else:
    #                 datas['internet'] = internet
    #                 datas['intrant'] = intrant
    #         # 旧形式代码, 需要整理 done
    #
    #         self.__ctx__.ftlog.debug('__ty_sdk_server_proxy__==', datas)
    #         self.__ty_sdk_server_proxy__ = datas

    def _handler_http_sdk_proxy_(self, httprequest):
        return False

    #         if not self.__ty_sdk_server_proxy__ :
    #             return False
    #
    #         rpath = httprequest.path
    #         if rpath.find('/open/') >= 0 \
    #             or rpath.find('/head/') >= 0 \
    #             or rpath.find('/v1/pay/') >= 0 :
    #
    #             self.__do_sdk_proxy__(rpath)
    #             self.doRequestFinish('', {}, rpath)

    #             if content == None or len(content) == 0 :
    #                 content = 'sdk proxy return error !!'
    #
    #             if content[0] == '{' :
    #                 contentype = {'Content-Type':'application/json;charset=UTF-8'}
    #             elif rpath.endswith('.png') :
    #                 contentype = {'Content-Type': 'image/png'}
    #             elif rpath.endswith('.jpg') or rpath.endswith('.jpeg'):
    #                 contentype = {'Content-Type': 'image/jpeg'}
    #             else:
    #                 contentype = {'Content-Type': 'text/html;charset=UTF-8'}
    #
    #             self.doRequestFinish(content, contentype, rpath)
    #             return True
    #         return False

    #     def __do_sdk_proxy__(self, rpath):
    #
    #         datas = self.convertArgsToDict()
    #         if 'authInfo' in datas :
    #             datas['authInfo'] = datas['authInfo'].replace(' ', '')
    #
    #         appId = self.getRequestParamInt('appId')
    #         if appId <= 0 :
    #             appId = self.getRequestParamInt('gameId')
    #             if appId <= 0 :
    #                 appId = self.getRequestParamInt('gameid')
    #                 if appId <= 0 :
    #                     appId = self.getRequestParamInt('appid')
    #                     if appId <= 0 :
    #                         appId = self.__ctx__.TYGlobal.gameid()
    #         self.__ty_sdk_server_proxy__['appId'] = appId
    # #         datas['_ty_test_server_'] = base64.b64encode(json.dumps(self.__ty_sdk_server_proxy__))
    #
    #         httpurl = self.__ctx__.TYGlobal.http_sdk() + rpath
    #         self.__ctx__.ftlog.debug('__do_sdk_proxy__ ', httpurl, datas)
    # #         response, httpurl = self.__ctx__.WebPage.webget(httpurl, [], None, datas)
    # #         self.__ctx__.ftlog.debug('__do_sdk_proxy__ ', httpurl, response)
    #
    #         return self.doHttpProxy(httpurl, datas)

    def doHttpProxy(self, httpurl, datas):
        myctx = self.__ctx__
        myctx.ftlog.debug('Proxy start', httpurl)
        postdata_ = urllib.urlencode(datas)
        body = StringProducer(postdata_)
        agent = Agent(reactor)
        d = agent.request(
            'POST', httpurl,
            Headers(
                {'User-Agent': ['Twisted Web Client Proxy'], 'Content-type': ['application/x-www-form-urlencoded']}),
            body)

        request = myctx.RunHttp.get_request()
        resultDeferred = defer.Deferred()

        def cbProxyBody(responsebody):
            myctx.ftlog.debug('Proxy response', httpurl, 'body=[', repr(responsebody), ']')
            try:
                request.write(responsebody)
            except:
                myctx.ftlog.exception('cbProxyBody', httpurl)
            try:
                resultDeferred.callback('')
            except:
                myctx.ftlog.exception('cbProxyBody', httpurl)

        def cbProxyRequest(response):
            myctx.ftlog.debug('Proxy response', httpurl, 'code=', response.code)
            try:
                request.setResponseCode(response.code)
                for k, v in response.headers.getAllRawHeaders():
                    myctx.ftlog.debug('Proxy response', httpurl, 'head->', k, '=', v)
                    if isinstance(v, (list, tuple)):
                        for vv in v:
                            request.setHeader(k, vv)
                    else:
                        request.setHeader(k, v)
            except:
                myctx.ftlog.exception('cbProxyRequest', httpurl)
            dd = readBody(response)
            dd.addCallback(cbProxyBody)
            return dd

        d.addCallback(cbProxyRequest)
        tasklet = myctx.getTasklet()
        tasklet._report_wait_prep_(httpurl)
        tasklet._wait_for_deferred_(resultDeferred, httpurl[:60])
        myctx.ftlog.debug('Proxy done', httpurl)
        return ''
