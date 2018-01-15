# -*- coding=utf-8 -*-


import json
import random

from tyframework.context import TyContext


class MockPay(object):
    __mock_funs__ = {}

    @classmethod
    def mock(cls, _):
        ''' args: paytype, pay version (v1/v3), platformOrderId, smstext,
        delay (before callback), expect (expected result).
        TODO add secret to avoid cheating.
        '''

        params = TyContext.RunHttp.convertArgsToDict()
        try:
            delay = params['delay']
        except:
            delay = 1

        paytype = params['paytype']
        if paytype not in cls.__mock_funs__:
            clsname = 'Mock' + paytype[0].upper() + paytype[1:].replace('.', '').lower()
            mockcls = None  # syntax sugar
            importstr = 'from tysdk.entity.mock.mock%s import %s as mockcls' % (
            paytype.replace('.', '').lower(), clsname)
            TyContext.ftlog.debug('load mockfun:', importstr)
            exec importstr
            mockfun = getattr(mockcls, 'mock')
            cls.__mock_funs__[paytype] = mockfun

        mockfun = cls.__mock_funs__[paytype]
        return mockfun(params)

    @classmethod
    def mockIosVerifyReceipt(cls, _):
        returnparams = {}
        receipt = {}
        returnparams['status'] = '0'
        receipt['product_id'] = 'cn.com.doudizhu.happy.1'
        original_transaction_id = random.randint(100000000000000, 699999999999999)
        receipt['original_transaction_id'] = original_transaction_id
        returnparams['receipt'] = receipt
        return json.dumps(returnparams)
