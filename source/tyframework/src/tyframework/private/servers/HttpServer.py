# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月13日 星期五 15时06分10秒
# FileName:      HttpServer.py
# Class:         LogRequestHandler, LogHttp, LogHttpFactory
from basic.commonservice import CommonService
from basic.globaldata import GlobalData
from protocol.httpserver import LogHttpFactory
from tyframework.protocol.server import HttpUdpSvrProtocol


# Main entry...
def main():
    gdata = GlobalData()

    gs = CommonService()
    gs.startup(gdata, httpFactory=LogHttpFactory, udpProtocol=HttpUdpSvrProtocol())


# Execute Main ...
if __name__ == '__main__':
    main()
