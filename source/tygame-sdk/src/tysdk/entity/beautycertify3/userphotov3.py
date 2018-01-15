# -*- coding: utf-8 -*-
'''
Created on 2014年5月5日

@author: zjgzzz@126.com
'''
import os
import random
import time

from datetime import datetime

from tyframework.context import TyContext
from tysdk.eventcenter.events import SdkEventBus, UserPhotoChangedEvent


class UserPhoto(object):
    PHOTO_TYPE_AVATAR = 1
    PHOTO_TYPE_LIFE = 2
    PHOTO_TYPE_AVATAR_VERIFYING = 3
    PHOTO_TYPES = set([PHOTO_TYPE_AVATAR_VERIFYING, PHOTO_TYPE_AVATAR, PHOTO_TYPE_LIFE])

    @classmethod
    def buildUserPath(cls, userId):
        return str(userId / 32 / 32) + '/' + str((userId / 32) % 32) + '/' + str(userId % 32) \
               + '/' + str(userId)

    @classmethod
    def buildPhotoPath(cls, userId, timestamp):
        datestr = datetime.fromtimestamp(timestamp).strftime('%Y%m%d')
        return '/' + datestr + '/' + cls.buildUserPath(userId) + '/' + str(int(timestamp)) \
               + '.jpg'

    @classmethod
    def isValidPhotoType(cls, photoType):
        return photoType in cls.PHOTO_TYPES


class UserPhotoDao(object):
    def load(self, userId, photoType):
        raise NotImplemented()

    def save(self, userId, photoType, url):
        raise NotImplemented()


class UserPhotoDaoImpl(UserPhotoDao):
    def load(self, userId, photoType):
        if photoType == UserPhoto.PHOTO_TYPE_AVATAR:
            return TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'purl')
        elif photoType == UserPhoto.PHOTO_TYPE_LIFE:
            return TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'lifepurl')
        else:
            raise TyContext.FreetimeException(1, 'Unknown head type ' + str(photoType))

    def save(self, userId, photoType, url):
        if photoType == UserPhoto.PHOTO_TYPE_AVATAR_VERIFYING:
            TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'purl_verifying', url)
        elif photoType == UserPhoto.PHOTO_TYPE_AVATAR:
            TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'purl', url)
        elif photoType == UserPhoto.PHOTO_TYPE_LIFE:
            TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'lifepurl', url)
        else:
            raise TyContext.FreetimeException(1, 'Unknown head type ' + str(photoType))


class UserPhotoService(object):
    userPhotoDao = UserPhotoDaoImpl()
    domain = None
    uploadStart = None

    @classmethod
    def getDomain(cls):
        domainConf = TyContext.Configure.get_global_item_str('photo.download.http.domain', '')
        if not domainConf.endswith('/'):
            cls.domain = domainConf + '/'
        else:
            cls.domain = domainConf
        cls.uploadStart = cls.domain + 'head/'
        return cls.domain

    @classmethod
    def getUploadStart(cls):
        if cls.uploadStart is None:
            cls.getDomain()
        return cls.uploadStart

    @classmethod
    def buildPhotoUrl(cls, photoPath):
        return cls.getDomain() + 'head' + photoPath

    @classmethod
    def buildPhotoFullPath(cls, photoPath):
        return TyContext.TYGlobal.path_webroot() + '/head' + photoPath

    @classmethod
    def isUpload(cls, url):
        if url:
            return url.startswith(cls.getUploadStart())
        return False

    @classmethod
    def savePhotoContent(cls, path, content):
        save_photo_service = TyContext.Configure.get_global_item_str('save_photo_service')
        if save_photo_service:
            cls.savePhotoContent_http(save_photo_service, path, content)
        else:
            cls.savePhotoContent_nfs(path, content)

    @classmethod
    def savePhotoContent_http(cls, service_uri, path, content):
        params = {'path': path, 'content': TyContext.strutil.b64encode(content)}
        TyContext.ftlog.debug('savePhotoContent_http request', service_uri, params)
        response = TyContext.WebPage.webget(service_uri, postdata_=params)
        TyContext.ftlog.debug('savePhotoContent_http response', response)

    @classmethod
    def savePhotoContent_nfs(cls, path, content):
        fullpath = cls.buildPhotoFullPath(path)
        dirname = os.path.dirname(fullpath)
        if not os.path.exists(dirname):
            os.makedirs(dirname, 0755)
        fd = None
        try:
            fd = os.open(fullpath, os.O_WRONLY | os.O_CREAT)
            os.write(fd, content)
        except:
            TyContext.ftlog.exception()
            raise TyContext.FreetimeException(1, 'Failed to save user head file')
        finally:
            if fd:
                os.close(fd)

    @classmethod
    def _removePhotoContent(cls, userId, url):
        #         try:
        #             fullpath = cls.buildPhotoFullPath(oldUserPhoto.path)
        #             TyContext.ftlog.info('HttpPhoto.uploadUserPhoto remove old head file', fullpath)
        #             os.remove(fullpath)
        #         except:
        #             TyContext.ftlog.exception()
        pass

    @classmethod
    def setUserPhoto(cls, userId, photoType, userPhoto):
        if cls.isUpload(userPhoto):
            return
        cls._setUserPhoto(userId, photoType, userPhoto)

    @classmethod
    def _setUserPhoto(cls, userId, photoType, userPhoto, reason=None):
        assert (UserPhoto.isValidPhotoType(photoType))
        oldUserPhoto = cls.userPhotoDao.load(userId, photoType)
        if oldUserPhoto != userPhoto:
            if reason == 'upload' and photoType == UserPhoto.PHOTO_TYPE_AVATAR:
                need_verify = TyContext.Configure.get_global_item_int('user.avatar.need.verify', 0)
                verifying_avatar = TyContext.Configure.get_global_item_str('user.avatar.verifying')
                if need_verify and verifying_avatar:
                    cls.userPhotoDao.save(userId, UserPhoto.PHOTO_TYPE_AVATAR, verifying_avatar)
                    cls.userPhotoDao.save(userId, UserPhoto.PHOTO_TYPE_AVATAR_VERIFYING, userPhoto)
                else:
                    cls.userPhotoDao.save(userId, UserPhoto.PHOTO_TYPE_AVATAR, userPhoto)
                    cls.userPhotoDao.save(userId, UserPhoto.PHOTO_TYPE_AVATAR_VERIFYING, '')
            else:
                cls.userPhotoDao.save(userId, photoType, userPhoto)
            if oldUserPhoto:
                cls._removePhotoContent(userId, oldUserPhoto)
            SdkEventBus.publishEvent(UserPhotoChangedEvent(userId, photoType, oldUserPhoto, userPhoto, reason))

    @classmethod
    def uploadUserPhoto(cls, userId, photoType, content):
        assert (UserPhoto.isValidPhotoType(photoType))
        path = UserPhoto.buildPhotoPath(userId, time.time())
        cls.savePhotoContent(path, content)
        newUserPhoto = cls.buildPhotoUrl(path)
        cls._setUserPhoto(userId, photoType, newUserPhoto, reason='upload')
        return newUserPhoto

    @classmethod
    def getUserPhoto(cls, userId, photoType):
        return cls.userPhotoDao.load(userId, photoType)

    @classmethod
    def getDefaultUserAvatar(cls, userId, clientId):
        defaultAvatars = TyContext.Configure.get_global_item_json('user.avatar.default', [])
        if defaultAvatars and isinstance(defaultAvatars, list) and len(defaultAvatars) > 0:
            idx = random.randint(0, len(defaultAvatars) - 1)
            return defaultAvatars[idx]
        return ''
