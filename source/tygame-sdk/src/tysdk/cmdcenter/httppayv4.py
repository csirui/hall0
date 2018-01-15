# -*- coding=utf-8 -*-
from tysdk.cmdcenter.httppayv3 import HttpPayV3
from tysdk.entity.pay4.charge_universal import ChargeUniversal
from tysdk.entity.pay4.decorator import payv4_callback
from tysdk.entity.user3.account_check import AccountCheck

__author__ = 'yuejianqiang'

from tyframework.context import TyContext


class HttpPayV4(object):
    JSONPATHS = None
    HTMLPATHS = None

    @classmethod
    def getJsonPaths(cls):

        at = TyContext.TYGlobal.http_sdk_inner()
        b = at

        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v4/pay/charge': cls.doCharge,  # 获取支付方式列表
                '/open/v4/pay/order': cls.doOrder,  # 开始支付
                '/open/v4/pay/query': cls.doQuery,  # 查询订单状态
                '/open/v4/pay/consume': cls.doConsume,  # 兑换金币或道具
            }
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                # '/open/vc/pay/now/callback': TuYouNow.doCallback,
            }
        cls.HTMLPATHS.update(payv4_callback.payv4_callback_map)
        return cls.HTMLPATHS

    @classmethod
    def doCharge(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            mo = TyContext.Cls_MsgPack()
            mo.setResult('code', 1)
            mo.setResult('info', "参数校验失败")
            return mo
        params = TyContext.RunHttp.convertToMsgPack()
        mo = ChargeUniversal.charge(params)
        return mo

    @classmethod
    def doOrder(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            mo = TyContext.Cls_MsgPack()
            mo.setResult('code', 1)
            mo.setResult('info', "参数校验失败")
            return mo
        params = TyContext.RunHttp.convertToMsgPack()
        mo = ChargeUniversal.order(params)
        return mo

    @classmethod
    def doQuery(cls, rpath):
        return HttpPayV3.doQueryStatus(rpath)

    @classmethod
    def doConsume(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            mo = TyContext.Cls_MsgPack()
            mo.setResult('code', 1)
            mo.setResult('info', "参数校验失败")
            return mo
        params = TyContext.RunHttp.convertToMsgPack()
        mo = ChargeUniversal.consume(params)
        return mo
