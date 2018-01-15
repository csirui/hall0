#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class ChargeConfigure(object):
    @classmethod
    def list_configure_key(cls, appId, clientId):
        if clientId:
            yield str(appId), clientId
            yield str(appId), clientId.split('_', 1)[0]
        yield (str(appId),)

    @classmethod
    def get_store_payment(cls, prodId, appId, **kwds):
        """
        获取支付方式
        :param prodId:
        :param appId:
        :param channel:
        :return:
        """
        for key in cls.list_configure_key(appId, kwds.get('clientId')):
            store_payment = cls.get_pay_info(prodId, *key)
            if store_payment:
                return store_payment
        # channel_payment = cls.get_pay_info(prodId, channel)
        # for pay_info in channel_payment:
        #    paytype = pay_info['paytype']
        #    # 渠道的支付配置更新产品的配置
        #    for pay_info2 in filter(lambda x:x['paytype'] == paytype, store_payment):
        #        pay_info.update(pay_info2)
        #        break
        #    else:
        #        store_payment.append(pay_info)
        # if channel_payment:
        #    store_payment = channel_payment
        #    return store_payment
        return []

    @classmethod
    def get_prod_dict(cls, appId, **kwds):
        prod_list = []
        for key in cls.list_configure_key(appId, kwds.get('clientId')):
            prod_list = TyContext.Configure.get_global_item_json('universal:items:%s' % ':'.join(key))
            if prod_list:
                break
        return dict([(x['id'], x) for x in prod_list])

    @classmethod
    def get_cpExt_info(cls, prodId, appId, **kwds):
        """
        获取 该支付方式的cp信息
        :param prodId:
        :param appId:
        :param channel:
        :param kwds:
        :return:
        """
        payment_list = cls.get_store_payment(prodId, appId, **kwds)
        chargeType = kwds.get('chargeType')
        payment = filter(lambda x: x['paytype'] == chargeType, payment_list)
        cpInfo = {}
        if payment:
            try:
                cpExtInfo = payment[0]['cpExtInfo']
            except:
                cpExtInfo = ""
                TyContext.ftlog.debug("get_cpExtInfo_info,get bouns error!")
        else:
            cpExtInfo = ""
        cpInfo['cpExtInfo'] = cpExtInfo
        return cpInfo

    @classmethod
    def get_prod_info(cls, appId, prodId, **kwds):
        """
        获取商品列表
        :param appId:
        :param prodId:
        :return:
        """
        for key in cls.list_configure_key(appId, kwds.get('clientId')):
            prod_info = TyContext.Configure.get_global_item_json('universal:items:%s' % ':'.join(key))
            if prod_info:
                break
        if prod_info:
            prod_info = filter(lambda x: x['id'] == prodId, prod_info)
            if prod_info:
                return prod_info[-1]
        return None

    @classmethod
    def get_consume_diamond(cls, appId, prodInfo, *args, **kwds):
        for key in cls.list_configure_key(appId, kwds.get('clientId')):
            items = TyContext.Configure.get_global_item_json('universal:items:%s' % ':'.join(key))
            if items:
                break
        diamondList = filter(lambda x: x.get('is_diamond'), items)
        diamondList.sort(lambda x, y: cmp(x['price'], y['price']))
        for diamondInfo in diamondList:
            if prodInfo['diamondPrice'] <= diamondInfo['diamondPrice']:
                return diamondInfo

    @classmethod
    def get_pay_info(cls, prodId, *args):
        """
        获取对应的store_payment配置项
        :param args:
        :return:
        """
        keys = []
        for key in args:
            if isinstance(key, list) or isinstance(key, tuple):
                keys.extend(key)
            else:
                keys.append(key)
        store_payment = None
        while keys and not store_payment:
            store_payment = TyContext.Configure.get_global_item_json('universal:store_payment:%s' % ':'.join(keys))
            if store_payment:
                prod_info = store_payment.get(prodId, store_payment.get('*'))
                if prod_info:
                    return prod_info
            keys = keys[:-1]
        return []

    @classmethod
    def get_third_config(cls, *args):
        key = 'universal:store_payment:%s' % ':'.join(args)
        return TyContext.Configure.get_global_item_json(key)
