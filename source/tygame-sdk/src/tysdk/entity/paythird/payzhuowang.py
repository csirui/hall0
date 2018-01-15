# -*- coding=utf-8 -*-

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay_common.clientrevision import ClientRevision


class TuYouPayZhuowang(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        mdo_config = TyContext.Configure.get_global_item_json('zwmdo_configs', {})
        price = int(float(chargeinfo['chargeTotal']))
        if not str(price) in mdo_config['smscodes']:
            TyContext.ftlog.error('can not find zhuowang smscode in the price=', price)
            return
        orderPlatformId = chargeinfo['platformOrderId']
        spnumber = mdo_config['spnumber']
        smscode = mdo_config['smscodes'][str(price)]
        shortorderid = ShortOrderIdMap.get_short_order_id(orderPlatformId)
        sms_msg = smscode.format(orderId=shortorderid)

        # type是短信支付的方式，1代表的是发一条短信支付
        userId = chargeinfo['uid']
        if not ClientRevision(userId).support_type0_smspayinfo:
            payinfo = SmsPayInfo.getSmsPayInfo(1, sms_msg, spnumber)
        else:
            no_hint = chargeinfo.get('nohint', None)
            messages = []
            messages.append((spnumber, sms_msg, 1000))
            payinfo = SmsPayInfo.build_sms_payinfo(messages, nohint=no_hint)
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}

    @classmethod
    def doZhuowangCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('doZhuowangCallback start, rparam=', rparam)

        try:
            sts = rparam['sts']
            shortorderid = rparam['cmd'].split(',')[-1]
        except:
            TyContext.ftlog.error('doZhuowangCallback->ERROR, param error !! rparam=', rparam)
            return 'error'

        orderPlatformId = ShortOrderIdMap.get_long_order_id(shortorderid)
        mobileId = rparam.get('usernumber', 'na')
        PayHelper.set_order_mobile(orderPlatformId, mobileId)
        rparam['third_orderid'] = rparam.get('tnsid', 'na')
        rparam['sub_paytype'] = rparam.get('feetype', 'na')
        if int(sts) != 0:
            errinfo = 'sts(%s) not 0' % sts
            PayHelper.callback_error(orderPlatformId, errinfo, rparam)
        else:
            total_fee = float(rparam['feecode']) / 100
            isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        return '0'  # success
