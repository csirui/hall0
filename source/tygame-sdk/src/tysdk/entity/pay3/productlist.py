# -*- coding=utf-8 -*-


from tyframework.context import TyContext
from tysdk.entity.pay3.diamondlist import TuyouPayDiamondList


class TuyouPayProductList(object):
    @classmethod
    def productlist(cls, mi):
        appId = mi.getParamInt('appId')
        clientId = mi.getParamStr('clientId')
        productlist = cls.productlist2(appId, clientId)
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('productlist')
        mo.setResult('products', productlist)
        return mo

    @classmethod
    def productlist2(cls, appId, clientId):
        # 目前SDK取商品列表校验，采用取配置信息内容
        # 后期可以采用重GAME服务查询的方式获得
        products = TuyouPayDiamondList._get_pay_products_list_(appId, clientId, 'products-v2', clientId)
        TyContext.ftlog.info('productlist2->', appId, clientId, products)
        return products

    @classmethod
    def product(cls, appId, clientId, prodId):
        TyContext.ftlog.info('product->', appId, clientId, prodId)
        products = cls.__get_products_config(appId, clientId)
        found = None
        for x in xrange(len(products)):
            product = products[x]
            if prodId == product['id']:
                found = product
                break
        return found

    @classmethod
    def __get_products_config(cls, appId, clientId):
        productconfs = TyContext.Configure.get_game_item_json(appId, 'products-v2', [])
        products = None
        for x in xrange(len(productconfs) - 1, -1, -1):
            productconf = productconfs[x]
            clientIds = productconf['clientIds']
            if TyContext.strutil.reg_matchlist(clientIds, clientId):
                products = productconf['products']
                TyContext.ftlog.debug('__get_products_config->', clientId, 'matches', clientIds, 'get', products)
                break
        return products
