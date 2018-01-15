# -*- coding=utf-8 -*-

import random

import datetime

from tyframework.context import TyContext
from tysdk.entity.friend3.friend import Friend
from tysdk.entity.user3.account_info import AccountInfo
from tysdk.entity.user3.account_login import AccountLogin
from tysdk.entity.user_common.account_360 import Account360
from tysdk.entity.user_common.account_helper import AccountHelper
from tysdk.entity.user_common.account_weixin import AccountWeixin
from tysdk.entity.user_common.constants import AccountConst


class AccountBind():
    @classmethod
    def doBindBySnsId(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doBindBySnsId->rparams=', rparams)

        userId = rparams['userId']
        snsId = rparams['snsId']
        if snsId.startswith('360'):
            if Account360.doGetUserInfo(rparams, snsId) != True:
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '360登录验证失败！')
                return
            else:
                snsId = rparams['snsId']

            # 绑定过程，不改变用户昵称
            if 'name' in rparams:
                del rparams['name']

        elif snsId.startswith('wx:'):
            if not AccountWeixin.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'wx登录验证失败！')
                #                TyContext.BiReport.report_bi_sdk_login(
                #                    TyContext.BIEventId.SDK_LOGIN_BY_SNSID_FAIL, 0,
                #                    rparams['appId'], rparams['clientId'], snsId,
                #                    AccountConst.CODE_USER_SNS_GETINFO_ERROR)
                return
            else:
                snsId = rparams['snsId']

        userIdBound = TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + snsId)
        if userIdBound:
            TyContext.MySqlSwap.checkUserDate(userIdBound)
            AccountHelper.restore_avatar_verify_set(userIdBound)
            mo.setResult('code', 0)
            mo.setResult('info', '绑定成功')
            mo.setResult('binduserstyle', 2)
            AccountLogin.__do_login_done__(rparams, userIdBound, mo, AccountConst.USER_TYPE_SNS)
            return

        # V3版一个tyid可以绑定多个snsId
        TyContext.MySqlSwap.checkUserDate(userId)
        AccountHelper.restore_avatar_verify_set(userId)
        TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId),
                                    'snsId', snsId,
                                    'isbind', AccountConst.USER_TYPE_SNS,
                                    'bindTime', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        TyContext.RedisUserKeys.execute('SET', 'snsidmap:' + snsId, userId)
        mo.setResult('code', 0)
        mo.setResult('binduserstyle', 1)
        mo.setResult('info', '绑定成功')
        AccountLogin.__do_login_done__(rparams, userId, mo, AccountConst.USER_TYPE_SNS)
        cls.__bind_success_callback_(rparams['appId'], 'bindsnsid',
                                     {'appId': rparams['appId'],
                                      'userId': userId, 'snsId': snsId})

    @classmethod
    def doBindByEmail(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doBindByEmail->rparams=', rparams)

        userId = rparams['userId']
        mail = rparams['mail']
        # 检查email是否已被绑定
        userOldEmail, isbind = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'email', 'isbind')
        if userOldEmail != None and userOldEmail != '' and int(isbind) == AccountConst.USER_TYPE_MAIL:
            # 邮件已经被绑定
            mo.setResult('code', AccountConst.CODE_USER_MAIL_BINDED)
            mo.setResult('info', '该邮箱已被使用，请绑定其它邮箱')
            return

        userIdByMap = cls.__find_userid_by_mail__(mail)
        if userIdByMap == 0:
            #             TyContext.ftlog.info('sdkUserBindEmail in userId=', userId, 'email=', mail, 'clientId=', rparams['clientId'])

            TyContext.RedisUserKeys.execute('SET', 'mailmap:' + mail, userId)
            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), 'email', mail, 'isbind',
                                        AccountConst.USER_TYPE_MAIL)
            mo.setResult('userEmail', mail)
            mo.setResult('code', 0)
            mo.setResult('info', '邮箱绑定成功')
        else:
            # 邮件已经被绑定
            mo.setResult('code', AccountConst.CODE_USER_MAIL_BINDED)
            mo.setResult('info', '该邮箱已被使用，请绑定其它邮箱')

    @classmethod
    def doBindByMobile(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doBindByMobile->rparams=', rparams)

        clientId = rparams['clientId']
        chkMobile = str(rparams['mobile'])
        appId = rparams['appId']
        chkUserId = str(rparams['userId'])
        bindOrderId = rparams['bindOrderId'] if 'bindOrderId' in rparams else ''

        userIdByMap = cls.__find_userid_by_mobile__(chkMobile)
        if userIdByMap > 0:
            if userIdByMap == int(chkUserId):
                TyContext.RedisUserKeys.execute('HMSET', 'bindOrder:' + bindOrderId,
                                                'state', AccountConst.MOBILE_BIND_BOUND,
                                                'userId', userIdByMap)
                mo.setResult('code', AccountConst.CODE_USER_MOBILE_BINDED)
                mo.setResult('info', '无需重复绑定（手机号已绑定）')
                return

            TyContext.RedisUserKeys.execute('HMSET', 'bindOrder:' + bindOrderId,
                                            'state', AccountConst.MOBILE_BIND_OCCUPIED, 'userId', chkMobile)
            mo.setResult('code', AccountConst.CODE_USER_MOBILE_BINDED)
            mo.setResult('info', '该手机号已被使用，请绑定其它手机号')
            return

        if chkUserId == '0':
            passwd = 'ty' + str(random.randint(100000, 999999))
            rparams['passwd'] = passwd
            chkUserId = AccountInfo.createNewUser(rparams, AccountConst.USER_TYPE_MOBILE)
            if chkUserId <= 0:
                TyContext.RedisUserKeys.execute('HSET', 'bindOrder:' + bindOrderId,
                                                'state', AccountConst.MOBILE_BIND_FAILED)
                mo.setResult('code', AccountConst.CODE_USER_MOBILE_REG_FAILE)
                mo.setResult('info', '手机用户注册失败')
                return
            smscontent = TyContext.Configure.get_global_item_json('smsdown_content', decodeutf8=True)
            content = smscontent['sendpwd'] % passwd
            if not TyContext.SmsDown.sendSms(chkMobile, content):
                TyContext.ftlog.error('AccountBind->doBindByMobile send mobile'
                                      ' passwd by sms failed! userid=', chkUserId,
                                      'mobile=', chkMobile, 'appId=', appId,
                                      'clientId=', clientId)
            chkUserId = str(chkUserId)

        TyContext.RedisUserKeys.execute('SET', 'mobilemap:' + chkMobile, chkUserId)
        TyContext.RedisUser.execute(chkUserId, 'HMSET', 'user:' + chkUserId,
                                    'bindMobile', chkMobile, 'clientId', clientId,
                                    'isbind', AccountConst.USER_TYPE_MOBILE)
        if len(bindOrderId) > 0:
            TyContext.RedisUserKeys.execute('HMSET', 'bindOrder:' + bindOrderId,
                                            'state', AccountConst.MOBILE_BIND_SUCCESS, 'userId', chkUserId)
        # ftlog.info('sdkUserRegisterMobile in userId=', chkUserId, 'mobile=', chkMobile, 'clientId=', clientId, 'appId=', appId)
        mo.setResult('code', AccountConst.CODE_USER_SUCCESS)
        mo.setResult('info', '手机号绑定成功')
        Friend.onUserRegisterMobile(appId, int(chkUserId), chkMobile)
        cls.__bind_success_callback_(appId, 'bindphone', {'userId': chkUserId})

    @classmethod
    def __find_userid_by_mobile__(cls, userMobile):
        uid = TyContext.RedisUserKeys.execute('GET', 'mobilemap:' + str(userMobile))
        if not uid or uid <= 0:
            return 0
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('__find_userid_by_mobile__ failed get cold data')
            return 0

    @classmethod
    def __find_userid_by_account__(cls, account):
        uid = TyContext.RedisUserKeys.execute('GET', 'accountmap:' + str(account))
        if not uid or uid <= 0:
            return 0
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('__find_userid_by_account__ failed get cold data')
            return 0

    @classmethod
    def __find_userid_by_mail__(cls, email):
        uid = TyContext.RedisUserKeys.execute('GET', 'mailmap:' + str(email))
        if not uid or uid <= 0:
            return 0
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('__find_userid_by_mail__ failed get cold data')
            return 0

    @classmethod
    def __find_userid_by_snsid__(cls, snsId):
        uid = TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + str(snsId))
        if not uid or uid <= 0:
            return 0
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('__find_userid_by_snsid__ failed get cold data')
            return 0

    @classmethod
    def __bind_success_callback_(cls, appid, bindstr, data):
        TyContext.ftlog.debug('AccountBind->__bind_success_callback_ begin', appid, bindstr, data)
        conf = TyContext.Configure.get_global_item_json(bindstr + '.reward.callback', {})
        if conf and str(appid) in conf:
            url = conf[str(appid)]
            response, requestUrl = TyContext.WebPage.webget(url, data)
            TyContext.ftlog.debug('AccountBind->__bind_success_callback_ success', response)
