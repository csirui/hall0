# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import copy
import datetime
import json
import urllib

from constants import CHARGE_RATE_RMB
from constants import PAY_STATE_CHARGE
from constants import PAY_STATE_CHARGE_ERROR
from constants import PAY_STATE_CHARGE_OK
from constants import PAY_STATE_CHARGE_WAIT
from constants import PAY_STATE_DELIVERY  # 开始投递货物
from constants import PAY_STATE_DELIVERY_ERROR  # 开始投递货物
from constants import PAY_STATE_DELIVERY_OK  # 交易结束
from constants import PAY_STATE_IDEL  # 初始的状态，开始进行交易
from constants import PAY_STATE_PAY_ERROR
from constants import PAY_STATE_PAY_OK  # 购买成功
from tyframework.context import TyContext
from tysdk.entity.pay_common.orderlog import Order


class TuyouPay(object):
    @classmethod
    def makeBuyChargeMessage(self, mo, datas):
        charge = int(float(datas['orderPrice']))
        mo.setResult('code', 0)
        mo.setResult('orderPlatformId', datas['orderPlatformId'])
        if 'orderName' in datas and datas['orderName'] != '':
            mo.setResult('goodsName', datas['orderName'])
        else:
            mo.setResult('goodsName', u'金币')
        mo.setResult('charge', charge)
        mo.setResult('payType', datas['payType'])
        mo.setResult('payData', '')
        mo.setResult('raffle', int(float(datas['raffle'])))

    @classmethod
    def createTransaction(self, userId, params):
        orderPlatformId = TyContext.ServerControl.makePlatformOrderIdV1(userId, params)
        if orderPlatformId == None:
            orderPlatformId = TyContext.RedisMix.execute('INCR', 'global.platformOrderid')
            orderPlatformId = orderPlatformId % 100
            orderPlatformId = datetime.datetime.now().strftime('%m%d%H%M%S') + \
                              '%02d' % (orderPlatformId)

        params['platformOrderId'] = orderPlatformId
        orderId = params['orderId']
        TyContext.ftlog.info('******** createTransaction in userId=', userId, 'orderId=', orderId, 'orderPlatformId=',
                             orderPlatformId)
        datas = ['userId', userId, 'orderId', orderId]
        TyContext.RedisPayData.execute('HMSET', 'platformOrder:' + orderPlatformId, *datas)
        TyContext.RedisPayData.execute('SET', 'platformOrderGame:' + str(orderId), orderPlatformId)

        self.changeTransState(orderPlatformId, PAY_STATE_IDEL, 'PAY_STATE_IDEL', params)
        return orderPlatformId

    @classmethod
    def changeTransState(self, orderPlatformId, state, paramKey, params):
        ct = datetime.datetime.now()
        params['_time_'] = ct.strftime('%Y-%m-%d %H:%M:%S.%f')
        datas = [paramKey, json.dumps(params), 'state', state]
        TyContext.RedisPayData.execute('HMSET', 'platformOrder:' + orderPlatformId, *datas)

    @classmethod
    def findTransaction(self, orderId):
        orderPlatformId = TyContext.RedisPayData.execute('GET', 'platformOrderGame:' + str(orderId))
        return orderPlatformId

    @classmethod
    def __patch_yeecard_pay(self, userId, payData):
        from tysdk.entity.pay3.request import TuyouPayRequest
        mi = TyContext.Cls_MsgPack()
        mi.setParam('userId', int(userId))
        mi.setParam('appId', payData.get('appId', 6))
        mi.setParam('clientId', payData.get('clientId', ''))
        mi.setParam('chargeType', payData['payType'])
        mi.setParam('platformOrderId', payData['orderId'])
        TyContext.ftlog.info('********** __patch_yeecard_pay mi=', mi)
        return TuyouPayRequest.request(mi)

    @classmethod
    def __patch_linkyun_port_stopped(cls, userId, paydata):
        citycode, _ = TyContext.UserSession.get_session_zipcode(userId)
        provs = TyContext.Configure.get_global_item_json('linkyun_stopped_provs', {})
        TyContext.ftlog.debug('__patch_linkyun_port_stopped userId=', userId, provs, paydata)
        if str(citycode) in provs:
            stop = provs[str(citycode)]['stopped_port']
            newport = provs[str(citycode)]['new_port']
            if 'orderPhone' in paydata and stop == paydata['orderPhone']:
                paydata['orderPhone'] = newport
                paydata['orderVerifyPhone'] = newport
                TyContext.ftlog.debug('__patch_linkyun_port_stopped replaced userId=',
                                      userId, provs[str(citycode)], stop, newport, paydata)

    # 目前只支持Android_2.92_360的YDJD，因为ydjd的代码目前只支持这个
    __ydmm_ydjd_dist = [0, 0]

    @classmethod
    def __ydmm_ydjd_paytype_switch(cls, userId, params):
        ''' return boolean value indicating whether switched to ydjd '''
        try:
            clientId = params['clientId']
            phone_type = TyContext.UserSession.get_session_phone_type(userId)
            if phone_type != TyContext.UserSession.PHONETYPE_CHINAMOBILE:
                return False
            client_share = TyContext.Configure.get_global_item_json(
                'ydjd_percentage_share_with_ydmm', {})
            share = client_share[clientId]
            if userId % 100 < share:
                params['payType'] = 'ydjd'
                TuyouPay.__ydmm_ydjd_dist[1] += 1
                real = 100.0 * TuyouPay.__ydmm_ydjd_dist[1] / sum(TuyouPay.__ydmm_ydjd_dist)
                TyContext.ftlog.info('__ydmm_ydjd_paytype_switch\'ed to ydjd userId=', userId,
                                     '__ydmm_ydjd_dist', TuyouPay.__ydmm_ydjd_dist,
                                     'target share %.1f%%' % share,
                                     'real share %.1f%%' % real)
                return True
            TuyouPay.__ydmm_ydjd_dist[0] += 1
        except:
            return False

    @classmethod
    def __do_buy_straight_w_location_based_duandai(cls, userId, params, mo):
        try:
            prodId = params['prodId']
            appId = params['appId']
            clientId = params['clientId']
            paychanneldict, gamepayitem = TyContext.PayType.get_paydata_by_user(
                appId, userId, prodId, clientId)
            if paychanneldict is None or gamepayitem is None:
                return False
            payData = copy.deepcopy(gamepayitem['paydata'])
            payData['issms'] = 1
            if payData.get('need_short_order_id', 0) == 1:
                orderPlatformId = params['orderPlatformId']
                from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
                shortOrderPlatformId = ShortOrderIdMap.get_short_order_id(orderPlatformId)
                mo.setResult('orderPlatformId', shortOrderPlatformId)
            cls.__patch_linkyun_port_stopped(userId, payData)
            params['payData'] = payData
            mo.setResult('payData', payData)
            if paychanneldict['paytype'] != params['payType']:
                params['payType'] = paychanneldict['paytype']
                mo.setResult('payType', params['payType'])
            return True

        except:
            TyContext.ftlog.exception()
            return False

    @classmethod
    def doBuyStraight(self, userId, params):
        TyContext.ftlog.info('******** doBuyStraight in userId=', userId, 'params=', params)
        orderPlatformId = self.createTransaction(userId, params)
        params['orderPlatformId'] = orderPlatformId
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('straight_charge')

        switched2ydjd = self.__ydmm_ydjd_paytype_switch(userId, params)

        self.makeBuyChargeMessage(mo, params)

        if not switched2ydjd and self.__do_buy_straight_w_location_based_duandai(userId, params, mo):
            TyContext.ftlog.info('******** doBuyStraight out location_based_duandai '
                                 'userId=', userId, 'params=', params, 'mo=', mo.packJson())
            self.changeTransState(orderPlatformId, PAY_STATE_CHARGE, 'PAY_STATE_CHARGE', params)
            Order.log(orderPlatformId, Order.CREATE, userId, params['appId'],
                      params['clientId'], paytype=params['payType'],
                      prodid=params['prodId'], prodOrderId=params['orderId'],
                      pay_appid=Order.get_pay_appid(mo.getResult('paytype'), None, params['clientId']),
                      charge_price=params['orderPrice'])
            return mo

        payType = params['payType']
        if payType == '360.msg':
            from tysdk.entity.pay.pay360 import TuYouPay360
            TuYouPay360.doBuyStraight(userId, params, mo)
        if payType == '360.sns':
            from tysdk.entity.pay.pay360sns import TuYouPay360SNS
            TuYouPay360SNS.doBuyStraight(userId, params, mo)
        if payType == '360.ydmm':
            from tysdk.entity.pay.pay360ydmm import TuYouPay360YdMm
            TuYouPay360YdMm.doBuyStraight(userId, params, mo)
        if payType == '360.liantong.wo':
            from tysdk.entity.pay.pay360liantongwo import TuYouPay360LianTongW
            TuYouPay360LianTongW.doBuyStraight(userId, params, mo)
        if payType == 'yingyonghui.msg':
            from tysdk.entity.pay.payyingyonghui import TuYouPayYingYongHui
            TuYouPayYingYongHui.doBuyStraight(userId, params, mo)
        if payType == 'duoku.msg':
            from tysdk.entity.pay.payduoku import TuYouPayDuoKu
            TuYouPayDuoKu.doBuyStraight(userId, params, mo)
        if payType == 'lenovo':
            from tysdk.entity.pay.paylenovo import TuYouPayLenovo
            TuYouPayLenovo.doBuyStraight(userId, params, mo)
        if payType == 'aibei':
            from tysdk.entity.pay.payaibei import TuYouPayAibei
            TuYouPayAibei.doBuyStraight(userId, params, mo)
        if payType == 'baidu':
            from tysdk.entity.pay.paybaidu import TuYouPayBaidu
            TuYouPayBaidu.doBuyStraight(userId, params, mo)
        if payType == 'yidongmm.msg':
            from tysdk.entity.pay.payyidongmm import TuYouPayYdMm
            TuYouPayYdMm.doBuyStraight(userId, params, mo)
        if payType == 'yidongmmtuyou.msg':
            from tysdk.entity.pay.payyidongmmtuyou import TuYouPayYdMmTy
            TuYouPayYdMmTy.doBuyStraight(userId, params, mo)
        if payType == 'liantong':
            from tysdk.entity.pay.payliantong import TuYouPayLianTong
            TuYouPayLianTong.doBuyStraight(userId, params, mo)
        if payType == 'EFTChinaUnion.msg':
            from tysdk.entity.pay.paymsgdx import TuYouPayMsgDx
            TuYouPayMsgDx.doBuyStraightU(userId, params, mo)
        if payType == 'EFTChinaTelecom.msg':
            from tysdk.entity.pay.paymsgdx import TuYouPayMsgDx
            TuYouPayMsgDx.doBuyStraightT(userId, params, mo)
        if payType == 'tianyi.msg':
            from tysdk.entity.pay.paytianyi import TuYouPayTianYi
            TuYouPayTianYi.doBuyStraight(userId, params, mo)
        if payType == 'momo':
            from tysdk.entity.pay.paymomo import TuYouPayMomo
            TuYouPayMomo.doBuyStraight(userId, params, mo)
        if payType == 'ydmm':
            from tysdk.entity.pay.payydmm import TuYouPayYdMmWeak
            TuYouPayYdMmWeak.doBuyStraight(userId, params, mo)
        if payType == 'ydjd':
            from tysdk.entity.pay.payydjd import TuYouPayYdjd
            TuYouPayYdjd.doBuyStraight(userId, params, mo)
        if payType == 'tuyooios':
            from tysdk.entity.pay.paytuyooios import TuYouPayMyIos
            TuYouPayMyIos.doBuyStraight(userId, params, mo)
        if payType == 'linkyun' or payType == 'linkyununion':
            from tysdk.entity.pay.paylinkyun import TuYouPayLinkYun
            TuYouPayLinkYun.doBuyStraight(userId, params, mo)
            payData = mo.getResult('payData')
            self.__patch_linkyun_port_stopped(userId, payData)
        if payType == 'linkyunltsdk':
            from tysdk.entity.pay.paylinkyun import TuYouPayLinkYun
            TuYouPayLinkYun.doBuyStraightLtsdk(userId, params, mo)
        if payType == 'linkyundx':
            from tysdk.entity.pay.paylinkyun import TuYouPayLinkYun
            TuYouPayLinkYun.doBuyStraightDx(userId, params, mo)
        if payType == 'nearme':
            from tysdk.entity.pay.payoppo import TuyouPayOppo
            TuyouPayOppo.doBuyStraight(userId, params, mo)
        if payType == 'huafubao':
            from tysdk.entity.pay.payhuafubao import TuyouPayHuafubao
            TuyouPayHuafubao.doBuyStraight(userId, params, mo)
        if payType == 'youku':
            from tysdk.entity.pay.payyouku import TuyouPayYouku
            TuyouPayYouku.doBuyStraight(userId, params, mo)
        if payType == 'liantong.wo':
            from tysdk.entity.pay.payliantongw import TuYouPayLianTongW
            TuYouPayLianTongW.doBuyStraight(userId, params, mo)
        if payType == 'yee2':
            from tysdk.entity.pay.payyee2 import TuYouPayYee2
            TuYouPayYee2.doBuyStraight(userId, params, mo)
        if payType == 'zhangqu':
            from tysdk.entity.pay.payzhangqu import TuYouPayZhangQu
            TuYouPayZhangQu.doBuyStraight(userId, params, mo)
        if payType == 'huawei':
            from tysdk.entity.pay.payhuawei import TuyouPayHuaWei
            TuyouPayHuaWei.doBuyStraight(userId, params, mo)
        if payType == 'zhuowangMdo':
            from tysdk.entity.pay.payzhuowang import TuYouPayZhuoWang
            TuYouPayZhuoWang.doBuyStraight(userId, params, mo)
        if payType == 'rdo':
            from tysdk.entity.pay.payrdo import TuYouPayRdo
            TuYouPayRdo.doBuyStraight(userId, params, mo)
        if payType == 'qtld':
            from tysdk.entity.pay.payqtld import TuyouPayQtld
            TuyouPayQtld.doBuyStraight(userId, params, mo)
        if payType == '114':
            from tysdk.entity.pay.pay114 import TuyouPay114
            TuyouPay114.doBuyStraight(userId, params, mo)
        if payType == 'doumeng':
            from tysdk.entity.pay.paydoumeng import TuyouPayDoumeng
            TuyouPayDoumeng.doBuyStraight(userId, params, mo)
        if payType == 'linkyun.ido':
            from tysdk.entity.pay.payido import TuyouPayIDO
            TuyouPayIDO.doBuyStraight(userId, params, mo)
        if payType == '360pay':
            from tysdk.entity.pay.pay360pay import TuyouPay360pay
            TuyouPay360pay.doBuyStraight(userId, params, mo)
        if payType == 'xiaomi.danji':
            from tysdk.entity.pay.payxiaomi import TuyouPayXiaomi
            TuyouPayXiaomi.doBuyStraight(userId, params, mo)
        if payType == 'aigame':
            # nothing to do besides sending platform orderid
            pass

        TyContext.ftlog.info('********** doBuyStraight out userId=', userId, 'params=', params, 'mo=', mo.packJson())
        self.changeTransState(orderPlatformId, PAY_STATE_CHARGE, 'PAY_STATE_CHARGE', params)
        Order.log(orderPlatformId, Order.CREATE, userId, params['appId'],
                  params['clientId'], paytype=params['payType'],
                  prodid=params['prodId'], prodOrderId=params['orderId'],
                  pay_appid=Order.get_pay_appid(payType, None, params['clientId']),
                  charge_price=params['orderPrice'])
        return mo

    @classmethod
    def doBuyCharge(self, userId, params):
        TyContext.ftlog.info('********** doBuyChanrge in params=', params)
        # 2014-12-05 修复客户端Android 3.33版本之前的3.0版本银联卡支付调用charge接口的bug
        if int(params['appId']) < 10000 and not params['orderId'].startswith('GO') and params['payType'].startswith(
                'yee2'):
            return self.__patch_yeecard_pay(userId, params)

        orderPlatformId = self.createTransaction(userId, params)
        params['orderPlatformId'] = orderPlatformId
        self.changeTransState(orderPlatformId, PAY_STATE_CHARGE, 'PAY_STATE_CHARGE', params)

        mo = self.doBuyChargeTuyouCoin(userId, params)
        if mo != None:
            return mo

        payType = params['payType']
        # 途游自己的支付宝支付和神州付
        from tysdk.entity.pay.paytuyou import TuyouPayTuyou
        if payType == 'tuyou.ali':
            mo = TuyouPayTuyou.doPayRequestAli(params)

        from tysdk.entity.pay.paywx import TuyouPayWXpay
        if payType == 'wxpay':
            mo = TuyouPayWXpay.doPayRequestWx(params)

        from tysdk.entity.pay.paymo9 import TuyouPayMo9pay
        if payType == 'mo9pay':
            params['userId'] = userId
            mo = TuyouPayMo9pay.doPayRequestMo9(params)

        if payType == 'tuyou.card.dx':
            mo = self.doPhoneCardPay(userId, params, 'dx', 'tuyoo')

        if payType == 'tuyou.card.yd':
            mo = self.doPhoneCardPay(userId, params, 'yd', 'tuyoo')

        if payType == 'tuyou.card.lt':
            mo = self.doPhoneCardPay(userId, params, 'lt', 'tuyoo')

        if payType == 'tuyou.caifutong':
            mo = TuyouPayTuyou.doPayRequestCaiFuTong(params)

        if payType == 'tuyou.msgyd':
            from tysdk.entity.pay.paymsgyd import TuYouPayMsgYd
            mo = TuYouPayMsgYd.doMsgYdRequest(params)

        if payType == 'tuyou.msgdx':
            # from tysdk.entity.pay.paymsgdx import TuYouPayMsgDx
            # mo = TuYouPayMsgDx.doMsgDxRequest( params)
            pass

        if payType == 'laohu.msg':
            from tysdk.entity.pay.paylaohu import TuYouPayLaoHu
            mo = TuYouPayLaoHu.doLaoHuCallback(params)

        # 爱游戏短信充值和其他充值
        if payType == 'aigame.msg' or payType == 'aigame':
            TyContext.ftlog.info('doBuyCharge WHO_IS_USING_THIS!!')
            from tysdk.entity.pay.payaigame import TuYouPayAiGame
            if payType == 'aigame.msg':
                mo = TuYouPayAiGame.doAiGameMsgCallback(params)
            if payType == 'aigame':
                mo = TuYouPayAiGame.doAiGameCallback(params)

        # 360的支付宝支付和神州付
        from tysdk.entity.pay.pay360 import TuYouPay360
        if payType == '360.ali':
            mo = TuYouPay360.doPayRequestAli(params)

        if payType == '360.card.dx':
            mo = TuYouPay360.doPayRequestCardDx(params)

        if payType == '360.card.yd':
            mo = TuYouPay360.doPayRequestCardYd(params)

        if payType == '360.card.lt':
            mo = TuYouPay360.doPayRequestCardLt(params)

        # 小米支付
        if payType == 'xiaomi.common':
            from tysdk.entity.pay.payxiaomi import TuyouPayXiaomi
            mo = TuyouPayXiaomi.doPayRequestXiaomiCommon(params)

        # 易宝支付
        if payType == 'yee.card':
            from tysdk.entity.pay.payyee import TuYouPayYee
            params['userId'] = userId
            mo = TuYouPayYee.doPayRequestCard(params)

        if payType == 'yee2.card1':
            from tysdk.entity.pay.payyee2 import TuYouPayYee2
            params['userId'] = userId
            mo = TuYouPayYee2.doPayRequestCard1(params)

        if payType == 'yee2.card2':
            from tysdk.entity.pay.payyee2 import TuYouPayYee2
            params['userId'] = userId
            mo = TuYouPayYee2.doPayRequestCard2(params)

        # 射雕的支付宝支付和神州付
        from tysdk.entity.pay.payshediao import TuyouPayShediao
        if payType == 'shediao.ali':
            mo = TuyouPayShediao.doPayRequestAli(params)

        if payType == 'shediao.card.dx':
            mo = self.doPhoneCardPay(userId, params, 'dx', 'shediao')

        if payType == 'shediao.card.yd':
            mo = self.doPhoneCardPay(userId, params, 'yd', 'shediao')

        if payType == 'shediao.card.lt':
            mo = self.doPhoneCardPay(userId, params, 'lt', 'shediao')

        # 射雕易宝支付
        if payType == 'shediao.yee.card':
            from tysdk.entity.pay.payshediaoyee import TuYouPayShediaoYee
            params['userId'] = userId
            mo = TuYouPayShediaoYee.doPayRequestCard(params)

        #         # 腾讯移动平台
        #         if payType == 'tencentm' :
        #             from tysdk.entity.pay.paytencentm import TuyouPayTencentm
        #             mo = TuyouPayTencentm.doPayRequestGoods(params)

        return mo

    # 电话充值卡充值优先走易宝充值渠道,如果易宝没有此卡面额走神州付.
    @classmethod
    def doPhoneCardPay(self, userId, params, sp, channel):
        from tysdk.entity.pay.paytuyou import TuyouPayTuyou
        from tysdk.entity.pay.payyee import TuYouPayYee
        from tysdk.entity.pay.payshediao import TuyouPayShediao
        from tysdk.entity.pay.payshediaoyee import TuYouPayShediaoYee
        yd_prices = [10, 20, 30, 50, 100, 300, 500]
        # 移动浙江卡
        yd_zj_prices = [10, 20, 30, 50, 100, 200, 300, 500, 1000]
        # 移动福建卡
        yd_fj_prices = [50, 100]
        lt_prices = [20, 30, 50, 100, 300, 500]
        dx_prices = [50, 100]
        mo = TyContext.Cls_MsgPack()
        params['userId'] = userId
        if sp == 'yd':
            params['card_code'] = 'SZX'
            if len(params['card_number']) == 10 and len(params['card_pwd']) == 8 and int(
                    params['card_amount']) in yd_zj_prices:
                if channel == 'shediao':
                    mo = TuYouPayShediaoYee.doPayRequestCard(params)
                else:
                    mo = TuYouPayYee.doPayRequestCard(params)
            if len(params['card_number']) == 16 and len(params['card_pwd']) == 17 and int(
                    params['card_amount']) in yd_fj_prices:
                if channel == 'shediao':
                    mo = TuYouPayShediaoYee.doPayRequestCard(params)
                else:
                    mo = TuYouPayYee.doPayRequestCard(params)
            elif int(params['card_amount']) in yd_prices:
                if channel == 'shediao':
                    mo = TuYouPayShediaoYee.doPayRequestCard(params)
                else:
                    mo = TuYouPayYee.doPayRequestCard(params)
            else:
                if channel == 'shediao':
                    mo = TuyouPayShediao.doPayRequestCardYd(params)
                else:
                    mo = TuyouPayTuyou.doPayRequestCardYd(params)
        elif sp == 'lt':
            if int(params['card_amount']) in lt_prices:
                params['card_code'] = 'UNICOM'
                if channel == 'shediao':
                    mo = TuYouPayShediaoYee.doPayRequestCard(params)
                else:
                    mo = TuYouPayYee.doPayRequestCard(params)
            else:
                if channel == 'shediao':
                    mo = TuyouPayShediao.doPayRequestCardLt(params)
                else:
                    mo = TuyouPayTuyou.doPayRequestCardLt(params)
        elif sp == 'dx':
            if int(params['card_amount']) in dx_prices:
                params['card_code'] = 'TELECOM'
                if channel == 'shediao':
                    mo = TuYouPayShediaoYee.doPayRequestCard(params)
                else:
                    mo = TuYouPayYee.doPayRequestCard(params)
            else:
                if channel == 'shediao':
                    mo = TuyouPayShediao.doPayRequestCardDx(params)
                else:
                    mo = TuyouPayTuyou.doPayRequestCardDx(params)

        return mo

    @classmethod
    def doBuyChargeTuyouCoin(self, userId, params):
        TyContext.ftlog.info('********** doBuyChargeTuyouCoin in userId=', userId, 'params=', params)
        charge = int(float(params['orderPrice']))
        orderPlatformId = params['orderPlatformId']
        coin = self.changeUserCoin(params['appId'], userId, -charge, 'orderId=' + orderPlatformId)
        TyContext.ftlog.info('********** doBuyChargeTuyouCoin orderPlatformId=', orderPlatformId, 'orderPrice=', charge,
                             'coin=', coin)
        if coin < 0:
            params['orderPrice'] = -coin
            TyContext.ftlog.info('********** doBuyChargeTuyouCoin out need charged coin=', coin)
            return None
        else:
            mo = TyContext.Cls_MsgPack()
            params['payType'] = 'tuyou.coin.ok'
            self.makeBuyChargeMessage(mo, params)
            self.changeTransState(orderPlatformId, PAY_STATE_PAY_OK, 'PAY_STATE_PAY_OK', params)
            self.deliveryProduct(orderPlatformId, charge)
            TyContext.ftlog.info('********** doBuyChargeTuyouCoin out ok coin=', coin)
            return mo

    @classmethod
    def doBuyChargeCallback(self, orderPlatformId, total_fee, trade_status, notifys):
        TyContext.RunMode.get_server_link(orderPlatformId)
        ret = self.doBuyChargeCallback_(orderPlatformId, total_fee, trade_status, notifys)
        TyContext.RunMode.del_server_link(orderPlatformId)
        return ret

    @classmethod
    def doBuyChargeCallback_(self, orderPlatformId, total_fee, trade_status, notifys):

        if self._is_danji_orderid(orderPlatformId, total_fee, trade_status, notifys):
            return True

        newState = PAY_STATE_CHARGE_ERROR
        ukeys = ['userId', 'orderId', 'state', 'PAY_STATE_CHARGE']
        userId, orderId, state, orderinfos = TyContext.RedisPayData.execute('HMGET', 'platformOrder:' + orderPlatformId,
                                                                            *ukeys)
        TyContext.ftlog.info('doBuyChargeCallback orderPlatformId=', orderPlatformId,
                             'total_fee=', total_fee, 'notifys=', notifys, 'userId', userId,
                             'orderId', orderId, 'state', state, 'orderinfos', orderinfos)
        if not userId > 0:
            TyContext.ftlog.error('doBuyChargeCallback the order is not exits by userId ! orderPlatformId=',
                                  orderPlatformId)
            return True
        if not orderId:
            TyContext.ftlog.error('doBuyChargeCallback the order is not exits by orderId ! orderPlatformId=',
                                  orderPlatformId)
            return True

        orderinfos = TyContext.strutil.loads(orderinfos, decodeutf8=True)
        if 'payType' in notifys:
            orderinfos['payType'] = notifys['payType']
        orderPrice = int(float(orderinfos['orderPrice']))
        payType = orderinfos['payType']
        appId = orderinfos['appId']
        clientId = orderinfos['clientId']
        prodId = orderinfos['prodId']

        if state == PAY_STATE_CHARGE or state == PAY_STATE_CHARGE_WAIT:
            if trade_status == 'WAIT_BUYER_PAY':
                newState = PAY_STATE_CHARGE_WAIT
                TuyouPay.changeTransState(orderPlatformId, PAY_STATE_CHARGE_WAIT, 'PAY_STATE_CHARGE_WAIT', notifys)
            elif trade_status == 'TRADE_FINISHED':
                newState = PAY_STATE_CHARGE_OK
                TuyouPay.changeTransState(orderPlatformId, PAY_STATE_CHARGE_OK, 'PAY_STATE_CHARGE_OK', notifys)
            elif trade_status == 'TRADE_FAILED':
                TuyouPay.changeTransState(orderPlatformId, PAY_STATE_CHARGE_ERROR, 'PAY_STATE_CHARGE_ERROR', notifys)
            else:
                TyContext.ftlog.error(
                    'doBuyChargeCallback the order notify_data.trade_status error  ! orderPlatformId=', orderPlatformId)
                return False
        elif state >= PAY_STATE_DELIVERY:
            # XXX if external orderid is new, consider re-delivery the order?!
            Order.log(orderPlatformId, Order.INTERNAL_ERR, userId, appId, clientId,
                      paytype=payType, prodOrderId=orderId, prodid=prodId,
                      charge_price=orderPrice, info='order state delivered',
                      sub_paytype=notifys.get('sub_paytype', 'na'),
                      third_orderid=notifys.get('third_orderid', 'na'),
                      third_prodid=notifys.get('third_prodid', 'na'))
            TyContext.ftlog.info('doBuyChargeCallback order already delivered! orderPlatformId=', orderPlatformId)
            return True
        elif state >= PAY_STATE_CHARGE_OK:
            Order.log(orderPlatformId, Order.INTERNAL_ERR, userId, appId, clientId,
                      paytype=payType, prodOrderId=orderId, prodid=prodId,
                      charge_price=orderPrice, info='order state charged',
                      sub_paytype=notifys.get('sub_paytype', 'na'),
                      third_orderid=notifys.get('third_orderid', 'na'),
                      third_prodid=notifys.get('third_prodid', 'na'))
            TyContext.ftlog.error('doBuyChargeCallback order already PAY_STATE_CHARGE_OK ! orderPlatformId=',
                                  orderPlatformId)
            return True
        else:
            Order.log(orderPlatformId, Order.INTERNAL_ERR, userId, appId, clientId,
                      paytype=payType, prodOrderId=orderId, prodid=prodId,
                      charge_price=orderPrice, info='order state ' + str(state))
            TyContext.ftlog.error('doBuyChargeCallback the order state is not in charge ! orderPlatformId=',
                                  orderPlatformId)
            return False

        if newState != PAY_STATE_CHARGE_OK:
            TyContext.ftlog.info('doBuyChargeCallback trade_status', trade_status,
                                 'orderPlatformId=', orderPlatformId)
            if trade_status == 'TRADE_FAILED':
                Order.log(orderPlatformId, Order.CALLBACK_FAIL, userId, appId,
                          clientId, paytype=payType, prodOrderId=orderId,
                          prodid=prodId, charge_price=orderPrice,
                          info=trade_status)
            return True

        total_fee = int(float(total_fee))
        if total_fee < 0:
            TyContext.ftlog.info('doBuyChargeCallback short message total_fee=', total_fee, 'orderPrice=', orderPrice)
            total_fee = int(float(orderPrice))

        Order.log(orderPlatformId, Order.CALLBACK_OK, userId, appId, clientId,
                  paytype=payType, prodid=prodId, prodOrderId=orderId,
                  charge_price=orderPrice, succ_price=total_fee,
                  sub_paytype=notifys.get('sub_paytype', 'na'),
                  third_orderid=notifys.get('third_orderid', 'na'),
                  third_prodid=notifys.get('third_prodid', 'na'),
                  pay_appid=notifys.get('pay_appid', 'na'),
                  mobile=orderinfos.get('vouchMobile', 'na'))

        chargeCoin = CHARGE_RATE_RMB * total_fee
        coin = TuyouPay.changeUserCoin(orderinfos['appId'], userId, chargeCoin, 'charge:' + orderPlatformId)

        ct = datetime.datetime.now()
        paykey = ct.strftime('pay:%Y%m%d')
        if paykey < 'pay:20140416':
            payinfo = ct.strftime('%Y%m%d%H%M%S') + '.' + str(userId) + '.' + \
                      unicode(orderinfos['appId']) + '.' + unicode(orderinfos['orderName']) + \
                      '.' + unicode(total_fee) + '.' + orderinfos['payType']
        else:
            if 'vouchMobile' in orderinfos and orderinfos['vouchMobile'] != None:
                vouchMobile = orderinfos['vouchMobile']
            else:
                vouchMobile = ''

            payinfo = {'time': ct.strftime('%Y%m%d%H%M%S'),
                       'uid': userId,
                       'appId': orderinfos['appId'],
                       'name': orderinfos['orderName'],
                       'fee': total_fee,
                       'type': orderinfos['payType'],
                       'clientId': orderinfos['clientId'],
                       'tyOrderId': orderPlatformId,
                       'appOrderId': orderId,
                       'prodId': orderinfos['prodId'],
                       'vouchMobile': vouchMobile
                       }
            payinfodumps = json.dumps(payinfo)

        TyContext.RedisPayData.execute('LPUSH', paykey, payinfodumps)

        TyContext.SmsPayCheck.update_sms_pay_info_by_type(userId, coin, payType)

        if coin >= 0:
            TyContext.RedisUser.execute(userId, 'HINCRBY', 'user:' + str(userId), 'payCount', '1')
            TyContext.RedisUser.execute(userId, 'HINCRBYFLOAT', 'user:' + str(userId), 'chargeTotal', total_fee)

            gameid = int(orderinfos['appId'])
            if gameid < 10000:
                payTodayTotal = 0
                datas = TyContext.Day1st.get_datas(userId, gameid)
                if 'payTodayTotal' in datas:
                    payTodayTotal = datas['payTodayTotal']
                datas['payTodayTotal'] = payTodayTotal + coin
                TyContext.Day1st.set_datas(userId, gameid, datas)

            if payType.find('msg') >= 0:
                pass
            else:
                TyContext.RedisUser.execute(userId, 'HINCRBY', 'user:' + str(userId), 'chargeTotalNoMsg1', total_fee)
        else:
            TuyouPay.changeTransState(orderPlatformId, PAY_STATE_CHARGE_ERROR, 'PAY_STATE_CHARGE_ERROR', notifys)
            TyContext.ftlog.error('doBuyChargeCallback, ERROR, charge error, coin is zero !')
            return False

        self.__prefer_alipay_processing(prodId, payType, userId)

        TyContext.ftlog.info('doBuyChargeCallback buy order info-->', orderinfos)
        orderPrice = orderinfos['orderPrice']
        params = {'orderId': orderId, 'orderName': orderinfos['orderName'], 'orderPlatformId': orderPlatformId,
                  'orderPrice': orderPrice, 'appId': orderinfos['appId']}
        mo = TyContext.Cls_MsgPack()
        success, errinfo = self.doBuyGoods(mo, userId, params)
        if success:
            Order.log(orderPlatformId, Order.DELIVER_OK, userId, appId, clientId,
                      paytype=payType, prodid=prodId, prodOrderId=orderId, charge_price=orderPrice,
                      sub_paytype=notifys.get('sub_paytype', 'na'),
                      third_orderid=notifys.get('third_orderid', 'na'),
                      third_prodid=notifys.get('third_prodid', 'na'))
        else:
            Order.log(orderPlatformId, Order.DELIVER_FAIL, userId, appId, clientId,
                      info=errinfo, paytype=payType, prodid=prodId, prodOrderId=orderId, charge_price=orderPrice,
                      sub_paytype=notifys.get('sub_paytype', 'na'),
                      third_orderid=notifys.get('third_orderid', 'na'),
                      third_prodid=notifys.get('third_prodid', 'na'))
        TyContext.ftlog.info('doBuyChargeCallback return-->', mo.packJson())
        return True

    @classmethod
    def doBuyGoods(self, mo, userId, params):
        orderId = params['orderId']
        orderPlatformId = params['orderPlatformId']
        orderPrice = int(float(params['orderPrice']))
        mo.setResult('orderName', params['orderName'])

        coin = self.changeUserCoin(params['appId'], userId, -orderPrice, 'orderId=' + str(orderId))
        TyContext.ftlog.info('********** doBuyGoods orderId=', orderId, 'orderPlatformId=', orderPlatformId,
                             'orderPrice=', orderPrice, 'coin=', coin)

        errinfo = None
        success = True
        if coin >= 0:
            # VIP 消费途游币处理
            # from tysdk.games import gameClass
            # gameClass[0]['item'].onUserConsumeCoin( userId, orderPrice)
            TyContext.RedisUser.execute(userId, 'HINCRBY', 'user:' + str(userId), 'consumeCoin', orderPrice)

            # 修改交易状态
            self.changeTransState(orderPlatformId, PAY_STATE_PAY_OK, 'PAY_STATE_PAY_OK', params)
            # 投递货物
            ok = self.deliveryProduct(orderPlatformId, orderPrice)
            if ok:
                mo.setResult('code', 0)
                mo.setResult('info', 'transaction success finished')
            else:
                mo.setResult('code', 1)
                success = False
                errinfo = 'transaction delivery error finished'
                mo.setResult('info', errinfo)
            mo.setResult('orderPlatformId', orderPlatformId)
            mo.setResult('orderId', orderId)
            mo.setResult('coin', coin)
            mo.setResult('orderPrice', orderPrice)
            TyContext.ftlog.info('********** doBuyGoods return ok -> orderId=', orderId, 'orderPlatformId=',
                                 orderPlatformId, 'orderPrice=', orderPrice, 'coin=', coin)
        else:
            self.changeTransState(orderPlatformId, PAY_STATE_PAY_ERROR, 'PAY_STATE_PAY_ERROR', params)
            mo.setResult('code', 2)
            success = False
            errinfo = 'transaction failed, not enough coin'
            mo.setResult('info', errinfo)
            mo.setResult('orderPlatformId', orderPlatformId)
            mo.setResult('orderId', orderId)
            mo.setResult('coin', coin)
            mo.setResult('orderPrice', orderPrice)
            TyContext.ftlog.info('********** doBuyGoods return false -> orderId=', orderId, 'orderPlatformId=',
                                 orderPlatformId, 'orderPrice=', orderPrice, 'coin=', coin)

        return success, errinfo

    @classmethod
    def changeUserCoin(self, appId, userId, deltaCoin, logTag):
        deltaCoin = int(float(deltaCoin))
        TyContext.ftlog.info('changeUserCoin->userId=', userId, 'deltaCoin=', deltaCoin, 'logTag', logTag)
        # coin = TyContext.RedisUser.execute(userId, 'HINCRBY', 'user:' + str(userId), 'coin', str(deltaCoin))
        trueDelta, coin = TyContext.UserProps.incr_coin(int(userId), int(appId), deltaCoin,
                                                        TyContext.ChipNotEnoughOpMode.NOOP, TyContext.BIEventId.UNKNOWN)
        TyContext.ftlog.info('changeUserCoinAfter->userId=', userId, 'trueDelta=', trueDelta, 'coin', coin)
        if trueDelta == deltaCoin and coin >= 0:
            TyContext.BiReport.coin_update(appId, userId, deltaCoin, coin, 'pay')
            return coin
        return deltaCoin

    #         TyContext.ftlog.coinUpdate(userId, 'pay', logTag, deltaCoin, coin)
    # if coin >= 0 :
    #    return coin
    # else:
    #    coin2 = TyContext.RedisUser.execute(userId, 'HINCRBY', 'user:' + str(userId), 'coin', str(-deltaCoin))
    #    TyContext.BiReport.coin_update(appId, userId, -deltaCoin, coin2, 'pay-revert')
    #      TyContext.ftlog.coinUpdate(userId, 'pay', logTag + '-REVERT', -deltaCoin, coin2)
    #    return coin

    @classmethod
    def _call_delivery_url(self, orderId, orderPlatformId, userId, orderPrice, errorInfo, prodId):
        TyContext.ftlog.info('_call_delivery_url->', orderId, orderPlatformId, userId, orderPrice, errorInfo, prodId)
        baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + orderPlatformId, 'PAY_STATE_IDEL')
        baseinfo = json.loads(baseinfo)
        appId = baseinfo['appId']
        appInfo = baseinfo['appInfo']
        authInfo = baseinfo['authInfo']
        clientId = baseinfo['clientId']
        raffle = baseinfo['raffle']
        if int(appId) < 10000:
            payType = baseinfo['payType']
        else:
            payType = 'tuyoo'

        appKey = TyContext.Configure.get_game_item_str(appId, 'appKey', '')
        deliveryUrl = TyContext.Configure.get_game_item_str(appId, 'deliveryUrl', '')
        isErrorNotify = TyContext.Configure.get_game_item_str(appId, 'isErrorNotify', '')

        if not str(deliveryUrl).startswith('http'):
            deliveryUrl = None
        if deliveryUrl == None:
            # tuyoo的游戏
            control = TyContext.ServerControl.findServerControl(appId, clientId)
            if control != None:
                deliveryUrl = control['http'] + '/v1/deliveryproduct'
            authInfo = urllib.quote(authInfo)

        TyContext.ftlog.info('deliveryProduct-->appId=', appId, 'url=', deliveryUrl)
        if deliveryUrl == None:
            raise Exception('deliveryProduct-->appId=' + str(appId) + 'can not find the deliveryUrl !!')

        authInfo = authInfo.replace(' ', '')
        params = []
        # CAUTIONS!!!! DON'T change parameters (add or remove), NOR should you
        # alter order of the list, for external appids (>10000). Or they will
        # complain that sign code check fails!!!
        if errorInfo:
            params.append('isError')
            params.append('true')
            params.append('uid')
            params.append(userId)
            params.append('authInfo')
            params.append(authInfo)
            params.append('orderId')
            params.append(orderId)
            params.append('appId')
            params.append(appId)
            params.append('appInfo')
            params.append(appInfo)
            params.append('platformOrder')
            params.append(orderPlatformId)
            params.append('raffle')
            params.append(raffle)
            params.append('error')
            params.append(errorInfo)
            params.append('payType')
            params.append(payType)
            if isErrorNotify != None and str(isErrorNotify).upper() == 'NO':
                return 'error', deliveryUrl
        else:
            params.append('uid')
            params.append(userId)
            params.append('authInfo')
            params.append(authInfo)
            params.append('orderId')
            params.append(orderId)
            params.append('appId')
            params.append(appId)
            params.append('appInfo')
            params.append(appInfo)
            params.append('platformOrder')
            params.append(orderPlatformId)
            params.append('raffle')
            params.append(raffle)
            params.append('orderPrice')
            params.append(orderPrice)
            params.append('payType')
            params.append(payType)
        if int(appId) < 10000 and prodId:
            params.append('prodId')
            params.append(prodId)

        response, deliveryUrl = TyContext.WebPage.webget(deliveryUrl, params, appKey)
        return response, deliveryUrl

    @classmethod
    def deliveryChargeError(self, orderPlatformId, notifys, errorInfo, targetServer=3):
        TyContext.ftlog.info('deliveryChargeError->orderPlatformId=', orderPlatformId, 'errorInfo=', errorInfo)

        TyContext.RunMode.get_server_link(orderPlatformId)

        ukeys = ['userId', 'orderId', 'PAY_STATE_CHARGE']
        userId, orderId, orderinfos = TyContext.RedisPayData.execute('HMGET', 'platformOrder:' + orderPlatformId,
                                                                     *ukeys)
        if userId > 0 and orderId != None:
            self.changeTransState(orderPlatformId, PAY_STATE_CHARGE_ERROR, 'PAY_STATE_CHARGE_ERROR', notifys)

            if errorInfo == None:
                errorInfo = 'ERROR'
            orderinfos = json.loads(orderinfos)
            payType = orderinfos['payType']
            appId = orderinfos['appId']
            clientId = orderinfos['clientId']
            prodId = orderinfos['prodId']
            Order.log(orderPlatformId, Order.CALLBACK_FAIL, userId, appId, clientId,
                      info=errorInfo, prodOrderId=orderId, paytype=payType, prodid=prodId,
                      charge_price=orderinfos.get('orderPrice', 'na'))
            self._call_delivery_url(orderId, orderPlatformId, userId, 0, errorInfo, prodId)
            TyContext.ftlog.error('deliveryChargeError->orderPlatformId=', orderPlatformId, ' done !')
        else:
            TyContext.ftlog.error('deliveryChargeError->orderPlatformId=', orderPlatformId, ' not found !')

        TyContext.RunMode.del_server_link(orderPlatformId)
        return True

    @classmethod
    def deliveryProduct(self, orderPlatformId, orderPrice):
        TyContext.ftlog.info('deliveryProduct->', orderPlatformId, orderPrice)
        ukeys = ['userId', 'orderId', 'state', 'PAY_STATE_CHARGE']
        userId, orderId, state, orderinfos = TyContext.RedisPayData.execute('HMGET', 'platformOrder:' + orderPlatformId,
                                                                            *ukeys)
        if state != PAY_STATE_PAY_OK:
            TyContext.ftlog.error('ERROR, deliveryProduct, state error, state=', state)
            return False

        self.changeTransState(orderPlatformId, PAY_STATE_DELIVERY, 'PAY_STATE_DELIVERY', {})

        orderinfos = json.loads(orderinfos)
        prodId = orderinfos['prodId']
        response, deliveryUrl = self._call_delivery_url(orderId, orderPlatformId, userId, orderPrice, None, prodId)

        if response == 'success':
            self.changeTransState(orderPlatformId, PAY_STATE_DELIVERY_OK, 'PAY_STATE_DELIVERY_OK', {})
            TyContext.ftlog.info('doDeliveryProductDone !!!!! ok ', response, ' url=', deliveryUrl)
            return True
        else:
            self.changeTransState(orderPlatformId, PAY_STATE_DELIVERY_ERROR, 'PAY_STATE_DELIVERY_ERROR', {})
            TyContext.ftlog.info('doDeliveryProductDone !!!!! error ', response, ' url=', deliveryUrl)
            return False

    @classmethod
    def __prefer_alipay_processing(cls, prodId, payType, userId):
        if 0 == TyContext.Configure.get_global_item_int('prefer_alipay_once_used'):
            return
        used = TyContext.RedisUser.execute(userId, 'HGET', 'user:%d' % userId, 'used_alipay')
        if used is None or used == 0:
            if payType not in ['360.ali', 'tuyou.ali']:
                return
            TyContext.RedisUser.execute(userId, 'HSET', 'user:%d' % userId, 'used_alipay', 1)
            TyContext.ftlog.info('alipay_stats: userid=', userId, 'buys', prodId, 'using alipay for the first time')
        else:
            TyContext.ftlog.info('alipay_stats: userid=', userId, 'buys', prodId, 'using paytype', payType)

    @classmethod
    def _is_danji_orderid(self, platformOrderId, total_fee, state, rparam):
        if not platformOrderId.startswith('f'):
            return False

        userId = TyContext.strutil.toint10(platformOrderId[5:10])
        if userId == 0:
            userId = 1
            clientId = 'Android_3.372_tuyoo.tuyoo.0-hall6.tuyoo.day'
            gameId = 6
        else:
            clientId = TyContext.UserSession.get_session_clientid(userId)
            gameId = TyContext.UserSession.get_session_gameid(userId)

        if state == 'TRADE_FAILED':
            Order.log(platformOrderId, Order.CALLBACK_FAIL, userId,
                      gameId, clientId,
                      prodid='TY9999R00020DJ',
                      diamondid='TY9999R00020DJ',
                      charge_price=total_fee,
                      paytype=rparam.get('payType', 'na'),
                      sub_paytype=rparam.get('sub_paytype', 'na'),
                      third_prodid=rparam.get('third_prodid', 'na'),
                      third_orderid=rparam.get('third_orderid', 'na'),
                      pay_appid=rparam.get('pay_appid', 'na'),
                      )
        elif state == 'TRADE_FINISHED':
            ct = datetime.datetime.now()
            paykey = ct.strftime('pay:%Y%m%d')
            payinfo = {'time': ct.strftime('%Y%m%d%H%M%S'),
                       'uid': userId,
                       'appId': gameId,
                       'name': '30000银币',
                       'fee': total_fee,
                       'type': rparam.get('payType', 'na'),
                       'clientId': clientId,
                       'tyOrderId': platformOrderId,
                       'appOrderId': '',
                       'prodId': 'TY9999R00020DJ',
                       'vouchMobile': rparam.get('vouchMobile', 'na')
                       }
            payinfodumps = json.dumps(payinfo)
            TyContext.RedisPayData.execute('LPUSH', paykey, payinfodumps)

            Order.log(platformOrderId, Order.CALLBACK_OK, userId,
                      gameId, clientId,
                      paytype=rparam.get('payType', 'na'),
                      prodid='TY9999R00020DJ',
                      diamondid='TY9999R00020DJ',
                      prod_price=2,
                      charge_price=2,
                      succ_price=total_fee,
                      sub_paytype=rparam.get('sub_paytype', 'na'),
                      third_prodid=rparam.get('third_prodid', 'na'),
                      third_orderid=rparam.get('third_orderid', 'na'),
                      pay_appid=rparam.get('pay_appid', 'na'),
                      )
        else:
            TyContext.ftlog.error(
                'wrong state', state, 'platformOrder', platformOrderId,
                'rparam', rparam)
        return True
