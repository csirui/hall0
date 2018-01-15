# -*- coding=utf-8 -*-

##############################################
# 同步推ios越狱渠道sdk接入代码
# created by zhangshibo at 2015-09-18
# version: 1.0.8
##############################################

import json
from collections import OrderedDict
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayTongBuTuiV4(PayBaseV4):
    @payv4_order('tongbutui')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/tongbutui/callback')
    def doTongBuTuiPayCallback(cls, rpath):
        success = json.dumps({'status': 'success'})
        fail = json.dumps({'status': 'fail'})
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayTongBuTui->doPayTongBuTuiCallback Request Params: ', params)
        rparam = OrderedDict()
        try:
            rparam['source'] = params['source']
            rparam['trade_no'] = params['trade_no']
            rparam['amount'] = params['amount']
            rparam['partner'] = params['partner']
            rparam['paydes'] = params['paydes']
            rparam['debug'] = params['debug']
            rparam['tborder'] = params['tborder']
            rparam['sign'] = params['sign']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayTongBuTui->doPayTongBuTuiCallback Get Params ERROR. ', e)
            return fail
        # appid = 150918, appkey = rBODan#VKXuF8He2B4Olyn@KhXu8RG2q
        # 获取key,根据partner
        keyvalue = TyContext.Configure.get_global_item_json('tongbutui_config', {})  # 获取同步推的key
        for value in keyvalue:
            if 0 == cmp(value['appid'], params['partner']):
                appkey = value['appkey']
                break
        else:
            TyContext.ftlog.error('TuYouPayHaiMaWan->doHaiMaWanPayCallback get appkey ERROR')
            return 'fail'
        rparam['key'] = appkey
        sign = cls.generate_verifysign(rparam)
        if 0 != cmp(sign, rparam['sign']):
            TyContext.ftlog.error('TuYouPayHaiMaWan->doHaiMaWanPayCallback verify sign ERROR.'
                                  'sign: [%s], verify_sign: [%s]' % (rparam['sign'], sign))
            return fail

        # 通知游戏服发货
        rparam['third_orderid'] = rparam['tborder']
        ChargeModel.save_third_pay_order_id(rparam['trade_no'], rparam['tborder'])
        PayHelperV4.callback_ok(rparam['trade_no'], float(rparam['amount']) / 100, rparam)
        return success

    @classmethod
    def generate_verifysign(cls, rparam):
        check_str = '&'.join([k + '=' + rparam[k] for k in rparam.keys() if k != 'sign'])
        TyContext.ftlog.debug('TuYouPayHaiMaWan->generate_verifysign, Before sign: ', check_str)
        sign = md5(check_str).hexdigest().lower()
        TyContext.ftlog.debug('TuYouPayHaiMaWan->generate_verifysign, After sign: ', sign)
        return sign
