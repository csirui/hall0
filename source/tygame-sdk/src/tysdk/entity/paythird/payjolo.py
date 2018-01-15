#! encoding=utf-8

import json
import urlparse

from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaVerify
from tysdk.entity.paythird.helper import PayHelper

__author__ = 'yuejianqiang'


class TuYouPayJolo(object):
    version = "5.0.0"
    encoding_UTF8 = "UTF-8"
    merId = '777290058124087'
    appTransUrl = 'https://101.231.204.80:5000/gateway/api/appTransReq.do'
    certId = '40220995861346480087409489142384722381'

    @classmethod
    def charge_data(cls, chargeinfo):
        platformOrderId = chargeinfo['platformOrderId']
        packageName = chargeinfo['packageName']
        jolo_config = TyContext.Configure.get_global_item_json('jolo_keys', {})
        notifyUrl = 'http://open.touch4.me/v1/pay/jolo/callback'
        userId = chargeinfo['uid']
        snsId, snsinfo = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%s' % userId, 'snsId', 'snsinfo')
        app_keys = jolo_config.get(packageName, {})
        chargeData = {
            'gameCode': app_keys['gameCode'],
            'gameName': app_keys['gameName'],
            'privateKey': app_keys['privateKey'],
            'session': snsinfo,
            'notifyUrl': notifyUrl,
        }
        chargeinfo['chargeData'] = chargeData

    @classmethod
    def doCallback(cls, rpath):
        postData = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.info("postData", postData)
        response = urlparse.parse_qs(postData)
        order = response['order'][0].strip('"')
        sign = response['sign'][0].strip('"')
        jsonData = json.loads(order)
        platformOrderId = jsonData['game_order_id']
        if not rsaVerify(order, sign, 'jolo'):
            TyContext.ftlog.debug('TuYouPayJolo->doCallback', 'order=%s' % order, 'sign=%s' % sign)
            return 'sign error'
        isOk = PayHelper.callback_ok(platformOrderId, -1, jsonData)
        if isOk:
            return 'success'
        else:
            return 'error'
