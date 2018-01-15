# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import traceback

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4
from tysdk.entity.pay_common.orderlog import Order


class TuYouPayWYXTV4(PayBaseV4):
    get_order_url = 'http://http://101.201.110.179:8901/sdkdispatcher/recvtuyouorder'

    @payv4_order('wyxt')
    def charge_data(self, mi):
        return self.handle_order(mi)

    @payv4_callback('/open/v4/pay/wyxt/request')
    def doPayRequst(self, rpaht):
        mo = TyContext.MsgPack()
        params = TyContext.RunHttp.convertArgsToDict()
        mobile = params.get('mobile', '')
        platformOrderId = params.get('platformOrderId', '')
        imsi = params.get('imsi', '')
        imei = params.get('imei', '')
        chargeInfo = self.get_charge_info_data(platformOrderId)
        price = chargeInfo.get('chargeTotal')
        config = GameItemConfigure(chargeInfo.get('appId')).get_game_channel_configure_by_package('wyxt', chargeInfo[
            'packageName'],
                                                                                                  chargeInfo[
                                                                                                      'mainChannel'])
        if not config:
            package = "com.tuyou.doudizhu.main"
            channel = 'wyxt'
            appId = '9999'
            config = GameItemConfigure(appId).get_game_channel_configure_by_package('wyxt', package, channel)
        config = config.get('app_config_%s' % price, {})
        if not config:
            mo.setResult('info', '计费点未配置，请检查')
            mo.setResult('code', 1)
            return mo
        postParams = {
            'mobile': mobile,
            'channelid': config.get('channel_id'),
            'app_name': config.get('app_name'),
            'itemid': config.get('itemid'),
            'imsi': imsi,
            'p_price': config.get('price'),
            'imei': imei,
            'callbackdata': platformOrderId,
        }
        try:
            response, _ = TyContext.WebPage.webget(self.get_order_url, postParams)
        except:
            mo.setResult('info', '支付请求失败，请稍后重试')
            mo.setResult('code', 1)
            return mo
        if 'ok' in response:
            mo.setResult('info', '支付请求成功')
            mo.setResult('code', 0)
        else:
            mo.setResult('info', '支付请求失败，请稍后重试')
            mo.setResult('code', 1)
        return mo

    @classmethod
    def get_charge_info_data(cls, platformOrderId):
        chargeKey = 'sdk.charge:' + platformOrderId
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        if chargeInfo == None:
            chargeInfo = {}
        else:
            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
        return chargeInfo

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

    @payv4_callback('/open/ve/pay/wyxt/callback')
    def doMomoCallback(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        clientIp = TyContext.RunHttp.get_client_ip()
        if clientIp != '101.201.110.179':
            print 'clientId diffrent,please check!', clientIp
        orderstate = params.get('orderstate', '')
        if str(orderstate) != '1':
            return 'error'
        orderId = params.get('orderid')
        chargeInfo = cls.get_charge_info_data(orderId)
        user_id = chargeInfo.get('userId', '')
        feevalue = params.get('feevalue', '')
        status = params.get('status', '')
        if str(status) == '-99':
            # 订购
            TyContext.RedisUser.execute(user_id, 'HMSET', 'user:' + user_id, 'isYouyifuVipUser', '1', 'youyifuVipMsg',
                                        message, 'bugYouyifuVipAppid', appId, 'bugYouyifuVipClientid', clientId)

            # 这个参数用来告诉游戏服务器，这个商品是一件优易付的会员包月商品
            params['isYouyifuMonthVip'] = '1'
            PayHelperV4.callback_ok(orderId, feevalue, params)
            cls.reportBi(Order.SUBSCRIBE, params, orderId)

        elif str(status) == '-100':
            # 退订
            status = cls._NotifyGameServerUnsubscribe(orderId, user_id)
            if not status:
                TyContext.ftlog.error(
                    'TuYouPayYi->doYiPayCallback Notify Game server user [%s] unsubscribed ERROR!' % user_id)
                return 'success'
            try:
                TyContext.MySqlSwap.checkUserDate(user_id)
            except:
                TyContext.ftlog.error('TuYouPayYi->doYiPayCallback get cold data')
            TyContext.RedisUser.execute(user_id, 'HSET', 'user:' + user_id, 'isYouyifuVipUser', '0')
            cls.reportBi(Order.UNSUBSCRIBE, params, orderId)

    @classmethod
    def reportBi(cls, eventId, params, platformOrderId, infomation='na'):
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
