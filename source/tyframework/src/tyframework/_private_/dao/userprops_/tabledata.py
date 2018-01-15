# -*- coding=utf-8 -*-

from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst


class TableData(DaoConst, DaoBase):
    def _init_singleton_(self):
        pass

    def get_table_attrs(self, tableid, attrlist, filterKeywords=True):
        '''
        获取用户游戏属性列表
        '''
        values = self.__ctx__.RedisTableData.execute(tableid, 'HMGET', self.HKEY_TABLEDATA + str(tableid), *attrlist)
        if values and filterKeywords:
            return self._filter_values_(attrlist, values)
        return values

    def set_table_attrs(self, tableid, attrlist, valuelist):
        '''
        设置用户游戏属性列表
        '''
        gdkv = []
        for k, v in zip(attrlist, valuelist):
            gdkv.append(k)
            gdkv.append(v)
            assert (k not in self.FILTER_MUST_FUNC_FIELDS)
        self.__ctx__.RedisTableData.execute(tableid, 'HMSET', self.HKEY_TABLEDATA + str(tableid), *gdkv)

    def get_table_attr(self, tableid, attrname, filterKeywords=True):
        '''
        获取用户游戏属性
        '''
        value = self.__ctx__.RedisTableData.execute(tableid, 'HGET', self.HKEY_TABLEDATA + str(tableid), attrname)
        if value and filterKeywords:
            return self._filter_value_(attrname, value)
        return value

    def set_table_attr(self, tableid, attrname, value):
        '''
        设置用户游戏属性
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        self.__ctx__.RedisTableData.execute(tableid, 'HSET', self.HKEY_TABLEDATA + str(tableid), attrname, value)

    def incr_table_attr(self, tableid, attrname, value):
        '''
        INCR用户游戏属性
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        return self.__ctx__.RedisTableData.execute(tableid, 'HINCRBY', self.HKEY_TABLEDATA + str(tableid), attrname,
                                                   value)

    def incr_table_attr_limit(self, tableid, attrname, deltaCount, lowLimit, highLimit, chipNotEnoughOpMode):
        '''
        INCR用户游戏属性
        参考: incr_chip_limit
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        trueDetal, finalCount, fixCount = self.__ctx__.RedisTableData.exec_lua_alias(tableid, self.INCR_CHIP_ALIAS,
                                                                                     6, deltaCount, lowLimit, highLimit,
                                                                                     chipNotEnoughOpMode,
                                                                                     self.HKEY_TABLEDATA + str(tableid),
                                                                                     attrname)
        return trueDetal, finalCount, fixCount
