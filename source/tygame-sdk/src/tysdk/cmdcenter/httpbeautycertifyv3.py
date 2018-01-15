# -*- coding: utf-8 -*-
'''
Created on 2014年4月28日

@author: zjgzzz@126.com
'''

import time

from datetime import datetime

from tyframework.context import TyContext
from tysdk.entity.beautycertify3.beautycertify import BeautyCertifyService, \
    BeautyCertifyStatus
from tysdk.utils.httputils import HttpUtils


class HttpBeautyCertifyv3(object):
    JSONPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v3/user/beautyCertify/state': cls.doGetBeautyCertifyState,
                '/open/v3/user/beautyCertify/apply': cls.doApplyBeautyCertify,
                '/open/v3/user/beautyCertify/requestVerify': cls.doRequestVerify,

                '/open/mgr/user/beautyCertify/accept': cls.doAccept,
                '/open/mgr/user/beautyCertify/reject': cls.doReject,
                '/open/mgr/user/beautyCertify/revoke': cls.doRevoke,
                '/open/mgr/user/beautyCertify/list': cls.doList,
                '/open/mgr/user/beautyCertify/remove': cls.doRemove,

                '/test/open/v3/user/beautyCertify/state': cls.doGetBeautyCertifyStateTest,
                '/test/open/v3/user/beautyCertify/apply': cls.doApplyBeautyCertifyTest,
                '/test/open/v3/user/beautyCertify/requestVerify': cls.doRequestVerifyTest,
            }
        return cls.JSONPATHS

    @classmethod
    def doGetBeautyCertifyStateTest(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            _gameId, userId = HttpUtils.checkGameRequest(False)
            status = BeautyCertifyService.getBeautyCertifyStatus(userId)
            mo.setResult('state', status.state)
            mo.setResult('info', status.info)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doGetBeautyCertifyState(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            _gameId, userId = HttpUtils.checkGameRequest()
            status = BeautyCertifyService.getBeautyCertifyStatus(userId)
            mo.setResult('state', status.state)
            mo.setResult('info', status.info)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doApplyBeautyCertify(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            gameId, userId = HttpUtils.checkGameRequest()
            status = BeautyCertifyService.applyBeautyCertify(gameId, userId)
            mo.setResult('state', status.state)
            mo.setResult('info', status.info)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doApplyBeautyCertifyTest(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            gameId, userId = HttpUtils.checkGameRequest(False)
            status = BeautyCertifyService.applyBeautyCertify(gameId, userId)
            mo.setResult('state', status.state)
            mo.setResult('info', status.info)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doRequestVerifyTest(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            _gameId, userId = HttpUtils.checkGameRequest(False)
            status = BeautyCertifyService.requestVerify(userId)
            mo.setResult('state', status.state)
            mo.setResult('info', status.info)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doRequestVerify(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            _gameId, userId = HttpUtils.checkGameRequest()
            status = BeautyCertifyService.requestVerify(userId)
            mo.setResult('state', status.state)
            mo.setResult('info', status.info)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doAccept(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            userId = HttpUtils.checkUserParam()
            status = BeautyCertifyService.accept(userId)
            mo.setResult('state', status.state)
            mo.setResult('info', status.info)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doReject(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            userId = HttpUtils.checkUserParam()
            reason = TyContext.RunHttp.getRequestParam('reason')
            status = BeautyCertifyService.reject(userId, reason)
            mo.setResult('state', status.state)
            mo.setResult('info', status.info)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doRevoke(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            userId = HttpUtils.checkUserParam()
            BeautyCertifyService.revoke(userId)
            mo.setResult('info', '')
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doRemove(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            userId = HttpUtils.checkUserParam()
            BeautyCertifyService.remove(userId)
            mo.setResult('info', '')
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def _getUserInfo(cls, userId):
        return TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'name', 'sex', 'purl', 'lifepurl')

    @classmethod
    def convertStatusToItem(cls, status):
        item = {
            'userId': status.userId,
            'gameId': status.gameId,
            'state': status.state,
            'time': status.updateTime,
            'reason': status.info,
        }
        name, sex, purl, lifepurl = cls._getUserInfo(status.userId)
        item['name'] = name
        item['sex'] = sex
        item['purl'] = purl
        item['lifepurl'] = '' if lifepurl is None else lifepurl
        return item

    @classmethod
    def doList(cls, path):
        mo = TyContext.Cls_MsgPack()
        try:
            userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
            items = []
            total = 0

            if userId != 0:
                status = BeautyCertifyService.getBeautyCertifyStatus(userId)
                if status:
                    total = 1
                    items.append(cls.convertStatusToItem(status))
            else:
                pageNo = TyContext.RunHttp.getRequestParamInt('pn', 0)
                pageSize = TyContext.RunHttp.getRequestParamInt('ps', 30)
                state = TyContext.RunHttp.getRequestParamInt('state', 0)
                startTimeStr = TyContext.RunHttp.getRequestParam('startTime')
                endTimeStr = TyContext.RunHttp.getRequestParam('endTime')
                states = None
                if (state >= BeautyCertifyStatus.STATE_VERIFYING and
                            state < BeautyCertifyStatus.STATE_REJECTED):
                    states = [state]
                else:
                    states = [3, 4]

                if startTimeStr is not None and endTimeStr is not None:
                    startTime = int(time.mktime(datetime.strptime(startTimeStr, '%Y-%m-%d %H:%M:%S').timetuple()))
                    endTime = int(time.mktime(datetime.strptime(endTimeStr, '%Y-%m-%d %H:%M:%S').timetuple()))
                else:
                    startTime = None
                    endTime = None
                total, statusList = BeautyCertifyService.listStatus(pageNo * pageSize, pageSize, states, startTime,
                                                                    endTime)

                for status in statusList:
                    items.append(cls.convertStatusToItem(status))
            mo.setResult('total', total)
            mo.setResult('items', items)
            mo.setResult('pn', pageNo)
            mo.setResult('ps', pageSize)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo
