# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月08日 星期日 14时46分54秒
# FileName:      common.py
# Class:         BasicTasklet

import random
import time

import stackless
import types
from twisted.internet import defer, reactor
from twisted.python import failure
from twisted.web import client

from tyframework.context import TyContext
from tyframework.tasklet.hotcmdhandler import HotCmdHandler

ASSERT_USER_KEYS = set(['chip', 'coupon', 'exp', 'charm'])

G_TASKLET_TIMES = {'__stime__': time.time()}
G_TASKLET_WAITS = {'__stime__': time.time()}
# G_TASKLET_STEPS = {}
G_TASKLET_COUNT = 0


def _report_tasklet_exec_start_(tasklet):
    global G_TASKLET_COUNT
    G_TASKLET_COUNT += 1
    setattr(tasklet, 'start_time__', time.time())


def _report_tasklet_exec_time(tasklet):
    global G_TASKLET_TIMES, G_TASKLET_WAITS, G_TASKLET_COUNT
    G_TASKLET_COUNT -= 1
    try:
        ct = time.time()
        wcount = getattr(tasklet, '_wait_count_', None)
        stime = getattr(tasklet, 'start_time__', None)
        if stime != None and wcount != None:
            utime = int((ct - stime) * 10)
            cmd = None
            try:
                msg = getattr(tasklet, 'msg', None)
                if msg:
                    cmd = msg.getCmd() + '.' + msg.getParamStr('action')

                if cmd == None:
                    msgline = getattr(tasklet, 'msgline', None)
                    if msgline:
                        cmd = msgline.cmd

                if cmd == None:
                    if getattr(tasklet, '_match', None) != None:
                        cmd = 'FlowingProcessTasklet'

                if cmd == None:
                    request = getattr(tasklet, 'request', None)
                    if request != None:
                        cmd = request.path

                if cmd == None:
                    cmd = 'unknow'
            except:
                cmd = '_exception_'

            if not cmd in G_TASKLET_TIMES:
                G_TASKLET_TIMES[cmd] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                G_TASKLET_WAITS[cmd] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            #                 G_TASKLET_STEPS[cmd] = []

            if utime < 1:
                utime = 0
            elif utime >= 1 and utime < 3:
                utime = 1
            elif utime >= 3 and utime < 7:
                utime = 2
            elif utime >= 7 and utime < 15:
                utime = 3
            elif utime >= 15 and utime < 31:
                utime = 4
            elif utime >= 31 and utime < 63:
                utime = 5
            elif utime >= 63 and utime < 127:
                utime = 6
            elif utime >= 127 and utime < 255:
                utime = 7
            elif utime >= 255 and utime < 511:
                utime = 8
            else:
                utime = 9

            if wcount < 1:
                wcount = 0
            elif wcount >= 1 and wcount < 3:
                wcount = 1
            elif wcount >= 3 and wcount < 7:
                wcount = 2
            elif wcount >= 7 and wcount < 15:
                wcount = 3
            elif wcount >= 15 and wcount < 31:
                wcount = 4
            elif wcount >= 31 and wcount < 63:
                wcount = 5
            elif wcount >= 63 and wcount < 127:
                wcount = 6
            elif wcount >= 127 and wcount < 255:
                wcount = 7
            elif wcount >= 255 and wcount < 511:
                wcount = 8
            else:
                wcount = 9

            G_TASKLET_TIMES[cmd][utime] += 1
            G_TASKLET_WAITS[cmd][wcount] += 1

        #             if utime >= 4 :
        #                 G_TASKLET_STEPS[cmd].append(getattr(tasklet, '_wait_list_', None))

        if ct - G_TASKLET_TIMES['__stime__'] > 10:
            G_TASKLET_TIMES['__etime__'] = ct
            runcount = stackless.getruncount()
            TyContext.ftlog.info('report_tasklet_exec_time', 'G_TASKLET_COUNT=', G_TASKLET_COUNT,
                                 'runcount=', runcount, G_TASKLET_TIMES)
            G_TASKLET_TIMES = {'__stime__': time.time()}

            #             for k, v in G_TASKLET_STEPS.items() :
            #                 for i in v :
            #                     TyContext.ftlog.info('report_tasklet_steps', k, i)
            #             G_TASKLET_STEPS = {}

            G_TASKLET_WAITS['__etime__'] = ct
            TyContext.ftlog.info('report_tasklet_wait_time', G_TASKLET_WAITS)
            G_TASKLET_WAITS = {'__stime__': time.time()}
    except:
        TyContext.ftlog.exception()


