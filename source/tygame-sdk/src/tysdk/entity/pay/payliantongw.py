# -*- coding=utf-8 -*-

import json
import string
import time
from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext


class TuYouPayLianTongW():
    # 一个cp只有一个appkey，这个是途游的。接第三方的联通沃需要修改
    appkeys = '8786914cc07009556fcf'
    XML_OK = '''<?xml version="1.0" encoding="UTF-8"?>
<callbackRsp>1</callbackRsp>
'''
    XML_ERRO = '''<?xml version="1.0" encoding="UTF-8"?>
<callbackRsp>0</callbackRsp>
'''

    XML_CHECKORDER_RET = '''<?xml version="1.0" encoding="UTF-8"?>
<paymessages>
    <checkOrderIdRsp>%s</checkOrderIdRsp>
    <appname>%s</appname>
    <feename>%s</feename>
    <payfee>%s</payfee>
    <appdeveloper>%s</appdeveloper>
    <gameaccount>%s</gameaccount>
    <macaddress>%s</macaddress>
    <appid>%s</appid>
    <ipaddress>%s</ipaddress>
    <serviceid>%s</serviceid>
    <channelid>%s</channelid>
    <cpid>%s</cpid>
    <ordertime>%s</ordertime>
    <imei>%s</imei>
    <appversion>%s</appversion>
</paymessages>
'''

    @classmethod
    def doBuyStraight(self, userId, params, mo):

        payData = self.__get_order_code(params)
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def __get_order_code(self, params):
        prodId = params['prodId']
        # use 10 yuan as default one, so it will not fail when prodId not found here
        payCode = '140519035439'
        orderProdCode = '9014273345620140519164257493800003'
        orderProdName = '10万金币'
        if prodId == 'T20K':
            payCode = '140519035437'
            orderProdCode = '9014273345620140519164257493800001'
            orderProdName = '2万金币'
        if prodId == 'T50K':
            payCode = '140519035438'
            orderProdCode = '9014273345620140519164257493800002'
            orderProdName = '5万金币'
        if prodId == 'T60K':
            payCode = '140716045598'
            orderProdCode = '9014273345620140519164257493800010'
            orderProdName = '6万金币'
        if prodId == 'T80K':
            payCode = '140716045601'
            orderProdCode = '9014273345620140519164257493800013'
            orderProdName = '8万金币'
        if prodId == 'T100K':
            payCode = '140519035439'
            orderProdCode = '9014273345620140519164257493800003'
            orderProdName = '10万金币'
        if prodId == 'RAFFLE':
            payCode = '140519035444'
            orderProdCode = '9014273345620140519164257493800008'
            orderProdName = '超值礼包'
        if prodId == 'RAFFLE_6':
            payCode = '140716045600'
            orderProdCode = '9014273345620140519164257493800012'
            orderProdName = '超值大礼包'
        if prodId == 'RAFFLE_NEW':
            payCode = '140716045602'
            orderProdCode = '9014273345620140519164257493800014'
            orderProdName = '超值豪华礼包'

        if prodId == 'ZHUANYUN':
            payCode = '140519035445'
            orderProdCode = '9014273345620140519164257493800009'
            orderProdName = '转运礼包'
        if prodId == 'ZHUANYUN_6':
            payCode = '140716045599'
            orderProdCode = '9014273345620140519164257493800011'
            orderProdName = '转运中礼包'
        if prodId == 'ZHUANYUN_MEZZO':
            payCode = '140716045603'
            orderProdCode = '9014273345620140519164257493800015'
            orderProdName = '转运大礼包'
        if prodId == 'CARDMATCH10':
            payCode = '140519035443'
            orderProdCode = '9014273345620140519164257493800007'
            orderProdName = '参赛券10张'
        if prodId == 'VOICE100':
            payCode = '140519035440'
            orderProdCode = '9014273345620140519164257493800004'
            orderProdName = '语音小喇叭100个'
        if prodId == 'MOONKEY':
            payCode = '140519035442'
            orderProdCode = '9014273345620140519164257493800006'
            orderProdName = '月光之钥1个'
        if prodId == 'MOONKEY3':
            payCode = '140519035441'
            orderProdCode = '9014273345620140519164257493800005'
            orderProdName = '月光之钥3个'

        payData = {'msgOrderCode': payCode, 'orderProdCode': orderProdCode, 'orderProdName': orderProdName}
        return payData

    @classmethod
    def __create_md5_sign__(self, tSign):

        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()

        return vSign

    @classmethod
    def __get_order_info__(self, orderPlatformId):
        appInfo = {}
        try:
            TyContext.RunMode.get_server_link(orderPlatformId)
            baseinfo, chargeinfo = TyContext.RedisPayData.execute('HMGET', 'platformOrder:' + str(orderPlatformId),
                                                                  'PAY_STATE_IDEL', 'PAY_STATE_CHARGE')
            baseinfo = json.loads(baseinfo)
            chargeinfo = json.loads(chargeinfo)
            if 'appInfo' in baseinfo and baseinfo['appInfo'] != None:
                appInfo = json.loads(baseinfo['appInfo'])
                if not isinstance(appInfo, dict):
                    appInfo = {}
            if '_time_' in baseinfo and baseinfo['_time_'] != None:
                datetmp = time.strptime(baseinfo['_time_'], '%Y-%m-%d %H:%M:%S.%f')
                appInfo['rtime'] = time.strftime('%Y%m%d%H%M%S', datetmp)
            if 'orderPrice' in baseinfo and baseinfo['orderPrice'] != None:
                appInfo['orderPrice'] = int(baseinfo['orderPrice']) * 100
            try:
                payData = chargeinfo['payData']
                appInfo['serviceid'] = payData['msgOrderCode']
                appInfo['feename'] = payData['orderProdName']
            except:
                pass
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLianTongWCallback->__get_order_info__ error', 'orderPlatformId=', orderPlatformId)
            return appInfo

        # ftlog.info('doLianTongWCallback->__get_order_info__', 'appInfo=',appInfo)
        return appInfo

    @classmethod
    def doLianTongWCallback(self, rpath):

        # 订单验证处理
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouPayLianTongW.doLianTongWCallback->rparam=', rparam)

        if 'serviceid' in rparam and rparam['serviceid'] == 'validateorderid':
            orderstatus = 0
            appname = ''
            feename = ''
            payfee = ''
            appdeveloper = ''
            gameaccount = ''
            macaddress = ''
            appid = ''
            ipaddress = ''
            serviceid = ''
            channelid = ''
            cpid = ''
            ordertime = ''
            imei = ''
            appversion = ''
            xmldata = TyContext.RunHttp.get_body_content()
            try:
                xmlroot = ElementTree.fromstring(xmldata)

                orderid = xmlroot.find('orderid').text
                signMsg = xmlroot.find('signMsg').text
                if len(orderid) == 24:
                    orderPlatformId = orderid[10:]
                    appInfo = self.__get_order_info__(orderPlatformId)
                    if 'appName' in appInfo and appInfo['appName'] != None:
                        appname = appInfo['appName']
                    if 'feename' in appInfo and appInfo['feename'] != None:
                        feename = appInfo['feename']
                    if 'orderPrice' in appInfo and appInfo['orderPrice'] != None:
                        payfee = appInfo['orderPrice']
                    if 'appDeveloper' in appInfo and appInfo['appDeveloper'] != None:
                        appdeveloper = appInfo['appDeveloper']
                    if 'uid' in appInfo and appInfo['uid'] != None:
                        gameaccount = appInfo['uid']
                    if 'mac' in appInfo and appInfo['mac'] != None:
                        macaddress = string.replace(appInfo['mac'], ':', '')
                    if 'woAppId' in appInfo and appInfo['woAppId'] != None:
                        appid = appInfo['woAppId']
                    if 'ip' in appInfo and appInfo['ip'] != None:
                        ipaddress = appInfo['ip']
                    if 'serviceid' in appInfo and appInfo['serviceid'] != None:
                        serviceid = appInfo['serviceid']
                    if 'channelId' in appInfo and appInfo['channelId'] != None:
                        channelid = appInfo['channelId']
                    if 'cpId' in appInfo and appInfo['cpId'] != None:
                        cpid = appInfo['cpId']
                    if 'rtime' in appInfo and appInfo['rtime'] != None:
                        ordertime = appInfo['rtime']
                    if 'imei' in appInfo and appInfo['imei'] != None:
                        imei = appInfo['imei']
                    if 'appversion' in appInfo and appInfo['appversion'] != None:
                        appversion = appInfo['appversion']
                else:
                    orderstatus = 1
                # 签名验证
                tSign = 'orderid=' + orderid + '&Key=' + TuYouPayLianTongW.__get_appkey(cpid)
                vSign = self.__create_md5_sign__(tSign)
                if signMsg != vSign:
                    TyContext.ftlog.info('TuYouPayLianTongW.checkOrder->ERROR, sign error !! sign=', signMsg, 'vSign=',
                                         vSign)
                    orderstatus = 1

            except:
                TyContext.ftlog.exception()
                TyContext.ftlog.info('TuYouPayLianTongW.doLianTongWCallback->ERROR, xmldata error !! xmldata=', xmldata)
                orderstatus = 1

            return TuYouPayLianTongW.XML_CHECKORDER_RET % (
            orderstatus, appname, feename, payfee, appdeveloper, gameaccount, macaddress, appid, ipaddress, serviceid,
            channelid, cpid, ordertime, imei, appversion)

        # 成功回调处理
        xmldata = TyContext.RunHttp.get_body_content()
        # ftlog.info('TuYouPayLianTongW.doLianTongWCallback in xmldata=', xmldata)
        # xmldata = '<callbackReq><orderid>XXX</orderid><ordertime>XXX</ordertime><cpid>XXX</cpid><appid>XXX</appid><fid>XXX</fid><consumeCode>XXX</consumeCode><payfee>XXX</payfee><payType>XXX</payType><hRet>XXX</hRet><status>XXX</status><signMsg>XXX</signMsg></callbackReq>'
        TyContext.ftlog.info('TuYouPayLianTongW.doLianTongWCallback in xmldata=', xmldata)

        try:
            xmlroot = ElementTree.fromstring(xmldata)

            orderid = xmlroot.find('orderid').text
            if len(orderid) == 24:
                orderPlatformId = orderid[10:]
            else:
                orderPlatformId = orderid

            ordertime = xmlroot.find('ordertime').text
            cpid = xmlroot.find('cpid').text

            if xmlroot.find('appid').text:
                appid = xmlroot.find('appid').text
            else:
                # appid = '905608778920130929155624363800'
                appid = ''

            # appid = xmlroot.find('appid').text
            if appid == None:
                appid = ''
            fid = xmlroot.find('fid').text
            consumeCode = xmlroot.find('consumeCode').text
            payfee = int(xmlroot.find('payfee').text)
            payType = int(xmlroot.find('payType').text)
            hRet = int(xmlroot.find('hRet').text)
            status = xmlroot.find('status').text
            signMsg = xmlroot.find('signMsg').text
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('TuYouPayLianTongW.doLianTongWCallback->ERROR, xmldata error !! xmldata=', xmldata)
            return TuYouPayLianTongW.XML_ERRO

        # tSign = 'orderid='+orderPlatformId+'&ordertime='+ordertime+'&cpid='+cpid+'&appid='+appid+'&fid='+fid+'&consumeCode='+consumeCode+'&payfee='+str(payfee)+'&payType='+str(payType)+'&hRet='+str(hRet)+'&status='+status+'&Key='+TuYouPayLianTongW.appkeys[str(appid)]
        TyContext.ftlog.debug('TuYouPayLianTongW.doLianTongWCallback ->', orderid, ordertime, cpid, appid, fid,
                              consumeCode, payfee, payType, hRet, status, TuYouPayLianTongW.__get_appkey(cpid))
        tSign = 'orderid=' + orderid + '&ordertime=' + ordertime + '&cpid=' + cpid + '&appid=' + appid + \
                '&fid=' + fid + '&consumeCode=' + consumeCode + '&payfee=' + str(payfee) + '&payType=' + str(payType) + \
                '&hRet=' + str(hRet) + '&status=' + status + '&Key=' + TuYouPayLianTongW.__get_appkey(cpid)
        vSign = self.__create_md5_sign__(tSign)

        if signMsg != vSign:
            TyContext.ftlog.info('TuYouPayLianTongW.doLianTongWCallback->ERROR, sign error !! sign=', signMsg, 'vSign=',
                                 vSign)
            return TuYouPayLianTongW.XML_ERRO

        # ftlog.info('TuYouPayLianTongW.doLianTongWCallback in orderPlatformId=', orderPlatformId, 'hRet=', hRet, 'status=', status)
        from tysdk.entity.pay.pay import TuyouPay
        notifys = {'xml': xmldata, 'sub_paytype': payType,
                   'pay_appid': appid if appid else 'na',
                   'third_prodid': consumeCode}
        if str(hRet) == '0' and str(status) == '00000':
            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, payfee / 100.0, 'TRADE_FINISHED', notifys)
            if isOk:
                retXml = TuYouPayLianTongW.XML_OK
            else:
                retXml = TuYouPayLianTongW.XML_ERRO
        else:
            TuyouPay.deliveryChargeError(orderPlatformId, notifys, str(hRet) + '|' + str(status), 1)
            retXml = TuYouPayLianTongW.XML_OK

        return retXml

    @classmethod
    def __get_appkey(cls, cpid):
        try:
            extdata = TyContext.PayType.get_pay_type_ext_datas('liantongwo')
            if extdata is not None:
                appkeys = extdata.get('appkeys', {})
                appkey = appkeys.get(cpid, '')
                if appkey is not None:
                    return appkey
        except:
            TyContext.ftlog.exception()

        appkey = cls.appkeys
        return appkey
