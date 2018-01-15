# -*- coding: utf-8 -*-
'''
Created on 2014年5月9日

@author: zjgzzz@126.com
'''
from tyframework.context import TyContext


class UserEvent(TyContext.TYEvent):
    def __init__(self, userId, timestamp=None):
        super(UserEvent, self).__init__(timestamp)
        self.userId = userId
