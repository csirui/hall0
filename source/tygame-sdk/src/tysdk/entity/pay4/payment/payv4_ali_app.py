import urllib

from datetime import datetime

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import _sign_with_privatekey_pycrypto, \
    _verify_with_publickey_pycrypto
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayAliAPPV4(PayBaseV4):
    '''
    蚂蚁金服开放平台，应用支付方式
    '''

    @payv4_order('alipay.app')
    def get_order(self, mi):
        chargeInfo = self.get_charge_info(mi)
        ali_appid = mi.getParamStr('ali_appid', '')
        platformOrderId = chargeInfo['platformOrderId']
        config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId, 'alipayapp')
        if not config:
            raise PayErrorV4(1, '请当前包的渠道参数配置')
        alipay_id = config.get('alipay_id')
        alipay_private_key = config.get('alipay_private_key')
        params = {
            'app_id': alipay_id,
            'method': 'alipay.trade.app.pay',
            'format': 'JSON',
            'charset': 'utf-8',
            'sign_type': 'RSA',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'version': '1.0',
            'notify_url': PayHelperV4.getSdkDomain() + '/v1/pay/alinewpay/app/callback'
        }

        biz_content = {
            'subject': chargeInfo['buttonName'],
            'out_trade_no': platformOrderId,
            'timeout_express': '90m',
            'total_amount': '%.2f' % chargeInfo['chargeTotal'],
            'product_code': 'QUICK_MSECURITY_PAY',
            'goods_type': '0',

        }
        import json
        params['biz_content'] = json.dumps(biz_content)
        signStr = '&'.join(k + '=' + str(params[k]) for k in sorted(params))
        params['sign'] = self.rsaAliSign(signStr, alipay_private_key)
        orderStr = '&'.join(k + '=' + urllib.quote(str(params[k])) for k in sorted(params))
        orderStr += '&sign=' + urllib.quote(self.rsaAliSign(signStr, alipay_private_key))
        payData = {
            'ali_config': orderStr
        }
        return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)

    @classmethod
    def rsaAliSign(cls, data, privateKey):
        privateKey = cls.loadRsaPrivateKey(privateKey)
        from Crypto.PublicKey import RSA
        priv_key = RSA.importKey(privateKey)
        return _sign_with_privatekey_pycrypto(data, priv_key)

    @payv4_callback('/open/ve/pay/alinewpay/app/callback')
    def handle_callback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        platformOrderId = rparams['out_trade_no']
        aliOrder = rparams['trade_no']
        config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId, 'alipayapp')
        pubkey = config.get('alipay_publick_key')
        if not self.rsaVerify(self.createLinkString(rparams), rparams['sign'], pubkey):
            return 'failure'
        if rparams['trade_status'] != 'TRADE_SUCCESS' and rparams['trade_status'] != 'TRADE_SUCCESS':
            return 'failure'
        total_fee = rparams['total_amount']
        rparams['third_orderid'] = aliOrder
        ChargeModel.save_third_pay_order_id(platformOrderId, aliOrder)
        PayHelperV4.callback_ok(platformOrderId, total_fee, rparams)
        return 'success'

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
    def rsaVerify(cls, data, sign, pubkey):
        pubkey = cls.loadRsaPublicKey(pubkey)
        from Crypto.PublicKey import RSA
        public_key = RSA.importKey(pubkey)
        return _verify_with_publickey_pycrypto(data, sign, public_key)
