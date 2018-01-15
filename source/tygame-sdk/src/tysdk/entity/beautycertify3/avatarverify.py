# -*- coding: utf-8 -*-
'''
Created on 2014年5月8日

@author: zjgzzz@126.com
'''
import time

from tyframework.context import TyContext
from tysdk.entity.beautycertify3.userphotov3 import UserPhoto, \
    UserPhotoService
from tysdk.eventcenter.events import SdkEventBus, UserPhotoChangedEvent

ERR_INVALID_STATE = 1
ERR_REMOVED = 4


class AvatarVerifyStatus(object):
    def __str__(self):
        return str({'userId': self.userId, 'purlVerify': self.purlVerify})

    def __init__(self, userId, purlVerify):
        self.userId = userId
        self.purlVerify = purlVerify


class AvatarVerifyDao(object):
    def load(self, userId):
        raise NotImplemented()

    def save(self, status):
        raise NotImplemented()

    def remove(self, userId):
        raise NotImplemented()


class VerifyingUserDao(object):
    def save(self, userId, timestamp):
        raise NotImplemented()

    def remove(self, userId):
        raise NotImplemented()

    def query(self, startIndex, count, startTime, endTime):
        raise NotImplemented()


class AvatarVerifyDaoImpl(AvatarVerifyDao):
    def load(self, userId):
        purlVerify = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId),
                                                 'purl_verifying')
        if not purlVerify:
            return None
        if '125.39.218.101' in purlVerify:
            purlVerify = purlVerify.replace('125.39.218.101', 'ddz.image.tuyoo.com')
            TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId),
                                        'purl_verifying', purlVerify)
        return AvatarVerifyStatus(userId, purlVerify)

    def accept(self, userId):
        purlVerify = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'purl_verifying')
        if purlVerify:
            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), 'purl_verifying', '',
                                        'purl', purlVerify)
            TyContext.ftlog.debug('AvatarVerifyDaoImpl HMSET', 'user:' + str(userId), 'purl_verifying', '',
                                  'purl', purlVerify)

    def remove(self, userId):
        TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), 'purl', '', 'purl_verifying', '')


class VerifyingUserDaoImpl(VerifyingUserDao):
    def _total(self, startTime, endTime):
        if startTime is not None and endTime is not None:
            return TyContext.RedisAvatar.execute('ZCOUNT', 'avatar.verify', startTime, endTime)
        return TyContext.RedisAvatar.execute('ZCARD', 'avatar.verify')

    def save(self, userId, timestamp):
        TyContext.RedisAvatar.execute('ZADD', 'avatar.verify', timestamp, userId)

    def remove(self, userId):
        if isinstance(userId, (list, tuple)):
            ret = TyContext.RedisAvatar.execute('ZREM', 'avatar.verify', *userId)
        else:
            ret = TyContext.RedisAvatar.execute('ZREM', 'avatar.verify', userId)
        TyContext.ftlog.info('VerifyingUserDaoImpl ZREM', 'avatar.verify', userId, 'ret', ret)

    def query(self, startIndex, count, startTime, endTime):
        total = self._total(startTime, endTime)
        if total <= 0:
            return 0, None

        if count <= 0:
            return total, None

        userIds = None
        if startTime is not None and endTime is not None:
            userIds = TyContext.RedisAvatar.execute('ZREVRANGEBYSCORE', 'avatar.verify',
                                                    int(endTime), int(startTime), 'limit',
                                                    startIndex, startIndex + count - 1)
            TyContext.ftlog.debug('VerifyingUserDaoImpl ZREVRANGEBYSCORE', 'avatar.verify', startTime, endTime,
                                  'limit', startIndex, count, 'return=', userIds)
        else:
            userIds = TyContext.RedisAvatar.execute('ZREVRANGE', 'avatar.verify',
                                                    startIndex, startIndex + count - 1)
            TyContext.ftlog.debug('VerifyingUserDaoImpl ZREVRANGE', 'avatar.verify', startIndex, startIndex + count - 1,
                                  'return=', userIds)

        return total, userIds


class AvatarVerifyService(object):
    avatar_verify_dao = AvatarVerifyDaoImpl()
    verifying_user_dao = None

    @classmethod
    def onInit(cls):
        cls.verifying_user_dao = VerifyingUserDaoImpl()
        SdkEventBus.subscribe(UserPhotoChangedEvent, AvatarVerifyService.handleUserPhotoChangedEvent)
        TyContext.ftlog.debug('AvatarVerifyService init finished')

    @classmethod
    def handleUserPhotoChangedEvent(cls, event):
        if event.reason == 'reject' or event.photoType != UserPhoto.PHOTO_TYPE_AVATAR:
            return

        TyContext.ftlog.debug('AvatarVerifyService.handleUserPhotoChangedEvent', event)

        oldIsUpload = UserPhotoService.isUpload(event.oldPhoto)
        newIsUpload = UserPhotoService.isUpload(event.newPhoto)

        TyContext.ftlog.debug('AvatarVerifyService.handleUserPhotoChangedEvent oldIsUpload', oldIsUpload, 'newIsUpload',
                              newIsUpload)

        if newIsUpload:
            cls.create(event.userId)
        else:
            cls.remove(event.userId)

    @classmethod
    def remove(cls, userId):
        status = cls.avatar_verify_dao.load(userId)
        TyContext.ftlog.debug('AvatarVerifyService.remove userId', userId, 'status', status)
        if status:
            cls.verifying_user_dao.remove(userId)
            TyContext.ftlog.info('Remove avatar status for userId=', userId)

    @classmethod
    def getStatus(cls, userId):
        return cls.avatar_verify_dao.load(userId)

    @classmethod
    def reject(cls, userId):
        cls.avatar_verify_dao.remove(userId)
        cls.verifying_user_dao.remove(userId)

    @classmethod
    def create(cls, userId, ts=None):
        ts = ts or time.time()
        cls.verifying_user_dao.save(userId, int(ts))

    @classmethod
    def accept(cls, userId):
        cls.avatar_verify_dao.accept(userId)
        cls.verifying_user_dao.remove(userId)
        return

    @classmethod
    def listStatus(cls, startIndex, count, startTime=None, endTime=None):
        ret_cnt = 0
        enough = False
        last = False
        statusList = []
        cnt_loop = 0
        stop = 100
        cold_users = []
        while (stop):
            total, userIds = cls.verifying_user_dao.query(
                startIndex + cnt_loop * count - len(cold_users), count,
                startTime, endTime)
            cnt_loop += 1
            # stop -= 1
            if not userIds or len(userIds) == 0:
                return 0, []

            if len(userIds) < count:
                last = True

            cold_users = []
            for userId in userIds:
                status = cls.avatar_verify_dao.load(userId)
                if not status:
                    cold_users.append(userId)
                    continue
                item = {}
                item['userId'] = status.userId
                item['purlVerify'] = status.purlVerify
                statusList.append(item)
                if len(statusList) >= count:
                    enough = True
                    break

            # XXX remove cold data from verifying set since we have implemented
            # the restoring machanism. after all cold data being removed, this
            # func can be greatly simplified
            if len(cold_users):
                cls.verifying_user_dao.remove(cold_users)

            if enough or last:
                break

        return total, statusList


if __name__ == '__main__':
    pass
