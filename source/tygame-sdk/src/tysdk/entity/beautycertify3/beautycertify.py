# -*- coding: utf-8 -*-
'''
Created on 2014年5月5日

@author: zjgzzz@126.com
'''
import json
import time

from tyframework.context import TyContext
from tysdk.entity.beautycertify3.userphotov3 import UserPhotoService, \
    UserPhoto
from tysdk.eventcenter.events import SdkEventBus, UserPhotoChangedEvent

ERR_INVALID_STATE = 1
ERR_MARGIN_NOT_ENOUGH = 2
ERR_NO_CUSTOM_HEAD = 3
ERR_REMOVED = 4

MYSQL_BEAUTY_NAME = 'beauty'


class BeautyCertifyStatus(object):
    STATE_IDLE = 0
    STATE_APPLIED = 1
    STATE_PHOTOED = 2
    STATE_VERIFYING = 3
    STATE_ACCEPTED = 4
    STATE_REJECTED = 5

    def __init__(self, userId, gameId=0, state=STATE_IDLE, info='', updateTime=None):
        self.userId = userId
        self.gameId = gameId
        self.state = state
        self.info = info
        self.updateTime = updateTime or int(time.time())


class BeautySignDao(object):
    BEAUTY_BIT = 1
    BEAUTY_EVER_BIT = 2
    BEAUTY_ALL = BEAUTY_BIT | BEAUTY_BIT

    def getBeauty(self, userId):
        raise NotImplemented()

    def setBeauty(self, userId, beauty):
        raise NotImplemented()


class BeautySignDaoImpl(BeautySignDao):
    def getBeauty(self, userId):
        beauty = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'beauty')
        if beauty is None:
            return 0
        return beauty

    def setBeauty(self, userId, beauty):
        TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'beauty', beauty)


class BeautyCertifyStatusDao(object):
    def load(self, userId):
        raise NotImplemented()

    def save(self, status):
        raise NotImplemented()

    def remove(self, userId):
        raise NotImplemented()

    def query(self, startIndex, count, state):
        raise NotImplemented()


class BeautyCertifyStatusDaoMysqlImpl(BeautyCertifyStatusDao):
    def __init__(self):
        self.__dbpool = None

    def load(self, userId):
        sqlstr = "select game_id, state, reason, timestamp from beauty_certify where user_id = %s"
        values = TyContext.DbMySql.query(MYSQL_BEAUTY_NAME, sqlstr, [userId])
        if not values or len(values) <= 0:
            return None
        return BeautyCertifyStatus(userId, int(values[0][0]), int(values[0][1]),
                                   str(values[0][2]), int(values[0][3]))

    def save(self, status):
        sqlstr = 'insert into beauty_certify (user_id, game_id, state, reason, timestamp)' \
                 ' values(%s,%s,%s,%s,%s) ON DUPLICATE KEY' \
                 ' update game_id=%s, state=%s, reason=%s, timestamp=%s'
        TyContext.DbMySql.query(MYSQL_BEAUTY_NAME, sqlstr, [status.userId,
                                                            status.gameId, status.state, status.info, status.updateTime,
                                                            status.gameId, status.state, status.info,
                                                            status.updateTime])

    def remove(self, userId):
        sqlstr = 'delete from beauty_certify where user_id=%s'
        TyContext.DbMySql.query(MYSQL_BEAUTY_NAME, sqlstr, [userId])

    def _runQuery(self, trans, *args):
        TyContext.ftlog.debug('BeautyCertifyStatusDaoMysqlImpl._runQuery args=', args)
        startIndex = args[0][0]
        count = args[0][1]
        states = args[0][2]
        startTime = args[0][3]
        endTime = args[0][4]

        sqlargs = []
        sqlstr = 'select SQL_CALC_FOUND_ROWS user_id, game_id, state, reason, timestamp from beauty_certify'
        if states is not None:
            sqlstr += ' where state in ('
            ql = ['%s' for _ in xrange(len(states))]
            substr = ','.join(ql)
            sqlstr += substr
            sqlstr += ')'
            sqlargs.extend(states)
            if startTime is not None and endTime is not None:
                sqlargs.append(startTime)
                sqlargs.append(endTime)
                sqlstr += ' and timestamp >= %s and timestamp <= %s'
        elif startTime is not None and endTime is not None:
            sqlargs.append(startTime)
            sqlargs.append(endTime)
            sqlstr += ' where timestamp >= %s and timestamp <= %s'
        sqlargs.append(startIndex)
        sqlargs.append(count)
        sqlstr += ' order by timestamp desc limit %s, %s'
        TyContext.ftlog.debug('query(', sqlstr, ', ', sqlargs, ')')
        trans.execute(sqlstr, sqlargs)
        values = trans.fetchall()
        TyContext.ftlog.debug('query(', sqlstr, ') ==> ', values)
        sqlstr = 'select found_rows()'
        trans.execute(sqlstr)
        totalvalues = trans.fetchall()
        if not totalvalues or len(totalvalues) <= 0:
            return 0, []
        TyContext.ftlog.debug('select found_rows() return ', totalvalues)
        total = totalvalues[0][0]
        statusList = []
        if values:
            for value in values:
                status = BeautyCertifyStatus(int(value[0]), int(value[1]), int(value[2]),
                                             str(value[3]), int(value[4]))
                statusList.append(status)
        return total, statusList

    def query(self, startIndex, count, states=None, startTime=None, endTime=None):
        assert (startIndex >= 0 and count > 0)
        TyContext.DbMySql.query(MYSQL_BEAUTY_NAME, self._runQuery, [startIndex, count, states, startTime, endTime])


