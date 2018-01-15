# -*- coding=utf-8 -*-

import hashlib

from tyframework.context import TyContext

datas = {  # price unit: rmb fen
    # 地主
    'T50K': {'price': '500', 'name': '50000金币'},
    'T60K': {'price': '600', 'name': '60000金币'},
    'T80K': {'price': '800', 'name': '80000金币'},
    'T100K': {'price': '1000', 'name': '110000金币'},
    'T300K': {'price': '3000', 'name': '400000金币'},
    'T500K': {'price': '5000', 'name': '700000金币'},
    'T1M': {'price': '10000', 'name': '1500000金币'},
    'T3M': {'price': '30000', 'name': '4500000金币'},
    'T10M': {'price': '100000', 'name': '12000000金币'},
    'RAFFLE': {'price': '500', 'name': '50000金币'},
    'RAFFLE_NEW': {'price': '800', 'name': '80000金币'},
    'VOICE100': {'price': '100', 'name': '语音小喇叭'},
    'MOONKEY': {'price': '200', 'name': '月光之钥'},
    'MOONKEY3': {'price': '300', 'name': '月光之钥X3'},
    'ZHUANYUN': {'price': '500', 'name': '转运礼包'},
    'ZHUANYUN_BIG': {'price': '600', 'name': '转运大礼包'},
    'VIP30': {'price': '3000', 'name': 'VIP（30天）'},
    'PRIVILEGE_30': {'price': '10000', 'name': '会员（30天）'},
    'PVIP': {'price': '3000', 'name': 'VIP普通礼包'},
    'PVIP_BIG': {'price': '5000', 'name': 'VIP豪华礼包'},
    'TEHUI1Y': {'price': '100', 'name': '1元特惠'},
    'CARDMATCH10': {'price': '200', 'name': '参赛券X10'},

    # 德州
    'TEXAS_COIN1': {'price': '200', 'name': u'2万筹码'},
    'TEXAS_COIN6': {'price': '500', 'name': u'5万筹码'},
    'TEXAS_COIN_R6': {'price': '600', 'name': u'6万筹码'},
    'TEXAS_COIN_R8': {'price': '800', 'name': u'8万筹码'},
    'TEXAS_COIN2': {'price': '1000', 'name': u'10万筹码'},
    'TEXAS_COIN_R12': {'price': '1200', 'name': u'12万筹码'},
    'TEXAS_COIN3': {'price': '3000', 'name': u"30万筹码+额外赠3万"},
    'TEXAS_COIN4': {'price': '5000', 'name': u"50万筹码+额外赠5万"},
    'TEXAS_COIN5': {'price': '10000', 'name': u"100万筹码+额外赠15万"},
    'TEXAS_COIN7': {'price': '30000', 'name': u"300万筹码+额外赠45万"},
    'TEXAS_COIN8': {'price': '100000', 'name': u"1000万筹码+额外赠200万"},
    'TEXAS_COIN_LUCKY_R6': {'price': '600', 'name': u"10万"},
    'TEXAS_COIN_LUCKY_R30': {'price': '3000', 'name': u"33万"},
    'TEXAS_COIN_LUCKY_R50': {'price': '5000', 'name': u"55万"},
    'TEXAS_COIN_LUCKY_R100': {'price': '10000', 'name': u"115万"},
    'TEXAS_COIN_LUCKY_R300': {'price': '30000', 'name': u"345万"},
    'TEXAS_COIN_LUCKY_R1000': {'price': '100000', 'name': u"1200万"},
    'TEXAS_VIP1': {'price': '3000', 'name': '会员(30天)'},
    'TEXAS_VIP2': {'price': '10000', 'name': '会员(30天)'},
    'TEXAS_VIP3': {'price': '30000', 'name': '会员(30天)'},
    'TEXAS_VIP4': {'price': '100000', 'name': '会员(30天)'},
    'TEXAS_ITEM_SEND_LED': {'price': '5000', 'name': '喇叭'},
    'TEXAS_ITEM_RENAME_CARD': {'price': '10000', 'name': '改名卡'},

    # 麻将
    "C2": {'name': u"2万金", 'price': "200"},
    "C6": {'name': u"6万金", 'price': "600"},
    "C5": {'name': u"5万金", 'price': "500"},
    "C8": {'name': u"8万金", 'price': "800"},
    "C10": {'name': u"10万金", 'price': "1000"},
    "C30": {'name': u"30万金", 'price': "3000"},
    "C50": {'name': u"50万金", 'price': "5000"},
    "C100": {'name': u"100万金", 'price': "10000"},
    "C300": {'name': u"300万金", 'price': "30000"},
    "C1000": {'name': u"1000万金", 'price': "100000"},
    "C30_MEMBER": {'name': u"周会员, 立得30万, 每天再送3万", 'price': "3000"},
    "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "10000"},
    "C5_RAFFLE": {'name': u"5元礼包", 'price': "500"},
    "C6_RAFFLE": {'name': u"6元礼包", 'price': "600"},
    "C8_RAFFLE": {'name': u"8元礼包", 'price': "800"},
    "C5_LUCKY": {'name': u"5元转运礼包", 'price': "500"},
    "C8_LUCKY": {'name': u"8元转运礼包", 'price': "800"},
    "C10_LUCKY": {'name': u"10元转运礼包", 'price': "1000"},
}

