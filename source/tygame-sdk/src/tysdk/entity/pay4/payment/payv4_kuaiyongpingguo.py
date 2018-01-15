# -*- coding=utf-8 -*-
import json

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto, _kuaiyongpingguo_pubkey_py, \
    KUAIYONGPINGGUO_PUB_KEY, rsa_decrypto_with_publickey
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayKuaiYongPingGuoV4(PayBaseV4):
    @payv4_order('kuaiyongpingguo')
    def charge_data(cls, mi):
        return cls.handle_order(mi)

    @payv4_callback('/open/ve/pay/kuaiyongpingguo/callback')
    def doKuaiYongPingGuoPayCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayKuaiYongPingGuo->doKuaiYongPingGuoPayCallback  rparam', rparam)

        '''
        uid = rparam['uid']
        subject = rparam['subject']
        version = rparam['version']
        '''

        thirdId = rparam['orderid']
        platformOrderId = rparam['dealseq']
        encryptData = rparam['notify_data']
        sign = rparam['sign']

        verifySign = ''.join([k + '=' + str(rparam[k]) + '&' for k in sorted(rparam.keys()) if k != 'sign'])
        verifySign = verifySign[0:-1]
        TyContext.ftlog.debug('TuYouPayKuaiYongPingGuo->doKuaiYongPingGuoPayCallback  verifySign', verifySign)
        # 公钥验签
        if not _verify_with_publickey_pycrypto(verifySign, sign, _kuaiyongpingguo_pubkey_py):
            TyContext.ftlog.error('TuYouPayKuaiYongPingGuo->doKuaiYongPingGuoPayCallback public verify fail')
            return 'failed'

        # 公钥解密:加载.so文件,python嵌入动态库
        decryptData = rsa_decrypto_with_publickey(encryptData, KUAIYONGPINGGUO_PUB_KEY, 1)
        TyContext.ftlog.debug('TuYouPayKuaiYongPingGuo->doKuaiYongPingGuoPayCallback  decryptData', decryptData)

        # 将dealseq=20130219160809567&fee=0 .01&payresult=0转化为dict结构.
        responseStatus = {}
        attr = decryptData.split('&')
        for param in attr:
            params = param.split('=')
            responseStatus[params[0]] = params[1]
        TyContext.ftlog.debug('TuYouPayKuaiYongPingGuo->doKuaiYongPingGuoPayCallback  responseStatus', responseStatus)

        rparam['third_orderid'] = thirdId
        rparam['chargeType'] = 'kuaiyongpingguo'
        if 0 == int(responseStatus['payresult']):
            total_fee = int(float(responseStatus['fee']))
            chargeKey = 'sdk.charge:' + platformOrderId
            chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
            chargeInfo = json.loads(chargeInfo)
            # 当返回的fee和商品定价不一致时,采用商品本身的价格
            TyContext.ftlog.debug('TuYouPayKuaiYongPingGuo->doKuaiYongPingGuoPayCallback  chargeInfo', chargeInfo,
                                  chargeInfo['chargeTotal'], total_fee)
            if chargeInfo['chargeTotal'] != total_fee:
                total_fee = chargeInfo['chargeTotal']
            ChargeModel.save_third_pay_order_id(platformOrderId, thirdId)
            PayHelperV4.callback_ok(platformOrderId, total_fee, rparam)
            return 'success'
        else:
            errinfo = '支付失败'
            PayHelperV4.callback_error(platformOrderId, errinfo, rparam)
            return 'failed'
