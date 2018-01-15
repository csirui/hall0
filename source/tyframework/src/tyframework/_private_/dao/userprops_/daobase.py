# -*- coding=utf-8 -*-

class DaoBase(object):
    def __init__(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def _incr_user_attr_(self, uid, attrname, value):
        val = self.__ctx__.RedisUser.execute(uid, 'HINCRBY', self.HKEY_USERDATA + str(uid), attrname, value)
        if val == None:
            val = 0
        return val

    def _get_user_attr_int_(self, uid, attrname):
        value = self.__ctx__.RedisUser.execute(uid, 'HGET', self.HKEY_USERDATA + str(uid), attrname)
        if not isinstance(value, (int, float)):
            return 0
        return int(value)

    def _filter_values_(self, attrlist, values):
        if (not isinstance(attrlist, list)
            or not isinstance(values, list)
            or len(attrlist) != len(values)):
            return values
        for i in xrange(len(values)):
            values[i] = self._filter_value_(attrlist[i], values[i])
        return values

    def _filter_value_(self, attr, value):
        if attr in self.FILTER_KEYWORD_FIELDS:
            value = unicode(value)
            return self.__ctx__.KeywordFilter.replace(value)
        return value
