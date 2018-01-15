# -*- coding=utf-8 -*-
'''
Created on 2015-5-21

@author: tiancz
'''
import json
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayYYGameV4(PayBaseV4):
    @payv4_order('yyduowan')
    def charge_data(cls, mi):
        return cls.handle_order(mi)

    @payv4_callback('/open/ve/pay/yygame/callback')
    def doYYgameCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doYYgameCallback rparam', rparam)
        try:
            total_fee = float(rparam['rmb'])
            subtype = rparam['type']
            account = rparam['account']
            orderid = rparam['orderid']
            orderPlatformId = rparam['cparam']
        except Exception as e:
            TyContext.ftlog.error('doYYgameCallback param error, exception', e)
            return json.dumps({'code': -10, 'data': None})

        if not cls._check_sign(rparam):
            TyContext.ftlog.error('TuYouPayYYGame _check_sign failed')
            return json.dumps({'code': -11, 'data': None})

        rparam['sub_paytype'] = subtype
        PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        cb_response = {'code': 1, 'data': {'orderid': orderid, 'rmb': total_fee
            , 'account': account}}
        TyContext.ftlog.info('doYYgameCallback return', cb_response)
        return json.dumps(cb_response)

    @classmethod
    def _check_sign(cls, rparam):
        game_config = TyContext.Configure.get_global_item_json('yygame_config', {})
        app_key = game_config['app_key']
        try:
            check_str = ''.join([rparam['account'], rparam['orderid'],
                                 rparam['rmb'], rparam['num'], rparam['type'],
                                 rparam['time'], rparam['game'], rparam['server'],
                                 rparam['role'], rparam['itemid'], rparam['price'],
                                 rparam['cparam'], app_key])
        except Exception as e:
            TyContext.ftlog.error('TuYouPayYYGame _check_sign->ERROR, rparam=',
                                  rparam, 'exception', e)
            return False

        m = md5()
        m.update(check_str)
        return m.hexdigest().lower() == rparam['sign']
