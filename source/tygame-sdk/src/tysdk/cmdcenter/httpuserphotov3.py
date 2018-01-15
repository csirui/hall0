# -*- coding: utf-8 -*-
'''
Created on 2014年4月28日

@author: zjgzzz@126.com
'''

import base64

from tyframework.context import TyContext
from tysdk.entity.beautycertify3.userphotov3 import UserPhoto, \
    UserPhotoService
from tysdk.utils.httputils import HttpUtils


class HttpUserPhotov3(object):
    JSONPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v3/user/uploadLifePhoto': cls.doUploadLifePhoto,
                '/test/open/v3/user/uploadLifePhoto': cls.doUploadLifePhotoTest,
            }
        return cls.JSONPATHS

    @classmethod
    def checkHeadUpload(cls, checkAuthCode=True):
        gameId, userId = HttpUtils.checkGameRequest(checkAuthCode)
        base64Content = TyContext.RunHttp.getRequestParam('photoContent')
        if base64Content is None:
            raise TyContext.FreetimeException(1, 'Bad photoContent param')
        try:
            content = base64.b64decode(base64Content)
        except:
            raise TyContext.FreetimeException(1, 'Bad photoContent param')
        return gameId, userId, content

    @classmethod
    def doUploadLifePhoto(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            gameId, userId, content = cls.checkHeadUpload()
            userPhoto = UserPhotoService.uploadUserPhoto(userId, UserPhoto.PHOTO_TYPE_LIFE, content)
            TyContext.ftlog.info('User upload life photo userId=', userId,
                                 'gameId=', gameId, 'lifepurl=', userPhoto)
            mo.setResult('purl', userPhoto)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo

    @classmethod
    def doUploadLifePhotoTest(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        try:
            gameId, userId, content = cls.checkHeadUpload(False)
            userPhoto = UserPhotoService.uploadUserPhoto(userId, UserPhoto.PHOTO_TYPE_LIFE, content)
            TyContext.ftlog.info('Test User upload life photo userId=', userId,
                                 'gameId=', gameId, 'lifepurl=', userPhoto)
            mo.setResult('purl', userPhoto)
        except TyContext.FreetimeException, e:
            mo.setError(e.errorCode, e.message)
        return mo
