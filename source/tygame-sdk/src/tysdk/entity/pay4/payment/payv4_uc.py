# -*- coding=utf-8 -*-
from hashlib import md5

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


class TuYouPayUcV4(PayBaseV4):
    @payv4_order('uc')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        notifyurl = PayHelperV4.getSdkDomain() + '/v1/pay/uc/callback'
        TyContext.ftlog.debug('TuYouPayUc charge_data callback url=', notifyurl)
        paydata = cls.generate_sign(mi, chargeinfo)
        chargeinfo['chargeData'] = {'notifyUrl': notifyurl, 'payData': paydata}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    def generate_sign(self, mi, chargeinfo):
        uc_uid = mi.getParamStr('uc_uid', '')
        params = {
            'amount': '%.2f' % chargeinfo['chargeTotal'],
            'notifyUrl': PayHelperV4.getSdkDomain() + '/v1/pay/uc/callback',
            'accountId': uc_uid,
            'signType': 'MD5',
            'callbackInfo': chargeinfo['userId'],
            'cpOrderId': chargeinfo['platformOrderId']
        }
        from hashlib import md5
        signStr = ''.join(k + '=' + str(params[k]) for k in sorted(params) if k != 'sign' and k != 'signType')
        config = GameItemConfigure.get_game_channel_configure_by_orderId(params['cpOrderId'], 'uc')
        if not config:
            TyContext.ftlog.error('TuYouPayUcV4,can not find uc config for package:', chargeinfo['packageName'])
            config = {}
        apiKey = config.get('apiKey', '')
        signStr += apiKey
        m = md5(signStr)
        params['sign'] = m.hexdigest().lower()
        return params

    @payv4_callback('/open/ve/pay/uc/callback')
    def doUcCallback(cls, rpath):
        TyContext.ftlog.debug('doUcCallback start')
        body = TyContext.RunHttp.get_body_content()
        rparam = TyContext.strutil.loads(body, decodeutf8=True)
        data = rparam['data']

        try:
            orderPlatformId = data['cpOrderId']
            state = data['orderStatus']
            total_fee = data['amount']
            sign = rparam['sign']
            thirdorderid = data['orderId']
        except:
            TyContext.ftlog.error('TuYouPayUc.doUcCallback->ERROR, param error !! rparam=', rparam)
            return 'SUCCESS'
        # 签名校验
        if not cls.__verify_sign(data, sign):
            TyContext.ftlog.error('TuYouPayUc.doUcCallback verify error !!')
            return 'FAILURE'
        # 充值状态校验
        if state != 'S':
            TyContext.ftlog.info('TuYouPayUc.doUcCallback, charge failed. fail reason:', data['failedDesc'])
            PayHelperV4.callback_error(orderPlatformId, data['failedDesc'], rparam)
            return 'SUCCESS'

        rparam['chargeType'] = 'uc'
        rparam['third_orderid'] = thirdorderid
        total_fee = float(total_fee)
        ChargeModel.save_third_pay_order_id(orderPlatformId, thirdorderid)
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, data)
        return 'SUCCESS'

    @classmethod
    def __verify_sign(cls, rparam, sign):
        ucconfig = TyContext.Configure.get_global_item_json('uc_config', {})
        gameid = rparam['gameId']
        try:
            ucgameidconfig = ucconfig[gameid]
            apiKey = str(ucgameidconfig['apiKey'])
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(rparam['cpOrderId'], 'uc')
            apiKey = config.get('apiKey')
        check_str = ('accountId=' + rparam['accountId']
                     + 'amount=' + rparam['amount']
                     + 'callbackInfo=' + rparam['callbackInfo']
                     + 'cpOrderId=' + rparam['cpOrderId']
                     + 'creator=' + rparam['creator']
                     + 'failedDesc=' + rparam['failedDesc']
                     + 'gameId=' + rparam['gameId']
                     + 'orderId=' + rparam['orderId']
                     + 'orderStatus=' + rparam['orderStatus']
                     + 'payWay=' + rparam['payWay']
                     + apiKey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayUc.doUcCallback verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
