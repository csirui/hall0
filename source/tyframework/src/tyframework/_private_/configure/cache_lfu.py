# -*- coding=utf-8 -*-

from tyframework._private_.util.lrucache import lfu_cache


class CacheLfu(object):
    def __init__(self, redis_data_provider):
        self.redis_data_provider = redis_data_provider

    @lfu_cache(maxsize=80000, cache_key_args_index=1)
    def _get_cache_data_(self, redisfullkey, datatype, decodeutf8):
        return self.redis_data_provider(redisfullkey, datatype, decodeutf8)

    def _clear_keys_(self, keylist):
        self._get_cache_data_.clear_keys(keylist)

    def _clear_keys_all_(self):
        self._get_cache_data_.clear()
