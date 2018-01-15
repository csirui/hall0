# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext


class TuYouPayMsgDx():
    appkeys = {'ZT': '8E26F8C036DB449D',  # 斗地主
               'MM': '85C6B6D4BB8C48A5',  # 麻将
               'QC': '5D619FC2CE414DB6',  # 德州
               # 'QZ' : '5D619FC2CE414DB6',  # 德州
               'VW': 'A0910DC2B1D24126',  # 新斗牛
               }

    @classmethod
    def doBuyStraightU(self, userId, params, mo):
        prodId = params['prodId']
        appId = params['appId']

        # 用10元点做缺省值
        payCode = 'wo#pf$'
        orderPhone = '10669202'
        if prodId == 'T20K':
            payCode = 'wo#pd$'
        if prodId == 'CARDMATCH10':
            payCode = 'wo#pm$'
        if prodId == 'T50K':
            payCode = 'wo#pe$'
        if prodId == 'T100K':
            payCode = 'wo#pf$'
        if prodId == 'T300K':
            payCode = 'wo#pg$'
        if prodId == 'MOONKEY':
            payCode = 'wo#pj$'
        if prodId == 'MOONKEY3':
            payCode = 'wo#pk$'
        if prodId == 'RAFFLE':
            payCode = 'wo#pk$'
        if prodId == 'ZHUANYUN' or prodId == 'ZHUANYUN_6' or prodId == 'RAFFLE_6':
            payCode = 'wo#pp$'
        if prodId == 'VOICE100':
            payCode = 'wo#ph$'
        if prodId == 'ZHUANYUN_MEZZO' or prodId == 'RAFFLE_NEW' or prodId == 'T80K':
            payCode = 'wo#rc$'
        if prodId == 'T60K':
            payCode = 'wo#rb$'
        # 麻将
        if prodId == 'C6_RAFFLE':
            payCode = 'wo#adg&'
        if prodId == 'C8_RAFFLE':
            payCode = 'wo#adj&'
        if prodId == 'C8_LUCKY':
            payCode = 'wo#adk&'
        if prodId == 'C10':
            payCode = 'wo#adm&'
        if prodId == 'C2':
            payCode = 'wo#ade&'
        if prodId == 'C6':
            payCode = 'wo#adf&'
        if prodId == 'C8':
            payCode = 'wo#adh&'

        # 德州
        if prodId == 'TEXAS_COIN_LUCKY_R6':
            payCode = 'wo#ahh&'
        if prodId == 'TEXAS_COIN_R6':
            payCode = 'wo#ahf&'
        if prodId == 'TEXAS_COIN2':
            payCode = 'wo#ahg&'
        if prodId == 'TEXAS_COIN_R8':
            payCode = 'wo#aus*'
        if prodId == 'TEXAS_COIN_LUCKY_R8':
            payCode = 'wo#aur*'

        # 新斗牛
        if prodId == 'D100':
            payCode = 'wo#aqw*'
        if prodId == 'D20':
            payCode = 'wo#aqu*'
        if prodId == 'D50':
            payCode = 'wo#aqv*'

        # 除斗地主外，对指令进行服务端组装
        if str(appId) == '7':
            # payCode = payCode + 'MM' + params['orderPlatformId']
            payCode = payCode + 'MM'
        # 德州
        if str(appId) == '8':
            payCode = payCode + 'QC'
        # 新斗牛
        if str(appId) == '10':
            payCode = payCode + 'VW'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode, 'orderPhone': orderPhone}
        params['payData'] = payData
        mo.setResult('payData', payData)

    @classmethod
    def doBuyStraightT(cls, userId, params, mo):
        prodId = params['prodId']
        appId = params['appId']
        prod_price_dict = TyContext.Configure.get_global_item_json('eft_telecom_prod_prices', {})
        prodPrice = prod_price_dict.get(prodId)
        if not prodPrice:
            raise Exception('can not find EFTChinaTelecom product define of prodId=' + prodId)

        telecom_msgcode = TyContext.Configure.get_global_item_json('eft_telecom_msgcode', {})
        payCode, orderPhone = telecom_msgcode[str(prodPrice)]
        # 电信共用一套代码,电信的一套代码  3款产品内用参数都一样
        if str(appId) != '6':
            # payCode = payCode + 'MM' + params['orderPlatformId']
            payCode = payCode + 'ZT'

        payData = {'msgOrderCode': payCode, 'orderPhone': orderPhone}
        params['payData'] = payData
        mo.setResult('payData', payData)

    @classmethod
    def doMsgDxCallback(self, rpath):

        MchNo = TyContext.RunHttp.getRequestParam('MchNo', '')
        Phone = TyContext.RunHttp.getRequestParam('Phone', '')
        Fee = TyContext.RunHttp.getRequestParam('Fee', '')
        OrderId = TyContext.RunHttp.getRequestParam('OrderId', '')
        MobileType = TyContext.RunHttp.getRequestParam('MobileType', '')
        Sign = TyContext.RunHttp.getRequestParam('Sign', '')
        if MchNo == '' or Phone == '' or Fee == '' or OrderId == '' or Sign == '':
            return '401~参数错误~'

        eft_skey = ''
        try:
            eft_appid = OrderId[0:2]
            eft_skey = TuYouPayMsgDx.appkeys.get(eft_appid)
        except:
            TyContext.ftlog.exception()
        tSign = MchNo + Phone + Fee + OrderId + eft_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if Sign != vSign:
            TyContext.ftlog.info('doMsgDxCallback->ERROR, sign error !! sign=', Sign, 'vSign=', vSign, 'eft_skey=',
                                 eft_skey)
            return '555~数字签名错误~'

        # 解密得到原始游戏订单号
        orderPlatformId = ''
        try:
            orderPlatformId = OrderId[2:]
            Fee = int(Fee)
        except:
            TyContext.ftlog.exception()
        TyContext.ftlog.info('TuYouPayMsgDx.doMsgDxCallback orderPlatformId=', orderPlatformId)

        notifys = {'MchNo': MchNo, 'vouchMobile': Phone, 'OrderId': OrderId, 'third_orderid': MchNo}
        if MobileType == 'LT':
            notifys['payType'] = 'EFTChinaUnion.msg'
        elif MobileType == 'DX':
            notifys['payType'] = 'EFTChinaTelecom.msg'
        from tysdk.entity.pay.pay import TuyouPay

        from tysdk.entity.paythird.helper import PayHelper
        PayHelper.set_order_mobile(orderPlatformId, Phone, 'v2')
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, Fee, 'TRADE_FINISHED', notifys)
        if isOk:
            return '000~成功~'
        else:
            return '111~失败~'
