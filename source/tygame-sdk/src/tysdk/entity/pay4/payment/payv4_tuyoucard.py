# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''

from tyframework.context import TyContext
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_yee import TuYouPayYeeV4
from tysdk.entity.paythird.payszfcard import TuYouPaySzfCard


class PayTuyooCardV4(PayBaseV4):
    @payv4_order('tuyoo.card')
    def doPayRequestCard(self, mi):
        chargeInfo = self.get_charge_info(mi)
        mo = TyContext.Cls_MsgPack()
        status = TuYouPayYeeV4.doPayRequestCard(chargeInfo, mi, mo)
        mo.setResult('chargeinfo', chargeInfo)
        mo.setResult('code', status)
        return self.return_mo(0, chargeInfo=chargeInfo)

    @payv4_order('tuyou.card.yd')
    def doPayRequestCardYd(self, mi):
        mo = TyContext.Cls_MsgPack()
        chargeInfo = self.get_charge_info(mi)
        yd_prices = [10, 20, 30, 50, 100, 300, 500]
        # 移动浙江卡
        yd_zj_prices = [10, 20, 30, 50, 100, 200, 300, 500, 1000]
        # 移动福建卡
        yd_fj_prices = [50, 100]
        mi.setParam('card_code', 'SZX')
        if len(mi.getParamStr('card_number')) == 10 and len(mi.getParamStr('card_pwd')) == 8 and int(
                mi.getParamStr('card_amount')) in yd_zj_prices:
            status = TuYouPayYeeV4.doPayRequestCard(chargeInfo, mi, mo)
        elif len(mi.getParamStr('card_number')) == 16 and len(mi.getParamStr('card_pwd')) == 17 and int(
                mi.getParamStr('card_amount')) in yd_fj_prices:
            status = TuYouPayYeeV4.doPayRequestCard(chargeInfo, mi, mo)
        elif int(mi.getParamStr('card_amount')) in yd_prices:
            status = TuYouPayYeeV4.doPayRequestCard(chargeInfo, mi, mo)
        else:
            status = TuYouPaySzfCard.doPayRequestCardYd(chargeInfo, mi, mo)
        mo.setResult('code', status)
        return mo

    @payv4_order('tuyou.card.lt')
    def doPayRequestCardLt(self, mi):
        mo = TyContext.Cls_MsgPack()
        chargeInfo = self.get_charge_info(mi)
        lt_prices = [20, 30, 50, 100, 300, 500]
        mi.setParam('card_code', 'UNICOM')
        if int(mi.getParamStr('card_amount')) in lt_prices:
            status = TuYouPayYeeV4.doPayRequestCard(chargeInfo, mi, mo)
        else:
            status = TuYouPaySzfCard.doPayRequestCardLt(chargeInfo, mi, mo)
        mo.setResult('code', status)
        return mo

    @payv4_order('tuyou.card.dx')
    def doPayRequestCardDx(self, mi):
        mo = TyContext.Cls_MsgPack()
        chargeInfo = self.get_charge_info(mi)
        dx_prices = [50, 100]
        mi.setParam('card_code', 'TELECOM')
        if int(mi.getParamStr('card_amount')) in dx_prices:
            status = TuYouPayYeeV4.doPayRequestCard(chargeInfo, mi, mo)
        else:
            status = TuYouPaySzfCard.doPayRequestCardDx(chargeInfo, mi, mo)
        mo.setResult('code', status)
        return mo
