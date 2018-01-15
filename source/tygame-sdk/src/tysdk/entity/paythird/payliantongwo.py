# -*- coding=utf-8 -*-

import json
import string
import time
from hashlib import md5
from xml.etree import ElementTree

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.duandai.paycodes import PayCodes


# 回调中的provinceid与省份邮编的对应表
# 4040, [200000,u"上海"
# 4041, [650000,u"云南"
# 4042, [10000,u"内蒙"
# 4043, [100000,u"北京"
# 4044, [130000,u"吉林"
# 4045, [610000,u"四川"
# 4046, [300000,u"天津"
# 4047, [750000,u"宁夏"
# 4048, [230000,u"安徽",
# 4049, [250000,u"山东"
# 4050, [30000,u"山西"
# 4051, [510000,u"广东"
# 4052, [530000,u"广西"
# 4053, [830000,u"新疆"
# 4055, [330000,u"江西"
# 4056, [50000,u"河北"  #容易与4043北京混
# 4057, [450000,u"河南"
# 4058, [310000,u"浙江"
# 4059, [570000,u"海南"
# 4060, [430000,u"湖北"
# 4061, [410000,u"湖南"
# 4063, [350000,u"福建"
# 4065, [550000,u"贵州"
# 4066, [110000,u"辽宁"
# 4067, [400000,u"重庆"
# 4068, [710000,u"陕西"
# 4069, [730000,u"甘肃"
# 4070, [150000,u"黑龙江"
# [850000,u"西藏"
# [210000,u"江苏"
# [810000,u"青海" #易与4069甘肃混

