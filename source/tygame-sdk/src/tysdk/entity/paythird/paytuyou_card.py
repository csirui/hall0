# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''

from payszfcard import TuYouPaySzfCard
from payyee import TuYouPayYee


class TuyouPayTuyouCard(object):
    @classmethod
    def doPayRequestCardYd(cls, chargeInfo, mi, mo):
        yd_prices = [10, 20, 30, 50, 100, 300, 500]
        # 移动浙江卡
        yd_zj_prices = [10, 20, 30, 50, 100, 200, 300, 500, 1000]
        # 移动福建卡
        yd_fj_prices = [50, 100]
        mi.setParam('card_code', 'SZX')
        status = None
        if len(mi.getParamStr('card_number')) == 10 and len(mi.getParamStr('card_pwd')) == 8 and int(
                mi.getParamStr('card_amount')) in yd_zj_prices:
            status = TuYouPayYee.doPayRequestCard(chargeInfo, mi, mo)
        elif len(mi.getParamStr('card_number')) == 16 and len(mi.getParamStr('card_pwd')) == 17 and int(
                mi.getParamStr('card_amount')) in yd_fj_prices:
            status = TuYouPayYee.doPayRequestCard(chargeInfo, mi, mo)
        elif int(mi.getParamStr('card_amount')) in yd_prices:
            status = TuYouPayYee.doPayRequestCard(chargeInfo, mi, mo)
        else:
            status = TuYouPaySzfCard.doPayRequestCardYd(chargeInfo, mi, mo)
        return status

    @classmethod
    def doPayRequestCardLt(cls, chargeInfo, mi, mo):
        lt_prices = [20, 30, 50, 100, 300, 500]
        mi.setParam('card_code', 'UNICOM')
        status = None
        if int(mi.getParamStr('card_amount')) in lt_prices:
            status = TuYouPayYee.doPayRequestCard(chargeInfo, mi, mo)
        else:
            status = TuYouPaySzfCard.doPayRequestCardLt(chargeInfo, mi, mo)
        return status

    @classmethod
    def doPayRequestCardDx(cls, chargeInfo, mi, mo):
        dx_prices = [50, 100]
        mi.setParam('card_code', 'TELECOM')
        status = None
        if int(mi.getParamStr('card_amount')) in dx_prices:
            status = TuYouPayYee.doPayRequestCard(chargeInfo, mi, mo)
        else:
            status = TuYouPaySzfCard.doPayRequestCardDx(chargeInfo, mi, mo)
        return status
