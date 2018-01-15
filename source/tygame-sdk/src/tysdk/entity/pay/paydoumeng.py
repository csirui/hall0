# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tyframework.orderids import orderid

datas = {  # price unit: rmb yuan
    'T50K': {'price': '5', 'name': '50000金币'},
    'T60K': {'price': '6', 'name': '60000金币'},
    'T80K': {'price': '8', 'name': '80000金币'},
    'T100K': {'price': '10', 'name': '110000金币'},
    'T300K': {'price': '30', 'name': '400000金币'},
    'T500K': {'price': '50', 'name': '700000金币'},
    'T1M': {'price': '100', 'name': '1500000金币'},
    'T3M': {'price': '300', 'name': '4500000金币'},
    'T10M': {'price': '1000', 'name': '12000000金币'},
    # 'RAFFLE'       : {'price':'5',    'name':'50000金币'},
    'RAFFLE_NEW': {'price': '8', 'name': '超值礼包'},
    'VOICE100': {'price': '1', 'name': '语音小喇叭'},
    'MOONKEY': {'price': '2', 'name': '月光之钥'},
    'MOONKEY3': {'price': '3', 'name': '月光之钥X3'},
    'ZHUANYUN': {'price': '5', 'name': '转运礼包'},
    'ZHUANYUN_BIG': {'price': '6', 'name': '转运大礼包'},
    'VIP30': {'price': '30', 'name': 'VIP（30天）'},
    'PRIVILEGE_30': {'price': '100', 'name': '会员（30天）'},
    'PVIP': {'price': '30', 'name': 'VIP普通礼包'},
    'PVIP_BIG': {'price': '50', 'name': 'VIP豪华礼包'},
    'TEHUI1Y': {'price': '1', 'name': '1元特惠'},
    'CARDMATCH10': {'price': '2', 'name': '参赛券X10'},

    'TEXAS_COIN1': {'price': '2', 'name': u'2万筹码'},
    'TEXAS_COIN6': {'price': '5', 'name': u'5万筹码'},
    'TEXAS_COIN_R6': {'price': '6', 'name': u'6万筹码'},
    'TEXAS_COIN_R8': {'price': '8', 'name': u'8万筹码'},
    'TEXAS_COIN2': {'price': '10', 'name': u'10万筹码'},
    'TEXAS_COIN_R12': {'price': '10', 'name': u'12万筹码'},
    'TEXAS_COIN3': {'price': '30', 'name': u"30万筹码+额外赠3万"},
    'TEXAS_COIN4': {'price': '50', 'name': u"50万筹码+额外赠5万"},
    'TEXAS_COIN5': {'price': '100', 'name': u"100万筹码+额外赠15万"},
    'TEXAS_COIN7': {'price': '300', 'name': u"300万筹码+额外赠45万"},
    'TEXAS_COIN8': {'price': '1000', 'name': u"1000万筹码+额外赠200万"},
    'TEXAS_COIN_LUCKY_R6': {'price': '6', 'name': u"10万"},
    'TEXAS_COIN_LUCKY_R30': {'price': '30', 'name': u"33万"},
    'TEXAS_COIN_LUCKY_R50': {'price': '50', 'name': u"55万"},
    'TEXAS_COIN_LUCKY_R100': {'price': '100', 'name': u"115万"},
    'TEXAS_COIN_LUCKY_R300': {'price': '300', 'name': u"345万"},
    'TEXAS_COIN_LUCKY_R1000': {'price': '1000', 'name': u"1200万"},
    'TEXAS_VIP1': {'price': '30', 'name': '会员(30天)'},
    'TEXAS_VIP2': {'price': '100', 'name': '会员(30天)'},
    'TEXAS_VIP3': {'price': '300', 'name': '会员(30天)'},
    'TEXAS_VIP4': {'price': '1000', 'name': '会员(30天)'},
    'TEXAS_ITEM_SEND_LED': {'price': '50', 'name': '喇叭'},
    'TEXAS_ITEM_RENAME_CARD': {'price': '100', 'name': '改名卡'},

    "C2": {'name': u"2万金", 'price': "2"},
    "C6": {'name': u"6万金", 'price': "6"},
    "C5": {'name': u"5万金", 'price': "5"},
    "C8": {'name': u"8万金", 'price': "8"},
    "C10": {'name': u"10万金", 'price': "10"},
    "C30": {'name': u"30万金", 'price': "30"},
    "C50": {'name': u"50万金", 'price': "50"},
    "C100": {'name': u"100万金", 'price': "100"},
    "C300": {'name': u"300万金", 'price': "300"},
    "C1000": {'name': u"1000万金", 'price': "1000"},
    "C30_MEMBER": {'name': u"周会员, 立得30万, 每天再送3万", 'price': "30"},
    "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "100"},
    "C5_RAFFLE": {'name': u"5元礼包", 'price': "5"},
    "C6_RAFFLE": {'name': u"6元礼包", 'price': "6"},
    "C8_RAFFLE": {'name': u"8元礼包", 'price': "8"},
    "C5_LUCKY": {'name': u"5元转运礼包", 'price': "5"},
    "C8_LUCKY": {'name': u"8元转运礼包", 'price': "8"},
    "C10_LUCKY": {'name': u"10元转运礼包", 'price': "10"},
}

paycode_dict = {
    # 斗地主商品计费点
    'T50K': '001',
    'T80K': '002',
    'T100K': '003',
    'MOONKEY': '004',
    'MOONKEY3': '005',
    'VOICE100': '006',
    'CARDMATCH10': '007',
    'ZHUANYUN_BIG': '008',
    'RAFFLE_NEW': '009',
}


class TuyouPayDoumeng(object):
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']
        appId = params['appId']

        prodconfig = TyContext.Configure.get_global_item_json('doumeng_prodids', {})
        data = prodconfig[str(appId)].get(prodId, None)
        if data:
            amount = data['price']
            prodName = data['name']
            payCode = data['feecode']
        else:
            raise Exception('can not find doumeng product define of prodId=' + prodId)

        payData = {'amount': amount, 'productId': prodId, 'productName': prodName, 'msgOrderCode': payCode}
        params['payData'] = payData
        mo.setResult('payData', payData)

    @classmethod
    def doDoumengCallback(cls, rpath):
        TyContext.ftlog.info('doDoumengCallback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderPlatformId = rparam['privstr']
            appId = orderid.get_appid_frm_order_id(orderPlatformId)
            paykey_dict = TyContext.Configure.get_global_item_json('doumeng_paykeys', {})
            paykey = str(paykey_dict[str(appId)])
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doDoumengCallback->ERROR, param error !! rparam=', rparam)
            return "fail"

            # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            TyContext.ftlog.error('TuyouPayDoumeng.doDoumengCallback sign verify error !!')
            return "fail"

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            return "ok"
        else:
            return "fail"

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        check_str = (paykey
                     + '&merid=' + rparam['merid']
                     + '&orderid=' + rparam['orderid']
                     + '&ordertime=' + rparam['ordertime']
                     + '&feecode=' + rparam['feecode']
                     + '&privstr=' + rparam['privstr']
                     + '&feestatus=' + rparam['feestatus'])
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuyouPayDoumeng verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
