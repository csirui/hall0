# -*- coding=utf-8 -*-

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaVerify, JUSDK_PUB_KEY, rsa_decrypto_with_publickey
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayJusdkV4(PayBaseV4):
    @payv4_order("jusdk")
    def charge_data(self, mi):
        chargeInfo = self.get_charge_info(mi)
        chargeInfo['chargeData'] = {
            'platformOrderId': chargeInfo['platformOrderId'],
            'notifyUrl': 'http://125.39.218.101:8002/open/ve/pay/jusdk/callback'
        }

        return self.return_mo(0, chargeInfo=chargeInfo)

    @payv4_callback("/open/ve/pay/jusdk/callback")
    def doCallback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        order_id = rparams['dealseq']
        TyContext.ftlog.debug('TuYouPayJusdkV4->doCallback,rparams=', rparams)

        if not self.verify_sign(rparams):
            return 'failed'

        notify_data = rparams['notify_data']
        data = rsa_decrypto_with_publickey(notify_data, JUSDK_PUB_KEY, 1)
        TyContext.ftlog.debug('TuYouPayJusdkV4 -> de rsa notify data = ', data)
        notify_dict = dict((l.split('=') for l in data.split('&')))

        if notify_dict.get('dealseq') != rparams.get('dealseq'):
            TyContext.ftlog.debug('TuYouPayJusdkV4 -> dealseq Different')
            return 'failed'

        if int(notify_dict.get('payresult')) != 0:
            TyContext.ftlog.debug('TuYouPayJusdkV4 -> payresult Different')
            return 'failed'

        is_ok = PayHelperV4.callback_ok(order_id, -1, rparams)
        if is_ok:
            return 'success'
        else:
            TyContext.ftlog.debug('TuYouPayJusdkV4 -> not ok')
            return 'failed'

    def verify_sign(self, rparams):
        sign = rparams.pop('sign')
        data = [(k, v,) for k, v in rparams.iteritems()]
        sorted_data = sorted(data, key=lambda x: x[0], reverse=False)
        list_data = ['%s=%s' % (str(k.encode("utf-8")), str(v.encode("utf-8"))) for k, v in sorted_data]
        text = '&'.join(list_data)
        return rsaVerify(text, sign, 'jusdk')
