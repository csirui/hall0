# -*- coding=utf-8 -*-

from xml.etree import ElementTree

from tyframework.context import TyContext


class TuYouPayMsgYd():
    XML_OK = '''<?xml version="1.0" encoding="UTF-8"?>
<response>
    <transIDO>%s</transIDO>
    <hRet>0</hRet>
    <message>Successful</message>
</response>
'''
    XML_ERRO = '''<?xml version="1.0" encoding="UTF-8"?>
<response>
    <transIDO>%s</transIDO>
    <hRet>1</hRet>
    <message>error</message>
</response>
'''

    @classmethod
    def doMsgYdRequest(self, datas):
        TyContext.ftlog.info('TuYouPayMsgYd.doMsgYdRequest in datas=', datas)
        mo = TyContext.Cls_MsgPack()
        from tysdk.entity.pay.pay import TuyouPay
        TuyouPay.makeBuyChargeMessage(mo, datas)
        return mo

    @classmethod
    def doMsgYdCallback(self, rpath):
        clientIp = TyContext.RunHttp.get_client_ip()
        TyContext.ftlog.info('TuYouPayMsgYd.doMsgYdCallback in clientIp=', clientIp)
        if not clientIp in ('112.4.3.36'):
            return TuYouPayMsgYd.XML_ERRO % ('')

        xmldata = TyContext.RunHttp.get_body_content()
        # ftlog.info('TuYouPayMsgYd.doMsgYdCallback in xmldata=', xmldata)
        # xmldata = '<?xml version="1.0" encoding="UTF-8"?><request><userId>1246488737</userId><cpServiceId>601810071546</cpServiceId><consumeCode>000071545001</consumeCode><cpParam>1234567890123456</cpParam><hRet>0</hRet><status>1101</status><transIDO>4163657PONE3017B1</transIDO><versionId>100</versionId></request>'
        TyContext.ftlog.info('TuYouPayMsgYd.doMsgYdCallback in xmldata=', xmldata)

        xmlroot = ElementTree.fromstring(xmldata)
        # userId = xmlroot.find('userId').text
        # cpServiceId = xmlroot.find('cpServiceId').text
        # consumeCode = xmlroot.find('consumeCode').text
        orderPlatformId = xmlroot.find('cpParam').text

        hRet = int(xmlroot.find('hRet').text)
        status = int(xmlroot.find('status').text)
        transIDO = xmlroot.find('transIDO').text
        # versionId = xmlroot.find('versionId').text

        TyContext.ftlog.info('TuYouPayMsgYd.doMsgYdCallback in orderPlatformId=', orderPlatformId, 'hRet=', hRet,
                             'status=', status)
        retXml = ''
        from tysdk.entity.pay.pay import TuyouPay
        notifys = {'xml': xmldata}
        if hRet == 0 and status == 1101:
            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', notifys)
            if isOk:
                retXml = TuYouPayMsgYd.XML_OK
            else:
                retXml = TuYouPayMsgYd.XML_ERRO
        else:
            TuyouPay.deliveryChargeError(orderPlatformId, notifys, str(hRet) + '|' + str(status), 1)
            retXml = TuYouPayMsgYd.XML_OK

        retXml = retXml % (transIDO)
        return retXml
