# -*- coding=utf-8 -*-
import copy
import datetime
import json

from charge import TuyouPayCharge
from diamondlist import TuyouPayDiamondList
from tyframework.context import TyContext
from tysdk.entity.pay3.consume_conf import TuyouPayConsumeConf
from tysdk.entity.pay_common.orderlog import Order


def tasklet_sleep(seconds):
    from twisted.internet import reactor
    import stackless
    channel = stackless.channel()
    reactor.callLater(seconds, channel.send, 0)
    channel.receive()


def _check_prod_price(mi):
    try:
        prodId = mi.getParamStr('prodId')
        prodPrice = mi.getParamFloat('prodPrice')

        defPrice = -1
        if prodId.startswith("TY"):
            lpid = len(prodId)
            if lpid >= 12:
                if prodId[6] == 'D' or prodId[6] == 'R':
                    defPrice = float(prodId[7:12])
        if defPrice >= 0:
            if prodPrice < defPrice * 0.8:
                TyContext.ftlog.info('CHECK_PROD_PRICE ERROR prodId=', prodId, 'defPrice=', defPrice, 'prodPrice=',
                                     prodPrice, mi)
                mo = TyContext.Cls_MsgPack()
                mo.setCmd('consume')
                mo.setError(2, '商品信息错误，请重新购买')
                return mo
            else:
                TyContext.ftlog.info('CHECK_PROD_PRICE OK prodId=', prodId, 'defPrice=', defPrice, 'prodPrice=',
                                     prodPrice, mi)
        else:
            TyContext.ftlog.info('CHECK_PROD_PRICE NG prodId=', prodId, 'defPrice=', defPrice, 'prodPrice=', prodPrice,
                                 mi)
    except Exception, e:
        TyContext.ftlog.error('CHECK_PROD_PRICE', e)
    return None


