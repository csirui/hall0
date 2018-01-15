# -*- coding=utf-8 -*-
from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst


class UserData(DaoConst, DaoBase):
    def _init_singleton_(self):
        pass

    def get_attrs(self, uid, attrlist, filterKeywords=True):
        '''
        获取用户属性列表
        '''
        values = self.__ctx__.RedisUser.execute(uid, 'HMGET', self.HKEY_USERDATA + str(uid), *attrlist)
        if values and filterKeywords:
            return self._filter_values_(attrlist, values)
        return values

    def set_attrs(self, uid, attrlist, valuelist):
        '''
        设置用户属性列表
        '''
        gdkv = []
        for k, v in zip(attrlist, valuelist):
            gdkv.append(k)
            gdkv.append(v)
            assert (k not in self.FILTER_MUST_FUNC_FIELDS)
        self.__ctx__.RedisUser.execute(uid, 'HMSET', self.HKEY_USERDATA + str(uid), *gdkv)

    def get_attr(self, uid, attrname, filterKeywords=True):
        '''
        获取用户属性
        '''
        value = self.__ctx__.RedisUser.execute(uid, 'HGET', self.HKEY_USERDATA + str(uid), attrname)
        if value and filterKeywords:
            return self._filter_value_(attrname, value)
        return value

    def get_attr_int(self, uid, attrname):
        '''
        获取用户属性
        '''
        return self._get_user_attr_int_(uid, attrname)

    def set_attr(self, uid, attrname, value):
        '''
        设置用户属性
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        self.__ctx__.RedisUser.execute(uid, 'HSET', self.HKEY_USERDATA + str(uid), attrname, value)

    def incr_attr(self, uid, attrname, value):
        '''
        INCR用户属性
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        return self._incr_user_attr_(uid, attrname, value)

    def incr_attr_limit(self, uid, attrname, deltaCount, lowLimit, highLimit, chipNotEnoughOpMode):
        '''
        INCR用户属性
        参考: incr_chip_limit
        '''
        assert (attrname not in self.FILTER_MUST_FUNC_FIELDS)
        trueDetal, finalCount, fixCount = self.__ctx__.RedisUser.exec_lua_alias(uid, self.INCR_CHIP_ALIAS,
                                                                                6, deltaCount, lowLimit, highLimit,
                                                                                chipNotEnoughOpMode,
                                                                                self.HKEY_USERDATA + str(uid), attrname)
        return trueDetal, finalCount, fixCount

    def get_exp(self, uid, gameid):
        '''
        取得用户的经验值
        '''
        return self._get_user_attr_int_(uid, self.ATT_EXP)

    def incr_exp(self, uid, gameid, detalExp):
        '''
        调整用户的经验值
        '''
        _, finalCount, _ = self.__ctx__.RedisUser.exec_lua_alias(uid, self.INCR_CHIP_ALIAS,
                                                                 6, detalExp, 0, -1,
                                                                 self.__ctx__.ChipNotEnoughOpMode.CLEAR_ZERO,
                                                                 self.HKEY_USERDATA + str(uid), self.ATT_EXP)
        return finalCount

    def get_charm(self, uid, gameid):
        '''
        取得用户的魅力值
        '''
        return self._get_user_attr_int_(uid, self.ATT_CHARM)

    def incr_charm(self, uid, gameid, detalCharm):
        '''
        调整用户的魅力值
        '''
        _, finalCount, _ = self.__ctx__.RedisUser.exec_lua_alias(uid, self.INCR_CHIP_ALIAS,
                                                                 6, detalCharm, 0, -1,
                                                                 self.__ctx__.ChipNotEnoughOpMode.CLEAR_ZERO,
                                                                 self.HKEY_USERDATA + str(uid), self.ATT_CHARM)
        return finalCount
