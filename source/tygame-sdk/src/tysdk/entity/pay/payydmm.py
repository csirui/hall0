# -*- coding=utf-8 -*-

from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.entity.pay.pay import TuyouPay


class TuYouPayYdMmWeak():
    appkeys = {'300007728518': '06E2A01050F52F6B',  # 斗地主
               '300008273516': '2D12958EADE42788',  # 炸金花
               '300008266521': '6A95A7D68439016A',  # 德州
               '300008273478': 'D52CD21CCC3F2BB9',  # 麻将
               }

    XML_RET = '''<?xml version="1.0" encoding="UTF-8"?>
<SyncAppOrderResp>
    <MsgType>SyncAppOrderResp</MsgType>
    <Version>1.0.0</Version>
    <hRet>%s</hRet>
</SyncAppOrderResp>
'''

    #     @classmethod
    #     def doBuyStraightNew(self, userId, params, mo):
    #
    #         prodId = params['prodId']
    #
    #         payCode = '30000772851803'
    #         if prodId == 'T60K' :
    #             payCode = '30000772851814'
    #         if prodId == 'T80K' :
    #             payCode = '30000772851818'
    #         if prodId == 'T100K' :
    #             payCode = '30000772851803'
    #         if prodId == 'MOONKEY' :
    #             payCode = '30000772851805'
    #         if prodId == 'MOONKEY3' :
    #             payCode = '30000772851806'
    #         if prodId == 'CARDMATCH10' :
    #             payCode = '30000772851810'
    #         if prodId == 'ZHUANYUN' :
    #             payCode = '30000772851815'
    #         if prodId == 'ZHUANYUN_BIG' :
    #             payCode = '30000772851817'
    #         if prodId == 'RAFFLE_NEW' :
    #             payCode = '30000772851819'
    #         if prodId == 'VOICE100' :
    #             payCode = '30000772851807'
    #
    #         payData = {'msgOrderCode':payCode}
    #         params['payData'] = payData
    #         mo.setResult('payData', payData)
    #         pass

    @classmethod
    def get_app_key(self, ydmm_appid):
        try:
            extdata = TyContext.PayType.get_pay_type_ext_datas('ydmm')
            if extdata != None:
                appkeys = extdata.get('appkeys', {})
                appkey = appkeys.get(ydmm_appid, None)
                if appkey != None:
                    return appkey
        except:
            TyContext.ftlog.exception()

        appkey = TuYouPayYdMmWeak.appkeys.get(ydmm_appid, None)
        return appkey

    @classmethod
    def doBuyStraight(self, userId, params, mo):

        #         if params['clientId'] in ['Android_2.88_ydmm'] :
        #             self.doBuyStraightNew(userId, params, mo)
        #             return

        prodId = params['prodId']
        appId = params['appId']

        payCode = '30000772851807'
        if prodId == 'T20K':
            payCode = '30000772851801'
        if prodId == 'T50K':
            payCode = '30000772851802'
        if prodId == 'T100K':
            payCode = '30000772851803'
        if prodId == 'T300K':
            payCode = '30000772851808'
        if prodId == 'MOONKEY':
            payCode = '30000772851805'
        if prodId == 'MOONKEY3':
            payCode = '30000772851806'
        if prodId == 'VOICE100':
            payCode = '30000772851807'
        if prodId == 'RAFFLE' and str(appId) == '6':
            payCode = '30000772851811'
        if prodId == 'CARDMATCH10':
            payCode = '30000772851810'
        if prodId == 'ZHUANYUN':
            payCode = '30000772851812'
        if prodId == 'T60K':
            payCode = '30000772851814'
        if prodId == 'ZHUANYUN_6':
            payCode = '30000772851815'
        if prodId == 'RAFFLE_6':
            payCode = '30000772851816'
        if prodId == 'ZHUANYUN_MEZZO':
            payCode = '30000772851817'
        if prodId == 'T80K':
            payCode = '30000772851818'
        if prodId == 'RAFFLE_NEW':
            payCode = '30000772851819'

        # 炸金花
        if prodId == 'TGBOX1':
            payCode = '30000827351601'
        if prodId == 'TGBOX2':
            payCode = '30000827351602'
        if prodId == 'TGBOX3':
            payCode = '30000827351603'
        if prodId == 'RAFFLE' and str(appId) == '1':
            payCode = '30000827351604'

        # 德州
        if prodId == 'TEXAS_COIN1':
            payCode = '30000826652101'
        if prodId == 'TEXAS_COIN6':
            payCode = '30000826652102'
        if prodId == 'TEXAS_COIN2':
            payCode = '30000826652103'
        if prodId == 'TEXAS_COIN3':
            payCode = '30000826652104'
        if prodId == 'TEXAS_COIN_R6':
            payCode = '30000826652105'
        if prodId == 'TEXAS_COIN_LUCKY_R6':
            payCode = '30000826652107'

        # 麻将
        if prodId == 'C5':
            payCode = '30000827347801'
        if prodId == 'C10':
            payCode = '30000827347802'
        if prodId == 'C5_RAFFLE':
            payCode = '30000827347803'
        if prodId == 'C2':
            payCode = '30000827347804'
        if prodId == 'C6':
            payCode = '30000827347805'
        if prodId == 'C8':
            payCode = '30000827347806'
        if prodId == 'C6_RAFFLE':
            payCode = '30000827347807'
        if prodId == 'C8_LUCKY':
            payCode = '30000827347808'
        if prodId == 'C8_RAFFLE':
            payCode = '30000827347809'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doYdMmCallback(self, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback in xmldata=', xmldata)

        orderPlatformId = ''
        try:
            xmlroot = ElementTree.fromstring(xmldata)

            # orderPlatformId = xmlroot.find('OrderId').text
            orderPlatformId = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ExData').text
            if orderPlatformId == '':
                TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback->ERROR, orderPlatformId error !! xmldata=',
                                     xmldata)
                return TuYouPayYdMmWeak.XML_RET % ('1')

            OrderID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}OrderID').text
            #             TradeID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}TradeID').text
            #             ActionTime = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ActionTime').text
            AppID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}AppID').text
            PayCode = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}PayCode').text
            ChannelID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ChannelID').text
            TotalPrice = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}TotalPrice').text  # 单位：分
            TotalPrice = int(TotalPrice)
            AppKey = self.get_app_key(AppID)
            if AppKey == None:
                TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback->ERROR, AppKey not found!! AppID=', AppID)
                return TuYouPayYdMmWeak.XML_RET % ('4003')
            MD5Sign = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}MD5Sign').text

        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback->ERROR, xmldata error !! xmldata=', xmldata)
            return TuYouPayYdMmWeak.XML_RET % ('1')

        notifys = {'xml': xmldata, 'third_orderid': OrderID,
                   'third_prodid': PayCode,
                   'pay_appid': AppID if AppID else 'na',
                   'payType': 'ydmm'}
        if OrderID == '0' * len(OrderID):
            TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback->ERROR, failed order: OrderID', OrderID)
            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FAILED', notifys)
            return TuYouPayYdMmWeak.XML_RET % ('0')

        tSign = OrderID + '#' + ChannelID + '#' + PayCode + '#' + AppKey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if MD5Sign != vSign.upper():
            TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback->ERROR, sign error !! sign=', MD5Sign, 'vSign=',
                                 vSign)
            return TuYouPayYdMmWeak.XML_RET % ('1')

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, TotalPrice / 100.0, 'TRADE_FINISHED', notifys)
        return TuYouPayYdMmWeak.XML_RET % ('0')