class MarginCollector(object):
    def collect(self, gameId, userId):
        raise NotImplemented()

    def back(self, gameId, userId):
        raise NotImplemented()

    def reward(self, gameId, userId):
        raise NotImplemented()


class MarginCollectorImpl(MarginCollector):
    def buildCollectUrl(self, gameId, userId):
        conf = TyContext.Configure.get_global_item_json('beauty.certify.margin', {})
        strGameId = str(gameId)
        if strGameId in conf:
            return conf[strGameId]['collect']
        return ''

    def buildBackUrl(self, gameId, userId):
        conf = TyContext.Configure.get_global_item_json('beauty.certify.margin', {})
        strGameId = str(gameId)
        if strGameId in conf:
            return conf[strGameId]['back']
        return ''

    def buildRewardUrl(self, gameId, userId):
        conf = TyContext.Configure.get_global_item_json('beauty.certify.margin', {})
        strGameId = str(gameId)
        if strGameId in conf:
            return conf[strGameId]['reward']
        return ''

    def collect(self, gameId, userId):
        url = self.buildCollectUrl(gameId, userId)
        if not url:
            TyContext.ftlog.error('MarginCollectorImpl collect url null: '
                                  'gameId', gameId, 'userId', userId)
            return
        response, requestUrl = TyContext.WebPage.webget(url, {'userId': userId})
        try:
            datas = json.loads(response)
            if 'error' in datas:
                raise TyContext.FreetimeException(ERR_MARGIN_NOT_ENOUGH, '金币不足')
        except:
            TyContext.ftlog.error('MarginCollectorImpl collect return ERROR, gameId=', gameId,
                                  'userId=', userId, 'requestUrl=', url, 'response=', response)
            raise TyContext.FreetimeException(ERR_MARGIN_NOT_ENOUGH, '金币不足')

    def back(self, gameId, userId):
        url = self.buildBackUrl(gameId, userId)
        TyContext.WebPage.webget(url, {'userId': userId})

    def reward(self, gameId, userId):
        url = self.buildRewardUrl(gameId, userId)
        TyContext.WebPage.webget(url, {'userId': userId})


