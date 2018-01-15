# -*- coding=utf-8 -*-

from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap


class TuYouPayZhuoWang():
    XML_RET = '<?xml version="1.0" encoding="gbk"?><ServiceGetData2SPRsp><transactionId>%s</transactionId><success>%s</success><results><result type="sms"><title></title></result></results></ServiceGetData2SPRsp>'

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        appId = params['appId']

        payCode = ''
        orderPhone = '10658077696611'
        if prodId == 'VOICE100':
            payCode = 'YX,258736,1,ff3f,1800529,611001'
        if prodId == 'MOONKEY':
            payCode = 'YX,258736,2,02fb,1800529,611001'
        if prodId == 'CARDMATCH10':
            payCode = 'YX,258736,3,0b75,1800529,611001'
        if prodId == 'T80K':
            payCode = 'YX,258736,4,3e00,1800529,611001'
        if prodId == 'T100K':
            payCode = 'YX,258736,5,9f1f,1800529,611001'
        if prodId == 'RAFFLE_NEW':
            payCode = 'YX,258736,6,a822,1800529,611001'
        if prodId == 'ZHUANYUN_MEZZO':
            payCode = 'YX,258736,7,c9ec,1800529,611001'

        orderPlatformId = ShortOrderIdMap.get_short_order_id(params['orderPlatformId'])
        payCode = payCode + ',' + orderPlatformId
        payData = {'msgOrderCode': payCode, 'orderPhone': orderPhone}
        params['payData'] = payData
        mo.setResult('payData', payData)
        mo.setResult('orderPlatformId', orderPlatformId)

        pass

    @classmethod
    def doZhuoWangCallback(self, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        xmldata = xmldata.replace('encoding="gbk"', 'encoding="utf-8"')
        xmldata = unicode(xmldata, encoding='gbk').encode('utf-8')
        TyContext.ftlog.info('zhuowangMdo encode->xmldata=', xmldata)
        transactionId = ''
        try:
            xmlroot = ElementTree.fromstring(xmldata)
            checkCode = xmlroot.find('checkCode').text
            transactionId = xmlroot.find('transactionId').text
            serviceId = xmlroot.find('serviceId').text
            spId = xmlroot.find('spId').text
            serviceType = xmlroot.find('serviceType').text
            feeType = xmlroot.find('feeType').text
            # 获取orderPlatformId
            orderPlatformId = ''
            parmMap = xmlroot.getiterator("paramMap")[0]
            for x in parmMap:
                k, v = x.getchildren()
                if k.text == 'command':
                    orderPlatformId = v.text
                    orderPlatformId = orderPlatformId.split(',')[-1]
                    orderPlatformId = ShortOrderIdMap.get_long_order_id(orderPlatformId)
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doZhuoWangCallback->ERROR, param error !! xmldata=', xmldata)
            return TuYouPayZhuoWang.XML_RET % (transactionId, '0')

        if len(orderPlatformId) != 14:
            TyContext.ftlog.info('doZhuoWangCallback->ERROR, orderPlatformId error !!', 'orderPlatformId=',
                                 orderPlatformId)
            return TuYouPayZhuoWang.XML_RET % (transactionId, '0')

        TyContext.RunMode.get_server_link(orderPlatformId)

        if str(checkCode) == '000':
            from tysdk.entity.pay.pay import TuyouPay
            trade_status = 'TRADE_FINISHED'
            notifys = {'xml': xmldata}
            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, notifys)
            if isOk:
                ret_msg = TuYouPayZhuoWang.XML_RET % (transactionId, '1')
            else:
                ret_msg = TuYouPayZhuoWang.XML_RET % (transactionId, '0')

            ret_msg = unicode(ret_msg, encoding='utf-8').encode('gbk')
            return ret_msg

        pass
