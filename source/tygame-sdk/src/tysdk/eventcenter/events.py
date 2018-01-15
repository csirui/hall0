# -*- coding: utf-8 -*-

'''
Created on 2014年4月29日

@author: zjgzzz@126.com
'''
from tyframework.context import TyContext
from tysdk.entity.user_common.events import UserEvent

SdkEventBus = TyContext.TYEventBus()


class UserPhotoChangedEvent(UserEvent):
    def __str__(self):
        return str({
            'userId': self.userId,
            'photoType': self.photoType,
            'oldPhoto': self.oldPhoto,
            'newPhoto': self.newPhoto,
            'reason': self.reason,
            'timestamp': self.timestamp,
        })

    def __init__(self, userId, photoType, oldPhoto, newPhoto, reason=None, timestamp=None):
        super(UserPhotoChangedEvent, self).__init__(userId, timestamp)
        self.photoType = photoType
        self.oldPhoto = oldPhoto
        self.newPhoto = newPhoto
        self.reason = reason


if __name__ == '__main__':
    pass
