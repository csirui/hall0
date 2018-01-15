# -*- coding: utf-8 -*-
'''
Created on 2014年4月29日

@author: zjgzzz@126.com
'''
from twisted.internet.ssl import ClientContextFactory
from twisted.web import client

from tyframework.context import TyContext


def getResourcePath(fileName):
    '''
    取得当前文件下某一个资源的绝对路径
    '''
    import os
    cpath = os.path.abspath(__file__)
    cpath = os.path.dirname(cpath)
    fpath = cpath + os.path.sep + fileName
    return fpath


class WebClientContextFactory(ClientContextFactory):
    def __init__(self, cfile, kfile):
        self.cfile = cfile
        self.kfile = kfile

    def getContext(self):
        ctx = ClientContextFactory.getContext(self)
        ctx.use_certificate_file(self.cfile)
        ctx.use_privatekey_file(self.kfile)
        #         ctx.use_certificate_file('./apiclient_cert.pem')
        #         ctx.use_privatekey_file('./apiclient_key.pem')
        return ctx


def queryHttpSsl(httpsurl, postdata, certificate_file, privatekey_file):
    '''
    示例：
    certfile = sslhttp.getResourcePath('./cacert_weixin/apiclient_cert.pem')
    keyfile = sslhttp.getResourcePath('./cacert_weixin/apiclient_key.pem')
    httpsurl = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
    postdata = .....
    res = sslhttp.queryHttpSsl(httpsurl, postdata, certfile, keyfile)
    print res
    '''
    contextFactory = WebClientContextFactory(certificate_file, privatekey_file)
    headers_ = {'Content-type': 'application/x-www-form-urlencoded'}
    tasklet = TyContext.getTasklet()
    tasklet._report_wait_prep_(httpsurl)
    d = client.getPage(httpsurl, method="POST", headers=headers_, postdata=postdata, contextFactory=contextFactory)
    r = tasklet._wait_for_deferred_(d, httpsurl[:60])
    return r
