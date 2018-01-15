# -*- coding=utf-8 -*-

from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.entity.duandai.paycodes import PayCodes
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4
from tysdk.entity.pay_common.platformorder import PlatformOrder


# 回调中的ProvinceID与省份邮编的对应表
#  1, [100000,u"北京"
#  2, [200000,u"上海"
#  3, [30000,u"山西"
#  4, [400000,u"重庆"
#  5, [150000,u"黑龙江"
#  6, [130000,u"吉林"
#  7, [110000,u"辽宁"
#  8, [10000,u"内蒙"
#  9, [50000,u"河北"
# 10, [450000,u"河南"
# 11, [510000,u"广东"
# 12, [430000,u"湖北"
# 13, [250000,u"山东"
# 15, [230000,u"安徽",
# 18, [650000,u"云南"
# 20, [810000,u"青海" #容易跟730000甘肃混
# 23, [410000,u"湖南"
# 24, [350000,u"福建"
# 26, [610000,u"四川"
# 27, [530000,u"广西"
# 28, [550000,u"贵州"
# 29, [570000,u"海南"
# 30, [850000,u"西藏"
# [210000,u"江苏"
# [330000,u"江西"
# [710000,u"陕西"
# [730000,u"甘肃"
# [750000,u"宁夏"
# [300000,u"天津"
# [830000,u"新疆"
# [310000,u"浙江"


