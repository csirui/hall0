# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 16时55分58秒
# FileName:      http91.py
# Class:         Http91Tasklet

# from trunk svn 7501 2014-10-04 10:58

from tyframework.context import TyContext
from tysdk.entity.pay.pay import TuyouPay
from tysdk.entity.pay.pay114 import TuyouPay114
from tysdk.entity.pay.pay360 import TuYouPay360
from tysdk.entity.pay.pay360liantongwo import TuYouPay360LianTongW
from tysdk.entity.pay.pay360pay import TuyouPay360pay
from tysdk.entity.pay.pay360sns import TuYouPay360SNS
from tysdk.entity.pay.pay360ydmm import TuYouPay360YdMm
from tysdk.entity.pay.payaibei import TuYouPayAibei
from tysdk.entity.pay.payaigame import TuYouPayAiGame
from tysdk.entity.pay.paybaidu import TuYouPayBaidu
from tysdk.entity.pay.paychangtianyou import TuYouChangeTianYou
from tysdk.entity.pay.paydoumeng import TuyouPayDoumeng
from tysdk.entity.pay.payduoku import TuYouPayDuoKu
from tysdk.entity.pay.payhuafubao import TuyouPayHuafubao
from tysdk.entity.pay.payhuawei import TuyouPayHuaWei
from tysdk.entity.pay.payido import TuyouPayIDO
from tysdk.entity.pay.payios import TuYouPayIos
from tysdk.entity.pay.payjingdong import TuYouPayJingDong
from tysdk.entity.pay.paylaohu import TuYouPayLaoHu
from tysdk.entity.pay.paylenovo import TuYouPayLenovo
from tysdk.entity.pay.payliantong import TuYouPayLianTong
from tysdk.entity.pay.payliantongw import TuYouPayLianTongW
from tysdk.entity.pay.paylinkyun import TuYouPayLinkYun
from tysdk.entity.pay.paylinkyunapp import TuYouPayLinkYunApp
from tysdk.entity.pay.paymo9 import TuyouPayMo9pay
from tysdk.entity.pay.paymomo import TuYouPayMomo
from tysdk.entity.pay.paymsgdx import TuYouPayMsgDx
from tysdk.entity.pay.paymsgyd import TuYouPayMsgYd
from tysdk.entity.pay.paymsgydgs import TuYouPayMsgYdGs
from tysdk.entity.pay.payoppo import TuyouPayOppo
from tysdk.entity.pay.payqtld import TuyouPayQtld
from tysdk.entity.pay.payrdo import TuYouPayRdo
from tysdk.entity.pay.payshediao import TuyouPayShediao
from tysdk.entity.pay.payshediaoyee import TuYouPayShediaoYee
from tysdk.entity.pay.paytencentpay import TuyouPayTencentPay
from tysdk.entity.pay.paytianyi import TuYouPayTianYi
from tysdk.entity.pay.paytuyou import TuyouPayTuyou
from tysdk.entity.pay.payuucun import TuYouPayUuCun
from tysdk.entity.pay.paywandoujia import TuYouPayWanDouJia
from tysdk.entity.pay.paywx import TuyouPayWXpay
from tysdk.entity.pay.payxiaomi import TuyouPayXiaomi
from tysdk.entity.pay.payxinyinhe import TuYouPayXinYinHe
from tysdk.entity.pay.payydjd import TuYouPayYdjd
from tysdk.entity.pay.payydmm import TuYouPayYdMmWeak
from tysdk.entity.pay.payyee import TuYouPayYee
from tysdk.entity.pay.payyee2 import TuYouPayYee2
from tysdk.entity.pay.payyidongmm import TuYouPayYdMm
from tysdk.entity.pay.payyidongmmtuyou import TuYouPayYdMmTy
from tysdk.entity.pay.payyingyonghui import TuYouPayYingYongHui
from tysdk.entity.pay.payyouku import TuyouPayYouku
from tysdk.entity.pay.payzhangqu import TuYouPayZhangQu
from tysdk.entity.pay.payzhuowang import TuYouPayZhuoWang


