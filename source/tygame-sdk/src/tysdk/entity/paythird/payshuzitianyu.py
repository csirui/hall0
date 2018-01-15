# -*- coding=utf-8 -*-

from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay_common.clientrevision import ClientRevision


class TuYouPaySzty(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        userId = chargeinfo['uid']
        price = int(float(chargeinfo['chargeTotal']))
        platformOrderId = chargeinfo['platformOrderId']
        shortOrderId = ShortOrderIdMap.get_short_order_id(platformOrderId)

        response, spnumber = cls.__create_order(price, shortOrderId)
        if len(response) == 1:
            TyContext.ftlog.error('TuYouPaySzty create_order failed for user', userId,
                                  'orderid', platformOrderId, 'response', response)
            return

        sms_msg = response
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
    def __create_order(cls, amount, orderPlatformId):
        sztyconfig = TyContext.Configure.get_global_item_json('shuzitianyu_config', {})
        createorder_url = str(sztyconfig['createorder_url'])
        payconfig = sztyconfig['paycode_config']
        port = payconfig[str(amount)]['port']
        params = {}
        params['oid'] = payconfig[str(amount)]['oid']
        params['feecode'] = payconfig[str(amount)]['feecode']
        params['orderid'] = payconfig[str(amount)]['channelid'] + '00' + orderPlatformId
        params['mobileid'] = ''
        params['sign'] = cls.__cal_sign(params)
        response_msg, final_url = TyContext.WebPage.webget(createorder_url, params)
        return response_msg, port

    @classmethod
    def doSztyPayCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        clientip = TyContext.RunHttp.get_client_ip()
        sztyconfig = TyContext.Configure.get_global_item_json('shuzitianyu_config', {})
        callback_ip = str(sztyconfig['callback_ip'])
        if clientip != callback_ip:
            TyContext.ftlog.error('doSztyPayCallback->ERROR, ip error !! ip =', clientip)
            return 'error'

        try:
            shortorderPlatformId = rparam['linkid'][7:]
            mobileId = rparam.get('mobile', '')
            status = int(rparam['status'])
        except:
            TyContext.ftlog.error('doSztyPayCallback->ERROR, param error !! rparam=', rparam)
            return 'error'

        orderPlatformId = ShortOrderIdMap.get_long_order_id(shortorderPlatformId)
        rparam['chargeType'] = 'shuzitianyu'
        if status == 1:
            PayHelper.set_order_mobile(orderPlatformId, mobileId)
            isOk = PayHelper.callback_ok(orderPlatformId, -1, rparam)
            # Youyifu will resend the callback if the response is NOT 'success'
            return 'success'
        else:
            PayHelper.callback_error(orderPlatformId, '支付失败', rparam)
            return 'success'

    @classmethod
    def __cal_sign(cls, params):
        check_str = params['orderid'] + params['oid'] + params['feecode'] + params['orderid'][-4:]
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().upper()
        return digest
