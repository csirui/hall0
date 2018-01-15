# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class MockLiantongwo(object):
    xmlrequest_template = '''<?xml version="1.0" encoding="UTF-8"?>
                             <callbackReq>
                                 <orderid>{platformOrderId}</orderid>
                                 <ordertime>20141119003718</ordertime>
                                 <cpid>86009366</cpid>
                                 <appid>9014273345620141028162751391500</appid>
                                 <fid>00018592</fid>
                                 <consumeCode>{payCode}</consumeCode>
                                 <payfee>{price}</payfee>
                                 <payType>2</payType>
                                 <hRet>0</hRet>
                                 <status>{status}</status>
                                 <signMsg>{sign}</signMsg>
                              </callbackReq>'''

    @classmethod
    def __calc_sign(cls, params):
        tSign = 'orderid=0000000000' + params[
            'platformOrderId'] + '&ordertime=20141119003718&cpid=86009366&appid=9014273345620141028162751391500&fid=00018592&consumeCode=' + \
                params['payCode'] + '&payfee=' + str(params['price']) + '&payType=2&hRet=0&status=' + params[
                    'status'] + '&Key=8786914cc07009556fcf'
        m = md5()
        m.update(tSign)
        return m.hexdigest()

    @classmethod
    def mock(cls, params):
        ''' args: paytype, pay version (v1/v3), platformOrderId, payCode
        expect (expected result) '''

        failcallback = params.get('failcallback', 0)
        if failcallback:
            trade_status = '00001'
        else:
            trade_status = '00000'
        params['status'] = trade_status
        cburl = PayHelper.getSdkDomain() + '/v1/pay/liantongw/callback'
        xmldata = cls.xmlrequest_template.format(
            payCode=params['payCode'],
            price=params['price'],
            platformOrderId='0000000000' + params['platformOrderId'],
            status=trade_status,
            sign=cls.__calc_sign(params)
        )
        # use GET instead of POST for now
        response, _ = TyContext.WebPage.webget(cburl, postdata_=xmldata, method_='GET')
        return 'liantongwo ok'
