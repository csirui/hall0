# -*- coding=utf-8 -*-

# from tyframework.context import TyContext
from tyframework.orderids import orderid

'''
短ID的映射开始时间:2014-6-27，预计循环时间大于一个月
'''


class ShortOrderIdMap(object):
    @classmethod
    def is_short_order_id_format(cls, shortOrderId):
        return orderid.is_short_order_id_format(shortOrderId)

    #         if isinstance(shortOrderId, int) :
    #             if len(str(shortOrderId)) == 6 :
    #                 return True
    #         elif isinstance(shortOrderId, (str, unicode)) :
    #             if len(shortOrderId) == 6 :
    #                 try:
    #                     shortOrderId = int(shortOrderId)
    #                     return True
    #                 except:
    #                     pass
    #         return False


    @classmethod
    def get_short_order_id(cls, orderPlatformId):
        return orderid.get_short_order_id(orderPlatformId)

    #         rdb = getattr(TyContext, 'RedisOnLineMix', None)
    #         if rdb is None :
    #             rdb = TyContext.RedisMix
    #
    #         shortOrderId = rdb.execute('INCR', 'global.orderid.seq.sort')
    #         #XXX this is buggy, when global.orderid.seq.short goes beyond 900000!
    #         # it will result in 0xxxxx short orderid, which will be shorten after
    #         # reading from redis
    #         shortOrderId = str(100000 + shortOrderId)[-6:]
    #         rdb.execute('HSET', 'sort.orderid.map', shortOrderId, orderPlatformId)
    #         TyContext.ftlog.debug('get_short_order_id', shortOrderId, 'for orderPlatformId', orderPlatformId, 'rdb', rdb.address)
    #         return shortOrderId

    @classmethod
    def get_long_order_id(cls, shortOrderId):
        return orderid.get_long_order_id(shortOrderId)

# if cls.is_short_order_id_format(shortOrderId) :
#             rdb = getattr(TyContext, 'RedisOnLineMix', None)
#             if rdb is None :
#                 rdb = TyContext.RedisMix
#             orderPlatformId = rdb.execute('HGET', 'sort.orderid.map', shortOrderId)
#             return str(orderPlatformId)
#         return shortOrderId
