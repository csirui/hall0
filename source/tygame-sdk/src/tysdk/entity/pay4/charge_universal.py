#! encoding=utf-8
from copy import deepcopy

from tyframework.context import TyContext
from tysdk.entity.pay3.consume import TuyouPayConsume
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.charge_v3_delegator import ChargeV3Delegator
from tysdk.entity.pay4.decorator import payv4_order
from tysdk.entity.pay4.decorator.payv4_filter import payv4_filter_map
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.strategy.ios_appstore_strategy import TuYooPayIOSAppStoreStrategy

__author__ = 'yuejianqiang'


class ChargeUniversal(object):
    @classmethod
    def charge(cls, mi):
        TyContext.ftlog.info(cls.__name__, 'charge mi', mi)
        mo = TyContext.Cls_MsgPack()
        ###
        userId = mi.getParamInt('userId', 0)
        appId = mi.getParamStr('appId', '9999')
        clientId = mi.getParamStr('clientId')
        ###
        prodId = mi.getParamStr('prodId')
        prodCount = mi.getParamInt('prodCount', 0)
        ###
        tyGameName = mi.getParamStr('tyGameName')
        tySubGameName = mi.getParamStr('tySubGameName')
        tyChannelName = mi.getParamStr('tyChannelName')
        tyVersionName = mi.getParamStr('tyVersionName')  # 3.71
        ###
        prodName = mi.getParamStr('prodName')
        prodPrice = mi.getParamInt('prodPrice', -1)  # 道具价格，单位元
        prodIcon = mi.getParamStr('prodIcon', "")
        # prodOrderId = mi.getParamStr('prodOrderId', '')
        mustcharge = mi.getParamInt('mustcharge', 0)
        # 获取商品信息
        prod_info = ChargeConfigure.get_prod_info(appId, prodId, clientId=clientId)
        if not prod_info:
            mo.setResult('code', 1)
            mo.setResult('info', '未找到对应的商品')
            return mo
        if not prodPrice or prodPrice < 0:
            prodPrice = prod_info['price']
        if not prodCount or prodCount < 0:
            prodCount = 1
        if not prodName:
            prodName = prod_info.get('name', '')
        if not prodIcon:
            prodIcon = prod_info.get('icon', '')

        store_payment = []
        payment_list = ChargeConfigure.get_store_payment(prodId, appId, clientId=clientId)
        for payment in payment_list:
            try:
                chargeType = payment['paytype']
                method = payv4_filter_map[chargeType]
                payment = deepcopy(payment)
                if not method(payment, prod_info, appId=appId, clientId=clientId, userId=userId):
                    continue
            except KeyError:
                pass
            store_payment.append(payment)
        # 过滤328 & 648 商品
        if len(payment_list) > 1 and filter(lambda x: x['paytype'] == 'tuyooios', payment_list):
            strategy = TuYooPayIOSAppStoreStrategy()
            if strategy(appId, userId, prodId):
                store_payment = filter(lambda x: x['paytype'] != 'tuyooios', payment_list)
        ## 完成
        mo.setResult('userId', userId)
        mo.setResult('appId', appId)
        mo.setResult('clientId', clientId)
        mo.setResult('prodId', prodId)
        mo.setResult('prodName', prodName)
        mo.setResult('prodIcon', prodIcon)
        mo.setResult('prodPrice', prodPrice)
        mo.setResult('prodCount', prodCount)
        mo.setResult('mustcharge', mustcharge)
        if store_payment:
            mo.setResult('code', 0)
            mo.setResult('store_payment', store_payment)
        else:
            mo.setResult('code', 1)
            mo.setResult('info', '支付类型未配置')
        mo.setCmd('charge')
        return mo

    @classmethod
    def order(cls, mi):
        chargeType = mi.getParamStr('chargeType')
        try:
            method = payv4_order.payv4_order_map[chargeType]
        except KeyError:
            return ChargeV3Delegator().order(mi)
        try:
            mo = method(mi)
        except PayErrorV4, err:
            return err.mo()
        return mo

    @classmethod
    def consume(cls, mi):
        userId = mi.getParamInt('userId')
        # authorCode = mi.getParamStr('authorCode')
        appId = mi.getParamInt('appId')
        clientId = mi.getParamStr('clientId')
        appInfo = mi.getParamStr('appInfo')
        prodId = mi.getParamStr('prodId')
        # prodName = mi.getParamStr('prodName')
        prodCount = mi.getParamInt('prodCount')
        # prodPrice = mi.getParamInt('prodPrice') # 商品的钻石价格
        # 用于第三方应用（appId>10000）传递游戏订单号。途游的游戏不用传或传空串
        prodOrderId = mi.getParamStr('prodOrderId', '')
        mustcharge = mi.getParamInt('mustcharge')
        clientPayType = mi.getParamStr('payType')
        payInfo = mi.getParamStr('payInfo')
        prodInfo = ChargeConfigure.get_prod_info(appId, prodId, clientId=clientId)
        mo = TyContext.Cls_MsgPack()
        if not prodInfo:
            mo.setResult('code', 1)
            mo.setResult('info', '未找到对应的商品')
            return mo
        prodPrice = prodInfo['diamondPrice']
        prodName = prodInfo['name']
        ##
        # 取得当前用户的COIN
        userDiamond = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'diamond')
        if isinstance(userDiamond, (int, float)):
            userDiamond = int(userDiamond)
        else:
            userDiamond = 0
        TyContext.ftlog.info('consume->appId=', appId, 'clientId=', clientId, 'userId=', userId, 'userCoin=',
                             userDiamond,
                             'prodPrice=', prodPrice, 'prodId=', prodId, 'prodName=', prodName, 'prodCount=', prodCount,
                             'prodOrderId=', prodOrderId, 'mustcharge=', mustcharge, 'clientPayType', clientPayType,
                             'payInfo=', payInfo)

        if prodCount <= 0:
            prodCount = 1
        else:
            prodCount = int(prodCount)

        prodPrice = int(prodPrice)
        consumeDiamond = int(prodPrice * prodCount)
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('consume')
        if not consumeDiamond:
            mo.setError(2, '商品价格信息错误，请检查')
            return mo
        # 是否需要充值
        if mustcharge == 1 or userDiamond < consumeDiamond:
            mi.setParam('mustcharge', 1)
            return cls.charge(mi)
        # 直接兑换道具或金币
        fail, prodOrderId = TuyouPayConsume._create_consume_transaction(
            appId, appInfo, clientId, userId, consumeDiamond, prodId, prodPrice,
            prodCount, prodName, prodOrderId, mo)
        if fail:
            mo.setError(3, '兑换错误，请稍后重试')
            return mo

        TuyouPayConsume.__consume_user_coin__(
            appId, appInfo, clientId, userId, consumeDiamond, prodId, prodPrice,
            prodCount, prodName, prodOrderId, mo)
        return mo
