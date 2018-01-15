#! encoding=utf-8
import copy
import hashlib
import random
from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.user3.account_info import AccountInfo
from tysdk.entity.user3.account_login import AccountLogin
from tysdk.entity.user4.account_model import AccountModel
from tysdk.entity.user4.account_util import AccountUtil
from tysdk.entity.user_common.account_helper import AccountHelper
from tysdk.entity.user_common.constants import AccountConst
from tysdk.entity.user_common.username import UsernameGenerator
from tysdk.entity.user_common.verify import AccountVerify
from tysdk.utils import sslhttp
from tysdk.utils.sslhttp import queryHttpSsl

__author__ = 'yuejianqiang'


class AccountUniversal:
    @classmethod
    def doChangeUserName(cls, mo, rpath):
        if not AccountVerify.sing_verify(rpath):
            mo.setResult('code', -1)
            mo.setResult('info', '验签失败')
            return
        rparam = TyContext.RunHttp.convertArgsToDict()
        userName = rparam.get('userName', '')
        userId = rparam.get('userId')
        UsernameGenerator.change_old_user_name(userName, userId, mo)

    @classmethod
    def getSmsBindCode(cls, rparams, mo):
        """
        获取上行短信内容和端口号，注册和绑定账号时使用
        # token用于游客绑定
        # userId用于已绑定的账号指定登录
        # 游客创建则token和userId都不要指定
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'getSmsBindCode->rparams=', rparams)
        appId = rparams['appId']
        clientId = rparams['clientId']
        userId = int(rparams.get('userId', 0))  # 指定用户登录
        passwd = rparams.get('passwd', '')
        token = rparams.get('token', '')  # 指定token登录
        # 检查参数
        if userId and passwd:
            TyContext.MySqlSwap.checkUserDate(userId)
            if not AccountLogin.__check_user_passwd__(userId, passwd):
                mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
                mo.setResult('info', '通行证或密码错误，请重新输入！')
                return
        # 绑定逻辑
        bindOrderId = TyContext.ServerControl.makeSmsBindOrderIdV3(userId, appId, clientId)
        shortId = ShortOrderIdMap.get_short_order_id(bindOrderId)
        smsconfig = TyContext.Configure.get_global_item_json('smsup_content', {})
        sms = smsconfig['bindcode'] % int(shortId)
        mo.setResult('code', 0)
        mo.setResult('sms', sms)
        # 手机注册绑定信息
        TyContext.RedisUserKeys.execute('HMSET', 'bindOrderV4:' + bindOrderId,
                                        'state', AccountConst.MOBILE_BIND_PENDING,
                                        'appId', appId,
                                        'clientId', clientId,
                                        'userId', userId,
                                        'token', token,
                                        'passwd', passwd, )
        TyContext.RedisUserKeys.execute('EXPIRE', 'bindOrderV4:' + bindOrderId, 5 * 60)
        mo.setResult('bindOrderId', bindOrderId)
        smsup_port = TyContext.Configure.get_global_item_str('smsup_port')
        mo.setResult('port', smsup_port)
        TyContext.ftlog.info(cls.__name__, 'doGetSmsBindCode->bindOrderId=', bindOrderId, 'userid=', userId, 'sms', sms,
                             'port', smsup_port)

    @classmethod
    def checkBindUser(cls, userId, passwd=None, token=None, bindMobile=None):
        bindUserId = AccountModel.get_mobile_bind_user(bindMobile)
        if userId:
            if passwd and AccountLogin.__check_user_passwd__(userId, passwd) and not bindUserId:
                return userId
            if token and AccountModel.get_user_by_token(token) == userId:
                return userId
            userMobile = AccountModel.get_user_mobile(userId)
            if AccountModel.is_valid_mobile(userMobile) and userMobile == bindMobile:
                return userId
        if token:
            userId = AccountModel.get_user_by_token(token)
            if userId:
                return userId
        return bindUserId

    @classmethod
    def doCheckSmsBindInfo(cls, rparams, mo):
        """
        检查客户端上行短信
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'getSmsBindCode->rparams=', rparams)
        bindOrderId = TyContext.RunHttp.getRequestParam('bindOrderId')
        state, _mobile, userId, token, passwd = TyContext.RedisUserKeys.execute('HMGET', 'bindOrderV4:' + bindOrderId,
                                                                                'state', 'mobile', 'userId', 'token',
                                                                                'passwd')
        bindMobile = str(_mobile)
        ###
        # 判断成功并且手机号正确
        if state == AccountConst.MOBILE_BIND_SUCCESS and AccountModel.is_valid_mobile(bindMobile):
            TyContext.RedisUserKeys.execute('DEL', 'bindOrderV4:' + bindOrderId)
            # 检查userId
            userId = cls.checkBindUser(userId, token=token, passwd=passwd, bindMobile=bindMobile)
            # 检查bindMobile
            if userId and userId > 0:
                userMobile = AccountModel.get_user_mobile(userId)
                if AccountModel.is_valid_mobile(userMobile):
                    if userMobile != bindMobile:
                        mo.setResult('code', 1)
                        mo.setResult('info', '已绑定尾数%s的手机号，请直接登录' % str(userMobile)[-4:])
                        return
                elif not userMobile and len(AccountModel.get_mobile_user_set(bindMobile)) >= 5:
                    mo.setResult('code', 1)
                    mo.setResult('info', '手机号绑定账号已超过上限')
                    return
            # 创建新账号
            else:
                # create user and token
                rparams['mobile'] = bindMobile
                loginType = AccountConst.USER_TYPE_MOBILE
                userId = AccountInfo.createNewUser(rparams, loginType, False)
                if userId <= 0:
                    mo.setResult('code', 1)
                    mo.setResult('info', '创建用户失败')
                    return
            # 手机号写入个人信息
            AccountModel.bind_user_to_mobile(userId, bindMobile)
            # 获取新的Token
            token = AccountModel.reset_user_token(userId, 'mobile', bindMobile)
            mo.setResult('code', 0)
            mo.setResult('token', token)
        else:
            mo.setResult('code', 1)
            mo.setResult('info', '手机绑定进行中，请稍候')

    @classmethod
    def externVerify(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        appId = rparam.get('appId', '9999')
        config = TyContext.Configure.get_global_item_json('externalLogin', {})
        md5Config = config.get(str(appId))
        if not md5Config:
            return False
        md5key = md5Config['md5']
        sign = rparam.get('sign', '')
        query = "&".join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) \
                         if k != 'sign')
        m = md5()
        m.update(query + ':' + md5key)
        return sign == m.hexdigest().lower() or True

    @classmethod
    def unbindUserExternId(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        if not cls.externVerify(rpath):
            mo.setResult('info', '验签失败！')
            mo.setResult('code', -1)
            return mo
        rparam = TyContext.RunHttp.convertArgsToDict()
        userId = rparam.get('userId', '')
        mobile = rparam.get('mobile', '')
        if mobile != AccountModel.get_user_mobile(userId):
            mo.setResult('info', '用户绑定信息错误！')
            mo.setResult('code', -2)
            return mo
        AccountModel.unbind_user_from_externId(userId)
        mo.setResult('info', '解绑成功!')
        mo.setResult('code', 0)
        return mo

    @classmethod
    def getUserByExternId(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        if not cls.externVerify(rpath):
            mo.setResult('info', '验签失败！')
            mo.setResult('code', -1)
            return mo
        rparam = TyContext.RunHttp.convertArgsToDict()
        externId = rparam.get('externId', '')
        mobile = rparam.get('mobile', '')
        userId = AccountModel.get_user_by_externId(externId)
        if mobile != AccountModel.get_user_mobile(userId):
            mo.setResult('info', '用户绑定信息有误！')
            mo.setResult('code', -2)
            return mo
        userList = []
        if AccountModel.is_valid_mobile(mobile):
            for accountId in AccountModel.get_mobile_user_set(mobile):
                TyContext.MySqlSwap.checkUserDate(accountId)
                userList.append(AccountModel.get_user_brief_info(accountId))
        mo.setResult('userList', userList)
        mo.setResult('code', 0)
        return mo

    @classmethod
    def bindByExternId(cls, rpath):
        '''
        绑定外部的一个标示到子账号上
        :param rpath:
        :return:
        '''
        mo = TyContext.Cls_MsgPack()
        if not cls.externVerify(rpath):
            mo.setResult('info', '验签失败！')
            mo.setResult('code', -1)
            return mo
        rparam = TyContext.RunHttp.convertArgsToDict()
        appId = rparam.get('appId', 9999)
        rparam['appId'] = appId
        config = TyContext.Configure.get_global_item_json('externalLogin', {})
        appIdConfig = config.get(str(appId))
        if appIdConfig and not rparam.get('clientId', ''):
            rparam['clientId'] = appIdConfig['clientId']
        externId = rparam.get('externId', "")
        mobile = rparam.get('mobile', '')
        userId = rparam.get('userId', '')
        if not externId or not mobile or not userId:
            mo.setResult('info', '参数错误！')
            mo.setResult('code', -2)
            return mo
        if mobile != AccountModel.get_user_mobile(userId):
            mo.setResult('info', '用户绑定信息有误！')
            mo.setResult('code', -2)
            return mo
        oldUid = rparam.get('oldUid', '')
        if oldUid:
            AccountModel.unbind_user_from_externId(oldUid)
        AccountModel.bind_user_to_externId(externId, userId)
        mo.setResult('code', 0)
        mo.setResult('info', "绑定成功！")
        return mo

    @classmethod
    def doSendSmsVerifyCodeExternal(cls, mo, rpath):
        '''
        微信合作
        :param mo:
        :param rpath:
        :return:
        '''
        if not cls.externVerify(rpath):
            mo.setResult('info', '验签失败！')
            mo.setResult('code', -1)
            return
        rparam = TyContext.RunHttp.convertArgsToDict()
        cls.doSendSmsVerifyCode(rparam, mo)

    @classmethod
    def doSendSmsVerifyCode(cls, rparams, mo, userId=0, token='', passwd=''):
        """
        使用短信验证码登录，ios或者android发送不了短信手机使用
        通过短信网关下发一条短信到手机上确认手机号
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'doSendSmsVerifyCode->rparams=', rparams)
        # appId = rparams['appId']
        # clientId = rparams['clientId']
        shediao_appId = TyContext.Configure.get_global_item_json('shediao_appId', [10003, 10029, 10032, 10048])
        appId = rparams.get('appId', 0)
        mobile = rparams['mobile']
        whatfor = rparams.get('whatfor', '')
        if not userId:
            userId = int(rparams.get('userId', 0))
        if not passwd:
            passwd = rparams.get('passwd', '')
        if not token:
            token = rparams.get('token', '')
        rkey = 'mobile:verify:code:' + str(mobile)
        ttl = TyContext.RedisMix.execute('TTL', rkey)
        if ttl >= 0:
            mo.setResult('code', 1)
            mo.setResult('info', '操作过于频繁，请您稍后再试。')
            return
        # 每个手机号最多允许绑定5个手机号
        if userId and userId > 0:
            userMobile = AccountModel.get_user_mobile(userId)
            if not userMobile and len(AccountModel.get_mobile_user_set(mobile)) >= 5:
                mo.setResult('code', 2)
                mo.setResult('info', '每个手机号最多允许绑定5个账号！')
                return
        mo.setResult('mobile', mobile)
        vcode = random.randint(100000, 999999)
        smscontent = TyContext.Configure.get_global_item_json('smsdown_content', decodeutf8=True)
        content = smscontent['sendcode'] % (vcode)
        smsConfig = TyContext.Configure.get_game_item_json(appId, "smsConfig", {})
        sdk_type = smsConfig.get('smstype', "tuyoo")  # 默认tuyoo
        content = smsConfig.get("sendcode", "验证码:%d(为保账号安全请勿告知他人，如有疑问请拨打客服电话：4008098000)") % vcode  # 默认用之前的文案
        sms_config = smsConfig.get('smsconfig', {})
        TyContext.ftlog.info(cls.__name__, 'doGetSmsVerifyCode', mobile, '', shediao_appId, appId, sdk_type)
        isOk = TyContext.SmsDown.sendSms(mobile, content, sdk_type, sms_config=sms_config)
        if isOk:
            # cd
            TyContext.RedisMix.execute('SET', rkey, vcode)
            TyContext.RedisMix.execute('EXPIRE', rkey, 1 * 60)
            # code
            vkey = '%s:%s' % (rkey, vcode)
            TyContext.RedisMix.execute('HMSET', vkey,
                                       'vcode', vcode,
                                       'userId', userId,
                                       'token', token,
                                       'passwd', passwd)
            TyContext.RedisMix.execute('EXPIRE', vkey, 5 * 60)
            bindUser = AccountModel.get_mobile_bind_user(mobile)
            mo.setResult('code', 0)
            mo.setResult('userId', bindUser if bindUser else 0)
            mo.setResult('info', '验证码短信发送成功')
        else:
            mo.setResult('code', 1)
            mo.setResult('info', '短信发送失败，请稍后再试')

    @classmethod
    def doCheckSmsVerifyCodeExternal(cls, mo, rpath):
        if not cls.externVerify(rpath):
            mo.setResult('info', '验签失败！')
            mo.setResult('code', -1)
            return
        rparams = TyContext.RunHttp.convertArgsToDict()
        appId = rparams.get('appId', 9999)
        rparams['appId'] = appId
        config = TyContext.Configure.get_global_item_json('externalLogin', {})
        appIdConfig = config.get(str(appId))
        if appIdConfig and not rparams.get('clientId', ''):
            rparams['clientId'] = appIdConfig['clientId']
        cls.doCheckSmsVerifyCode(rparams, mo)

    @classmethod
    def doCheckSmsVerifyCode(cls, rparams, mo):
        """
        检查短信验证码
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'doCheckSmsVerifyCode->rparams=', rparams)
        _mobile = rparams['mobile']
        bindMobile = str(_mobile)
        vcode = rparams['vcode']
        password = rparams.get('password', '')
        if password and len(password) < 6:
            mo.setResult('code', 1)
            mo.setResult('info', '密码必须包含至少6个字符')
            return
        # 获取verify code userid
        rkey = 'mobile:verify:code:' + str(bindMobile)
        vkey = '%s:%s' % (rkey, vcode)
        vcodeDb, userId, token, passwd = TyContext.RedisMix.execute('HMGET', vkey, 'vcode', 'userId', 'token', 'passwd')
        createUser = False
        if vcodeDb and int(vcodeDb) == int(vcode):
            TyContext.RedisMix.execute('DEL', vkey)
            clientId = rparams.get('clientId')
            clientList = TyContext.Configure.get_game_item_json('9999', 'ios.idfa.show.clientids')
            # IOS提审宝配置
            if clientId and clientId in clientList:
                userId = AccountModel.get_mobile_client_bind_user(bindMobile, clientId)
                if userId <= 0:
                    del rparams['mobile']
                    createUser = True
                    userId = AccountInfo.createNewUser(rparams, AccountConst.USER_TYPE_MOBILE)
                    AccountInfo.fillUserLoginInfoV3(rparams, mo, userId, True, True)
                    AccountModel.bind_user_to_mobile_client(userId, bindMobile, clientId)
            else:
                userId = cls.checkBindUser(userId, passwd=passwd, token=token, bindMobile=bindMobile)
                # 检查用户是否已经绑定手机
                if userId and userId > 0:
                    userMobile = AccountModel.get_user_mobile(userId)
                    if AccountModel.is_valid_mobile(userMobile):
                        if userMobile != bindMobile:
                            mo.setResult('code', 1)
                            mo.setResult('info', '已绑定尾数%s的手机号，请直接登录' % str(userMobile)[-4:])
                            return
                    elif not userMobile and len(AccountModel.get_mobile_user_set(bindMobile)) >= 5:
                        mo.setResult('code', 1)
                        mo.setResult('info', '手机号绑定账号已超过上限')
                        return
                # 创建新用户
                else:
                    loginType = AccountConst.USER_TYPE_MOBILE
                    userId = AccountInfo.createNewUser(rparams, loginType, False)
                    createUser = True
                    if userId <= 0:
                        mo.setResult('code', 1)
                        mo.setResult('info', '创建用户失败')
                        return
                # 手机号写入个人信息
                AccountModel.bind_user_to_mobile(userId, bindMobile)
            if password:
                AccountModel.set_mobile_password(bindMobile, password)
            token = AccountModel.reset_user_token(userId, 'mobile', bindMobile)
            mo.setResult('code', 0)
            mo.setResult('createUser', createUser)
            mo.setResult('token', token)
        else:
            mo.setResult('code', 1)
            mo.setResult('info', '短信验证码无效，请重新输入或获取验证码')

    @classmethod
    def bindByDevice(cls, rparams, mo):
        """
        绑定游客账号（设备号）到手机账号
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'bindByDevice->rparams=', rparams)
        # chkMobile = rparams['mobile']
        deviceId = rparams['deviceId']
        userId = AccountLogin.__find_userid_by_devid_map_v3__(deviceId)
        # 检查密码
        if 'passwd' in rparams and not AccountLogin.__check_user_passwd__(userId, rparams['passwd']):
            mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
        if userId > 0:
            token = AccountModel.reset_user_token(userId)
            AccountUniversal.doSendSmsVerifyCode(rparams, mo, userId=userId, token=token)
        else:
            mo.setResult('code', AccountConst.CODE_USER_DEV_REG_FAILE)
            mo.setResult('info', '设备未注册账号！')

    @classmethod
    def bindByTyId(cls, rparams, mo):
        """
        绑定TuyooID到手机号
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'bindByTyId->rparams=', rparams)
        tuyooId = int(rparams['tuyooId'])
        TyContext.MySqlSwap.checkUserDate(tuyooId)
        if not AccountLogin.__check_user_passwd__(tuyooId, rparams['passwd']):
            mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            return
        userId = AccountLogin.__find_userid_by_tyid__(tuyooId)
        if userId > 0:
            token = AccountModel.reset_user_token(userId)
            AccountUniversal.doSendSmsVerifyCode(rparams, mo, userId=userId, token=token)
        else:
            mo.setResult('code', AccountConst.CODE_USER_DEV_REG_FAILE)
            mo.setResult('info', '未注册Tuyoo Id！')

    @classmethod
    def bindByMail(cls, rparams, mo):
        """
        绑定邮箱账号到手机号
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'doLoginByMail->rparams=', rparams)
        mail = rparams['mail']
        userId = AccountLogin.__find_userid_by_mail__(mail)
        if userId <= 0:
            # 补丁:重度游戏那边的邮箱用户
            userId = AccountLogin.__find_userid_by_account__(mail)
        if 'passwd' in rparams and not AccountLogin.__check_user_passwd__(userId, rparams['passwd']):
            mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
        if userId > 0:
            token = AccountModel.reset_user_token(userId)
            AccountUniversal.doSendSmsVerifyCode(rparams, mo, userId=userId, token=token)
        else:
            mo.setResult('code', AccountConst.CODE_USER_DEV_REG_FAILE)
            mo.setResult('info', '邮箱未注册账号！')

    @classmethod
    def doLoginByTokenExternal(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        if not cls.externVerify(rpath):
            mo.setResult('info', '验签失败！')
            mo.setResult('code', -1)
            return mo
        rparams = TyContext.RunHttp.convertArgsToDict()
        appId = rparams.get('appId', 9999)
        rparams['appId'] = appId
        config = TyContext.Configure.get_global_item_json('externalLogin', {})
        appIdConfig = config.get(str(appId))
        if appIdConfig and not rparams.get('clientId', ''):
            rparams['clientId'] = appIdConfig['clientId']
        cls.doLoginByToken(rparams, mo)
        mout = TyContext.Cls_MsgPack()
        if mo.getResult('code') != 0:
            return mo
        mout.setResult('code', 0)
        mout.setResult('userList', mo.getResult('userList'))
        mout.setResult('userId', mo.getResult('userId'))
        return mout

    @classmethod
    def doLoginByToken(cls, rparams, mo):
        """
        根据token获取用户信息（登录）
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'doLoginByToken->rparams=', rparams)
        token = rparams['token']
        userId, loginType, loginMobile = cls.__find_userid_by_token(token)
        if not userId:
            mo.setResult('code', AccountConst.CODE_USER_INVALID_TOKEN)
            mo.setResult('info', '您的登录状态已失效，请重新登录!')
            return
        clientIp = TyContext.UserSession.get_session_client_ip(int(userId))
        TyContext.ftlog.info("UNIVERSAL_LOG_LOGIN", "userId=", userId, 'clientIp=', clientIp, 'version=', 'v4',
                             'login_params=', rparams)
        mo.setResult('token', token)
        AccountModel.set_mobile_default_user(userId)
        AccountLogin._do_check_login(rparams, userId, mo, AccountConst.USER_TYPE_MOBILE)
        mobile = AccountModel.get_user_mobile(userId)
        userList = []
        if AccountModel.is_valid_mobile(mobile):
            for accountId in AccountModel.get_mobile_user_set(mobile):
                TyContext.MySqlSwap.checkUserDate(accountId)
                userList.append(AccountModel.get_user_brief_info(accountId))
        mo.setResult('userList', userList)
        if True or mo.getParamInt('appId', 0) != 9999:
            if loginType == 'device':
                mo.setResult('loginTips', '游客%d登录成功' % userId)
            elif loginType == 'mobile':
                mo.setResult('loginTips', '手机%s登录成功' % loginMobile)
            else:
                mo.setResult('loginTips', "用户%d登录成功" % userId)

    @classmethod
    def __find_userid_by_token(cls, token):
        uid, loginType, loginMobile = AccountModel.get_token_info(token)
        if not uid or uid <= 0:
            return 0, None, None
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid, loginType, loginMobile
        except:
            TyContext.ftlog.error('__find_userid_by_token failed get cold data')
            return 0, None, None

    @classmethod
    def createGuest(cls, rparams, mo):
        """
        创建游客账号
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'createGuest->rparams=', rparams)
        deviceId = rparams['deviceId']
        clientId = rparams.get('clientId')
        # ios提审宝检查
        clientList = TyContext.Configure.get_game_item_json('9999', 'ios.idfa.show.clientids')
        if clientId and clientId in clientList:
            deviceId = hashlib.md5('%s@%s' % (deviceId, clientId)).hexdigest()
            rparams['deviceId'] = deviceId
        userId = AccountModel.get_user_by_device(deviceId)
        if not userId or userId < 0:
            loginType = AccountConst.USER_TYPE_DEVICE
            # 游客初次登陆注册,注册后,返回初次注册的信息
            rparams['passwd'] = 'ty' + str(random.randint(100000, 999999))
            userId = AccountInfo.createNewUser(rparams, loginType)
            if userId > 0:
                AccountInfo.fillUserLoginInfoV3(rparams, mo, userId, True, True)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[loginType], userId,
                    rparams['appId'], rparams['clientId'],
                    str(rparams.get(AccountConst.LOGIN_BINDID_KEY[loginType], '')),
                    0, devId=rparams.get('deviceId', ''))
                token = AccountModel.reset_user_token(userId, 'device')
                mo.setResult('code', 0)
                mo.setResult('token', token)
            else:
                if userId == -1:
                    mo.setResult('code', AccountConst.CODE_USER_DEV_REG_FAILE)
                    mo.setResult('info', '您的IP地址异常，暂时无法注册新账号，请电话联系客服：400-8098-000')
                    mo.setResult('tips', '您的IP地址异常，暂时无法注册新账号')
                    return
                mo.setResult('code', AccountConst.CODE_USER_GUEST_REG_FAILE)
                mo.setResult('info', '设备用户注册失败')
        else:
            token = AccountModel.reset_user_token(userId, 'device')
            mo.setResult('code', 0)
            mo.setResult('token', token)

    @classmethod
    def checkPassword(cls, rparams, mo):
        """
        通过手机号和密码验证获取Token（用于登录)
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'checkPassword->rparams=', rparams)
        userId = int(rparams.get('userId', 0))
        mobile = rparams.get('mobile', '')
        password = rparams['password']
        clientId = rparams.get('clientId', '')
        ### ios提审宝检查
        clientList = TyContext.Configure.get_game_item_json('9999', 'ios.idfa.show.clientids')
        if clientId and clientId in clientList:
            userId = AccountModel.get_mobile_client_bind_user(mobile, clientId)
            if userId <= 0:
                del rparams['mobile']
                userId = AccountInfo.createNewUser(rparams, AccountConst.USER_TYPE_MOBILE)
                AccountInfo.fillUserLoginInfoV3(rparams, mo, userId, True, True)
                AccountModel.bind_user_to_mobile_client(userId, mobile, clientId)
        # 客户端指定账号
        if not userId or userId <= 0:
            userId = AccountModel.get_mobile_bind_user(mobile)
        if userId <= 0:
            mo.setResult('code', AccountConst.CODE_USER_MOBILE_REG_FAILE)
            mo.setResult('info', '手机号未绑定账号！')
            return mo
        if AccountLogin.__check_user_passwd__(userId, password):
            token = AccountModel.reset_user_token(userId, 'mobile', mobile)
            mo.setResult('code', 0)
            mo.setResult('token', token)
            return mo
        if AccountModel.check_mobile_password(mobile, password):
            token = AccountModel.reset_user_token(userId, 'mobile', mobile)
            mo.setResult('code', 0)
            mo.setResult('token', token)
            return mo
        mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
        mo.setResult('info', '账号或密码错误！')
        return mo

    @classmethod
    def changePassword(cls, rparams, mo):
        """
        修改手机号和密码(通过短信验证码）
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'changePassword->rparams=', rparams)
        mobile = rparams['mobile']
        vcode = rparams['vcode']
        password = rparams['password']
        rkey = 'mobile:verify:code:' + str(mobile)
        vkey = '%s:%s' % (rkey, vcode)
        vcodeDb = TyContext.RedisMix.execute('HGET', vkey, 'vcode')
        if vcodeDb and int(vcodeDb) == int(vcode):
            TyContext.RedisMix.execute('DEL', vkey)
            for userId in AccountModel.get_mobile_user_set(mobile):
                AccountModel.set_user_password(userId, password)
            AccountModel.set_mobile_password(mobile, password)
            mo.setResult('code', 0)
            mo.setResult('info', "密码修改成功")
        else:
            mo.setResult('code', 1)
            mo.setResult('info', "验证码错误")
        return mo

    @classmethod
    def listUser(cls, rparams, mo):
        """
        返回所有绑定此手机号的账号列表
        :param rparams:
        :param mo:
        :return:
        """
        TyContext.ftlog.info(cls.__name__, 'listUser->rparams=', rparams)
        token = rparams['token']
        userId, loginType, loginMobile = cls.__find_userid_by_token(token)
        if not userId:
            mo.setResult('code', AccountConst.CODE_USER_INVALID_TOKEN)
            mo.setResult('info', 'token已经失效！')
            return
        # render
        userList = []
        mobile = AccountModel.get_user_mobile(userId)
        if not mobile:
            mo.setResult('code', AccountConst.CODE_USER_MOBILE_INVALID)
            mo.setResult('info', '用户未绑定手机号！')
            return
        for userId in AccountModel.get_mobile_user_set(mobile):
            TyContext.MySqlSwap.checkUserDate(userId)
            accountInfo = AccountModel.get_user_brief_info(userId)
            userList.append(accountInfo)
        mo.setResult('code', 0)
        # mo.setResult('token', token)
        mo.setResult('userList', userList)
        return mo

    @classmethod
    def sendSms2user(cls, userId, mobile, content, mo):
        TyContext.ftlog.info(cls.__name__, 'sendSms2user-> userId=%s' % userId, ' mobile=%s' % mobile,
                             ' content=%s' % content)
        sdk_type = 'tuyoo'
        if not userId or userId < 0:
            mo.setResult('code', AccountConst.CODE_USER_NOT_FOUND)
            mo.setResult('info', 'token已经失效！')
            TyContext.ftlog.info(cls.__name__, 'sendSms2user->result userId error')
            return
        if not mobile:
            mobile = AccountModel.get_user_mobile(userId)
        if not mobile or len(mobile) != 11:
            mo.setResult('code', AccountConst.CODE_USER_MOBILE_REG_FAILE)
            mo.setResult('info', '手机号错误！')
            TyContext.ftlog.info(cls.__name__, 'sendSms2user->result mobile error')
            return
        isOk = TyContext.SmsDown.sendSms(mobile, content, sdk_type)
        if isOk:
            mo.setResult('code', 0)
            TyContext.ftlog.info(cls.__name__, 'sendSms2user->result success')
            mo.setResult('info', '发送短信成功！')
            return
        else:
            mo.setResult('code', 1)
            TyContext.ftlog.info(cls.__name__, 'sendSms2user->result failed')
            mo.setResult('info', '发送短信失败！')
            return

    @classmethod
    def doCheckLoginStrategy(cls, mo):
        TyContext.ftlog.debug(cls.__name__, 'doCheckLoginStrategy', mo)
        # 0 游客
        # 1 手机绑定
        # 4 sns登陆
        userType = mo.getResult('userType')
        appId = mo.getResult('appId')
        code = mo.getResult('code')
        # 登陆未成功直接返回
        if code:
            return mo
        loginStrategy = TyContext.Configure.get_global_item_json('login_strategy', {})
        appidConfig = loginStrategy.get(str(appId), None)
        if not appidConfig:
            return mo
        if appidConfig['switch'] != 'on':
            return mo
        userConfig = appidConfig.get(str(userType), None)
        if not userConfig:
            return mo
        mo = TyContext.Cls_MsgPack()
        mo.setResult('code', userConfig['code'])
        mo.setResult('info', userConfig['info'])
        return mo

    @classmethod
    def getGameLoginType(cls, mo, rparams):
        appId = rparams.get('appId', '9999')
        config = {}
        for key in ['clientId', 'packageName']:
            config = TyContext.Configure.get_game_item_json(appId, 'gameLoginConfig:%s' % rparams.get(key, ''), {})
            if config:
                break
        if not config:
            mo.setResult('code', 2)
            mo.setResult('info', '当前游戏未配置登陆方式')
            return
        mo.setResult('code', 0)
        mo.setResult('config', config)

    @classmethod
    def getLoginType(cls, mo, rparams):
        TyContext.ftlog.debug(cls.__name__, 'doGetLoginType', rparams)
        package = rparams.get('package', '')
        clientSdk = rparams.get('clientSdk', '')

        def getParams(rparams):
            keys = ['appId', 'mac', 'androidId', 'clientId', 'package', 'uuid', 'imei']
            for key in keys:
                param = rparams.get(key, '')
                if param:
                    yield param

        appId = rparams.get("appId", "9999")
        loginConfig = TyContext.Configure.get_game_item_json(appId, "sdkLoginConfig", {})
        for key in getParams(rparams):
            paramConfig = filter(lambda x: key in x.values(), loginConfig)
            if paramConfig:
                paramConfig = paramConfig[0]
                break
        if not paramConfig:
            mo.setResult('code', 2)
            mo.setResult('info', '服务端未指定登陆方式')
            return
        mo.setResult('code', 0)
        mo.setResult('tips', paramConfig.get('tips'))
        mo.setResult('sdks', paramConfig.get('sdks'))
        mo.setResult('local', paramConfig.get('local'))
        mo.setResult('single', paramConfig.get('single'))
        mo.setResult('account', paramConfig.get('showEntryPwd'))
        mo.setResult('snsIdVisible', paramConfig.get('snsIdVisible'))

    @classmethod
    def doCheckBindStateByMobile(cls, mo, rpath):
        if not AccountVerify.sing_verify(rpath):
            mo.setResult('code', -1)
            mo.setResult('info', "签名错误！")
            return
        rparam = TyContext.RunHttp.convertArgsToDict()
        mobile = rparam.get('mobile', '')
        if not mobile:
            mo.setResult('code', -2)
            mo.setResult('info', "参数错误！")
            return
        mo.setResult('code', 0)
        if not AccountModel.get_mobile_bind_user(mobile) or not AccountModel.get_mobile_user_set(mobile):
            mo.setResult('isBind', False)
        else:
            mo.setResult('isBind', True)

    @classmethod
    def doWxActBindByOpenId(cls, mo, rpath):
        if not cls.externVerify(rpath):
            mo.setResult('info', "验签失败")
            mo.setResult('code', 1)
            return mo
        rparam = TyContext.RunHttp.convertArgsToDict()
        userId = rparam.get('userId', "")
        openId = rparam.get('openId', "")
        nickName = rparam.get('nickName', "")
        try:
            tyId = int(userId)
            userId = AccountLogin.__find_userid_by_tyid__(tyId)
            if userId <= 0:
                mo.setResult('code', 5)
                mo.setResult('info', '该ID未注册！')
                return mo
        except:
            mo.setResult('info', '用户ID只能为数字，请重新输入!')
            mo.setResult('code', 5)
            return mo
        if not userId or not openId or not nickName:
            mo.setResult('info', "参数错误！")
            mo.setResult('code', 2)
            return mo
        _bindedId = TyContext.RedisUserKeys.execute('GET', 'wxOpenIdmap:%s' % openId)
        if _bindedId:
            mo.setResult('info', '该微信已经绑定过游戏账号')
            mo.setResult('code', 5)
            return mo
        name = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'name')
        if str.strip(str(name)) != str(nickName):
            mo.setResult('info', '用户名与用户ID不匹配')
            mo.setResult('code', 4)
            return mo
        if AccountModel.is_user_bind_with_wxopenId(userId):
            mo.setResult('info', "该用户已绑定过微信账号")
            mo.setResult('code', 3)
            return mo
        AccountModel.bind_user_by_wxopenId(userId, openId)
        mo.setResult('info', "绑定成功！")
        mo.setResult('code', 0)

    @classmethod
    def doWxActCheckBindState(cls, mo, rpath):
        if not cls.externVerify(rpath):
            mo.setResult('info', "验签失败")
            mo.setResult('code', 1)
            return mo
        rparam = TyContext.RunHttp.convertArgsToDict()
        userId = rparam.get('userId', "")
        openId = rparam.get('openId', "")
        needUnbind = rparam.get('unbind', False)
        if not userId:
            mo.setResult('info', "参数错误！")
            mo.setResult('code', 2)
            return mo
        if needUnbind:
            TyContext.RedisUserKeys.execute('DEL', 'wxOpenIdmap:%s' % openId)
            TyContext.RedisUser.execute(userId, 'HDEL', 'user:' + str(userId), 'wxOpenId')
        ret = AccountModel.is_user_bind_with_wxopenId(userId)
        mo.setResult('isBind', ret)
        mo.setResult('code', 0)
        return mo

    @classmethod
    def doWxActSendHBToUser(cls, mo, rpath):
        if not AccountVerify.sing_verify(rpath) and False:
            mo.setResult('info', "验签失败")
            mo.setResult('code', 1)
            return mo
        rparam = TyContext.RunHttp.convertArgsToDict()
        userId = rparam.get('userId', "")
        amount = rparam.get('amount', "")
        wishing = rparam.get('wishing', "")
        act_name = rparam.get('act_name', "")
        remark = rparam.get("remark", "")
        send_name = rparam.get('send_name', "")
        appId = rparam.get('appId', "9999")
        weChatAccount = rparam.get('wxappid', 'wxb01a635a437adb75')
        config = TyContext.Configure.get_global_item_json('wx_hb_config', {})
        wxHbConfig = config.get(weChatAccount, {})
        if not wxHbConfig:
            wxHbConfig = config.get(appId, {})
        if not userId or not amount:
            mo.setResult('info', "参数错误！")
            mo.setResult('code', 2)
            return mo
        if AccountModel.is_user_bind_with_wxopenId(userId):
            re_openid = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'wxOpenId')
        else:
            mo.setResult('info', "该用户未绑定公众号")
            mo.setResult('code', 3)
            return mo
        if not act_name:
            act_name = wxHbConfig.get('act_name', "")
            wishing = wxHbConfig.get('wishing', "")
            remark = wxHbConfig.get('remark', "")
            send_name = wxHbConfig.get('send_name', "")
            ip = wxHbConfig.get('ip', '')
        mch_id = wxHbConfig.get('mch_id')
        partnerKey = wxHbConfig.get('partnerKey')
        wxappid = wxHbConfig.get('wxappid')
        prepayUrl = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/sendredpack'
        postparams = {}
        postparams['nonce_str'] = "sdfadfasfdsafdsafdsafadsf"
        from datetime import datetime
        now = datetime.now()
        import random, string
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        postparams['mch_billno'] = mch_id + now.strftime('%Y%m%d') + salt  # 商户订单号
        postparams['mch_id'] = mch_id  # 商户号
        postparams['wxappid'] = wxappid
        postparams['send_name'] = send_name  # 商户名称 发送红包者
        postparams['re_openid'] = str(re_openid)  # 接受红包用户Id
        postparams['total_amount'] = amount  # 金额，分
        postparams['wishing'] = wishing  # 红包祝福语
        postparams['client_ip'] = ip  # 本机IP
        postparams['total_num'] = '1'  # 红包人数
        postparams['act_name'] = act_name  # 活动名称
        postparams['remark'] = remark  # 活动备注

        calStr = '&'.join(k + "=" + str(postparams[k]) for k in sorted(postparams.keys())) + '&key=' + partnerKey
        signValue = md5(calStr).hexdigest().upper()
        postparams['sign'] = signValue
        from xml.etree import ElementTree
        rootXml = ElementTree.Element('xml')
        for i in postparams:
            element = ElementTree.SubElement(rootXml, i)
            element.text = postparams[i]
        postXml = ElementTree.tostring(rootXml, encoding='utf-8')
        apiclient_cert = './cacert_weixin/%s/apiclient_cert.pem' % wxappid
        apiclient_key = './cacert_weixin/%s/apiclient_key.pem' % wxappid
        response = queryHttpSsl(prepayUrl, postXml.encode('utf-8'), sslhttp.getResourcePath(apiclient_cert),
                                sslhttp.getResourcePath(apiclient_key))
        xmlResponse = ElementTree.fromstring(response)
        wxHbMsgConfig = TyContext.Configure.get_global_item_json('wx_hb_erro_msg', {})
        if 'SUCCESS' == xmlResponse.find('return_code').text:
            if 'SUCCESS' == xmlResponse.find('result_code').text:
                TyContext.ftlog.info('doWxActSendHBToUser,userId,', userId, 'amount', amount, '')
                mo.setResult('info', "红包发送成功！")
                mo.setResult('code', 0)
            else:
                errMsg = wxHbMsgConfig.get(xmlResponse.find('err_code').text, "")
                if not errMsg:
                    errMsg = wxHbMsgConfig.get("DEFAULT", "")
                mo.setResult('info', errMsg)
                mo.setResult('code', 4)
                TyContext.ftlog.info('doWxActSendHBToUser, failed,userId', userId, 'amount', amount, 'reason',
                                     xmlResponse.find('err_code').text)
        else:
            errMsg = wxHbMsgConfig.get(xmlResponse.find('err_code').text, "")
            if not errMsg:
                errMsg = wxHbMsgConfig.get("DEFAULT", "")
            mo.setResult('info', errMsg)
            mo.setResult('code', 4)
            TyContext.ftlog.info('doWxActSendHBToUser, failed,userId', userId, 'amount', amount, 'reason',
                                 xmlResponse.find('err_code').text)
        return mo

    @classmethod
    def sendAwardToUser(cls, mo, rpath):
        config = TyContext.Configure.get_global_item_json('1shang_award_config', {})
        isTest = config.get('isTest', False)
        if not isTest and not AccountVerify.sing_verify(rpath):
            mo.setResult('info', "验签失败")
            mo.setResult('code', 1)
            return mo
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('sendAwrdToUser,params', rparam)
        userId = rparam.get('userId', "")
        mobile = rparam.get('mobile', "")
        prizeId = rparam.get('prizeId', "")
        if not mobile or not prizeId:
            mo.setResult('info', "参数错误")
            mo.setResult('code', 2)
            return mo
        appId = rparam.get('appId', "9999")
        clientId = rparam.get('clientId', "Android_3.701_360.360,yisdkpay.0-hall6.360.day")
        postparam = {}
        config = config.get(appId, {})
        userId = config.get('userId', "")
        postparam['userId'] = userId
        postparam['orderId'] = config.get('orderId', "")
        postparam['prizeId'] = prizeId
        prodConfig = config.get('prod', {})
        prizePriceTypeId = prodConfig.get(prizeId, "")
        postparam['prizePriceTypeId'] = prizePriceTypeId
        postparam['phone'] = mobile
        customOrderCode = TyContext.ServerControl.makeChargeOrderIdV4(userId, appId, clientId)
        postparam['customOrderCode'] = customOrderCode
        postparam['operation'] = 'recharge'
        postparam['service'] = 'getAward'
        md5key = config.get('key')
        query = "".join(str(postparam[k]) for k in sorted(postparam.keys()))
        m = md5()
        m.update(query + md5key)
        sign = m.hexdigest().lower()
        postparam['sign'] = sign
        prepayUrl = "http://api.1shang.com/service/apiService?"
        response, _ = TyContext.WebPage.webget(prepayUrl, postdata_=postparam)
        import json
        datas = json.loads(response)
        if datas.get('result') == "10000":
            mo.setResult("info", datas.get('message', "请求成功"))
            mo.setResult('customOrderCode', customOrderCode)
            mo.setResult('code', 0)
            TyContext.ftlog.info('sendAwrdToUser,success,customOrderCode', customOrderCode, 'prizeId', prizeId,
                                 'ishang_uid', userId)
        else:
            mo.setResult("info", datas.get('message', "请求失败"))
            mo.setResult('code', 3)
            TyContext.ftlog.info('sendAwrdToUser,failed,prizeId', prizeId, '1shang_uid', userId)
        return mo

    @classmethod
    def doQuery1ShangStatus(cls, mo, rpath):
        config = TyContext.Configure.get_global_item_json('1shang_award_config', {})
        isTest = config.get('isTest', False)
        if not isTest and not AccountVerify.sing_verify(rpath):
            mo.setResult('info', "验签失败")
            mo.setResult('code', 1)
            return mo
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doQuery1ShangStatus,params', rparam)
        customOrderCode = rparam.get('customOrderCode', "")
        if not customOrderCode:
            mo.setResult('info', "参数错误")
            mo.setResult('code', 2)
            return mo
        appId = rparam.get('appId', "9999")
        config = config.get(appId, "")
        postparam = {}
        postparam['userId'] = config.get('userId')
        postparam['orderId'] = config.get('orderId')
        postparam['customOrderCode'] = customOrderCode
        postparam['service'] = 'queryStatus'
        md5key = config.get('key')
        query = "".join(str(postparam[k]) for k in sorted(postparam.keys()))
        m = md5()
        m.update(query + md5key)
        sign = m.hexdigest().lower()
        postparam['sign'] = sign
        posturl = "http://api.1shang.com/service/apiService?"
        response, _ = TyContext.WebPage.webget(posturl, postdata_=postparam)
        import json
        datas = json.loads(response)

        status = {'API_GET': "发放成功", "API_CHARGE_GET": "发放成功", 'API_ERROR': '发放失败', 'IN_CHARGE': '处理中'}

        if datas.get('result') == "10000":
            mo.setResult("info", datas.get('message'))
            mo.setResult('result', datas.get('result'))
            mo.setResult('status', status.get(datas.get('status', "")))
            mo.setResult('code', 3)
            TyContext.ftlog.info('doQuery1ShangStatus,success,status', datas.get('status'), 'customOrderCode',
                                 datas.get('customOrderCode'))
        else:
            mo.setResult('info', datas.get('message'))
            mo.setResult('result', datas.get('result'))
            mo.setResult('status', status.get(datas.get('status', "")))
            mo.setResult('code', 4)
            TyContext.ftlog.info('doQuery1ShangStatus,failed,status', datas.get('status'), 'customOrderCode',
                                 datas.get('customOrderCode'))
        return mo

    @classmethod
    def doSendEmailToUser(cls, mo, rpath):
        if not AccountVerify.sing_verify(rpath) and False:  # TODO 2016年08月22日11:30:44 去掉验签限制
            mo.setResult('code', '-1')
            mo.setResult('info', "验签失败")
            return
        rparam = TyContext.RunHttp.convertArgsToDict()
        toAddr = rparam.get('toAddr')
        subject = rparam.get('subject')
        content = rparam.get('content')
        appId = rparam.get('appId', "9999")
        whatfor = rparam.get('whatfor', '')
        clientId = rparam.get('clientId', 'IOS_3.781_tuyoo.appStore,weixinPay,alipay.0-hall28.appStore.bydzz')
        if not toAddr:
            mo.setResult('code', 1)
            mo.setResult('info', "发送地址,主题，内容不可为空")
            return

        def isBindByEmail(toAddr):  # TODO 检查用户是否绑定邮箱
            return True

        if not isBindByEmail(toAddr):
            mo.setResult('code', 2)
            mo.setResult('info', "该邮箱未绑定游戏账号")
            return
        mailConfig = TyContext.Configure.get_game_item_json(appId, "emailConfig", {})
        subject = mailConfig.get('subject') if not subject else subject
        content = mailConfig.get('content') if not content else content
        sendSuccTip = mailConfig.get('succTips')
        userId = AccountLogin.__find_userid_by_account__(toAddr)
        userName = '小明'  # TODO 获取用户名
        vcode = TyContext.ServerControl.makeChargeOrderIdV4(userId, appId, clientId)
        rkey = 'email:' + toAddr
        validTime = int(mailConfig.get('expire', 10))
        TyContext.RedisMix.execute('SET', rkey, vcode)
        TyContext.RedisMix.execute('EXPIRE', rkey, validTime * 60)
        verifyUrl = TyContext.TYGlobal.http_sdk() + '/open/v4/user/verifyEmail?email=%s&vcode=%s&whatfor=%s&appId=%s' % (
            toAddr, vcode, whatfor, appId)
        if whatfor == 'changePwd':
            tips = '重置%s的密码' % userName
        elif whatfor == 'changeEmail':
            tips = '更换%s的密保邮箱'
        else:
            tips = '邮箱验证'
        htmlcontent = content % {'dosth': tips, 'url': verifyUrl}
        TyContext.ftlog.debug('sendEmailToUser,to:', toAddr, "verifyUrl", verifyUrl)
        if not AccountUtil.sendMail(toAddr, subject, htmlcontent, appId=appId):
            mo.setResult('code', 3)
            mo.setResult('info', "邮件发送失败，请稍后重试")
        else:
            mo.setResult('code', 0)
            mo.setResult('info', sendSuccTip % validTime)

    @classmethod
    def verifyEmail(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        vcode = rparam.get('vcode')
        appId = rparam.get('appId', '9999')
        mailConfig = TyContext.Configure.get_game_item_json(appId, "emailConfig", {})
        tipConfigSucc = mailConfig.get('bindTipsSucc')
        tipConfigFail = mailConfig.get('bindTipsFail')
        if not vcode:
            return tipConfigFail % {'reason': "参数不合法"}
        mail = rparam.get('email')
        rkey = 'email:' + mail
        if vcode != TyContext.RedisMix.execute('GET', rkey):
            return tipConfigFail % {'reason': '验证此链接已超过有效期，请重试。'}
        TyContext.RedisMix.execute('DEL', rkey)
        userName = '小明'
        whatfor = rparam.get('whatfor')
        if whatfor == 'changePwd':
            tips = '您的游戏账号%s的密保邮箱已成功更换为%s' % (userName, mail)
            tipConfigSucc = tipConfigSucc % tips
            return tipConfigSucc
        elif whatfor == 'changeEmail':
            tips = '您的游戏账号%s的密码已重置成功' % userName
            tipConfigSucc = tipConfigSucc % tips
            return tipConfigSucc
        else:
            pass

        return tipConfigSucc % "邮箱绑定成功"

    @classmethod
    def getWxShareConfig(cls, rpath, mo):
        rparams = TyContext.RunHttp.convertArgsToDict()
        appId = rparams.get('appId', '9999')
        config = {}
        for key in ['clientId', 'packageName']:
            config = copy.deepcopy(
                TyContext.Configure.get_game_item_json(appId, 'wxShareConfig:%s' % rparams.get(key, ''), {}))
            if config:
                break
        if config:
            import random
            config['text'] = random.choice(config['text'].split('|'))
            config['title'] = config['text']
            config['wechatid'] = random.choice(config['wechatid'])['share_wxid']
            mo.setResult('code', 0)
        else:
            mo.setResult('code', 2)
        for key in ['wechatid', 'text']:
            if not config.get(key):
                mo.setResult('code', 2)
                mo.setResult('shareConfig', {})
                return
        mo.setResult('shareConfig', config)
