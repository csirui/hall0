# -*- coding=utf-8 -*-

from tyframework.context import TyContext

from tysdk.entity.paythird.helper import PayHelper


class MockYee2card(object):
    @classmethod
    def mock(cls, params):
        ''' args: paytype, pay version (v1/v3), platformOrderId, price,
        expect (expected result) '''
        postparams = {}
        postparams['mock'] = '1'
        failcallback = params.get('failcallback', 0)
        if failcallback:
            postparams['status'] = 0
        else:
            postparams['status'] = 1
        postparams['orderid'] = params['platformOrderId']
        postparams['amount'] = str(float(params['price']))
        postparams['yborderid'] = 'yee2orderid123'
        cburl = PayHelper.getSdkDomain() + '/v1/pay/yee2/callback10'
        # use GET instead of POST for now
        response, _ = TyContext.WebPage.webget(cburl, postdata_=postparams)
        return 'yee.card ok'
