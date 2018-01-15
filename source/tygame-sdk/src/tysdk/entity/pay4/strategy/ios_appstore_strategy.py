#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class TuYooPayIOSAppStoreStrategy:
    def __call__(self, appId, userId, diamondId):
        # 648 & 328 商品第一次购买可以使用appstore，以后只能使用微信支付
        ios_control = TyContext.Configure.get_global_item_json('ios_weinxin_pay_control', {})
        if diamondId in ios_control.get('weixin_products', []):
            wxpay_count = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'wxpay_flag')
            if wxpay_count and int(wxpay_count) >= ios_control.get('wxpay_limit_count', 3):
                return True
        return False