class TuyouPayConsume(object):
    __consume_ext_diamond_funs__ = {}

    @classmethod
    def consume(cls, mi):
        userId = mi.getParamInt('userId')
        authorCode = mi.getParamStr('authorCode')
        appId = mi.getParamInt('appId')
        clientId = mi.getParamStr('clientId')
        appInfo = mi.getParamStr('appInfo')
        prodId = mi.getParamStr('prodId')
        prodName = mi.getParamStr('prodName')
        prodCount = mi.getParamInt('prodCount')
        prodPrice = mi.getParamInt('prodPrice')
        # 用于第三方应用（appId>10000）传递游戏订单号。途游的游戏不用传或传空串
        prodOrderId = mi.getParamStr('prodOrderId')
        mustcharge = mi.getParamInt('mustcharge')
        clientPayType = mi.getParamStr('payType')
        packageName = mi.getParamStr('packageName', '')
        channelName = mi.getParamStr('channelName', '')
        # example "payInfo": {"appid": {"ydmm": "300008410694"}}
        payInfo = mi.getParamStr('payInfo')
        if payInfo:
            payInfo = TyContext.strutil.loads(payInfo, decodeutf8=True)

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('consume')

        m2 = _check_prod_price(mi)
        if m2 != None:
            return m2

        #         # 取得道具的配置PRICE
        #         appProdPrice = -1
        #         appProducts = TuyouPayProductList.productlist2(appId, clientId)
        #         for x in xrange(len(appProducts)):
        #             product = appProducts[x]
        #             if prodId == product['id'] :
        #                 appProdPrice = int(product['price'])
        #                 break
        #         if prodPrice <= 0 or appProdPrice <= 0 or appProdPrice != prodPrice :
        #             mo.setError(2, '商品信息错误，请重新购买')
        #             return mo

        # 取得当前用户的COIN
        userCoin = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'diamond')
        if isinstance(userCoin, (int, float)):
            userCoin = int(userCoin)
        else:
            userCoin = 0

        TyContext.ftlog.info('consume->appId=', appId, 'clientId=', clientId, 'userId=', userId, 'userCoin=', userCoin,
                             'prodPrice=', prodPrice, 'prodId=', prodId, 'prodName=', prodName, 'prodCount=', prodCount,
                             'prodOrderId=', prodOrderId, 'mustcharge=', mustcharge, 'clientPayType', clientPayType,
                             'payInfo=', payInfo)

        if prodCount <= 0:
            prodCount = 1
        else:
            prodCount = int(prodCount)

        # if prodCount != 1 :
        #    mo.setError(2, '商品信息错误，请重新购买')
        #    return mo

        prodPrice = int(prodPrice)
        consumeCoin = int(prodPrice * prodCount)
        if not consumeCoin:
            mo.setError(2, '商品价格信息错误，请检查')
            return mo

        fail, prodOrderId = cls._create_consume_transaction(
            appId, appInfo, clientId, userId, consumeCoin, prodId, prodPrice,
            prodCount, prodName, prodOrderId, mo)
        if fail:
            return mo

        if mustcharge == 1 or userCoin < consumeCoin:
            cls.__consume_charge__(
                appId, appInfo, clientId, userId, authorCode, consumeCoin, prodId,
                prodPrice, prodCount, prodName, prodOrderId, mustcharge,
                clientPayType, payInfo, mo, packageName=packageName, channelName=channelName)
        else:
            cls.__consume_user_coin__(
                appId, appInfo, clientId, userId, consumeCoin, prodId, prodPrice,
                prodCount, prodName, prodOrderId, mo)
        return mo

    @classmethod
    def __get_extra_delivery(cls, charge_info):
        found = None
        try:
            TyContext.ftlog.debug('__get_extra_delivery charge_info:', charge_info)
            categories = charge_info['chargeCategories']
            paytype = charge_info['chargeType']
            for cat in categories:
                _paytype = cat['paytype']
                if paytype == _paytype or paytype in _paytype:
                    found = cat['extra_deliver']
                    break
        finally:
            TyContext.ftlog.debug('__get_extra_delivery: extra_deliver', found)
            return found

    @classmethod
    def _create_consume_transaction(cls, appId, appInfo, clientId, userId,
                                    consumeCoin, prodId, prodPrice, prodCount, prodName, prodOrderId, mo):

        if appId > 10000:
            # 其他第三方游戏，如果未携带事务ID，缺省为-
            if not prodOrderId or len(prodOrderId) <= 0:
                prodOrderId = '-'
            return False, prodOrderId

        prodOrderId = TyContext.ServerControl.makeConsumeOrderIdV3(userId, appId, clientId)
        control = TyContext.ServerControl.findServerControl(appId, clientId)
        try:
            consumeUrl = control['http'] + '/v2/game/consume/transaction'
        except:
            mo.setError(3, '系统服务配置错误')
            return True, prodOrderId

        params = ['appId', appId, 'clientId', clientId, 'userId', userId,
                  'prodPrice', prodPrice, 'prodId', prodId, 'prodCount', prodCount,
                  'prodOrderId', prodOrderId]
        datas, _ = TyContext.WebPage.webget_json(consumeUrl, params)
        try:
            mo.setError(5, datas['error']['info'])
            return True, prodOrderId
        except:
            if prodOrderId != datas['result']['prodOrderId']:
                mo.setError(4, '系统错误，无法建立商品购买事务')
                return True, prodOrderId

        return False, prodOrderId

    @classmethod
    def __consume_user_coin__(cls, appId, appInfo, clientId, userId, consumeCoin,
                              prodId, prodPrice, prodCount, prodName, prodOrderId,
                              mo, chargeInfo=None):
        # 获取服务配置
        deliveryUrl = None
        control = TyContext.ServerControl.findServerControl(appId, clientId)
        if appId < 10000:
            # 途游自己的游戏，固定的投递地址
            # control = TyContext.ServerControl.findServerControl(appId, clientId)
            # if control :
            deliveryUrl = control['http'] + '/v2/game/consume/delivery'
        else:
            deliveryUrl = TyContext.Configure.get_game_item_str(appId, 'deliveryUrl', '')
        appKey = TyContext.Configure.get_game_item_str(appId, 'appKey', '')
        if not appKey:
            gameConfig = TyContext.Configure.get_game_item_json(appId, 'game')
            appKey = gameConfig.get('appKey', '')
            deliveryUrl = gameConfig.get('deliveryUrl', '')
            isErrorNotify = gameConfig.get('isErrorNotify', '')
        TyContext.ftlog.debug('__consume_user_coin__ deliveryUrl=', deliveryUrl, 'appKey=', appKey)
        if not deliveryUrl or not appKey or len(deliveryUrl) == 0 or len(appKey) == 0:
            TyContext.ftlog.error('__consume_user_coin__ deliveryUrl or appKey error')
            mo.setError(3, '系统服务配置错误,缺少回调地址')
            if chargeInfo:
                Order.log(chargeInfo['platformOrderId'], Order.INTERNAL_ERR,
                          userId, appId, clientId, info='consume delivery cfg err')
            return True

        # 取得唯一事物ID
        consumeId = TyContext.ServerControl.makeConsumeOrderIdV3(userId, appId, clientId)

        ct = datetime.datetime.now()
        timestamp = ct.strftime('%Y-%m-%d %H:%M:%S')
        paykey = ct.strftime('sdk.consume:%Y%m%d')
        consumeinfo = {'time': timestamp,
                       'uid': userId,
                       'appId': appId,
                       'name': prodName,
                       'fee': consumeCoin,
                       'clientId': clientId,
                       'appOrderId': prodOrderId,
                       'prodId': prodId,
                       'consumeId': consumeId
                       }
        params = {'userId': userId, 'orderId': prodOrderId, 'consumeCoin': consumeCoin,
                  'appId': appId, 'appInfo': appInfo, 'clientId': clientId,
                  'prodPrice': prodPrice, 'prodId': prodId, 'prodCount': prodCount,
                  'consumeId': consumeId, 'apiver': '2'
                  }
        if chargeInfo:
            if 'chargeType' in chargeInfo and appId < 10000:
                params['chargeType'] = chargeInfo['chargeType']
            params['platformOrder'] = chargeInfo['platformOrderId']
            params['chargedRmbs'] = chargeInfo['chargedRmbs']
            params['chargedDiamonds'] = chargeInfo['chargedDiamonds']
            if 'cpExtInfo' in chargeInfo and chargeInfo['cpExtInfo']:
                params['cpExtInfo'] = chargeInfo['cpExtInfo']
        # modified by zhangshibo at 2015-09-09，标识是优易付会员订阅
        if mo.getParam('is_monthly'):
            params['is_monthly'] = '1'
        # end modify

        extra_delivery = cls.__get_extra_delivery(chargeInfo)
        if extra_delivery is not None:
            params['extra_deliver'] = extra_delivery

        # 首先扣除三方钻石
        ok = cls.__consume_ext_diamond__(params, False)
        if not ok:
            mo.setError(8, '三方钻石扣款失败')
            TyContext.ftlog.error('__consume_user_coin__ consume ext diamond '
                                  'ERROR: paykey', paykey, 'consumeinfo', consumeinfo)
            if chargeInfo:
                Order.log(chargeInfo['platformOrderId'], Order.INTERNAL_ERR,
                          userId, appId, clientId, info='third party consume diamond err')
            return True

        # 扣除钻石
        # leftCoin = TyContext.RedisUser.execute(userId, 'HINCRBY', 'user:' + str(userId), 'diamond', -consumeCoin)
        delta, leftCoin = TyContext.UserProps.incr_diamond(int(userId), int(appId), -consumeCoin,
                                                           TyContext.ChipNotEnoughOpMode.NOOP,
                                                           TyContext.BIEventId.UNKNOWN)
        TyContext.BiReport.diamond_update(appId, userId, -consumeCoin, leftCoin, 'sdk.pay.v3.consume')
        if delta != -consumeCoin:
            TyContext.ftlog.error('__consume_user_coin__ diamond update error')
            # leftCoin = TyContext.RedisUser.execute(userId, 'HINCRBY', 'user:' + str(userId), 'diamond', consumeCoin)
            # TyContext.BiReport.diamond_update(appId, userId, consumeCoin, leftCoin, 'sdk.pay.v3.consume.cancel')
            mo.setError(4, '购买太频繁，请稍后购买')
            mo.setResult('leftCoin', leftCoin)
            mo.setResult('needCoin', consumeCoin)
            if chargeInfo:
                Order.log(chargeInfo['platformOrderId'], Order.INTERNAL_ERR,
                          userId, appId, clientId, info='deduct diamond err')
            return True

        # 记录全局消费记录
        consumeinfo = json.dumps(consumeinfo)
        TyContext.ftlog.info('__consume_user_coin__ consumeinfo', paykey, consumeinfo)
        TyContext.RedisPayData.execute('LPUSH', paykey, consumeinfo)

        mo.setResult('time', timestamp)
        mo.setResult('userId', userId)
        mo.setResult('orderId', prodOrderId)
        mo.setResult('consumeCoin', consumeCoin)
        mo.setResult('appId', appId)
        mo.setResult('appInfo', appInfo)
        mo.setResult('clientId', clientId)
        mo.setResult('prodPrice', prodPrice)
        mo.setResult('prodId', prodId)
        mo.setResult('prodCount', prodCount)
        mo.setResult('leftCoin', leftCoin)

        # 投递货物
        if deliveryUrl == 'http://none':
            response = 'success'
            httpurl = deliveryUrl
        else:
            retry_sleeps = [3, 10, 60, 600, 3600, 36000]
            for wait in retry_sleeps:
                try:
                    response, httpurl = TyContext.WebPage.webget(deliveryUrl, params, appKey)
                    break
                except Exception, e:
                    TyContext.ftlog.error('__consume_user_coin__ failed deliver product to', deliveryUrl, 'error:', e)
                    tasklet_sleep(wait)

        if 'success' == response:
            TyContext.ftlog.info('__consume_user_coin__ transaction ok', paykey, consumeinfo)
            if chargeInfo:
                Order.log(chargeInfo['platformOrderId'], Order.DELIVER_OK,
                          userId, appId, clientId, prodOrderId=prodOrderId,
                          shortId=chargeInfo.get('shortDiamondOrderId', 'na'),
                          diamondid=chargeInfo.get('diamondId', 'na'),
                          charge_price=chargeInfo.get('chargeTotal', 'na'),
                          paytype=chargeInfo.get('chargeType', 'na'),
                          prodid=prodId, prod_price=prodPrice)
        else:
            if chargeInfo:
                Order.log(chargeInfo['platformOrderId'], Order.DELIVER_FAIL,
                          userId, appId, clientId, info='prod delivery err',
                          prodOrderId=prodOrderId,
                          shortId=chargeInfo.get('shortDiamondOrderId', 'na'),
                          diamondid=chargeInfo.get('diamondId', 'na'),
                          charge_price=chargeInfo.get('chargeTotal', 'na'),
                          prodid=prodId, prod_price=prodPrice)
            mo.setError(5, '钻石扣款成功，商品投递失败')
            TyContext.ftlog.error('__consume_user_coin__ transaction ERROR', response, paykey, consumeinfo)
            # 回滚扣除三方钻石
            ok = cls.__consume_ext_diamond__(params, True)
            if not ok:
                TyContext.ftlog.error('__consume_user_coin__ transaction ERROR: cancel_consume_ext_diamond failed')
        # 结束事务
        return True

    @classmethod
    def _patch_ios_client_bug(cls, clientId, diamondlist):
        if 'IOS_3' not in clientId:
            return diamondlist
        castrated = copy.deepcopy(diamondlist)
        for i in xrange(len(castrated)):
            diamond = castrated[i]
            if diamond['id'] == 'TY9999R0003001':
                del castrated[i]
                break
        return castrated

    @classmethod
    def __consume_charge__(cls, appId, appInfo, clientId, userId, authorCode,
                           consumeCoin, prodId, prodPrice, prodCount, prodName,
                           prodOrderId, mustcharge, clientPayType, payInfo, mo, **kwds):
        # 取得钻石列表，自动匹配可购买的钻石项目
        diamondlist = TuyouPayDiamondList.diamondlist2(appId, clientId)
        if not diamondlist:
            TyContext.ftlog.error('__consume_charge__ diamondlist ERROR', appId, clientId)
            mo.setError(6, '钻石列表配置错误')
            return True

        ios_patch = TyContext.Configure.get_global_item_int('patch_ios_bug_TY9999R0003001', 1)
        if ios_patch:
            diamondlist = cls._patch_ios_client_bug(clientId, diamondlist)

        diamond = None
        if mustcharge == 1:
            count = prodPrice
            price = count / 10 if count >= 10 else count / 10.0
            diamond = {'id': prodId, 'count': count, 'price': price, 'name': prodName}
        else:
            for diamond in diamondlist:
                count = diamond['count']
                if count >= consumeCoin:
                    break
            else:
                TyContext.ftlog.error('__consume_charge__ find charge diamond ERROR', appId, clientId, consumeCoin,
                                      diamondlist)
                mo.setError(7, '钻石项目取得失败')
                return True

        consumeinfo = {
            'appId': appId,
            'appInfo': appInfo,
            'clientId': clientId,
            'userId': userId,
            'consumeCoin': consumeCoin,
            'prodId': prodId,
            'prodPrice': prodPrice,
            'prodCount': prodCount,
            'prodName': prodName,
            'prodOrderId': prodOrderId,
            'mustcharge': mustcharge,
        }
        diamondId = diamond['id']
        diamondPrice = diamond['price']
        diamondCount = 1
        diamondName = diamond['name'] if mustcharge != 1 else prodName
        TuyouPayCharge.__charge_begin__(appId, appInfo, clientId, userId,
                                        authorCode, diamondId, diamondPrice, diamondCount,
                                        diamondName, count, mo, consumeinfo, clientPayType, payInfo,
                                        packageName=kwds.get('packageName', ''),
                                        channelName=kwds.get('channelName', ''))
        return True

    @classmethod
    def __consume_ext_diamond__(cls, params, iscancel):
        userId = params['userId']
        appId = params['appId']
        clientId = params['clientId']
        prodId = params['prodId']

        chargeType = TyContext.PayType.get_paytype_by_user(appId, userId, prodId, clientId)
        TyContext.ftlog.debug('__consume_ext_diamond__', chargeType, iscancel)

        cfun = None
        if chargeType in cls.__consume_ext_diamond_funs__:
            cfun = cls.__consume_ext_diamond_funs__[chargeType]
        else:
            if chargeType in TuyouPayConsumeConf.CONSUME_DATA:
                cpath = TuyouPayConsumeConf.CONSUME_DATA[chargeType]
                tks = cpath.split('.')
                mpackage = '.'.join(tks[0:-1])
                clsName = tks[-1]
                clazz = None
                exec 'from %s import %s as clazz' % (mpackage, clsName)
                cfun = getattr(clazz, 'consume_ext_diamond')
                cls.__consume_ext_diamond_funs__[chargeType] = cfun
            else:
                cls.__consume_ext_diamond_funs__[chargeType] = None
        isOK = True
        if cfun:
            try:
                isOK = cfun(params, iscancel)
            except:
                isOK = False
                TyContext.ftlog.exception()
        TyContext.ftlog.debug('__consume_ext_diamond__', isOK, cfun)
        return isOK
