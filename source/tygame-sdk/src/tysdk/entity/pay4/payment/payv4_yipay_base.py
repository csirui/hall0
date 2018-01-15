# -*- coding=utf-8 -*-

import traceback
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay_common.orderlog import Order

create_errmsg = {
    '10000': '系统异常',
    '10002': '请求参数异常',
    '10005': '未知数据异常',
    '20901': '请求运营商返回无效结果',
    '20902': '短信验证码错误',
    '20903': '手机号被运营商锁定',
    '20904': '发送验证码失败',
    '20905': '手机号超过日消费限额',
    '20906': '手机号超过月消费限额',
    '20907': '用户名超过日消费限额',
    '20908': '用户名超过月消费限额',
    '20909': '同一设备为不同账号充值超过上限',
    '20910': '同一手机号为不同用户充值超过上限',
    '20911': '同一个手机号为不同用户充值超过上限',
    '20912': '手机号余额不足',
    '20913': 'MD5签名校验失败',
    '20915': '黑名单用户',
}


class TuYouPayYiBase(PayBaseV4):
    def do_yipay_callback(cls, paytype):
        rparam = TyContext.RunHttp.convertArgsToDict()
        try:
            orderPlatformId = rparam['app_orderid']
            mobileId = rparam.get('phone', '')
            if not mobileId and 'phone' in rparam.keys():
                del rparam['phone']
            sign = rparam['sign']
            merc_id = rparam['merc_id']
            status = int(rparam['status'])
            user_id = rparam['userid']
            is_monthly = int(rparam['is_monthly'])
        except Exception as e:
            TyContext.ftlog.error('do_yipay_callback->ERROR, exception', e, 'rparam', rparam)
            return 'error'

        # 签名校验
        appkey_config = TyContext.Configure.get_global_item_json('yipay_appkey_config', {})
        try:
            appkey = appkey_config[merc_id]
        except:
            TyContext.ftlog.error('do_yipay_callback appkey not configed'
                                  ' for merc_id', merc_id)
            return 'error'
        if not cls._verify_sign(rparam, sign, appkey):
            return 'error'

        rec_amount = rparam['rec_amount']
        pay_amount = rparam['pay_amount']
        if rec_amount != pay_amount:
            TyContext.ftlog.error('do_yipay_callback pay_amount', pay_amount,
                                  'not equal to rec_amount', rec_amount)
        total_fee = float(pay_amount) / 100
        rparam['third_orderid'] = rparam['orderid']
        rparam['sub_paytype'] = rparam['ch_type']
        rparam['chargeType'] = paytype
        rparam['mobileId'] = mobileId
        if status == 1:
            PayHelperV4.set_order_mobile(orderPlatformId, mobileId)
            # 判断用户购买的是不是包月会员
            if 2 == is_monthly:
                TyContext.ftlog.debug('TuYouPayYi->doYiPayCallback User [%s] buy monthly goods.' % user_id)
                # 修改用户表，将用户状态置为会员状态
                '''
                if 'message' in rparam:
                    message = rparam['message']
                else:
                    TyContext.ftlog.info('TuYouPayYi->doYiPayCallback ERROR, Doesn\'t has message parameter.'
                                          'userid: [%s], platformorderid: [%s], third_id: [%s]'
                                          % (user_id, orderPlatformId, rparam['third_orderid']))
                    message = '退订请联系会员退订专用电话: 4008-098-000'
                '''
                message = '退订请联系会员退订专用电话: 4008-098-000'
                # 记录购买会员的appId、clientId
                chargeKey = 'sdk.charge:' + orderPlatformId
                chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
                if chargeInfo == None:
                    chargeInfo = {}
                else:
                    chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)

                appId = chargeInfo.get('appId', 9999)
                clientId = chargeInfo.get('clientId', '')

                TyContext.RedisUser.execute(user_id, 'HMSET', 'user:' + user_id, 'isYouyifuVipUser', '1',
                                            'youyifuVipMsg', message, 'bugYouyifuVipAppid', appId,
                                            'bugYouyifuVipClientid', clientId)

                # 这个参数用来告诉游戏服务器，这个商品是一件优易付的会员包月商品
                rparam['isYouyifuMonthVip'] = '1'
                PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
                cls.reportBi(Order.SUBSCRIBE, rparam)
                TyContext.ftlog.info('TuYouPayYi->doYiPayCallback user %s has subscribed Monthly VIP.' % user_id)
            else:
                PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
            return 'success'
        elif status == 3:
            # 包月退订,修改用户表,将用户状态置为非会员状态,并通知游戏服用户退订
            status = cls._NotifyGameServerUnsubscribe(orderPlatformId, user_id)
            if not status:
                TyContext.ftlog.error(
                    'TuYouPayYi->doYiPayCallback Notify Game server user [%s] unsubscribed ERROR!' % user_id)
                return 'success'
            try:
                TyContext.MySqlSwap.checkUserDate(user_id)
            except:
                TyContext.ftlog.error('TuYouPayYi->doYiPayCallback get cold data')
            TyContext.RedisUser.execute(user_id, 'HSET', 'user:' + user_id, 'isYouyifuVipUser', '0')
            cls.reportBi(Order.UNSUBSCRIBE, rparam)
            return 'success'
        else:
            errinfo = '支付失败' + str(rparam.get('status_desc', ''))
            PayHelperV4.callback_error(orderPlatformId, errinfo, rparam)
            return 'success'

    def _cal_sign(cls, params):
        params['merc_key'] = cls.yipay_key
        check_str = '&'.join(k + "=" + str(params[k]) for k in sorted(params.keys()) if k != 'sign')
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        del params['merc_key']
        return digest

    def _verify_sign(cls, rparam, sign, appkey):
        rparam['merc_key'] = appkey
        check_str = '&'.join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) if k != 'sign')
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayYi verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True

    @classmethod
    def _NotifyGameServerUnsubscribe(cls, orderPlatformId, user_id):
        chargeKey = 'sdk.charge:' + orderPlatformId
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        if chargeInfo == None:
            appId, clientId = TyContext.RedisUser.execute(user_id, 'HMGET', 'user:' + str(user_id),
                                                          'bugYouyifuVipAppid', 'bugYouyifuVipClientid')
        else:
            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
            appId = chargeInfo.get('appId', 9999)
            clientId = chargeInfo.get('clientId', '')

        if clientId == None or clientId == '':
            # TyContext.ftlog.error('TuYouPayYi->doYiPayCallback Get appId and clientId ERROR.')
            # return False
            clientId = 'Android_3.73_360,tyGuest.360,yisdkpay4.0-hall6.360.dj'

        try:
            control = TyContext.ServerControl.findServerControl(appId, clientId)
            deliveryUrl = control['http'] + '/v2/game/sdk/youyifuVip/unsubscribe'
            TyContext.ftlog.debug('TuYouPayYi->doYiPayCallback deliveryUrl %s.' % deliveryUrl)
        except Exception as e:
            TyContext.ftlog.error('TuYouPayYi->doYiPayCallback Get GameServer IP ERROR! exception ', e)
            traceback.print_exc()
            return False

        parameter = {'userId': user_id}
        response, request_url = TyContext.WebPage.webget(deliveryUrl, parameter)
        if 0 != cmp(response, 'success'):
            TyContext.ftlog.error(
                'TuYouPayYi->doYiPayCallback Notify game server user %s has unsubscribed Monthly VIP ERROR.' % user_id)
            return False
        TyContext.ftlog.info('TuYouPayYi->doYiPayCallback user %s has unsubscribed Monthly VIP.' % user_id)
        return True

    @classmethod
    def reportBi(cls, eventId, params, infomation='na'):
        platformOrderId = params['app_orderid']
        chargeKey = 'sdk.charge:' + platformOrderId
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        if chargeInfo == None:
            chargeInfo = {}
            appId, clientId = TyContext.RedisUser.execute(params['userid'], 'HMGET', 'user:' + str(params['userid']),
                                                          'bugYouyifuVipAppid', 'bugYouyifuVipClientid')
        else:
            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
            appId = chargeInfo.get('appId', 9999)
            clientId = chargeInfo.get('clientId', '')

        if clientId == None or clientId == '':
            # TyContext.ftlog.error('TuYouPayYi->doYiPayCallback Get appId and clientId ERROR.')
            # return False
            clientId = 'Android_3.73_360,tyGuest.360,yisdkpay4.0-hall6.360.dj'

        Order.log(platformOrderId, eventId, chargeInfo.get('uid', params['userid']), str(appId), clientId,
                  info=infomation,
                  paytype=chargeInfo.get('chargeType', 'na'),
                  diamondid=chargeInfo.get('diamondId', 'na'),
                  charge_price=chargeInfo.get('chargeTotal', 'na'),
                  succ_price=chargeInfo.get('chargeTotal', 'na'),
                  prod_price=chargeInfo.get('chargeTotal', 'na'),
                  sub_paytype=params.get('sub_paytype', 'na'),
                  mobile=params.get('mobileId', 'na')
                  )
