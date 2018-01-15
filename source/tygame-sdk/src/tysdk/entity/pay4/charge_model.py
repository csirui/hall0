#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class ChargeModel:
    @classmethod
    def save_order(cls, orderId, *datas):
        TyContext.RedisPayData.execute('HMSET', 'sdk.charge:' + orderId, *datas)

    @classmethod
    def get_order(cls, orderId, *keys):
        return TyContext.RedisPayData.execute('HMGET', 'sdk.charge:' + orderId, *keys)

    @classmethod
    def save_charge_info(cls, orderId, key, value):
        chargeInfo = cls.get_order(orderId, ['charge'])
        chargeInfo = chargeInfo[0] if chargeInfo else None
        if not chargeInfo:
            return
        import json
        chargeInfo = json.loads(chargeInfo)
        chargeInfo[key] = value
        datas = ['charge', json.dumps(chargeInfo)]
        cls.save_order(orderId, *datas)

    @classmethod
    def save_third_pay_order_id(cls, tyOrderId, thirdOrderId):
        '''
        保存支付渠道的订单，以供对账使用
        :param tyOrderId:
        :param thirdOrderId:
        :return:
        '''
        cls.save_charge_info(tyOrderId, 'thirdOrderId', thirdOrderId)
