# -*- coding=utf-8 -*-

'''
Created on 2013-3-18

@author: Administrator
'''
from time import time

from datetime import datetime, timedelta

'''
quick start 服务器循环重试，scan->room enter->table enter->sit
room 加 对user级别的锁
table 加 对table的锁

enter的时候，如果为online对应的rid或tid或sid不为0，那么错误返回
                      如果为tableoffline，那么必须和offline的loc一致

在线状态：online offline tableoffline
connSrv--> 新链接   -> 如果是offline --> 转换为online，其他状态不进行处理
                -> 如果是online，状态错误
                -> 如果是tableoffline  --> gameSrv -> Sync sit -> 如果是online， 不做处理
                                                             -> 如果是tableoffline，转换为online
                                                             -> 如果是offline，状态错误
connSrv--> 掉线    -> gameSrv -> Sync roomLeave -> online -> 如果是play状态 -> 转换为tableoffline
                                                      -> 如果非play状态 -> 转换为offline
                                            -> offline -> 状态错误
                                            -> tableoffline -> 如果是play状态，不做处理
                                                            -> 如果非play状态 -> 转换为offline
gameSrv  --> readyTimeOut -> 如果是online，不做处理
                          -> 如果是offline，不做处理
                          -> 如果是tableoffline，转换为offline
'''

import sys


