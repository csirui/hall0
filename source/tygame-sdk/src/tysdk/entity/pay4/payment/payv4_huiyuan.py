# -*- coding=utf-8 -*-
#################################################
# 会员订阅获取短信内容和支付结果回掉的主要逻辑实现
# 目前接入的运营商有：移动，联通和电信
# Created by Zhang Shibo at 2015/10/15
#################################################

import json
import re
import time
import traceback
from hashlib import md5

import datetime

from payv4_helper import PayHelperV4
from tyframework._private_.util.iccid_loc_new import IccidLoc
from tyframework.context import TyContext
from tysdk.cmdcenter.httpgateway import HttpGateWay
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay_common.clientrevision import ClientRevision
from tysdk.entity.pay_common.orderlog import Order

liantongerrmsg = {
    '2': '成功',
    '1': '计费失败',
    '20': '延时计费',
    '9020': '用户主动退订(仅针对包月用户)',
    '9021': '无该用户某个产品的当月包的包月扣费信息(仅针对包月用户)或包月已失效',
    '50': '不支持该号段',
    '52': '访问认证失败',
    '53': '产品不存在',
    '54': '验证码无效',
    '55': '数据签名错误',
    '56': '风控限制',
    '57': '访问频率限制',
    '605': '超过当天扣费限额。',
    '606': '超过当月扣费限额。',
    '607': '扣费失败。',
    '608': '因用户余额不足，扣费失败。',
    '611': '必选参数不能为空。',
    '01003': '订购用户欠费，预付费用户计费失败',
    '01099': '其他错误',
    '03101': '用户余额不足',
    '91006': '消费超过限额',
    '91011': '产品使用未过期(包月)',
    '91022': '当月已经成功订购过某包月产品',
    '91023': '未录入短信模板'
}


