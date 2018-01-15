# -*- coding=utf-8 -*-

import base64
import json
import time

from constants import PHONETYPE_CHINAMOBILE, PHONETYPE_CHINAUNION
from payv4_helper import PayHelperV4
from payv4_yipay_base import TuYouPayYiBase
from tyframework.context import TyContext
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay_common.clientrevision import ClientRevision

create_errmsg = {
    '10000': '系统异常',
    '10002': '请求参数异常',
    '10005': '未知数据异常',
    '20901': '请求运营商返回无效结果',
    '20902': '短信验证码错误',
    '20903': '手机号被运营商锁定',
    '20904': '发送验证码失败',
    '20905': '手机号超过日消费限额',
    '20906': '手机号超过月消费限额',
    '20907': '用户名超过日消费限额',
    '20908': '用户名超过月消费限额',
    '20909': '同一设备为不同账号充值超过上限',
    '20910': '同一手机号为不同用户充值超过上限',
    '20911': '同一个手机号为不同用户充值超过上限',
    '20912': '手机号余额不足',
    '20913': 'MD5签名校验失败',
    '20915': '黑名单用户',
}


class TuYouPayYiV4(TuYouPayYiBase):
    # merc_id = '2000024'
    # yipay_appid = '5969fac8a69c11e49758c6a10b512583'
    # yipay_key = 'fda8c042c87f2fdb031110c9eadc8dec'
    # createorder_url = 'http://fee.aiyuedu.cn:23000/sdkfee/api2/create_order'

    @payv4_order("yisdk")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        yiconfig = TyContext.Configure.get_global_item_json('yipay_config', {})
        cls.merc_id = str(yiconfig['merc_id'])
        cls.yipay_appid = str(yiconfig['app_id'])
        cls.yipay_key = str(yiconfig['yipay_key'])
        cls.createorder_url = str(yiconfig['createorder_url'])

        userId = chargeinfo['uid']
        appId = chargeinfo['appId']
        phoneType = TyContext.UserSession.get_phone_type_name(chargeinfo['phoneType'])
        buttonId = chargeinfo['buttonId']
        price = int(float(chargeinfo['chargeTotal'])) * 100
        platformOrderId = chargeinfo['platformOrderId']
        if buttonId in yiconfig['monthly_prods']:
            is_monthly = '2'
        else:
            is_monthly = '0'
        response = cls._create_order(phoneType, userId, price, platformOrderId, is_monthly)
        status = response['status']
        msg = create_errmsg.get(status, response['msg'])
        if int(status) != 0:
            TyContext.ftlog.error('TuYouPayYi create_order failed for user', userId,
                                  'orderid', platformOrderId, 'status', status, 'msg', msg)
            chargeinfo['chargeData'] = {}
            return cls.return_mo(1, chargeInfo=chargeinfo)
        res = response['res']
        sep = res.get('sms_separator', '@@@')
        sms_count = int(res['sms_count'])
        sms_count = sms_count if sms_count > 1 else 1  # 0/1 is 1
        sms_msg = base64.decodestring(res['sms_msg'])
        spnumber = res['spnumber']
        sms_interval = res.get('sms_interval', 1)
        if not sms_interval:
            sms_interval = 1000
        else:
            sms_interval = int(sms_interval) * 1000
        if sms_count > 1:
            sms_msgs = sms_msg.split(sep)
            spnumbers = spnumber.split(sep)
        else:
            sms_msgs = (sms_msg,)
            spnumbers = (spnumber,)

        if not ClientRevision(userId).support_type0_smspayinfo:
            if sms_count > 2:
                return cls.return_mo(0, chargeInfo=chargeinfo)
            elif sms_count == 2:
                payinfo = SmsPayInfo.getSmsPayInfo(3, sms_msgs[0], spnumbers[0],
                                                   sms_msgs[1], spnumbers[1])
            elif sms_count == 1:
                payinfo = SmsPayInfo.getSmsPayInfo(1, sms_msg, spnumber)
            chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
            return cls.return_mo(0, chargeInfo=chargeinfo)

        messages = []
        for i in xrange(sms_count):
            messages.append((spnumbers[i], sms_msgs[i], sms_interval))
        no_hint = chargeinfo.get('nohint', None)
        payinfo = SmsPayInfo.build_sms_payinfo(messages, nohint=no_hint)
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    def _create_order(cls, phoneType, userId, amount, orderPlatformId, is_monthly):
        yiconfig = TyContext.Configure.get_global_item_json('yipay_config', {})
        iccid = TyContext.UserSession.get_session_iccid(userId)
        imei = TyContext.UserSession.get_session_imei(userId)
        imsi = TyContext.UserSession.get_session_imsi(userId)
        params = {}
        if phoneType == PHONETYPE_CHINAMOBILE:
            params['corp_type'] = '1'
        elif phoneType == PHONETYPE_CHINAUNION:
            params['corp_type'] = '2'
        else:
            params['corp_type'] = '3'

        params['merc_id'] = cls.merc_id
        params['amount'] = str(amount)
        if iccid:
            params['iccid'] = iccid
        if imei:
            params['imei'] = imei
        if imsi:
            params['imsi'] = imsi
        params['user_id'] = userId
        params['app_id'] = cls.yipay_appid
        params['site_type'] = '3'
        params['scheme'] = '3'
        params['ver'] = '2.0'

        params['pay_code'] = yiconfig['paycode_config'][str(amount / 100)]
        # 0非包月, 2包月
        params['is_monthly'] = is_monthly

        notifyurl = PayHelperV4.getSdkDomain() + '/v1/pay/yipay/callback'
        params['app_orderid'] = orderPlatformId
        params['ip'] = TyContext.RunHttp.get_client_ip()
        params['noti_url'] = notifyurl
        params['time'] = str(int(time.time()))
        params['sign'] = cls._cal_sign(params)
        response_msg, final_url = TyContext.WebPage.webget(cls.createorder_url, params)

        response = json.loads(response_msg)
        return response

    @payv4_callback("/ve/pay/yipay/callback")
    def doYiPayCallback(self, rpath):
        return self.do_yipay_callback('yipay')
