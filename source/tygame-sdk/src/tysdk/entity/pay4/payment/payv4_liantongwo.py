# -*- coding=utf-8 -*-

import string
from hashlib import md5
from xml.etree import ElementTree

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.duandai.paycodes import PayCodes
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYouPayLianTongWoV4(PayBaseV4):
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

    @payv4_order("liantong.wo")
    def get_order_info(self, mi):
        chargeinfo = self.get_charge_info(mi)
        if self.is_out_pay_limit(chargeinfo):
            config = TyContext.Configure.get_global_item_json('smspay_strategy')
            tips = config.get('out_limit_tips', '暂时无法支付，请稍后重试!')
            raise PayErrorV4(1, tips)
        chargetype = chargeinfo['chargeType']
        clientId = chargeinfo['clientId']
        paycodes = TyContext.Configure.get_global_item_json('paycodes',
                                                            clientid=clientId)
        clientip = TyContext.UserSession.get_session_client_ip(chargeinfo['userId'])
        from tysdk.entity.pay_common.fengkong import Fengkong
        if Fengkong.is_ip_limited(clientip, clientId, 'liantong.wo'):
            raise PayErrorV4(
                1, '对不起，您已超出支付限制，请联系客服4008-098-000')
        buttonId = chargeinfo['buttonId']
        try:
            pdata = paycodes[chargetype]['paydata']
        except Exception as e:
            TyContext.ftlog.error('paycodes', paycodes, 'config error for',
                                  clientId, 'buttonId', buttonId)
            raise PayErrorV4(-1, "找不到%s的联通计费点配置！" % buttonId)

        chargeData = filter(lambda x: x['prodid'] == buttonId, pdata)
        if not chargeData:
            raise PayErrorV4(-1, "找不到%s的联通计费点配置！" % buttonId)
        return self.return_mo(0, chargeInfo=chargeinfo, payData=chargeData[0])

    def check_charge_info(self, mi, chargeInfo):
        appId = chargeInfo['appId']
        # packageName = chargeInfo['packageName']
        clientId = chargeInfo['clientId']
        diamondId = chargeInfo['diamondId']
        diamondPrice = chargeInfo['diamondPrice']
        chargetype = chargeInfo['chargeType']
        prodDict = ChargeConfigure.get_prod_dict(appId, clientId=clientId)
        payCodes = TyContext.Configure.get_global_item_json('paycodes', clientid=clientId)
        payData = payCodes[chargetype]['paydata']
        prodList = []
        for data in payData:
            prodid = data['prodid']
            if diamondId == prodid:
                return
            # 单机商品过滤掉
            if prodid.endswith('DJ'):
                continue
            try:
                prodInfo = prodDict[prodid]
            except KeyError:
                continue
            if int(prodInfo.get('is_diamond', 0)) and prodInfo['price'] >= diamondPrice:
                prodList.append(prodInfo)
        if prodList:
            prodList.sort(lambda x, y: cmp(x['price'], y['price']))
            prodInfo = prodList[0]
            chargeInfo['buttonId'] = prodInfo['id']
            chargeInfo['diamondId'] = prodInfo['id']
            chargeInfo['diamondName'] = prodInfo['name']
            chargeInfo['buttonName'] = prodInfo['name']
            chargeInfo['diamondPrice'] = prodInfo['price']
            chargeInfo['chargeTotal'] = prodInfo['price'] * chargeInfo['diamondCount']
            chargeInfo['chargeCoin'] = prodInfo['diamondPrice'] * chargeInfo['diamondCount']

    @classmethod
    def _calc_md5_sign(cls, tSign):
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        return vSign

    @classmethod
    def _get_order_info(cls, orderPlatformId):
        chargeKey = 'sdk.charge:' + orderPlatformId
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        appInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
        return appInfo

    @classmethod
    def _get_appkey(cls, cpid, clientid):
        if clientid:
            paycodes = PayCodes(clientid)
            appkey = paycodes.get_appkey('liantong.wo')
            if appkey:
                TyContext.ftlog.debug('TuYouPayLianTongWoV4 _get_app_key from paycodes'
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

        appkey = TuYouPayLianTongWoV4.appkeys.get(cpid, '')
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
            tSign = 'orderid=' + orderid + '&Key=' + TuYouPayLianTongWoV4._get_appkey(cpid, clientId)
            vSign = cls._calc_md5_sign(tSign)
            if signMsg != vSign:
                TyContext.ftlog.info('TuYouPayLianTongWoV4.doLianTongWoCallback->ERROR, sign error !! sign=', signMsg,
                                     'vSign=', vSign)
                orderstatus = 1

        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('TuYouPayLianTongWoV4.doLianTongWoCallback->ERROR, xmldata error !! xmldata=', xmldata)
            orderstatus = 1

        TyContext.ftlog.debug('TuYouPayLianTongWoV4.doLianTongWoCallback RET',
                              'orderstatus, appname, feename, payfee, appdeveloper, gameaccount, '
                              'macaddress, appid, ipaddress, serviceid, channelid, cpid, ordertime, '
                              'imei, appversion',
                              orderstatus, appname, feename, payfee, appdeveloper, gameaccount,
                              macaddress, appid, ipaddress, serviceid, channelid, cpid, ordertime,
                              imei, appversion)
        return TuYouPayLianTongWoV4.XML_CHECKORDER_RET % (
            orderstatus, appname, feename, payfee, appdeveloper, gameaccount,
            macaddress, appid, ipaddress, serviceid, channelid, cpid, ordertime,
            imei, appversion)

    @payv4_callback("/open/ve/pay/liantongw/callback")
    def doLianTongWoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouPayLianTongWoV4.doLianTongWoCallback->rparam=', rparam)

        # 订单验证处理
        if 'serviceid' in rparam and rparam['serviceid'] == 'validateorderid':
            return cls._validate_orderid(rparam)

        # 成功回调处理
        xmldata = TyContext.RunHttp.get_body_content()
        # xmldata = '<callbackReq><orderid>XXX</orderid><ordertime>XXX</ordertime>
        # <cpid>XXX</cpid><appid>XXX</appid><fid>XXX</fid><consumeCode>XXX</consumeCode>
        # <payfee>XXX</payfee><payType>XXX</payType><hRet>XXX</hRet>
        # <status>XXX</status><signMsg>XXX</signMsg></callbackReq>'
        TyContext.ftlog.info('TuYouPayLianTongWoV4.doLianTongWoCallback in xmldata=', xmldata)

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
            TyContext.ftlog.info('TuYouPayLianTongWoV4.doLianTongWoCallback->ERROR, exception', e)
            return TuYouPayLianTongWoV4.XML_ERRO

        appInfo = cls._get_order_info(orderPlatformId)
        clientId = appInfo.get('clientId', '')

        # tSign = 'orderid='+orderPlatformId+'&ordertime='+ordertime+'&cpid='+cpid
        # +'&appid='+appid+'&fid='+fid+'&consumeCode='+consumeCode
        # +'&payfee='+str(payfee)+'&payType='+str(payType)+'&hRet='+str(hRet)
        # +'&status='+status+'&Key='+TuYouPayLianTongWoV4V4.appkeys[str(appid)]
        TyContext.ftlog.debug(
            'TuYouPayLianTongWoV4V4.doLianTongWoCallback ->', orderid, ordertime,
            cpid, appid, fid, consumeCode, payfee, payType, hRet, status,
            TuYouPayLianTongWoV4.appkeys)
        tSign = 'orderid=' + orderid + '&ordertime=' + ordertime + '&cpid=' + cpid + '&appid=' + appid + \
                '&fid=' + fid + '&consumeCode=' + consumeCode + '&payfee=' + str(payfee) + '&payType=' + str(payType) + \
                '&hRet=' + str(hRet) + '&status=' + status + '&Key=' + TuYouPayLianTongWoV4._get_appkey(cpid, clientId)
        vSign = cls._calc_md5_sign(tSign)

        if signMsg != vSign:
            TyContext.ftlog.info('TuYouPayLianTongWoV4V4.doLianTongWoCallback->ERROR, sign error !! sign=', signMsg,
                                 'vSign=', vSign)
            return TuYouPayLianTongWoV4.XML_ERRO

        # TyContext.ftlog.info('TuYouPayLianTongWoV4.doLianTongWoCallback in orderPlatformId=', orderPlatformId, 'hRet=', hRet, 'status=', status)
        notifys = {'xml': xmldata, 'chargeType': 'liantong.wo',
                   'pay_appid': appid if appid else 'na',
                   'sub_paytype': payType, 'third_prodid': consumeCode}
        provinceid = TyContext.RedisPayData.execute(
            'HGET', 'liantongwo:' + str(orderPlatformId), 'provinceid')
        if provinceid:
            notifys['third_provid'] = provinceid
        # 联通集成其他短信支付以后status码会出现其他值，
        if str(hRet) == '0':  # and str(status) == '00000' :
            isOk = PayHelperV4.callback_ok(orderPlatformId, -1, notifys)
            if isOk:
                retXml = TuYouPayLianTongWoV4.XML_OK
            else:
                retXml = TuYouPayLianTongWoV4.XML_ERRO
        else:
            PayHelperV4.callback_error(orderPlatformId, str(hRet) + '|' + str(status), notifys)
            retXml = TuYouPayLianTongWoV4.XML_OK

        return retXml
