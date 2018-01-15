# -*- coding=utf-8 -*-


from tyframework.context import TyContext


class TuyouPayDiamondList(object):
    @classmethod
    def diamondlist(cls, mi):
        appId = mi.getParamInt('appId')
        clientId = mi.getParamStr('clientId')

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('diamondlist')
        diamondlist = cls.diamondlist2(appId, clientId)
        mo.setResult('diamonds', diamondlist)
        return mo

    @classmethod
    def _diamondlist_from_config_centre(cls, clientId):
        alldiamonds = TyContext.Configure.get_global_item_json('diamonds_superset')
        payconfig = TyContext.Configure.get_global_item_json('store_payment',
                                                             clientid=clientId)
        if not alldiamonds or not payconfig:
            TyContext.ftlog.debug('_diamondlist_from_config_centre-> not '
                                  'alldiamonds or not payconfig', clientId)
            return []

        cats = payconfig['payment']['default_category']
        products = []
        for cat in cats:
            if cat.get('is_diamond', 0):
                for diamond in alldiamonds:
                    if diamond['id'] == cat['id']:
                        products.append(diamond)
        TyContext.ftlog.debug('_diamondlist_from_config_centre->', clientId, products)
        if len(products) == 0:
            TyContext.ftlog.debug('alldiamonds->', alldiamonds)
            TyContext.ftlog.debug('cats->', cats)
        return products

    @classmethod
    def diamondlist2(cls, appId, clientId):
        products = cls._diamondlist_from_config_centre(clientId)
        if products:
            return products

        matchStr = str(appId) + ':' + clientId
        # 全体钻石列表 取配置时使用APPID = 0
        products = cls._get_pay_products_list_(0, clientId, 'products-v2', matchStr)
        TyContext.ftlog.debug('diamondlist2->', appId, clientId, matchStr, products)
        return products

    @classmethod
    def _get_pay_products_list_(cls, appId, clientId, rediskey, matchStr):
        productconfs = TyContext.Configure.get_game_item_json(appId, rediskey, [])
        products = None
        if productconfs:
            for x in xrange(len(productconfs) - 1, -1, -1):
                productconf = productconfs[x]
                clientIds = productconf['clientIds']
                if TyContext.strutil.reg_matchlist(clientIds, matchStr):
                    products = productconf['products']
                    break
        TyContext.ftlog.debug('__get_pay_products_list__->', appId, clientId, rediskey, matchStr, products)
        return products
