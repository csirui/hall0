# -*- coding=utf-8 -*-

from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayEftUnion():
    appkeys = {
        'ZT': '8E26F8C036DB449D',  # 斗地主
        'VW': 'A0910DC2B1D24126',  # 新斗牛
        'MM': '85C6B6D4BB8C48A5',  # 麻将
        'QC': '5D619FC2CE414DB6',  # 德州
    }

    @classmethod
    def charge_data(cls, chargeinfo):
        diamondId = chargeinfo['diamondId']
        appId = chargeinfo['appId']
        orderPlatformId = chargeinfo['platformOrderId']
        orderPhone = '10669202'
        # 用10元点做缺省值
        payCode = 'wo#aqw*'
        # 新斗牛
        if diamondId == 'D100':
            payCode = 'wo#aqw*'
        if diamondId == 'D20':
            payCode = 'wo#aqu*'
        if diamondId == 'D50':
            payCode = 'wo#aqv*'

        # 除斗地主外，对指令进行服务端组装
        # 新斗牛
        if str(appId) == '10':
            payCode = payCode + 'VW'

        # type是短信支付的方式，1代表的是发一条短信支付
        if str(appId) == '6':
            smsMsg = payCode + 'ZT' + orderPlatformId
        elif str(appId) == '10':
            smsMsg = payCode + 'VW' + orderPlatformId
        else:
            smsMsg = payCode + orderPlatformId

        smsPayinfo = {'type': '1', 'smsMsg': smsMsg, 'smsPort': orderPhone}
        chargeinfo['chargeData'] = {'issms': 1, 'msgOrderCode': payCode,
                                    'orderPhone': orderPhone, 'smsPayinfo': smsPayinfo}

    # 联通、电信共用此回调
    @classmethod
    def doMsgDxCallback(self, rpath):

        MchNo = TyContext.RunHttp.getRequestParam('MchNo', '')
        Phone = TyContext.RunHttp.getRequestParam('Phone', '')
        Fee = TyContext.RunHttp.getRequestParam('Fee', '')  # 单位：元
        OrderId = TyContext.RunHttp.getRequestParam('OrderId', '')
        MobileType = TyContext.RunHttp.getRequestParam('MobileType', '')
        Sign = TyContext.RunHttp.getRequestParam('Sign', '')
        if MchNo == '' or Phone == '' or Fee == '' or OrderId == '' or Sign == '':
            return '401~参数错误~'

        eft_skey = ''
        try:
            eft_appid = OrderId[0:2]
            eft_skey = TuYouPayEftUnion.appkeys.get(eft_appid, None)
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
            Fee = float(Fee)
        except:
            TyContext.ftlog.exception()
        TyContext.ftlog.info('TuYouPayEftUnion.doMsgDxCallback orderPlatformId=', orderPlatformId)

        notifys = {'MchNo': MchNo, 'Phone': Phone, 'OrderId': OrderId, 'third_orderid': MchNo}
        if MobileType == 'LT':
            notifys['chargeType'] = 'EFTChinaUnion.msg'
        elif MobileType == 'DX':
            notifys['chargeType'] = 'EFTChinaTelecom.msg'
        PayHelper.set_order_mobile(orderPlatformId, Phone)
        isOk = PayHelper.callback_ok(orderPlatformId, Fee, notifys)
        if isOk:
            return '000~成功~'
        else:
            return '111~失败~'