class TuYouPayHuiYuanBaoYueV4(PayBaseV4):
    @payv4_order('huiyuan')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        userId, platformOrderId, phoneType = chargeinfo['uid'], chargeinfo['platformOrderId'], chargeinfo['phoneType']
        shortOrderId = ShortOrderIdMap.get_short_order_id(platformOrderId)
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->charge_data platformOrderId:[%s] and shortOrderId:[%s]' % (
        platformOrderId, shortOrderId))
        phoneType = TyContext.UserSession.get_phone_type_name(phoneType)
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->charge_data phoneType:[%s].' % phoneType)
        reportBiParams = {}
        reportBiParams['platformOrderId'] = platformOrderId
        reportBiParams['userId'] = userId
        reportBiParams['appId'] = chargeinfo['appId']
        reportBiParams['mobile'] = 'na'
        reportBiParams['clientId'] = chargeinfo['clientId']
        reportBiParams['productId'] = chargeinfo.get('diamondId',
                                                     chargeinfo.get('buttonId', chargeinfo.get('prodId', 'na')))
        reportBiParams['payType'] = chargeinfo.get('chargeType', 'na')

        if 0 == cmp(phoneType, 'chinaMobile'):
            iccid = TyContext.UserSession.get_session_iccid(userId)
            citycode = self.getCityCode(iccid)
            if citycode == 1:
                self.chargeDataErrorMsg(chargeinfo, shortOrderId, citycode)
                return self.return_mo(0, chargeInfo=chargeinfo)
            elif citycode == 2:
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->charge_data User client not support Monthly VIP, iccid: [%s]' % iccid)
                self.reportBi(Order.CLIENT_CANCELED, reportBiParams)
                self.chargeDataErrorMsg(chargeinfo, shortOrderId, citycode)
                return self.return_mo(0, chargeInfo=chargeinfo)
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->charge_data citycode:[%s].' % citycode)
            smsConfigInfo = TyContext.Configure.get_global_item_json('chinaMobile_monthly_smsContent', {})
            smsInfo = smsConfigInfo.get(str(citycode), None)
            if not smsInfo:
                self.chargeDataErrorMsg(chargeinfo, shortOrderId, 2)
                self.reportBi(Order.CLIENT_CANCELED, reportBiParams)
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->charge_data User client not support Monthly VIP, iccid: [%s]' % iccid)
                return self.return_mo(0, chargeInfo=chargeinfo)
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->charge_data smsInfo is: ', smsInfo)
            sms_msg, spnumber = smsInfo['subscribe']
            autoReplyMsg = smsInfo['auto_reply']
            unsub_sms_msg, unsub_spnumber = smsInfo['unsubscribe']
            TyContext.ftlog.debug(
                'TuYouPayHuiYuanBaoYue->charge_data sms_msg:[%s] and spnumber:[%s] and antuReplyMsg:[%s].' % (
                sms_msg, spnumber, autoReplyMsg))
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->charge_data unsub_sms_msg:[%s] and unsub_spnumber:[%s].' % (
            unsub_sms_msg, unsub_spnumber))
            TyContext.RedisPayData.execute('SET', 'unsubMonthlySmsInfo:' + str(userId),
                                           self.getUnsubscribeSms(unsub_sms_msg, unsub_spnumber))

            # 获取自动回复功能的短信监听内容
            autoReplyListenContent = TyContext.Configure.get_global_item_json(
                'monthly_vip_sms_auto_reply_listen_content', {})
            listenContent = autoReplyListenContent[phoneType]
            messageContent = [autoReplyMsg, ""]
            messageContent += listenContent

            monthlyVipParams = TyContext.Configure.get_global_item_json('monthly_vip_params', {})
            orderIdPhonenum = monthlyVipParams['orderIdPhonenum']
            order_sms_msg = '1125ty' + shortOrderId
            messages = []
            message1 = (orderIdPhonenum, order_sms_msg, 0)
            message2 = (spnumber, sms_msg, 0)
            message3 = ('', '', -1, messageContent)
            messages.append(message1)
            messages.append(message2)
            messages.append(message3)
            if not ClientRevision(userId).support_type0_smspayinfo:
                payinfo = SmsPayInfo.getSmsPayInfo(5, order_sms_msg, orderIdPhonenum, sms_msg, spnumber)
                chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
                return self.return_mo(0, chargeInfo=chargeinfo)
            no_hint = chargeinfo.get('nohint', None)
            payinfo = {'messages': messages}
            payinfo['support'] = 'true'
            if no_hint:
                payinfo['nohint'] = no_hint
            SmsPayInfo.fill_in_dialog_text(
                payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
            chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
            return self.return_mo(0, chargeInfo=chargeinfo)

        elif 0 == cmp(phoneType, 'chinaUnion'):
            iccid = TyContext.UserSession.get_session_iccid(userId)
            citycode = self.getChinaUnionCityCode(iccid)
            if citycode == 1:
                self.chargeDataErrorMsg(chargeinfo, shortOrderId, citycode)
                return self.return_mo(0, chargeInfo=chargeinfo)
            elif citycode == 2:
                self.reportBi(Order.CLIENT_CANCELED, reportBiParams)
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->charge_data User client not support Monthly VIP, iccid [%s]' % iccid)
                self.chargeDataErrorMsg(chargeinfo, shortOrderId, citycode)
                return self.return_mo(0, chargeInfo=chargeinfo)
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->charge_data citycode:[%s].' % citycode)
            smsConfigInfo = TyContext.Configure.get_global_item_json('chinaUnion_monthly_smsContent', {})
            smsInfo = smsConfigInfo.get(str(citycode), None)
            if not smsInfo:
                self.chargeDataErrorMsg(chargeinfo, shortOrderId, 2)
                self.reportBi(Order.CLIENT_CANCELED, reportBiParams)
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->charge_data User client not support Monthly VIP, iccid: [%s]' % iccid)
                return self.return_mo(0, chargeInfo=chargeinfo)
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->charge_data smsInfo is: ', smsInfo)
            sms_msg, spnumber = smsInfo['subscribe']
            autoReplyMsg = smsInfo['auto_reply']
            unsub_sms_msg, unsub_spnumber = smsInfo['unsubscribe']
            TyContext.ftlog.debug(
                'TuYouPayHuiYuanBaoYue->charge_data sms_msg:[%s] and spnumber:[%s] and antuReplyMsg:[%s].' % (
                sms_msg, spnumber, autoReplyMsg))

            # 获取自动回复功能的短信监听内容
            autoReplyListenContent = TyContext.Configure.get_global_item_json(
                'monthly_vip_sms_auto_reply_listen_content', {})
            listenContent = autoReplyListenContent[phoneType]
            messageContent = [autoReplyMsg, ""]
            messageContent += listenContent

            sms_msg = sms_msg + '_' + shortOrderId
            messages = []
            message1 = (spnumber, sms_msg, 0)
            message2 = ('', '', -1, messageContent)
            messages.append(message1)
            messages.append(message2)

        elif 0 == cmp(phoneType, 'chinaTelecom'):
            smsConfigInfo = TyContext.Configure.get_global_item_json('chinaTelecom_monthly_smsContent', {})
            sms_msg, spnumber = smsConfigInfo['subscribe']
            autoReplyMsg = smsConfigInfo['auto_reply']
            unsub_sms_msg, unsub_spnumber = smsConfigInfo['unsubscribe']
            TyContext.ftlog.debug(
                'TuYouPayHuiYuanBaoYue->charge_data sms_msg:[%s] and spnumber:[%s] and antuReplyMsg:[%s].' % (
                sms_msg, spnumber, autoReplyMsg))

            # 获取自动回复功能的短信监听内容
            autoReplyListenContent = TyContext.Configure.get_global_item_json(
                'monthly_vip_sms_auto_reply_listen_content', {})
            listenContent = autoReplyListenContent[phoneType]
            messageContent = [autoReplyMsg, ""]
            messageContent += listenContent

            sms_msg = sms_msg + '_' + shortOrderId
            messages = []
            message1 = (spnumber, sms_msg, 0)
            message2 = ('', '', -1, messageContent)
            messages.append(message1)
            messages.append(message2)

        else:
            self.chargeDataErrorMsg(chargeinfo, shortOrderId, 1)
            return self.return_mo(0, chargeInfo=chargeinfo)

        # 联通和电信会走该逻辑
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->charge_data unsub_sms_msg:[%s] and unsub_spnumber:[%s].' % (
        unsub_sms_msg, unsub_spnumber))
        TyContext.RedisPayData.execute('SET', 'unsubMonthlySmsInfo:' + str(userId),
                                       self.getUnsubscribeSms(unsub_sms_msg, unsub_spnumber))
        if not ClientRevision(userId).support_type0_smspayinfo:
            payinfo = SmsPayInfo.getSmsPayInfo(1, sms_msg, spnumber)
            chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
            return self.return_mo(0, chargeInfo=chargeinfo)
        no_hint = chargeinfo.get('nohint', None)
        payinfo = {'messages': messages}
        payinfo['support'] = 'true'
        if no_hint:
            payinfo['nohint'] = no_hint
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/vipchinaunion/callback')
    def doChinaUnionMonthlycallback(cls, rpath):
        urlParam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback Url params is:', urlParam)
        try:
            orderid = urlParam['orderid']
            mobile = urlParam['mobile']
            smscontext = urlParam['smscontext']
            status = urlParam['status']
            signature = urlParam['signature']
            prodcode = urlParam['prodcode']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback ERROR: ', e)
            return 'fail'
        monthlyVipParams = TyContext.Configure.get_global_item_json('monthly_vip_params', {})
        key = monthlyVipParams['key']
        checkstr = orderid + mobile + key
        if not cls.checkSignature(checkstr, signature):
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback sign failed.')
            return 'fail'

        orderId = ['']
        if status == '2':
            param = cls.getUserInfo(smscontext, mobile, False, orderId)
        else:
            param = cls.getUserInfo(smscontext, mobile, True, orderId, 'chinaUnion')
        if not param:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback ERROR'
                                  ' Get platformOrderId or uid by phonenum [%s] failed.' % mobile)
            rtnParam = {}
            rtnParam['platformOrderId'] = orderId[0]
            rtnParam['errorcode'] = status
            rtnParam['errormsg'] = liantongerrmsg[status]
            cls.userSubscribeFailed(rtnParam)
            return 'fail'

        if 0 == TyContext.MySqlSwap.checkUserDate(param['userId']):
            TyContext.ftlog.error(
                'TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback get cold userId {userId} failed.'.format(
                    userId=param['userId']))
            return 'fail'

        if status == '20':
            # 订阅成功:20是用户首次订阅72小时之内，延时计费
            param['third_orderid'] = orderid
            userInfoStatus = cls.getUserInfoStatus('vipuser:' + mobile)
            if 0 != cmp(userInfoStatus, 'success'):
                param['message'] = cls.getUnsubscribeMessage('chinaUnion', param['userId'], mobile)
                cls.notifyGameServerDelivery(param)
                cls.reportBi(Order.SUBSCRIBE, param, 'ChinaUnion charge info')
            else:
                # 次月收费
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback [ChinaUnion charge info : %s]' % cls.getLogUserInfo(
                        param))
                cls.reportBi(Order.RENEW_SUBSCRIBE, param, 'ChinaUnion charge info')
            return 'ok'
        elif status == '2':
            # 订阅成功，并开始扣费 或者停机后再次扣费成功，将redis中用户vip信息置为是，标记用户会员恢复
            TyContext.RedisUser.execute(param['userId'], 'HSET', 'user:' + str(param['userId']), 'isYouyifuVipUser',
                                        '1')
            cls.reportBi(Order.RENEW_SUBSCRIBE, param, 'ChinaUnion charge info')
            TyContext.ftlog.info(
                'TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback [ChinaUnion charge info : %s]' % cls.getLogUserInfo(
                    param))
            return 'ok'
        elif status == '9020':
            # 退订
            if not cls.notifyGameServerUserUnsubscribe(param):
                TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback ERROR Notify Game server '
                                      ' User[%s, mobile:%s] unsubscribed ERROR!' % (param['userId'], mobile))
                return 'fail'
            return 'ok'
        elif status == '1' or status == '607' or status == '608' or status == '03101':
            # 停机，将redis中用户vip信息置为否，标记用户会员暂停
            TyContext.RedisUser.execute(param['userId'], 'HSET', 'user:' + str(param['userId']), 'isYouyifuVipUser',
                                        '0')
            TyContext.ftlog.info(
                'TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback [ChinaUnion halt info : %s]' % cls.getLogUserInfo(
                    param))
            cls.reportBi(Order.OUTOFSERVICE, param, 'ChinaUnion charge info')
            return 'ok'
        else:
            # 订阅失败
            # 注:这里修改状态是因为不确定联通扣费失败是按哪种方式通知的。
            TyContext.RedisUser.execute(param['userId'], 'HSET', 'user:' + str(param['userId']), 'isYouyifuVipUser',
                                        '0')

            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback User[%s, mobile:%s, orderid:%s] '
                                  'subscribe mothly vip failed.' % (
                                  param['userId'], mobile, param.get('platformOrderId', '')))
            param['errorcode'] = status
            param['errormsg'] = liantongerrmsg[status]
            cls.userSubscribeFailed(param)
            return 'fail'

    @payv4_callback('/open/ve/pay/vipchinamobile/callback')
    def doChinaMobileMonthlycallback(cls, rpath):
        urlParam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback Url params is:', urlParam)
        try:
            usernumber = urlParam['usernumber']
            orderstate = urlParam['orderstate']
            msg = urlParam['msg']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback ERROR: ', e)
            return 'fail'
        orderId = ['']
        param = cls.getUserInfo(msg, usernumber, True, orderId)
        if not param:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback ERROR'
                                  ' Get platformOrderId or uid by phonenum [%s] failed.' % usernumber)
            rtnParam = {}
            rtnParam['platformOrderId'] = orderId[0]
            rtnParam['errorcode'] = orderstate
            rtnParam['errormsg'] = '重复订阅'
            cls.userSubscribeFailed(rtnParam)
            return 'fail'

        if 0 == TyContext.MySqlSwap.checkUserDate(param['userId']):
            TyContext.ftlog.error(
                'TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback get cold userId {userId} failed.'.format(
                    userId=param['userId']))
            return 'fail'

        if orderstate == '1':
            # 订阅成功
            retValue = TyContext.RedisPayData.execute('SISMEMBER', '10yuanMonthlyVipMobile', param['mobile'])
            if int(retValue) == 1:
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback [ChinaMobile charge info (first time) : %s]' % cls.getLogUserInfo(
                        param))
            else:
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback [ChinaMobile charge info : %s]' % cls.getLogUserInfo(
                        param))
            userInfoStatus = cls.getUserInfoStatus('vipuser:' + usernumber)
            if 0 != cmp(userInfoStatus, 'success'):
                param['message'] = cls.getUnsubscribeMessage('chinaMobile', param['userId'], usernumber)
                cls.notifyGameServerDelivery(param)
                cls.reportBi(Order.SUBSCRIBE, param, 'ChinaMobile charge info')
            else:
                # 次月收费
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback [ChinaMobile charge info : %s]' % cls.getLogUserInfo(
                        param))
                cls.reportBi(Order.RENEW_SUBSCRIBE, param, 'ChinaMobile charge info')
            return 'ok'
        elif orderstate == '0':
            # 退订
            if not cls.notifyGameServerUserUnsubscribe(param):
                TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback ERROR Notify Game server '
                                      ' User[%s, mobile:%s] unsubscribed ERROR!' % (param['userId'], usernumber))
                return 'fail'
            return 'ok'
        elif orderstate == '2':
            # 停机，将redis中用户vip信息置为否，标记用户会员暂停
            TyContext.RedisUser.execute(param['userId'], 'HSET', 'user:' + str(param['userId']), 'isYouyifuVipUser',
                                        '0')
            TyContext.ftlog.info(
                'TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback [ChinaMobile halt info : %s]' % cls.getLogUserInfo(
                    param))
            cls.reportBi(Order.OUTOFSERVICE, param, 'ChinaMobile charge info')
            return 'ok'
        elif orderstate == '3':
            # 复机，将redis中用户vip信息置为是，标记用户会员恢复
            TyContext.RedisUser.execute(param['userId'], 'HSET', 'user:' + str(param['userId']), 'isYouyifuVipUser',
                                        '1')
            TyContext.ftlog.info(
                'TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback [ChinaMobile active info : %s]' % cls.getLogUserInfo(
                    param))
            return 'ok'
        else:
            TyContext.ftlog.error(
                'TuYouPayHuiYuanBaoYue->doChinaMobileMonthlycallback ERROR orderstate [%s] doesn\'t exist.' % orderstate)
            return 'fail'

    @payv4_callback('/open/ve/pay/viptelecom/callback1')
    def doChinaTelecomMonthlycallback1(cls, rpath):
        urlParam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback1 Url params is:', urlParam)
        try:
            productid = urlParam['productid']
            mobile = urlParam['mobile']
            mo = urlParam['mo']
            timestr = urlParam['timestr']
            signature = urlParam['signature']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback1 ERROR: ', e)
            return 'fail'
        monthlyVipParams = TyContext.Configure.get_global_item_json('monthly_vip_params', {})
        key = monthlyVipParams['key']
        checkstr = productid + mobile + timestr + key
        if not cls.checkSignature(checkstr, signature):
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback1 sign failed.')
            return 'fail'

        orderId = ['']
        param = cls.getUserInfo(mo, mobile, True, orderId, 'chinaTelecom')
        if not param:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback1 ERROR'
                                  ' Get platformOrderId or uid by phonenum [%s] failed.' % mobile)
            rtnParam = {}
            rtnParam['platformOrderId'] = orderId[0]
            rtnParam['errorcode'] = 'RD'
            rtnParam['errormsg'] = '重复订阅'
            cls.userSubscribeFailed(rtnParam)
            return 'fail'
        TyContext.ftlog.info(
            'TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback1 Phonenum mapping to OrderId successed!.[%s]',
            cls.getLogUserInfo(param))
        return 'ok'

    @payv4_callback('/open/ve/pay/viptelecom/callback2')
    def doChinaTelecomMonthlycallback2(cls, rpath):
        urlParam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 Url params is:', urlParam)
        try:
            productid = urlParam['productid']
            mobile = urlParam['mobile']
            timestr = urlParam['timestr']
            orderstate = urlParam['orderstate']
            reason = urlParam['reason']
            signature = urlParam['signature']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 ERROR: ', e)
            return 'fail'
        monthlyVipParams = TyContext.Configure.get_global_item_json('monthly_vip_params', {})
        key = monthlyVipParams['key']
        checkstr = productid + mobile + timestr + key
        if not cls.checkSignature(checkstr, signature):
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 sign failed.')
            return 'fail'
        orderId = ['']
        param = cls.getUserInfo(reason, mobile, False, orderId)
        if not param:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 ERROR'
                                  ' Get platformOrderId or uid by phonenum [%s] failed.' % mobile)
            return 'fail'

        if 0 == TyContext.MySqlSwap.checkUserDate(param['userId']):
            TyContext.ftlog.error(
                'TuYouPayHuiYuanBaoYue->doChinaUnionMonthlycallback get cold userId {userId} failed.'.format(
                    userId=param['userId']))
            return 'fail'

        if orderstate == 'RD':
            # 订阅成功
            userInfoStatus = cls.getUserInfoStatus('vipuser:' + mobile)
            if 0 != cmp(userInfoStatus, 'success'):
                param['message'] = cls.getUnsubscribeMessage('chinaTelecom', param['userId'], mobile)
                cls.notifyGameServerDelivery(param)
                cls.reportBi(Order.SUBSCRIBE, param, 'chinaTelecom charge info')
            else:
                # 次月收费
                TyContext.ftlog.info(
                    'TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 [chinaTelecom charge info : %s]' % cls.getLogUserInfo(
                        param))
                cls.reportBi(Order.RENEW_SUBSCRIBE, param, 'chinaTelecom charge info')
            return 'ok'
        elif orderstate == 'CD':
            # 退订
            if not cls.notifyGameServerUserUnsubscribe(param):
                TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 ERROR Notify Game server '
                                      ' User[%s, mobile:%s] unsubscribed ERROR!' % (param['userId'], mobile))
                return 'fail'
            return 'ok'
        elif orderstate == 'AD':
            # 复机，将redis中用户vip信息置为是，标记用户会员恢复
            TyContext.RedisUser.execute(param['userId'], 'HSET', 'user:' + str(param['userId']), 'isYouyifuVipUser',
                                        '1')
            TyContext.ftlog.info(
                'TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 [ChinaTelecom active info : %s]' % cls.getLogUserInfo(
                    param))
            return 'ok'
        elif orderstate == 'PD':
            # 停机，将redis中用户vip信息置为否，标记用户会员暂停
            TyContext.RedisUser.execute(param['userId'], 'HSET', 'user:' + str(param['userId']), 'isYouyifuVipUser',
                                        '0')
            TyContext.ftlog.info(
                'TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 [ChinaTelecom halt info : %s]' % cls.getLogUserInfo(
                    param))
            cls.reportBi(Order.OUTOFSERVICE, param, 'ChinaTelecom charge info')
            return 'ok'
        else:
            TyContext.ftlog.error(
                'TuYouPayHuiYuanBaoYue->doChinaTelecomMonthlycallback2 ERROR orderstate [%s] doesn\'t exist.' % orderstate)
            return 'fail'

    @payv4_callback('/open/ve/pay/vipmobiletoorder/callback')
    def doGetPhonenumToOrdercallback(cls, rpath):
        urlParam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->doGetPhonenumToOrdercallback Url params is:', urlParam)
        try:
            mo = urlParam['mo']
            recvtime = urlParam['recvtime']
            mobile = urlParam['mobile']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doGetPhonenumToOrdercallback ERROR: ', e)
            return 'fail'
        signature = urlParam.get('signature', None)
        monthlyVipParams = TyContext.Configure.get_global_item_json('monthly_vip_params', {})
        key = monthlyVipParams['key']
        checkstr = mobile + mo + recvtime + key
        if signature and not cls.checkSignature(checkstr, signature):
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doGetPhonenumToOrdercallback sign failed.')
            return 'fail'
        orderId = ['']
        param = cls.getUserInfo(mo, mobile, True, orderId, 'chinaMobile')
        if not param:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->doGetPhonenumToOrdercallback ERROR'
                                  ' Get platformOrderId or uid by phonenum [%s] failed.' % mobile)
            return 'fail'
        TyContext.ftlog.info(
            'TuYouPayHuiYuanBaoYue->doGetPhonenumToOrdercallback Phonenum mapping to OrderId successed!.[%s]',
            cls.getLogUserInfo(param))
        return 'success'

    def getChinaUnionCityCode(cls, iccid):
        if not iccid:
            return 1
        if iccid[:4] != '8986' or \
                not re.match('^[0-9a-fA-F]{9,30}$', iccid):
            return 2

        _operator = '01'
        iccidLoc = IccidLoc()
        try:
            # 先判断10，11两位
            provid = iccid[9:11]
            if provid in iccidLoc.iccid2prov_map[_operator]:
                cityCode = iccidLoc.prov2pc_map[iccidLoc.iccid2prov_map[_operator][provid]]
                return cityCode * 10000

            _operator = '03'
            # 再判断11，12，13三位
            provid = iccid[10:13]
            if provid in iccidLoc.iccid2prov_map[_operator]:
                cityCode = iccidLoc.prov2pc_map[iccidLoc.iccid2prov_map[_operator][provid]]
                return cityCode * 10000

            _operator = '01'
            # 再判断11，12两位
            provid = iccid[10:12]
            if provid in iccidLoc.iccid2prov_map[_operator]:
                cityCode = iccidLoc.prov2pc_map[iccidLoc.iccid2prov_map[_operator][provid]]
                return cityCode * 10000
        except Exception as e:
            return 2
        return 2

    def getCityCode(cls, iccid):
        if not iccid:
            return 1
        iccidLoc = IccidLoc()
        citycode = iccidLoc.get_provid(iccid)
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getCityCode iccid is:[%s] citycode is: [%s]' % (iccid, citycode))
        if citycode > 0:
            citycode *= 10000
            return citycode
        else:
            return 2

    def chargeDataErrorMsg(cls, chargeinfo, shortOrderId, errorCode):
        errorInfo = TyContext.Configure.get_global_item_json('monthly_vip_subscribe_error_info', {})
        sms_msg = '_' + shortOrderId
        spnumber = ''
        if not ClientRevision(chargeinfo['uid']).support_type0_smspayinfo:
            payinfo = SmsPayInfo.getSmsPayInfo(1, sms_msg, spnumber)
            chargeinfo['chargeData'] = {'smsPayinfo': payinfo}
            return
        messages = [(spnumber, sms_msg, 0)]
        payinfo = {'messages': messages}
        no_hint = chargeinfo.get('nohint', None)
        if no_hint:
            payinfo['nohint'] = no_hint
        payinfo['text1'] = errorInfo[str(errorCode)]
        payinfo['text2'] = errorInfo['0']
        payinfo['support'] = 'false'
        monthlyVipParams = TyContext.Configure.get_global_item_json('monthly_vip_params', {})
        payinfo['alternativeProdId'] = monthlyVipParams['alternativeProdId']
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}

    def getUnsubscribeMessage(cls, operator, userId, mobile):
        smsInfo = TyContext.RedisPayData.execute('GET', 'unsubMonthlySmsInfo:' + str(userId))
        if smsInfo:
            TyContext.RedisPayData.execute('DEL', 'unsubMonthlySmsInfo:' + str(userId))
            return smsInfo
        iccid = TyContext.UserSession.get_session_iccid(userId)
        try:
            if 0 == cmp(operator, 'chinaMobile'):
                citycode = cls.getCityCode(iccid)
                TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getUnsubscribeMessage citycode:[%s].' % citycode)
                smsConfigInfo = TyContext.Configure.get_global_item_json('chinaMobile_monthly_smsContent', {})
                smsInfo = smsConfigInfo.get(str(citycode), None)
                sms_msg, spnumber = smsInfo['unsubscribe']
            elif 0 == cmp(operator, 'chinaUnion'):
                citycode = cls.getChinaUnionCityCode(iccid)
                TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getUnsubscribeMessage citycode:[%s].' % citycode)
                smsConfigInfo = TyContext.Configure.get_global_item_json('chinaUnion_monthly_smsContent', {})
                smsInfo = smsConfigInfo.get(str(citycode), None)
                sms_msg, spnumber = smsInfo['unsubscribe']
            else:
                smsConfigInfo = TyContext.Configure.get_global_item_json('chinaTelecom_monthly_smsContent', {})
                sms_msg, spnumber = smsConfigInfo['unsubscribe']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->getUnsubscribeMessage ERROR', e,
                                  ' iccid: [%s], mobile: [%s], userId: [%s]' % (iccid, mobile, userId))
            return '请联系客服4008-098-000退订'
        return cls.getUnsubscribeSms(sms_msg, spnumber)

    def getUnsubscribeSms(cls, sms, port):
        return '退订请编辑短信' + sms + '到' + port

    def reportBi(cls, eventId, params, infomation='na'):
        Order.log(params['platformOrderId'], eventId, params['userId'],
                  params['appId'], params['clientId'], info=infomation,
                  paytype=params['payType'], diamondid=params['productId'],
                  mobile=params['mobile']
                  )

    def checkSignature(cls, checkstr, sign):
        signcalc = md5(checkstr).hexdigest().lower()
        TyContext.ftlog.debug('calculate sign is: [%s], excepted sign is: [%s].' % (signcalc, sign))
        if 0 != cmp(signcalc, sign.lower()):
            return False
        return True

    def getLogUserInfo(cls, rparam):
        return '[User:%s, mobile:%s, phoneType:%s, orderid:%s, appId:%s, clientId:%s, total_fee:%s, time:%s]' \
               % (rparam['userId'], rparam['mobile'], rparam['phoneType'], rparam['platformOrderId'], rparam['appId'],
                  rparam['clientId'], rparam['total_fee'], datetime.datetime.now())

    def getChargeInfo(cls, platformOrderId, mobile):
        chargeKey = 'sdk.charge:' + platformOrderId
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getChargeInfo Redis key: ', chargeKey)
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getChargeInfo old chargeInfo: ', chargeInfo)

        # 将用户包月的电话号码写入chargeInfo
        chargeInfo['vouchMobile'] = mobile
        chargeInfo_dumps = json.dumps(chargeInfo)
        TyContext.RedisPayData.execute('HSET', chargeKey, 'charge', chargeInfo_dumps)
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->notifyGameServerDelivery Updated chargeInfo: ', chargeInfo_dumps)
        return chargeInfo

    def getUserInfo(cls, smsContent, mobile, status, OrderId, phoneType='na'):
        # 只有当用户订阅的时候，smsContent中才有可能会有订单号，是在_或者ty后面
        redisKey = 'vipuser:' + mobile
        TyContext.ftlog.info('TuYouPayHuiYuanBaoYue->getUserInfo status is:[%s] redisKey is:[%s].' % (status, redisKey))

        # 联通和电信用户订阅时，由客户端发送的短信息，含有_订单号；移动用户订阅时，由客户端发短信，第三方回掉，含有ty订单号
        # 第一层控制，通过status，让特定的情况修改redis
        if status and ('_' in smsContent or 'ty' in smsContent):
            if '_' in smsContent:
                shortOrderId = smsContent.split('_')[1]
            else:
                shortOrderId = smsContent.split('ty')[1]

            # 第二层控制，判断短订单号是否和之前的相同
            if HttpGateWay.isShortOrderIdSame(mobile, shortOrderId):
                return HttpGateWay.getUserInfoParam(mobile)

            OrderId[0] = platformOrderId = ShortOrderIdMap.get_long_order_id(shortOrderId)
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getUserInfo shortOrderId : [%s], platformOrderId :[%s]'
                                  % (shortOrderId, platformOrderId))

            retValue = TyContext.RedisPayData.execute('EXISTS', redisKey)
            if int(retValue) == 1:
                UserInfostatus = cls.getUserInfoStatus(redisKey)
                # 第三层控制，判断之前的订单是否是成功的
                if 0 == cmp(UserInfostatus, 'success'):
                    TyContext.ftlog.error(
                        'TuYouPayHuiYuanBaoYue->getUserInfo Mobile [%s] has already bind to somebody already. ' % mobile)
                    return None

            # 程序能走到这里，只有含有订单号信息的回调、无绑定记录的电话号码、之前绑定的订单号的状态是失败的，这几种情况才可以
            # 举个例子：用户重发订阅时含有订单号的短信，用户再次订阅，联通的状态为91022的回调都不会都到这儿来
            chargeInfo = cls.getChargeInfo(platformOrderId, mobile)
            if not chargeInfo:
                TyContext.ftlog.error(
                    'TuYouPayHuiYuanBaoYue->getUserInfo Doesn\'t exit chargeInfo, key is: sdk.charge:', platformOrderId)
                return None
            try:
                params = {
                    'userId': str(chargeInfo['uid']),
                    'mobile': mobile,
                    'phoneType': phoneType,
                    'iccid': TyContext.UserSession.get_session_iccid(str(chargeInfo['uid'])),
                    'platformOrderId': platformOrderId,
                    'shortOrderId': shortOrderId,
                    'productId': chargeInfo.get('diamondId',
                                                chargeInfo.get('buttonId', chargeInfo.get('prodId', 'na'))),
                    'payType': chargeInfo.get('chargeType', 'na'),
                    'total_fee': chargeInfo['chargeTotal'],
                    'appId': str(chargeInfo['appId']),
                    'clientId': chargeInfo['clientId'],
                    'subscribeTime': time.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': 'create',
                }
            except Exception, e:
                TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->getUserInfo ERROR: ', e)
                return None
            paramsStr = json.dumps(params)
            TyContext.RedisPayData.execute('SET', redisKey, paramsStr)
        else:
            # 用户退订，不含orderId
            params = HttpGateWay.getUserInfoParam(mobile)
            OrderId[0] = params['platformOrderId']
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getUserInfo params :', params)
        return params

    def changeUserInfoStatus(cls, redisKey, status):
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->changeUserInfoStatus redisKey is: ', redisKey, ' status is: ',
                              status)
        paramsStr = TyContext.RedisPayData.execute('GET', redisKey)
        try:
            params = json.loads(paramsStr)
        except Exception, e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->changeUserInfoStatus ERROR: ', e)
            return False
        params['status'] = status
        paramsStr = json.dumps(params)
        TyContext.RedisPayData.execute('SET', redisKey, paramsStr)
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->changeUserInfoStatus Change status successed.')
        return True

    def getUserInfoStatus(cls, redisKey):
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getUserInfoStatus redisKey is: ', redisKey)
        paramsStr = TyContext.RedisPayData.execute('GET', redisKey)
        try:
            params = json.loads(paramsStr)
        except Exception, e:
            TyContext.ftlog.error('TuYouPayHuiYuanBaoYue->getUserInfoStatus ERROR: ', e)
            return None
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getUserInfoStatus Get status successed.')
        return params['status']

    def getOrderStatus(cls, platformOrderId):
        chargeKey = 'sdk.charge:' + platformOrderId
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->getOrderStatus chargeKey is: ', chargeKey)
        oldState = TyContext.RedisPayData.execute('HGET', chargeKey, 'state')
        return oldState

    def isTempVipUser(cls, param):
        # 判断电话号码是否是新卡
        retValue = TyContext.RedisPayData.execute('SISMEMBER', '10yuanMonthlyVipMobile', param['mobile'])
        if int(retValue) == 1:
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->isTempVipUser user[%s] use mobile[%s] subscribed before.'
                                  % (param['userId'], param['mobile']))
            return False

        # 判断是否是超过72小时
        # 分别获取订阅的时间和取消订阅的时间
        timeBefore = param['subscribeTime']
        timeNow = time.strftime('%Y-%m-%d %H:%M:%S')
        TyContext.ftlog.debug(
            'TuYouPayHuiYuanBaoYue->isTempVipUser subcribed at:[%s], unsubscribed at:[%s]' % (timeBefore, timeNow))

        # 将时间放入时间数组中
        timeBefore = time.strptime(timeBefore, '%Y-%m-%d %H:%M:%S')
        timeNow = time.strptime(timeNow, '%Y-%m-%d %H:%M:%S')

        # 讲时间数组转为datetime类型
        timeBefore = datetime.datetime(*timeBefore[:6])
        timeNow = datetime.datetime(*timeNow[:6])

        if (timeNow - timeBefore).seconds <= (72 * 3600):
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->isTempVipUser Isn\'t Formal vip user. user[%s] mobile[%s].'
                                  % (param['userId'], param['mobile']))
            return True
        else:
            TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->isTempVipUser Is Formal vip user. user[%s] mobile[%s]'
                                  % (param['userId'], param['mobile']))
            return False

    def notifyGameServerDelivery(self, rparam):
        TyContext.ftlog.debug('TuYouPayHuiYuanBaoYue->notifyGameServerDelivery User[%s, mobile:%s, orderid:%s] '
                              'subscribe monthly vip!' % (
                              rparam['userId'], rparam['mobile'], rparam['platformOrderId']))
        TyContext.RedisUser.execute(rparam['userId'], 'HMSET', 'user:' + rparam['userId'], 'isYouyifuVipUser', '1',
                                    'youyifuVipMsg', rparam['message'])

        # 这个参数用来告诉游戏服务器，这个商品是一件会员包月商品
        rparam['isYouyifuMonthVip'] = '1'
        PayHelperV4.callback_ok(rparam['platformOrderId'], rparam['total_fee'], rparam)
        self.changeUserInfoStatus('vipuser:' + rparam['mobile'], 'success')
        TyContext.ftlog.info(
            'TuYouPayHuiYuanBaoYue->notifyGameServerDelivery %s has subscribed Monthly VIP.' % self.getLogUserInfo(
                rparam))

    def notifyGameServerUserUnsubscribe(cls, rparam):
        try:
            control = TyContext.ServerControl.findServerControl(rparam['appId'], rparam['clientId'])
            deliveryUrl = control['http'] + '/v2/game/sdk/youyifuVip/unsubscribe'
            TyContext.ftlog.debug(
                'TuYouPayHuiYuanBaoYue->notifyGameServerUserUnsubscribe deliveryUrl %s.' % deliveryUrl)
        except Exception as e:
            TyContext.ftlog.error(
                'TuYouPayHuiYuanBaoYue->notifyGameServerUserUnsubscribe Get GameServer IP ERROR! exception ', e)
            traceback.print_exc()
            return False

        parameter = {'userId': rparam['userId']}
        if cls.isTempVipUser(rparam):
            parameter['isTempVipUser'] = 1
            cls.reportBi(Order.UNSUBSCRIBE_TMP, rparam, rparam['phoneType'])
        else:
            parameter['isTempVipUser'] = 0
            cls.reportBi(Order.UNSUBSCRIBE, rparam, rparam['phoneType'])

        # 将redis中用户vip信息置为否，并通知游戏服
        TyContext.RedisUser.execute(rparam['userId'], 'HSET', 'user:' + rparam['userId'], 'isYouyifuVipUser', '0')
        response, request_url = TyContext.WebPage.webget(deliveryUrl, parameter)
        if 0 != cmp(response, 'success'):
            TyContext.ftlog.error(
                'TuYouPayHuiYuanBaoYue->notifyGameServerUserUnsubscribe Notify game server User[%s, mobile:%s, orderid:%s] '
                'has unsubscribed Monthly VIP ERROR.' % (rparam['userId'], rparam['mobile'], rparam['platformOrderId']))
            return False
        if 1 == parameter['isTempVipUser']:
            TyContext.ftlog.info(
                'TuYouPayHuiYuanBaoYue->notifyGameServerUserUnsubscribe %s has unsubscribed Monthly VIP'
                ' Which during the 72 hours probation period.' % cls.getLogUserInfo(rparam))
        else:
            TyContext.ftlog.info(
                'TuYouPayHuiYuanBaoYue->notifyGameServerUserUnsubscribe %s has unsubscribed Monthly VIP.' % cls.getLogUserInfo(
                    rparam))

        # 将用户电话号码与uid的对应关系删除，将该号码标记为不能使用72小时免费会员的号码
        TyContext.RedisPayData.execute('DEL', 'vipuser:' + rparam['mobile'])
        TyContext.RedisPayData.execute('SADD', '10yuanMonthlyVipMobile', rparam['mobile'])
        return True

    def userSubscribeFailed(cls, param):
        PayHelperV4.callback_error(param['platformOrderId'], param['errorcode'] + ':' + param['errormsg'], param)