class SimpleTasklet():
    def tasklet(self):
        _report_tasklet_exec_start_(self)
        self.return_channel = TyContext.NWChannel()
        self.me = stackless.getcurrent()
        self.me._tyTasklet = self
        try:
            self.handle()
        except:
            TyContext.ftlog.exception()
        self.canSendMainUdpMsg = True
        _report_tasklet_exec_time(self)

    def __report_wait_init__(self, tips):
        if getattr(self, 'start_time__', None) == None:
            return False
        c1 = getattr(self, '_wait_count_', None)
        if c1 == None:
            setattr(self, '_wait_count_', 0)

        c1 = getattr(self, '_wait_list_', None)
        if c1 == None:
            setattr(self, '_wait_list_', [])

        return True

    def _report_wait_prep_(self, tips):
        try:
            if self.__report_wait_init__(tips):
                self._wait_count_ += 1
                t = int((time.time() - self.start_time__) * 1000)
                self._wait_list_.append([tips, t])
        except:
            TyContext.ftlog.exception()

    def _report_wait_in_(self, tips):
        try:
            if self.__report_wait_init__(tips):
                i = self._wait_count_ - 1
                witem = self._wait_list_[i]
                witem.append(int((time.time() - self.start_time__) * 1000))
        except:
            TyContext.ftlog.exception()

    def _report_wait_out_(self, tips):
        try:
            if self.__report_wait_init__(tips):
                i = self._wait_count_ - 1
                witem = self._wait_list_[i]
                witem.append(int((time.time() - self.start_time__) * 1000))
                runcount = stackless.getruncount()
                witem.append(str(runcount))
        except:
            TyContext.ftlog.exception()

    def _sleep_(self, timeout):
        d = defer.Deferred()
        reactor.callLater(timeout, d.callback, '')
        self._wait_for_deferred_(d, 'tasklet_sleep')

    def _wait_for_deferred_(self, d, tips):
        self._report_wait_in_(tips)
        try:
            #             if TyContext.TYGlobal.mode() > 2 :
            #                 self._wait_time_out_ = reactor.callLater(2, self.__timeout_deferred__, 1, d, tips)
            d.addCallback(self.__successful_deferred__)
            d.addErrback(self.__error_deferred__)
            return self.return_channel.receive()
        except Exception, e:
            TyContext.ftlog.exception(tips, e)
            raise e
        finally:
            self._report_wait_out_(tips)

    def __timeout_deferred__(self, tag, d, tips):
        if tag:
            if self._wait_time_out_ != None:
                self._wait_time_out_ = None
                if not d.called:
                    TyContext.ftlog.error('__timeout_deferred__ timeout-->', tag, tips, d)
                    d.errback(failure.Failure(TyContext.TimeoutException(str(tips))))
        else:
            try:
                to = getattr(self, '_wait_time_out_', None)
                if to:
                    self._wait_time_out_ = None
                    to.cancel()
            except:
                TyContext.ftlog.exception('Error !! cancel __timeout_deferred__')

    def __successful_deferred__(self, resmsg):
        try:
            self.__timeout_deferred__(0, None, '')
            self.return_channel.send_nowait(resmsg)
        except:
            TyContext.ftlog.exception('__successful_deferred__', str(resmsg))
            ex = Exception('__successful_deferred__ERROR')
            self.return_channel.send_exception_nowait(Exception, ex)

        if stackless.getcurrent() != self.me:
            stackless.schedule()

    def __error_deferred__(self, fault):
        try:
            self.__timeout_deferred__(0, None, '')
            self.return_channel.send_exception_nowait(fault.type, fault.value)
        except:
            TyContext.ftlog.exception('__error_deferred__', type(fault), str(fault))
            ex = Exception('__error_deferred__ERROR')
            self.return_channel.send_exception_nowait(Exception, ex)

        if stackless.getcurrent() != self.me:
            stackless.schedule()

    def sendToLedServer(self, gameId, ledmsg):
        mo = TyContext.MsgPack()
        mo.setCmd('send_led')
        mo.setParam('msg', ledmsg)
        mo.setParam('gameId', gameId)
        self.sendToLedServer2(0, mo)

    def sendToLedServer2(self, userId, msg):
        cmdServerIds = self.gdata.map_type_servers[6]
        mt = type(msg)
        if mt == types.StringType or mt == types.UnicodeType:
            pass
        else:
            msg = msg.pack()

        if userId > 0:
            index = userId % len(cmdServerIds)
            serverId = cmdServerIds[index]
            mainClient = self.gdata.clientmap[serverId]
            mainClient.sendMessage2(userId, msg)
        else:
            for index in xrange(len(cmdServerIds)):
                serverId = cmdServerIds[index]
                mainClient = self.gdata.clientmap[serverId]
                mainClient.sendMessage2(userId, msg)

    # 发送一个消息到TCP链接管理服务器， trgetUserId 为必须参数，可以使数字也可以是一个数字列表
    def sendUdpToMainServer(self, mo, trgetUserId, serverId=11):
        if self.canSendMainUdpMsg:
            targets = None
            if (type(trgetUserId) == int and trgetUserId >= 0):
                targets = [trgetUserId]
            elif len(trgetUserId) > 0:
                targets = trgetUserId
            if targets != None:
                mt = type(mo)
                msg = mo
                if mt == types.StringType or mt == types.UnicodeType:
                    pass
                else:
                    msg = mo.pack()
                if serverId == 11:
                    for uid in targets:
                        if uid > 10000:
                            sids = TyContext.TYGlobal.conn_server_ids()
                            subserverid = sids[uid % len(sids)]
                        else:
                            subserverid = 10
                        mainClient = self.gdata.clientmap[subserverid]
                        mainClient.sendMessage2([uid], msg)
                else:
                    mainClient = self.gdata.clientmap[serverId]
                    mainClient.sendMessage2(targets, msg)
            else:
                TyContext.ftlog.debug('sendUdpToMainServer no target input !!')
        else:
            TyContext.ftlog.debug('sendUdpToMainServer is forbidden !!')

    # 发送一个消息到TCP链接管理服务器， trgetUserId 为必须参数，可以使数字也可以是一个数字列表
    def sendUdpToMainServerOldSsl(self, mo, trgetUserId, serverId=10):
        if self.canSendMainUdpMsg:
            targets = None
            if (type(trgetUserId) == int and trgetUserId >= 0):
                targets = [trgetUserId]
            elif len(trgetUserId) > 0:
                targets = trgetUserId
            if targets != None:
                mainClient = self.gdata.clientmap[serverId]
                mt = type(mo)
                if mt == types.StringType or mt == types.UnicodeType:
                    mainClient.sendMessage2(targets, mo)
                else:
                    mainClient.sendMessage2(targets, mo.pack())
            else:
                TyContext.ftlog.debug('sendUdpToMainServer no target input !!')
        else:
            TyContext.ftlog.debug('sendUdpToMainServer is forbidden !!')

    # 发送一个消息到TCP链接管理服务器， trgetUserId 为必须参数，可以使数字也可以是一个数字列表
    def sendUdpToServerType(self, mo, trgetUserId, serverType):
        targets = None
        if (type(trgetUserId) == int and trgetUserId >= 0):
            targets = [trgetUserId]
        elif len(trgetUserId) > 0:
            targets = trgetUserId
        if targets == None:
            return

        cmdServerIds = self.gdata.map_type_servers[serverType]
        mt = type(mo)
        if mt == types.StringType or mt == types.UnicodeType:
            pass
        else:
            mo = mo.pack()
        for x in xrange(len(targets)):
            userId = targets[x]
            index = userId % len(cmdServerIds)
            serverId = cmdServerIds[index]
            mainClient = self.gdata.clientmap[serverId]
            mainClient.sendMessage2(targets, mo)

    # Internal udp request...
    def waitForUDPClient(self, client, reqmsg, userids=None):
        try:
            addr = getattr(client, 'toaddress')
            if addr:
                tips = 'waitForUDPClient-' + repr(addr)
            else:
                host = getattr(client, 'host')
                if host:
                    tips = 'waitForUDPClient-' + repr(host) + ':' + getattr(client, 'port', 0)
                else:
                    tips = 'waitForUDPClient-?'
        except:
            tips = 'waitForUDPClient-errtips'

        self._report_wait_prep_(tips)
        d = client.query(reqmsg, 30, userids)
        return self._wait_for_deferred_(d, tips)

    def __get_redis_conn_old__(self, cmd, key):
        redis_conn = None
        # user:10001
        # gamedata:6:10001
        # day1st:6:10001
        # item:6:10001
        # medal:6:10001
        # coupon:6:10001
        # match:6:10001
        # message:g6u10001

        # 如果是初始化的configitems，直接从redis_pool中获取，在麻将服务中，配置
        # 库与mixer库是分离的
        if key.find('configitems') >= 0:
            return self.gdata.redis_pool

        gdata = self.gdata
        if gdata.redis_cluster_len == 0:
            return gdata.redis_pool

        try:
            userId = 0
            datas = key.split(':')
            dlen = len(datas)
            if dlen > 1:
                head = datas[0]
                if dlen == 2 and head == 'user':
                    userId = int(datas[1])
                elif dlen == 3 and head in {'gamedata': 0, 'day1st': 0, 'item': 0,
                                            'medal': 0, 'coupon': 0, 'match': 0,
                                            'medal2': 0, 'day1st4': 0, 'month1st': 0,
                                            'week1st': 0, 'friend': 0}:
                    userId = int(datas[2])
                elif head == 'message' or head == 'gifts':
                    udatas = datas[1].split('u')
                    if len(udatas) == 2:
                        userId = int(udatas[1])
            redis_conn = None
            modid = -1
            if userId == 0:
                # 100指向mixer库
                if 100 in gdata.redis_cluster:
                    redis_conn = gdata.redis_cluster[100]
                else:
                    redis_conn = gdata.redis_pool
            else:
                modid = userId % gdata.redis_cluster_len
                redis_conn = gdata.redis_cluster[modid]
            return redis_conn
        except Exception, e:
            TyContext.ftlog.exception()
            TyContext.ftlog.error('ERROR __get_redis_conn__cmd=' + cmd + ' key=' + key, e)

        return gdata.redis_pool

    def __get_redis_conn_new__(self, cmd, key):
        redis_conn = None
        # user:10001
        # gamedata:6:10001
        # day1st:6:10001
        # item:6:10001
        # medal:6:10001
        # coupon:6:10001
        # match:6:10001
        # message:g6u10001

        # 如果是初始化的configitems，直接从redis_pool中获取，在麻将服务中，配置
        # 库与mixer库是分离的
        if key.find('configitems') >= 0:
            return self.gdata.redis_pool_config__

        gdata = self.gdata
        if gdata.redis_cluster_len__ == 0:
            return gdata.redis_pool_mix__

        try:
            userId = 0
            datas = key.split(':')
            dlen = len(datas)
            if dlen > 1:
                head = datas[0]
                if dlen == 2 and head == 'user':
                    userId = int(datas[1])
                elif dlen == 3 and head in {'gamedata': 0, 'day1st': 0, 'item': 0,
                                            'medal': 0, 'coupon': 0, 'match': 0,
                                            'medal2': 0, 'day1st4': 0, 'month1st': 0,
                                            'week1st': 0, 'friend': 0}:
                    userId = int(datas[2])
                elif head == 'message' or head == 'gifts':
                    udatas = datas[1].split('u')
                    if len(udatas) == 2:
                        userId = int(udatas[1])
            redis_conn = None
            modid = -1
            if userId == 0:
                redis_conn = gdata.redis_pool_mix__
            else:
                modid = userId % gdata.redis_cluster_len__
                redis_conn = gdata.redis_cluster__[modid]
            return redis_conn
        except Exception, e:
            TyContext.ftlog.exception()
            TyContext.ftlog.error('ERROR __get_redis_conn__cmd=' + cmd + ' key=' + key, e)

        return gdata.redis_pool_mix__

    def __get_redis_conn__(self, *cmds):
        if getattr(self.gdata, 'redis_pool_config__', None) != None:
            redis_conn = self.__get_redis_conn_new__(cmds[0], cmds[1])
        else:
            redis_conn = self.__get_redis_conn_old__(cmds[0], cmds[1])
        return redis_conn

    def __assert_for_data_hall_mode__(self, cmds):
        for cmd in cmds:
            if not isinstance(cmd, (int, str, unicode, float)):
                TyContext.ftlog.error('__assert_for_data_hall_mode__: cmd:', cmd, 'type(cmd):', type(cmd))
                assert (isinstance(cmd, (int, str, unicode, float)))

        cmdlen = len(cmds)
        if cmdlen > 2:
            mkey = cmds[1]
            if mkey.startswith('user:') or mkey.startswith('gamedata:'):
                for x in xrange(2, cmdlen):
                    if cmds[x] in ASSERT_USER_KEYS:
                        TyContext.ftlog.error('__assert_for_data_hall_mode__', cmds)
                        assert (cmds[x] not in ASSERT_USER_KEYS)

    # Redis single request...
    def waitForRedis(self, *cmds):
        # 只应该有mix和data cluster的操作进入次方法
        userId = 0
        try:
            cmd, key = cmds[0], cmds[1]
            datas = key.split(':')
            dlen = len(datas)
            if dlen > 1:
                head = datas[0]
                if dlen == 2 and head == 'user':
                    userId = int(datas[1])
                elif dlen == 3 and head in {'gamedata': 0, 'day1st': 0, 'item': 0,
                                            'medal': 0, 'coupon': 0, 'match': 0,
                                            'medal2': 0, 'day1st4': 0, 'month1st': 0,
                                            'week1st': 0, 'friend': 0}:
                    userId = int(datas[2])
                elif head == 'message' or head == 'gifts':
                    udatas = datas[1].split('u')
                    if len(udatas) == 2:
                        userId = int(udatas[1])
        except Exception, e:
            TyContext.ftlog.exception()
            TyContext.ftlog.error('ERROR __get_redis_conn__cmd=' + cmd + ' key=' + key, e)
            raise e

        self.__assert_for_data_hall_mode__(cmds)

        if userId <= 0:
            return TyContext.RedisMix.execute(*cmds)
        else:
            return TyContext.RedisUser.execute(userId, *cmds)

    # Redis single request...
    def waitForPage(self, deliveryUrl, postdata_='',
                    method_='POST',
                    headers_={'Content-type': 'application/x-www-form-urlencoded'},
                    timeout=6):
        try:
            tips = 'waitForPage' + repr(deliveryUrl[0:10])
        except:
            tips = 'waitForPage-errtips'
        self._report_wait_prep_(tips)
        if isinstance(deliveryUrl, unicode):
            deliveryUrl = deliveryUrl.encode('utf8')
        TyContext.ftlog.debug('waitForPage', deliveryUrl, method_, headers_, postdata_)
        if headers_ == None or len(headers_) == 0:
            headers_ = {'Content-type': 'application/x-www-form-urlencoded'}
        d = client.getPage(deliveryUrl, method=method_, headers=headers_, postdata=postdata_, timeout=timeout)
        if d:
            try:
                return self._wait_for_deferred_(d, tips)
            except Exception, e:
                TyContext.ftlog.exception()
                raise e
        else:
            return ""

    # Redis single request...
    def waitForMysql(self, mysqlconn, sqlStr):
        try:
            tips = 'waitForMysql' + repr(sqlStr[0:10])
        except:
            tips = 'waitForMysql-errtips'
        self._report_wait_prep_(tips)
        d = mysqlconn.runQuery(sqlStr)
        if d:
            try:
                return self._wait_for_deferred_(d, tips)
            except Exception, e:
                TyContext.ftlog.exception()
                raise e
        else:
            return ""

    def waitForRedisByConn(self, redis_conn, *cmds):
        self.__assert_for_data_hall_mode__(cmds)
        try:
            tips = 'waitForRedisByConn' + repr(cmds[0:3])
        except:
            tips = 'waitForRedisByConn-errtips'
        self._report_wait_prep_(tips)
        d = redis_conn.execute_command(*cmds, taskid=self.me._task_id)
        if d:
            try:
                return self._wait_for_deferred_(d, tips)
            except Exception, e:
                TyContext.ftlog.exception()
                raise e
        else:
            return ""

    def handle(self):
        pass

    def reset_heartbeat_interval(self, interval):
        if interval < self.gdata.next_heart_beat_interval:
            self.gdata.next_heart_beat_interval = interval


