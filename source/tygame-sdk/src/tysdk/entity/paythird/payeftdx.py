# -*- coding=utf-8 -*-


class TuYouPayMsgDx():
    appkeys = {
        'VW': 'A0910DC2B1D24126',  # 新斗牛
        'ZT': '8E26F8C036DB449D',  # 斗地主
        'MM': '85C6B6D4BB8C48A5',  # 麻将
        'QC': '5D619FC2CE414DB6',  # 德州
    }

    @classmethod
    def charge_data(cls, chargeinfo):
        diamondId = chargeinfo['diamondId']
        appId = chargeinfo['appId']
        orderPlatformId = chargeinfo['platformOrderId']
        # 用10元做缺省值
        payCode = '170#HJ47#'
        orderPhone = '1066916504'
        if diamondId == 'D20':
            payCode = 'qz'
            orderPhone = '106605504'
        if diamondId == 'D50':
            payCode = 'cz'
            orderPhone = '106605502'
        if diamondId == 'D100':
            payCode = '170#HJ47#'
            orderPhone = '1066916504'

        # 电信共用一套代码,电信的一套代码  3款产品内用参数都一样
        if str(appId) != '6':
            # payCode = payCode + 'MM' + params['orderPlatformId']
            payCode = payCode + 'ZT'
        smsMsg = payCode + 'ZT' + orderPlatformId

        # type是短信支付的方式，1代表的是发一条短信支付
        smsPayinfo = {'type': '1', 'smsMsg': smsMsg, 'smsPort': orderPhone}
        chargeinfo['chargeData'] = {'issms': 1, 'msgOrderCode': payCode,
                                    'orderPhone': orderPhone, 'smsPayinfo': smsPayinfo}
