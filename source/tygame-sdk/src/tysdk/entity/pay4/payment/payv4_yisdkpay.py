# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import datetime
import json
import re

from payv4_yipay_base import TuYouPayYiBase
from tyframework.context import TyContext
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_filter import payv4_filter
from tysdk.entity.pay4.decorator.payv4_order import payv4_order


class TuYouPayYiSdkV4(TuYouPayYiBase):
    @classmethod
    def get_client_channel(cls, clientId):
        p = '([^_]+)_([0-9\.]+)_([^\.]+)\.([^\.]+)\.([^\.]+)\.([^\.]+)\.(.+)'
        m = re.match(p, clientId)
        if m:
            return m.group(6)
        return ''

    def check_charge_info(self, mi, chargeInfo):
        appId = chargeInfo['appId']
        diamondId = chargeInfo['diamondId']
        prodConfig = TyContext.Configure.get_global_item_json('yisdkpay_prodids', {})
        yipayDict = prodConfig[str(appId)]
        if not diamondId in yipayDict:
            clientId = chargeInfo['clientId']
            diamondPrice = chargeInfo['diamondPrice']
            prodDict = ChargeConfigure.get_prod_dict(appId, clientId=clientId)
            prodList = []
            for id in yipayDict:
                # 单机商品过滤掉
                if id.endswith('DJ'):
                    continue
                prodInfo = prodDict[id]
                if int(prodInfo.get('is_diamond', 0)) and prodInfo['price'] >= diamondPrice:
                    prodList.append(prodInfo)
            if prodList:
                prodList.sort(lambda x, y: cmp(x['price'], y['price']))
                prodInfo = prodList[0]
                chargeInfo['diamondId'] = prodInfo['id']
                chargeInfo['diamondName'] = prodInfo['name']
                chargeInfo['diamondPrice'] = prodInfo['price']
                chargeInfo['chargeTotal'] = prodInfo['price'] * chargeInfo['diamondCount']
                chargeInfo['chargeCoin'] = prodInfo['diamondPrice'] * chargeInfo['diamondCount']

    @payv4_filter('yisdkpay')
    def filter_payment(self, payment, prod_info, **kwargs):
        """
        支付方式列表中过滤检查，没有计费点得商品就不要显示此支付方式
        :param prodInfo:
        :param chargeInfo:
        :param kwargs:
        :return:
        """
        appId = kwargs['appId']
        clientId = kwargs['clientId']
        prodConfig = TyContext.Configure.get_global_item_json('yisdkpay_prodids', {})
        yipayDict = prodConfig[str(appId)]
        prodId, prodPrice = prod_info['id'], prod_info['price']
        # 计费点直购
        prodDict = ChargeConfigure.get_prod_dict(appId, clientId=clientId)
        if prodId in yipayDict:
            return True
        # 替代计费点
        for id in yipayDict:
            tmpProdInfo = prodDict[id]
            if int(tmpProdInfo.get('is_diamond', 0)) and tmpProdInfo['price'] >= prodPrice:
                return True
        return False

    @payv4_order('yisdkpay')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        TyContext.ftlog.debug('TuYouPayYiSdk charge_data chargeinfo', chargeinfo)
        appId = chargeinfo['appId']
        diamondId = chargeinfo['diamondId']  # 此处不能取buttonId，和buttonName
        prodconfig = TyContext.Configure.get_global_item_json('yisdkpay_prodids', {})
        data = prodconfig[str(appId)].get(str(diamondId), None)
        if data:
            payCode = data['feecode']
        else:
            raise Exception('can not find yisdkpay product define of diamondId='
                            + diamondId + ' clientId= ' + chargeinfo['clientId'])

        if payCode == '12':
            codeType = 2
        else:
            codeType = 0
        chargeData = {'msgOrderCode': payCode, 'codeType': codeType,
                      "alternativeProdId": data.get('alternativeProdId', ""),
                      "alternativeProdName": data.get('alternativeProdName', ""), }
        # 控制二次确认窗口是否显示
        channel = self.get_client_channel(chargeinfo['clientId'])
        confirm_threshold = prodconfig.get('confirm_threshold', 0)
        if channel in prodconfig.get('confirm_channel', []) and confirm_threshold > 0:
            userId = chargeinfo['uid']
            gameDataKey = 'gamedata:9999:%s' % userId
            totaltime, todaytime = TyContext.RedisGame.execute(userId, 'HMGET', gameDataKey, 'totaltime', 'todaytime')
            vip = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'vip')
            TyContext.ftlog.error('yisdkpay confirm info',
                                  'userId=%d' % userId,
                                  'channel=%s' % channel,
                                  'vip=%s' % vip,
                                  'totaltime=%s' % totaltime,
                                  'todaytime=%s' % todaytime,
                                  'confirm_threshold=%s' % confirm_threshold)

            if todaytime:
                obj = json.loads(todaytime)
                today_time = obj.get(datetime.datetime.now().strftime('%y%m%d'), 0)
                if today_time > confirm_threshold:
                    chargeData['isClosedConfirm'] = True
        chargeinfo['chargeData'] = chargeData
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/yipaysdk/callback")
    def handle_callback(self, rpath):
        return self.do_yipay_callback("yisdkpay")
