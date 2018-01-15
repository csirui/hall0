# -*- coding=utf-8 -*-

import json
import string
import time
from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext


class TuYouPay360LianTongW():
    appkeys = '4996dcc43b5be197b588'
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
        payCode = '140610039847'
        orderProdCode = '906364425020140610113843600300002'
        orderProdName = '5万金币'
        if prodId == 'T20K':
            payCode = '140610039846'
            orderProdCode = '906364425020140610113843600300001'
            orderProdName = '2万金币'
        if prodId == 'T50K':
            payCode = '140610039847'
            orderProdCode = '906364425020140610113843600300002'
            orderProdName = '5万金币'
        if prodId == 'T100K':
            payCode = '140610039848'
            orderProdCode = '906364425020140610113843600300003'
            orderProdName = '10万金币'
        if prodId == 'VOICE100':
            payCode = '140610039849'
            orderProdCode = '906364425020140610113843600300004'
            orderProdName = '语音小喇叭100个'
        if prodId == 'MOONKEY3':
            payCode = '140610039850'
            orderProdCode = '906364425020140610113843600300005'
            orderProdName = '月光之钥3个'
        if prodId == 'MOONKEY':
            payCode = '140610039851'
            orderProdCode = '906364425020140610113843600300006'
            orderProdName = '月光之钥1个'
        if prodId == 'CARDMATCH10':
            payCode = '140610039852'
            orderProdCode = '906364425020140610113843600300007'
            orderProdName = '参赛券10张'
        if prodId == 'RAFFLE' or prodId == 'RAFFLE_NEW':
            payCode = '140610039853'
            orderProdCode = '906364425020140610113843600300008'
            orderProdName = '超值礼包'
        if prodId == 'ZHUANYUN':
            payCode = '140610039854'
            orderProdCode = '906364425020140610113843600300009'
            orderProdName = '转运礼包'

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
            baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'PAY_STATE_IDEL')
            baseinfo = json.loads(baseinfo)
            if 'appInfo' in baseinfo and baseinfo['appInfo'] != None:
                appInfo = eval(baseinfo['appInfo'])
            if '_time_' in baseinfo and baseinfo['_time_'] != None:
                datetmp = time.strptime(baseinfo['_time_'], '%Y-%m-%d %H:%M:%S.%f')
                appInfo['rtime'] = time.strftime('%Y%m%d%H%M%S', datetmp)
            if 'orderPrice' in baseinfo and baseinfo['orderPrice'] != None:
                appInfo['orderPrice'] = int(baseinfo['orderPrice']) * 100
            if 'appId' in baseinfo and baseinfo['appId'] != None and 'prodId' in baseinfo and baseinfo[
                'prodId'] != None:
                params = {'appId': baseinfo['appId'], 'prodId': baseinfo['prodId']}
                payData = self.__get_order_code(params)
                if 'msgOrderCode' in payData and payData['msgOrderCode'] != None:
                    appInfo['serviceid'] = payData['msgOrderCode']
                if 'orderProdName' in payData and payData['orderProdName'] != None:
                    appInfo['feename'] = payData['orderProdName']
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
        TyContext.ftlog.info('TuYouPay360LianTongW.doLianTongWCallback->rparam=', rparam)

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
                tSign = 'orderid=' + orderid + '&Key=' + TuYouPay360LianTongW.appkeys
                vSign = self.__create_md5_sign__(tSign)
                if signMsg != vSign:
                    TyContext.ftlog.info('TuYouPay360LianTongW.checkOrder->ERROR, sign error !! sign=', signMsg,
                                         'vSign=', vSign)
                    orderstatus = 1

            except:
                TyContext.ftlog.exception()
                TyContext.ftlog.info('TuYouPay360LianTongW.doLianTongWCallback->ERROR, xmldata error !! xmldata=',
                                     xmldata)
                orderstatus = 1

            return TuYouPay360LianTongW.XML_CHECKORDER_RET % (
            orderstatus, appname, feename, payfee, appdeveloper, gameaccount, macaddress, appid, ipaddress, serviceid,
            channelid, cpid, ordertime, imei, appversion)

        # 成功回调处理
        xmldata = TyContext.RunHttp.get_body_content()
        # ftlog.info('TuYouPay360LianTongW.doLianTongWCallback in xmldata=', xmldata)
        # xmldata = '<callbackReq><orderid>XXX</orderid><ordertime>XXX</ordertime><cpid>XXX</cpid><appid>XXX</appid><fid>XXX</fid><consumeCode>XXX</consumeCode><payfee>XXX</payfee><payType>XXX</payType><hRet>XXX</hRet><status>XXX</status><signMsg>XXX</signMsg></callbackReq>'
        TyContext.ftlog.info('TuYouPay360LianTongW.doLianTongWCallback in xmldata=', xmldata)

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
            TyContext.ftlog.info('TuYouPay360LianTongW.doLianTongWCallback->ERROR, xmldata error !! xmldata=', xmldata)
            return TuYouPay360LianTongW.XML_ERRO

        # tSign = 'orderid='+orderPlatformId+'&ordertime='+ordertime+'&cpid='+cpid+'&appid='+appid+'&fid='+fid+'&consumeCode='+consumeCode+'&payfee='+str(payfee)+'&payType='+str(payType)+'&hRet='+str(hRet)+'&status='+status+'&Key='+TuYouPay360LianTongW.appkeys[str(appid)]
        TyContext.ftlog.debug('TuYouPay360LianTongW.doLianTongWCallback ->', orderid, ordertime, cpid, appid, fid,
                              consumeCode, payfee, payType, hRet, status, TuYouPay360LianTongW.appkeys)
        tSign = 'orderid=' + orderid + '&ordertime=' + ordertime + '&cpid=' + cpid + '&appid=' + appid + \
                '&fid=' + fid + '&consumeCode=' + consumeCode + '&payfee=' + str(payfee) + '&payType=' + str(payType) + \
                '&hRet=' + str(hRet) + '&status=' + status + '&Key=' + TuYouPay360LianTongW.appkeys
        vSign = self.__create_md5_sign__(tSign)

        if signMsg != vSign:
            TyContext.ftlog.info('TuYouPay360LianTongW.doLianTongWCallback->ERROR, sign error !! sign=', signMsg,
                                 'vSign=', vSign)
            return TuYouPay360LianTongW.XML_ERRO

        # ftlog.info('TuYouPay360LianTongW.doLianTongWCallback in orderPlatformId=', orderPlatformId, 'hRet=', hRet, 'status=', status)
        retXml = ''
        from tysdk.entity.pay.pay import TuyouPay
        notifys = {'xml': xmldata}
        if str(hRet) == '0' and str(status) == '00000':
            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', notifys)
            if isOk:
                retXml = TuYouPay360LianTongW.XML_OK
            else:
                retXml = TuYouPay360LianTongW.XML_ERRO
        else:
            TuyouPay.deliveryChargeError(orderPlatformId, notifys, str(hRet) + '|' + str(status), 1)
            retXml = TuYouPay360LianTongW.XML_OK

        return retXml
