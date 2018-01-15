# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''

from tyframework.context import TyContext
from tysdk.entity.pay3.diamondlist import TuyouPayDiamondList


class TuYouPayMyIos(object):
    @classmethod
    def get_pay_ios_product(cls, appId, prodId, clientId, checkIdKey):
        TyContext.ftlog.debug('xitontong,here!')
        products = TuyouPayDiamondList._get_pay_products_list_(appId, clientId, 'ios-products-v2', clientId)
        if products is None:
            TyContext.ftlog.error('get_pay_ios_product products not found ! appId=', appId, 'prodId=', prodId,
                                  'clientId=', clientId, 'checkIdKey=', checkIdKey)
            return None
        for x in xrange(len(products)):
            if products[x][checkIdKey] == prodId:
                TyContext.ftlog.debug('get_pay_ios_product the ios pay product appId=', appId, 'prodId=', prodId,
                                      'clientId=', clientId, 'checkIdKey=', checkIdKey, 'product=', products[x])
                return products[x]
        TyContext.ftlog.error('get_pay_ios_product the ios pay product not found ! appId=', appId, 'prodId=', prodId,
                              'clientId=', clientId, 'checkIdKey=', checkIdKey)
        return None

    @classmethod
    def get_pay_ios_product_new(cls, appId, prodId, clientId, checkIdKey, *args, **kw):
        iosConfig = TyContext.Configure.get_global_item_json('ios-products-v2', {})
        appIdConfig = iosConfig.get(str(appId))
        if not appIdConfig:
            TyContext.ftlog.error('get_pay_ios_product the ios pay product not found ! appId=', iosConfig, \
                                  appId, 'prodId=', prodId, 'clientId=', clientId, 'checkIdKey=', checkIdKey)
            # return None
            return cls.get_pay_ios_product(appId, prodId, clientId, checkIdKey)
        packageName = kw.get('packageName')
        products = None
        appIdConfig = filter(lambda x: x.has_key('clientIds'), appIdConfig)
        clientIdConfig = filter(lambda x: x["clientIds"] and TyContext.strutil.reg_matchlist(x["clientIds"], clientId),
                                appIdConfig)
        if not clientIdConfig:
            TyContext.ftlog.debug("can not find IOS products by clientId:", clientId)
        else:
            products = clientIdConfig[0]['products']
        if not products and packageName:
            appIdConfig = filter(lambda x: x.has_key('package_name'), appIdConfig)
            productConfig = filter(lambda x: x['package_name'] == packageName, appIdConfig)
            if not productConfig:
                TyContext.ftlog.debug("can not find IOS products by packageName")
            else:
                products = productConfig[0]['products']
        if not products:
            # return None
            return cls.get_pay_ios_product(appId, prodId, clientId, checkIdKey)
        else:
            productList = filter(lambda x: x[checkIdKey] == prodId, products)
            if not productList:
                return cls.get_pay_ios_product(appId, prodId, clientId, checkIdKey)
            else:
                TyContext.ftlog.debug("OK,Finded IOS products:", productList)
                return productList[0]

    @classmethod
    def charge_data(cls, chargeinfo):
        TyContext.ftlog.debug(cls.__name__, 'charge_data->chargeinfo', chargeinfo)
        buttonId = chargeinfo['buttonId']
        clientId = chargeinfo['clientId']
        appId = chargeinfo['appId']
        userId = chargeinfo['uid']
        product = None
        packageName = chargeinfo['packageName']
        product = cls.get_pay_ios_product_new(appId, buttonId, clientId, 'tyid', packageName=packageName)

        if not product:
            raise Exception('the ios pay code not found ! userId=' + str(userId)
                            + ' appId=' + str(appId) + ' buttonId=' + str(buttonId)
                            + ' clientId=' + str(clientId))
        payCode = product['iosid']
        orderProdName = product['name']
        chargeinfo['chargeData'] = {'orderIosCode': payCode,
                                    'orderProdName': orderProdName}