class BasicTasklet(SimpleTasklet):
    def tasklet(self):
        _report_tasklet_exec_start_(self)
        self.return_channel = TyContext.NWChannel()
        self.me = stackless.getcurrent()
        self.me._tyTasklet = self
        self.canSendMainUdpMsg = True
        if self.msgline == None:  # 仅仅在timer callback时进入此分支
            cmd = self.getMsg().getCmd()
        else:
            cmd = self.msgline.cmd
        if cmd == 'server_heart_beat':
            try:
                hc = self.gdata.heartCounter
                self.doServerHeartBeat(hc)
                self.__sync_globacl_datas__(hc)
                #                 TyContext.Configure.reload(hc, True) # 由热更新命令直接带动, 不再循环检查变化
                TyContext.DbMySql.keep_alive(hc)
                if hc > 31536000:  # 1年
                    self.gdata.heartCounter = 0
                else:
                    self.gdata.heartCounter = hc + 1
            except Exception, e:
                TyContext.ftlog.error('HANDLE_ERROR', self.msgline.dumpMsg())
                TyContext.ftlog.error('HANDLE_ERROR', e)
                TyContext.ftlog.exception()
            self.gdata.service.scheduleHeartBeat()

        elif cmd == HotCmdHandler.cmdname:
            HotCmdHandler.handel_msg(self, self.getMsg())

        elif len(cmd) > 0:
            try:
                #                 self.msg = self.getMsg()
                self.handle(cmd)
            except Exception, e:
                if self.msgline:
                    TyContext.ftlog.error('HANDLE_ERROR', self.msgline.dumpMsg())
                TyContext.ftlog.error('HANDLE_ERROR', e)
                TyContext.ftlog.exception()
        else:
            TyContext.ftlog.error('HANDLE_ERROR EMPTY CMD', self.msgline.dumpMsg())

        _report_tasklet_exec_time(self)

    def __sync_globacl_datas__(self, count):
        TyContext.TySync.sync_global_configure(count)

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def getMsg(self):
        if self.msg == None:
            self.msg = TyContext.MsgPack()
            self.msg.unpack(self.msgline.message)
        return self.msg

    def doParamError(self, cmd, uid, info):
        TyContext.ftlog.error('ERROR, doParamError->cmd=', cmd, 'uid=', uid, 'info=', info)
        if uid > 0:
            mo = TyContext.MsgPack()
            mo.setCmd(cmd)
            mo.setError(0, info)
            self.sendUdpToMainServer(mo, uid)

    def responseParamError(self, cmd, uid=-1, gid=-1, rid=-1, tid=-1, sid=-1, user=None, room=None, table=None):
        TyContext.ftlog.error('ERROR, ', cmd, ':params error! uid=', uid, 'gid=', gid, 'rid=', rid, 'tid=', tid, 'sid=',
                              sid, 'user=', user, 'room=', room, 'table=', table, 'msg==', self.msgline.dumpMsg())
        mo = TyContext.MsgPack()
        mo.setCmd(cmd)
        if gid != -1:
            mo.setResult('gameId', gid)
        if uid != -1:
            mo.setResult('userId', uid)
        if rid != -1:
            mo.setResult('roomId', rid)
        if tid != -1:
            mo.setResult('tableId', tid)
        if sid != -1:
            mo.setResult('seatId', sid)
        mo.setError(0, 'PARAMS ERROR')
        mo.setResult('ret', 'PARAMS ERROR')
        self.sendUdpToMainServer(mo, uid)
        pass

    def doServiceReady(self):
        rsid = self.getMsg().getParam('serverId')
        mo = TyContext.MsgPack()
        mo.setCmd('server_ready')
        mo.setParam('serverId', self.gdata.serverId)
        mo.setParam('targetServerId', rsid)
        self.sendUdpToMainServer(mo, 0)

    def onConfigerUpdate(self):
        # TyContext.ftlog.debug('Server onConfigerUpdate !!')
        pass

    def doServerHeartBeat(self, hc):
        TyContext.ftlog.debug('Server Heart Beat !!')
        pass

    def findUserById(self, userId, load=True):
        if userId in self.gdata.usermap:
            return self.gdata.usermap[userId]
        else:
            if userId > 0 and load:
                from freetime.entity.user import User
                user = User(userId, self)
                if user._stat >= 0:
                    # TyContext.ftlog.info('findUserById load user user into usermap', userId, len(self.gdata.usermap))
                    self.gdata.usermap[userId] = user
                    if user._stat == 0:
                        user.initdata(self)
                    return user
        return None

    def removeCacheUserById(self, userId):
        if userId in self.gdata.usermap:
            del self.gdata.usermap[userId]
            # TyContext.ftlog.info('removeCacheUserById del user user from usermap', userId, len(self.gdata.usermap))
        pass

    def handle(self, cmd):
        pass

    # --------------------------------------------------------------------------
    # 依据当前的消息命令和消息的roomId、gameId找到处理该消息的唯一的一个子服务ID
    # --------------------------------------------------------------------------
    def findServerIdByMsg_OLD(self, cmd, gameId=-1, roomId=-1):
        serverId = 0
        cmdServerIds = self.gdata.getServerIdByMsg(cmd)
        if not cmdServerIds:
            TyContext.ftlog.error('ERROR, the cmmand [', cmd, '] is illegal !!')
            return serverId

        if len(cmdServerIds) == 1:
            # 连接管理服务、账户服务、内容服务
            serverId = cmdServerIds[0]
        else:
            # 游戏服务
            if roomId == -1:
                roomId = self.msgline.getRoomId();
            if roomId >= 0:
                gameServerIds = self.gdata.getServerIdByRoomId(roomId)
                if gameServerIds:
                    if len(gameServerIds) == 1:
                        serverId = gameServerIds[0]
                    else:
                        TyContext.ftlog.error('ERROR, the room id [', roomId, '] has more the one servers ',
                                              gameServerIds, ' !')
                else:
                    TyContext.ftlog.error('ERROR, the room id [', roomId, '] has no servers !')
            else:
                if gameId == -1:
                    gameId = self.msgline.getGameId()
                if gameId >= 0:
                    gameServerIds = self.gdata.getServerIdByGameId(gameId)
                    if gameServerIds:
                        if len(gameServerIds) == 1:
                            serverId = gameServerIds[0]
                        else:
                            TyContext.ftlog.error('ERROR, the game id [', gameId, '] has more the one servers ',
                                                  gameServerIds, ' !')
                    else:
                        if gameId != 0:
                            TyContext.ftlog.error('ERROR, the game id [', gameId, '] has no servers !')
                else:
                    TyContext.ftlog.error('ERROR, the command [', cmd, '] have no roomId or gameId !')

            if serverId > 0 and not (serverId in cmdServerIds):
                serverId = 0
                TyContext.ftlog.error('ERROR, the serverId [', serverId, '] not in command maps !! cmd=', cmd,
                                      'gameId=', gameId, 'roomId=', roomId)

            #         if serverId == self.gdata.serverId :
            #             serverId = 0
            #             TyContext.ftlog.error('ERROR, the serverId [', serverId, '] can not be self serverId !! cmd=', cmd, 'gameId=', gameId, 'roomId=', roomId)

        if serverId > 0 and not self.gdata.clientmap.has_key(serverId):
            serverId = 0
            TyContext.ftlog.error('ERROR, the serverId [', serverId, '] is not in client maps !! cmd=', cmd, 'gameId=',
                                  gameId, 'roomId=', roomId)
        return serverId

    # --------------------------------------------------------------------------
    # 依据当前的消息命令和消息的roomId、gameId找到处理该消息的唯一的一个子服务ID
    # --------------------------------------------------------------------------
    def findServerIdByMsg(self, cmd, gameId=-1, roomId=-1):
        serverId = 0
        serverType = -1
        serverTypes = self.gdata.map_cmd_srvtypes
        if cmd in serverTypes:
            serverType = serverTypes[cmd][0]
        else:
            TyContext.ftlog.error('ERROR, the cmd [', cmd, '] not in server types !')
            return 0
        cmdServerIds = self.gdata.map_type_servers[serverType]

        if serverType == 4:
            # 游戏服务
            if roomId == -1:
                roomId = self.msgline.getRoomId();
            if gameId == -1:
                gameId = self.msgline.getGameId()
            if roomId >= 0:
                if gameId == 7:
                    serverId = self.__find_serverid_for_majiang(roomId, gameId)
                else:
                    roomId = self.__fix_roomId(gameId, roomId, self.msgline.getUserId())
                    TyContext.ftlog.debug('ConnTasklet->__fix_roomId end', gameId, roomId, self.msgline.getUserId())
                    gameServerIds = self.gdata.getServerIdByRoomId(roomId)
                    if gameServerIds:
                        if len(gameServerIds) == 1:
                            serverId = gameServerIds[0]
                        else:
                            TyContext.ftlog.error('ERROR, the room id [', roomId, '] has more the one servers ',
                                                  gameServerIds, ' !')
                    else:
                        TyContext.ftlog.error('ERROR, the room id [', roomId, '] has no servers !')
            else:
                if gameId == -1:
                    gameId = self.msgline.getGameId()
                if gameId >= 0:
                    gameServerIds = self.gdata.getServerIdByGameId(gameId)
                    if gameServerIds:
                        if len(gameServerIds) == 1:
                            serverId = gameServerIds[0]
                        else:
                            serverId = random.choice(gameServerIds)
                            # TyContext.ftlog.error('ERROR, the game id [', gameId, '] has more the one servers ', gameServerIds, ' !')
                    else:
                        if gameId != 0:
                            TyContext.ftlog.error('ERROR, the game id [', gameId, '] has no servers !')
                else:
                    TyContext.ftlog.error('ERROR, the command [', cmd, '] have no roomId or gameId !')
        else:
            if serverType == 2:  # acc服务,因为有多客户端使用同一个账号的BUG, 因此不能使用mod方式
                serverId = random.choice(cmdServerIds)
            else:
                userId = 0
                if self.msgline != None:
                    userId = self.msgline.getUserId()
                if userId > 0:
                    index = userId % len(cmdServerIds)
                    serverId = cmdServerIds[index]
                else:
                    TyContext.ftlog.error('ERROR, the command [', cmd, '] have no userId !')
                    serverId = random.choice(cmdServerIds)

        if serverId > 0 and not self.gdata.clientmap.has_key(serverId):
            TyContext.ftlog.error('ERROR, the serverId [', serverId, '] is not in client maps !! cmd=', cmd, 'gameId=',
                                  gameId, 'roomId=', roomId)
            serverId = 0
        return serverId

    def __fix_roomId(self, gameId, roomId, userId):
        TyContext.ftlog.debug('ConnTasklet->__fix_roomId begin', gameId, roomId, userId)
        if userId == 0:
            return roomId

        regroup = TyContext.Configure.get_game_item_json(gameId, 'regroup.rooms')
        if isinstance(regroup, list):
            for roomlist in regroup:
                if roomId in roomlist:
                    clientId = self.msgline.getClientId()
                    ver = TyContext.ClientUtils.getVersionFromClientId(clientId)
                    if ver >= 3.0: break

                    len_ = len(roomlist)
                    mod_ = userId % len_
                    new_roomId = roomlist[mod_]
                    if roomId == new_roomId:
                        break

                    if not self.__replace_roomId(new_roomId):
                        return roomId
                    else:
                        return new_roomId
        return roomId

    def __replace_roomId(self, roomId):
        TyContext.ftlog.debug('ConnTasklet->__replace_roomId begin', roomId, self.msgline.message)
        msg_ = self.msgline.message
        if isinstance(msg_, (str, unicode)):
            pos_ = msg_.find('''"roomId"''')
            if pos_ >= 0:
                end_pos_ = -1
                for i in xrange(pos_, len(msg_)):
                    if msg_[i] == ',' or msg_[i] == '}':
                        end_pos_ = i
                        break
                if end_pos_ > 0:
                    findstr = msg_[pos_:end_pos_]
                    repstr = '''"roomId":''' + str(roomId)
                    self.msgline.message = self.msgline.message.replace(findstr, repstr)
                    TyContext.ftlog.debug('ConnTasklet->__replace_roomId end', findstr, repstr, self.msgline.message)
                    return True
        return False

    def __find_serverid_for_majiang(self, roomId, gameId):
        """ 根据roomId找到匹配的serverId
        """
        if roomId > 10000:
            return roomId
        gameServerIds = self.gdata.getServerIdByRoomId(roomId)
        if gameServerIds:
            if len(gameServerIds) == 1:
                return gameServerIds[0]
            else:
                serverIds = self.__get_available_serverids(roomId, gameId,
                                                           gameServerIds)
                user_id = self.msgline.getUserId()
                if user_id == -1:
                    return serverIds[0]
                else:
                    return serverIds[user_id % len(serverIds)]
        TyContext.ftlog.error('not find server_id for roomId', roomId, 'gameId', gameId)
        return -1

    def __get_available_serverids(self, roomId, gameId, serverIds):
        """ 可以配置哪些serverId可用
        """
        open_serverids = TyContext.Configure.get_game_item_json(gameId, 'open_serverids',
                                                                None)
        ret = []
        if open_serverids:
            for sid in serverIds:
                if sid in open_serverids:
                    ret.append(sid)
        if len(ret) > 0:
            return ret
        return serverIds
