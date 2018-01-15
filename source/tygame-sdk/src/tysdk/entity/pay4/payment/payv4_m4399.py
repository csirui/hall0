#! encoding=utf-8
from tysdk.configure.game_item import GameItemConfigure

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
from payv4_helper import PayHelperV4
import hashlib

from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.decorator.payv4_order import payv4_order


class TuYouPayM4399V4(PayBaseV4):
    @payv4_order("m4399")
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId'], }
        m4399_keys = TyContext.Configure.get_global_item_json('m4399_keys', {})
        packageName = chargeinfo['packageName']
        try:
            appInfo = m4399_keys[packageName]
            appKey = appInfo['appKey']
            appSecret = appInfo['appSecret']
        except KeyError:
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('4399', packageName,
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])
            appKey = config.get('m4399_appKey')
            appSecret = config.get('m4399_appSecret')
        chargeKey = 'sdk.charge:m4399:%s' % chargeinfo['platformOrderId']
        TyContext.RedisPayData.execute('HMSET', chargeKey, 'appKey', appKey, 'appSecret', appSecret)
        TyContext.RedisPayData.execute('EXPIRE', chargeKey, 60 * 60)
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/4399/callback")
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayM4399->doCallback, rparams=', rparams)
        orderid = rparams['orderid']
        p_type = rparams['p_type']
        uid = rparams['uid']
        money = rparams['money']
        gamemoney = rparams['gamemoney']
        serverid = rparams.get('serverid', '')
        mark = rparams.get('mark', '')
        roleid = rparams.get('roleid', '')
        time = rparams.get('time', '')
        sign = rparams.get('sign', '')
        ###
        platformOrderId = mark
        chargeKey = 'sdk.charge:m4399:%s' % platformOrderId
        appKey, appSecret = TyContext.RedisPayData.execute('HMGET', chargeKey, 'appKey', 'appSecret')
        # TyContext.ftlog.debug('TuYouPayM4399->get order info:', 'userId=%s platformOrderId=%s appKey=%s' % (userId, platformOrderId, appKey))
        signList = [orderid, uid, money, gamemoney, serverid, appSecret, mark, roleid, time]
        mysign = hashlib.md5(''.join(signList)).hexdigest()
        if mysign != sign:
            TyContext.ftlog.error('doIDOCallback->ERROR, sign error !! rparam=', rparams)
            return '{"status":1, "code":"sign_error", "money":"%s", "gamemoney":"%s", "msg":"充值成功"}' % (
            money, gamemoney)
        # do charge
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return '{"status":2,"code":null, "money":"%s", "gamemoney":"%s", "msg":"充值成功"}' % (money, gamemoney)
        else:
            return '{"status":1,"code":"other_error", "money":"%s", "gamemoney":"%s", "msg":"充值成功"}' % (
            money, gamemoney)
