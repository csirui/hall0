# -*- coding: utf-8 -*-
'''
Created on 2014年5月9日

@author: zjgzzz@126.com
'''
import time

from datetime import datetime

from tyframework.context import TyContext
from tysdk.entity.beautycertify3.avatarverify import AvatarVerifyService


class HttpAvatarVerifyv3(object):
    JSONPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/mgr/user/avatar/accept': cls.doAccept,
                '/open/mgr/user/avatar/remove': cls.doRemove,
                '/open/mgr/user/avatar/list': cls.doList,
            }
        return cls.JSONPATHS

    @classmethod
    def doAccept(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            userIdParam = TyContext.RunHttp.getRequestParam('userIds')
            userIds = userIdParam.split(',')
            for userId in userIds:
                AvatarVerifyService.accept(userId)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doRemove(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            userIdParam = TyContext.RunHttp.getRequestParam('userIds')
            userIds = userIdParam.split(',')
            for userId in userIds:
                AvatarVerifyService.reject(userId)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doList(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
            items = []
            total = 0
            pageNo = 0
            pageSize = 30

            if userId != 0:
                purlVerifying = AvatarVerifyService.getStatus(userId)
                if purlVerifying:
                    total = 1
                    item = {}
                    item['userId'] = purlVerifying.userId
                    item['purlVerify'] = purlVerifying.purlVerify
                items.append(item)
            else:
                pageNo = TyContext.RunHttp.getRequestParamInt('pn', 0)
                pageSize = TyContext.RunHttp.getRequestParamInt('ps', 30)
                startTimeStr = TyContext.RunHttp.getRequestParam('startTime')
                endTimeStr = TyContext.RunHttp.getRequestParam('endTime')

                if startTimeStr is not None and endTimeStr is not None:
                    startTime = int(time.mktime(datetime.strptime(startTimeStr, '%Y-%m-%d %H:%M:%S').timetuple()))
                    endTime = int(time.mktime(datetime.strptime(endTimeStr, '%Y-%m-%d %H:%M:%S').timetuple()))
                else:
                    startTime = None
                    endTime = None
                total, items = AvatarVerifyService.listStatus(pageNo * pageSize, pageSize, startTime, endTime)

            mo.setResult('total', total)
            mo.setResult('items', items)
            mo.setResult('pn', pageNo)
            mo.setResult('ps', pageSize)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo


if __name__ == '__main__':
    pass
