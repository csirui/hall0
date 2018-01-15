# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaVerify
from tysdk.entity.pay3.constants import PayConst


class TuyouPayShediaoAli(object):
    @classmethod
    def doPayRequestAli(self, chargeInfo, mi, mo):
        return PayConst.CHARGE_STATE_REQUEST

    @classmethod
    def createLinkString(self, rparam):
        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            # 去掉空值与签名参数后的新签名参数组
            if k != 'sign' and k != 'sign_type' and str(rparam[k]) != '':
                ret = ret + str(k) + '=' + str(rparam[k]) + '&'

        return ret[:-1]

    @classmethod
    def doAliCallback(self, rpath):
        rparam = PayHelper.getArgsDict()
        TyContext.ftlog.info('doAliCallbackNew->args=', rparam)

        sign = rparam['sign']
        notify_data = self.createLinkString(rparam)
        # TyContext.ftlog.info('doAliCallbackNew->notify_data=', notify_data)
        # TyContext.ftlog.info('doAliCallbackNew->sign=', sign)
        # 签名校验
        if not rsaVerify(notify_data, sign, 'shediao'):
            TyContext.ftlog.error('TuyouPayTuyou.doAliCallback rsa verify error !!')
            return 'error'

        trade_status = rparam['trade_status']
        total_fee = rparam['total_fee']
        subject = rparam['subject']
        out_trade_no = rparam['out_trade_no']
        trade_no = rparam['trade_no']

        platformOrderId = out_trade_no
        notifys = {'status': trade_status, 'total_fee': total_fee,
                   'subject': subject, 'out_trade_no': out_trade_no,
                   'trade_no': trade_no, 'sign': sign, 'notify_data': notify_data,
                   'chargeType': 'shediao.ali', 'third_orderid': trade_no}

        if trade_status == 'TRADE_CLOSED':
            PayHelper.callback_error(platformOrderId, 'TRADE_CLOSED', notifys)
            return 'success'

        if trade_status != 'TRADE_FINISHED':
            return 'success'

        isOK = PayHelper.callback_ok(platformOrderId, total_fee, notifys)
        if isOK:
            return 'success'
        else:
            return 'error'
