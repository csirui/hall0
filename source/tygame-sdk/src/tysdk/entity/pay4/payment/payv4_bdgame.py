# -*- coding=utf-8 -*-

import json
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayBDGameV4(PayBaseV4):
    @payv4_order("bdgame")
    def charge_data(self, mi):
        chargeInfo = self.get_charge_info(mi)
        chargeInfo['chargeData'] = {
            'platformOrderId': chargeInfo['platformOrderId'],
            'notifyUrl': PayHelperV4.getSdkDomain() + '/v1/pay/bdgame/callback'
        }
        return self.return_mo(0, chargeInfo=chargeInfo)

    @payv4_callback("/open/ve/pay/bdgame/callback")
    def doCallback(self, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        order_id = rparams['CooperatorOrderSerial']

        TyContext.ftlog.debug('TuYouPayBDGameV4->doCallback, rparams=', rparams)

        if not self.check_sign(rparams):
            # 1成功,不等于1失败
            return self.build_response(rparams, 1001, '验签失败')

        isOk = PayHelperV4.callback_ok(order_id, -1, rparams)

        if isOk:
            return self.build_response(rparams, 1, '发货成功')
        else:
            return self.build_response(rparams, 1002, '发货失败')

    def build_response(self, rparams, resule_code, result_msg):
        app_id = rparams['AppID']
        order_id = rparams['CooperatorOrderSerial']
        config = TyContext.Configure.get_global_item_json("bdgame_keys", {})
        try:
            secret_key = config[str(app_id)]['secretKey']
        except:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(order_id, "bdgame")
            secret_key = config.get('bdgame_secretKey', "")

        result = {
            'AppID': app_id,
            'ResultCode': resule_code,
            'ResultMsg': result_msg,
            'Sign': md5('%s%s%s' % (app_id, resule_code, secret_key)).hexdigest(),
            'Content': ''
        }

        TyContext.ftlog.debug('TuYouPayYiwanV4-> resp ->', result)

        return json.dumps(result)

    def check_sign(self, rparams):
        sign = rparams['Sign']
        app_id = rparams['AppID']
        order_serial = rparams['OrderSerial']
        order_id = rparams['CooperatorOrderSerial']
        content = rparams['Content']

        config = TyContext.Configure.get_global_item_json("bdgame_keys", {})
        try:
            secret_key = config[str(app_id)]['secretKey']
        except:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(order_id, "bdgame")
            secret_key = config.get('bdgame_secretKey', "")
            if not secret_key:
                TyContext.ftlog.debug("do BdgameCallback ->cannot find sdkconfig for", app_id)
                return False
        text = '%s%s%s%s%s' % (app_id, order_serial, order_id, content, secret_key)

        if sign == md5(text).hexdigest():
            return True
        else:
            return False
