# -*- coding=utf-8 -*-

import base64
import json


class AuthorCode(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def creatUserAuthorCode(self, userId):
        '''
        生成用户的授权字符串
        '''
        ukey = ['name', 'createTime', 'authorTime']
        uname, createTime, authorTime = self.__ctx__.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), *ukey)
        if isinstance(createTime, basestring):  # createTime是每个用户的必有字段，以此来确保真正的查到了一条数据
            ct = self.__ctx__.MySqlSwap.updateUserDataAuthorTime(userId, authorTime)
            uname = unicode(uname)
            ut = self.__get_or_refresh_author_token(userId)
            authCode = json.dumps({'uid': userId, 'uname': uname,
                                   'utime': ct, 'utoken': ut})
            authCode = base64.b64encode(authCode)
            return uname, authCode
        else:
            return '', ''

    def __get_or_refresh_author_token(self, userId):
        ctfull = self.__ctx__.TimeStamp.format_time_ms()
        authorToken = self.__ctx__.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'authorToken')
        if authorToken:
            elapse = self.__ctx__.TimeStamp.get_time_str_f_diff(authorToken, ctfull)
            guard = self.__ctx__.Configure.get_global_item_int('authortoken_guardtime_in_seconds', 18000)  # 5 hours
            expire = self.__ctx__.Configure.get_global_item_int('authortoken_expire_in_seconds', 86400)  # 1 day
            if elapse < expire - guard:
                return authorToken
        self.__ctx__.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'authorToken', ctfull)
        return ctfull

    def creatUserAuthorCodeNew(self, userId):
        '''
        生成用户的授权字符串
        '''
        ukey = ['name', 'coin', 'createTime', 'email', 'authorTime']
        uname, coin, createTime, email, authorTime = self.__ctx__.RedisUser.execute(userId, 'HMGET',
                                                                                    'user:' + str(userId), *ukey)
        if isinstance(createTime, basestring):  # createTime是每个用户的必有字段，以此来确保真正的查到了一条数据
            ct = self.__ctx__.MySqlSwap.updateUserDataAuthorTime(userId, authorTime)
            uname = unicode(uname)
            ut = self.__get_or_refresh_author_token(userId)
            authStr = json.dumps({'uid': userId, 'uname': uname, 'email': email,
                                  'coin': coin if coin else 0,
                                  'utoken': ut, 'utime': ct})
            authStr = base64.b64encode(authStr)
            return uname, authStr, email
        else:
            return '', '', ''

    def checkUserAuthorInfo(self, authInfo):
        '''
        校验用户的授权字符串
        '''
        if not authInfo:
            #             self.__ctx__.ftlog.error('ERROR, checkUserAuthorInfo empty authInfo', authInfo)
            return 0, '', ''

        try:
            authInfos = self.__ctx__.strutil.loads(authInfo)
            authorcode_b64str = authInfos['authcode']
            userId = authInfos['uid']
            authcode = self.checkUserAuthorCode(userId, authorcode_b64str)
            if not authcode:
                return 0, '', ''
            authorTime = self.__ctx__.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'authorTime')
            return userId, authcode['uname'], authorTime

        except Exception, e:
            self.__ctx__.ftlog.error('ERROR, checkUserAuthorInfo exception', e,
                                     'authInfo', authInfo,
                                     'http_raw_data', self.__ctx__.RunHttp.get_request_raw_data())
            self.__ctx__.ftlog.exception()
            return 0, '', ''

    def checkUserAuthorCode(self, userId, authorcode_b64str):
        '''
        校验用户的授权字符串
        '''
        if not authorcode_b64str:
            return False
        if len(authorcode_b64str) < 10:
            self.__ctx__.ftlog.error('ERROR, checkUserAuthorCode user', userId,
                                     'wrong authorcode', authorcode_b64str,
                                     'http_raw_data', self.__ctx__.RunHttp.get_request_raw_data())
            return False

        if str(userId) == 11:  # this is a mobile phone number
            realUserId = self.__ctx__.RedisUserKeys.execute('GET', 'mobilemap:' + str(userId))
            if not realUserId:
                self.__ctx__.ftlog.error('ERROR, checkUserAuthorCode mobile', userId, 'has no mapped userId!')
                return False
            userId = realUserId

        try:
            authcode = self.__ctx__.strutil.loadsbase64(authorcode_b64str)
            if 'uid' not in authcode or authcode['uid'] != userId:
                self.__ctx__.ftlog.error('ERROR, checkUserAuthorCode user', userId, 'wrong authorcode', authcode)
                return False

            utoken = authcode['utoken']
            authorToken = self.__ctx__.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'authorToken')
            if not authorToken or authorToken != utoken:
                self.__ctx__.ftlog.error('ERROR, checkUserAuthorCode user', userId, 'authorToken timeout!', authorToken,
                                         authcode)
                return False

            return authcode

        except Exception, e:
            self.__ctx__.ftlog.error('ERROR, checkUserAuthorCode exception', e,
                                     'user', userId, 'authorcode', authorcode_b64str,
                                     'http_raw_data', self.__ctx__.RunHttp.get_request_raw_data())
            self.__ctx__.ftlog.exception()
            return False

    def makeLoginCode(self, userId, appId, authorCode):
        '''
        生成登录校验码
        '''
        # code= md5(str(userId)+str(appId)+str(appKey) + str(authorCode))
        appKey = self.__ctx__.Configure.get_game_item_str(appId, 'appKey', '')
        checkstr = str(userId) + str(appId) + str(appKey) + str(authorCode)
        return self.__ctx__.strutil.md5digest(checkstr)


AuthorCode = AuthorCode()
