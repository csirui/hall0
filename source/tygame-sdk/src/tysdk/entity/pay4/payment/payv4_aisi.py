# -*- coding=utf-8 -*-
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsa_decrypto_with_publickey, aisi_pubkey_str

######################################################################
# aisi callback过程的主要逻辑实现
# Modified by Zhangshibo at 2015/11/04
# 目前接入的游戏有 途游斗地主,单机斗地主,
# Version:1.0
######################################################################
from tysdk.entity.pay4.charge_model import ChargeModel

from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayAiSiV4(PayBaseV4):
    @payv4_order("aisi")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        TyContext.ftlog.debug('TuYouPayAiSi->chargeinfo', chargeinfo)

        platformOrderId = chargeinfo['platformOrderId']
        chargeTotal = chargeinfo['chargeTotal']
        buttonName = chargeinfo['buttonName']

        chargeinfo['chargeData'] = {'platformOrderId': platformOrderId, 'chargeTotal': chargeTotal,
                                    'buttonName': buttonName}

        TyContext.ftlog.debug('TuYouPayAiSi->chargeData', chargeinfo['chargeData'])
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/aisi/callback")
    def doPayAiSiCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayAiSi->rparam', rparam)
        try:
            orderPlatformId = rparam['billno']
            total_fee = float(rparam['amount'])
            status = int(rparam['status'])
            sign = rparam['sign']
            third_orderid = rparam['order_id']
            appid = rparam['app_id']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayAiSi->doPayAiSiCallback Error: ', e)
            return 'fail'

        # 验签
        if not cls.VerifySign(sign, rparam):
            TyContext.ftlog.error('TuYouPayMiDaShi->doMiDaShiPayCallback Verify sign ERROR!')
            return 'fail'

        rparam['third_orderid'] = third_orderid
        rparam['chargeType'] = 'aisi'
        if status == 0:
            ChargeModel.save_third_pay_order_id(orderPlatformId, third_orderid)
            PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
            return 'success'
        elif status == 1:
            return 'success'
        else:
            errinfo = '支付失败'
            PayHelperV4.callback_error(orderPlatformId, errinfo, rparam)
            return 'fail'

    @classmethod
    def VerifySign(cls, pristr, params):
        try:
            pristr = "".join(pristr.split())
            TyContext.ftlog.debug('TuYouPayAiSi->VerifySign Before decrypt: ', pristr)
            data = rsa_decrypto_with_publickey(pristr, aisi_pubkey_str, 1)
            TyContext.ftlog.debug('TuYouPayAiSi->VerifySign After decrypt: ', data)
            priParam = {}
            for item in data.split('&'):
                tmplist = item.split('=')
                priParam[tmplist[0]] = tmplist[1]
            TyContext.ftlog.debug('TuYouPayAiSi->VerifySign priParam is: ', priParam)
            for item in params:
                if item == 'sign':
                    continue
                if params[item] != priParam[item]:
                    return False
        except Exception as e:
            TyContext.ftlog.error('TuYouPayAiSi->VerifySign Error: ', e)
            return False
        return True
