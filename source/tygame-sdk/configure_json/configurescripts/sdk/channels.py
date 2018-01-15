# -*- coding=utf-8 -*-
from _base_._configure_base_ import ConfigureBase

class ConfigureData(ConfigureBase):

    def __init__(self):
        super(ConfigureData, self).__init__()
    
    def get_info(self):
        return {'name' : '通道切换'}

    def verify_editor_data(self, datas):
        errors = []
        liantong_wo = datas['paycodes'].get('liantong.wo')
        if liantong_wo :
            paydata = liantong_wo['paydata']
        
        for val in paydata.itervalues():
            val['orderProdName'] = self.data_str(val, 'orderProdName')
            
        return errors
    
    def generate_redis_datas(self, datas, redisdata):
        redisdata.add('global:channels', datas)
