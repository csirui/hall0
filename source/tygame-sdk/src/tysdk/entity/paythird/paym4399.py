#! encoding=utf-8

__author__ = 'yuejianqiang'

import hashlib

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayM4399(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId'], }
        m4399_keys = TyContext.Configure.get_global_item_json('m4399_keys', {})
        packageName = chargeinfo['packageName']
        appInfo = m4399_keys[packageName]
        appKey = appInfo['appKey']
        appSecret = appInfo['appSecret']
        chargeKey = 'sdk.charge:m4399:%s' % chargeinfo['platformOrderId']
        TyContext.RedisPayData.execute('HMSET', chargeKey, 'appKey', appKey, 'appSecret', appSecret)

    @classmethod
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
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return '{"status":2,"code":null, "money":"%s", "gamemoney":"%s", "msg":"充值成功"}' % (money, gamemoney)
        else:
            return '{"status":1,"code":"other_error", "money":"%s", "gamemoney":"%s", "msg":"充值成功"}' % (
            money, gamemoney)
