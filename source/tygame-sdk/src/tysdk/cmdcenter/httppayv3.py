# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 16时55分58秒
# FileName:      http91.py
# Class:         Http91Tasklet

# from trunk svn 7501 2014-10-04 10:58


from tyframework.context import TyContext
from tysdk.entity.mock.mockpay import MockPay
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay3.charge import TuyouPayCharge
from tysdk.entity.pay3.consume import TuyouPayConsume
from tysdk.entity.pay3.diamondlist import TuyouPayDiamondList
from tysdk.entity.pay3.query import TuyouPayQuery
from tysdk.entity.pay3.request import TuyouPayRequest
from tysdk.entity.pay_common.orderlog import Order
from tysdk.entity.pay_common.paysll import TuYouSLL
from tysdk.entity.paythird.pay360 import TuYouPay360
from tysdk.entity.paythird.pay360msg import TuYouPay360Msg
from tysdk.entity.paythird.pay360pay import TuYouPay360pay
from tysdk.entity.paythird.payaidongman import TuYouPayAiDongMan
from tysdk.entity.paythird.payaigame import TuYouPayAiGame
from tysdk.entity.paythird.payaisi import TuYouPayAiSi
from tysdk.entity.paythird.payanzhi import TuYouPayAnZhi
from tysdk.entity.paythird.paychangba import TuYouPayChangba
from tysdk.entity.paythird.paycoolpad import TuYouPayCoolpad
from tysdk.entity.paythird.paydaodao import TuYouPayDaodao
from tysdk.entity.paythird.payduoku import TuYouPayDuoKu
from tysdk.entity.paythird.payeftunion import TuYouPayEftUnion
from tysdk.entity.paythird.paygefu import TuYouPayGeFu
from tysdk.entity.paythird.paygefubigsdk import TuYouPayGeFuBigSdk
from tysdk.entity.paythird.paygoogleiab import TuyouPayGoogleIAB
from tysdk.entity.paythird.payhaimawan import TuYouPayHaiMaWan
from tysdk.entity.paythird.payhuawei import TuYouPayHuaWei
from tysdk.entity.paythird.payhuiyuan import TuYouPayHuiYuanBaoYue
from tysdk.entity.paythird.payiTools import TuYouPayiTools
from tysdk.entity.paythird.payiappay import TuYooIappay
from tysdk.entity.paythird.payido import TuYouPayIDO
from tysdk.entity.paythird.payiiapple import TuYouIIApple
from tysdk.entity.paythird.payios import TuYouPayIos
from tysdk.entity.paythird.payjinli import TuYouPayJinli
from tysdk.entity.paythird.payjinri import TuYouPayJinri
from tysdk.entity.paythird.payjinritoutiao import TuYouPayJinritoutiao
from tysdk.entity.paythird.payjiuxiu import TuYouPayJiuxiu
from tysdk.entity.paythird.payjolo import TuYouPayJolo
from tysdk.entity.paythird.paykuaiwan import TuYouPayKuaiwan
from tysdk.entity.paythird.paykuaiyongpingguo import TuYouPayKuaiYongPingGuo
from tysdk.entity.paythird.paylangtian import TuYouPayLangtian
from tysdk.entity.paythird.paylenovo import TuYouPayLenovo
from tysdk.entity.paythird.paylenovodj import TuYouPayLenovoDanji
from tysdk.entity.paythird.payletv import TuYouPayLetv
from tysdk.entity.paythird.payliantongwo import TuYouPayLianTongWo
from tysdk.entity.paythird.paylinkyun import TuYouPayLinkYun
from tysdk.entity.paythird.paylinkyun_union import TuYouPayLinkYunUnion
from tysdk.entity.paythird.paylinkyunapi import TuYouPayLinkYunApi
from tysdk.entity.paythird.paylizi import TuYouPayLizi
from tysdk.entity.paythird.paym4399 import TuYouPayM4399
from tysdk.entity.paythird.paymaopao import TuYouMaoPao
from tysdk.entity.paythird.paymeizu import TuYouPayMeizu
from tysdk.entity.paythird.paymidashi import TuYouPayMiDaShi
from tysdk.entity.paythird.paymingtiandongli import TuYouPayMingTianDongLiApi
from tysdk.entity.paythird.paymomo import TuYouPayMomo
from tysdk.entity.paythird.paymumayi import TuYouPayMumayi
from tysdk.entity.paythird.paymuzhiwan import TuYouPayMuzhiwan
from tysdk.entity.paythird.paynow import TuYouNow
from tysdk.entity.paythird.paynubia import TuYouPayNubia
from tysdk.entity.paythird.payoppo import TuyouPayOppo
from tysdk.entity.paythird.paypalm import TuYouPayPalm
from tysdk.entity.paythird.paypapa import TuYouPayPapa
from tysdk.entity.paythird.paypengyouwan import TuYouPayPengyouwan
from tysdk.entity.paythird.paypps import TuYouPayPPS
from tysdk.entity.paythird.payppzhushou import TuYouPayPPZhuShou
from tysdk.entity.paythird.payshediao_ali import TuyouPayShediaoAli
from tysdk.entity.paythird.payshuzitianyu import TuYouPaySzty
from tysdk.entity.paythird.payshuzitianyuh5 import TuYouPayShuzitianyuH5
from tysdk.entity.paythird.paysougou import TuYouPaySougou
from tysdk.entity.paythird.payszfcard import TuYouPaySzfCard
from tysdk.entity.paythird.paytongbutui import TuYouPayTongBuTui
from tysdk.entity.paythird.paytuyou_ali import TuyouPayTuyouAli
from tysdk.entity.paythird.payuc import TuYouPayUc
from tysdk.entity.paythird.payucdj import TuYouPayUcDj
from tysdk.entity.paythird.payunionpay import TuYouPayUnionPay
from tysdk.entity.paythird.payvivo import TuYouPayVivo
from tysdk.entity.paythird.paywandoujia import TuYouPayWanDouJia
from tysdk.entity.paythird.paywx import TuYouPayWXpay
from tysdk.entity.paythird.payxiaomi import TuYouPayXiaomi
from tysdk.entity.paythird.payxyzs import TuYouPayXYZS
from tysdk.entity.paythird.payydjd import TuYouPayYdjd
from tysdk.entity.paythird.payydmm import TuYouPayYdMmWeak
from tysdk.entity.paythird.payyee import TuYouPayYee
from tysdk.entity.paythird.payyee2 import TuYouPayYee2
from tysdk.entity.paythird.payyi import TuYouPayYi
from tysdk.entity.paythird.payyisdk import TuYouPayYiSdk
from tysdk.entity.paythird.payyiwap import TuYouPayYiWap
from tysdk.entity.paythird.payyouku import TuYouPayYouKu
from tysdk.entity.paythird.payyygame import TuYouPayYYGame
from tysdk.entity.paythird.payzhangyue import TuYouPayZhangYue
from tysdk.entity.paythird.payzhuowang import TuYouPayZhuowang
from tysdk.entity.paythird.payzhuoyi import TuYouPayZhuoyi
from tysdk.entity.upgradev3.checkplugin import TuYouCheckPlugin
from tysdk.entity.user3.account_check import AccountCheck


