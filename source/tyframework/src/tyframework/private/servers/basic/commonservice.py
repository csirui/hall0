# -*- coding=utf-8 -*-

import base64
import json
import os
import sys
import time
from operator import isCallable

import datetime
import stackless
from twisted.internet import ssl, reactor
from twisted.internet.protocol import Factory

from tyframework.context import TyContext
from tyframework.private.servers.protocol.network.udpclient import InternalUDPClientProtocol, UDPClientProxy
from tyframework.protocol.server import _init_game_tasklets_
from tyframework.tasklet.basic import SimpleTasklet


class InitTasklet(SimpleTasklet):
    def __init__(self, clsServer):
        self.clsServer = clsServer
        self.gdata = clsServer.gdata
        self.canSendMainUdpMsg = True

    def tasklet(self):
        self.return_channel = TyContext.NWChannel()
        self.me = stackless.getcurrent()
        self.me._tyTasklet = self
        self.clsServer._startup_(self)


class CommonService:
    def __init__(self):
        pass

    def startup(self, gdata, tcpProtocol=None, udpProtocol=None, tcpProtocolZip=None, httpFactory=None):
        try:
            self.gdata = gdata
            self.tcpProtocol = tcpProtocol
            self.udpProtocol = udpProtocol
            self.tcpProtocolZip = tcpProtocolZip
            self.httpFactory = httpFactory
            self.udpProtocol.gdata = gdata

            TyContext.ftlog.info('service starup ...')
            if len(sys.argv) < 2:
                TyContext.ftlog.info("Usage: Server.py <PROCID>")
                exit()
            self.procid = sys.argv[1]
            datas = self.procid.split(':')
            self.rHost = datas[0]
            self.rPort = int(datas[1])
            self.rDbid = int(datas[2])
            self.logFile = datas[3] + '.log'
            datas = datas[3].split('-')

            if len(datas) == 4:  # TODO ZQH 老的启动模式,需删除, 需测试
                self.gameName = datas[1]
                self.gameId = int(datas[2])
                self.serverId = int(datas[3])
            else:
                self.gameName = datas[1]
                self.gameId = 9999
                self.serverId = int(datas[2])
            self.logoutpath = os.environ['PATH_LOG']
            self.webroot = os.environ['PATH_WEBROOT']

            workpath = os.environ['PYTHONPATH']
            workpath = workpath.split(':')[0]
            self.workpath = workpath

            TyContext.ftlog.info('InitParams workpath       =', self.workpath)
            TyContext.ftlog.info('InitParams webroot        =', self.webroot)
            TyContext.ftlog.info('InitParams logoutpath     =', self.logoutpath)
            TyContext.ftlog.info('InitParams log file       =', self.logFile)
            TyContext.ftlog.info('InitParams procid         =', self.procid)
            TyContext.ftlog.info('InitParams rHost          =', self.rHost)
            TyContext.ftlog.info('InitParams rPort          =', self.rPort)
            TyContext.ftlog.info('InitParams rDbid          =', self.rDbid)
            TyContext.ftlog.info('InitParams serverId       =', self.serverId)
            TyContext.ftlog.info('InitParams gdata          =', self.gdata)
            TyContext.ftlog.info('InitParams tcpProtocol    =', self.tcpProtocol)
            TyContext.ftlog.info('InitParams udpProtocol    =', self.udpProtocol)
            TyContext.ftlog.info('InitParams tcpProtocolZip =', self.tcpProtocolZip)

            TyContext.ftlog.info('InitTasklet startup ...')
            stackless.tasklet(reactor.run)()
            stackless.tasklet(InitTasklet(self).tasklet)()
            reactor.callLater(0, stackless.schedule)
            stackless.run()
        except:
            TyContext.ftlog.exception()

    def _startup_(self, tasklet):
        TyContext.ftlog.info('InitTasklet startup ...', tasklet)

        params = {
            'gdata': self.gdata,
            'serverId': self.serverId,
            'logFile': self.logFile,
            'redis.config': {'host': self.rHost, 'port': self.rPort, 'dbid': self.rDbid},
        }
        from tyframework import tycontext_init
        tycontext_init(params)

        self.gdata.service = self
        self.gdata.gameName = self.gameName
        self.gdata.gameId = self.gameId
        self.gdata.serverId = self.serverId
        self.gdata.workpath = self.workpath
        self.gdata.webroot = self.webroot
        self.gdata.logFile = self.logFile
        self.gdata.logoutpath = self.logoutpath
        self.gdata.next_heart_beat_interval = 1
        self.gdata.initData(tasklet, TyContext.RedisConfig.__db__.__redisPool__)
        self.gdata.initVarDatas(tasklet)

        mysrvdef = TyContext.TYGlobal.run_process()
        TyContext.ftlog.info('NETWORK Define : mysrvdef=', mysrvdef)

        tcport = mysrvdef.get('tcp', 0)
        sslport = mysrvdef.get('ssl', 0)
        httpport = mysrvdef.get('http', 0)
        udpport = mysrvdef.get('udp', 0)

        udpClient = self.creatSelfUDPClient(udpport)
        for sdef in TyContext.TYGlobal.all_process():
            sid = sdef['id']
            intrant1 = sdef['intrant']
            udpport1 = sdef['udp']
            proxy = UDPClientProxy(sid, intrant1, udpport1, udpClient)
            TyContext.ftlog.info('found udp target of :', sid, intrant1, udpport1)
            self.gdata.clientmap[sid] = proxy
        self.gdata.udpClient = udpClient

        gamefuns = self.__load_sub_game_init_funs__()
        gameids = []
        for gamefun in gamefuns:
            TyContext.ftlog.info('begin game ->', gamefun)
            typath = gamefun['typath']
            if typath == 'tygame':
                _init_game_tasklets_()
            gids = gamefun['tygame_init']()
            if isinstance(gids, list):
                gameids.extend(gids)
            TyContext.ftlog.info('end game ->', gamefun)

        if udpport > 0:
            self.listenUdp(udpport)
        if sslport > 0:  # SSL
            self.listenTcpSSL(sslport)
        if tcport > 0:  # ZIP
            if TyContext.TYGlobal.newtcpbridge():
                self.listenTcpBridge(tcport + 1000)
            self.listenTcpZIP(tcport)
        if httpport > 0:  # HTTP
            self.listenTcpHTTP(httpport)

        TyContext.ftlog.debug('====== onHeartBeat first begin======')
        self.onHeartBeat()
        TyContext.ftlog.debug('====== onHeartBeat first end======')

        mkey = 'script.' + str(self.rHost) + ':' + str(self.rPort) + ':' + str(self.rDbid)
        TyContext.RedisConfig.execute('HSET', mkey, self.procid, int(time.time()))
        try:
            self.report_online(gameids)
        except:
            TyContext.ftlog.exception()
        TyContext.ftlog.info('game service starup ... ok')
        TyContext.ftlog.info('*' * 40)

    def report_online(self, gameids):
        if TyContext.TYGlobal.is_control_process():
            #             if not TyContext.TYGlobal.newtcpbridge() :
            posturl = '%s/_game_server_online_?' % (TyContext.TYGlobal.http_sdk())
            datas = {'http_game': TyContext.TYGlobal.http_game(),
                     'conns': TyContext.TYGlobal.conn_ip_port_list(),
                     'mode': TyContext.TYGlobal.mode(),
                     'name': TyContext.TYGlobal.name(),
                     'time': int(time.time())
                     }
            TyContext.ftlog.info(posturl, datas)
            datas = base64.b64encode(json.dumps(datas))
            mo, posturl = TyContext.WebPage.webget_json(posturl, {'params': datas})
            TyContext.ftlog.info('_game_server_online_->', mo, posturl)
            #             else:
            #                 TyContext.ftlog.info('_game_server_online_-> bridge mode, not report !')

            #             datas = {
            #                 'tag' :-1,  # 由utils服务进行分配
            #                 'tcpsrv'  : TyContext.TYGlobal.conn_ip_port_list(),  # 游戏的长连接接入地址列表
            #                 'http' : TyContext.TYGlobal.http_game(),  # 使用的游戏的HTTP服务地址
            #                 'http.sdk' : TyContext.TYGlobal.http_sdk(),  # 使用的登录SDK服务地址
            #                 'mode' : TyContext.TYGlobal.mode(),  # 运行模式
            #             }
            #             TyContext.ftlog.debug('report_online->', datas)
            #             datas = base64.b64encode(json.dumps(datas))
            #             for x in xrange(len(gameids)) :
            #                 gameids[x] = str(gameids[x])
            #             gameids = ','.join(gameids)
            #             syncurl = TyContext.TYGlobal.http_global_api_server_online()
            #
            #             mo, syncurl = TyContext.WebPage.webget_json(syncurl, {'gameId':gameids, 'server' : datas})
            #             code = mo.get('result', {}).get('code', -1)
            #             if code == 200 :
            #                 TyContext.ftlog.debug('report_online->ok', gameids)
            #             else:
            #                 TyContext.ftlog.error('report_online->ERROR', code, gameids)

    def __load_sub_game_init_funs__(self):
        gamefuns = []
        binpath = TyContext.TYGlobal.path_bin()
        subdirs = os.listdir(binpath)
        for subdir in subdirs:
            if not os.path.isdir(binpath + '/' + subdir):
                continue
            if subdir[0] != '.' and not subdir in ('tyframework', ''):
                _game_pack_ = None
                try:
                    exec 'import %s as _game_pack_' % (subdir)
                except:
                    _game_pack_ = None
                if _game_pack_ != None:

                    initfun = getattr(_game_pack_, 'tygame_init', None)
                    if not isCallable(initfun):
                        initfun = None

                    startfun = getattr(_game_pack_, 'tygame_start', None)
                    if not isCallable(startfun):
                        startfun = None

                    if initfun != None:
                        gamefuns.append({'typath': subdir, 'tygame_init': initfun, 'tygame_start': startfun})
                        TyContext.ftlog.info('find game package of :', gamefuns[-1])
                    else:
                        TyContext.ftlog.info('find no game package of :', subdir)
                else:
                    TyContext.ftlog.info('find unknow 2 package of :', subdir)
        return gamefuns

    def listenTcpSSL(self, tcport):
        TyContext.ftlog.info('SOCKET listen TCP-SSL on port=', tcport, 'protocol=', self.tcpProtocol)
        self.tcpProtocol.gdata = self.gdata
        TyContext.ftlog.info('start TCP SSL at', tcport)
        factory = Factory()
        factory.protocol = self.tcpProtocol
        pathCertKey = self.workpath + '/cert/server.key'
        pathCertCrt = self.workpath + '/cert/server.crt'
        TyContext.ftlog.debug('pathCertKey==', pathCertKey)
        TyContext.ftlog.debug('pathCertCrt==', pathCertCrt)
        from OpenSSL import SSL
        reactor.listenSSL(tcport, factory, ssl.DefaultOpenSSLContextFactory(pathCertKey, pathCertCrt, SSL.SSLv3_METHOD))

    def listenTcpZIP(self, tcport):
        TyContext.ftlog.info('SOCKET listen TCP-ZIP on port=', tcport, 'protocol=', self.tcpProtocolZip)
        self.tcpProtocolZip.gdata = self.gdata
        TyContext.ftlog.info('start TCP ZIP at', tcport)
        factoryZip = Factory()
        factoryZip.protocol = self.tcpProtocolZip
        reactor.listenTCP(tcport, factoryZip)

    def listenTcpBridge(self, tcpport):
        from tyframework.protocol.server import ConnTCPSrvBridgeProtocol
        TyContext.ftlog.info('SOCKET listen TCP-BRIDGE on port=', tcpport, 'protocol=', ConnTCPSrvBridgeProtocol)
        ConnTCPSrvBridgeProtocol.gdata = self.gdata
        factoryZip = Factory()
        factoryZip.protocol = ConnTCPSrvBridgeProtocol
        reactor.listenTCP(tcpport, factoryZip)

    def listenTcpHTTP(self, tcport):
        TyContext.ftlog.info('SOCKET listen TCP-HTTP on port=', tcport, 'protocol=', self.httpFactory)
        reactor.listenTCP(tcport, self.httpFactory(self.gdata))

    def listenUdp(self, udpport):
        TyContext.ftlog.info('SOCKET listen UDP on port=', udpport, 'for recive')
        self.udpProtocol.gdata = self.gdata
        if udpport > 0:
            reactor.listenUDP(udpport, self.udpProtocol, maxPacketSize=65536)

    def creatSelfUDPClient(self, udpport):
        if udpport > 0:
            udpport = udpport + 1  # 当前进程监听的UDP为偶数，奇数即为发送端口
        else:
            udpport = 0  # 使用随机端口
        TyContext.ftlog.info('SOCKET listen UDP on port=', udpport, 'for send and query')
        udpClient = InternalUDPClientProtocol()
        reactor.listenUDP(udpport, udpClient, maxPacketSize=65536)
        return udpClient

    def onHeartBeat(self):
        try:
            t = datetime.datetime.now()
            if t.minute == 1 and t.second == 1:
                self.gdata.checkUserObjects(self.gdata)
        except:
            TyContext.ftlog.exception()

        try:
            if self.udpProtocol:
                mi = TyContext.MsgLine(0, [], '{"cmd":"server_heart_beat"}\n\0')
                tc = getattr(self.udpProtocol, 'makeTimerTasklet', None)
                if tc != None:
                    c = self.udpProtocol.makeTimerTasklet(self)
                else:
                    c = self.udpProtocol.makeTasklet(mi, None, None)
                stackless.tasklet(c.tasklet)()
                reactor.callLater(0, stackless.schedule)
            elif self.httpFactory:
                c = self.httpFactory.makeHeartBeatTasklet()
                if c:
                    stackless.tasklet(c.tasklet)()
                    reactor.callLater(0, stackless.schedule)
            else:
                TyContext.ftlog.error('ERROR, Can not creat heart beat tasklet !')
        except:
            TyContext.ftlog.exception('onHeartBeat')

    def scheduleHeartBeat(self, interval=0):
        interval = self.gdata.next_heart_beat_interval
        if interval < 0:
            interval = 0
        self.gdata.next_heart_beat_interval = 1
        reactor.callLater(interval, self.onHeartBeat)
