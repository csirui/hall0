# -*- coding=utf-8 -*-
'''
Created on 2015年6月10日

@author: zqh
'''
from tyframework.context import TyContext
from tyframework.orderids import orderid


class HttpTestOrder(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/_testorder_make_id': cls.doMakeOrderId,
                '/_testorder_get_short_id': cls.doGetShortOrderId,
                '/_testorder_get_long_id': cls.doGetLongOrderId
            }
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
            }
        return cls.HTMLPATHS

    def __init__(self):
        pass

    @classmethod
    def doMakeOrderId(self, rpath):
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        orderIdVer62 = TyContext.RunHttp.getRequestParam('orderIdVer62', '')
        httpcallback = TyContext.RunHttp.getRequestParam('httpcallback', None)
        assert (appId > 0)
        assert (isinstance(orderIdVer62, basestring))
        assert (len(orderIdVer62) == 1)
        assert (isinstance(httpcallback, basestring))
        assert (httpcallback.find('http://') == 0)

        oid = orderid.make_order_id(appId, orderIdVer62, httpcallback, True)
        return {'orderPlatformId': oid}

    @classmethod
    def doSetOrderIdCallBack(self, rpath):
        orderId = TyContext.RunHttp.getRequestParam('orderId', '')
        httpcallback = TyContext.RunHttp.getRequestParam('httpcallback', None)
        assert (isinstance(orderId, basestring))
        assert (len(orderId) > 1)
        assert (isinstance(httpcallback, basestring))
        assert (httpcallback.find('http://') == 0)
        orderId = orderid.set_order_id_callback(orderId, httpcallback)
        return {'orderPlatformId': orderId}

    @classmethod
    def doGetShortOrderId(self, rpath):
        orderPlatformId = TyContext.RunHttp.getRequestParam('orderPlatformId', '')
        oid = orderid.get_short_order_id(orderPlatformId)
        return {'sortOrderPlatformId': oid}

    @classmethod
    def doGetLongOrderId(self, rpath):
        sortOrderPlatformId = TyContext.RunHttp.getRequestParam('sortOrderPlatformId', '')
        oid = orderid.get_long_order_id(sortOrderPlatformId)
        return {'orderPlatformId': oid}
