# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import datetime
import json

from diamondlist import TuyouPayDiamondList
from tyframework.context import TyContext
from tysdk.entity.duandai.channels import Channels
from tysdk.entity.duandai.riskcontrol import RiskControl
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.pay_common.orderlog import Order
from tysdk.entity.paythird.helper import PayHelper
from tysdk.entity.report4.report_reyun import ReportReyun
from tysdk.entity.user4.universal_user import UniversalUser


def _check_price(platformOrderId, total_fee, state, rparam, errorInfo, chargeInfo, consumeInfo):
    try:
        charge_price = chargeInfo.get('chargeTotal', -1)
        if total_fee >= 0 and charge_price >= 0 and (total_fee < charge_price * 0.8 or total_fee >= charge_price + 100):
            TyContext.ftlog.info('CHECK_PROD_PRICE CB Error ! total_fee=', total_fee, 'charge_price=', charge_price,
                                 'inputs=', platformOrderId, total_fee, state, rparam, errorInfo,
                                 'chargeInfo=', chargeInfo, 'consumeInfo=', consumeInfo)
            return True
        TyContext.ftlog.info('CHECK_PROD_PRICE CB OK ! total_fee=', total_fee, 'charge_price=', charge_price,
                             'platformOrderId=', platformOrderId)
    except Exception, e:
        TyContext.ftlog.error(e)
    return False


