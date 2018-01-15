# -*- coding=utf-8 -*-

import hmac
import types

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class MockYeecard(object):
    merchantKey = "S31ka5Lw8aA256Gum8FA31F5x9F610f5rv529e8p2W0g3kYUMcg587125m1u"

    @classmethod
    def getHmacString(cls, rparam):
        # 易宝仅支持GBK编码
        hstr = ""
        hstr += rparam.get('r0_Cmd', '')
        hstr += rparam.get('r1_Code', '')
        hstr += rparam.get('p1_MerId', '')
        hstr += rparam.get('p2_Order', '')
        hstr += rparam.get('p3_Amt', '')
        hstr += rparam.get('p4_FrpId', '')
        hstr += rparam.get('p5_CardNo', '')
        hstr += rparam.get('p6_confirmAmount', '')
        hstr += rparam.get('p7_realAmount', '')
        hstr += rparam.get('p8_cardStatus', '')
        hstr += rparam.get('p9_MP', '')
        hstr += rparam.get('pb_BalanceAmt', '')
        hstr += rparam.get('pc_BalanceAct', '')
        TyContext.ftlog.debug('MockYeecard getHmacString==', repr(hstr))
        if type(hstr) != types.UnicodeType:
            hstr = unicode(hstr, "utf8")
        sbOld = hstr.encode("GBK")
        mac = hmac.new(cls.merchantKey)
        mac.update(sbOld)
        hmacStr = mac.hexdigest()
        TyContext.ftlog.debug('MockYeecard getHmacString==', repr(hmacStr))
        return hmacStr

    @classmethod
    def mock(cls, params):
        ''' args: paytype, pay version (v1/v3), platformOrderId, price,
        expect (expected result) '''
        postparams = {}
        postparams['r0_Cmd'] = 'ChargeCardDirect'
        postparams['pc_BalanceAct'] = ''
        postparams['p5_CardNo'] = '14128110398186699'
        postparams['p2_Order'] = params['platformOrderId']
        postparams['p9_MP'] = ''
        postparams['pb_BalanceAmt'] = ''
        postparams['p1_MerId'] = '10012097952'
        failcallback = params.get('failcallback', 0)
        if failcallback:
            postparams['r1_Code'] = '0'
            postparams['p8_cardStatus'] = '7'
        else:
            postparams['r1_Code'] = '1'
            postparams['p8_cardStatus'] = '0'
        postparams['p4_FrpId'] = 'SZX'
        postparams['r2_TrxId'] = '315261293636892I'
        postparams['p7_realAmount'] = str(float(params['price']))
        postparams['p3_Amt'] = str(float(params['price']))
        postparams['p6_confirmAmount'] = str(float(params['price']))
        postparams['hmac'] = cls.getHmacString(postparams)
        cburl = PayHelper.getSdkDomain() + '/v1/pay/yee/callback'
        # use GET instead of POST for now
        response, _ = TyContext.WebPage.webget(cburl, postdata_=postparams)
        return 'yee.card ok'
