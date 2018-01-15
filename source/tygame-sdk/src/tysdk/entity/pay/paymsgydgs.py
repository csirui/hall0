# -*- coding=utf-8 -*-


from tyframework.context import TyContext


class TuYouPayMsgYdGs():
    @classmethod
    def doMsgYdGsRequest(self, datas):
        TyContext.ftlog.info('TuYouPayMsgYdGs.doMsgYdGsRequest in datas=', datas)

        mo = TyContext.Cls_MsgPack()
        from tysdk.entity.pay.pay import TuyouPay
        TuyouPay.makeBuyChargeMessage(mo, datas)
        return mo

    @classmethod
    def doMsgYdGsCallback(self, rpath):
        return 'success'