class HttpPay(object):
    JSONPATHS = None
    HTMLPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not HttpPay.JSONPATHS:
            HttpPay.JSONPATHS = {
                '/v1/pay/charge': HttpPay.doCharge,
                '/v1/pay/straight': HttpPay.doStraight,
                '/v1/pay/coupon/charge/request': HttpPay.doChangTianYouChargeRequest,
                '/v1/pay/coupon/charge/confirm': HttpPay.doChangTianYouChargeConfirm,
                '/v1/pay/coupon/charge/history': HttpPay.doChangTianYouChargeHistory,
                '/v1/pay/paytype/get': HttpPay.doGetPayType,
                '/open/v1/pay/coupon/charge/request_inner': HttpPay.doChangTianYouChargeRequestInner,
            }
        return HttpPay.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not HttpPay.HTMLPATHS:
            HttpPay.HTMLPATHS = {
                '/open/va/pay/alipay/callback': TuyouPayTuyou.doAliCallback,
                '/open/va/pay/wxpay/callback': TuyouPayWXpay.doWXpayCallback,
                '/open/va/pay/card/callback': TuyouPayTuyou.doCardCallback,
                '/open/va/pay/caifutong/notify': TuyouPayTuyou.doCaiFuTongNotify,
                '/open/va/pay/caifutong/callback': TuyouPayTuyou.doCaiFuTongCallback,
                '/open/va/pay/shediao/alipay/callback': TuyouPayShediao.doAliCallback,
                '/open/va/pay/shediao/card/callback': TuyouPayShediao.doCardCallback,
                '/open/va/pay/shediao/caifutong/notify': TuyouPayShediao.doCaiFuTongNotify,
                '/open/va/pay/shediao/caifutong/callback': TuyouPayShediao.doCaiFuTongCallback,
                '/open/va/pay/360/callback': TuYouPay360.do360Callback,
                '/open/va/pay/360/msg/callback': TuYouPay360.do360CallbackMsg,
                '/open/va/pay/yingyonghui/msg/callback': TuYouPayYingYongHui.doYyhCallbackMsg,
                '/open/va/pay/duoku/msg/callback': TuYouPayDuoKu.doDuoKuCallbackMsg,
                '/open/va/pay/xiaomi/callback': TuyouPayXiaomi.doXiaomiCallback,
                '/open/va/pay/xiaomidanji/callback': TuyouPayXiaomi.doXiaomiDanJiCallback,
                '/open/va/pay/yd/callback': TuYouPayMsgYd.doMsgYdCallback,
                '/open/va/pay/mh/callback': TuYouPayMsgDx.doMsgDxCallback,
                '/open/va/pay/ydgs/callback': TuYouPayMsgYdGs.doMsgYdGsCallback,
                '/open/va/pay/yee/callback': TuYouPayYee.doCardCallback,
                '/open/va/pay/shediaoyee/callback': TuYouPayShediaoYee.doCardCallback,
                '/open/va/pay/ios/callback': TuYouPayIos.doIosCallback,
                '/open/va/pay/wandoujia/callback': TuYouPayWanDouJia.doWanDouJiaCallback,
                '/open/va/pay/lenovo/callback': TuYouPayLenovo.doLenovoCallback,
                '/open/va/pay/jingdong/callback': TuYouPayJingDong.doJingDongCallback,
                '/open/va/pay/jingdong/getrole': TuYouPayJingDong.doJingDongGetRole,
                '/open/va/pay/jingdong/getorder': TuYouPayJingDong.doJingDongGetOrder,
                '/open/va/pay/aibei/callback': TuYouPayAibei.doAiBeiCallback,
                '/open/va/pay/baidu/callback': TuYouPayBaidu.doBaiDuCallback,
                '/open/va/pay/yidongmm/msg/callback': TuYouPayYdMm.doYdMmCallbackMsg,
                '/open/va/pay/yidongmmtuyou/msg/callback': TuYouPayYdMmTy.doYdMmTyCallbackMsg,
                '/open/va/pay/liantong/callback': TuYouPayLianTong.doLianTongCallback,

                '/open/va/pay/changtianyou/callback': TuYouChangeTianYou.doChangTianYouCallback,
                '/open/vc/pay/changtianyou/callback': TuYouChangeTianYou.doChangTianYouCallback,

                '/open/va/pay/tianyi/msg/callback': TuYouPayTianYi.doTianyiCallbackMsg,
                '/open/va/pay/aigame/msg/callback': TuYouPayAiGame.doAiGameMsgCallback,
                '/open/va/pay/aiyouxi/callback1': TuYouPayAiGame.doAiGameMsgCallback,
                '/open/va/pay/aigame/callback': TuYouPayAiGame.doAiGameCallback,
                '/open/va/pay/aiyouxi/callback2': TuYouPayAiGame.doAiGameCallback,

                '/open/va/pay/aiyouxi/callback/dizhu/happy': TuYouPayAiGame.doAiGameCallbackDizhuHappy,
                '/open/va/pay/aiyouxi/callback/dizhu/huabei': TuYouPayAiGame.doAiGameCallbackDizhuHuabei,
                '/open/va/pay/aiyouxi/callback/dizhustar/zszh/wf': TuYouPayAiGame.doAiGameCallbackDizhuStarZszhWF,
                '/open/va/pay/aiyouxi/callback/dizhustar/zszh/pt': TuYouPayAiGame.doAiGameCallbackDizhuStarZszhPT,

                '/open/va/pay/aigame/all/callback': TuYouPayAiGame.doAiGameAllCallback,

                '/open/va/pay/laohu/callback': TuYouPayLaoHu.doLaoHuCallback,
                '/open/va/pay/momo/callback': TuYouPayMomo.doMomoCallback,
                '/open/va/pay/ydmm/callback': TuYouPayYdMmWeak.doYdMmCallback,
                '/open/va/pay/ydjd/callback': TuYouPayYdjd.doYdjdCallback,
                '/open/va/pay/linkyun/confirm': TuYouPayLinkYun.doLinkYunConfirm,
                '/open/va/pay/linkyun/callback': TuYouPayLinkYun.doLinkYunCallback,
                '/open/va/pay/linkyun/union/confirm': TuYouPayLinkYun.doLinkYunUnionConfirm,
                '/open/va/pay/linkyun/union/callback': TuYouPayLinkYun.doLinkYunUnionCallback,
                '/open/va/pay/linkyun/ltsdk/callback': TuYouPayLinkYun.doLinkYunLtsdkCallback,
                '/open/va/pay/linkyun/dx/callback': TuYouPayLinkYun.doLinkYunDxCallback,
                '/open/va/pay/linkyunapp/callback': TuYouPayLinkYunApp.doLinkYunCallback,
                '/open/va/pay/linkyunapp/union/callback': TuYouPayLinkYunApp.doLinkYunUnionCallback,
                '/open/va/pay/oppo/callback': TuyouPayOppo.doOppoCallback,
                '/open/va/pay/youku/callback': TuyouPayYouku.doYoukuCallback,
                '/open/va/pay/qtld/callback': TuyouPayQtld.doQtldCallback,
                '/open/va/pay/114/callback': TuyouPay114.do114Callback,
                '/open/va/pay/360pay/callback': TuyouPay360pay.do360payCallback,
                '/open/va/pay/linkyun/ido/callback': TuyouPayIDO.doIDOCallback,
                '/open/va/pay/doumeng/callback': TuyouPayDoumeng.doDoumengCallback,
                '/open/va/pay/huafubao/callback': TuyouPayHuafubao.doHuafubaoCallback,
                '/open/va/pay/huafubao/getorder': TuyouPayHuafubao.doHuafubaoGetOrder,
                '/open/va/pay/liantongw/callback': TuYouPayLianTongW.doLianTongWCallback,
                '/open/va/pay/yee2/callback10': TuYouPayYee2.doTestCallback,
                '/open/va/pay/yee2/callback11': TuYouPayYee2.doCallback2,
                '/open/va/pay/yee2/callback20': TuYouPayYee2.doTuYouCallback,
                '/open/va/pay/yee2/callback21': TuYouPayYee2.doCallback2,
                '/open/va/pay/yee2/callback30': TuYouPayYee2.doSheDiaoCallback,
                '/open/va/pay/yee2/callback31': TuYouPayYee2.doCallback2,
                '/open/va/pay/360sns/callback': TuYouPay360SNS.do360CallbackSNS,
                '/open/va/pay/360ydmm/callback': TuYouPay360YdMm.do360YdMmCallback,
                '/open/va/pay/360liantongwo/callback': TuYouPay360LianTongW.doLianTongWCallback,
                '/open/va/pay/xinyinhe/callback': TuYouPayXinYinHe.doXinYinHeCallback,
                '/open/va/pay/zhangqu/callback': TuYouPayZhangQu.doZhangQuCallback,
                '/open/va/pay/uucun/callback': TuYouPayUuCun.doUuCunCallback,
                '/open/va/pay/huawei/callback': TuyouPayHuaWei.doHuaWeiCallback,
                '/open/va/pay/tencent/callback': TuyouPayTencentPay.doTencentPayCallback,
                '/open/va/pay/zhuowang/callback': TuYouPayZhuoWang.doZhuoWangCallback,
                '/open/va/pay/rdo/callback': TuYouPayRdo.doRdoCallback,
                '/open/va/pay/mo9/callback': TuyouPayMo9pay.doMo9payCallback,
            }
        return HttpPay.HTMLPATHS

    @classmethod
    def _checkPayParams(self):
        errors = []
        params = {}
        TyContext.RunHttp.getRequestParamJs(params, 'authInfo', '')
        TyContext.RunHttp.getRequestParamJs(params, 'appId', '0')
        TyContext.RunHttp.getRequestParamJs(params, 'clientId', '')
        TyContext.RunHttp.getRequestParamJs(params, 'deviceId', '')
        TyContext.RunHttp.getRequestParamJs(params, 'appInfo', '')
        TyContext.RunHttp.getRequestParamJs(params, 'orderId', '')
        TyContext.RunHttp.getRequestParamJs(params, 'orderName', '')
        TyContext.RunHttp.getRequestParamJs(params, 'orderPrice', '0')
        TyContext.RunHttp.getRequestParamJs(params, 'orderDesc', '')
        TyContext.RunHttp.getRequestParamJs(params, 'orderPicUrl', '')
        TyContext.RunHttp.getRequestParamJs(params, 'payType', '')
        TyContext.RunHttp.getRequestParamJs(params, 'card_amount', '')
        TyContext.RunHttp.getRequestParamJs(params, 'card_number', '')
        TyContext.RunHttp.getRequestParamJs(params, 'card_pwd', '')
        TyContext.RunHttp.getRequestParamJs(params, 'card_code', '')
        TyContext.RunHttp.getRequestParamJs(params, 'phonenum', '')
        TyContext.RunHttp.getRequestParamJs(params, 'raffle', '0')
        TyContext.RunHttp.getRequestParamJs(params, 'prodId', '')
        TyContext.RunHttp.getRequestParamJs(params, 'phoneType', '')
        TyContext.RunHttp.getRequestParamJs(params, 'wxappId', '')
        TyContext.RunHttp.getRequestParamJs(params, 'mo9appId', '')
        TyContext.RunHttp.getRequestParamJs(params, 'yeeChannel', 'tuyoo')

        userId, userName, userTime = TyContext.AuthorCode.checkUserAuthorInfo(params['authInfo'])
        if userId <= 0:
            errors.append('authInfo is incorrect, ')

        gameOrderId = params['orderId']
        if gameOrderId <= 0:
            errors.append('order Id is missing, ')
        platformOrderId = TyContext.RedisPayData.execute('HGET', 'gameOrder:' + str(gameOrderId), 'platformOrder')
        if platformOrderId:
            errors.append('orderId %s is already bound to platformOrder %s, ' % (gameOrderId, platformOrderId))

        try:
            if int(float(params['orderPrice'])) <= 0:
                errors.append('order Price is zero, ')
        except:
            errors.append('order Price is incorrect, ')

        checkCard = False
        checkPhoneNum = False
        payType = params['payType']
        if payType in ['tuyou.card.lt', 'tuyou.card.dx', 'tuyou.card.yd']:
            checkCard = True
        elif payType in ['shediao.card.lt', 'shediao.card.dx', 'shediao.card.yd']:
            checkCard = True
        elif payType in ['tuyou.msgyd', 'tuyou.msgdx']:
            checkPhoneNum = True
        elif payType in ['tuyou.ali', 'tuyou.caifutong', 'tuyou.msgyd', 'tuyou.msgdx']:
            pass
        elif payType in ['shediao.ali', 'shediao.caifutong', 'shediao.msgyd', 'shediao.msgdx']:
            pass
        elif payType in ['360.card.dx', '360.card.yd', '360.card.lt']:
            checkCard = True
        elif payType in ['360.msg']:
            prodId = params['prodId']
            if len(prodId) == 0:
                errors.append('prodId is incorrect')
        elif payType in ['tencentpay', 'qq.coin', 'qq.goods']:
            pass
        elif payType in ['360.ali', '360.msg']:
            pass
        elif payType in ['wxpay']:
            pass
        elif payType in ['mo9pay']:
            pass
        elif payType in ['xiaomi.common', 'xiaomi.danji', 'yingyonghui.msg', 'duoku.msg', 'lenovo', 'wandoujia',
                         'aibei', 'baidu', 'yidongmm.msg',
                         'yidongmmtuyou.msg', 'liantong', 'jingdong', 'EFTChinaUnion.msg', 'EFTChinaTelecom.msg',
                         'tianyi.msg', 'aigame.msg',
                         'aigame', 'laohu.msg', 'momo', 'ydmm', 'ydjd',
                         'tuyooios', 'linkyun', 'linkyununion', 'linkyunltsdk', 'linkyundx', 'nearme', 'huafubao',
                         'kugou', 'liantong.wo',
                         'yee2', 'yee2.card1', 'yee2.card2', '360pay', '360.sns', '360.ydmm', '360.liantong.wo',
                         'newYinHe', 'zhangqu', 'uu.msg', 'YingYongBao', 'zhuowangMdo',
                         'huawei', 'youku', 'qtld', '114', 'doumeng', 'linkyun.ido', 'rdo']:
            pass
        elif payType in ['yee.card']:
            checkCard = True
            card_code = params['card_code']
            if not card_code in ['JUNNET', 'SNDACARD', 'SZX', 'ZHENGTU', 'QQCARD', \
                                 'UNICOM', 'JIUYOU', 'YPCARD', 'NETEASE', 'WANMEI', \
                                 'SOHU', 'TELECOM', 'ZONGYOU', 'TIANXIA', 'TIANHONG']:
                errors.append('card_code is missing, ')

        elif payType in ['shediao.yee.card']:
            checkCard = True
            card_code = params['card_code']
            if not card_code in ['JUNNET', 'SNDACARD', 'SZX', 'ZHENGTU', 'QQCARD', \
                                 'UNICOM', 'JIUYOU', 'YPCARD', 'NETEASE', 'WANMEI', \
                                 'SOHU', 'TELECOM', 'ZONGYOU', 'TIANXIA', 'TIANHONG']:
                errors.append('card_code is missing, ')
        else:
            errors.append('payType is incorrect, ')

        if checkCard:
            '''
            try:
                if float(params['card_amount']) <= 0 :
                    errors.append('card_amount is zero, ')
            except: 
                errors.append('card_amount is incorrect, ')
                
            if len(params['card_number']) <= 0 :
                errors.append('card_number is missing, ')

            if len(params['card_pwd']) <= 0 :
                errors.append('card_pwd is missing, ')
            '''
            try:
                if float(params['card_amount']) <= 0:
                    errors.append('卡面额不正确 ')
            except:
                errors.append('卡面额不正确 ')

            try:
                card_num = str(params['card_number'])
                lcard_num = len(card_num)
                card_pwd = str(params['card_pwd'])
                lcard_pwd = len(card_pwd)
                if lcard_num <= 0 or lcard_num > 100 \
                        or lcard_pwd <= 0 or lcard_pwd > 100 \
                        or not card_num.isalnum() or not card_pwd.isalnum():
                    errors.append('卡号或卡密不正确 ')
            except:
                errors.append('卡号或卡密不正确 ')

        if checkPhoneNum:
            if len(params['phonenum']) < 11:
                # errors.append('phone number is missing, ')
                errors.append('手机号不正确 ')

        try:
            if int(float(params['raffle'])) < 0:
                errors.append('raffle is incorrect, ')
        except:
            errors.append('raffle is incorrect, ')

        # 根据userId获取手机卡类型
        if params['phoneType'] == '' and userId > 0:
            phoneType = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sessionPhoneType')
            params['phoneType'] = phoneType

        return userId, errors, params

    @classmethod
    def doCharge(self, rpath):
        userId, errors, params = self._checkPayParams()
        if userId <= 0 or len(errors) > 0:
            errinfo = ', '.join(errors)
            #             TyContext.ftlog.error('******** doCharge out errors=', errinfo)
            mo = TyContext.Cls_MsgPack()
            mo.setCmd('/v1/pay/charge')
            mo.setError('code', 1)
            mo.setError('info', errinfo)
            return mo
        mo = TuyouPay.doBuyCharge(userId, params)
        #         TyContext.ftlog.info('********** doCharge out return=', mo.packJson())
        return mo

    @classmethod
    def doStraight(self, rpath):
        userId, errors, params = self._checkPayParams()
        if userId <= 0 or len(errors) > 0:
            errinfo = ', '.join(errors)
            #             TyContext.ftlog.error('******** doStraight out errors=', errinfo)
            mo = TyContext.Cls_MsgPack()
            mo.setCmd('/v1/pay/straight')
            mo.setError(1, errinfo)
            return mo
        mo = TuyouPay.doBuyStraight(userId, params)
        #         TyContext.ftlog.info('********** doStraight out return=', mo.packJson())
        return mo

    @classmethod
    def doChangTianYouChargeRequest(cls, path):
        gameId, userId, mo = cls.checkUserInfo()
        if userId > 0:
            money = TyContext.RunHttp.getRequestParamInt('chargeMoney')
            couponCount = TyContext.RunHttp.getRequestParamInt('couponCount')
            TuYouChangeTianYou.doChangTianYouChargeRequest(gameId, userId, mo, couponCount, money)
        # TyContext.ftlog.info('********** doChangTianYouChargeRequest out return=', mo.packJson())
        return mo

    @classmethod
    def doChangTianYouChargeRequestInner(cls, path):
        mo = TyContext.Cls_MsgPack()
        money = TyContext.RunHttp.getRequestParamInt('money')
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        userId = TyContext.RunHttp.getRequestParamInt('userId')
        couponCount = TyContext.RunHttp.getRequestParamInt('couponCount')
        TuYouChangeTianYou.doChangTianYouChargeRequest(gameId, userId, mo, couponCount, money)
        #         TyContext.ftlog.info('********** doChangTianYouChargeRequest out return=', mo.packJson())
        return mo

    @classmethod
    def doChangTianYouChargeConfirm(cls, path):
        mo = TyContext.Cls_MsgPack()
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        TuYouChangeTianYou.doChangTianYouChargeConfirm(gameId, mo)
        #         TyContext.ftlog.info('********** doChangTianYouChargeConfirm out return=', mo.packJson())
        return mo

    @classmethod
    def doChangTianYouChargeHistory(cls, path):
        gameId, userId, mo = cls.checkUserInfo()
        if userId > 0:
            TuYouChangeTianYou.doChangTianYouChargeHistory(gameId, userId, mo)
        # TyContext.ftlog.info('********** doChangTianYouChargeHistory out return=', mo.packJson())
        return mo

    @classmethod
    def __process_ydmm_stopped_list(cls, citycode, clientId, mo):
        price = mo.getResultInt('price')
        paytype = mo.getResultStr('payType')
        if paytype != 'ydmm':
            TyContext.ftlog.debug('ydmm_stopped_list not ydmm, is', paytype)
            return
        stoplist = TyContext.Configure.get_global_item_json('ydmm_stopped_list', {})
        TyContext.ftlog.debug('ydmm_stopped_list stoplist', stoplist, 'mo', mo, 'citycode', citycode, 'clientId',
                              clientId)
        for config in stoplist.values():
            if clientId not in config['resortto']:
                continue
            if str(citycode) not in config['stopped_provs']:
                continue
            if 'fallback' in config['stopped_provs'] \
                    and price in config['stopped_provs']['prices']:
                mo.setResult('payType', config['stopped_provs']['fallback'])
                TyContext.ftlog.debug('ydmm_stopped_list paytype fallback to', config['stopped_provs']['fallback'])
                return
            mo.setResult('payType', config['resortto'][clientId])
            TyContext.ftlog.debug('ydmm_stopped_list paytype resort to', config['resortto'][clientId])
            return
        TyContext.ftlog.debug('ydmm_stopped_list ydmm not changed')

    @classmethod
    def doGetPayType(cls, path):
        mo = TyContext.Cls_MsgPack()
        appId = TyContext.RunHttp.getRequestParam('appId', '')
        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        buttonId = TyContext.RunHttp.getRequestParam('buttonId', '')
        # unlimit = TyContext.RunHttp.getRequestParam('unlimit', '0')
        phonetype = TyContext.RunHttp.getRequestParam('phonetype', '0')
        authInfo = TyContext.RunHttp.getRequestParam('authInfo', '')
        userId, userName, userTime = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        if userId > 0:
            unlimit = TyContext.SmsPayCheck.is_sms_pay_limited(userId)
            # citycode = TyContext.UserSession.get_session_city_zip(userId)
            citycode, _ = TyContext.UserSession.get_session_zipcode(userId)
            TyContext.PayType.append_pay_type_info(appId, clientId, buttonId, unlimit, phonetype, citycode, userId, mo)
            try:
                cls.__process_ydmm_stopped_list(citycode, clientId, mo)
            except:
                TyContext.ftlog.exception()
        else:
            mo.setResult('code', '2')
            mo.setResult('info', 'authInfo is timeout !')
        return mo

    @classmethod
    def checkUserInfo(cls):
        gameId = TyContext.RunHttp.getRequestParamInt('gameId')
        authInfo = TyContext.RunHttp.getRequestParam('authInfo')
        userId, userName, authorTime = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        mo = TyContext.Cls_MsgPack()
        if userId > 0 and gameId > 0:
            return gameId, userId, mo
        else:
            mo.setError(1, 'gameId authorInfo error')
            return 0, 0, mo
