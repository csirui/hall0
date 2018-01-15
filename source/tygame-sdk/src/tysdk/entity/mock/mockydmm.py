# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper
from tysdk.entity.paythird.payydmm import TuYouPayYdMmWeak


class MockYdmm(object):
    orderid = '11130619144434998192'
    fail_orderid = '00000000000000000000'
    xmlrequest_template = '''<?xml version="1.0" encoding="UTF-8"?>
<SyncAppOrderReq xmlns="http://www.monternet.com/dsmp/schemas/">
<TransactionID>CSSP16122856</TransactionID>
<MsgType>SyncAppOrderReq</MsgType>
<Version>1.0.0</Version>
<Send_Address>
<DeviceType>200</DeviceType>
<DeviceID>CSSP</DeviceID>
</Send_Address>
<Dest_Address>
<DeviceType>400</DeviceType>
<DeviceID>SPSYN</DeviceID>
</Dest_Address>
<OrderID>{orderId}</OrderID>
<CheckID>0</CheckID>
<ActionTime>20130619144435</ActionTime>
<ActionID>1</ActionID>
<MSISDN></MSISDN>
<FeeMSISDN>ECAD2EVFADF3AE2A</FeeMSISDN>
<AppID>{appId}</AppID>
<PayCode>{payCode}</PayCode>
<TradeID>L0IF7AF2J4L5IF1B</TradeID>
<Price>100</Price>
<TotalPrice>{totalPrice}</TotalPrice>
<SubsNumb>1</SubsNumb>
<SubsSeq>1</SubsSeq>
<ChannelID>{channelId}</ChannelID>
<ExData>{platformOrderId}</ExData>
<OrderType>1</OrderType>
<MD5Sign>{sign}</MD5Sign>
</SyncAppOrderReq>'''

    @classmethod
    def __calc_sign(cls, params):
        tSign = params['orderId'] + '#' + str(params['channelId']) + '#' + params['payCode'] + '#' + str(
            params['appKey'])
        m = md5()
        m.update(tSign)
        return m.hexdigest().upper()

    @classmethod
    def mock(cls, params):
        ''' args: paytype, pay version (v1/v3), platformOrderId, smstext,
        expect (expected result) '''

        paytype = params['paytype']
        smstext = params['smstext']
        payCode = smstext
        channelId = 1
        appId = payCode[:12]
        appKey = cls.get_app_key(appId)
        params['payCode'] = payCode
        params['appId'] = payCode[:12]
        params['appKey'] = appKey
        params['channelId'] = channelId
        failcallback = params.get('failcallback', 0)
        if failcallback:
            params['orderId'] = cls.fail_orderid
        else:
            params['orderId'] = cls.orderid
        cburl = PayHelper.getSdkDomain() + '/v1/pay/ydmm/callback'
        xmldata = cls.xmlrequest_template.format(
            orderId=params['orderId'],
            appId=params['appId'],
            payCode=params['payCode'],
            totalPrice=params['price'],
            channelId=params['channelId'],
            platformOrderId=params['platformOrderId'],
            sign=cls.__calc_sign(params)
        )
        # use GET instead of POST for now
        response, _ = TyContext.WebPage.webget(cburl, postdata_=xmldata, method_='GET')
        return 'ydmm ok'

    @classmethod
    def get_app_key(cls, ydmm_appid):
        try:
            extdata = TyContext.PayType.get_pay_type_ext_datas('ydmm')
            if extdata is not None:
                appkeys = extdata.get('appkeys', {})
                appkey = appkeys.get(ydmm_appid, None)
                if appkey is not None:
                    return appkey
        except:
            TyContext.ftlog.exception()

        appkey = TuYouPayYdMmWeak.appkeys.get(ydmm_appid, None)
        return appkey
