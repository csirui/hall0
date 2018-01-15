# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 16时55分58秒
# FileName:      http91.py
# Class:         Http91Tasklet

# from trunk svn 7501 2014-10-04 10:58


from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay3.charge import TuyouPayCharge
from tysdk.entity.pay3.consume import TuyouPayConsume
from tysdk.entity.pay3.diamondlist import TuyouPayDiamondList
from tysdk.entity.pay3.query import TuyouPayQuery
from tysdk.entity.pay3.request import TuyouPayRequest
from tysdk.entity.pay_common.orderlog import Order
from tysdk.entity.paythird.payyoukuh5 import TuYouPayYouKuH5
from tysdk.entity.user3.account_check_h5 import AccountCheck


class HttpPayH5V3(object):
    JSONPATHS = None
    HTMLPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/h5v3/pay/consume': cls.doConsume,
                '/open/h5v3/pay/diamondlist': cls.doDiamondList,
                '/open/h5v3/pay/charge': cls.doCharge,
                '/open/h5v3/pay/request': cls.doRequest,
                '/open/h5v3/pay/querystatus': cls.doQueryStatus,
                '/open/h5v3/pay/cancelorder': cls.doCancelOrder,  # 新老版的支付都用这个接口
            }
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                '/open/vc/pay/youkuh5/callback': TuYouPayYouKuH5.doYouKuCallback,
                '/open/vc/pay/youkuh5/vip_callback': TuYouPayYouKuH5.doYoukuVipCallback
            }

            from tysdk import is_test_sdk_server
            if is_test_sdk_server():
                cls.HTMLPATHS.update({

                })
        return cls.HTMLPATHS

    @classmethod
    def jsonApiIntercept(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        return isReturn, params

    @classmethod
    def doConsume(cls, path):
        mi = TyContext.RunHttp.convertToMsgPack(
            ['userId', 'authorCode', 'appId', 'clientId', 'appInfo', 'prodId',
             'prodName', 'prodCount', 'prodPrice', 'prodOrderId', 'mustcharge',
             'payType', 'payInfo'])
        mo = TuyouPayConsume.consume(mi)
        mo = mo.packJson()
        #         TyContext.ftlog.info('********** doConsume out return=', mo)
        return mo

    @classmethod
    def doDiamondList(cls, path):
        mi = TyContext.RunHttp.convertToMsgPack(['userId', 'authorCode', 'appId', 'clientId'])
        mo = TuyouPayDiamondList.diamondlist(mi)
        mo = mo.packJson()
        #         TyContext.ftlog.info('********** doDiamondList out return=', mo)
        return mo

    @classmethod
    def doRequest(cls, path):
        mi = TyContext.RunHttp.convertToMsgPack()
        mo = TuyouPayRequest.request(mi)
        mo = mo.packJson()
        #         TyContext.ftlog.info('********** doRequest out return=', mo)
        return mo

    @classmethod
    def doCharge(cls, path):
        mi = TyContext.RunHttp.convertToMsgPack(['userId', 'authorCode', 'appId', 'clientId', 'appInfo',
                                                 'diamondId', 'diamondCount', 'diamondName', 'diamondPrice',
                                                 'payType', 'payInfo'])
        mo = TuyouPayCharge.charge(mi)
        mo = mo.packJson()
        #         TyContext.ftlog.info('********** doCharge out return=', mo)
        return mo

    @classmethod
    def doQueryStatus(cls, path):
        mi = TyContext.RunHttp.convertToMsgPack()
        mo = TuyouPayQuery.status(mi)
        mo = mo.packJson()
        #         TyContext.ftlog.info('********** doQueryStatus out return=', mo)
        return mo

    @classmethod
    def doCancelOrder(cls, path):
        ''' 用于客户端支付失败后取消订单
            reason 0: user cancel the order for client sdk (e.g. ydmm/ltw) failed
                   1: user cancel the order in the first place
                   2: user cancel the order on sms send fail
                   3: user cancel the order on sms send timeout
        '''
        mi = TyContext.RunHttp.convertToMsgPack()
        platformOrderId = mi.getParamStr('platformOrderId', 'na')
        productOrderId = mi.getParamStr('productOrderId', 'na')
        shortId = 'na'
        if ShortOrderIdMap.is_short_order_id_format(platformOrderId):
            shortId, platformOrderId = platformOrderId, ShortOrderIdMap.get_long_order_id(platformOrderId)
        appId = mi.getParamInt('appId', 'na')
        userId = mi.getParamInt('userId', 'na')
        clientId = mi.getParamStr('clientId', 'na')
        paytype = mi.getParamStr('payType', 'na')
        errinfo = mi.getParamStr('errInfo', 'na')
        reason = mi.getParamStr('reason', 'na')

        Order.log(platformOrderId, Order.CLIENT_CANCELED, userId, appId, clientId,
                  shortId=shortId, prodOrderId=productOrderId, paytype=paytype,
                  subevent=reason, info=errinfo if errinfo else 'na')
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('cancelorder')
        mo = mo.packJson()
        return mo