# 盛大
sd_mcpid = "sdlshengqi"
sd_cm = "M3660010"
sd_key = "hongwen"

key_dict = {sd_mcpid: sd_key, }


class TuYouPayRdo(object):
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        orderNo = 'tulvrp' + params['orderPlatformId']
        prodId = params['prodId']
        # data = datas.get(prodId, None)
        data = {}
        data['feeCode'] = '10005001'
        data['price'] = '1'
        if data:
            price = data['price']
            # prodName = data['name']
            feeCode = data['feeCode']
        else:
            raise Exception('can not find rdo product define of prodId=' + prodId)
        payData = {
            'price': price,
            # 'productName':prodName,
            'productId': prodId,
            'feeCode': feeCode,
            'orderNo': orderNo,
            'mcpid': sd_mcpid,
            'cm': sd_cm,
            'key': sd_key,
        }
        bindMobile = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'bindMobile')
        if bindMobile is not None:
            payData['bindMobile'] = bindMobile
        params['payData'] = payData
        mo.setResult('payData', payData)

    @classmethod
    def doRdoCallback(cls, rpath):
        cb_rsp = {}
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            orderNo = rparam['orderNo']
            mcpid = rparam['mcpid']
            feeCode = rparam['feeCode']
            reqtime = rparam['reqtime']
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doRdoCallback->ERROR, param error !! rparam=', rparam)
            return 'param error'

        orderPlatformId = orderNo[6:]
        # 签名校验
        if not cls.__verify_sign(mcpid, feeCode, orderNo, reqtime, sign):
            TyContext.ftlog.error('TuyouPayRdo.doRdoCallback sign verify error !!')
            return 'sign error'

        trade_status = 'TRADE_FINISHED'
        total_fee = -1

        from tysdk.entity.pay.pay import TuyouPay
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee,
                                            trade_status, rparam)
        if isOk:
            return 'prod delivery ok'
        else:
            return 'prod delivery failed'

    @classmethod
    def __verify_sign(cls, mcpid, feeCode, orderNo, reqtime, sign):
        check_str = mcpid + feeCode + orderNo + reqtime + key_dict[mcpid]
        check_sign = hashlib.md5()
        check_sign.update(check_str)
        digest = check_sign.hexdigest().upper()
        if digest != sign:
            TyContext.ftlog.error('TuyouPayRdo verify sign failed: expected sign', sign,
                                  'calculated', digest, 'check_str', check_str)
            return False
        return True