class TuyouPayCallBack(object):
    @classmethod
    def callback(cls, platformOrderId, total_fee, state, rparam, errorInfo):
        TyContext.ftlog.info('****** callback platformOrderId=', platformOrderId, 'total_fee=', total_fee,
                             'state=', state, 'errorInfo=', errorInfo, 'rparam=', rparam)

        chargeKey = 'sdk.charge:' + platformOrderId
        oldState, chargeInfo, consumeInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'state', 'charge',
                                                                           'consume')
        if oldState == None or chargeInfo == None:
            TyContext.ftlog.error('platformOrderId not found !', platformOrderId)
            return True

        chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
        paytype = rparam.get('chargeType', chargeInfo.get('chargeType', 'na'))
        if state == PayConst.CHARGE_STATE_ERROR_CALLBACK:
            if oldState < PayConst.CHARGE_STATE_ERROR_REQUEST:
                # 第三方通知充值失败
                if errorInfo == None or len(errorInfo) == 0:
                    errorInfo = '充值失败，请关闭页面重试'
                cls.__change_callback_state__(chargeKey, state, errorInfo, None)
            else:
                TyContext.ftlog.info('callback platformOrderId=', platformOrderId, 'old state error, oldState=',
                                     oldState, 'newState=', state)

            Order.log(platformOrderId, Order.CALLBACK_FAIL, chargeInfo['uid'],
                      chargeInfo['appId'], chargeInfo['clientId'], info=errorInfo,
                      prodid=chargeInfo.get('prodId', 'na'),
                      diamondid=chargeInfo['diamondId'],
                      charge_price=chargeInfo.get('chargeTotal', 'na'),
                      succ_price=total_fee,
                      paytype=paytype,
                      sub_paytype=rparam.get('sub_paytype', 'na'),
                      third_prodid=rparam.get('third_prodid', 'na'),
                      third_orderid=rparam.get('third_orderid', 'na'),
                      third_provid=rparam.get('third_provid', 'na'),
                      third_userid=rparam.get('third_userid', 'na'),
                      pay_appid=rparam.get('pay_appid', 'na'),
                      )
            return True

        if state == PayConst.CHARGE_STATE_CALLBACK_OK:
            isDone = True
            if oldState < PayConst.CHARGE_STATE_CALLBACK_OK:
                if oldState < PayConst.CHARGE_STATE_CLIENT_PAY_DONE:
                    Order.log(platformOrderId, Order.CLIENT_FINISHED, chargeInfo['uid'],
                              chargeInfo['appId'], chargeInfo['clientId'], paytype=paytype,
                              prodid=chargeInfo.get('prodId', 'na'),
                              diamondid=chargeInfo['diamondId'],
                              charge_price=chargeInfo.get('chargeTotal', 'na'),
                              succ_price=total_fee
                              )
                isDone = False
            if oldState >= PayConst.CHARGE_STATE_ERROR_REQUEST:
                isDone = False
            if isDone:
                # XXX if external orderid is new, consider re-delivery the order?!
                Order.log(platformOrderId, Order.INTERNAL_ERR, chargeInfo['uid'],
                          chargeInfo['appId'], chargeInfo['clientId'],
                          paytype=paytype,
                          prodid=chargeInfo.get('prodId', 'na'),
                          diamondid=chargeInfo['diamondId'],
                          charge_price=chargeInfo['chargeTotal'],
                          succ_price=total_fee,
                          sub_paytype=rparam.get('sub_paytype', 'na'),
                          third_prodid=rparam.get('third_prodid', 'na'),
                          third_orderid=rparam.get('third_orderid', 'na'),
                          third_provid=rparam.get('third_provid', 'na'),
                          third_userid=rparam.get('third_userid', 'na'),
                          pay_appid=rparam.get('pay_appid', 'na'),
                          info='order state charged',
                          )
                TyContext.ftlog.info('callback platformOrderId=', platformOrderId,
                                     'old state is done, oldState=', oldState,
                                     'newState=', state)
                return True

            # save charge data
            UniversalUser().increase_user_charge_data(chargeInfo['uid'],
                                                      chargeInfo['appId'],
                                                      chargeInfo['clientId'],
                                                      chargeInfo['chargeTotal'],
                                                      chargeInfo.get('chargeType', 'na'))

            chargecategories_config = TyContext.Configure.get_global_item_json(
                'charge_categories_config', {})
            # 单机商城商品TY9999R00020DJ的订单，没有chargeType
            if 'chargeType' in chargeInfo:
                for key in chargecategories_config.keys():
                    if chargeInfo['chargeType'] in key:
                        lastChargeCategory = chargecategories_config[key]
                        TyContext.RedisUser.execute(
                            chargeInfo['uid'], 'HSET', 'user:' + str(chargeInfo['uid']),
                            'lastChargeCategory', lastChargeCategory)
                        break
            try:
                chargeInfo['isTestOrder'] = rparam['isTestOrder']
            except:
                pass
            try:
                chargeInfo['chargeType'] = rparam['chargeType']
            except:
                pass

            if consumeInfo:
                consumeInfo = json.loads(consumeInfo)

            Order.log(platformOrderId, Order.CALLBACK_OK, chargeInfo['uid'],
                      chargeInfo['appId'], chargeInfo['clientId'],
                      paytype=rparam.get('chargeType', 'na'),
                      prodid=chargeInfo.get('prodId', 'na'),
                      diamondid=chargeInfo['diamondId'],
                      prod_price=consumeInfo['consumeCoin'] if consumeInfo else 'na',
                      charge_price=chargeInfo['chargeTotal'],
                      succ_price=total_fee,
                      sub_paytype=rparam.get('sub_paytype', 'na'),
                      third_prodid=rparam.get('third_prodid', 'na'),
                      third_provid=rparam.get('third_provid', 'na'),
                      third_userid=rparam.get('third_userid', 'na'),
                      third_orderid=rparam.get('third_orderid', 'na'),
                      pay_appid=rparam.get('pay_appid', 'na'),
                      mobile=chargeInfo.get('vouchMobile', 'na'),
                      )
            try:
                chargeInfo['paytype_w_appid'] = '_'.join(
                    [chargeInfo['chargeType'], rparam['pay_appid']])
            except:
                pass
            # 记录支付通道的子渠道
            try:
                chargeInfo['sub_paytype'] = rparam.get('sub_paytype', '')
            except:
                pass

            if _check_price(platformOrderId, total_fee, state, rparam, errorInfo, chargeInfo, consumeInfo):
                return True

            # 给用户增加钻石
            cls.__change_user_coin__(platformOrderId, total_fee, chargeInfo, consumeInfo)

            if not consumeInfo:
                cls.__change_callback_state__(chargeKey, PayConst.CHARGE_STATE_DONE, '', None)
                Order.log(platformOrderId, Order.DELIVER_OK, chargeInfo['uid'],
                          chargeInfo['appId'], chargeInfo['clientId'],
                          paytype=paytype,
                          diamondid=chargeInfo['diamondId'],
                          charge_price=chargeInfo['chargeTotal'],
                          succ_price=total_fee,
                          sub_paytype=rparam.get('sub_paytype', 'na'),
                          third_prodid=rparam.get('third_prodid', 'na'),
                          third_orderid=rparam.get('third_orderid', 'na'),
                          pay_appid=rparam.get('pay_appid', 'na'),
                          )
                PayHelper.notify_game_server_on_diamond_change(
                    {'appId': chargeInfo['appId'], 'clientId': chargeInfo['clientId'],
                     'userId': chargeInfo['uid'], 'buttonId': chargeInfo['diamondId'],
                     'diamonds': chargeInfo['chargedDiamonds'],
                     'rmbs': chargeInfo['chargedRmbs']})
                return True

            cls.__change_callback_state__(chargeKey, PayConst.CHARGE_STATE_CONSUME, '', None)
            appId = consumeInfo['appId']
            appInfo = consumeInfo['appInfo']
            clientId = consumeInfo['clientId']
            userId = consumeInfo['userId']
            consumeCoin = consumeInfo['consumeCoin']
            prodId = consumeInfo['prodId']
            prodPrice = consumeInfo['prodPrice']
            prodCount = consumeInfo['prodCount']
            prodName = consumeInfo['prodName']
            prodOrderId = consumeInfo['prodOrderId']

            mo = TyContext.Cls_MsgPack()
            mo.setCmd('consume')
            # modified by zhangshibo at 2015-09-09
            if 'isYouyifuMonthVip' in rparam:
                TyContext.ftlog.debug('callback-> Has isYouyifuMonthVip info in rparam.')
                mo.setParam('is_monthly', '1')
            # end modify
            from consume import TuyouPayConsume
            TuyouPayConsume.__consume_user_coin__(
                appId, appInfo, clientId, userId, consumeCoin, prodId,
                prodPrice, prodCount, prodName, prodOrderId, mo,
                chargeInfo)
            if mo.isError():
                cls.__change_callback_state__(chargeKey, PayConst.CHARGE_STATE_ERROR_CONSUME, '', mo)
            else:
                cls.__change_callback_state__(chargeKey, PayConst.CHARGE_STATE_DONE_CONSUME, '', mo)
            PayHelper.notify_game_server_on_diamond_change(
                {'appId': appId, 'clientId': clientId, 'userId': userId,
                 'buttonId': prodId, 'diamonds': chargeInfo['chargedDiamonds'],
                 'rmbs': chargeInfo['chargedRmbs']})
            return True

        TyContext.ftlog.error('SHOULDNOT REACH HERE: callback invalid state', state,
                              'platformOrderId', platformOrderId)
        return True

    @classmethod
    def __change_callback_state__(cls, chargeKey, state, errorInfo, mo):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        datas = ['state', state, 'cbTime', timestamp]
        if errorInfo and len(errorInfo) > 0:
            datas.append('errorInfo')
            datas.append(errorInfo)
        if mo != None:
            datas.append('consume:mo')
            datas.append(mo.packJson())

        TyContext.RedisPayData.execute('HMSET', chargeKey, *datas)

    @classmethod
    def _is_danji_prods(cls, diamondId):
        danji_prods = TyContext.Configure.get_global_item_json('danji_prods')
        return diamondId in danji_prods

    @classmethod
    def __change_user_coin__(cls, platformOrderId, total_fee, chargeInfo, consumeInfo):

        TyContext.ftlog.debug('__change_user_coin__ platformOrderId, total_fee, chargeInfo, consumeInfo',
                              platformOrderId, total_fee, chargeInfo, consumeInfo)
        total_fee = float(total_fee)
        if total_fee < 0:
            total_fee = float(chargeInfo['chargeTotal'])

        userId = chargeInfo['uid']
        appId = chargeInfo['appId']
        clientId = chargeInfo['clientId']
        diamondId = chargeInfo['diamondId']
        diamondCount = cls.__cal_diamond_count__(appId, clientId, diamondId, total_fee)
        chargeInfo['chargedRmbs'] = total_fee
        chargeInfo['chargedDiamonds'] = diamondCount
        is_danji_order = cls._is_danji_prods(diamondId)
        clientip = TyContext.UserSession.get_session_client_ip(userId)
        userName = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'name')
        if userName == None:
            userName = ''

        # 记录全局充值记录
        appOrderId = ''
        if consumeInfo and 'prodOrderId' in consumeInfo:
            appOrderId = consumeInfo['prodOrderId']

        ct = datetime.datetime.now()
        paykey = ct.strftime('pay:%Y%m%d')
        chargehistory = {
            'time': ct.strftime('%Y%m%d%H%M%S'),
            'uid': userId,
            'appId': appId,
            'name': chargeInfo['diamondName'],
            'fee': total_fee,
            'clientId': clientId,
            'tyOrderId': platformOrderId,
            'appOrderId': appOrderId,
            'appInfo': chargeInfo.get('appInfo', ''),
            'diamondId': diamondId,
            'diamondCount': diamondCount,
            'vouchMobile': chargeInfo.get('vouchMobile', ''),
            'vouchIP': clientip,
            'subPaytype': chargeInfo.get('sub_paytype', ''),
            'userName': userName,
        }
        if consumeInfo:
            chargehistory['prodId'] = consumeInfo['prodId']
        if 'chargeType' in chargeInfo:
            chargehistory['type'] = chargeInfo['chargeType']
        if 'categories' in chargeInfo:
            chargehistory['categories'] = chargeInfo['chargeCategories']
        if chargeInfo.get('isTestOrder', False):
            chargehistory['isTestOrder'] = True
        chargehistory_dump = json.dumps(chargehistory)
        TyContext.ftlog.info('__change_user_coin__ chargehistory', paykey, chargehistory_dump)
        TyContext.RedisPayData.execute('LPUSH', paykey, chargehistory_dump)

        userKey = 'user:' + str(userId)
        if not is_danji_order:
            _, coin = TyContext.UserProps.incr_diamond(
                int(userId), int(appId), diamondCount,
                TyContext.ChipNotEnoughOpMode.NOOP, TyContext.BIEventId.UNKNOWN)
            TyContext.BiReport.diamond_update(appId, userId, diamondCount, coin,
                                              'charge.callback')

        # 增加用户的充值次数
        PayHelper.incr_paycount(userId)

        # 增加用户总体支付的数量
        TyContext.RedisUser.execute(userId, 'HINCRBYFLOAT', userKey, 'chargeTotal', total_fee)

        # 增加用户的钻石购买的数据
        RiskControl(userId).record_diamond(diamondId)
        try:
            ReportReyun().reportPayment(**chargeInfo)
        except:
            TyContext.ftlog.exception()
        # 更新IOS充值
        if 'type' in chargehistory and chargehistory['type'] == 'tuyooios':
            from tysdk.entity.paythird.payios import TuYouPayIos
            TuYouPayIos._update_ios_quota(userId, total_fee)
            # 增加玩家充值信息
            TuYouPayIos._zadd_user_ios_pay(userId, total_fee)

        # 修改用户的短信支付限额信息
        duandais = TyContext.Configure.get_global_item_json('all_duandai_paytypes', {})
        if 'type' in chargehistory:
            paytype = chargehistory['type']
            if paytype in duandais:
                TyContext.SmsPayCheck.update_sms_pay_info_by_type(
                    userId, total_fee, paytype)
                TyContext.SmsPayCheck.update_sms_pay_timestamp(userId, paytype)
                try:
                    paytype = chargeInfo['paytype_w_appid']
                except:
                    pass
                RiskControl(userId).record_usage(paytype, total_fee)
                operator = TyContext.UserSession.get_phone_type_name(
                    TyContext.UserSession.get_session_phone_type(userId))
                Channels.incr_volume(operator, paytype, total_fee)
                # 对同一IP支付次数进行更新
                clientip = TyContext.UserSession.get_session_client_ip(userId)
                Channels.incr_ip_count(paytype, clientip)
            else:
                TyContext.SmsPayCheck.update_sms_pay_info(userId, total_fee)

    @classmethod
    def __cal_diamond_count__(cls, appId, clientId, diamondId, total_fee):
        TyContext.ftlog.debug('__cal_diamond_count__', appId, clientId, diamondId, total_fee)
        diamond = None
        appDiamonds = TuyouPayDiamondList.diamondlist2(appId, clientId)
        for x in xrange(len(appDiamonds) - 1, -1, -1):
            diamond = appDiamonds[x]
            if diamondId == diamond['id']:
                break
        diamondPrice = diamond['price']
        TyContext.ftlog.debug('__cal_diamond_count__', diamondPrice, total_fee, diamond)
        if diamondPrice == total_fee:
            diamondCount = diamond['count']
        else:
            diamondCount = int(float(total_fee) * (float(diamond['count']) / float(diamondPrice)))

        return diamondCount
