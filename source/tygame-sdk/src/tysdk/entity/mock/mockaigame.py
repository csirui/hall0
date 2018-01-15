# -*- coding=utf-8 -*-

from hashlib import md5
from xml.etree import ElementTree

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class MockAigame(object):
    appKey = '89df51ef2ece07a06ed513d4c522266f'

    @classmethod
    def __calc_check_sign(cls, params):
        tSign = params['cp_order_id'] + str(params['correlator']) + params['order_time'] + str(
            params['method'] + cls.appKey)
        m = md5()
        m.update(tSign)
        return m.hexdigest()

    @classmethod
    def __calc_callback_sign(cls, params):
        tSign = params['cp_order_id'] + str(params['correlator']) + params['result_code'] + params['fee'] + params[
            'pay_type'] + str(params['method']) + cls.appKey
        m = md5()
        m.update(tSign)
        return m.hexdigest()

    @classmethod
    def mock(cls, params):
        ''' args: paytype, pay version (v1/v3), platformOrderId, price,
        expect (expected result) '''

        failcallback = params.get('failcallback', 0)
        postparams = {}
        postparams['method'] = 'check'
        postparams['cp_order_id'] = params['platformOrderId']
        postparams['correlator'] = 'tuyoomock'
        postparams['order_time'] = '20130619144435'
        postparams['sign'] = cls.__calc_check_sign(postparams)
        cburl = PayHelper.getSdkDomain() + '/v1/pay/aiyouxi/callback/dizhu/tyhall'
        # use GET instead of POST for now
        response, _ = TyContext.WebPage.webget(cburl, postdata_=postparams)
        xmlroot = ElementTree.fromstring(response)
        if_pay = xmlroot.find('if_pay').text
        if int(if_pay) == 0:
            postparams['method'] = 'callback'
            postparams['pay_type'] = 'smsPay'
            if failcallback:
                postparams['result_code'] = '01'
            else:
                postparams['result_code'] = '00'
            postparams['fee'] = params['price']
            postparams['sign'] = cls.__calc_callback_sign(postparams)
            response, _ = TyContext.WebPage.webget(cburl, postdata_=postparams)
        else:
            TyContext.ftlog.info('MockAigame.__check_callback->ERROR, response=', response)
        return 'aigame ok'