class HttpPayV3(object):
    JSONPATHS = None
    HTMLPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v3/pay/consume': cls.doConsume,
                '/open/v3/pay/diamondlist': cls.doDiamondList,
                '/open/v3/pay/charge': cls.doCharge,
                '/open/v3/pay/request': cls.doRequest,
                '/open/v3/pay/querystatus': cls.doQueryStatus,
                '/open/v3/pay/cancelorder': cls.doCancelOrder,  # 新老版的支付都用这个接口
            }
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                '/open/vc/pay/ios/callback': TuYouPayIos.doIosCallback,
                '/open/vc/pay/360/callback': TuYouPay360.callback,
                '/open/vc/pay/360/msg/callback': TuYouPay360Msg.callback,
                '/open/vc/pay/alipay/callback': TuyouPayTuyouAli.doAliCallback,
                '/open/vc/pay/shediao/alipay/callback': TuyouPayShediaoAli.doAliCallback,
                '/open/vc/pay/alinewpay/callback': TuyouPayTuyouAli.doAliCallbackNew,
                '/open/vc/pay/card/callback': TuYouPaySzfCard.doCardCallback,
                '/open/vc/pay/yee/callback': TuYouPayYee.doCardCallback,
                '/open/vc/pay/linkyun/confirm': TuYouPayLinkYun.doLinkYunConfirm,
                '/open/vc/pay/linkyun/callback': TuYouPayLinkYun.doLinkYunCallback,
                '/open/vc/pay/linkyun/union/confirm': TuYouPayLinkYunUnion.doLinkYunUnionConfirm,
                '/open/vc/pay/linkyun/union/callback': TuYouPayLinkYunUnion.doLinkYunUnionCallback,
                '/open/vc/pay/linkyun/api/callback': TuYouPayLinkYunApi.doLinkYunApiCallback,
                '/open/vc/pay/mh/callback': TuYouPayEftUnion.doMsgDxCallback,
                '/open/vc/pay/ydmm/callback': TuYouPayYdMmWeak.doYdMmCallback,
                '/open/vc/pay/ydjd/callback': TuYouPayYdjd.doYdjdCallback,
                '/open/vc/pay/yee2/callback10': TuYouPayYee2.doCallback1,
                '/open/vc/pay/yee2/callback11': TuYouPayYee2.doCallback2,
                '/open/vc/pay/yee2/callback20': TuYouPayYee2.doCallback1,
                '/open/vc/pay/yee2/callback21': TuYouPayYee2.doCallback2,

                '/open/vc/pay/liantongw/callback': TuYouPayLianTongWo.doLianTongWoCallback,

                '/open/vc/pay/aigame/msg/callback': TuYouPayAiGame.doAiGameMsgCallback,
                '/open/vc/pay/aiyouxi/callback1': TuYouPayAiGame.doAiGameMsgCallback,
                '/open/vc/pay/aigame/callback': TuYouPayAiGame.doAiGameCallback,
                '/open/vc/pay/aiyouxi/callback2': TuYouPayAiGame.doAiGameCallback,

                '/open/vc/pay/aiyouxi/callback/dizhu/happy': TuYouPayAiGame.doAiGameCallbackDizhuHappy,
                '/open/vc/pay/aiyouxi/callback/dizhu/tyhall': TuYouPayAiGame.doAiGameCallbackDizhuHappy,
                '/open/vc/pay/aiyouxi/callback/dizhu/kugou': TuYouPayAiGame.doAiGameCallbackDizhuHappy,
                '/open/vc/pay/aiyouxi/callback/dizhu/huabei': TuYouPayAiGame.doAiGameCallbackDizhuHuabei,
                '/open/vc/pay/aiyouxi/callback/dizhustar/zszh/wf': TuYouPayAiGame.doAiGameCallbackDizhuStarZszhWF,
                '/open/vc/pay/aiyouxi/callback/dizhustar/zszh/pt': TuYouPayAiGame.doAiGameCallbackDizhuStarZszhPT,
                '/open/vc/pay/aiyouxi/callback/dizhu/happy/dj': TuYouPayAiGame.doAiGameCallbackDizhuHappyDj,

                '/open/vc/pay/aigame/all/callback': TuYouPayAiGame.doAiGameAllCallback,
                '/open/vc/pay/oppo/callback': TuyouPayOppo.doOppoCallback,
                '/open/vc/pay/lenovo/callback': TuYouPayLenovo.doLenovoCallback,
                '/open/vc/pay/lenovodj/callback': TuYouPayLenovoDanji.doLenovoDanjiCallback,
                '/open/vc/pay/vivo/callback': TuYouPayVivo.doVivoCallback,
                '/open/vc/pay/xiaomi/callback': TuYouPayXiaomi.doXiaomiCallback,
                '/open/vc/pay/xiaomidanji/callback': TuYouPayXiaomi.doXiaomiDanJiCallback,
                '/open/vc/pay/360pay/callback': TuYouPay360pay.do360payCallback,
                '/open/vc/pay/linkyun/ido/callback': TuYouPayIDO.doIDOCallback,
                '/open/vc/pay/huawei/callback': TuYouPayHuaWei.doHuaWeiCallback,
                '/open/vc/pay/youku/callback': TuYouPayYouKu.doYouKuCallback,
                '/open/vc/pay/pps/callback': TuYouPayPPS.doPPSCallback,
                '/open/vc/pay/langtian/callback': TuYouPayLangtian.doLangtianCallback,
                '/open/vc/pay/yipay/callback': TuYouPayYi.doYiPayCallback,
                '/open/vc/pay/yipaysdk/callback': TuYouPayYiSdk.doYiSdkPayCallback,
                '/open/vc/pay/muzhiwan/callback': TuYouPayMuzhiwan.doMuzhiwanCallback,
                '/open/vc/pay/jinri/callback': TuYouPayJinri.doJinriCallback,
                '/open/vc/pay/zhangyue/callback': TuYouPayZhangYue.doZhangYueCallback,
                '/open/vc/pay/zhangyuenew/callback': TuYouPayZhangYue.doZhangYueCallback,
                '/open/vc/pay/zhuowang/callback': TuYouPayZhuowang.doZhuowangCallback,
                '/open/vc/pay/uc/callback': TuYouPayUc.doUcCallback,
                '/open/vc/pay/ucdj/callback': TuYouPayUcDj.doUcDjCallback,
                '/open/vc/pay/9xiu/callback': TuYouPayJiuxiu.doJiuxiuCallback,
                '/open/vc/pay/duoku/msg/callback': TuYouPayDuoKu.doDuoKuCallback,
                '/open/vc/pay/wxpay/callback': TuYouPayWXpay.doWXpayCallback,
                '/open/vc/pay/shuzitianyu/callback': TuYouPaySzty.doSztyPayCallback,
                '/open/vc/pay/szty/h5/callback': TuYouPayShuzitianyuH5.doSztyPayH5Callback,
                '/open/vc/pay/momo/callback': TuYouPayMomo.doMomoCallback,
                '/open/vc/pay/palm/callback': TuYouPayPalm.doPalmCallback,
                '/open/vc/pay/palm/closeview/callback': TuYouPayPalm.doPalmCloseCallback,
                '/open/vc/pay/yygame/callback': TuYouPayYYGame.doYYgameCallback,
                '/open/vc/pay/meizu/callback': TuYouPayMeizu.doMeizuPayCallback,
                '/open/vc/pay/jinritoutiao/callback': TuYouPayJinritoutiao.doJinritoutiaoCallback,
                '/open/vc/pay/gefu/callback': TuYouPayGeFu.doGeFuPayCallback,
                '/open/vc/pay/gefusdk/callback': TuYouPayGeFu.doGeFuPayCallback,
                '/open/vc/pay/googleiab/callback': TuyouPayGoogleIAB.doGoogleIABCallback,
                '/open/vc/pay/maopao/callback': TuYouMaoPao.doMaopaoPayCallback,
                '/open/vc/pay/daodao/callback': TuYouPayDaodao.doDaodaoCallback,
                '/open/vc/pay/gefubigsdk/callback': TuYouPayGeFuBigSdk.doGeFuBigPaySdkCallback,
                '/open/vc/pay/jinli/callback': TuYouPayJinli.doJinliCallback,
                '/open/vc/pay/aidongman/callback': TuYouPayAiDongMan.doAiDongManCallback,
                '/open/vc/pay/xyzs/callback': TuYouPayXYZS.doXYZSPayCallback,
                '/open/vc/pay/xyzsdj/callback': TuYouPayXYZS.doXYZSDJPayCallback,
                '/open/vc/pay/mingtiandongli/callback': TuYouPayMingTianDongLiApi.doMingTianDongLiApiCallback,
                # '/open/vc/pay/alinewpay/callback' : TuyouPayTuyouAli.doAliCallbackNew,
                '/open/vc/pay/ppzhushou/callback': TuYouPayPPZhuShou.doPPZhuShouPayCallback,
                '/open/vc/pay/aisi/callback': TuYouPayAiSi.doPayAiSiCallback,
                '/open/vc/pay/haimawan/callback': TuYouPayHaiMaWan.doPayHaiMaWanCallback,
                '/open/vc/pay/itools/callback': TuYouPayiTools.doiToolsPayCallback,
                '/open/vc/pay/kuaiyongpingguo/callback': TuYouPayKuaiYongPingGuo.doKuaiYongPingGuoPayCallback,
                '/open/vc/pay/anzhi/callback': TuYouPayAnZhi.doAnZhiCallback,
                '/open/vc/pay/tongbutui/callback': TuYouPayTongBuTui.doTongBuTuiPayCallback,
                '/open/vc/pay/vipchinamobile/callback': TuYouPayHuiYuanBaoYue.doChinaMobileMonthlycallback,
                '/open/vc/pay/vipchinaunion/callback': TuYouPayHuiYuanBaoYue.doChinaUnionMonthlycallback,
                '/open/vc/pay/viptelecom/callback1': TuYouPayHuiYuanBaoYue.doChinaTelecomMonthlycallback1,
                '/open/vc/pay/viptelecom/callback2': TuYouPayHuiYuanBaoYue.doChinaTelecomMonthlycallback2,
                '/open/vc/pay/vipmobiletoorder/callback': TuYouPayHuiYuanBaoYue.doGetPhonenumToOrdercallback,
                '/open/vc/pay/midashi/callback': TuYouPayMiDaShi.doMiDaShiPayCallback,
                '/open/vc/pay/iappay/callback': TuYooIappay.doIappayPayCallback,
                # for ty/360 http api
                '/open/v3/pay/getchip': TuYouSLL.get_chip,
                '/open/v3/pay/incrchip': TuYouSLL.incr_chip,
                '/open/v3/pay/exchangebean': TuYouSLL.exchange_bean,
                # qipai pay
                '/open/v3/pay/qipai/addchip': TuYouSLL.qipai_addchip,
                '/open/v3/pay/qipai/getchip': TuYouSLL.qipai_getchip,
                # for payyiwap html charge data
                '/open/v3/pay/payyiwap/consume': TuYouPayYiWap.charge_data,
                '/open/v3/pay/payyiwap/verifyReceipt': TuYouPayYiWap.verify_receipt,
                '/open/v3/pay/payyiwap/paddingPhoneNumber': TuYouPayYiWap.padding_phonenumber,
                # for return plug info
                '/open/v3/upgradev3/checkplugin/plugininfo': TuYouCheckPlugin.plugin_info,
                # iiapple
                '/open/vc/pay/iiapple/callback': TuYouIIApple.doCallback,
                # borui now
                '/open/vc/pay/now/callback': TuYouNow.doCallback,
                '/open/vc/pay/wandoujia/callback': TuYouPayWanDouJia.doWanDouJiaCallback,
                '/open/vc/pay/unionpay/callback': TuYouPayUnionPay.doUnionPayCallback,
                '/open/vc/pay/mumayi/callback': TuYouPayMumayi.doCallback,
                '/open/vc/pay/pengyouwan/callback': TuYouPayPengyouwan.doCallback,
                '/open/vc/pay/4399/callback': TuYouPayM4399.doCallback,
                '/open/vc/pay/zhuoyi/callback': TuYouPayZhuoyi.doCallback,
                '/open/vc/pay/sougou/callback': TuYouPaySougou.doCallback,
                '/open/vc/pay/coolpad/callback': TuYouPayCoolpad.doCallback,
                '/open/vc/pay/jolo/callback': TuYouPayJolo.doCallback,
                '/open/vc/pay/papa/callback': TuYouPayPapa.doCallback,
                '/open/vc/pay/kuaiwan/callback': TuYouPayKuaiwan.doCallback,
                '/open/vc/pay/changba/callback': TuYouPayChangba.doCallback,
                '/open/vc/pay/lizi/callback': TuYouPayLizi.doCallback,
                '/open/vc/pay/nubia/callback': TuYouPayNubia.doCallback,
                '/open/vc/pay/letv/callback': TuYouPayLetv.doCallback,
            }

            from tysdk import is_test_sdk_server
            if is_test_sdk_server():
                cls.HTMLPATHS.update({
                    '/open/v3/pay/mockpay': MockPay.mock,
                    '/open/v3/mockios/verifyReceipt': MockPay.mockIosVerifyReceipt,
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
             'payType', 'payInfo', 'packageName', 'channelName'])
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
                                                 'payType', 'payInfo', 'packageName', 'channelName'])
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

        chargeKey = 'sdk.charge:' + platformOrderId
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        if chargeInfo == None:
            chargeInfo = {}
        else:
            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)

        Order.log(platformOrderId, Order.CLIENT_CANCELED, userId, appId, clientId,
                  shortId=shortId, prodOrderId=productOrderId, paytype=paytype,
                  prodid=chargeInfo.get('prodId', 'na'),
                  diamondid=chargeInfo.get('diamondId', 'na'),
                  charge_price=chargeInfo.get('chargeTotal', 'na'),
                  subevent=reason, info=errinfo if errinfo else 'na')
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('cancelorder')
        mo = mo.packJson()
        return mo
