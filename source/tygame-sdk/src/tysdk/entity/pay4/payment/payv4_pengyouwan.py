#! encoding=utf-8
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
from payv4_helper import PayHelperV4
import hashlib
import json

from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.decorator.payv4_order import payv4_order


class TuYouPayPengyouwanV4(PayBaseV4):
    @payv4_order('pengyouwan')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        cls.check_charge_info(mi, chargeinfo)
        config = GameItemConfigure.get_game_channel_configure_by_orderId(chargeinfo['platformOrderId'])
        prodConfig = config.get('products', {})
        diamondList = filter(lambda x: chargeinfo['diamondId'] in x.values(), prodConfig)
        diamondConfig = diamondList[0] if diamondList else {}

        code = diamondConfig.get('feecode', "")
        if not code:
            raise PayErrorV4(1, "找不到计费点")
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId'], 'code': code}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    def check_charge_info(self, mi, chargeinfo):
        '''
        检查计费点有没有配置，
        没有：找所有产品里面不小于当前计费点价格的最小钻石替换充值信息
        :param chargeinfo:
        :return:
        '''
        config = GameItemConfigure.get_game_channel_configure_by_orderId(chargeinfo['platformOrderId'])
        diamondId = chargeinfo['diamondId']
        prodConfig = config.get('products', {})
        diamondList = filter(lambda x: diamondId in x.values(), prodConfig)
        diamondConfig = diamondList[0] if diamondList else {}
        if diamondConfig:
            return
        idSet = set([])
        for v in prodConfig:
            id = v.get('prodId')
            if id:
                idSet.add(id)
        # 配置为空，用其他方式修改 chargeinfo
        if not idSet:
            return
        self.change_chargeinfo(idSet, chargeinfo)

    @payv4_callback('/open/ve/pay/pengyouwan/callback')
    def doCallback(cls, rpath):
        postData = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.debug('TuYouPayPengyouwan->doCallback, postData=', postData)
        try:
            rparams = json.loads(postData)
        except:
            TyContext.ftlog.error('TuYouPayPengyouwan->callback, json error !! postData=', postData)
            return 'error'
        platformOrderId = rparams['cp_orderid']
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('doIDOCallback->ERROR, sign error !! rparam=', rparams)
            return 'error'
        ChargeModel.save_third_pay_order_id(platformOrderId, rparams.get('ch_orderid', ''))
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return '{"ack":200, "msg":"Ok"}'
        else:
            return '{"ack":500, "msg":"Error"}'

    @classmethod
    def check_sign(cls, rparams):
        cp_orderid = rparams['cp_orderid']
        ch_orderid = rparams['ch_orderid']
        amount = rparams['amount']
        gameKey = rparams['gamekey']
        pengyouwan_keys = TyContext.Configure.get_global_item_json('pengyouwan_keys', {})
        try:
            apiSecret = pengyouwan_keys[gameKey]
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(cp_orderid, 'pengyouwan')
            apiSecret = config.get('pyw_payKey', "")
        sign = rparams['sign']
        if sign != hashlib.md5('%s%s%s%s' % (apiSecret, cp_orderid, ch_orderid, amount)).hexdigest():
            return False
        return True
