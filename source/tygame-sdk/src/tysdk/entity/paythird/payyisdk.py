# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json
import re

import datetime

from tyframework.context import TyContext
from tysdk.entity.pay3.charge_conf import TuyouPayChargeConf


class TuYouPayYiSdk(object):
    @classmethod
    def get_client_channel(cls, clientId):
        p = '([^_]+)_([0-9\.]+)_([^\.]+)\.([^\.]+)\.([^\.]+)\.([^\.]+)\.(.+)'
        m = re.match(p, clientId)
        if m:
            return m.group(6)
        return ''

    @classmethod
    def charge_data(cls, chargeinfo):
        TyContext.ftlog.debug('TuYouPayYiSdk charge_data chargeinfo', chargeinfo)
        if 'secondBuy' in chargeinfo['appInfo'] and len(chargeinfo['appInfo']) > len('secondBuy '):
            secondBuy = chargeinfo['appInfo'].split(' ')
            TyContext.ftlog.debug('TuYouPayYiSdk charge_data secondBuy list', secondBuy)
            secondBuyType = secondBuy[1]
            cfun = TuyouPayChargeConf.get_charge_data_func(secondBuyType)
            cfun(chargeinfo)
            chargeinfo['chargeType'] = secondBuyType
            return

        appId = chargeinfo['appId']
        buttonId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('yisdkpay_prodids', {})
        data = prodconfig[str(appId)].get(str(buttonId), None)

        if data:
            payCode = data['feecode']
        else:
            raise Exception('can not find yisdkpay product define of buttonId='
                            + buttonId + ' clientId= ' + chargeinfo['clientId'])

        if payCode == '12':
            codeType = 2
        else:
            codeType = 0
        chargeData = {'msgOrderCode': payCode, 'codeType': codeType,
                      "alternativeProdId": data.get('alternativeProdId', ""),
                      "alternativeProdName": data.get('alternativeProdName', ""), }
        # 控制二次确认窗口是否显示
        channel = cls.get_client_channel(chargeinfo['clientId'])
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

    @classmethod
    def doYiSdkPayCallback(cls, rpath):
        from payyi import TuYouPayYi
        return TuYouPayYi.do_yipay_callback('yisdkpay')
