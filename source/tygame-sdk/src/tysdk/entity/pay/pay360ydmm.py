# -*- coding=utf-8 -*-

from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext


class TuYouPay360YdMm():
    appkeys = {'300008304702': '96176936E87B274E',  # 斗地主
               }

    XML_RET = '''<?xml version="1.0" encoding="UTF-8"?>
<SyncAppOrderResp>
    <MsgType>SyncAppOrderResp</MsgType>
    <Version>1.0.0</Version>
    <hRet>%s</hRet>
</SyncAppOrderResp>
'''

    @classmethod
    def doBuyStraight(self, userId, params, mo):

        prodId = params['prodId']
        appId = params['appId']

        payCode = '30000830470203'
        if prodId == 'T20K':
            payCode = '30000830470201'
        if prodId == 'T50K':
            payCode = '30000830470202'
        if prodId == 'T100K':
            payCode = '30000830470203'
        if prodId == 'RAFFLE' or prodId == 'RAFFLE_NEW':
            payCode = '30000830470204'
        if prodId == 'VOICE100':
            payCode = '30000830470205'
        if prodId == 'MOONKEY3':
            payCode = '30000830470206'
        if prodId == 'MOONKEY':
            payCode = '30000830470207'
        if prodId == 'CARDMATCH10':
            payCode = '30000830470208'
        if prodId == 'ZHUANYUN':
            payCode = '30000830470209'

        payData = {'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def do360YdMmCallback(self, rpath):

        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info('360YdMmCallback.doYdMmCallback in xmldata=', xmldata)

        orderPlatformId = ''
        try:
            xmlroot = ElementTree.fromstring(xmldata)

            # orderPlatformId = xmlroot.find('OrderId').text
            orderPlatformId = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ExData').text
            if orderPlatformId == '':
                TyContext.ftlog.info('360YdMmCallback.doYdMmCallback->ERROR, orderPlatformId error !! xmldata=',
                                     xmldata)
                return TuYouPay360YdMm.XML_RET % ('1')

            OrderID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}OrderID').text
            #             TradeID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}TradeID').text
            #             ActionTime = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ActionTime').text
            AppID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}AppID').text
            PayCode = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}PayCode').text
            ChannelID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ChannelID').text
            AppKey = ''
            if TuYouPay360YdMm.appkeys.has_key(AppID):
                AppKey = TuYouPay360YdMm.appkeys[AppID]
            else:
                return TuYouPay360YdMm.XML_RET % ('4003')
            MD5Sign = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}MD5Sign').text

        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('TuYouPay360YdMm.doYdMmCallback->ERROR, xmldata error !! xmldata=', xmldata)
            return TuYouPay360YdMm.XML_RET % ('1')

        tSign = OrderID + '#' + ChannelID + '#' + PayCode + '#' + AppKey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if MD5Sign != vSign.upper():
            TyContext.ftlog.info('TuYouPay360YdMm.doYdMmCallback->ERROR, sign error !! sign=', MD5Sign, 'vSign=', vSign)
            return TuYouPay360YdMm.XML_RET % ('1')

        from tysdk.entity.pay.pay import TuyouPay
        notifys = {'xml': xmldata}
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', notifys)
        if isOk:
            return TuYouPay360YdMm.XML_RET % ('0')
        else:
            return TuYouPay360YdMm.XML_RET % ('2')
