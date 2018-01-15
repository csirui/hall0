# -*- coding=utf-8 -*-
'''
Created on 2015-5-30

@author: tiancz
'''
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import _import_rsa_key_, \
    _verify_with_publickey_pycrypto


class TuYouPayJinritoutiao(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'fake': ''}
        TyContext.ftlog.debug('TuYouPayJinRiTouTiao charge_data chargeinfo',
                              chargeinfo)

    @classmethod
    def doJinritoutiaoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doJinritoutiaoCallback rparam', rparam)

        try:
            total_fee = int(rparam['total_fee'])
            trade_status = rparam['trade_status']
            orderPlatformId = rparam['out_trade_no']
            appid = rparam['client_id']

        except Exception as e:
            TyContext.ftlog.error('doJinritoutiaoCallback param error, '
                                  'exception', e)
            return 'error'

        configs = TyContext.Configure.get_global_item_json('jinritoutiao_config', {})
        try:
            config = configs[appid]
            public_key = _import_rsa_key_(config['pay_ras_pub_key'])
        except Exception, e:
            TyContext.ftlog.error('doJinritoutiaoCallback config or public_key invalid',
                                  e)
            return 'error'

        if not cls._check_ras_code(public_key, rparam):
            TyContext.ftlog.error('doJinritoutiaoCallback check rsa sign error',
                                  orderPlatformId)
            return 'error'
        if trade_status != '3' and trade_status != '0':
            TyContext.ftlog.error('doJinritoutiaoCallback trade_status ',
                                  trade_status)
            PayHelper.callback_error(orderPlatformId, '支付失败', rparam)
            return 'error'
        PayHelper.callback_ok(orderPlatformId, total_fee / 100.0, rparam)
        return 'success'

    @classmethod
    def _check_ras_code(cls, public_key, rparam):
        TyContext.ftlog.debug('_check_ras_code->', rparam)
        sign = rparam['tt_sign']
        sigdata = "&".join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) \
                           if k != 'tt_sign' and k != 'tt_sign_type')
        TyContext.ftlog.debug('__check_ras_code__ verify ', sign, sigdata, public_key)
        return _verify_with_publickey_pycrypto(sigdata, sign, public_key)
