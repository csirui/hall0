# -*- coding=utf-8 -*-
from _base_._configure_base_ import ConfigureBase
import os

class ConfigureData(ConfigureBase):

    def __init__(self):
        super(ConfigureData, self).__init__()
        #self.default_category = ('CAT_DUANDAI', 'CAT_DUANYAN', 'CAT_THIRDPAY', 'CAT_ALIPAY', 'CAT_DEBIT_CARD', 'CAT_CREDIT_CARD', 'CAT_PHONECHARGE_CARD', 'CAT_JUNNET_CARD')
        #self.more_categories = ('CAT_LIST_TUYOU' , 'CAT_LIST_360' , 'CAT_LIST_360_DEZHOU')

    def get_info(self):
        return {'name' : 'game_item'}

    def verify_editor_data(self, datas):
        errors = []
        return errors

    def generate_redis_datas_recursive(self, jsonfile, datas, redisdata, **kwargs):
        parent = os.path.split(jsonfile)[0]
        base = []
        while parent and parent != '.' and parent != '/':
            parent, tail = os.path.split(parent)
            base.insert(0, tail)
        if base:
            redisdata.add('game:%s' % ':'.join(base), datas)
        else:
            redisdata.add('game', datas)
