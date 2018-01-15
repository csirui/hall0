# -*- coding=utf-8 -*-

from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst


class GameData(DaoConst, DaoBase):
    def _init_singleton_(self):
        pass

    def get_game_attrs(self, uid, gameid, attrlist, filterKeywords=True):
        '''
        获取用户游戏属性列表
        '''
        values = self.__ctx__.RedisUser.execute(uid, 'HMGET', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid),
                                                *attrlist)
        if values and filterKeywords:
            return self._filter_values_(attrlist, values)
        return values

    def set_game_attrs(self, uid, gameid, attrlist, valuelist):
        '''
        设置用户游戏属性列表
        '''
        gdkv = []
        for k, v in zip(attrlist, valuelist):
            gdkv.append(k)
            gdkv.append(v)
            assert (k not in self.FILTER_MUST_FUNC_FIELDS)
        self.__ctx__.RedisUser.execute(uid, 'HMSET', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid), *gdkv)

    def get_game_attr(self, uid, gameid, attrname, filterKeywords=True):
        '''
        获取用户游戏属性
        '''
        value = self.__ctx__.RedisUser.execute(uid, 'HGET', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid), attrname)
        if value and filterKeywords:
            return self._filter_value_(attrname, value)
        return value

    def set_game_attr(self, uid, gameid, attrname, value):
        '''
        设置用户游戏属性
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        self.__ctx__.RedisUser.execute(uid, 'HSET', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid), attrname, value)

    def incr_game_attr(self, uid, gameid, attrname, value):
        '''
        INCR用户游戏属性
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        return self.__ctx__.RedisUser.execute(uid, 'HINCRBY', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid),
                                              attrname, value)

    def incr_game_attr_limit(self, uid, gameid, attrname, deltaCount, lowLimit, highLimit, chipNotEnoughOpMode):
        '''
        INCR用户游戏属性
        参考: incr_chip_limit
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        trueDetal, finalCount, fixCount = self.__ctx__.RedisUser.exec_lua_alias(uid, self.INCR_CHIP_ALIAS,
                                                                                6, deltaCount, lowLimit, highLimit,
                                                                                chipNotEnoughOpMode,
                                                                                self.HKEY_GAMEDATA + str(
                                                                                    gameid) + ':' + str(uid), attrname)
        return trueDetal, finalCount, fixCount

    def _get_game_attr_int_(self, uid, gameid, attrname):
        value = self.__ctx__.RedisUser.execute(uid, 'HGET', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid), attrname)
        if not isinstance(value, (int, float)):
            return 0
        return int(value)

    def del_game_attr(self, uid, gameid, attrname):
        '''
        删除用户游戏属性
        '''
        self.__ctx__.RedisUser.execute(uid, 'HDEL', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid), attrname)
