# -*- coding=utf-8 -*-

import time

from tyframework.context import TyContext
from tyframework.private.servers.basic.config import Config


class GlobalData(Config):
    def __init__(self):
        Config.__init__(self)

    def initVarDatas(self, tasklet):
        # ReadWrite Data
        self.robotclientmap = {}  # kye=<ip:port> value=<UDP Client>
        self.clientmap = {}  # kye=<serverid> value=<UDP Client>
        self.usermap = {}  # key=<userId> value=<ConnUser|User>
        self.new_protocols = {}  # item=<ConnTCPSrvProtocol=ConnTCPSrvProtocol>
        self.maproom = {}  # key=<roomId> value=<Room>
        self.eventBus = TyContext.TYEventBus()
        self.initVarDatas2()
        self.heartCounter = 0

    def getServerClient(self, gameId, cmd):
        gsids = self.getServerIdByGameId(gameId)
        csids = self.getServerIdByMsg(cmd)
        sid = -1
        if gsids and csids:
            if len(gsids) == 1:
                if gsids[0] in csids:
                    sid = gsids[0]
            elif len(csids) == 1:
                if csids[0] in gsids:
                    sid = csids
        if sid in self.clientmap:
            return self.clientmap[sid]
        return None

    def initVarDatas2(self):
        pass

    @classmethod
    def getTaskletCount(self):
        return stackless.getruncount()

    @classmethod
    def checkUserObjects(cls, gdata):
        TyContext.ftlog.info('checkUserObjects-delete-count in')
        delusercount = 0
        if TyContext.TYGlobal.run_process_type() == TyContext.TYGlobal.RUN_TYPE_GAME:
            ct = int(time.time())
            usermap = gdata.usermap
            for uid in usermap.keys():
                user = usermap[uid]
                if ct - user._stat >= 3600:
                    del usermap[uid]
                    delusercount += 1
        TyContext.ftlog.info('checkUserObjects-delete-count->', delusercount)
        pass
