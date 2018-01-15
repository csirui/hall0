# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
from xml.etree import ElementTree

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaVerify
from tysdk.entity.pay3.constants import PayConst


class TuyouPayTuyouAli(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'chargeType': 'tuyou.ali'}

    @classmethod
    def doPayRequestAli(self, chargeInfo, mi, mo):
        return PayConst.CHARGE_STATE_REQUEST

    @classmethod
    def doAliCallback(self, rpath):
        rparam = PayHelper.getArgsDict()
        TyContext.ftlog.info('doAliCallback->args=', rparam)

        sign = rparam['sign']
        notify_data = rparam['notify_data']
        mock = rparam.get('mock', '')
        # 签名校验
        if not rsaVerify('notify_data=' + notify_data, sign, mock=mock):
            TyContext.ftlog.error('TuyouPayTuyou.doAliCallback rsa verify error !!')
            return 'error'

        xmlroot = ElementTree.fromstring(notify_data)
        trade_status = xmlroot.find('trade_status').text
        total_fee = float(xmlroot.find('total_fee').text)
        subject = xmlroot.find('subject').text
        out_trade_no = xmlroot.find('out_trade_no').text
        trade_no = xmlroot.find('trade_no').text
        nodeTime = xmlroot.find('notify_reg_time')
        if not nodeTime:
            nodeTime = xmlroot.find('gmt_create')
        if nodeTime:
            notify_reg_time = nodeTime.text
        else:
            notify_reg_time = 'not know'

        platformOrderId = out_trade_no
        notifys = {'status': trade_status, 'total_fee': total_fee,
                   'subject': subject, 'out_trade_no': out_trade_no,
                   'notify_reg_time': notify_reg_time, 'trade_no': trade_no,
                   'sign': sign, 'notify_data': notify_data,
                   'chargeType': 'tuyou.ali', 'third_orderid': trade_no}

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
    def doAliCallbackNew(self, rpath):
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
                   'chargeType': 'tuyou.ali', 'third_orderid': trade_no}

        if trade_status == 'TRADE_CLOSED':
            PayHelper.callback_error(platformOrderId, 'TRADE_CLOSED', notifys)
            return 'success'

        if trade_status != 'TRADE_FINISHED' and trade_status != 'TRADE_SUCCESS':
            return 'success'

        isOK = PayHelper.callback_ok(platformOrderId, total_fee, notifys)
        if isOK:
            return 'success'
        else:
            return 'error'
