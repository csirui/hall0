# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class MockZhangyue(object):
    @classmethod
    def __calc_callback_sign(cls, rparam):
        paykey_dict = TyContext.Configure.get_global_item_json('zhangyue_paykeys', {})
        paykey = str(paykey_dict[rparam['appId']])
        transData = rparam['transData']
        check_str = (rparam['merId'] + '|' +
                     rparam['appId'] + '|' +
                     transData['orderId'] + '|' +
                     transData['payAmt'] + '|' +
                     paykey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        return digest

    @classmethod
    def mock(cls, params):
        ''' args: paytype, pay version (v1/v3), platformOrderId, price,
        expect (expected result) '''

        postparams = {}
        transData = {}
        postparams['appId'] = '3e02f7a3e7fd2ca62cc3'
        postparams['merId'] = '691'
        transData['orderId'] = '11133'
        transData['merOrderId'] = params['platformOrderId']
        transData['payAmt'] = params['price']
        postparams['transData'] = transData
        transData['md5SignValue'] = cls.__calc_callback_sign(postparams)
        postparams['transData'] = json.dumps(transData)
        cburl = PayHelper.getSdkDomain() + '/v1/pay/zhangyue/callback'
        # use GET instead of POST for now
        response, _ = TyContext.WebPage.webget(cburl, postdata_=postparams)
        return 'zhangyue ok'
