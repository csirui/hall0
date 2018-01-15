from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayLiebaoV4(PayBaseV4):
    '''
    猎豹移动SDK
    '''

    @payv4_order('liebao')
    def get_order(self, mi):
        chargeInfo = self.get_charge_info(mi)
        payData = {}
        return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)

    @payv4_callback('/open/ve/pay/liebao/callback')
    def handle_callback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        sigStr = '&'.join(k + '=' + rparams[k] for k in sorted(rparams) if k != 'sign' and rparams[k])
        platformOrderId = rparams['cp_order_id']
        config = GameItemConfigure.get_game_channel_configure_by_orderId(platformOrderId, 'liebao')
        md5key = config.get('liebao_key', 'kxkSJClvdDidZ7AOc9T1wGfLQiXd6r8P')
        sigStr += md5key
        from hashlib import md5
        m = md5(sigStr)
        if m.hexdigest().lower() != rparams['sign']:
            return 'fail'
        if rparams['status'] != "2":
            TyContext.ftlog.info("liebao callback fail,status error", rparams['status'])
            return 'fail'
        total_fee = rparams['total_price']
        ChargeModel.save_third_pay_order_id(platformOrderId, rparams['order_id'])
        PayHelperV4.callback_ok(platformOrderId, total_fee, rparams)
        return 'success'
