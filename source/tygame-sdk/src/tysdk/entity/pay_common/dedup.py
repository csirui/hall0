# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class Deduplicates(object):
    ''' make sure a key (e.g. a transactionid) is globally unique in a peroid '''

    def __init__(self, key, ttl=60 * 60 * 24 * 30):
        self._key = key
        self._ttl = ttl

    def mark_key_exists(self, newkey):
        if not newkey:
            return
        ttl = TyContext.RedisMix.execute('TTL', self._key)
        TyContext.RedisMix.execute('SADD', self._key, newkey)
        TyContext.ftlog.info('Deduplicates(%s)' % self._key, 'add new key',
                             newkey, 'ttl:', ttl)
        if ttl < 0:
            TyContext.RedisMix.execute('EXPIRE', self._key, self._ttl)

    def is_key_duplicated(self, newkey):
        if not newkey:
            return True
        return 1 == TyContext.RedisMix.execute('SISMEMBER', self._key, newkey)