class TuYouPayLianTongWo():
    # cpid -> appkey 一个cp只有一个appkey
    appkeys = {
        '86009366': '8786914cc07009556fcf',  # 途游
    }
    XML_OK = '''<?xml version="1.0" encoding="UTF-8"?>
<callbackRsp>1</callbackRsp>
'''
    XML_ERRO = '''<?xml version="1.0" encoding="UTF-8"?>
<callbackRsp>0</callbackRsp>
'''

    XML_CHECKORDER_RET = u'''<?xml version="1.0" encoding="UTF-8"?>
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
    def _calc_md5_sign(cls, tSign):
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        return vSign

    @classmethod
    def _get_order_info(cls, orderPlatformId):
        appInfo = {}
        try:
            TyContext.RunMode.get_server_link(orderPlatformId)
            baseinfo = TyContext.RedisPayData.execute('HGET', 'sdk.charge:' + str(orderPlatformId), 'charge')
            baseinfo = json.loads(baseinfo)
            if 'appInfo' in baseinfo and baseinfo['appInfo'] is not None:
                appInfo = json.loads(baseinfo['appInfo'])
                if not isinstance(appInfo, dict):
                    appInfo = {}
            appInfo['orderPrice'] = int(baseinfo['diamondPrice']) * 100
            appInfo['feename'] = baseinfo['diamondName']
            appInfo['rtime'] = time.strftime('%Y%m%d%H%M%S', time.gmtime())
            appInfo['serviceid'] = baseinfo['chargeData']['msgOrderCode']
            appInfo['clientId'] = baseinfo['clientId']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayLianTongWo _get_order_info failed for'
                                  ' orderPlatformId', orderPlatformId,
                                  'exception', e)

        # TyContext.ftlog.info('doLianTongWoCallback->_get_order_info', 'appInfo=',appInfo)
        return appInfo

    @classmethod
    def _get_appkey(cls, cpid, clientid):
        if clientid:
            paycodes = PayCodes(clientid)
            appkey = paycodes.get_appkey('liantong.wo')
            if appkey:
                TyContext.ftlog.debug('TuYouPayLianTongWo _get_app_key from paycodes'
                                      ' config', appkey)
                return appkey

        try:
            extdata = TyContext.PayType.get_pay_type_ext_datas('liantongwo')
            if extdata is not None:
                appkeys = extdata.get('appkeys', {})
                appkey = appkeys.get(cpid, '')
                if appkey is not None:
                    return appkey
        except:
            TyContext.ftlog.exception()

        appkey = TuYouPayLianTongWo.appkeys.get(cpid, '')
        return appkey

    @classmethod
    def _validate_orderid(cls, rparam):
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
        cpid = '86009366'  # 途游的cpid
        ordertime = ''
        imei = ''
        appversion = ''
        xmldata = TyContext.RunHttp.get_body_content()
        try:
            xmlroot = ElementTree.fromstring(xmldata)

            orderid = xmlroot.find('orderid').text
            signMsg = xmlroot.find('signMsg').text
            if len(orderid) != 24:
                orderstatus = 1
                clientId = ''
            else:
                orderPlatformId = orderid[10:]
                provinceid = xmlroot.find('provinceid')
                if provinceid is not None:
                    TyContext.RedisPayData.execute(
                        'HSET', 'liantongwo:' + str(orderPlatformId),
                        'provinceid', provinceid.text)
                    TyContext.RedisPayData.execute(
                        'EXPIRE', 'liantongwo:' + str(orderPlatformId), 60)
                # cityid = xmlroot.find('cityid')
                # if cityid is not None:
                #    cityid = cityid.text
                appInfo = cls._get_order_info(orderPlatformId)
                clientId = appInfo['clientId']
                if 'serviceid' in appInfo and appInfo['serviceid'] is not None:
                    serviceid = appInfo['serviceid']
                if 'feename' in appInfo and appInfo['feename'] is not None:
                    feename = appInfo['feename']
                if 'orderPrice' in appInfo and appInfo['orderPrice'] is not None:
                    payfee = appInfo['orderPrice']
                if 'appName' in appInfo and appInfo['appName'] is not None:
                    appname = appInfo['appName']
                if 'appDeveloper' in appInfo and appInfo['appDeveloper'] is not None:
                    appdeveloper = appInfo['appDeveloper']
                if 'uid' in appInfo and appInfo['uid'] is not None:
                    gameaccount = appInfo['uid']
                if 'mac' in appInfo and appInfo['mac'] is not None:
                    macaddress = string.replace(appInfo['mac'], ':', '')
                if 'woAppId' in appInfo and appInfo['woAppId'] is not None:
                    appid = appInfo['woAppId']
                if 'ip' in appInfo and appInfo['ip'] is not None:
                    ipaddress = appInfo['ip']
                if 'channelId' in appInfo and appInfo['channelId'] is not None:
                    channelid = appInfo['channelId']
                if 'cpId' in appInfo and appInfo['cpId'] is not None:
                    cpid = appInfo['cpId']
                if 'rtime' in appInfo and appInfo['rtime'] is not None:
                    ordertime = appInfo['rtime']
                if 'imei' in appInfo and appInfo['imei'] is not None:
                    imei = appInfo['imei']
                if 'appversion' in appInfo and appInfo['appversion'] is not None:
                    appversion = appInfo['appversion']

            # 签名验证
            tSign = 'orderid=' + orderid + '&Key=' + TuYouPayLianTongWo._get_appkey(cpid, clientId)
            vSign = cls._calc_md5_sign(tSign)
            if signMsg != vSign:
                TyContext.ftlog.info('TuYouPayLianTongWo.doLianTongWoCallback->ERROR, sign error !! sign=', signMsg,
                                     'vSign=', vSign)
                orderstatus = 1

        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('TuYouPayLianTongWo.doLianTongWoCallback->ERROR, xmldata error !! xmldata=', xmldata)
            orderstatus = 1

        TyContext.ftlog.debug('TuYouPayLianTongWo.doLianTongWoCallback RET',
                              'orderstatus, appname, feename, payfee, appdeveloper, gameaccount, '
                              'macaddress, appid, ipaddress, serviceid, channelid, cpid, ordertime, '
                              'imei, appversion',
                              orderstatus, appname, feename, payfee, appdeveloper, gameaccount,
                              macaddress, appid, ipaddress, serviceid, channelid, cpid, ordertime,
                              imei, appversion)
        return TuYouPayLianTongWo.XML_CHECKORDER_RET % (
            orderstatus, appname, feename, payfee, appdeveloper, gameaccount,
            macaddress, appid, ipaddress, serviceid, channelid, cpid, ordertime,
            imei, appversion)

    @classmethod
    def doLianTongWoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouPayLianTongWo.doLianTongWoCallback->rparam=', rparam)

        # 订单验证处理
        if 'serviceid' in rparam and rparam['serviceid'] == 'validateorderid':
            return cls._validate_orderid(rparam)

        # 成功回调处理
        xmldata = TyContext.RunHttp.get_body_content()
        # xmldata = '<callbackReq><orderid>XXX</orderid><ordertime>XXX</ordertime>
        # <cpid>XXX</cpid><appid>XXX</appid><fid>XXX</fid><consumeCode>XXX</consumeCode>
        # <payfee>XXX</payfee><payType>XXX</payType><hRet>XXX</hRet>
        # <status>XXX</status><signMsg>XXX</signMsg></callbackReq>'
        TyContext.ftlog.info('TuYouPayLianTongWo.doLianTongWoCallback in xmldata=', xmldata)

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
            if appid is None:
                appid = ''
            fid = xmlroot.find('fid').text
            consumeCode = xmlroot.find('consumeCode').text
            payfee = int(xmlroot.find('payfee').text)  # 单位：分
            payType = int(xmlroot.find('payType').text)
            hRet = int(xmlroot.find('hRet').text)
            status = xmlroot.find('status').text
            signMsg = xmlroot.find('signMsg').text
        except Exception as e:
            TyContext.ftlog.info('TuYouPayLianTongWo.doLianTongWoCallback->ERROR, exception', e)
            return TuYouPayLianTongWo.XML_ERRO

        appInfo = cls._get_order_info(orderPlatformId)
        clientId = appInfo.get('clientId', '')

        # tSign = 'orderid='+orderPlatformId+'&ordertime='+ordertime+'&cpid='+cpid
        # +'&appid='+appid+'&fid='+fid+'&consumeCode='+consumeCode
        # +'&payfee='+str(payfee)+'&payType='+str(payType)+'&hRet='+str(hRet)
        # +'&status='+status+'&Key='+TuYouPayLianTongWo.appkeys[str(appid)]
        TyContext.ftlog.debug(
            'TuYouPayLianTongWo.doLianTongWoCallback ->', orderid, ordertime,
            cpid, appid, fid, consumeCode, payfee, payType, hRet, status,
            TuYouPayLianTongWo.appkeys)
        tSign = 'orderid=' + orderid + '&ordertime=' + ordertime + '&cpid=' + cpid + '&appid=' + appid + \
                '&fid=' + fid + '&consumeCode=' + consumeCode + '&payfee=' + str(payfee) + '&payType=' + str(payType) + \
                '&hRet=' + str(hRet) + '&status=' + status + '&Key=' + TuYouPayLianTongWo._get_appkey(cpid, clientId)
        vSign = cls._calc_md5_sign(tSign)

        if signMsg != vSign:
            TyContext.ftlog.info('TuYouPayLianTongWo.doLianTongWoCallback->ERROR, sign error !! sign=', signMsg,
                                 'vSign=', vSign)
            return TuYouPayLianTongWo.XML_ERRO

        # TyContext.ftlog.info('TuYouPayLianTongWo.doLianTongWoCallback in orderPlatformId=', orderPlatformId, 'hRet=', hRet, 'status=', status)
        notifys = {'xml': xmldata, 'chargeType': 'liantong.wo',
                   'pay_appid': appid if appid else 'na',
                   'sub_paytype': payType, 'third_prodid': consumeCode}
        provinceid = TyContext.RedisPayData.execute(
            'HGET', 'liantongwo:' + str(orderPlatformId), 'provinceid')
        if provinceid:
            notifys['third_provid'] = provinceid
        # 联通集成其他短信支付以后status码会出现其他值，
        if str(hRet) == '0':  # and str(status) == '00000' :
            isOk = PayHelper.callback_ok(orderPlatformId, -1, notifys)
            if isOk:
                retXml = TuYouPayLianTongWo.XML_OK
            else:
                retXml = TuYouPayLianTongWo.XML_ERRO
        else:
            PayHelper.callback_error(orderPlatformId, str(hRet) + '|' + str(status), notifys)
            retXml = TuYouPayLianTongWo.XML_OK

        return retXml
