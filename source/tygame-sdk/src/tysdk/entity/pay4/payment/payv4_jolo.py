#! encoding=utf-8

import json
import urlparse

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import rsaVerify
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4

__author__ = 'yuejianqiang'


class TuYouPayJoloV4(PayBaseV4):
    version = "5.0.0"
    encoding_UTF8 = "UTF-8"
    merId = '777290058124087'
    appTransUrl = 'https://101.231.204.80:5000/gateway/api/appTransReq.do'
    certId = '40220995861346480087409489142384722381'

    @payv4_order("jolo")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        platformOrderId = chargeinfo['platformOrderId']
        packageName = chargeinfo['packageName']
        jolo_config = TyContext.Configure.get_global_item_json('jolo_keys', {})
        notifyUrl = 'http://open.touch4.me/v1/pay/jolo/callback'
        userId = chargeinfo['uid']
        snsId, snsinfo = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%s' % userId, 'snsId', 'snsinfo')
        try:
            app_keys = jolo_config[packageName]
        except KeyError:
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('htc', packageName,
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])
            app_keys = {
                'gameCode': config.get('htc_gamecode'),
                'gameName': config.get('htc_gamename'),
                'privateKey': config.get('htc_jolo_private_key')
            }
        chargeData = {
            'gameCode': app_keys['gameCode'],
            'gameName': app_keys['gameName'],
            'privateKey': app_keys['privateKey'],
            'session': snsinfo,
            'notifyUrl': notifyUrl,
        }
        chargeinfo['chargeData'] = chargeData
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback("/open/ve/pay/jolo/callback")
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
        ChargeModel.save_third_pay_order_id(platformOrderId, jsonData.get('jolo_order_id', ''))
        isOk = PayHelperV4.callback_ok(platformOrderId, -1, jsonData)
        if isOk:
            return 'success'
        else:
            return 'error'
