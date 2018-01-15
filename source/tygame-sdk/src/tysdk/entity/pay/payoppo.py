# -*- coding=utf-8 -*-

from rsacrypto import rsaVerify

from tyframework.context import TyContext


class TuyouPayOppo():
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']

        datas = {'T20K': {'count': '20000', 'name': '金币'},
                 'T50K': {'count': '50000', 'name': '金币'},
                 'T60K': {'count': '60000', 'name': '金币'},
                 'T80K': {'count': '80000', 'name': '金币'},
                 'T100K': {'count': '110000', 'name': '金币'},
                 'T300K': {'count': '400000', 'name': '金币'},
                 'T500K': {'count': '700000', 'name': '金币'},
                 'T1M': {'count': '1500000', 'name': '金币'},
                 'T3M': {'count': '4500000', 'name': '金币'},
                 'T10M': {'count': '12000000', 'name': '金币'},
                 'RAFFLE': {'count': '50000', 'name': '金币'},
                 'RAFFLE_NEW': {'count': '80000', 'name': '金币'},
                 'VOICE100': {'count': '100', 'name': '语音小喇叭'},
                 'MOONKEY': {'count': '1', 'name': '月光之钥'},
                 'MOONKEY3': {'count': '3', 'name': '月光之钥'},
                 'ZHUANYUN': {'count': '100000', 'name': '金币'},
                 'ZHUANYUN_BIG': {'count': '600000', 'name': '金币'},
                 'VIP30': {'count': '1', 'name': 'VIP（30天）'},
                 'PRIVILEGE_30': {'count': '1', 'name': '会员（30天）'},
                 'PVIP': {'count': '1', 'name': 'VIP普通礼包'},
                 'PVIP_BIG': {'count': '1', 'name': 'VIP豪华礼包'},
                 'CARDMATCH10': {'count': '10', 'name': '参赛券'},

                 'TEXAS_COIN1': {'count': '20000', 'name': '筹码'},
                 'TEXAS_COIN6': {'count': '50000', 'name': '筹码'},
                 'TEXAS_COIN_R6': {'count': '60000', 'name': '筹码'},
                 'TEXAS_COIN_R8': {'count': '80000', 'name': '筹码'},
                 'TEXAS_COIN2': {'count': '100000', 'name': '筹码'},
                 'TEXAS_COIN_R12': {'count': '120000', 'name': '筹码'},
                 'TEXAS_COIN3': {'count': '330000', 'name': '筹码'},
                 'TEXAS_COIN4': {'count': '550000', 'name': '筹码'},
                 'TEXAS_COIN5': {'count': '1150000', 'name': '筹码'},
                 'TEXAS_COIN7': {'count': '3450000', 'name': '筹码'},
                 'TEXAS_COIN8': {'count': '12000000', 'name': '筹码'},
                 'TEXAS_COIN_LUCKY_R6': {'count': '100000', 'name': '筹码'},
                 'TEXAS_COIN_LUCKY_R30': {'count': '330000', 'name': '筹码'},
                 'TEXAS_COIN_LUCKY_R50': {'count': '550000', 'name': '筹码'},
                 'TEXAS_COIN_LUCKY_R100': {'count': '1150000', 'name': '筹码'},
                 'TEXAS_COIN_LUCKY_R300': {'count': '3450000', 'name': '筹码'},
                 'TEXAS_COIN_LUCKY_R1000': {'count': '12000000', 'name': '筹码'},
                 'TEXAS_VIP1': {'count': '1', 'name': '会员(30天)'},
                 'TEXAS_VIP2': {'count': '1', 'name': '会员(30天)'},
                 'TEXAS_VIP3': {'count': '1', 'name': '会员(100天)'},
                 'TEXAS_VIP4': {'count': '1', 'name': '会员(1000天)'},
                 'TEXAS_ITEM_SEND_LED': {'count': '1', 'name': '喇叭'},
                 'TEXAS_ITEM_RENAME_CARD': {'count': '1', 'name': '改名卡'},
                 }

        data = datas.get(prodId, None)
        if data:
            oppoCount = data['count']
            oppoProdName = data['name']
        else:
            raise Exception('can not find oppo product define of prodId=' + prodId)
        # payCode = '000072803' + payCode
        payData = {'oppoCount': oppoCount, 'oppoProdName': oppoProdName}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doOppoCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = ''
        try:
            notifyId = rparam['notifyId']
            orderPlatformId = rparam['partnerOrder']

            productName = rparam['productName']
            productDesc = rparam['productDesc']
            price = rparam['price']
            count = rparam['count']
            attach = rparam['attach']
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doOppoCallback->ERROR, param error !! rparam=', rparam)
            return 'result=FAIL&resultMsg=参数错误'

        baseString = 'notifyId=' + notifyId + '&partnerOrder=' + orderPlatformId + '&productName=' + productName + '&productDesc=' + productDesc + '&price=' + str(
            price) + '&count=' + str(count) + '&attach=' + attach
        # 签名校验
        if rsaVerify(baseString, sign, 'oppo') != True:
            TyContext.ftlog.error('TuyouPayOppo.doOppoCallback rsa verify error !!')
            return 'result=FAIL&resultMsg=签名验证失败'

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'

        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            return 'result=OK&resultMsg=成功'
        else:
            return 'result=FAIL&resultMsg=发商品失败'

        pass
