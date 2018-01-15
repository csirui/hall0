# -*- coding=utf-8
'''
Created on 2015年6月3日

@author: zhaoqh
'''
import re

from datetime import datetime

orderIdVer1 = 'a'  # Decimal62.tostr62(10, 1)  # a
consumeOrderIdVer1 = 'b'  # Decimal62.tostr62(11, 1)  # b
orderIdVer3 = 'c'  # Decimal62.tostr62(12, 1)  # c
consumeOrderIdVer3 = 'd'  # Decimal62.tostr62(13, 1)  # d
danjiOrderIdVer3 = 'f'  # Decimal62.tostr62(15, 1)  # f
smsBindOrderIdVer3 = 's'  # Decimal62.tostr62(13, 1)  # d
changTianYouOrderIdVer3 = 'y'  # Decimal62.tostr62(13, 1)  # d
orderIdVer4 = 'e'  # Decimal62.tostr62(12, 1)  # e


def is_valid_orderid_str(orderid):
    return re.match(r'^[a-zA-Z0-9]{14}', orderid)


def trim_order_id(orderId):
    if len(orderId) == 14:
        return orderId.lower()
    return orderId[0:14].lower()


def get_appid_frm_order_id(orderId):
    # a00111x54Lq00l
    # apiVer, appId, seq
    _, appId = get_order_id_info(orderId)
    return appId


def get_order_id_info(orderId):
    from tyframework.context import TyContext
    # a00111x54Lq00l
    apiVer, appId = '0', 0
    try:
        apiVer = orderId[0]
        try:
            appId = int(orderId[1:5], 16)
        except:
            TyContext.ftlog.exception('orderId=', orderId)
    except:
        TyContext.ftlog.exception('orderId=', orderId)
    return apiVer, appId


def makeConsumeOrderIdV3(userId, appId, clientId):
    return make_order_id(appId, consumeOrderIdVer3)


def makeChargeOrderIdV3(userId, appId, clientId):
    return make_order_id(appId, orderIdVer3)


def makeChargeOrderIdV4(userId, appId, clientId):
    return make_order_id(appId, orderIdVer4)


def makeSmsBindOrderIdV3(userId, appId, clientId):
    return make_order_id(appId, smsBindOrderIdVer3)


def makeChangTianYouOrderIdV3(userId, appId, clientId):
    return make_order_id(appId, changTianYouOrderIdVer3)


def makePlatformOrderIdV1(userId, params):
    appId = int(params['appId'])
    return make_order_id(appId, orderIdVer1)


def makeGameOrderIdV1(userId, params):
    appId = int(params['appId'])
    return make_order_id(appId, consumeOrderIdVer1)


def _httpOnlieGateWay(orderIdVer62='', isRemote=False):
    from tyframework.context import TyContext
    gs = TyContext.Configure.get_game_item_json(9998, 'http_gateway')
    if TyContext.TYGlobal.mode() == 1 or isRemote:
        if orderIdVer62 in gs:
            return gs[orderIdVer62]
        return None
    else:
        if orderIdVer62 in gs:
            return gs[orderIdVer62]
        return gs['default']


def set_order_id_callback(orderId, httpcallback):
    # 记录单号回应的回调地址
    from tyframework.context import TyContext
    TyContext.RedisMix.execute('HSET', 'global.orderid.callback', orderId, httpcallback)
    return orderId


def make_order_id(appId, orderIdVer62, httpcallback=None, isRemote=False):
    httpgateway = _httpOnlieGateWay(orderIdVer62, isRemote)
    from tyframework.context import TyContext
    if not httpgateway:
        appId = int(appId)
        seqNum = TyContext.RedisMix.execute('INCR', 'global.orderid.seq.' + orderIdVer62)
        ct = datetime.now()
        dd = ct.strftime('%d')
        # orderId构成:<1位API版本号>+<4位APPID>+DD+<5位序号>，共14位
        a = hex(appId)[2:][-4:]
        a = '0' * (4 - len(a)) + a
        b = hex(seqNum)[2:][-7:]
        b = '0' * (7 - len(b)) + b
        oid = orderIdVer62 + a + dd + b
        # 记录单号回应的回调地址
        if httpcallback != None and isinstance(httpcallback, (str, unicode)) and httpcallback.find('http://') == 0:
            set_order_id_callback(oid, httpcallback)
        return oid
    else:
        # 通知订单数据中心(线上GATEWAY服务), 产生了一个新订单, 需要进行 单号<->回调服务的记录
        httpurl = httpgateway + '/_testorder_make_id'
        datas = {
            'appId': appId,
            'orderIdVer62': orderIdVer62,
            'httpcallback': TyContext.TYGlobal.http_sdk()
        }
        result, _ = TyContext.WebPage.webget_json(httpurl, datas, None)
        return result['orderPlatformId']


def getOrderIdHttpCallBack(orderId):
    from tyframework.context import TyContext
    # 取得单号对应的callback地址, 如果没有Name意味就是本机线上服务单号
    orderId = trim_order_id(orderId)
    httpcallback = TyContext.RedisMix.execute('HGET', 'global.orderid.callback', orderId)
    if httpcallback != None and isinstance(httpcallback, (str, unicode)) and httpcallback.find('http://') == 0:
        nsize = TyContext.RedisMix.execute('HLEN', 'global.orderid.callback')
        if nsize > 10000:
            TyContext.RedisMix.execute('DEL', 'global.orderid.callback')
            TyContext.ftlog.error('the test order "global.orderid.callback" too much (> 10000) !! ' +
                                  'auto clean up !! some test order maybe callback to online !' +
                                  'this is not an error, just a warring !!')
        return httpcallback
    return TyContext.TYGlobal.http_sdk_inner()


def is_short_order_id_format(shortOrderId):
    if isinstance(shortOrderId, int):
        if len(str(shortOrderId)) == 6:
            return True
    elif isinstance(shortOrderId, (str, unicode)):
        if len(shortOrderId) == 6:
            try:
                shortOrderId = int(shortOrderId)
                return True
            except:
                pass
    return False


def get_short_order_id(orderPlatformId):
    from tyframework.context import TyContext
    if TyContext.TYGlobal.mode() == 1:
        # 若是线上正式服, 那么再mix库中生成短单号
        shortOrderId = TyContext.RedisMix.execute('INCR', 'global.orderid.seq.sort')
        shortOrderId = str(100000 + shortOrderId)[-6:]
        TyContext.RedisMix.execute('HSET', 'sort.orderid.map', shortOrderId, orderPlatformId)
        return shortOrderId
    else:
        # 若是测试服务, 那么调用正式服远程API生成单号
        httpurl = _httpOnlieGateWay() + '/_testorder_get_short_id'
        datas = {
            'orderPlatformId': orderPlatformId
        }
        result, _ = TyContext.WebPage.webget_json(httpurl, datas, None)
        return result['sortOrderPlatformId']


def get_long_order_id(shortOrderId):
    from tyframework.context import TyContext
    if not is_short_order_id_format(shortOrderId):
        return shortOrderId

    if TyContext.TYGlobal.mode() == 1:
        # 若是线上正式服, 那么重mix库中取得长单号
        orderPlatformId = TyContext.RedisMix.execute('HGET', 'sort.orderid.map', shortOrderId)
        return str(orderPlatformId)
    else:
        # 若是测试服务, 那么调用正式服远程API取得长单号
        httpurl = _httpOnlieGateWay() + '/_testorder_get_long_id'
        datas = {
            'sortOrderPlatformId': shortOrderId
        }
        result, _ = TyContext.WebPage.webget_json(httpurl, datas, None)
        return result['orderPlatformId']
