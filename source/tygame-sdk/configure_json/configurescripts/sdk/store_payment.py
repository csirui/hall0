# -*- coding=utf-8 -*-
from _base_._configure_base_ import ConfigureBase

class ConfigureData(ConfigureBase):

    def __init__(self):
        super(ConfigureData, self).__init__()
        self.default_category = ('CAT_DUANDAI', 'CAT_DUANYAN', 'CAT_THIRDPAY', 'CAT_ALIPAY', 'CAT_DEBIT_CARD', 'CAT_CREDIT_CARD', 'CAT_PHONECHARGE_CARD', 'CAT_JUNNET_CARD')
        self.more_categories = ('CAT_LIST_TUYOU' , 'CAT_LIST_360' , 'CAT_LIST_360_DEZHOU')
    
    def get_info(self):
        return {'name' : '商城支付'}

    def verify_editor_data(self, datas):
        from tymanager.managers.productdefmgr import ProductDefMgr
        errors = []
        # TODO 简单的处理客户端的数据类型
        store_list = datas['store']
        payment_dic = datas['payment']
        for idx in xrange(len(store_list)) :
            store_list[idx]['displayName'] = self.data_str(store_list[idx], 'displayName')
            store_list[idx]['visible'] = self.data_int(store_list[idx], 'visible')
            #校验商品ID合法性
            products = store_list[idx]['products']
            for eachid in products :
                if not ProductDefMgr.is_valid_productid(eachid) :
                    errors.append('store productid = %s, not define' % eachid)
            
        #校验充值类别
        payment_dic['more_categories'] = self.data_str(payment_dic, 'more_categories')
        if payment_dic['more_categories'] not in self.more_categories :
            errors.append('%s not in more_categories: %s' % (payment_dic['more_categories'], self.more_categories))
        
        default_cat = payment_dic['default_category']    
        for idx in xrange(len(default_cat)):
            default_cat[idx]['category'] = self.data_str(default_cat[idx], 'category')
            if default_cat[idx]['category'] not in self.default_category :
                errors.append('%s not in default_category: %s' % (default_cat[idx]['category'], self.default_category))
                
            if not ProductDefMgr.is_valid_productid(default_cat[idx]['id']) :
                errors.append('payment productid = %s, not define' % default_cat[idx]['id'])
                
        return errors

    def generate_redis_datas(self, datas, redisdata):
        is360 = '360' in datas['payment']['more_categories']
        for cat in datas['payment']['default_category']:
            if cat['id'][6] == 'R' and cat['id'][-2:] != 'DJ':
                cat['is_diamond'] = 1
            if is360:
                if cat['category'] == 'CAT_ALIPAY':
                    cat['paytype'] = '360.ali'
                elif cat['category'] == 'CAT_DEBIT_CARD':
                    cat['paytype'] = '360.card1'
                elif cat['category'] == 'CAT_CREDIT_CARD':
                    cat['paytype'] = '360.card2'
                elif cat['category'] == 'CAT_PHONECHARGE_CARD':
                    cat['paytype'] = ['360.card.yd', '360.card.lt', '360.card.dx']
            else: # is tuyoo
                if cat['category'] == 'CAT_ALIPAY':
                    cat['paytype'] = 'tuyou.ali'
                elif cat['category'] == 'CAT_DEBIT_CARD':
                    cat['paytype'] = 'yee2.card1'
                elif cat['category'] == 'CAT_CREDIT_CARD':
                    cat['paytype'] = 'yee2.card2'
                elif cat['category'] == 'CAT_PHONECHARGE_CARD':
                    cat['paytype'] = ['tuyou.card.yd', 'tuyou.card.lt', 'tuyou.card.dx']

        redisdata.add('global:store_payment', datas)

