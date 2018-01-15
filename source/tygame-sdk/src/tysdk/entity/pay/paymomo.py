# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''

from tyframework.context import TyContext


class TuYouPayMomo(object):
    @classmethod
    def doBuyStraight(self, userId, params, mo):
        if params['clientId'] in ['Android_2.97_momo', 'Android_2.98_momo', 'Android_2.99_momo']:
            self.doBuyStraightNew(userId, params, mo)
            return
        prodId = params['prodId']
        payCode = 'com.wemomo.game.ddz.28'
        orderProdName = '6万金币'
        if prodId == 'IOS_T20K':
            orderProdName = '6万金币'
            payCode = 'com.wemomo.game.ddz.28'
        if prodId == 'IOS_T50K':
            orderProdName = '12万金币'
            payCode = 'com.wemomo.game.ddz.29'
        if prodId == 'IOS_T100K':
            orderProdName = '18万金币'
            payCode = 'com.wemomo.game.ddz.30'
        if prodId == 'IOS_T300K':
            orderProdName = '32万金币'
            payCode = 'com.wemomo.game.ddz.31'
        if prodId == 'IOS_T500K':
            orderProdName = '74万金币'
            payCode = 'com.wemomo.game.ddz.32'
        if prodId == 'IOS_T1M':
            orderProdName = '143万金币'
            payCode = 'com.wemomo.game.ddz.33'
        if prodId == 'IOS_MOONKEY3':
            orderProdName = '月光之钥3个'
            payCode = 'com.wemomo.game.ddz.35'
        if prodId == 'IOS_VOICE100':
            orderProdName = '语音小喇叭100个'
            payCode = 'com.wemomo.game.ddz.34'
        if prodId == 'T20K':
            orderProdName = '50000金币'
            payCode = 'com.wemomo.game.ddz.20'
        if prodId == 'T50K':
            orderProdName = '100000金币'
            payCode = 'com.wemomo.game.ddz.21'
        if prodId == 'T100K':
            orderProdName = '300000金币'
            payCode = 'com.wemomo.game.ddz.22'
        if prodId == 'T300K':
            orderProdName = '700000金币'
            payCode = 'com.wemomo.game.ddz.23'
        if prodId == 'T500K':
            orderProdName = '1500000金币'
            payCode = 'com.wemomo.game.ddz.24'
        if prodId == 'T1M':
            orderProdName = '4000000金币'
            payCode = 'com.wemomo.game.ddz.25'
        if prodId == 'VOICE100':
            orderProdName = '语音小喇叭100个'
            payCode = 'com.wemomo.game.ddz.26'
        if prodId == 'CARDNOTE7':
            orderProdName = '7天记牌器'
            payCode = 'com.wemomo.game.ddz.27'
        if prodId == 'MOONKEY3':
            orderProdName = '月光之钥3个'
            payCode = 'com.wemomo.game.ddz.36'
        if prodId == 'CARDMATCH30':
            orderProdName = '参赛券x30'
            payCode = 'com.wemomo.game.ddz.37'
        if prodId == 'ZHUANYUN':
            orderProdName = '转运礼包'
            payCode = 'com.wemomo.game.ddz.38'
        if prodId == 'ZHUANYUN_BIG':
            orderProdName = '转运大礼包'
            payCode = 'com.wemomo.game.ddz.39'
        if prodId == 'IOS_ZHUANYUN':
            orderProdName = '转运礼包'
            payCode = 'com.wemomo.game.ddz.40'
        if prodId == 'IOS_ZHUANYUN_BIG':
            orderProdName = '转运大礼包'
            payCode = 'com.wemomo.game.ddz.41'
        if prodId == 'VIP30':
            orderProdName = 'VIP普通礼包'
            payCode = 'com.wemomo.game.ddz.42'
        if prodId == 'VIP68':
            orderProdName = 'VIP豪华礼包'
            payCode = 'com.wemomo.game.ddz.43'

        if prodId == 'IOS_CARDNOTE7':
            orderProdName = '7天记牌器'
            payCode = 'com.wemomo.game.ddz.45'
        if prodId == 'IOS_VIP30':
            orderProdName = 'VIP普通礼包'
            payCode = 'com.wemomo.game.ddz.46'
        if prodId == 'IOS_VIP68':
            orderProdName = 'VIP豪华礼包'
            payCode = 'com.wemomo.game.ddz.47'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode, 'orderProdName': orderProdName}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doBuyStraightNew(self, userId, params, mo):
        prodId = params['prodId']
        payCode = 'com.wemomo.game.ddz.28'
        orderProdName = '6万金币'
        if prodId == 'IOS_T20K':
            orderProdName = '6万金币'
            payCode = 'com.wemomo.game.ddz.28'
        if prodId == 'IOS_T50K':
            orderProdName = '12万金币'
            payCode = 'com.wemomo.game.ddz.29'
        if prodId == 'IOS_T100K':
            orderProdName = '18万金币'
            payCode = 'com.wemomo.game.ddz.30'
        if prodId == 'IOS_T300K':
            orderProdName = '32万金币'
            payCode = 'com.wemomo.game.ddz.31'
        if prodId == 'IOS_T500K':
            orderProdName = '74万金币'
            payCode = 'com.wemomo.game.ddz.32'
        if prodId == 'IOS_T1M':
            orderProdName = '143万金币'
            payCode = 'com.wemomo.game.ddz.33'
        if prodId == 'IOS_MOONKEY3':
            orderProdName = '月光之钥3个'
            payCode = 'com.wemomo.game.ddz.35'
        if prodId == 'IOS_VOICE100':
            orderProdName = '语音小喇叭100个'
            payCode = 'com.wemomo.game.ddz.34'

        if prodId == 'T300K':
            orderProdName = '300000金币'
            payCode = 'com.wemomo.game.ddz.23'
        if prodId == 'T500K':
            orderProdName = '1500000金币'
            payCode = 'com.wemomo.game.ddz.24'
        if prodId == 'T1M':
            orderProdName = '4000000金币'
            payCode = 'com.wemomo.game.ddz.25'

        if prodId == 'T20K':
            orderProdName = '地主体验礼包'
            payCode = 'com.wemomo.game.ddz.48'
        if prodId == 'T50K':
            orderProdName = '地主特惠礼包'
            payCode = 'com.wemomo.game.ddz.49'
        if prodId == 'T100K':
            orderProdName = '地主豪华礼包'
            payCode = 'com.wemomo.game.ddz.50'
        if prodId == 'VOICE100':
            orderProdName = '语音小喇叭100个'
            payCode = 'com.wemomo.game.ddz.51'
        if prodId == 'CARDNOTE7':
            orderProdName = '7天记牌器'
            payCode = 'com.wemomo.game.ddz.52'
        if prodId == 'MOONKEY3':
            orderProdName = '月光宝盒礼包'
            payCode = 'com.wemomo.game.ddz.53'
        if prodId == 'CARDMATCH30':
            orderProdName = '参赛券*30'
            payCode = 'com.wemomo.game.ddz.54'
        if prodId == 'ZHUANYUN':
            orderProdName = '转运礼包'
            payCode = 'com.wemomo.game.ddz.55'
        if prodId == 'ZHUANYUN_BIG':
            orderProdName = '转运大礼包'
            payCode = 'com.wemomo.game.ddz.56'
        if prodId == 'VIP30':
            orderProdName = 'VIP普通礼包'
            payCode = 'com.wemomo.game.ddz.57'

        if prodId == 'IOS_ZHUANYUN':
            orderProdName = '转运礼包'
            payCode = 'com.wemomo.game.ddz.40'
        if prodId == 'IOS_ZHUANYUN_BIG':
            orderProdName = '转运大礼包'
            payCode = 'com.wemomo.game.ddz.41'
        if prodId == 'VIP68':
            orderProdName = 'VIP豪华礼包'
            payCode = 'com.wemomo.game.ddz.43'

        if prodId == 'IOS_CARDNOTE7':
            orderProdName = '7天记牌器'
            payCode = 'com.wemomo.game.ddz.45'
        if prodId == 'IOS_VIP30':
            orderProdName = 'VIP普通礼包'
            payCode = 'com.wemomo.game.ddz.46'
        if prodId == 'IOS_VIP68':
            orderProdName = 'VIP豪华礼包'
            payCode = 'com.wemomo.game.ddz.47'

        # payCode = '000072803' + payCode
        payData = {'msgOrderCode': payCode, 'orderProdName': orderProdName}
        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def doMomoCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doMomoCallback->rparam=', rparam)

        orderPlatformId = ''
        sign = ''
        trade_no = ''
        try:
            if 'app_trade_no' in rparam:
                orderPlatformId = rparam['app_trade_no']
            if len(orderPlatformId) != 14:
                TyContext.ftlog.info('doMomoCallback->ERROR, orderPlatformId error !! orderPlatformId=',
                                     orderPlatformId)
                return 'fail-app-trade-no'

            # channel_type   string 支付渠道 0-苹果 1-支付宝 2-短信 3-陌陌币 4-网页版
            # channel_type = rparam['channel_type']
            trade_no = rparam['trade_no']
            sign = rparam['sign']
            if trade_no == '' or sign == '':
                TyContext.ftlog.info('doMomoCallback->ERROR, orderPlatformId error !! orderPlatformId=',
                                     orderPlatformId, 'trade_no=', trade_no, 'sign=', sign)
                return 'fail'
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doMomoCallback->ERROR, trade_no error !! trade_no=', trade_no)
            return 'fail'

        trade_status = 'TRADE_FINISHED'
        total_fee = -1

        from tysdk.entity.pay.pay import TuyouPay
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return 'success'
        else:
            return 'fail'
