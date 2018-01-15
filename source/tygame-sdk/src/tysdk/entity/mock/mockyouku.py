# -*- coding=utf-8 -*-

import hmac
import urllib

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class MockYouku(object):
    @classmethod
    def __calc_callback_sign(cls, rparam):
        paykey_dict = TyContext.Configure.get_global_item_json('youku_paykeys', {})
        paykey = str(paykey_dict[rparam['passthrough']])
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/youku/callback'
        sorted_args = [('apporderID', rparam['apporderID']),
                       ('price', rparam['price']), ('uid', rparam['uid'])]
        encoded_args = urllib.urlencode(sorted_args)
        check_str = notifyurl + '?' + encoded_args
        check_sign = hmac.new(paykey)
        check_sign.update(check_str)
        digest = check_sign.hexdigest()
        return digest

    @classmethod
    def mock(cls, params):
        ''' args: paytype, pay version (v1/v3), platformOrderId, price,
        expect (expected result) '''

        postparams = {}
        postparams['uid'] = '792050'
        postparams['apporderID'] = params['platformOrderId']
        postparams['passthrough'] = '691'
        postparams['price'] = params['price']
        postparams['type'] = '1'
        postparams['sign'] = cls.__calc_callback_sign(postparams)
        cburl = PayHelper.getSdkDomain() + '/v1/pay/youku/callback'
        # use GET instead of POST for now
        response, _ = TyContext.WebPage.webget(cburl, postdata_=postparams)
        return 'youku ok'
