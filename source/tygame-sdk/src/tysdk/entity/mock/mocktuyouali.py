# -*- coding=utf-8 -*-

from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaAliSign

from tysdk.entity.paythird.helper import PayHelper


class MockTuyouali(object):
    xmlrequest_template = '''<?xml version="1.0" encoding="UTF-8"?>
<notify>
<trade_status>{status}</trade_status>
<total_fee>{price}</total_fee>
<subject>subject</subject>
<out_trade_no>{platformOrderId}</out_trade_no>
<trade_no>2014102772341078</trade_no>
<notify_reg_time>2014-10-27 14:10:49</notify_reg_time>
</notify>'''

    @classmethod
    def __calc_sign(cls, data):
        return rsaAliSign(data)

    @classmethod
    def mock(cls, params):
        ''' args: paytype, pay version (v1/v3), platformOrderId,
        expect (expected result) '''

        failcallback = params.get('failcallback', 0)
        if failcallback:
            trade_status = 'TRADE_CLOSED'
        else:
            trade_status = 'TRADE_FINISHED'
        cburl = PayHelper.getSdkDomain() + '/v1/pay/alipay/callback'
        xmldata = cls.xmlrequest_template.format(
            platformOrderId=params['platformOrderId'],
            price=float(params['price']),
            status=trade_status,
        )
        postparams = {}
        postparams['notify_data'] = xmldata
        postparams['sign'] = cls.__calc_sign('notify_data=' + xmldata)
        postparams['sign_type'] = "RSA"
        postparams['mock'] = "true"
        # use GET instead of POST for now
        response, _ = TyContext.WebPage.webget(cburl, postdata_=postparams, method_='POST')
        return 'tuyou ali ok'
