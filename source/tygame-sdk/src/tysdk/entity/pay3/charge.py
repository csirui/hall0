# -*- coding=utf-8 -*-

import copy
import json

import datetime

from charge_conf import TuyouPayChargeConf
from constants import PayConst
from diamondlist import TuyouPayDiamondList
from productlist import TuyouPayProductList
from tyframework.context import TyContext
from tysdk.entity.duandai.riskcontrol import RiskControl
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay4.strategy.ios_appstore_strategy import TuYooPayIOSAppStoreStrategy
from tysdk.entity.pay4.strategy.ios_weixin_strategy import TuYooIOSPayWeixinStrategy
from tysdk.entity.pay_common.orderlog import Order


class TuyouPayCharge(object):
    _charg_data_funs = {}

    @classmethod
    def charge(cls, mi):

        TyContext.ftlog.info(cls.__name__, 'charge mi', mi)

        userId = mi.getParamInt('userId')
        authorCode = mi.getParamStr('authorCode')
        appId = mi.getParamInt('appId')
        clientId = mi.getParamStr('clientId')
        appInfo = mi.getParamStr('appInfo')
        diamondId = mi.getParamStr('diamondId')
        diamondName = mi.getParamStr('diamondName')
        diamondCount = mi.getParamInt('diamondCount')
        diamondPrice = mi.getParamInt('diamondPrice', -1)
        packageName = mi.getParamStr('packageName', '')
        channelName = mi.getParamStr('channelName', '')
        # 为支持0.1元商品加入
        if diamondPrice == -1:
            diamondPrice = mi.getParamFloat('diamondPrice')
        clientPayType = mi.getParamStr('payType')
        # example "payInfo": {"appid": {"ydmm": "300008410694"}}
        payInfo = mi.getParamStr('payInfo')
        if payInfo:
            payInfo = TyContext.strutil.loads(payInfo, decodeutf8=True)

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('charge')

        # 取得道具的配置PRICE
        appDiamondPrice = -1
        appDiamonds = TuyouPayDiamondList.diamondlist2(appId, clientId)
        for x in xrange(len(appDiamonds)):
            diamond = appDiamonds[x]
            if diamondId == diamond['id']:
                appDiamondPrice = diamond['price']
                appDiamondsPerUnit = int(diamond['count'])
                break
        # 单机商城的商品效验
        danji_products = TyContext.Configure.get_global_item_json('danji_products',
                                                                  ['TY9999R00020DJ', 'TY9999R00021DJ'])
        if diamondId in danji_products:
            appDiamondPrice = 2
            appDiamondsPerUnit = 20
        if diamondPrice <= 0 or appDiamondPrice <= 0 or diamondPrice != appDiamondPrice:
            TyContext.ftlog.error(cls.__name__, 'charge diamond info error diamondId=', diamondId,
                                  'diamondPrice=', diamondPrice, 'appDiamondPrice=', appDiamondPrice)
            mo.setError(2, '钻石信息错误，请重新充值')
            return mo
        # 钻石购买限购判断
        if RiskControl(userId).is_diamond_limited(diamondId):
            diamonds_limit_config = TyContext.Configure.get_global_item_json('diamonds_limit_config', {})
            errorInfo = diamonds_limit_config[diamondId].get('des', '您的购买次数已经达到上限')
            mo.setError(2, errorInfo)
            return mo

        cls.__charge_begin__(appId, appInfo, clientId, userId, authorCode,
                             diamondId, diamondPrice, diamondCount, diamondName,
                             appDiamondsPerUnit, mo, None, clientPayType, payInfo, packageName=packageName,
                             channelName=channelName)
        return mo

    @classmethod
    def __charge_begin__(cls, appId, appInfo, clientId, userId, authorCode,
                         diamondId, diamondPrice, diamondCount, diamondName,
                         diamondsPerUnit, mo, consumeinfo, clientPayType, payInfo, **kwds):
        TyContext.ftlog.info(
            cls.__name__, '__charge_begin__', appId, appInfo, clientId, userId,
            authorCode, diamondId, diamondPrice, diamondCount, diamondName,
            diamondsPerUnit, mo, consumeinfo, clientPayType, payInfo)

        if TyContext.Configure.get_global_item_json('store_payment',
                                                    clientid=clientId):
            cls._charge_begin_w_new_categories(
                appId, appInfo, clientId, userId, authorCode, diamondId,
                diamondPrice, diamondCount, diamondName, diamondsPerUnit,
                mo, consumeinfo, clientPayType, payInfo, **kwds)
            return mo
        # IOS客户端如果是非越狱版本，consume和charge时都需传payType=tuyooios
        # 参数；如果是越狱版本则不传此参数，跟android走相同的逻辑（使用相同
        # 的商品配置）。
        if clientPayType == 'tuyooios' \
                or clientId not in TyContext.Configure.get_global_item_json(
                    'clientids_using_charge_categories', {}):
            cls._charge_begin_w_paytype(
                appId, appInfo, clientId, userId, authorCode, diamondId,
                diamondPrice, diamondCount, diamondName, diamondsPerUnit,
                mo, consumeinfo, clientPayType, payInfo, **kwds)
        else:
            cls._charge_begin_w_categories(
                appId, appInfo, clientId, userId, authorCode, diamondId,
                diamondPrice, diamondCount, diamondName, diamondsPerUnit,
                mo, consumeinfo, payInfo, **kwds)

    @classmethod
    def _charge_begin_w_new_categories(cls, appId, appInfo, clientId, userId,
                                       authorCode, diamondId, diamondPrice, diamondCount, diamondName,
                                       diamondsPerUnit, mo, consumeinfo, clientPayType, payInfo, **kwds):
        mo.setCmd('charge')
        # 取得钻石的购买信息
        if diamondCount <= 0:
            diamondCount = 1
        else:
            diamondCount = int(diamondCount)
        if diamondCount != 1:
            TyContext.ftlog.error(cls.__name__, 'charge diamond count error')
            mo.setError(2, '钻石信息错误，请重新充值')
            return

        chargeTotal = diamondPrice * diamondCount

        # 建立充值事物
        diamondOrderId = TyContext.ServerControl.makeChargeOrderIdV3(userId, appId, clientId)

        if consumeinfo and consumeinfo['mustcharge']:
            buttonId = consumeinfo['prodId']
            buttonName = consumeinfo['prodName']
        else:
            buttonId = diamondId
            buttonName = diamondName

        payconfig = TyContext.Configure.get_global_item_json('store_payment', clientid=clientId)
        try:
            cats = payconfig['payment']['default_category']
            for cat in cats:
                if cat['id'] == buttonId:
                    break
            else:
                TyContext.ftlog.error(cls.__name__, 'buttonId', buttonId,
                                      'missing in store_payment', payconfig,
                                      'for clientid', clientId)
                mo.setError(2, '商品(%s)未配置，请检查store_payment配置' % buttonId)
                return
        except Exception as e:
            TyContext.ftlog.error(cls.__name__, 'exception', e,
                                  'store_payment', payconfig,
                                  'not configed for clientid', clientId,
                                  'or pay config error')
            mo.setError(2, '商品配置信息错误，请稍后重试')
            return

        TyContext.ftlog.debug(cls.__name__, 'buttonId', buttonId, 'default_category config', cat)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        chargeinfo = {'uid': userId,
                      'appId': appId,
                      'appInfo': appInfo,
                      'clientId': clientId,
                      'diamondId': diamondId,
                      'diamondPrice': diamondPrice,
                      'diamondCount': diamondCount,
                      'diamondsPerUnit': diamondsPerUnit,
                      'diamondName': diamondName,
                      'chargeTotal': chargeTotal,
                      'platformOrderId': diamondOrderId,
                      'phoneType': TyContext.UserSession.get_session_phone_type(userId),
                      'payInfo': payInfo,
                      'buttonId': buttonId,
                      'buttonName': buttonName,
                      'packageName': kwds.get('packageName', ''),
                      'channelName': kwds.get('channelName', ''),
                      }
        if consumeinfo:
            chargeinfo['prodId'] = consumeinfo['prodId']
        # list more pay type if clientPayType is more_categories
        if clientPayType == 'more_categories':
            category = payconfig['payment']['more_categories'].lower()
        elif cat['category'] == 'CAT_THIRDPAY' and cat['paytype'] == 'fake':
            ios_control = TyContext.Configure.get_global_item_json('ios_weinxin_pay_control', {})
            strategy_name = cat.get('strategy', 'default_strategy')
            strategy = TuYooIOSPayWeixinStrategy(strategy_name)
            test_flag = strategy(appId=appId, userId=userId)
            if not test_flag:
                category = 'tuyooios'
            elif clientPayType:
                category = clientPayType
            else:
                category = cat['paytype']
            strategy = TuYooPayIOSAppStoreStrategy()
            if strategy(appId=appId, userId=userId, diamondId=diamondId):
                category = 'wxpay'
        elif cat['category'] == 'CAT_DUANDAI':
            category = 'cat_duandai'
        elif cat['category'] == 'CAT_THIRDPAY':
            category = cat['paytype']
        else:
            category = payconfig['payment']['more_categories'].lower()
        lastChargeCategory = TyContext.RedisUser.execute(
            userId, 'HGET', 'user:' + str(userId), 'lastChargeCategory')
        if not lastChargeCategory and cat['category'] != 'CAT_MORE':
            lastChargeCategory = cat['category']

        chargeinfo['chargeType'] = category
        # ios充值限制
        if category == 'tuyooios' and int(appId) < 10000:
            from tysdk.entity.paythird.payios import TuYouPayIos
            check_ret, check_msg = TuYouPayIos._check_user_ios_pay(userId)
            TyContext.ftlog.info('check_ret', check_ret, 'check_msg', check_msg)
            if check_ret:
                mo.setError(2, check_msg)
                return mo
            # 判断5分钟内的充值
            if TuYouPayIos._check_ios_pay_5mins(userId) and TuYouPayIos._check_user_gametime(userId):
                mo.setError(2, '单日充值达到上限')
                return mo

        try:
            cls._charge_data_new(chargeinfo)
        except TyContext.FreetimeException as e:
            TyContext.ftlog.error('_charge_begin_w_new_categories exception', e)
            mo.setError(e.errorCode, e.message)
            return

        TyContext.ftlog.info('_charge_begin_w_new_categories transaction',
                             chargeinfo, consumeinfo)

        chargeinfo_dump = json.dumps(chargeinfo)
        datas = ['state', PayConst.CHARGE_STATE_BEGIN,
                 'charge', chargeinfo_dump,
                 'createTime', timestamp]
        if consumeinfo:
            datas.append('consume')
            datas.append(json.dumps(consumeinfo))

        TyContext.RedisPayData.execute('HMSET', 'sdk.charge:' + diamondOrderId, *datas)
        # 返回数据
        mo.setResult('userId', userId)
        mo.setResult('appId', appId)
        mo.setResult('appInfo', appInfo)
        mo.setResult('clientId', clientId)
        # 兼容googleplay
        '''
        try:
            products_low_all = TyContext.Configure.get_global_item_json('products_low_all', ['googleiab'])
            if chargeinfo['chargeType'] == 'googleiab' or chargeinfo['chargeType'] in products_low_all:
                mo.setResult('diamondId', diamondId.lower())
            else:
                mo.setResult('diamondId', diamondId)
        except:
            pass
        TyContext.ftlog.info(products_low_all,chargeinfo['chargeType'], diamondId)
        '''
        mo.setResult('diamondId', diamondId)
        mo.setResult('diamondPrice', diamondPrice)
        mo.setResult('diamondCount', diamondCount)
        mo.setResult('diamondsPerUnit', diamondsPerUnit)
        mo.setResult('diamondName', diamondName)
        # 客户端SDK根据消息里是带chargeType还是chargeCategories来区分是老版支付
        # 界面还是新版支付界面
        try:
            mo.setResult('chargeData', chargeinfo['chargeData'])
            mo.setResult('chargeType', chargeinfo['chargeType'])
        except:
            categories = chargeinfo.get('chargeCategories', [])
            isenable = TyContext.Configure.get_global_item_int('last.charge.on', 1)
            if isenable:
                # temp workaround for client sdk bug: CAT_PHONECHARGE_CARD
                if lastChargeCategory and lastChargeCategory != 'CAT_PHONECHARGE_CARD':
                    for category in categories:
                        if lastChargeCategory == category['category']:
                            mo.setResult('lastChargeCategory', lastChargeCategory)
                            break
                else:
                    mo.setResult('lastChargeCategory', '')
            else:
                mo.setResult('lastChargeCategory', '')
            mo.setResult('chargeCategories', categories)
        pay_appid = Order.get_pay_appid(chargeinfo.get('chargeType', 'na'),
                                        payInfo, clientId)
        shortId = chargeinfo.get('shortDiamondOrderId', 'na')
        Order.log(diamondOrderId, Order.CREATE, userId, appId, clientId,
                  diamondid=diamondId, prodid=consumeinfo['prodId'] if consumeinfo else 'na',
                  prod_price=consumeinfo['prodPrice'] if consumeinfo else 'na',
                  paytype=chargeinfo.get('chargeType', 'na'),
                  charge_price=chargeTotal, shortId=shortId, pay_appid=pay_appid)
        mo.setResult('platformOrderId', chargeinfo.get('shortDiamondOrderId',
                                                       diamondOrderId))

        payConfig = TyContext.Configure.get_global_item_json('store_payment', clientid=clientId)
        failreturnconfig = TyContext.Configure.get_global_item_json('payfail_returnconfig', {})
        if payConfig and 'payment' in payConfig and 'more_categories' in payConfig['payment']:
            if payConfig['payment']['more_categories'] in failreturnconfig:
                failreturnconfig = TyContext.Configure.get_global_item_json('payfail_returnconfig', {})
                payMoreType = failreturnconfig[payConfig['payment']['more_categories']]
                paytemplateconfig = TyContext.Configure.get_global_item_json(payMoreType)
                mo.setResult('morePayType', paytemplateconfig)
                #    else:
                #        mo.setResult('morePayType', payConfig['payment']['more_categories'])
                # else:
                #    mo.setResult('morePayType', '')

    @classmethod
    def _charge_begin_w_categories(cls, appId, appInfo, clientId, userId,
                                   authorCode, diamondId, diamondPrice, diamondCount, diamondName,
                                   diamondsPerUnit, mo, consumeinfo, payInfo, **kwds):
        mo.setCmd('charge')
        # 取得钻石的购买信息
        if diamondCount <= 0:
            diamondCount = 1
        else:
            diamondCount = int(diamondCount)
        if diamondCount != 1:
            TyContext.ftlog.error(cls.__name__, 'charge diamond count error')
            mo.setError(2, '钻石信息错误，请重新充值')
            return

        chargeTotal = diamondPrice * diamondCount

        # 建立充值事物
        diamondOrderId = TyContext.ServerControl.makeChargeOrderIdV3(userId, appId, clientId)
        shortDiamondOrderId = diamondOrderId

        product = None
        if consumeinfo:
            prodId = consumeinfo['prodId']
            product = TuyouPayProductList.product(appId, clientId, prodId)
        if product:
            buttonId = prodId
            buttonName = consumeinfo['prodName']
        else:
            product = TuyouPayProductList.product(appId, clientId, diamondId)
            buttonId = diamondId
            buttonName = diamondName
        TyContext.ftlog.debug(cls.__name__, 'product', product)
        if product is None or 'charge_categories' not in product:
            TyContext.ftlog.error(cls.__name__, 'product not exist or '
                                                'charge_categories absent in product', product)
            mo.setError(2, '商品配置信息错误，请稍后重试')
            return

        chargeCategories = copy.deepcopy(product['charge_categories'])
        phoneType = TyContext.UserSession.get_session_phone_type(userId)
        is_shortcut = cls._process_shortcut_category(userId, clientId, chargeCategories)
        TyContext.ftlog.debug(cls.__name__, 'after _process_shortcut_category is_shortcut',
                              is_shortcut, 'chargeCategories', chargeCategories)
        chargeinfo = {'uid': userId,
                      'appId': appId,
                      'appInfo': appInfo,
                      'clientId': clientId,
                      'diamondId': diamondId,
                      'diamondPrice': diamondPrice,
                      'diamondCount': diamondCount,
                      'diamondsPerUnit': diamondsPerUnit,
                      'diamondName': diamondName,
                      'chargeTotal': chargeTotal,
                      'platformOrderId': diamondOrderId,
                      'phoneType': phoneType,
                      'payInfo': payInfo,
                      'buttonId': buttonId,
                      'buttonName': buttonName,
                      'packageName': kwds.get('packageName', ''),
                      'channelName': kwds.get('channelName', ''),
                      }
        if consumeinfo:
            chargeinfo['prodId'] = prodId

        has_duandai, needShort = cls._process_duandai_category(
            appId, userId, clientId, phoneType, buttonId, chargeCategories, chargeinfo)
        if has_duandai:
            if needShort:
                shortDiamondOrderId = ShortOrderIdMap.get_short_order_id(diamondOrderId)
        elif is_shortcut:
            chargeCategories = copy.deepcopy(product['charge_categories'])
            cls._remove_duandai_category(chargeCategories)
            is_shortcut = 0
        TyContext.ftlog.debug(cls.__name__, 'after _process_duandai_category is_shortcut',
                              is_shortcut, 'chargeCategories', chargeCategories)

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if len(shortDiamondOrderId) < len(diamondOrderId):
            chargeinfo['shortDiamondOrderId'] = shortDiamondOrderId
        if is_shortcut:
            chargeinfo['chargeType'] = chargeCategories[0]['paytype']
            chargeinfo['chargeData'] = chargeCategories[0]['payData']
        else:
            chargeinfo['chargeCategories'] = chargeCategories
        chargeinfo_dump = json.dumps(chargeinfo)

        TyContext.ftlog.info('_charge_begin_w_categories transaction',
                             chargeinfo_dump, consumeinfo)
        datas = ['state', PayConst.CHARGE_STATE_BEGIN,
                 'charge', chargeinfo_dump,
                 'createTime', timestamp]
        if consumeinfo:
            datas.append('consume')
            datas.append(json.dumps(consumeinfo))

        TyContext.RedisPayData.execute('HMSET', 'sdk.charge:' + diamondOrderId, *datas)
        # 返回数据
        mo.setResult('userId', userId)
        mo.setResult('appId', appId)
        mo.setResult('appInfo', appInfo)
        mo.setResult('clientId', clientId)
        mo.setResult('diamondId', diamondId)
        mo.setResult('diamondPrice', diamondPrice)
        mo.setResult('diamondCount', diamondCount)
        mo.setResult('diamondsPerUnit', diamondsPerUnit)
        mo.setResult('diamondName', diamondName)
        # 客户端SDK根据消息里是带chargeType还是chargeCategories来区分是老版支付
        # 界面还是新版支付界面
        if is_shortcut:
            mo.setResult('chargeType', chargeinfo['chargeType'])
            mo.setResult('chargeData', chargeinfo['chargeData'])
        else:
            mo.setResult('chargeCategories', chargeCategories)
        try:
            third_prodid = chargeinfo['chargeData']['paydata']['msgOrderCode']
        except:
            third_prodid = 'na'

        pay_appid = Order.get_pay_appid(chargeinfo.get('chargeType', 'na'), payInfo, clientId)
        shortId = shortDiamondOrderId if len(shortDiamondOrderId) < len(diamondOrderId) else 'na'
        Order.log(diamondOrderId, Order.CREATE, userId, appId, clientId,
                  diamondid=diamondId, prodid=prodId if consumeinfo else 'na',
                  prod_price=consumeinfo['prodPrice'] if consumeinfo else 'na',
                  paytype=chargeinfo.get('chargeType', 'na'),
                  charge_price=chargeTotal, shortId=shortId,
                  third_prodid=third_prodid, pay_appid=pay_appid)
        mo.setResult('platformOrderId', shortDiamondOrderId)

    @classmethod
    def _process_shortcut_category(cls, userId, clientId, chargeCategories):
        ''' return true if shortcut exists and remove all other categories '''

        def has_shortcut_flg(cat):
            return 'is_shortcut' in cat

        def is_duandai_cat(cat):
            return cat['category'] == 'CAT_DUANDAI'

        duandai_rule_id, is_tishen = TyContext.Configure.get_global_item_json(
            'clientids_using_charge_categories')[clientId]
        if duandai_rule_id == 'duandai_rule_FORBID':
            cls._remove_duandai_category(chargeCategories)
            return False

        if is_tishen:
            condition = is_duandai_cat
        else:
            condition = has_shortcut_flg
            duandai_rule = TyContext.Configure.get_global_item_json(duandai_rule_id)
            if duandai_rule['new_payer_shortcut'] == 1:
                is_newpayer = 1
                paycnt = TyContext.RedisUser.execute(userId, 'HGET',
                                                     'user:' + str(userId), 'payCount')
                if paycnt is not None and paycnt > 0:
                    is_newpayer = 0
                if is_newpayer:
                    condition = is_duandai_cat

        idx_shortcut = -1
        total_len = len(chargeCategories)
        i = 0
        while i < total_len:
            if idx_shortcut >= 0:
                del chargeCategories[i]
                total_len -= 1
                continue
            cat = chargeCategories[i]
            if condition(cat):
                idx_shortcut = i
            i += 1
        for _ in xrange(idx_shortcut):
            del chargeCategories[0]
        return idx_shortcut >= 0

    @classmethod
    def _process_duandai_category(cls, appId, userId, clientId, phoneType,
                                  buttonId, chargeCategories, chargeinfo):
        ''' return tuple of (has_duandai, whether or not need short orderid) '''
        duandai_cat = None
        for i in xrange(len(chargeCategories)):
            cat = chargeCategories[i]
            if cat['category'] == 'CAT_DUANDAI':
                duandai_cat = cat
                break
        if duandai_cat is None:
            TyContext.ftlog.debug(cls.__name__, '_process_duandai_category no duandai: not configed')
            return False, False
        if phoneType == TyContext.UserSession.PHONETYPE_OTHER:
            del chargeCategories[i]
            TyContext.ftlog.debug(cls.__name__, '_process_duandai_category no duandai: phonetype is other')
            return False, False
        if TyContext.SmsPayCheck.is_sms_pay_limited(userId):
            del chargeCategories[i]
            TyContext.ftlog.debug(cls.__name__, '_process_duandai_category no duandai: sms pay limit reached')
            return False, False
        paytype, payData = cls._get_duandai_paydata(appId, buttonId, clientId,
                                                    phoneType, chargeinfo)
        if payData is None:
            del chargeCategories[i]
            TyContext.ftlog.debug(cls.__name__, '_process_duandai_category no duandai: paydata is none')
            return False, False
        if TyContext.SmsPayCheck.is_sms_pay_speed_limited(userId, paytype):
            del chargeCategories[i]
            TyContext.ftlog.debug(cls.__name__, '_process_duandai_category no duandai: sms pay speed limit reached')
            return False, False
        clientip = TyContext.UserSession.get_session_client_ip(userId)
        from tysdk.entity.pay_common.fengkong import Fengkong
        if Fengkong.is_ip_limited(clientip, clientId, paytype):
            return False, False
        duandai_cat['paytype'] = paytype
        duandai_cat['payData'] = payData
        if payData.get('need_short_order_id', 0) == 1:
            return True, True
        return True, False

    @classmethod
    def _remove_duandai_category(cls, charge_categories):
        for i in xrange(len(charge_categories)):
            cat = charge_categories[i]
            if cat['category'] == 'CAT_DUANDAI':
                del charge_categories[i]
                break

    @classmethod
    def _get_duandai_paydata(cls, appId, buttonId, clientId, phonetype, chargeinfo):
        userId = chargeinfo['uid']
        zipcode, _ = TyContext.UserSession.get_session_zipcode(userId)
        zipcode = str(zipcode)
        paytype, payData = TyContext.PayType.get_paydata_by_clientid(
            appId, clientId, buttonId, phonetype, zipcode)
        TyContext.ftlog.debug(cls.__name__, "_get_duandai_paydata appId, clientId,"
                                            " buttonId, phonetype, zipcode, chargeinfo", appId, clientId,
                              buttonId, phonetype, zipcode, chargeinfo)
        try:
            chargeinfo['nohint'] = payData['nohint']
        except:
            pass

        paytype = cls._ydmm_ydjd_paytype_switch(userId, clientId, paytype)

        noncfg_paytypes = TyContext.Configure.get_global_item_json("nonconfigured_duandai_paytypes")
        if paytype in noncfg_paytypes:
            chargeinfo['chargeType'] = paytype
            cls._charge_data(chargeinfo)
            if 'chargeData' not in chargeinfo or not chargeinfo['chargeData']:
                TyContext.ftlog.error('_get_duandai_paydata return None for paytype=', paytype,
                                      'appId', appId, 'clientId', clientId,
                                      'buttonId', buttonId, 'phonetype', phonetype,
                                      'zipcode', zipcode, 'chargeinfo', chargeinfo)
                del chargeinfo['chargeType']
                return None, None
            payData = chargeinfo['chargeData']
        if payData is None:
            TyContext.ftlog.error('_get_duandai_paydata return None: appId', appId,
                                  'clientId', clientId, 'buttonId', buttonId,
                                  'phonetype', phonetype, 'zipcode', zipcode,
                                  'chargeinfo', chargeinfo)
            return None, None

        payData['issms'] = 1
        # 配置短代充值失败后二次挽留的支付类型
        failed_paytype = TyContext.Configure.get_global_item_str('msg.failed.paytype')
        payData['failed_paytype'] = failed_paytype

        TyContext.ftlog.debug(cls.__name__, '_get_duandai_paydata paytype:', paytype,
                              'paydata:', payData)
        return paytype, payData

    _ydmm_ydjd_dist = [0, 0]

    @classmethod
    def _ydmm_ydjd_paytype_switch(cls, userId, clientId, paytype):
        ''' return boolean value indicating whether switched to ydjd '''

        if paytype != 'ydmm':
            return paytype

        dist = TuyouPayCharge._ydmm_ydjd_dist
        try:
            client_share = TyContext.Configure.get_global_item_json(
                'ydjd_percentage_share_with_ydmm', {})
            share = client_share[clientId]
            if userId % 100 < share:
                dist[1] += 1
                real = 100.0 * dist[1] / sum(dist)
                TyContext.ftlog.info('_ydmm_ydjd_paytype_switch\'ed to ydjd '
                                     'userId', userId, '_ydmm_ydjd_dist_v3', dist,
                                     'target share %.1f%%' % share,
                                     'real share %.1f%%' % real)
                return 'ydjd'
            dist[0] += 1
        except:
            pass
        return paytype

    @classmethod
    def _is_sms_pay_speed_limited(cls, userId, paytype, clientId):
        if TyContext.SmsPayCheck.is_sms_pay_speed_limited(userId, paytype):
            from tysdk.entity.paythird.helper import get_default_paytype
            return True, get_default_paytype(clientId)
        return False, None

    @classmethod
    def _charge_begin_w_paytype(cls, appId, appInfo, clientId, userId, authorCode,
                                diamondId, diamondPrice, diamondCount, diamondName,
                                diamondsPerUnit, mo, consumeinfo, clientPayType, payInfo, **kwds):
        mo.setCmd('charge')
        # 取得钻石的购买信息
        if diamondCount <= 0:
            diamondCount = 1
        else:
            diamondCount = int(diamondCount)
        if diamondCount != 1:
            TyContext.ftlog.error(cls.__name__, 'charge diamond count error')
            mo.setError(2, '钻石信息错误，请重新充值')
            return mo

        diamondPrice = int(diamondPrice)
        chargeTotal = int(diamondPrice * diamondCount)

        # ios支付限制
        TyContext.ftlog.info('clientPayType', clientPayType, 'userId', userId)
        if clientPayType == 'tuyooios':
            from tysdk.entity.paythird.payios import TuYouPayIos
            check_ret, check_msg = TuYouPayIos._check_user_ios_pay(userId)
            TyContext.ftlog.info('check_ret', check_ret, 'check_msg', check_msg)
            if check_ret:
                mo.setError(2, check_msg)
                return mo
            # 判断5分钟内的充值
            if TuYouPayIos._check_ios_pay_5mins(userId) and TuYouPayIos._check_user_gametime(userId):
                mo.setError(2, '单日充值达到上限')
                return mo

        # 建立充值事物
        diamondOrderId = TyContext.ServerControl.makeChargeOrderIdV3(userId, appId, clientId)

        # 取得当前的客户端可使用的支付类型
        if consumeinfo and consumeinfo['mustcharge']:
            buttonId = consumeinfo['prodId']
            buttonName = consumeinfo['prodName']
        else:
            buttonId = diamondId
            buttonName = diamondName
        if clientPayType == 'tuyooios':
            chargeType = 'tuyooios'
            phoneType = ''
            zipcode = '1'
        else:
            phoneType = TyContext.UserSession.get_session_phone_type(userId)
            phoneType = TyContext.UserSession.get_phone_type_name(phoneType)
            zipcode, _ = TyContext.UserSession.get_session_zipcode(userId)
            zipcode = str(zipcode)
            chargeType = TyContext.PayType.get_paytype_by_user(appId, userId, buttonId, clientId)
            chargeType = cls._ydmm_ydjd_paytype_switch(userId, clientId, chargeType)
            limited, new_chargetype = cls._is_sms_pay_speed_limited(userId, chargeType, clientId)
            if limited:
                chargeType = new_chargetype

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        chargeinfo = {'uid': userId,
                      'appId': appId,
                      'appInfo': appInfo,
                      'clientId': clientId,
                      'diamondId': diamondId,
                      'diamondPrice': diamondPrice,
                      'diamondCount': diamondCount,
                      'diamondsPerUnit': diamondsPerUnit,
                      'diamondName': diamondName,
                      'chargeTotal': chargeTotal,
                      'chargeType': chargeType,
                      'platformOrderId': diamondOrderId,
                      'phoneType': phoneType,
                      'zipcode': zipcode,
                      'payInfo': payInfo,
                      'buttonId': buttonId,
                      'buttonName': buttonName,
                      'packageName': kwds.get('packageName', ''),
                      'channelName': kwds.get('channelName', ''),
                      }
        if consumeinfo:
            chargeinfo['prodId'] = consumeinfo['prodId']

        # 当前支付类型的特殊数据初始化
        cls._charge_data(chargeinfo)

        clientip = TyContext.UserSession.get_session_client_ip(userId)
        from tysdk.entity.pay_common.fengkong import Fengkong
        if Fengkong.is_ip_limited(clientip, clientId, chargeinfo['chargeType']):
            mo.setError(1, '对不起，您已超出支付限制，请联系客服4008-098-000')
            return

        TyContext.ftlog.info('_charge_begin_w_paytype transaction', diamondOrderId,
                             'chargeinfo', chargeinfo, 'consumeinfo', consumeinfo)
        datas = ['state', PayConst.CHARGE_STATE_BEGIN,
                 'charge', json.dumps(chargeinfo),
                 'createTime', timestamp]
        if consumeinfo:
            datas.append('consume')
            datas.append(json.dumps(consumeinfo))

        TyContext.RedisPayData.execute('HMSET', 'sdk.charge:' + diamondOrderId, *datas)
        # 返回数据
        mo.setResult('userId', userId)
        mo.setResult('appId', appId)
        mo.setResult('appInfo', appInfo)
        mo.setResult('clientId', clientId)
        mo.setResult('diamondId', diamondId)
        mo.setResult('diamondPrice', diamondPrice)
        mo.setResult('diamondCount', diamondCount)
        mo.setResult('diamondsPerUnit', diamondsPerUnit)
        mo.setResult('diamondName', diamondName)
        mo.setResult('chargeTotal', chargeTotal)
        mo.setResult('chargeType', chargeinfo['chargeType'])
        mo.setResult('chargeData', chargeinfo.get('chargeData', {}))
        shortOrderId = chargeinfo.get('shortDiamondOrderId')
        mo.setResult('platformOrderId', shortOrderId if shortOrderId else diamondOrderId)

        try:
            third_prodid = chargeinfo['chargeData']['paydata']['msgOrderCode']
        except:
            third_prodid = 'na'

        pay_appid = Order.get_pay_appid(chargeType, payInfo, clientId)
        Order.log(diamondOrderId, Order.CREATE, userId, appId, clientId,
                  diamondid=diamondId,
                  prodid=consumeinfo['prodId'] if consumeinfo else 'na',
                  prod_price=consumeinfo['prodPrice'] if consumeinfo else 'na',
                  paytype=chargeinfo['chargeType'],
                  charge_price=chargeTotal,
                  third_prodid=third_prodid, pay_appid=pay_appid,
                  shortId=shortOrderId if shortOrderId else 'na')

    @classmethod
    def _charge_data(cls, chargeinfo):
        duandai_paytypes = TyContext.Configure.get_global_item_json("all_duandai_paytypes")
        noncfg_paytypes = TyContext.Configure.get_global_item_json("nonconfigured_duandai_paytypes")
        chargeType = chargeinfo['chargeType']
        cfun, cdata = None, {}
        if chargeType in duandai_paytypes and chargeType not in noncfg_paytypes:
            phoneType = TyContext.UserSession.get_phone_type_code(chargeinfo['phoneType'])
            _, cdata = cls._get_duandai_paydata(
                chargeinfo['appId'], chargeinfo['buttonId'], chargeinfo['clientId'],
                phoneType, chargeinfo)
            chargeinfo['chargeData'] = cdata
        else:
            if chargeType in cls._charg_data_funs:
                cfun = cls._charg_data_funs[chargeType]
            else:
                if chargeType in TuyouPayChargeConf.CHARGE_DATA:
                    cpath = TuyouPayChargeConf.CHARGE_DATA[chargeType]
                    tks = cpath.split('.')
                    mpackage = '.'.join(tks[0:-1])
                    clsName = tks[-1]
                    clazz = None
                    exec 'from %s import %s as clazz' % (mpackage, clsName)
                    cfun = getattr(clazz, 'charge_data')
                    cls._charg_data_funs[chargeType] = cfun
                else:
                    cls._charg_data_funs[chargeType] = None
            if cfun:
                try:
                    cfun(chargeinfo)
                    cdata = chargeinfo['chargeData']
                except:
                    pass

        TyContext.ftlog.debug('_charge_data', 'chargeinfo', chargeinfo,
                              'cfun', cfun, 'cdata', cdata)
        if not cdata:
            return
        if cdata.get('need_short_order_id', 0) == 1:
            chargeinfo['shortDiamondOrderId'] = \
                ShortOrderIdMap.get_short_order_id(chargeinfo['platformOrderId'])

    @classmethod
    def _charge_data_new(cls, chargeinfo):
        ''' delegate to charge_data func of thirdpay '''

        cfun = TuyouPayChargeConf.get_charge_data_func(chargeinfo['chargeType'])
        try:
            TyContext.ftlog.debug('_charge_data_new before: chargeinfo', chargeinfo, 'cfun', cfun)
            cfun(chargeinfo)
            TyContext.ftlog.debug('_charge_data_new after: chargeinfo', chargeinfo, 'cfun', cfun)
        except TyContext.FreetimeException as e:
            raise
        except Exception as e:
            TyContext.ftlog.exception()
            return

        if 'chargeData' not in chargeinfo and 'chargeCategories' not in chargeinfo:
            raise Exception('neither chargeData nor chargeCategories in chargeinfo')

        try:
            if chargeinfo['chargeData'].get('need_short_order_id', 0):
                chargeinfo['shortDiamondOrderId'] = ShortOrderIdMap.get_short_order_id(
                    chargeinfo['platformOrderId'])
        except:
            pass
