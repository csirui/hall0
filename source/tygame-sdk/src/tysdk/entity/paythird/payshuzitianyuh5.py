# -*- coding=utf-8 -*-

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay_common.clientrevision import ClientRevision


class TuYouPayShuzitianyuH5(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        TyContext.ftlog.debug('TuyoPayShuzitianyuH5 chare_data ,chargeinfo=', chargeinfo)
        userId = chargeinfo['uid']
        price = int(float(chargeinfo['chargeTotal']))
        platformOrderId = chargeinfo['platformOrderId']
        sms_msg, spnumber = cls._create_order(price, platformOrderId)
        if not sms_msg:
            TyContext.ftlog.error('TuYouPayShuzitianyuH5 create_order failed for user', userId,
                                  'orderid', platformOrderId, 'response', sms_msg)
            return

        if not ClientRevision(userId).support_type0_smspayinfo:
            payinfo = SmsPayInfo.getSmsPayInfo(1, sms_msg, spnumber)
            chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
            return
        messages = [(spnumber, sms_msg, 1000)]
        no_hint = chargeinfo.get('nohint', None)
        payinfo = SmsPayInfo.build_sms_payinfo(messages, nohint=no_hint)
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}

    @classmethod
    def _create_order(cls, amount, orderPlatformId):
        szty_config = TyContext.Configure.get_global_item_json('shuzitianyu_h5_config', {})
        createorder_url = str(szty_config['createorder_url'])
        payconfig = szty_config['paycode_config']
        port = payconfig[str(amount)]['port']
        params = {}
        params['orderid'] = orderPlatformId
        params['scid'] = payconfig[str(amount)]['scid']
        try:
            response_msg, final_url = TyContext.WebPage.webget(createorder_url, params)
            TyContext.ftlog.debug('shuzitianyu_h5 create_order succ ,response_msg=',
                                  response_msg)
            return response_msg, port
        except Exception as e:
            TyContext.ftlog.error('payshuzitianyuh5 _ctreate_order webget \
                                  failed. exception:', e)
            return None, 0

    @classmethod
    def doSztyPayH5Callback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doSztyPayH5Callback', rparam)
        clientip = TyContext.RunHttp.get_client_ip()
        szty_config = TyContext.Configure.get_global_item_json('shuzitianyu_h5_config', {})
        callback_ip = str(szty_config['callback_ip'])
        if clientip != callback_ip:
            TyContext.ftlog.error('doSztyPayH5Callback->ip auth failed. '
                                  'callback ip', clientip, 'expected', callback_ip)
            return 'error'

        try:
            orderPlatformId = rparam['orderid']
            mobileId = rparam.get('mob', '')
            state = int(rparam['state'])
            price = int(rparam['price'])
        except Exception as e:
            TyContext.ftlog.error('doSztyPayH5Callback->param error !! rparam=',
                                  rparam, 'Exception:', e)
            return 'error'

        TyContext.ftlog.debug('doSztyPayH5Callback orderId', orderPlatformId)
        if state == 0:
            PayHelper.set_order_mobile(orderPlatformId, mobileId)
            isOk = PayHelper.callback_ok(orderPlatformId, price / 100.0, rparam)
            return 'ok'
        else:
            PayHelper.callback_error(orderPlatformId, '支付失败', rparam)
            return 'error'
