# -*- coding=utf-8 -*-
from _base_._configure_base_ import ConfigureBase

class ConfigureData(ConfigureBase):

    def __init__(self):
        super(ConfigureData, self).__init__()

    def get_info(self):
        return {'name' : '计费点绑定'}

    def verify_editor_data(self, datas):
        from tymanager.managers.productdefmgr import ProductDefMgr
        errors = []

        #校验商品ID合法性
        ydmm = datas['paycodes'].get('ydmm')
        if ydmm :
            paydata = ydmm['paydata']
            for idx in xrange(len(paydata)):
                paydata[idx]['orderProdName'] = self.data_str(paydata[idx], 'orderProdName')
                if not ProductDefMgr.is_valid_productid(paydata[idx]['id']) :
                    errors.append('ydmm productid = %s, not define' % paydata[idx]['id'])

        #XXX add ydjd
        # contentId is appid
        # it has also cpid

        liantongwo = datas['paycodes'].get('liantongwo')
        if liantongwo :
            paydata = liantongwo['paydata']
            for idx in xrange(len(paydata)):
                paydata[idx]['orderProdName'] = self.data_str(paydata[idx], 'orderProdName')
                if not ProductDefMgr.is_valid_productid(paydata[idx]['id']) :
                    errors.append('liantongwo productid = %s, not define' % paydata[idx]['id'])

        #XXX need to add ydjd/aigame/weixin/etc

        return errors

    def generate_redis_datas(self, datas, redisdata):
        redisdata.add('global:paycodes', datas)
        #XXX need to convert liantongwo to liantong.wo
