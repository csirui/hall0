# -*- coding=utf-8 -*-

import copy

from tyframework.context import TyContext


class TuyouPayChargeConf(object):
    _chargetype2thirdpay_dict = {
        'cat_duandai': 'tysdk.entity.paythird.payduandai.TuYouPayDuandai',
        'cat_list_tuyou': 'tysdk.entity.paythird.paycattuyou.TuYouPayCatTuyou',
        'cat_list_tuyou_weixin': 'tysdk.entity.paythird.paycattuyouweixin.TuYouPayCatTuyouWeixin',
        'cat_list_360': 'tysdk.entity.paythird.paycat360.TuYouPayCat360',
        'cat_list_360_dezhou': 'tysdk.entity.paythird.paycat360dezhou.TuYouPayCat360Dezhou',
        '360.msg': 'tysdk.entity.paythird.pay360msg.TuYouPay360Msg',
        'tuyou.ali': 'tysdk.entity.paythird.paytuyou_ali.TuyouPayTuyouAli',
        #         'yingyonghui.msg'       : 'tysdk.entity.paythird.payyingyonghui.TuYouPayYingYongHui',
        #         'duoku.msg'             : 'tysdk.entity.paythird.payduoku.TuYouPayDuoKu',
        #         'lenovo'                : 'tysdk.entity.paythird.paylenovo.TuYouPayLenovo',
        #         'aibei'                 : 'tysdk.entity.paythird.payaibei.TuYouPayAibei',
        #         'baidu'                 : 'tysdk.entity.paythird.paybaidu.TuYouPayBaidu',
        #         'yidongmm.msg'          : 'tysdk.entity.paythird.payyidongmm.TuYouPayYdMm',
        #         'yidongmmtuyou.msg'     : 'tysdk.entity.paythird.payyidongmmtuyou.TuYouPayYdMmTy',
        #         'liantong'              : 'tysdk.entity.paythird.payliantong.TuYouPayLianTong',
        'liantong.wo': 'tysdk.entity.paythird.payliantongwo.TuYouPayLianTongWo',
        'EFTChinaUnion.msg': 'tysdk.entity.paythird.payeftunion.TuYouPayEftUnion',
        'EFTChinaTelecom.msg': 'tysdk.entity.paythird.payeftdx.TuYouPayMsgDx',
        #         'tianyi.msg'            : 'tysdk.entity.paythird.paytianyi.TuYouPayTianYi',
        #         'momo'                  : 'tysdk.entity.paythird.paymomo.TuYouPayMomo',
        'ydmm': 'tysdk.entity.paythird.payydmm.TuYouPayYdMmWeak',
        'ydjd': 'tysdk.entity.paythird.payydjd.TuYouPayYdjd',
        'aigame': 'tysdk.entity.paythird.payaigame.TuYouPayAiGame',
        'tuyooios': 'tysdk.entity.paythird.paytuyooios.TuYouPayMyIos',
        'linkyun': 'tysdk.entity.paythird.paylinkyun.TuYouPayLinkYun',
        'nearme': 'tysdk.entity.paythird.payoppo.TuyouPayOppo',
        'lenovo': 'tysdk.entity.paythird.paylenovo.TuYouPayLenovo',
        'vivo': 'tysdk.entity.paythird.payvivo.TuYouPayVivo',
        'xiaomi.common': 'tysdk.entity.paythird.payxiaomi.TuYouPayXiaomi',
        '360pay': 'tysdk.entity.paythird.pay360pay.TuYouPay360pay',
        'linkyun.ido': 'tysdk.entity.paythird.payido.TuYouPayIDO',
        'linkyun.api': 'tysdk.entity.paythird.paylinkyunapi.TuYouPayLinkYunApi',
        'xiaomi.danji': 'tysdk.entity.paythird.payxiaomi.TuYouPayXiaomi',
        'huawei': 'tysdk.entity.paythird.payhuawei.TuYouPayHuaWei',
        'youku': 'tysdk.entity.paythird.payyouku.TuYouPayYouKu',
        'pps': 'tysdk.entity.paythird.paypps.TuYouPayPPS',
        'yipay': 'tysdk.entity.paythird.payyi.TuYouPayYi',
        'zhangyue': 'tysdk.entity.paythird.payzhangyue.TuYouPayZhangYue',
        #         'payhuafubao'           : 'tysdk.entity.paythird.payhuafubao.TuyouPayHuafubao',
        'langtian': 'tysdk.entity.paythird.paylangtian.TuYouPayLangtian',
        'zhuowang': 'tysdk.entity.paythird.payzhuowang.TuYouPayZhuowang',
        'uc': 'tysdk.entity.paythird.payuc.TuYouPayUc',
        'ucdanji': 'tysdk.entity.paythird.payucdj.TuYouPayUcDj',
        '9xiu': 'tysdk.entity.paythird.payjiuxiu.TuYouPayJiuxiu',
        'duoku': 'tysdk.entity.paythird.payduoku.TuYouPayDuoKu',
        'EFT.api': 'tysdk.entity.paythird.payeftapi.TuYouPayEftApi',
        'lenovodj': 'tysdk.entity.paythird.paylenovodj.TuYouPayLenovoDanji',
        'yisdkpay': 'tysdk.entity.paythird.payyisdk.TuYouPayYiSdk',
        'migu': 'tysdk.entity.paythird.payyisdk.TuYouPayYiSdk',
        'muzhiwan': 'tysdk.entity.paythird.paymuzhiwan.TuYouPayMuzhiwan',
        'jinri': 'tysdk.entity.paythird.payjinri.TuYouPayJinri',
        'shuzitianyu': 'tysdk.entity.paythird.payshuzitianyu.TuYouPaySzty',
        'shuzitianyu.h5': 'tysdk.entity.paythird.payshuzitianyuh5.TuYouPayShuzitianyuH5',
        'momo': 'tysdk.entity.paythird.paymomo.TuYouPayMomo',
        'yyduowan': 'tysdk.entity.paythird.payyygame.TuYouPayYYGame',
        'meizu': 'tysdk.entity.paythird.paymeizu.TuYouPayMeizu',
        'jinritoutiao': 'tysdk.entity.paythird.payjinritoutiao.TuYouPayJinritoutiao',
        'gefu': 'tysdk.entity.paythird.paygefu.TuYouPayGeFu',
        'googleiab': 'tysdk.entity.paythird.paygoogleiab.TuyouPayGoogleIAB',
        'maopao': 'tysdk.entity.paythird.paymaopao.TuYouMaoPao',
        'daodao': 'tysdk.entity.paythird.paydaodao.TuYouPayDaodao',
        'gefusdk': 'tysdk.entity.paythird.paygefusdk.TuYouGeFuSdk',
        'gefubigsdk': 'tysdk.entity.paythird.paygefubigsdk.TuYouPayGeFuBigSdk',
        'jinli': 'tysdk.entity.paythird.payjinli.TuYouPayJinli',
        'aidongman': 'tysdk.entity.paythird.payaidongman.TuYouPayAiDongMan',
        'wxpay': 'tysdk.entity.paythird.paywx.TuYouPayWXpay',
        'xyzs': 'tysdk.entity.paythird.payxyzs.TuYouPayXYZS',
        'mingtiandongli': 'tysdk.entity.paythird.paymingtiandongli.TuYouPayMingTianDongLiApi',
        'ppzhushou': 'tysdk.entity.paythird.payppzhushou.TuYouPayPPZhuShou',
        'aisi': 'tysdk.entity.paythird.payaisi.TuYouPayAiSi',
        'haimawan': 'tysdk.entity.paythird.payhaimawan.TuYouPayHaiMaWan',
        'huabeidianhua': 'tysdk.entity.paythird.payaigame.TuYouPayAiGame',
        'itools': 'tysdk.entity.paythird.payiTools.TuYouPayiTools',
        'anzhi': 'tysdk.entity.paythird.payanzhi.TuYouPayAnZhi',
        'kuaiyongpingguo': 'tysdk.entity.paythird.paykuaiyongpingguo.TuYouPayKuaiYongPingGuo',
        'tongbutui': 'tysdk.entity.paythird.paytongbutui.TuYouPayTongBuTui',
        'huiyuan': 'tysdk.entity.paythird.payhuiyuan.TuYouPayHuiYuanBaoYue',
        'h5.youku': 'tysdk.entity.paythird.payyoukuh5.TuYouPayYouKuH5',
        'midashi': 'tysdk.entity.paythird.paymidashi.TuYouPayMiDaShi',
        'iiApple': 'tysdk.entity.paythird.payiiapple.TuYouIIApple',
        'iappay': 'tysdk.entity.paythird.payiappay.TuYooIappay',
        'iPaynow': 'tysdk.entity.paythird.paynow.TuYouNow',
        'wannew': 'tysdk.entity.paythird.paywandoujia.TuYouPayWanDouJia',
        # 'weixin'                : 'tysdk.entity.paythird.paynow.TuYouNow'
        'unionpay': 'tysdk.entity.paythird.payunionpay.TuYouPayUnionPay',
        'mumayi': 'tysdk.entity.paythird.paymumayi.TuYouPayMumayi',
        'pengyouwan': 'tysdk.entity.paythird.paypengyouwan.TuYouPayPengyouwan',
        'm4399': 'tysdk.entity.paythird.paym4399.TuYouPayM4399',
        'zhuoyi': 'tysdk.entity.paythird.payzhuoyi.TuYouPayZhuoyi',
        'sogou': 'tysdk.entity.paythird.paysougou.TuYouPaySougou',
        'coolpad': 'tysdk.entity.paythird.paycoolpad.TuYouPayCoolpad',
        'jolo': 'tysdk.entity.paythird.payjolo.TuYouPayJolo',
        'papa': 'tysdk.entity.paythird.paypapa.TuYouPayPapa',
        'kuaiwan': 'tysdk.entity.paythird.paykuaiwan.TuYouPayKuaiwan',
        'changba': 'tysdk.entity.paythird.paychangba.TuYouPayChangba',
        'lizi': 'tysdk.entity.paythird.paylizi.TuYouPayLizi',
        'nubia': 'tysdk.entity.paythird.paynubia.TuYouPayNubia',
        'letv': 'tysdk.entity.paythird.payletv.TuYouPayLetv',
    }

    # for backward compatible
    CHARGE_DATA = _chargetype2thirdpay_dict

    @classmethod
    def _import_thirdpay_func(cls, cache_funcs, chargeType, func_name):
        cpath = cls._chargetype2thirdpay_dict[chargeType]
        tks = cpath.split('.')
        mpackage = '.'.join(tks[0:-1])
        clsName = tks[-1]
        clazz = None
        exec 'from %s import %s as clazz' % (mpackage, clsName)
        cfun = getattr(clazz, func_name)
        TyContext.ftlog.debug('_import_thirdpay_func get cfun', cfun, 'for', chargeType, 'func_name', func_name)
        cache_funcs[chargeType] = cfun
        return cfun

    @classmethod
    def _get_thirdpay_func(cls, cache_funcs, chargeType, func_name):
        try:
            cfun = cache_funcs[chargeType]
        except KeyError as e:
            cfun = cls._import_thirdpay_func(cache_funcs, chargeType, func_name)
        return cfun

    @classmethod
    def _default_charge_data_func(cls, chargeinfo):
        userId = chargeinfo['uid']
        buttonId = chargeinfo['buttonId']
        clientId = chargeinfo['clientId']
        chargetype = chargeinfo['chargeType']
        clientip = TyContext.UserSession.get_session_client_ip(userId)

        from tysdk.entity.pay_common.fengkong import Fengkong
        if Fengkong.is_ip_limited(clientip, clientId, chargetype):
            raise TyContext.FreetimeException(
                1, '对不起，您已超出支付限制，请联系客服4008-098-000')

        paycodes = TyContext.Configure.get_global_item_json('paycodes',
                                                            clientid=clientId)
        try:
            pdata = paycodes[chargetype]['paydata']
        except Exception as e:
            TyContext.ftlog.error('paycodes', paycodes, 'config error for',
                                  clientId, 'buttonId', buttonId)
            raise
        for data in pdata:
            if data['prodid'] == buttonId:
                break
        else:
            raise Exception('product %s not found in paycodes(%s) config'
                            % (buttonId, clientId))
        cdata = copy.deepcopy(data)
        del cdata['prodid']
        chargeinfo['chargeData'] = cdata

    @classmethod
    def get_charge_data_func(cls, chargeType):
        ''' returns the charge_data func of chargeType thirdpay.

        The charge_data function prototype:
            def charge_data(cls, chargeinfo)
            @param chargeinfo: the chargeinfo context
            the func should set either chargeType/chargeData or chargeCategories
            in chargeinfo
        '''
        try:
            _ = cls._charge_data_funcs
        except AttributeError as e:
            cls._charge_data_funcs = {}
            TyContext.ftlog.debug('get_charge_data_func init _charge_data_funcs', cls._charge_data_funcs)
        try:
            return cls._get_thirdpay_func(cls._charge_data_funcs, chargeType,
                                          'charge_data')
        except Exception as e:
            TyContext.ftlog.error('get_charge_data_func exception', e)
            return cls._default_charge_data_func

    @classmethod
    def _default_support_this_func(cls, paytype, clientid, buttonid):
        paycodes = TyContext.Configure.get_global_item_json('paycodes',
                                                            clientid=clientid)
        if not paycodes:
            TyContext.ftlog.debug('clientid', clientid, 'paycodes not configured,'
                                                        '_default_support_this_func return True')
            return True

        paytype = paytype.split('_')[0]
        try:
            app = paycodes[paytype]
        except KeyError as e:
            TyContext.ftlog.debug(
                '_default_support_this_func return True for paytype', paytype,
                'clientid', clientid, 'paycodes', paycodes)
            return True

        try:
            pdata = app['paydata']
            for data in pdata:
                if data['prodid'] == buttonid:
                    break
            else:
                raise Exception('product %s not found in paytype %s'
                                % (buttonid, paytype))
        except Exception as e:
            TyContext.ftlog.error(
                '_default_support_this_func clientid', clientid,
                'do not support this in paycodes config', paycodes,
                'buttonid', buttonid, 'exception:', e)
            return False

        TyContext.ftlog.debug('clientid', clientid, 'support_this True:',
                              'buttonid', buttonid, 'paytype', paytype)
        return True

    @classmethod
    def get_support_this_func(cls, chargeType):
        ''' return the support_this func of chargeType thirdpay.

        The support_this function prototype:
            def support_this(cls, paytype, clientid, buttonid)
            @param paytype: paytype (string)
            @param clientid: clientid (string)
            @param buttonid: buttonid (string)
            @return: whether the clientid's paytype support the buttonid (boolean)
        '''
        try:
            _ = cls._support_this_funcs
        except AttributeError as e:
            cls._support_this_funcs = {}
            TyContext.ftlog.debug('get_support_this_func init _support_this_funcs', cls._support_this_funcs)
        try:
            return cls._get_thirdpay_func(cls._support_this_funcs, chargeType,
                                          'support_this')
        except AttributeError as e:
            TyContext.ftlog.error('get_support_this_func exception', e)
            return cls._default_support_this_func
