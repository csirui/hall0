# -*- coding=utf-8 -*-
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsa_decrypto_with_publickey, aisi_pubkey_str


######################################################################
# aisi callback过程的主要逻辑实现
# Modified by Zhangshibo at 2015/11/04
# 目前接入的游戏有 途游斗地主,单机斗地主,
# Version:1.0
######################################################################

class TuYouPayAiSi(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        TyContext.ftlog.debug('TuYouPayAiSi->chargeinfo', chargeinfo)

        platformOrderId = chargeinfo['platformOrderId']
        chargeTotal = chargeinfo['chargeTotal']
        buttonName = chargeinfo['buttonName']

        chargeinfo['chargeData'] = {'platformOrderId': platformOrderId, 'chargeTotal': chargeTotal,
                                    'buttonName': buttonName}

        TyContext.ftlog.debug('TuYouPayAiSi->chargeData', chargeinfo['chargeData'])

    @classmethod
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
            PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
            return 'success'
        elif status == 1:
            return 'success'
        else:
            errinfo = '支付失败'
            PayHelper.callback_error(orderPlatformId, errinfo, rparam)
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
