import json
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayPPZhuShouV4(PayBaseV4):
    @payv4_order('ppzhushou')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        TyContext.ftlog.info('TuYouPayPPZhuShou->chargeinfo', chargeinfo)

        orderNo = chargeinfo['platformOrderId']
        fee = int(chargeinfo['chargeTotal'])
        productDesc = chargeinfo['buttonName']
        notifyUrl = PayHelperV4.getSdkDomain() + '/v1/pay/ppzhushou/callback'

        chargeinfo['chargeData'] = {'orderNo': orderNo, 'fee': fee,
                                    'productDesc': productDesc, 'notifyUrl': notifyUrl}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/ppzhushou/callback')
    def doPPZhuShouPayCallback(cls, rpath):
        postData = TyContext.RunHttp.get_body_content()
        jsondata = json.loads(postData)
        TyContext.ftlog.info('TuYouPayPPZhuShou->jsondata', jsondata)

        param = eval(''.join(str(jsondata).replace('&', '').split()))

        TyContext.ftlog.debug('TuYouPayPPZhuShou->param after eval()', param)
        # 去除字符串中的回车和换行符
        rparams = param['data']
        orderPlatformId = rparams['orderId']
        config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'ppzhushou')
        if config:
            md5key = config.get('PPZHUSHOU_md5key', "")
        else:
            ppzhushouconfig = TyContext.Configure.get_global_item_json('ppzhushou_config', {})
            md5key = ppzhushouconfig['md5key']
        strSign = cls._cal_sign(rparams, md5key)
        TyContext.ftlog.debug('TuYouPayPPZhuShou->strSign', strSign, 'sign', param['sign'])

        total_fee = float(rparams['amount'])
        rparams['third_orderid'] = rparams['tradeId']
        rparams['chargeType'] = 'ppzhushou'

        if strSign == param['sign']:
            if 'S' == rparams['orderStatus']:
                PayHelperV4.callback_ok(orderPlatformId, total_fee, rparams)
                return 'SUCCESS'
            else:
                errorInfo = '错误订单,等待正确订单......'
                TyContext.ftlog.info('TuYouPayPPZhuShou->errorInfo', errorInfo, 'failedDesc', rparams['failedDesc'])
                return 'SUCCESS'

        else:
            errorInfo = '签名校验错误'
            TyContext.ftlog.error('TuYouPayPPZhuShou->errorInfo', errorInfo)
            return 'FAILURE'

    @classmethod
    def _cal_sign(cls, rparams, md5key):
        strSign = ''.join([k + '=' + str(rparams[k]) for k in sorted(rparams.keys())])
        TyContext.ftlog.debug('TuYouPayPPZhuShou->strSign', strSign)
        m = md5()
        m.update(strSign + md5key)
        digest = m.hexdigest().lower()
        return digest
