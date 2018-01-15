#! encoding=utf-8
import json

import datetime

from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.pay3.consume import TuyouPayConsume
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_metaclass import payv4_metaclass
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.strategy.android_smspay_strategy import RiskControlV4
from tysdk.entity.pay_common.orderlog import Order

__author__ = 'yuejianqiang'


class PayBaseV4(object):
    __metaclass__ = payv4_metaclass

    def __init__(self):
        self.need_short_order_id = False

    def handle_order(self, mi):
        chargeInfo = self.get_charge_info(mi)
        return self.return_mo(0, chargeInfo=chargeInfo)

    def make_order_id(self, userId, appId, clientId):
        orderId = TyContext.ServerControl.makeChargeOrderIdV4(userId, appId, clientId)
        if self.need_short_order_id:
            return ShortOrderIdMap.get_short_order_id(orderId)
        return orderId

    def return_mo(self, code, **kwds):
        mo = TyContext.Cls_MsgPack()
        for k, v in kwds.items():
            mo.setResult(k, v)
        mo.setResult('code', code)
        return mo

    def check_store_payment(self, mi):
        prodId = mi.getParamStr('prodId')
        chargeType = mi.getParamStr('chargeType')
        appId = mi.getParamStr('appId', '9999')
        clientId = mi.getParamStr('clientId')
        # mustcharge = mi.getParamInt('mustcharge')
        # tyGameName = mi.getParamStr('tyGameName')
        # tySubGameName = mi.getParamStr('tySubGameName')
        tyChannelName = mi.getParamStr('tyChannelName')
        # tyVersionName = mi.getParamStr('tyVersionName') # 3.71
        store_payment = ChargeConfigure.get_store_payment(prodId, appId, clientId=clientId)
        if not store_payment:
            raise PayErrorV4(1, '支付类型未配置')
        # 获取对应的支付类型
        payInfo = filter(lambda x: x['paytype'] == chargeType, store_payment)
        if not payInfo:
            raise PayErrorV4(1, '支付类型无效')

    def get_charge_info(self, mi):
        """
        获取购买信息，prodId可能是钻石Id，也可能是道具Id
        :param mi:
        :return:
        """
        userId = mi.getParamInt('userId', 0)
        appId = mi.getParamStr('appId', '9999')
        clientId = mi.getParamStr('clientId')
        appInfo = mi.getParamStr('appInfo', '')
        chargeType = mi.getParamStr('chargeType')
        prodId = mi.getParamStr('prodId')
        prodName = mi.getParamStr('prodName')
        prodCount = mi.getParamInt('prodCount', 0)
        prodPrice = float(mi.getParamStr('prodPrice', 0))
        mustcharge = mi.getParamInt('mustcharge', 0)
        # tyChannelName = mi.getParamStr('tyChannelName')
        platformOrderId = mi.getParamStr('platformOrderId', '')
        if not platformOrderId:
            platformOrderId = self.make_order_id(userId, appId, clientId)
        # 获取商品信息
        prod_info = ChargeConfigure.get_prod_info(appId, prodId, clientId=clientId)
        if not prod_info:
            raise PayErrorV4(1, '商品信息错误')
        if prodPrice >= 0.1 and abs(prodPrice - prod_info['price']) > 0.1:
            raise PayErrorV4(2, '商品信息错误')
        # 商品加个通过后台配置
        prodPrice = prod_info['price']
        if not prodCount or prodCount < 0:
            prodCount = 1
        if not prodName:
            prodName = prod_info.get('name', '')
            # 获取折扣信息
        cpExtInfo = ""
        cpExtObj = ChargeConfigure.get_cpExt_info(prodId, appId, clientId=clientId, chargeType=chargeType)
        if cpExtObj:
            cpExtInfo = cpExtObj.get('cpExtInfo', 0)
        chargeInfo = {'uid': userId,
                      'userId': userId,
                      'appId': int(appId),
                      'clientId': clientId,
                      'appInfo': appInfo,
                      'chargeType': chargeType,
                      'diamondId': prodId,
                      'diamondName': prodName,
                      'diamondPrice': prodPrice,
                      'diamondCount': prodCount,
                      'chargeTotal': prodPrice * prodCount,  # 充值的RMB数量
                      'chargeCoin': prodCount * prod_info['diamondPrice'],  # 充值的钻石数量
                      'platformOrderId': platformOrderId,
                      'phoneType': TyContext.UserSession.get_session_phone_type(userId),
                      'buttonId': prodId,
                      'buttonName': prodName,
                      'cpExtInfo': cpExtInfo,
                      'mustcharge': mustcharge,
                      'prodOrderId': mi.getParamStr('prodOrderId', ''),
                      'mainChannel': clientId.split('.')[-2],
                      'packageName': mi.getParamStr('tyPackageName', '') or mi.getParamStr('packageName', ''),
                      'channelName': mi.getParamStr('tyChannelName', ''),
                      }
        # 非钻石需要兑换或途游游戏
        if not int(prod_info.get('is_diamond', 0)) or int(appId) > 9999:
            consumeInfo = self.get_consume_info(chargeInfo)
        else:
            consumeInfo = None
        # 计费点获取(有些钻石也需要)
        self.check_charge_info(mi, chargeInfo)
        self.save_order(chargeInfo, consumeInfo)
        # bi report
        Order.log(platformOrderId, Order.CREATE, userId, appId, clientId,
                  diamondid=chargeInfo['diamondId'], prodid=consumeInfo['prodId'] if consumeInfo else 'na',
                  prod_price=consumeInfo['prodPrice'] if consumeInfo else 'na',
                  paytype=chargeInfo.get('chargeType', 'na'),
                  charge_price=chargeInfo['chargeTotal'], shortId='', pay_appid='')
        return chargeInfo

    def get_consume_info(self, chargeInfo):
        prodInfo = ChargeConfigure.get_prod_info(chargeInfo['appId'], chargeInfo['diamondId'],
                                                 clientId=chargeInfo['clientId'])
        prodDiamondPrice = prodInfo['diamondPrice']  # 商品钻石价格（一般等于10*prodInfo['price'])
        ###
        prodCount = chargeInfo['diamondCount']
        appId = chargeInfo['appId']
        appInfo = chargeInfo.get('appInfo', '')
        clientId = chargeInfo['clientId']
        userId = chargeInfo['userId']
        prodId = chargeInfo['diamondId']
        prodPrice = chargeInfo['diamondPrice']
        prodCount = prodCount
        prodName = chargeInfo['diamondName']
        consumeCoin = prodCount * prodDiamondPrice
        prodOrderId = chargeInfo['prodOrderId']
        mo = TyContext.Cls_MsgPack()
        # 创建消耗订单
        fail, consumeOrderId = TuyouPayConsume._create_consume_transaction(
            appId, appInfo, clientId, userId, consumeCoin, prodId, prodPrice,
            prodCount, prodName, prodOrderId, mo)
        if fail:
            raise PayErrorV4(mo.getErrorCode(), mo.getErrorInfo())
        consumeInfo = {
            'appId': int(chargeInfo['appId']),
            'appInfo': chargeInfo['appInfo'],
            'clientId': chargeInfo['clientId'],
            'userId': chargeInfo['userId'],
            'consumeCoin': consumeCoin,
            'prodId': chargeInfo['diamondId'],
            'prodPrice': chargeInfo['diamondPrice'],
            'prodCount': chargeInfo['diamondCount'],
            'prodName': chargeInfo['diamondName'],
            'prodOrderId': consumeOrderId,
            'mustcharge': '1',
        }
        # diamondInfo = self.get_consume_diamond(chargeInfo['appId'], prodInfo,clientId=chargeInfo['clientId'])
        # replace item
        # chargeInfo['diamondId'] = diamondInfo['id']
        # chargeInfo['diamondName'] = diamondInfo['name']
        # chargeInfo['diamondPrice'] = diamondInfo['price']
        # consumeInfo['diamondCount'] = diamondInfo['']
        # self.check_charge_info(chargeInfo)
        return consumeInfo

    def check_charge_info(self, mi, chargeInfo):
        # return ChargeConfigure.get_consume_diamond(appId, prodInfo,clientId=clientId)
        pass

    def save_order(self, chargeInfo, consumeInfo):
        orderId = chargeInfo['platformOrderId']
        datas = ['state', PayConst.CHARGE_STATE_BEGIN,
                 'createTime', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 'charge', json.dumps(chargeInfo), ]
        if consumeInfo:
            datas.extend(['consume', json.dumps(consumeInfo)])
        ChargeModel.save_order(orderId, *datas)

    def change_chargeinfo(self, diamondList, chargeInfo):
        clientId = chargeInfo['clientId']
        diamondPrice = chargeInfo['diamondPrice']
        prodDict = ChargeConfigure.get_prod_dict(chargeInfo['appId'], clientId=clientId)
        prodList = []
        for id in diamondList:
            # 单机商品过滤掉
            if id.endswith('DJ'):
                continue
            try:
                prodInfo = prodDict[id]
            except KeyError:
                continue
            if int(prodInfo.get('is_diamond', 0)) and prodInfo['price'] >= diamondPrice:
                prodList.append(prodInfo)
        if prodList:
            prodList.sort(lambda x, y: cmp(x['price'], y['price']))
            prodInfo = prodList[0]
            chargeInfo['diamondId'] = prodInfo['id']
            chargeInfo['diamondName'] = prodInfo['name']
            chargeInfo['buttonName'] = prodInfo['name']
            chargeInfo['diamondPrice'] = prodInfo['price']
            chargeInfo['chargeTotal'] = prodInfo['price'] * chargeInfo['diamondCount']
            chargeInfo['chargeCoin'] = prodInfo['diamondPrice'] * chargeInfo['diamondCount']

    def is_out_pay_limit(self, chargeinfo):
        chargeType = chargeinfo['chargeType']
        user_control = RiskControlV4(chargeinfo['uid'])
        if user_control.is_limited(chargeType):
            return True
        return False

    @classmethod
    def upgrade_user_paylimit_state(self, userId, paytype, amount):
        user_control = RiskControlV4(userId)
        user_control.record_usage(paytype, amount)

    @classmethod
    def load_order_charge_info(cls, platformOrderId):
        chargeKey = 'sdk.charge:' + platformOrderId
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        if chargeInfo:
            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
        return chargeInfo

    @classmethod
    def loadRsaKey(cls, key, prefix, suffix):
        key = key.replace('\r', '')
        key = key.replace('\n', '')
        if key.find(prefix) >= 0:
            key = key[len(prefix):]
        if key.find(suffix) >= 0:
            key = key[:-len(suffix)]
        data = [prefix, ]
        for i in range(0, len(key), 64):
            data.append(key[i:i + 64])
        data.append(suffix)
        return '\n'.join(data)

    @classmethod
    def loadRsaPrivateKey(cls, key):
        return cls.loadRsaKey(key, prefix='-----BEGIN PRIVATE KEY-----', suffix='-----END PRIVATE KEY-----')

    @classmethod
    def loadRsaPublicKey(cls, key):
        return cls.loadRsaKey(key, prefix='-----BEGIN PUBLIC KEY-----', suffix='-----END PUBLIC KEY-----')

    @classmethod
    def loadRsaCertKey(cls, key):
        return cls.loadRsaKey(key, prefix='-----BEGIN CERTIFICATE-----', suffix='-----END CERTIFICATE-----')
