# -*- coding=utf-8 -*-
from _base_._configure_base_ import ConfigureBase

class ConfigureData(ConfigureBase):

    def __init__(self):
        super(ConfigureData, self).__init__()

    def get_info(self):
        return {'name' : 'global_item'}

    def verify_editor_data(self, datas):
        errors = []
        return errors

    def generate_redis_datas(self, datas, redisdata):
        redisdata.add('global', datas)
