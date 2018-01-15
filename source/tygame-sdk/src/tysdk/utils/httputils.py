# -*- coding: utf-8 -*-
'''
Created on 2014年4月29日

@author: zjgzzz@126.com
'''
from tyframework.context import TyContext


class HttpUtils(object):
    @classmethod
    def checkGameRequest(cls, checkAuthorCode=True):
        userId = TyContext.RunHttp.getRequestParamInt('userId')
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        if userId <= 0:
            raise TyContext.FreetimeException(1, 'Bad userId')
        if gameId <= 0:
            gameId = TyContext.RunHttp.getRequestParamInt('appId')
        if gameId <= 0:
            raise TyContext.FreetimeException(1, 'Bad gameId')
        if checkAuthorCode:
            authorCode = TyContext.RunHttp.getRequestParam('authorCode')
            if not TyContext.AuthorCode.checkUserAuthorCode(userId, authorCode):
                raise TyContext.FreetimeException(1, 'Bad authorCode')
        return gameId, userId

    @classmethod
    def checkUserParam(cls):
        userId = TyContext.RunHttp.getRequestParamInt('userId')
        if userId > 0:
            return userId
        else:
            raise TyContext.FreetimeException(1, 'Bad userId')


if __name__ == '__main__':
    pass
