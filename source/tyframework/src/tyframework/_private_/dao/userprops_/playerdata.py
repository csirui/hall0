# -*- coding=utf-8 -*-

from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst


class PlayerData(DaoConst, DaoBase):
    def _init_singleton_(self):
        pass

    def get_player_attrs(self, uid, tableid, attrlist, filterKeywords=True):
        '''
        获取用户游戏属性列表
        '''
        values = self.__ctx__.RedisUser.execute(uid, 'HMGET', self.HKEY_PLAYERDATA + str(uid) + ':' + str(tableid),
                                                *attrlist)
        if values and filterKeywords:
            return self._filter_values_(attrlist, values)
        return values

    def set_player_attrs(self, uid, tableid, attrlist, valuelist):
        '''
        设置用户游戏属性列表
        '''
        gdkv = []
        for k, v in zip(attrlist, valuelist):
            gdkv.append(k)
            gdkv.append(v)
            assert (k not in self.FILTER_MUST_FUNC_FIELDS)
        self.__ctx__.RedisUser.execute(uid, 'HMSET', self.HKEY_PLAYERDATA + str(uid) + ':' + str(tableid), *gdkv)

    def get_player_attr(self, uid, tableid, attrname, filterKeywords=True):
        '''
        获取用户游戏属性
        '''
        value = self.__ctx__.RedisUser.execute(uid, 'HGET', self.HKEY_PLAYERDATA + str(uid) + ':' + str(tableid),
                                               attrname)
        if value and filterKeywords:
            return self._filter_value_(attrname, value)
        return value

    def set_player_attr(self, uid, tableid, attrname, value):
        '''
        设置用户游戏属性
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        self.__ctx__.RedisUser.execute(uid, 'HSET', self.HKEY_PLAYERDATA + str(uid) + ':' + str(tableid), attrname,
                                       value)

    def incr_player_attr(self, uid, tableid, attrname, value):
        '''
        INCR用户游戏属性
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        return self.__ctx__.RedisUser.execute(uid, 'HINCRBY', self.HKEY_PLAYERDATA + str(uid) + ':' + str(tableid),
                                              attrname, value)

    def incr_player_attr_limit(self, uid, tableid, attrname, deltaCount, lowLimit, highLimit, chipNotEnoughOpMode):
        '''
        INCR用户游戏属性
        参考: incr_chip_limit
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        trueDetal, finalCount, fixCount = self.__ctx__.RedisUser.exec_lua_alias(uid, self.INCR_CHIP_ALIAS,
                                                                                6, deltaCount, lowLimit, highLimit,
                                                                                chipNotEnoughOpMode,
                                                                                self.HKEY_PLAYERDATA + str(
                                                                                    uid) + ':' + str(tableid), attrname)
        return trueDetal, finalCount, fixCount