class TuYouPayYdMmWeakV4(PayBaseV4):
    # hRet取值说明：
    # 0：成功
    #    当AP成功接收到订单通知时，返回给MM平台。
    #    注意：错单同步中，错单的orderID都是20个0，请应用服务器方返回0
    # 9015：收到重复订单
    #    用于应用服务器已经收到过该订单，但因网络或处理延时，没有及时应答MM平台，
    #    MM平台重发机制再次发送过来的情况。此种情况下，也可直接返回0。
    # 其他值：当MM平台收到其他错误码时，会启动重发机制。

    XML_RET = '''<?xml version="1.0" encoding="UTF-8"?>
<SyncAppOrderResp>
    <MsgType>SyncAppOrderResp</MsgType>
    <Version>1.0.0</Version>
    <hRet>%s</hRet>
</SyncAppOrderResp>
'''

    @payv4_order("ydmm")
    def get_order_info(self, mi):
        chargeinfo = self.get_charge_info(mi)
        chargetype = chargeinfo['chargeType']
        clientId = chargeinfo['clientId']
        paycodes = TyContext.Configure.get_global_item_json('paycodes',
                                                            clientid=clientId)
        buttonId = chargeinfo['buttonId']
        try:
            pdata = paycodes[chargetype]['paydata']
        except Exception as e:
            TyContext.ftlog.error('paycodes', paycodes, 'config error for',
                                  clientId, 'buttonId', buttonId)
            raise PayErrorV4(-1, "找不到%s的MM计费点配置！" % buttonId)

        chargeData = filter(lambda x: x['prodid'] == buttonId, pdata)
        if not chargeData:
            raise PayErrorV4(-1, "找不到%s的MM计费点配置！" % buttonId)
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
    def _get_app_key(cls, ydmm_appid, clientid):
        paycodes = PayCodes(clientid)
        appkey = paycodes.get_appkey('ydmm')
        if appkey:
            TyContext.ftlog.debug('TuYouPayYdMmWeak _get_app_key from paycodes'
                                  ' config', appkey)
            return appkey

        appkey = ''
        try:
            extdata = TyContext.PayType.get_pay_type_ext_datas('ydmm')
            appkey = extdata['appkeys'][ydmm_appid]
        except:
            TyContext.ftlog.exception()
        return appkey

    @classmethod
    def _check_sign(cls, AppID, OrderID, ChannelID, PayCode, MD5Sign, platformOrderId):
        clientId = PlatformOrder(platformOrderId).clientid
        AppKey = cls._get_app_key(AppID, clientId)
        if not AppKey:
            TyContext.ftlog.error('TuYouPayYdMmWeak _check_sign error !! '
                                  'appkey not found for appid', AppID)
            return False
        tSign = OrderID + '#' + ChannelID + '#' + PayCode + '#' + AppKey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest().upper()
        if MD5Sign != vSign:
            TyContext.ftlog.error('TuYouPayYdMmWeak _check_sign error !! '
                                  'sign=', MD5Sign, 'vSign=', vSign)
            return False
        return True

    @payv4_callback("/open/ve/pay/ydmm/callback")
    def doYdMmCallback(cls, rpath):
        xmldata = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback in xmldata=',
                             ''.join(xmldata.splitlines()))
        orderPlatformId = ''
        try:
            xmlroot = ElementTree.fromstring(xmldata)

            # orderPlatformId = xmlroot.find('OrderId').text
            orderPlatformId = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ExData').text
            if not orderPlatformId:
                TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback->ERROR, orderPlatformId error !! xmldata=',
                                     xmldata)
                return TuYouPayYdMmWeakV4.XML_RET % ('1')

            OrderID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}OrderID').text
            #             TradeID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}TradeID').text
            #             ActionTime = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ActionTime').text
            AppID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}AppID').text
            PayCode = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}PayCode').text
            ChannelID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ChannelID').text
            TotalPrice = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}TotalPrice').text  # 单位：分
            MD5Sign = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}MD5Sign').text

        except Exception as e:
            TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback->xmldata error', e)
            return TuYouPayYdMmWeakV4.XML_RET % ('1')

        notifys = {'xml': xmldata, 'chargeType': 'ydmm', 'pay_appid': AppID,
                   'third_orderid': OrderID, 'third_prodid': PayCode}

        ProvinceID = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ProvinceID')
        FeeMSISDN = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}FeeMSISDN')
        OrderType = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}OrderType')
        ReturnStatus = xmlroot.find('{http://www.monternet.com/dsmp/schemas/}ReturnStatus')
        if OrderType is None or OrderType.text == '0':
            TyContext.ftlog.info('doYdMmCallback->isTestOrder: OrderID', OrderID,
                                 'platformOrder', orderPlatformId,
                                 'OrderType', OrderType.text)
            notifys['isTestOrder'] = True
        if FeeMSISDN is not None:
            notifys['third_userid'] = FeeMSISDN.text
        if ProvinceID is not None:
            notifys['third_provid'] = ProvinceID.text

        if OrderID == '0' * len(OrderID):
            errorMessage = cls.StatusMessage(ReturnStatus)
            TyContext.ftlog.info('TuYouPayYdMmWeak.doYdMmCallback->ERROR, failed order: OrderID: [%s], message: [%s]',
                                 (OrderID, errorMessage))
            PayHelperV4.callback_error(orderPlatformId, errorMessage, notifys)
            # 需要回0，否则ydmm会一直重试
            return TuYouPayYdMmWeakV4.XML_RET % ('0')

        if not cls._check_sign(AppID, OrderID, ChannelID, PayCode, MD5Sign,
                               orderPlatformId):
            order = PlatformOrder(orderPlatformId)
            TyContext.ftlog.error(
                'doYdMmCallback check sign failed, might be config error: orderid',
                orderPlatformId, 'userId', order.userid, 'clientId', order.clientid,
                'buttonId', order.buttonid, 'AppID', AppID, 'PayCode', PayCode)
            return TuYouPayYdMmWeakV4.XML_RET % ('1')

        isOk = PayHelperV4.callback_ok(orderPlatformId, float(TotalPrice) / 100.0, notifys)
        # 需要回0，否则ydmm会一直重试
        return TuYouPayYdMmWeakV4.XML_RET % ('0')

    @classmethod
    def StatusMessage(cls, code):
        if not code:
            return '移动代计费失败'
        message = {
            '2026': '余额查询超时',
            '204': '余额不足',
            '2029': '余额鉴权错误',
            '2032': '余额查询返回错误码',
            '2033': '余额查询返回余额非法',
            '2034': '网状网余额查询返回的类型非00000',
            '2035': '网状网余额鉴权balanceEnough非法'
        }
        errormessage = message.get(code, '移动代计费失败')
        return code + ' : ' + errormessage
