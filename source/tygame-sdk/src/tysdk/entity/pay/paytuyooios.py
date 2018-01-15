# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''

from tyframework.context import TyContext


class TuYouPayMyIos(object):
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        TyContext.ftlog.info('TuYouPayMyIos->doBuyStraight in args=', params)
        prodId = params['prodId']
        clientId = params['clientId']
        appId = params['appId']
        products = []
        if clientId != '':
            products = TyContext.Configure.get_game_item_json(str(appId) + ':' + str(clientId), 'products')
        if products == None:
            products = TyContext.Configure.get_game_item_json(appId, 'products')
        if products == None:
            products = []
        # TyContext.ftlog.info('TuYouPayMyIos->doBuyStraight in products=', products)        
        payCode = ''
        orderProdName = ''
        for x in xrange(len(products)):
            if len(products[x]) > 3 and products[x][3] == prodId:
                payCode = products[x][0]
                orderProdName = products[x][1]
                break

        payData = {'msgOrderCode': payCode, 'orderProdName': orderProdName}
        params['payData'] = payData
        mo.setResult('payData', payData)
