# -*- coding=utf-8 -*-

from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext


class TuYouPayLianTong():
    appkeys = {'905608778920130929155624363800': '9813b270ed0288e7c038',  # 斗地主
               }
    XML_OK = '''<?xml version="1.0" encoding="UTF-8"?>
<callbackRsp>1</callbackRsp>
'''
    XML_ERRO = '''<?xml version="1.0" encoding="UTF-8"?>
<callbackRsp>0</callbackRsp>
'''

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        payCode = '130929012542'
        orderProdCode = '905608778920130929155624363800002'
        orderProdName = '5万金币'
        if prodId == 'T20K':
            payCode = '130929012541'
            orderProdCode = '905608778920130929155624363800001'
            orderProdName = '2万金币'
        if prodId == 'T50K':
            payCode = '130929012542'
            orderProdCode = '905608778920130929155624363800002'
            orderProdName = '5万金币'
        if prodId == 'T100K':
            payCode = '130929012543'
            orderProdCode = '905608778920130929155624363800003'
            orderProdName = '10万金币'
        if prodId == 'T300K':
            payCode = '130929012544'
            orderProdCode = '905608778920130929155624363800004'
            orderProdName = '30万金币'
        if prodId == 'MOONKEY':
            payCode = '130929012545'
            orderProdCode = '905608778920130929155624363800005'
            orderProdName = '月光之钥'
        if prodId == 'MOONKEY3':
            payCode = '130929012546'
            orderProdCode = '905608778920130929155624363800006'
            orderProdName = '月光之钥3个'
        if prodId == 'VOICE100':
            payCode = '130929012547'
            orderProdCode = '905608778920130929155624363800007'
            orderProdName = '语音小喇叭100个'
        if prodId == 'RAFFLE':
            payCode = '130929012541'
            orderProdCode = '905608778920130929155624363800001'
            orderProdName = '翻倍抽奖'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode, 'orderProdCode': orderProdCode, 'orderProdName': orderProdName}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doLianTongCallback(self, rpath):

        xmldata = TyContext.RunHttp.get_body_content()
        # ftlog.info('TuYouPayLianTong.doLianTongCallback in xmldata=', xmldata)
        # xmldata = '<callbackReq><orderid>XXX</orderid><ordertime>XXX</ordertime><cpid>XXX</cpid><appid>XXX</appid><fid>XXX</fid><consumeCode>XXX</consumeCode><payfee>XXX</payfee><payType>XXX</payType><hRet>XXX</hRet><status>XXX</status><signMsg>XXX</signMsg></callbackReq>'
        TyContext.ftlog.info('TuYouPayLianTong.doLianTongCallback in xmldata=', xmldata)

        try:
            xmlroot = ElementTree.fromstring(xmldata)

            orderPlatformId = xmlroot.find('orderid').text

            ordertime = xmlroot.find('ordertime').text
            cpid = xmlroot.find('cpid').text
            #             if xmlroot.find('appid').text:
            #                 appid = xmlroot.find('appid').text
            #             else:
            #                 appid = '905608778920130929155624363800'
            fid = xmlroot.find('fid').text
            consumeCode = xmlroot.find('consumeCode').text
            payfee = int(xmlroot.find('payfee').text)
            payType = int(xmlroot.find('payType').text)
            hRet = int(xmlroot.find('hRet').text)
            status = xmlroot.find('status').text
            signMsg = xmlroot.find('signMsg').text
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('TuYouPayLianTong.doLianTongCallback->ERROR, xmldata error !! xmldata=', xmldata)
            return TuYouPayLianTong.XML_ERRO

        # tSign = 'orderid='+orderPlatformId+'&ordertime='+ordertime+'&cpid='+cpid+'&appid='+appid+'&fid='+fid+'&consumeCode='+consumeCode+'&payfee='+str(payfee)+'&payType='+str(payType)+'&hRet='+str(hRet)+'&status='+status+'&Key='+TuYouPayLianTong.appkeys[str(appid)]
        tSign = 'orderid=' + orderPlatformId + '&ordertime=' + ordertime + '&cpid=' + cpid + '&appid=&fid=' + fid + '&consumeCode=' + consumeCode + '&payfee=' + str(
            payfee) + '&payType=' + str(payType) + '&hRet=' + str(
            hRet) + '&status=' + status + '&Key=9813b270ed0288e7c038'
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if signMsg != vSign:
            TyContext.ftlog.info('TuYouPayLianTong.doLianTongCallback->ERROR, sign error !! sign=', signMsg, 'vSign=',
                                 vSign)
            return TuYouPayLianTong.XML_ERRO

        TyContext.ftlog.info('TuYouPayLianTong.doLianTongCallback in orderPlatformId=', orderPlatformId, 'hRet=', hRet,
                             'status=', status)
        retXml = ''
        from tysdk.entity.pay.pay import TuyouPay
        notifys = {'xml': xmldata}
        if str(hRet) == '0' and str(status) == '00000':
            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', notifys)
            if isOk:
                retXml = TuYouPayLianTong.XML_OK
            else:
                retXml = TuYouPayLianTong.XML_ERRO
        else:
            TuyouPay.deliveryChargeError(orderPlatformId, notifys, str(hRet) + '|' + str(status), 1)
            retXml = TuYouPayLianTong.XML_OK

        return retXml