class OnLine(object):
    OFFLINE = 0
    ONLINE = 1
    TABLEOFFLINE = 2
    _debug = True
    _withCache = False

    REDISHEAD = None

    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def __execute_redis_cmd__(self, tasklet, cmd, userid, *params):
        if self.REDISHEAD == None:
            _fixhead_ = getattr(tasklet.gdata, 'redis_fixhead_', '')
            self.REDISHEAD = _fixhead_ + 'loc:'
        lockey = self.REDISHEAD + str(userid)
        if cmd == 'EXPIRE':
            self.__ctx__.RedisOnline.sendcmd(userid, 'EXPIRE', lockey, 172800)  # 1小时失效
        else:
            if self._withCache:
                ret = self.__excute_with_cache__(userid, cmd, lockey, *params)
            else:
                ret = self.__ctx__.RedisOnline.execute(userid, cmd, lockey, *params)
            if cmd == 'HSET' or cmd == 'HMSET' or cmd == 'HINCRBY':
                self.__ctx__.RedisOnline.sendcmd(userid, 'EXPIRE', lockey, 172800)  # 1小时失效
            return ret

    def __excute_with_cache__(self, userid, cmd, lockey, *params):
        '''添加了一层cache, 优化进入、离开房间时需要多次访问OnLine状态的问题
            cache 只在一个 tasklet 生命周期内生效, 不考虑被别的并行 tasklet 修改 redis 的情况
            不管是否加 cache 都无法处理这种问题，这种问题应该由别的逻辑保证避免出现。
        '''

        tasklet = self.__ctx__.getTasklet()
        if not hasattr(tasklet, 'onlineLocCache'):
            tasklet.onlineLocCache = {}
        if not userid in tasklet.onlineLocCache:
            tasklet.onlineLocCache[userid] = {}
            self.__ctx__.ftlog.debug('set onlineLocCache:', tasklet.onlineLocCache)

        from freetime.entity.game_common import utils
        if cmd == 'HSET' or cmd == 'HMSET':
            for k, v in utils.pairwise(params):
                if k == 'S' or k == 'L':
                    tasklet.onlineLocCache[userid][k] = v
                    self.__ctx__.ftlog.debug('set onlineLocCache:', tasklet.onlineLocCache)
            return self.__ctx__.RedisOnline.execute(userid, cmd, lockey, *params)
        elif cmd == 'HGET':
            k = params[0]
            if k in tasklet.onlineLocCache[userid]:
                self.__ctx__.ftlog.debug('get onlineLocCache:', k, tasklet.onlineLocCache)
                return tasklet.onlineLocCache[userid][k]
            else:
                ret = self.__ctx__.RedisOnline.execute(userid, cmd, lockey, *params)
                tasklet.onlineLocCache[userid][k] = ret
                self.__ctx__.ftlog.debug('set onlineLocCache:', tasklet.onlineLocCache, k, ret)
                return ret
        elif cmd == 'HMGET':
            results = {}
            _params = []  # 未被缓存的 onlineloc fields
            for k in params:
                if k in tasklet.onlineLocCache[userid]:
                    results[k] = tasklet.onlineLocCache[userid][k]
                    self.__ctx__.ftlog.debug('get onlineLocCache:', k, tasklet.onlineLocCache)
                else:
                    _params.append(k)
            if _params:
                ret = self.__ctx__.RedisOnline.execute(userid, cmd, lockey, *_params)
                for k, v in zip(_params, ret):
                    results[k] = v
                    if k == 'S' or k == 'L':
                        tasklet.onlineLocCache[userid][k] = v
                        self.__ctx__.ftlog.debug('set onlineLocCache:', tasklet.onlineLocCache, k, v)
            return map(results.get, params)
        else:
            return self.__ctx__.RedisOnline.execute(userid, cmd, lockey, *params)

    def isNeedReConn(self, obj):
        if obj._gid in [1, 3, 6, 8, 10, 18, 20]:
            return True
        return False

    def incOnLineMacthCount(self, tasklet, userId):
        count = self.__execute_redis_cmd__(tasklet, 'HINCRBY', userId, 'M', 1)
        return count

    def delOnLineMacthCount(self, tasklet, userId):
        count = self.__execute_redis_cmd__(tasklet, 'HDEL', userId, 'M')
        return count

    def getOnLineState(self, tasklet, userId):
        state = self.__execute_redis_cmd__(tasklet, 'HGET', userId, 'S')
        if state not in (OnLine.OFFLINE, OnLine.ONLINE, OnLine.TABLEOFFLINE):
            state = OnLine.OFFLINE
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.getOnLineState->userId=', userId, 'state=', state)
        return state

    def setOnLineState(self, tasklet, userId, oldState, newState):
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.setOnLineState->userId=', userId, 'oldState=', oldState, 'newState=',
                                     newState)
        if newState == OnLine.OFFLINE:
            self.__execute_redis_cmd__(tasklet, 'HDEL', userId, 'S')
            self.__ctx__.RedisUser.execute(userId, 'DEL', 'pt:%d' % (userId))
        else:
            self.__execute_redis_cmd__(tasklet, 'HSET', userId, 'S', newState)

    def getOnLineLoc(self, tasklet, userId):
        loc = self.__execute_redis_cmd__(tasklet, 'HGET', userId, 'L')
        if loc == None:
            loc = '0.0.0.0'
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.getOnLineLoc->userId=', userId, 'loc=', loc)
        locs = loc.split('.')
        return int(locs[0]), int(locs[1]), int(locs[2]), int(locs[3]),

    def setOnLineGameId(self, tasklet, userId, gameId):
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.setOnLineGameId->userId=', userId, 'gameId=', gameId)

        self.__execute_redis_cmd__(tasklet, 'HSET', userId, 'G', gameId)

    def getOnLineGameId(self, tasklet, userId):
        gameId = self.__execute_redis_cmd__(tasklet, 'HGET', userId, 'G')
        if gameId == None:
            self.__ctx__.ftlog.error('OnLine.getOnLineGameId->userId=', userId, 'gameId=', gameId)
            gameId = 9999
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.getOnLineGameId->userId=', userId, 'gameId=', gameId)
        return int(gameId)

    def getOnLineLocAndState(self, tasklet, userId):
        loc, state = self.__execute_redis_cmd__(tasklet, 'HMGET', userId, 'L', 'S')
        if loc == None:
            loc = '0.0.0.0'
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.getOnLineLocAndState->userId=', userId, 'loc=', loc, 'state=', state)
        if state not in (OnLine.OFFLINE, OnLine.ONLINE, OnLine.TABLEOFFLINE):
            state = OnLine.OFFLINE
        locs = loc.split('.')
        return int(locs[0]), int(locs[1]), int(locs[2]), int(locs[3]), state

    def setOnLineLoc(self, tasklet, userId, gid, rid, tid, sid):
        loc = str(gid) + '.' + str(rid) + '.' + str(tid) + '.' + str(sid)
        state = self.getOnLineState(tasklet, userId)
        if state != OnLine.ONLINE:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.setOnLineLoc error->userId=', userId, 'loc=', loc,
                                         'not online state ! not set loc !!')
            return False
        self.__ctx__.ftlog.info('OnLine.setOnLineLoc->userId=', userId, 'loc=', loc)
        self.__execute_redis_cmd__(tasklet, 'HSET', userId, 'L', loc)
        self._changePlayTime(tasklet, userId, gid, rid, tid)
        return True

    def setOnLineStateForce(self, tasklet, userId, isOnline, gid, rid, tid, sid):
        loc = str(gid) + '.' + str(rid) + '.' + str(tid) + '.' + str(sid)
        self.__ctx__.ftlog.info('OnLine.setOnLineStateForce->userId=', userId, 'loc=', loc, 'isOnline=', isOnline)
        if isOnline:
            state = OnLine.ONLINE
            self.__execute_redis_cmd__(tasklet, 'HMSET', userId, 'S', state, 'L', loc)
            self._changePlayTime(tasklet, userId, gid, rid, tid)
        else:
            self.__ctx__.RedisUser.execute(userId, 'DEL', 'pt:%d' % (userId))
            self.__execute_redis_cmd__(tasklet, 'DEL', userId)
            self._changePlayTime(tasklet, userId, 0, 0, 0)

    def setOnlineLocListForce(self, tasklet, gid, rid, tid, userSeatList):
        '''
        userSeatList = [(userId, seatId),...]
        '''
        for userSeat in userSeatList:
            loc = '%s.%s.%s.%s' % (gid, rid, tid, userSeat[1])
            self.__ctx__.ftlog.info('Online.setOnlineLocListForce->userId=', userSeat[0], 'loc=', loc)
            self.__execute_redis_cmd__(tasklet, 'HSET', userSeat[0], 'L', loc)
            self._changePlayTime(tasklet, userSeat[0], gid, rid, tid)

    def _changePlayTime(self, tasklet, userId, gid, rid, tid):
        try:
            _, rid1, tid1, _ = self.getOnLineLoc(tasklet, userId)
            if rid1 == rid and tid1 == tid:
                return
            subkey = 'hall0_time'
            ptkey = 'pt:%d' % (userId)
            if rid == 0 and tid == 0:
                # 清理loc, 增加时间
                st = self.__ctx__.RedisUser.execute(userId, 'HGET', ptkey, subkey)
                if isinstance(st, int):
                    dt = int(time()) - st
                    if dt > 10 and dt < 86400:  # 如何判定loc的时间变化是一个有效值? 桌子上最少待10秒, 最大不可能超过1天
                        # 增加游戏时间
                        self.incrPlayTime(userId, dt)
                    self.__ctx__.RedisUser.execute(userId, 'HDEL', ptkey, subkey)
                    self.__ctx__.RedisUser.execute(userId, 'EXPIRE', ptkey, 86400)
                pass
            else:
                # 设置loc, 重置时间
                self.__ctx__.RedisUser.execute(userId, 'HSET', ptkey, subkey, int(time()))
                self.__ctx__.RedisUser.execute(userId, 'EXPIRE', ptkey, 86400)
                pass
        except:
            self.__ctx__.ftlog.error()

    def incrPlayTime(self, userId, detalTime):
        self.__ctx__.RedisUser.execute(userId, 'HINCRBY', 'gamedata:9999:%d' % (userId), 'totaltime', detalTime)
        mkey = 'gamedata:9999:%d' % (userId)
        self.__ctx__.RedisUser.sendcmd(userId, 'HINCRBY', mkey, 'totaltime', detalTime)

        datas = self.__ctx__.RedisUser.execute(userId, 'HGET', mkey, 'todaytime')
        datas = self.__ctx__.strutil.loads(datas, ignoreException=True, execptionValue={})
        today = datetime.now().strftime('%Y%m%d')[-6:]
        if today in datas:
            datas[today] += detalTime
        else:
            datas[today] = detalTime

        oldday = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')[-6:]
        for k in datas.keys()[:]:
            if k < oldday:
                del datas[k]
        self.__ctx__.RedisUser.sendcmd(userId, 'HSET', mkey, 'todaytime', self.__ctx__.strutil.dumps(datas))

    def onHeartBeat(self, tasklet, userId):
        self.__execute_redis_cmd__(tasklet, 'EXPIRE', userId)

    def onConnected(self, tasklet, userId):
        gid, rid, tid, sid, state = self.getOnLineLocAndState(tasklet, userId)
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.onConnected->userId=', userId, 'state=', state, 'loc=', gid, rid, tid, sid)
        if state == OnLine.OFFLINE:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onConnected->userId=', userId, 'from offline to online !!!')
            self.setOnLineState(tasklet, userId, state, OnLine.ONLINE)
        #         elif state == OnLine.TABLEOFFLINE and gid == 8:
        #             if OnLine._debug :
        #                 self.__ctx__.ftlog.debug('OnLine.onConnected->userId=', userId, 'texas: from tableoffline to online !!!')
        #             self.setOnLineState(tasklet, userId, state, OnLine.ONLINE)
        elif state == OnLine.TABLEOFFLINE:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onConnected->userId=', userId, 'state=', state,
                                         'wait for game server update state !!')
        elif state == OnLine.ONLINE:
            self.__ctx__.ftlog.error('OnLine.onConnected->userId=', userId, 'state=', state,
                                     'the state is online error !!!')
        return gid, rid, tid, sid

    def onLostConnect(self, tasklet, userId):
        gid, rid, tid, sid, state = self.getOnLineLocAndState(tasklet, userId)
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.onLostConnect user=', userId, 'loc==', 'gid=', gid, 'rid=', rid, 'tid=',
                                     tid, 'sid=', sid)
        haveRoom = True
        if rid == 0 and tid == 0 and sid == 0:
            if state == OnLine.ONLINE:
                self.setOnLineState(tasklet, userId, state, OnLine.OFFLINE)
            elif state == OnLine.TABLEOFFLINE:
                self.setOnLineState(tasklet, userId, state, OnLine.OFFLINE)
                if OnLine._debug:
                    self.__ctx__.ftlog.debug('the user ', userId,
                                             'is already off line, but state is table offline error')
            else:
                if OnLine._debug:
                    self.__ctx__.ftlog.debug('the user ', userId, 'is already off line')
            haveRoom = False
        return gid, rid, tid, sid, haveRoom

    def onRoomEnter(self, tasklet, userId, room):
        gid, rid, tid, sid, state = self.getOnLineLocAndState(tasklet, userId)
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.onRoomEnter->userId=', userId, 'room.id=', room._id, 'state=', state,
                                     'gid=', gid, 'rid=', rid, 'tid=', tid, 'sid', sid)
        if self.isNeedReConn(room):
            if state == OnLine.OFFLINE:
                self.__ctx__.ftlog.error('OnLine.onRoomEnter->userId=', userId, 'state=', state,
                                         'the state is offline error !!!')
                return False
            elif state == OnLine.TABLEOFFLINE:
                if room._gid != gid or room._id != rid:
                    self.__ctx__.ftlog.error('OnLine.onRoomEnter->userId=', userId, 'enter not match !!! room._gid=', \
                                             room._gid, 'room._id=', room._id, 'gid=', gid, 'rid=', rid)
                    return False
                else:
                    if OnLine._debug:
                        self.__ctx__.ftlog.debug('OnLine.onRoomEnter->userId=', userId, 'enter match !!!')
            elif state == OnLine.ONLINE:
                if tid == 0 and sid == 0:
                    if OnLine._debug:
                        self.__ctx__.ftlog.debug('OnLine.onRoomEnter->userId=', userId, 'enter ok !!!')
                else:
                    self.__ctx__.ftlog.error('OnLine.onRoomEnter->userId=', userId, 'enter false !!! room._gid=', \
                                             room._gid, 'room._id=', room._id, 'gid=', gid, 'rid=', rid)
                    return False
        ret = self.setOnLineLoc(tasklet, userId, room._gid, room._id, 0, 0)
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.onRoomEnter done->userId=', userId)
        return ret

    '''
    v2 系列将废除TABLE OFFLINE状态， 玩家发起bind_user时设置为ONLINE
    '''

    _LEAVE_ROOM_REASON_ACTIVE = 0  # 玩家主动离开房间
    _LEAVE_ROOM_REASON_LOST_CONNECTION = 1  # 网络连接丢失被踢出房间
    _LEAVE_ROOM_REASON_TIMEOUT = 2  # 玩家操作超时被踢出房间
    _LEAVE_ROOM_REASON_SYSTEM = 3  # 系统把玩家踢出房间
    _LEAVE_ROOM_REASON_LESS_MIN = 4  # 玩家所持金币数 < 该房间准入最小金币数
    _LEAVE_ROOM_REASON_GREATER_MAX = 5  # 玩家所持金币数 > 该房间准入最大金币数

    def onRoomLeaveV2(self, userId, room, reason):
        '''
        @author:  Zhouhao
        
        Args:
            reason: 离开房间原因
        '''
        methodFullName = "<%s>[%s.%s]" % (room._gid, 'OnLine', sys._getframe().f_code.co_name)

        if OnLine._debug:
            self.__ctx__.ftlog.debug(methodFullName, '<< |userId, roomId, reason:', userId, room._id, reason)

        tasklet = self.__ctx__.getTasklet()
        gid, rid, tid, sid, state = self.getOnLineLocAndState(tasklet, userId)

        if reason == self._LEAVE_ROOM_REASON_LOST_CONNECTION:
            if OnLine._debug:
                self.__ctx__.ftlog.debug(methodFullName, 'lost connection! |userId=', userId, 'state=', state, 'gid=',
                                         gid, 'rid=', rid, 'tid=', tid, 'sid', sid)

            room = None
            rooms = tasklet.gdata.maproom
            if rid in rooms:
                room = rooms[rid]
            #                 if tid in room.maptable:
            #                     table = room.maptable[tid]

            if room == None:
                self.__ctx__.ftlog.error(methodFullName, 'the room is not found! |rid=', rid)
                return False

            if room._gid != gid:
                self.__ctx__.ftlog.error(methodFullName, 'the room game id and loc gid is not equal')
                return False

            if state == OnLine.OFFLINE:
                self.__ctx__.ftlog.error(methodFullName, 'already offline! |userId, tableId, sid:', userId, tid, sid)
            else:
                if tid > 0:
                    self.__ctx__.ftlog.info(methodFullName, 'keep user in table. |userId, tableId, sid:', userId, tid,
                                            sid)
                else:
                    self.__ctx__.ftlog.info(methodFullName, 'clear loc. |userId:', userId)
                    self.setOnLineLoc(tasklet, userId, 0, 0, 0, 0)

                self.setOnLineState(tasklet, userId, state, OnLine.OFFLINE)
                state = OnLine.OFFLINE

        else:
            if tid > 0:
                if OnLine._debug:
                    self.__ctx__.ftlog.error(methodFullName, 'tid>0, |userId, tid:', userId, tid)
                return False
            else:
                self.setOnLineLoc(tasklet, userId, 0, 0, 0, 0)

        if OnLine._debug:
            self.__ctx__.ftlog.debug(methodFullName, '>> |userId, roomId, reason:', userId, room._id, reason)

        return True

    def onRoomLeave(self, tasklet, userId, room, reason):
        if room._gid == 8 or room._gid == 15:
            return self.onRoomLeaveV2(userId, room, reason)

        self.onRoomLeaveV1(tasklet, userId, room, reason)
        return True

    # reason :
    # 1 -- 网络断线
    # playState :
    # 1 -- 在座位上，IDEL状态
    # 2 -- 在座位上，PLAY状态，需要短线重连
    # 3 -- 在旁观中
    # 4 -- 错误状态，即在旁观中，又在IDEL状态
    # 5 -- 错误状态，即在旁观中，又在PLAY状态
    def onRoomLeaveV1(self, tasklet, userId, room, reason):
        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.onRoomLeave in ->userId=', userId)
        gid, rid, tid, sid, state = self.getOnLineLocAndState(tasklet, userId)

        if reason == 1:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onRoomLeave->userId=', userId, 'state=', state, 'gid=', gid, 'rid=',
                                         rid, 'tid=', tid, 'sid', sid)

            room = None
            playState = 0
            rooms = tasklet.gdata.maproom
            if rid in rooms:
                room = rooms[rid]
                if tid in room.maptable:
                    table = room.maptable[tid]
                    playState = table.getUserState(userId)

            if room == None:
                if OnLine._debug:
                    self.__ctx__.ftlog.debug('OnLine.onRoomLeave->the room is not found !! rid=', rid)
                return

            if room._gid != gid:
                if OnLine._debug:
                    self.__ctx__.ftlog.debug('OnLine.onRoomLeave->the room game id and loc gid is not equal')
                return

            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onRoomLeave->playState=', playState)
            if state == OnLine.OFFLINE:
                self.__ctx__.ftlog.error('OnLine.onRoomLeave->the user is already offline !!')
            elif state == OnLine.ONLINE:
                if playState == 2:
                    if OnLine._debug:
                        self.__ctx__.ftlog.debug('OnLine.onRoomLeave->userId=', userId,
                                                 'from online to table offline !!!')
                    self.setOnLineState(tasklet, userId, state, OnLine.TABLEOFFLINE)
                    state = OnLine.TABLEOFFLINE
                else:
                    if OnLine._debug:
                        self.__ctx__.ftlog.debug('OnLine.onRoomLeave->userId=', userId, 'from online to offline !!!')
                    self.setOnLineLoc(tasklet, userId, 0, 0, 0, 0)
                    self.setOnLineState(tasklet, userId, state, OnLine.OFFLINE)
                    state = OnLine.OFFLINE
            elif state == OnLine.TABLEOFFLINE:
                if playState == 1 or playState == 5:
                    if OnLine._debug:
                        self.__ctx__.ftlog.debug('OnLine.onRoomLeave-> table offline, not change')
                else:
                    if OnLine._debug:
                        self.__ctx__.ftlog.debug('OnLine.onRoomLeave->userId=', userId,
                                                 'from table offline to offline !!!')
                    if gid == 7:
                        self.__execute_redis_cmd__(tasklet, 'HSET', userId, 'S', OnLine.OFFLINE)
                    else:
                        self.setOnLineState(tasklet, userId, state, OnLine.OFFLINE)
                    state = OnLine.OFFLINE

        if sid != 0 or tid != 0:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onRoomLeave error->userId=', userId, 'the sid or tid is not 0 !!')
            return

        if state == OnLine.ONLINE:
            self.setOnLineLoc(tasklet, userId, 0, 0, 0, 0)

        if OnLine._debug:
            self.__ctx__.ftlog.debug('OnLine.onRoomLeave done->userId=', userId)
        pass

    def onTableEnter(self, tasklet, userId, table):
        '''支持旁观断线重连
        @modifiedBy:  Zhouhao
        '''
        methodFullName = "<%s>[%s.%s]" % (table._gid, 'OnLine', sys._getframe().f_code.co_name)

        gid, rid, tid, sid, state = self.getOnLineLocAndState(tasklet, userId)

        if OnLine._debug:
            self.__ctx__.ftlog.debug(methodFullName, 'userId=', userId, 'table.id=', table._id, 'state=', state, 'gid=',
                                     gid, 'rid=', rid, 'tid=', tid, 'sid', sid)

        if state == OnLine.OFFLINE:
            self.__ctx__.ftlog.error(methodFullName, 'userId=', userId, 'state=', state,
                                     'the state is offline error !!!')
            return False

        if state == OnLine.TABLEOFFLINE:
            if not self.isNeedReConn(table):
                self.__ctx__.ftlog.error(methodFullName, 'table offline but not need reconn! |userId, tableId:', userId,
                                         table._id)
                return False

            if table._gid != gid or table._rid != rid or table._id != tid:
                self.__ctx__.ftlog.error(methodFullName, 'userId=', userId, 'enter not match !!! room._gid=', \
                                         table._gid, 'table._rid=', table._rid, 'table._id=', table._id, 'gid=', gid,
                                         'rid=', rid, 'tid=', tid)
                return False
            else:
                if OnLine._debug:
                    self.__ctx__.ftlog.debug(methodFullName, 'userId=', userId,
                                             'enter match， from table offline to online !!!')
                self.setOnLineState(tasklet, userId, state, OnLine.ONLINE)
                return True

        if state == OnLine.ONLINE:
            if gid == table._gid and rid == table._rid and (tid == table._id or tid == 0):
                if OnLine._debug:
                    self.__ctx__.ftlog.debug(methodFullName, 'userId=', userId, 'enter ok !!!')
                return self.setOnLineLoc(tasklet, userId, table._gid, table._rid, table._id, 0)
            else:
                self.__ctx__.ftlog.error(methodFullName, 'userId=', userId, 'enter error !!! room._gid=', \
                                         table._gid, 'table._rid=', table._rid, 'table._id=', table._id, 'gid=', gid,
                                         'rid=', rid, 'tid=', tid)
                return False

        self.__ctx__.ftlog.error(methodFullName, 'unknown state! |userId, state:', userId, state)
        return False

    def onTableLeave(self, tasklet, userId, table):
        gid, rid, _, sid, state = self.getOnLineLocAndState(tasklet, userId)
        if sid != 0:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onTableLeave error->userId=', userId, 'the sid is not 0 !!')
            return
        if state != OnLine.ONLINE:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onTableLeave->userId=', userId, 'not online state ! not set loc !!')
            return
        self.setOnLineLoc(tasklet, userId, gid, rid, 0, 0)
        pass

    def onObserv(self, tasklet, userId, table):
        '''支持旁观断线重连
        @author:  zhouhao
        '''
        methodFullName = "<%s>[%s.%s]" % (table.gameId, 'OnLine', sys._getframe().f_code.co_name)
        if self.isNeedReConn(table):
            gid, rid, tid, sid, state = self.getOnLineLocAndState(tasklet, userId)

            if OnLine._debug:
                self.__ctx__.ftlog.debug(methodFullName, '|userId=', userId, 'table.id=', table._id, 'state=', state,
                                         'gid=', gid, 'rid=', rid, 'tid=', tid, 'sid', sid)

            if state == OnLine.OFFLINE:
                self.__ctx__.ftlog.error(methodFullName, '|userId=', userId, 'state=', state,
                                         'the state is offline error !!!')
                return False

            if table._gid != gid or table._rid != rid or table._id != tid:
                self.__ctx__.ftlog.error(methodFullName, '|userId=', userId, 'loc not match !!! room._gid=', \
                                         table._gid, 'table._rid=', table._rid, 'table._id=', table._id, \
                                         'gid=', gid, 'rid=', rid, 'tid=', tid)
                return False

            if state == OnLine.TABLEOFFLINE:
                if OnLine._debug:
                    self.__ctx__.ftlog.debug(methodFullName, '|userId=', userId,
                                             'loc match !!! from table offline to online !!!')
                self.setOnLineState(tasklet, userId, state, OnLine.ONLINE)

        return True

    def onSitDown(self, tasklet, userId, table, seatId=0):
        if seatId < 0:
            seatId = table.findSeatByUserId(userId)
        if seatId <= 0:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onSitDown error ->userId=', userId, 'seatid is zero !!!')
            return False

        gid, rid, tid, sid, state = self.getOnLineLocAndState(tasklet, userId)
        if self.isNeedReConn(table):
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onSitDown->userId=', userId, 'table.id=', table._id, 'state=', state,
                                         'gid=', gid, 'rid=', rid, 'tid=', tid, 'sid', sid)
            if state == OnLine.OFFLINE:
                self.__ctx__.ftlog.error('OnLine.canSit->userId=', userId, 'state=', state,
                                         'the state is offline error !!!')
                return False
            elif state == OnLine.TABLEOFFLINE:
                if table._gid != gid or table._rid != rid or table._id != tid or seatId != sid:
                    self.__ctx__.ftlog.error('OnLine.onSitDown->userId=', userId, 'sit not match !!! room._gid=', \
                                             table._gid, 'table._rid=', table._rid, 'table._id=', table._id, \
                                             'seatId=', seatId, 'gid=', gid, 'rid=', rid, 'tid=', tid, 'sid=', sid)
                    return False
                else:
                    if OnLine._debug:
                        self.__ctx__.ftlog.debug('OnLine.onSitDown->userId=', userId, 'sit match !!!')
            elif state == OnLine.ONLINE:
                if gid == table._gid and rid == table._rid and tid == table._id and (
                        sid == 0 or (sid > 0 and sid == seatId)):
                    if OnLine._debug:
                        self.__ctx__.ftlog.debug('OnLine.onSitDown->userId=', userId, 'sit ok !!!')
                else:
                    self.__ctx__.ftlog.error('OnLine.onSitDown->userId=', userId, 'sit error !!! room._gid=', \
                                             table._gid, 'table._rid=', table._rid, 'table._id=', table._id, \
                                             'seatId=', seatId, 'gid=', gid, 'rid=', rid, 'tid=', tid, 'sid=', sid)
                    return False

        if state == OnLine.OFFLINE:
            self.__ctx__.ftlog.error('OnLine.onSitDown->userId=', userId, 'state=', state,
                                     'the state is offline error !!!')
        elif state == OnLine.TABLEOFFLINE:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onSitDown->userId=', userId, 'from table offline to online !!!')
            self.setOnLineState(tasklet, userId, state, OnLine.ONLINE)
            state = OnLine.ONLINE
        elif state == OnLine.ONLINE:
            if OnLine._debug:
                self.__ctx__.ftlog.debug('OnLine.onSitDown->userId=', userId, 'state=', state,
                                         'the state is online !!!')

        return self.setOnLineLoc(tasklet, userId, table._gid, table._rid, table._id, seatId)

    def onStandUp(self, tasklet, userId):
        gid, rid, tid, _, _ = self.getOnLineLocAndState(tasklet, userId)
        self.setOnLineLoc(tasklet, userId, gid, rid, tid, 0)


OnLine = OnLine()
