# -*- coding=utf-8 -*-

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayDaodao(object):
    @classmethod
    def doDaodaoCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doDaodaoCallback', rparam)
        try:
            orderPlatformId = rparam['cpparam']
            total_fee = rparam['successMoney']
        except Exception as e:
            TyContext.ftlog.error('doDaodaoCallback ,param err,exception ', e)
        PayHelper.callback_ok(orderPlatformId, float(total_fee), rparam)