class BeautyCertifyService(object):
    beautyCertifyStatusDao = BeautyCertifyStatusDaoMysqlImpl()
    marginCollector = MarginCollectorImpl()
    beautySignDao = BeautySignDaoImpl()

    @classmethod
    def onInit(cls):
        SdkEventBus.subscribe(UserPhotoChangedEvent, BeautyCertifyService.handleUserPhotoChangedEvent)
        dbconf = TyContext.TYGlobal.mysql(MYSQL_BEAUTY_NAME)
        TyContext.ftlog.debug('BeautyCertifyStatusDaoMysqlImpl.__getMysqlConn dbconf=', dbconf)
        TyContext.DbMySql.connect(MYSQL_BEAUTY_NAME, dbconf)

    @classmethod
    def handleUserPhotoChangedEvent(cls, event):
        TyContext.ftlog.info('BeautyCertifyService.handleUserPhotoChangedEvent userId=', event.userId,
                             'headType=', event.photoType)
        if (event.photoType == UserPhoto.PHOTO_TYPE_LIFE):
            status = cls.beautyCertifyStatusDao.load(event.userId)
            if status is not None and status.state == BeautyCertifyStatus.STATE_APPLIED:
                cls.updateState(status, BeautyCertifyStatus.STATE_PHOTOED)
                cls.beautyCertifyStatusDao.save(status)
        elif (event.photoType == UserPhoto.PHOTO_TYPE_AVATAR):
            status = cls.beautyCertifyStatusDao.load(event.userId)
            if status is not None and status.state != BeautyCertifyStatus.STATE_IDLE:
                cls.remove(event.userId)

    @classmethod
    def onUserSexChanged(cls, userId, oldSex, newSex):
        if oldSex != newSex:
            TyContext.ftlog.info('BeautyCertifyService.onUserSexChanged userId=', userId,
                                 'oldSex=', oldSex, 'newSex=', newSex)

            status = cls.beautyCertifyStatusDao.load(userId)
            if status is not None and status.state != BeautyCertifyStatus.STATE_IDLE:
                cls.updateState(status, BeautyCertifyStatus.STATE_IDLE)
                cls.beautyCertifyStatusDao.save(status)

    @classmethod
    def getBeautyCertifyStatus(cls, userId):
        status = cls.beautyCertifyStatusDao.load(userId)
        if status is None:
            return BeautyCertifyStatus(userId)
        return status

    @classmethod
    def updateState(cls, status, newState, info=''):
        oldState = status.state
        status.state = newState
        status.info = info
        status.updateTime = int(time.time())
        TyContext.ftlog.info('BeautyCertifyService.updateState userId=', status.userId,
                             'oldState=', oldState, 'newState=', newState, 'info=', info)

    @classmethod
    def listStatus(cls, startIndex, count, states=None, startTime=None, endTime=None):
        TyContext.ftlog.debug('BeautyCertifyService.listStatus startIndex=', startIndex,
                              'count=', count, 'states=', states, 'startTime=', startTime,
                              'endTime=', endTime)
        total, statusList = cls.beautyCertifyStatusDao.query(startIndex, count, states, startTime, endTime)
        if statusList is None:
            statusList = []
        return total, statusList

    @classmethod
    def requestVerify(cls, userId):
        status = cls.beautyCertifyStatusDao.load(userId)
        if status is None:
            raise TyContext.FreetimeException(ERR_REMOVED, '记录已被删除')
        if BeautyCertifyStatus.STATE_PHOTOED != status.state:
            raise TyContext.FreetimeException(ERR_INVALID_STATE, '还没有上传生活照')

        TyContext.ftlog.info('BeautyCertifyService.requestVerify accept=', userId)
        cls.updateState(status, BeautyCertifyStatus.STATE_VERIFYING, '')
        cls.beautyCertifyStatusDao.save(status)
        return status

    @classmethod
    def accept(cls, userId):
        status = cls.beautyCertifyStatusDao.load(userId)
        if status is None:
            raise TyContext.FreetimeException(ERR_REMOVED, '记录已被删除')
        if BeautyCertifyStatus.STATE_VERIFYING != status.state:
            raise TyContext.FreetimeException(ERR_INVALID_STATE, '审核中的才能通过')

        TyContext.ftlog.info('BeautyCertifyService.accept userId=', userId)
        cls.marginCollector.back(status.gameId, status.userId)
        cls.updateState(status, BeautyCertifyStatus.STATE_ACCEPTED)
        cls.beautyCertifyStatusDao.save(status)
        beauty = cls.beautySignDao.getBeauty(status.userId)
        everBit = beauty & BeautySignDao.BEAUTY_EVER_BIT
        cls.beautySignDao.setBeauty(status.userId, BeautySignDao.BEAUTY_EVER_BIT | BeautySignDao.BEAUTY_BIT)
        if everBit == 0:
            cls.marginCollector.reward(status.gameId, status.userId)
        return status

    @classmethod
    def reject(cls, userId, reason=''):
        status = cls.beautyCertifyStatusDao.load(userId)
        if status is None:
            raise TyContext.FreetimeException(ERR_REMOVED, '记录已被删除')
        if BeautyCertifyStatus.STATE_VERIFYING != status.state:
            raise TyContext.FreetimeException(ERR_INVALID_STATE, '审核中的才能拒绝')

        TyContext.ftlog.info('BeautyCertifyService.reject userId=', userId)
        cls.updateState(status, BeautyCertifyStatus.STATE_REJECTED)
        cls.beautyCertifyStatusDao.save(status)
        return status

    @classmethod
    def revoke(cls, userId):
        status = cls.beautyCertifyStatusDao.load(userId)
        if status is None:
            raise TyContext.FreetimeException(ERR_REMOVED, '记录已被删除')
        if BeautyCertifyStatus.STATE_ACCEPTED != status.state:
            raise TyContext.FreetimeException(ERR_INVALID_STATE, '通过的才能撤销')
        TyContext.ftlog.info('BeautyCertifyService.revoke userId=', userId)
        cls._remove(status)
        beauty = cls.beautySignDao.getBeauty(status.userId)
        beauty &= ~BeautySignDao.BEAUTY_BIT
        cls.beautySignDao.setBeauty(userId, beauty)

    @classmethod
    def remove(cls, userId):
        status = cls.beautyCertifyStatusDao.load(userId)
        if status is None:
            raise TyContext.FreetimeException(ERR_REMOVED, '记录已被删除')
        TyContext.ftlog.info('BeautyCertifyService.remove userId=', userId)
        cls._remove(status)

    @classmethod
    def _remove(cls, status):
        beauty = cls.beautySignDao.getBeauty(status.userId)
        beauty &= ~BeautySignDao.BEAUTY_BIT
        cls.beautySignDao.setBeauty(status.userId, beauty)
        cls.beautyCertifyStatusDao.remove(status.userId)

    @classmethod
    def applyBeautyCertify(cls, gameId, userId):
        status = cls.getBeautyCertifyStatus(userId)
        if status.state > BeautyCertifyStatus.STATE_VERIFYING:
            status.state = BeautyCertifyStatus.STATE_IDLE
            status.gameId = 0
        if status.state != BeautyCertifyStatus.STATE_IDLE:
            raise TyContext.FreetimeException(ERR_INVALID_STATE, '错误的状态')

        userCustomHead = UserPhotoService.getUserPhoto(userId, UserPhoto.PHOTO_TYPE_AVATAR)
        if not userCustomHead:
            raise TyContext.FreetimeException(ERR_NO_CUSTOM_HEAD, '没有自定义头像')

        cls.marginCollector.collect(gameId, userId)

        status.gameId = gameId
        userLifeHead = UserPhotoService.getUserPhoto(userId, UserPhoto.PHOTO_TYPE_LIFE)
        if userLifeHead:
            newState = BeautyCertifyStatus.STATE_PHOTOED
        else:
            newState = BeautyCertifyStatus.STATE_APPLIED
        cls.updateState(status, newState)
        cls.beautyCertifyStatusDao.save(status)
        return status
