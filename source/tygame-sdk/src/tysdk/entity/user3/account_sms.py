# -*- coding=utf-8 -*-

import random
import re

from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.user3.account_bind import AccountBind
from tysdk.entity.user3.account_info import AccountInfo
from tysdk.entity.user_common.account_helper import AccountHelper
from tysdk.entity.user_common.constants import AccountConst
from tysdk.entity.user_common.verify import AccountVerify


class AccountSms():
    @classmethod
    def doGetSmsBindCode(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doGetSmsBindCode->rparams=', rparams)
        appId = rparams['appId']
        clientId = rparams['clientId']
        userId = rparams['userId']

        bound = False
        if userId > 0:
            bindMobile = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'bindMobile')
            if bindMobile is not None and len(str(bindMobile)) == 11:
                bound = True

        if bound:
            mo.setResult('code', AccountConst.CODE_USER_MOBILE_BINDED)
            mo.setResult('info', '当前账号已绑定手机')
            return

        bindOrderId = TyContext.ServerControl.makeSmsBindOrderIdV3(userId, appId, clientId)
        shortId = ShortOrderIdMap.get_short_order_id(bindOrderId)
        smsconfig = TyContext.Configure.get_global_item_json('smsup_content', {})
        sms = smsconfig['bindcode'] % int(shortId)
        mo.setResult('code', 0)
        mo.setResult('sms', sms)
        ###
        TyContext.RedisUserKeys.execute('HMSET', 'bindOrder:' + bindOrderId,
                                        'state', AccountConst.MOBILE_BIND_PENDING,
                                        'userId', userId, 'appId', appId, 'clientId', clientId)
        TyContext.RedisUserKeys.execute('EXPIRE', 'bindOrder:' + bindOrderId, 5 * 60)
        mo.setResult('bindOrderId', bindOrderId)
        smsup_port = TyContext.Configure.get_global_item_str('smsup_port')
        mo.setResult('port', smsup_port)
        TyContext.ftlog.info(cls.__name__, 'doGetSmsBindCode->bindOrderId=', bindOrderId,
                             'userid=', userId, 'sms', sms, 'port', smsup_port)

    @classmethod
    def doSmsBindCallBack(cls, rparams):
        TyContext.ftlog.info(cls.__name__, 'doSmsBindCallBack->rparams=', rparams)
        mobile = rparams['mobile']
        sms = rparams['sms']

        try:
            template = TyContext.Configure.get_global_item_json(
                'smsup_content', decodeutf8=True)
            smsre = template['bindcode_re']
            if smsre and isinstance(smsre, unicode):
                smsre = smsre.encode('utf8')
            shortId = re.match(smsre, sms).group(1)
            if not shortId:
                raise Exception('fail get new format smsupcontent')
            bindOrderId = ShortOrderIdMap.get_long_order_id(shortId)
            TyContext.RunMode.get_server_link(bindOrderId)
            # V4版本绑定手机号
            if TyContext.RedisUserKeys.execute('EXISTS', 'bindOrderV4:%s' % bindOrderId):
                TyContext.RedisUserKeys.execute('HMSET', 'bindOrderV4:%s' % bindOrderId,
                                                'mobile', mobile,
                                                'state', AccountConst.MOBILE_BIND_SUCCESS)
                TyContext.ftlog.info(cls.__name__, 'doSmsBindCallBack->bindOrderV4', mobile, bindOrderId)
                return
            ### 用来保存订单和手机号的对于关系
            userId, appId, clientId = TyContext.RedisUserKeys.execute(
                'HMGET', 'bindOrder:' + bindOrderId, 'userId', 'appId', 'clientId')

            if not userId or not clientId:
                TyContext.ftlog.info(
                    cls.__name__, 'doSmsBindCallBack->bind user timed out',
                    mobile, bindOrderId)
                TyContext.RunMode.del_server_link(bindOrderId)
                return

        except Exception as e:
            TyContext.ftlog.debug('_get_sms_orderid error parsing new format bindOrderId exception', e)
            sms = AccountVerify.decode64(sms)
            datas = sms.split('|')
            bindOrderId = datas[0]
            userId = int(datas[1])
            clientId = datas[2]
            appId = int(datas[3])
            TyContext.RunMode.get_server_link(bindOrderId)

        TyContext.ftlog.info(cls.__name__, 'doSmsBindCallBack->bind user of', mobile, bindOrderId, appId, userId,
                             clientId)

        bindparams = {'mobile': mobile,
                      'userId': userId,
                      'appId': appId,
                      'clientId': clientId,
                      'bindOrderId': bindOrderId,
                      }
        mo = TyContext.Cls_MsgPack()
        AccountBind.doBindByMobile(bindparams, mo)
        TyContext.RunMode.del_server_link(bindOrderId)

    # 前后端接口，返回值：
    # code: 0 - 表示成功
    #       1 - 表示失败，客户端会重试3次
    #       2 - 表示失败，手机号已绑定其他UID
    @classmethod
    def doCheckSmsBind(cls, rparams, mo):
        bindOrderId = TyContext.RunHttp.getRequestParam('bindOrderId')
        loginFlag = rparams.get('loginFlag', 0)
        if bindOrderId is not None:
            rparams['bindOrderId'] = bindOrderId

        TyContext.ftlog.info(cls.__name__, 'doCheckSmsBind->rparams=', rparams)
        if 'bindOrderId' in rparams:
            bindOrderId = rparams['bindOrderId']
            state, userId = TyContext.RedisUserKeys.execute('HMGET', 'bindOrder:' + bindOrderId, 'state', 'userId')
            if state is None:
                mo.setResult('code', 1)
                mo.setResult('info', '手机绑定失败，请重试')
                TyContext.ftlog.error('doCheckSmsBind wrong state: no pending bindOrder',
                                      bindOrderId, 'rparams', rparams)
                return
            if state == AccountConst.MOBILE_BIND_PENDING:
                mo.setResult('code', 1)
                mo.setResult('info', '手机绑定进行中，请稍候')
                return
            if state == AccountConst.MOBILE_BIND_FAILED:
                mo.setResult('code', 1)
                mo.setResult('info', '手机绑定失败，请重试')
                return
            if state == AccountConst.MOBILE_BIND_OCCUPIED and loginFlag == 0:
                mo.setResult('code', AccountConst.MOBILE_BIND_OCCUPIED)  # 2
                mo.setResult('info', '该手机号已被使用，请绑定其它手机号')
                return
            if state == AccountConst.MOBILE_BIND_SUCCESS \
                    or state == AccountConst.MOBILE_BIND_BOUND \
                    or state == AccountConst.MOBILE_BIND_OCCUPIED:
                if len(str(userId)) == 11:
                    userId = TyContext.RedisUserKeys.execute('GET', 'mobilemap:' + str(userId))
                AccountInfo.fillUserLoginInfoV3(rparams, mo, userId, True, False)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[AccountConst.USER_TYPE_MOBILE],
                    userId, rparams['appId'], rparams['clientId'],
                    mo.getResultStr('mobile'), 0, devId=rparams.get('deviceId', ''))
                TyContext.BiReport.user_login(rparams['appId'], userId, AccountConst.USER_TYPE_MOBILE,
                                              rparams['clientId'], TyContext.RunHttp.get_client_ip(),
                                              rparams.get('deviceId', ''), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                mo.setResult('code', 0)
                mo.setResult('info', '手机绑定成功')
            return

        userId = rparams['userId']
        if userId <= 0:
            mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'userId incorrect')
            return

        bindMobile = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'bindMobile')
        if bindMobile is None or len(str(bindMobile)) != 11:
            mo.setResult('code', 1)
            mo.setResult('info', '手机绑定进行中，请稍候')
            return

        mo.setResult('code', 0)
        mo.setResult('info', '手机绑定成功')
        AccountInfo.fillUserLoginInfoV3(rparams, mo, userId, True, False)
        TyContext.BiReport.user_login(rparams['appId'], userId, AccountConst.USER_TYPE_MOBILE,
                                      rparams['clientId'], TyContext.RunHttp.get_client_ip(),
                                      rparams.get('deviceId', ''), params=TyContext.RunHttp.convertArgsToDict(),
                                      rpath=TyContext.RunHttp.get_request_path())
        # Report.recoderUserLogin( rparams['appId'], userId, AccountConst.USER_TYPE_MOBILE)

    @classmethod
    def doGetSmsVerifyCode(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doGetSmsVerifyCode->rparams=', rparams)
        # appId = rparams['appId']
        # clientId = rparams['clientId']
        # userId = rparams['userId']
        shediao_appId = TyContext.Configure.get_global_item_json('shediao_appId', [10003, 10029, 10032])
        appId = rparams.get('appId', 0)
        mobile = rparams['mobile']
        whatfor = rparams['whatfor']
        userId = TyContext.RedisUserKeys.execute('GET', "mobilemap:" + str(mobile))
        if whatfor == 'bind_mobile' and userId and userId > 0:
            mo.setResult('code', 1)
            mo.setResult('info', '该手机号已被绑定，请您使用其他号码继续绑定。')
            return
        if whatfor == 'set_password' and (not userId or userId <= 0):
            mo.setResult('code', 1)
            mo.setResult('info', '该手机号还未绑定，无法进行密码重置操作。')
            return
        rkey = 'mobile:verify:code:' + str(mobile)
        ttl = TyContext.RedisMix.execute('TTL', rkey)
        if ttl >= 0:
            mo.setResult('code', 1)
            mo.setResult('info', '操作过于频繁，请您稍后再试。')
            return
        # mo.setResult('userId', userId)
        # mo.setResult('appId', appId)
        # mo.setResult('clientId', clientId)
        mo.setResult('mobile', mobile)

        vcode = random.randint(100000, 999999)
        smscontent = TyContext.Configure.get_global_item_json('smsdown_content', decodeutf8=True)
        content = smscontent['sendcode'] % (vcode)
        if appId in shediao_appId:
            sdk_type = 'shediao'
        else:
            sdk_type = 'tuyoo'
        TyContext.ftlog.info(cls.__name__, 'doGetSmsVerifyCode', mobile, whatfor, shediao_appId, appId, sdk_type)
        isOk = TyContext.SmsDown.sendSms(mobile, content, sdk_type)
        if isOk:
            TyContext.RedisMix.execute('SET', rkey, vcode)
            TyContext.RedisMix.execute('EXPIRE', rkey, 60)
            mo.setResult('code', 0)
            mo.setResult('info', '验证码短信发送成功')
        else:
            mo.setResult('code', 1)
            mo.setResult('info', '短信发送失败，请稍后再试')

    @classmethod
    def doBindMobileByVerifyCode(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doBindMobileByVerifyCode->rparams=', rparams)
        appId = rparams['appId']
        clientId = rparams['clientId']
        userId = rparams['userId']
        mobile = rparams['mobile']
        vcode = rparams['vcode']
        rkey = 'mobile:verify:code:' + str(mobile)
        vcodeDb = TyContext.RedisMix.execute('GET', rkey)
        if vcodeDb and int(vcodeDb) == int(vcode):
            TyContext.RedisMix.execute('DEL', rkey)
            bindparams = {
                'mobile': mobile,
                'userId': userId,
                'appId': appId,
                'clientId': clientId,
            }
            AccountBind.doBindByMobile(bindparams, mo)
        else:
            mo.setResult('code', 1)
            mo.setResult('info', '短信验证码无效，请重新输入或获取验证码')

    @classmethod
    def doSetPasswordByVerifyCode(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doSetPasswordByVerifyCode->rparams=', rparams)
        # appId = rparams['appId']
        # clientId = rparams['clientId']
        # userId = rparams['userId']
        mobile = rparams['mobile']
        vcode = rparams['vcode']

        userId = cls._find_userid_by_mobile(mobile)
        if not userId:
            mo.setResult('code', 2)
            mo.setResult('info', '手机号未绑定')
            return mo

        rparams['userId'] = userId
        rkey = 'mobile:verify:code:' + str(mobile)
        vcodeDb = TyContext.RedisMix.execute('GET', rkey)
        if vcodeDb and int(vcodeDb) == int(vcode):
            TyContext.RedisMix.execute('DEL', rkey)
            AccountInfo.doSetPasswd(rparams, mo, False)
            return mo
        else:
            mo.setResult('code', 1)
            mo.setResult('info', '短信验证码无效，请重新输入或获取验证码')
            return mo

    @classmethod
    def _find_userid_by_mobile(cls, mobile):
        uid = TyContext.RedisUserKeys.execute('GET', 'mobilemap:' + str(mobile))
        if not uid or uid <= 0:
            return 0
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('_find_userid_by_mobile failed get cold data')
            return 0
