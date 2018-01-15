# -*- coding=utf-8 -*-

# Author:        zhaoqinghui@hoolai.com
# Company:       Hoolai.Inc
# Created:       2013年01月25日 星期六 00时34分53秒
# FileName:      account.py
# Class:         Account

from hashlib import md5
from string import strip

import datetime
import json
import random

from tyframework.context import TyContext
from tysdk.entity.user.account360 import Account360
from tysdk.entity.user.accountmomo import AccountMomo
from tysdk.entity.user_common.account_helper import AccountHelper
from tysdk.entity.user_common.constants import AccountConst
from tysdk.entity.user_common.username import UsernameGenerator
from tysdk.entity.user_common.verify import AccountVerify

CODE_USER_PARAM_ERROR = -2  # 客户端参数错误
CODE_USER_VERSION_ERROR = -1  # 客户端参数错误
CODE_USER_SUCCESS = 0  # 登录成功
CODE_USER_PWD_ERROR = 1  # 用户名、密码错误
CODE_USER_MAIL_EXITS = 2  # 注册或绑定的邮箱已经存在
CODE_USER_DEV_REG_FAILE = 3  # 设备ID注册失败
CODE_USER_MAIL_REG_FAILE = 4  # Mail注册失败
CODE_USER_SNS_REG_FAILE = 5  # SNS ID注册失败
CODE_USER_OLD_PWD_ERROR = 6  # 密码不一致
CODE_USER_MAIL_BINDED = 7  # 邮箱已经绑定
CODE_USER_MOBILE_BINDED = 8  # 手机已经绑定
CODE_USER_GUEST_REG_FAILE = 9  # 游客注册失败
CODE_USER_LOGIN_FORBID = 10  # 禁止登陆

USER_TYPE_DEVICE = 0  # 设备注册用户,试玩用户
USER_TYPE_REGISTER = 1  # 正式注册用户,mail注册用户
USER_TYPE_SNS = 2  # SNS用户,sns id注册用户
USER_TYPE_MOBILE = 3  # 正式注册用户,手机注册用户

######################################################################
# redis 数据库定义
#
# 用户-基本信息：采用HASHES实现,
#     Key      user:<userid>  
#     Value    mail(str, 用户邮箱)
#              mdevid(str, 手持设备ID)
#              isbind (int, 0-没有绑定 1-已经绑定)
#              passwd(str, 密码)
#              name(str, 昵称)
#              purl(str, 头像url)
#              coin(int, 金币)
#              snsid (str, 第三方登录用户ID)
#              state (int, 用户状态)
#              sex (int, 性别 0-女 1-男)
#              address (str, 用户所在的地域)
#              payCount (int, 充值的次数) 
#              source (str) 用户推广的来源
#              snsinfo (str,用于保存SNS用户补充的联系方式)
#
# 用户-关联信息-SNS第三方ID：采用Key-Value实现
#     Key      snsidmap:<snsid>  
#     Value    <userid> (int, 系统用户ID)
#
# 用户-关联信息-MAIL：采用Key-Value实现
#     Key      mailmap:<mail>
#     Value    <userid> (int, 系统用户ID)
#
# 用户-关联信息-设备ID：采用Key-Set实现
#     Key      devidmap:<devid>  
#     Value    Set[<userid>, <userid>] (int, 系统用户ID)
#
######################################################################
USER_DATA_KEYS = ['password', 'mdevid', 'isbind', 'snsId', 'name', \
                  # 'source', 'coin', 'purl', 'address', 'sex', \
                  'source', 'purl', 'address', 'sex', \
                  'state', 'payCount', 'snsinfo', 'vip', 'dayang', \
                  'idcardno', 'phonenumber', 'truename', 'detect_phonenumber', 'email', \
                  'createTime', 'userAccount', 'clientId', 'appId', 'bindMobile']


######################################################################
# 登录过程的主要逻辑实现
#
######################################################################
class Account():
    # ---------------------------------------------------------------------------------
    # 按照途游的加密方式解码一个键值
    # 有效返回解码后的值，并修改原有键值内容
    # 无效返回None
    # ---------------------------------------------------------------------------------
    @classmethod
    def decodeItem(self, msg, key):
        keyOld = key + '____'
        valueOld = ''
        value = ''
        try:
            if msg.getParam(keyOld) != None:
                return msg.getParamStr(key)

            valueOld = strip(msg.getParamStr(key), '')
            value = valueOld
            if len(valueOld) > 0 and 0:
                #                 desobj = DES.new('tuyoocom', DES.MODE_ECB)
                #                 value = base64.b64decode(valueOld)
                #                 value = desobj.decrypt(value)
                #                 postail = value.find('~POKER201309031548')
                #                 poshead = value.find('TUYOO~')
                #                 if poshead == 0 and postail > 6:
                #                     value = value[6:postail]
                pass
            msg.setParam(key, value)
            msg.setParam(keyOld, valueOld)
            return value
        except Exception, e:
            msg.setParam(key, '')
            msg.setParam(keyOld, valueOld)
            TyContext.ftlog.error('ERROR, Account3.decodeItem', e, value)
            TyContext.ftlog.exception()
        return None

    # ---------------------------------------------------------------------------------
    # 取得参数appId,参数中得appId与gameId含义一致
    # 有效返回正确的gameId
    # 无效返回0
    # ---------------------------------------------------------------------------------
    @classmethod
    def checkAppId(self, msg):
        appId = msg.getParam('gameId')
        if appId == None:
            appId = msg.getParam('appId')
            if appId == None:
                appId = 0
        # TODO 客户端BUGFIX，象棋的一个终端未传递appid
        if appId == '':
            clientid = msg.getParamStr('clientId', 'none')
            datas = TyContext.Configure.get_global_item_json('bug_fix_clientid_appid', {})
            appId = datas.get(clientid, 0)
            msg.setParam('gameId', appId)
            TyContext.ftlog.error('checkAppId appId empty bugfix->', clientid, appId)
        appId = int(appId)
        msg.setParam('appId', appId)
        return appId

    # ---------------------------------------------------------------------------------
    # 取得参数gameId,参数中得appId与gameId含义一致
    # 有效返回正确的gameId
    # 无效返回0
    # ---------------------------------------------------------------------------------
    @classmethod
    def checkClientId(cls, msg):
        clientId = cls.decodeItem(msg, 'clientId')
        if clientId:
            try:
                # 获取白名单的clientid
                is_check_waived = TyContext.Configure.get_global_item_int('clientid.waived.confirm', 1)
                if is_check_waived:
                    all_waived_clientids = TyContext.Configure.get_configure_json('clientid.number.map', {})
                    if all_waived_clientids:
                        clientIdNum = all_waived_clientids.get(clientId)
                        if clientIdNum is None:
                            return False
                if clientId and TyContext.RedisForbidden.execute('EXISTS', 'forbidden:cid:' + str(clientId)):
                    return False
            except:
                TyContext.ftlog.error('checkClientId error, clientId=', clientId)
                pass
            infos = clientId.split('_')
            if len(infos) > 2:
                try:
                    msg.setParam('clientSystem', infos[0])
                    msg.setParam('clientVersion', TyContext.ClientUtils.getVersionFromClientId(clientId))
                    msg.setParam('clientChannel', infos[2])
                    return True
                except:
                    TyContext.ftlog.error('checkClientId error, clientId=', clientId)
                    pass
        return False

    # ---------------------------------------------------------------------------------
    # 检查device id的有效性
    # 有效返回正确的device id
    # 无效返回None
    # ---------------------------------------------------------------------------------
    @classmethod
    def checkDeviceId(cls, msg):
        deviceId = cls.decodeItem(msg, 'deviceId')
        if deviceId != None and len(deviceId) >= 32:
            return True
        return False

    @classmethod
    def checkSnsId(cls, msg):
        snsId = cls.decodeItem(msg, 'snsId')
        if snsId != None and len(snsId) > 0:
            return True
        return False

    # ---------------------------------------------------------------------------------
    # 取得参数mail
    # 有效返回正确的mail
    # 无效返回None
    # ---------------------------------------------------------------------------------
    @classmethod
    def checkUserAccount(self, msg):
        account = msg.getParam('userAccount')
        if account:
            try:
                account = strip(unicode(account, encoding='utf-8')).lower()
            except:
                TyContext.ftlog.exception()
                account = repr(account)
            if len(account) > 0:
                return account
        return None

    # ---------------------------------------------------------------------------------
    # 取得参数mail
    # 有效返回正确的mail
    # 无效返回None
    # ---------------------------------------------------------------------------------
    @classmethod
    def checkUserEmail(self, msg):
        mail = msg.getParam('email')
        if mail:
            # mail = strip(unicode(mail)).lower()
            mail = strip(unicode(mail))
            if len(mail) > 0:
                return mail
        return None

    # ---------------------------------------------------------------------------------
    # 取得参数password
    # 有效返回正确的mail
    # 无效返回None
    # ---------------------------------------------------------------------------------
    @classmethod
    def checkPassword(self, msg, key='userPwd'):
        pwd = msg.getParam(key)
        if pwd and len(pwd) > 0:
            return pwd
        else:
            return None

    @classmethod
    def checkUserId(cls, msg):
        userId = cls.decodeItem(msg, 'userId')
        if userId != None and len(userId) > 0:
            return True
        return False

    # ---------------------------------------------------------------------------------
    # 直接更新用户信息
    # ---------------------------------------------------------------------------------
    @classmethod
    def updateUserBaseInfo(self, userId, msg):
        TyContext.ftlog.debug('updateUserBaseInfo msg=', msg.packJson())
        ukvs = []

        sex = self.getIntegerParam(msg, 'sex', -1)
        if sex == 1 or sex == 0:
            ukvs.append('sex')
            ukvs.append(int(sex))

        name = self.getStringParam(msg, 'name')
        if len(name) > 0:
            newNameIs360Default = Account360.isDefault360Username(name)
            if newNameIs360Default:
                oldname = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'name')
                if oldname is None or Account360.isDefault360Username(oldname):
                    if sex not in ('0', '1'):
                        sex = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sex')
                    name = UsernameGenerator.getInstance().generate(sex)
                else:
                    name = None
            else:
                pass
            if name != None:
                ukvs.append('name')
                ukvs.append(name)

        address = self.getStringParam(msg, 'address')
        if len(address) > 0:
            ukvs.append('address')
            ukvs.append(address)

        purl = self.getStringParam(msg, 'picUrl')
        if len(purl) > 0:
            ukvs.append('purl')
            ukvs.append(purl)

        snsinfo = self.getStringParam(msg, 'snsinfo')
        if len(snsinfo) > 0:
            ukvs.append('snsinfo')
            ukvs.append(snsinfo)
            ukvs.append('isbind')
            ukvs.append(USER_TYPE_SNS)

        idcardno = self.getStringParam(msg, 'idcardno')
        if len(idcardno) > 0:
            ukvs.append('idcardno')
            ukvs.append(idcardno)

        phonenumber = self.getStringParam(msg, 'phonenumber')
        if len(phonenumber) > 0:
            ukvs.append('phonenumber')
            ukvs.append(phonenumber)

        detect_phonenumber = self.getStringParam(msg, 'detect_phonenumber')
        if len(detect_phonenumber) > 0:
            ukvs.append('detect_phonenumber')
            ukvs.append(detect_phonenumber)

        truename = self.getStringParam(msg, 'truename')
        if len(truename) > 0:
            ukvs.append('truename')
            ukvs.append(truename)

        if len(ukvs) > 0:
            TyContext.ftlog.debug('updateUserBaseInfo->uid=', userId, 'values=', ukvs)
            TyContext.MySqlSwap.checkUserDate(userId)
            AccountHelper.restore_avatar_verify_set(userId)
            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), *ukvs)

    # ---------------------------------------------------------------------------------
    # 用户进行登录
    # ---------------------------------------------------------------------------------
    @classmethod
    def doLogin(cls, msg, mo):
        TyContext.ftlog.info('doLogin', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setError(1, 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setError(1, 'client error')
            return

        # 设备ID检查
        cls.checkDeviceId(msg)

        # 检查SNS 登录
        isOK = cls.checkSnsId(msg)
        if isOK:
            snsId = msg.getParamStr('snsId')
            # 360 第一次登录，特殊处理
            if snsId.startswith('360:') and len(snsId) > 20:
                ret = Account360.doGetUserInfo(snsId, msg)
                if ret != True:
                    mo.setError(2, 'register by sns id fail')
                    return
                else:
                    snsId = msg.getParamStr('snsId')
            elif snsId.startswith('momo:'):
                ret = AccountMomo.doGetUserInfo(snsId, msg)
                if not ret:
                    code = msg.getParamInt('code', 2)
                    mo.setError(code, 'fail')
                    return

            # 处理SNS登录
            userId = cls.findUserIdBySnsId(snsId)
            if userId > 0:
                if cls.__checkForbidden(userId, msg, mo):
                    return

                # 此SNS ID 已经注册了平台账户,同时更新用户信息
                TyContext.MySqlSwap.checkUserDate(userId)
                AccountHelper.restore_avatar_verify_set(userId)
                cls.updateUserBaseInfo(userId, msg)
                TyContext.UserProps.check_data_update_hall(userId, appId)
                cls.fillUserLoginInfo(msg, mo, userId, True, False)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_SNS], userId, appId,
                    msg.getParamStr('clientId'), snsId, 0, devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_SNS,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                #                 Report.recoderUserLogin( appId, userId, USER_TYPE_SNS)
                return
            else:
                # 在平台注册此SNS ID账户
                userId = cls.createNewUser(msg, USER_TYPE_SNS)
                cls.fillUserLoginInfo(msg, mo, userId, True, True)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_SNS], userId, appId,
                    msg.getParamStr('clientId'), snsId, 0, devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_SNS,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                return

        userAccount = cls.checkUserAccount(msg)
        passWord = cls.checkPassword(msg)
        if userAccount and passWord:
            # 注册用户登录系统
            userId = cls.findUserIdByAccountPwd(userAccount, passWord)
            if userId > 0:
                TyContext.UserProps.check_data_update_hall(userId, appId)
                cls.fillUserLoginInfo(msg, mo, userId, True, False)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_REGISTER], userId, appId,
                    msg.getParamStr('clientId'), userAccount, 0, devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_REGISTER,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                #                 Report.recoderUserLogin( appId, userId, USER_TYPE_REGISTER)
                return
            mo.setError(3, '通行证或密码错误，请重新输入！')
            return
        else:
            mo.setError(1, '通行证或密码错误，请重新输入！')
            return

    # ---------------------------------------------------------------------------------
    # 用户snsId进行登录
    # ---------------------------------------------------------------------------------
    @classmethod
    def doLoginBySnsId(cls, msg, mo):
        TyContext.ftlog.info('doLoginBySnsId', msg.packJson())

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        # 设备ID检查
        # isOK = cls.checkDeviceId(msg)
        # if not isOK:
        #    mo.setResult('code', 1)
        #    mo.setResult('info', 'deviceId error')
        #    return

        # 检查SNS 登录
        isOK = cls.checkSnsId(msg)
        if isOK:
            snsId = msg.getParamStr('snsId')
            # 360 第一次登录，特殊处理
            if snsId.startswith('360:') and len(snsId) > 20:
                ret = Account360.doGetUserInfo(snsId, msg)
                if ret != True:
                    mo.setResult('code', 2)
                    mo.setResult('info', 'register by sns id fail')
                    return
                else:
                    snsId = cls.getStringParam(msg, 'snsId')
            elif snsId.startswith('momo:'):
                ret = AccountMomo.doGetUserInfo(snsId, msg)
                if not ret:
                    code = msg.getParamInt('code', 2)
                    mo.setError(code, 'fail')
                    return

            # 处理SNS登录
            userId = cls.findUserIdBySnsId(snsId)
            if userId > 0:
                if cls.__checkForbidden(userId, msg, mo):
                    return
                # 此SNS ID 已经注册了平台账户,同时更新用户信息
                TyContext.MySqlSwap.checkUserDate(userId)
                AccountHelper.restore_avatar_verify_set(userId)
                dbPassword = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'password')
                if dbPassword != None:
                    dbPassword = str(dbPassword)
                if dbPassword == None or len(dbPassword) == 0:
                    pwd = 'ty' + str(random.randint(100000, 999999))
                    TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId),
                                                'password', pwd,
                                                'userSignature', AccountVerify.md5(pwd))
                cls.updateUserBaseInfo(userId, msg)
                TyContext.UserProps.check_data_update_hall(userId, appId)
                cls.fillUserLoginInfoNew(msg, mo, userId, True, False)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_SNS], userId, appId,
                    msg.getParamStr('clientId'), snsId, 0, devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_SNS,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                #                 Report.recoderUserLogin( appId, userId, USER_TYPE_SNS)
                return
            else:
                currentUserId = cls.getIntegerParam(msg, 'userId')
                if currentUserId > 0:
                    TyContext.MySqlSwap.checkUserDate(currentUserId)
                    AccountHelper.restore_avatar_verify_set(currentUserId)
                    TyContext.RedisUser.execute(currentUserId, 'HMSET', 'user:' + str(currentUserId), 'snsId', snsId)
                    TyContext.RedisUserKeys.execute('SET', 'snsidmap:' + snsId, currentUserId)
                    cls.updateUserBaseInfo(currentUserId, msg)
                    TyContext.UserProps.check_data_update_hall(currentUserId, appId)
                    cls.fillUserLoginInfoNew(msg, mo, currentUserId, True, False)
                    TyContext.BiReport.report_bi_sdk_login(
                        AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_SNS], currentUserId, appId,
                        msg.getParamStr('clientId'), snsId, 0, devId=msg.getParamStr('deviceId'))
                    TyContext.BiReport.user_login(appId, userId, USER_TYPE_SNS,
                                                  msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                                  msg.getParamStr('deviceId'),
                                                  params=TyContext.RunHttp.convertArgsToDict(),
                                                  rpath=TyContext.RunHttp.get_request_path())
                    #                    Report.recoderUserLogin( appId, currentUserId, USER_TYPE_SNS)
                    return
                # 在平台注册此SNS ID账户
                pwd = 'ty' + str(random.randint(100000, 999999))
                msg.setParam('userPwd', pwd)
                userId = cls.createNewUser(msg, USER_TYPE_SNS)
                TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'isbind', USER_TYPE_SNS)
                cls.fillUserLoginInfoNew(msg, mo, userId, True, True)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_SNS], userId, appId,
                    msg.getParamStr('clientId'), snsId, 0, devId=msg.getParamStr('deviceId'))
                return

        else:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'snsId missing')
            return

    # ---------------------------------------------------------------------------------
    # 用户email进行登录
    # ---------------------------------------------------------------------------------
    @classmethod
    def doLoginByEmail(cls, msg, mo):
        TyContext.ftlog.info('doLoginByEmail', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        # 设备ID检查
        # isOK = cls.checkDeviceId(msg)
        # if not isOK:
        #    mo.setResult('code', 1)
        #    mo.setResult('info', 'deviceId error')
        #    return

        userEmail = cls.checkUserEmail(msg)
        passWord = cls.checkPassword(msg)
        if userEmail and passWord:
            # 注册用户登录系统
            userId = cls.findUserIdByEmailPwd(userEmail, passWord)
            # 这里判断重度游戏那边的邮箱用户
            if userId <= 0:
                userId = cls.findUserIdByAccountPwd(userEmail, passWord)
            if userId > 0:
                if cls.__checkForbidden(userId, msg, mo):
                    return
                TyContext.UserProps.check_data_update_hall(userId, appId)
                cls.fillUserLoginInfoNew(msg, mo, userId, True, False)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_REGISTER], userId, appId,
                    msg.getParamStr('clientId'), msg.getParamStr('email'), 0,
                    devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_REGISTER,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                #                 Report.recoderUserLogin( appId, userId, USER_TYPE_REGISTER)
                return
            mo.setResult('code', CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            return
        else:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            return

    # ---------------------------------------------------------------------------------
    # 用户短信进行登录，返回客户端userId、userPwd
    # ---------------------------------------------------------------------------------
    @classmethod
    def doLoginSms(cls, msg, mo):
        TyContext.ftlog.info('doLoginSms', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        # 设备ID检查
        # isOK = cls.checkDeviceId(msg)
        # if not isOK:
        #    mo.setResult('code', 1)
        #    mo.setResult('info', 'deviceId error')
        #    return


        userId = cls.getIntegerParam(msg, 'userId')
        if userId > 0:
            if cls.__checkForbidden(userId, msg, mo):
                return

            TyContext.MySqlSwap.checkUserDate(userId)
            AccountHelper.restore_avatar_verify_set(userId)
            dbPassword, bindMobile, isbind = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId),
                                                                         'password', 'bindMobile', 'isbind')
            # TyContext.ftlog.info('doLoginSms', 'bindMobile',bindMobile,'isbind',isbind)
            if bindMobile != None and isbind != None and int(isbind) == 3:
                mo.setResult('code', 0)
                mo.setResult('mobile', bindMobile)
                mo.setResult('userPwd', dbPassword)
                TyContext.UserProps.check_data_update_hall(userId, appId)
                cls.fillUserLoginInfoNew(msg, mo, userId, True, False)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_MOBILE], userId, appId,
                    msg.getParamStr('clientId'), '', 0,
                    devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_MOBILE,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                #                 Report.recoderUserLogin( appId, userId, USER_TYPE_MOBILE)
                return
            else:
                mo.setResult('code', CODE_USER_MOBILE_BINDED)
                mo.setResult('info', '手机已绑定其他账号')
                return
        else:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'userId incorrect')
            return

    # ---------------------------------------------------------------------------------
    # 用户手机号进行登录
    # ---------------------------------------------------------------------------------
    @classmethod
    def doLoginByMobile(cls, msg, mo):
        TyContext.ftlog.info('doLoginByMobile', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        # 设备ID检查
        # isOK = cls.checkDeviceId(msg)
        # if not isOK:
        #    mo.setResult('code', 1)
        #    mo.setResult('info', 'deviceId error')
        #    return


        chkMobile = msg.getParam('mobile')
        if chkMobile == None or len(str(chkMobile)) != 11:
            mo.setResult('code', 2)
            mo.setResult('info', 'mobile num is empty or not correct')
            return

        passWord = cls.checkPassword(msg)
        if chkMobile and passWord:
            # 注册用户登录系统
            userId = cls.findUserIdByMobilePwd(chkMobile, passWord)
            if userId > 0:
                if cls.__checkForbidden(userId, msg, mo):
                    return
                TyContext.UserProps.check_data_update_hall(userId, appId)
                cls.fillUserLoginInfoNew(msg, mo, userId, True, False)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_MOBILE], userId, appId,
                    msg.getParamStr('clientId'), chkMobile, 0,
                    devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_MOBILE,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                #                 Report.recoderUserLogin( appId, userId, USER_TYPE_MOBILE)
                return
            mo.setResult('code', CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            return
        else:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            return

    # ---------------------------------------------------------------------------------
    # 游客进行登录
    # ---------------------------------------------------------------------------------
    @classmethod
    def doLoginByGuest(cls, msg, mo):
        TyContext.ftlog.info('doLoginByGuest', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        # 设备ID检查
        isOK = cls.checkDeviceId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'deviceId error')
            return

        # 判断deviceId是否已注册过
        deviceId = cls.decodeItem(msg, 'deviceId')

        userId = cls.findUserIdByNewDeviceId(deviceId)
        if userId > 0:
            if cls.__checkForbidden(userId, msg, mo):
                return

            TyContext.MySqlSwap.checkUserDate(userId)
            AccountHelper.restore_avatar_verify_set(userId)
            TyContext.ftlog.info('doLoginByGuest->deviceId is exist', 'deviceId=', deviceId, 'userId=', userId)
            TyContext.UserProps.check_data_update_hall(userId, appId)
            cls.fillUserLoginInfoNew(msg, mo, userId, True, False)
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_DEVICE], userId, appId,
                msg.getParamStr('clientId'), '', 0, devId=deviceId)
            TyContext.BiReport.user_login(appId, userId, USER_TYPE_DEVICE,
                                          msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                          msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                          rpath=TyContext.RunHttp.get_request_path())
            #             Report.recoderUserLogin( appId, userId, USER_TYPE_DEVICE)
            return

        # 游客初次登陆注册,注册后,返回初次注册的信息
        pwd = 'ty' + str(random.randint(100000, 999999))
        msg.setParam('userPwd', pwd)
        mo.setResult('userPwd', pwd)
        userId = cls.createNewUser(msg, USER_TYPE_DEVICE)
        if userId > 0:
            deviceName = msg.getParam('deviceName')
            if deviceName == None:
                deviceName = ''

            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), 'isbind', USER_TYPE_DEVICE, 'name',
                                        deviceName)
            cls.fillUserLoginInfoNew(msg, mo, userId, True, True)
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_DEVICE], userId, appId,
                msg.getParamStr('clientId'), '', 0, devId=deviceId)
            return
        else:
            mo.setResult('code', CODE_USER_GUEST_REG_FAILE)
            mo.setResult('info', 'guest register fail')
            return

    # ---------------------------------------------------------------------------------
    # 通过tuyooId进行登录
    # ---------------------------------------------------------------------------------
    @classmethod
    def doLoginByTyId(cls, msg, mo):
        TyContext.ftlog.info('doLoginByTyId', msg.packJson())
        apiVer = msg.getParamInt('apiVer', 1)

        userId = cls.getIntegerParam(msg, 'userId')
        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        # 设备ID检查
        isOK = cls.checkDeviceId(msg)
        clientId = cls.decodeItem(msg, 'clientId')
        if isOK and clientId == 'Android_2.67_360':
            devId = cls.getStringParam(msg, 'deviceId')
            if devId == '528c8e6cd4a3c6598999a0e9df15ad32':
                ids = []
            else:
                ids = TyContext.RedisUserKeys.execute('LRANGE', 'devidmap:' + str(devId), 0, -1)
            devidUserId = ''
            if ids:
                for uid in ids:
                    TyContext.MySqlSwap.checkUserDate(uid)
                    AccountHelper.restore_avatar_verify_set(uid)
                    mail, snsId, userPwd = TyContext.RedisUser.execute(uid, 'HMGET', 'user:' + str(uid), 'email',
                                                                       'snsId', 'password')
                    if (not mail or len(mail) <= 0) and (not snsId or len(snsId) <= 0):
                        devidUserId = uid;
                        break
            if devidUserId != '' and devidUserId != userId:
                TyContext.ftlog.info('doLoginByTyId fix2.67', 'AfterfixUserId=', devidUserId, 'BeforefixUserId=',
                                     userId)
                userId = devidUserId
                if cls.__checkForbidden(userId, msg, mo):
                    return
                TyContext.UserProps.check_data_update_hall(userId, appId)
                cls.fillUserLoginInfoNew(msg, mo, userId, True, False)
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_DEVICE,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                #                 Report.recoderUserLogin( appId, userId, USER_TYPE_DEVICE)
                return

        # mo.setResult('code', 1)
        #    mo.setResult('info', 'deviceId error')
        #    return

        isOK = cls.checkUserId(msg)
        if isOK:
            # 兼容重度游戏老版本注册账号为数字的玩家账号
            if apiVer == 2:
                thirdUserId = cls.findUserIdByAccount(userId)
                if thirdUserId > 0:
                    userId = thirdUserId
            if userId > 0:
                if cls.__checkForbidden(userId, msg, mo):
                    return
                TyContext.MySqlSwap.checkUserDate(userId)
                AccountHelper.restore_avatar_verify_set(userId)
                passWord = cls.checkPassword(msg)
                m = md5()
                m.update(str(passWord))
                passWordmd5 = m.hexdigest()

                dbPassword = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'password')
                # 补救password没设置值的bug
                if (dbPassword == None or dbPassword == '') and passWord != None:
                    TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId),
                                                'password', passWord,
                                                'userSignature', AccountVerify.md5(passWord))
                    dbPassword = passWord
                    TyContext.ftlog.info('doLoginByTyId->dbPassword is empty', 'userId=', userId, 'dbPassword=',
                                         passWord)

                if str(dbPassword) != str(passWord) and str(dbPassword) != passWordmd5:
                    mo.setResult('code', CODE_USER_PWD_ERROR)
                    mo.setResult('info', '通行证或密码错误，请重新输入！')
                    TyContext.ftlog.info('doLoginByTyId->password incorrect', 'userId=', userId, 'dbPassword=',
                                         dbPassword, 'passWord=', passWord)
                    return

                TyContext.UserProps.check_data_update_hall(userId, appId)
                cls.fillUserLoginInfoNew(msg, mo, userId, True, False)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_DEVICE], userId, appId,
                    msg.getParamStr('clientId'), '', 0, devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_DEVICE,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
                #                 Report.recoderUserLogin( appId, userId, USER_TYPE_DEVICE)
                return
            else:
                mo.setResult('code', CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'userId incorrect')
                return
        else:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'userId not empty')
            return

    # ---------------------------------------------------------------------------------
    # 游客进行登录
    # ---------------------------------------------------------------------------------
    @classmethod
    def doRegisterTyId(cls, msg, mo):
        TyContext.ftlog.info('doRegisterTyId', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        # 设备ID检查
        # isOK = cls.checkDeviceId(msg)
        # if not isOK:
        #    mo.setResult('code', 1)
        #    mo.setResult('info', 'deviceId error')
        #    return

        # 游客初次登陆注册,注册后,返回初次注册的信息
        pwd = 'ty' + str(random.randint(100000, 999999))
        msg.setParam('userPwd', pwd)
        mo.setResult('userPwd', pwd)
        userId = cls.createNewUser(msg, USER_TYPE_DEVICE)
        if userId > 0:
            deviceName = msg.getParam('deviceName')
            if deviceName == None:
                deviceName = ''

            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), 'isbind', USER_TYPE_DEVICE, 'name',
                                        deviceName)
            cls.fillUserLoginInfoNew(msg, mo, userId, True, True)
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_DEVICE], userId, appId,
                msg.getParamStr('clientId'), '', 0, devId=msg.getParamStr('deviceId'))
            return
        else:
            mo.setResult('code', CODE_USER_GUEST_REG_FAILE)
            mo.setResult('info', 'guest register fail')
            return

    # ---------------------------------------------------------------------------------
    # 用户使用邮件和密码注册一个用户
    # ---------------------------------------------------------------------------------
    @classmethod
    def doRegister(cls, msg, mo):
        TyContext.ftlog.debug('doRegister', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setError(1, 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setError(1, 'client error')
            return

        # 设备ID检查
        cls.checkDeviceId(msg)

        userAccount = cls.checkUserAccount(msg)
        passWord = cls.checkPassword(msg)
        if userAccount and passWord:
            # 注册用户登录系统
            userId = cls.findUserIdByAccount(userAccount)
            if userId == 0:
                userId = cls.createNewUser(msg, USER_TYPE_REGISTER)
                cls.fillUserLoginInfo(msg, mo, userId, True, True)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_REGISTER], userId, appId,
                    msg.getParamStr('clientId'), userAccount, 0, devId=msg.getParamStr('deviceId'))
                TyContext.BiReport.user_login(appId, userId, USER_TYPE_REGISTER,
                                              msg.getParamStr('clientId'), TyContext.RunHttp.get_client_ip(),
                                              msg.getParamStr('deviceId'), params=TyContext.RunHttp.convertArgsToDict(),
                                              rpath=TyContext.RunHttp.get_request_path())
            else:
                mo.setError(1, 'userAccount already register')
        else:
            mo.setError(1, 'userAccount or password missing')

    # ---------------------------------------------------------------------------------
    # 随机生成一个有效的途游账户
    # ---------------------------------------------------------------------------------
    @classmethod
    def doRandom(cls, mo):
        head = 'TY'
        account = ''
        while True:
            rabdomint = str(random.randint(100000, 999999))
            account = head + rabdomint
            data = TyContext.RedisUserKeys.execute('GET', 'accountmap:' + account)
            if data == None:
                TyContext.RedisUserKeys.execute('SET', 'accountmap:' + account, 0)
                TyContext.RedisUserKeys.execute('EXPIRE', 'accountmap:' + account, 60)
                break

        pwd = str(random.randint(100000, 999999))
        mo.setResult('account', account)
        mo.setResult('pwd', pwd)
        return

    # ---------------------------------------------------------------------------------
    # 用户使用邮件和密码注册一个用户
    # ---------------------------------------------------------------------------------
    @classmethod
    def doRegisterEmail(cls, msg, mo):
        TyContext.ftlog.debug('doRegisterEmail', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        # 设备ID检查
        isOK = cls.checkDeviceId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'deviceId error')
            return

        userEmail = cls.checkUserEmail(msg)
        passWord = cls.checkPassword(msg)
        if userEmail and passWord:
            # 注册用户登录系统
            userId = cls.findUserIdByMail(userEmail)
            if userId == 0:
                userId = cls.createNewUser(msg, USER_TYPE_REGISTER)
                # 设置该账户已绑定邮箱
                TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'isbind', USER_TYPE_REGISTER)
                cls.fillUserLoginInfoNew(msg, mo, userId, True, True)
                TyContext.BiReport.report_bi_sdk_login(
                    AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_REGISTER], userId, appId,
                    msg.getParamStr('clientId'), userEmail, 0, devId=msg.getParamStr('deviceId'))
            else:
                # 邮件已经被注册
                mo.setResult('code', CODE_USER_MAIL_EXITS)
                mo.setResult('info', 'mail is registered')
        else:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'mail is missing or incorrect')

    # ---------------------------------------------------------------------------------
    # 用户使用邮件和密码注册一个用户
    # ---------------------------------------------------------------------------------
    @classmethod
    def doRegisterMobile(cls, msg):
        TyContext.ftlog.debug('doRegisterMobile', msg.packJson())

        clientId = msg.getParam('clientId')
        # deviceId = msg.getParam('deviceId')
        chkMobile = msg.getParam('mobile')
        if chkMobile == None or len(str(chkMobile)) != 11:
            return

        chkUserId = cls.getIntegerParam(msg, 'userId')
        if chkUserId <= 0:
            return

        userIdByMap = cls.findUserIdByMobile(chkMobile)
        if userIdByMap == 0:
            TyContext.RedisUserKeys.execute('SET', 'mobilemap:' + chkMobile, chkUserId)
            TyContext.RedisUser.execute(chkUserId, 'HMSET', 'user:' + str(chkUserId), 'bindMobile', chkMobile,
                                        'clientId', clientId, 'isbind', USER_TYPE_MOBILE)

            TyContext.ftlog.info('sdkUserRegisterMobile in userId=', chkUserId, 'mobile=', chkMobile, 'clientId=',
                                 msg.getParamStr('clientId', 'unknow'))

        return

    # ---------------------------------------------------------------------------------
    # 用户修改登录密码
    # ---------------------------------------------------------------------------------
    @classmethod
    def doChangePwd(cls, msg, mo):
        # 当前登录信息检查
        authInfo = cls.getStringParam(msg, 'authInfo')
        userId, userName, userTime = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        if userId <= 0:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'authInfo incorrect')
            return

        oldPassword = cls.checkPassword(msg, 'oldPwd')
        if not oldPassword:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', '旧密码输入错误！')
            return

        dbPassword = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'password')
        m = md5()
        m.update(str(oldPassword))
        oldPasswordmd5 = m.hexdigest()
        if str(dbPassword) != str(oldPassword) and str(dbPassword) != oldPasswordmd5:
            mo.setResult('code', CODE_USER_OLD_PWD_ERROR)
            mo.setResult('info', '旧密码输入错误！')
            return

        # 检查密码参数
        newPassWord = cls.checkPassword(msg, 'newPwd')
        if not newPassWord:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'new password is empty')
            return
        TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId),
                                    'password', newPassWord,
                                    'userSignature', AccountVerify.md5(newPassWord))
        userEmail, userMobile = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'email',
                                                            'bindMobile')
        mo.setResult('userId', userId)
        mo.setResult('userPwd', newPassWord)
        mo.setResult('userEmail', userEmail)
        mo.setResult('userMobile', userMobile)
        mo.setResult('code', CODE_USER_SUCCESS)
        mo.setResult('info', 'ok')
        return

    # ---------------------------------------------------------------------------------
    # 游客修改登录密码
    # ---------------------------------------------------------------------------------
    @classmethod
    def doChangeGuestPwd(cls, msg, mo):
        # 当前登录信息检查
        authInfo = cls.getStringParam(msg, 'authInfo')
        userId, userName, userTime = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        if userId <= 0:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'authInfo incorrect')
            return

        # 检查密码参数
        newPassWord = cls.checkPassword(msg)
        if not newPassWord:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'new password is empty')
            return

        TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId),
                                    'password', newPassWord,
                                    'userSignature', AccountVerify.md5(newPassWord))
        mo.setResult('userId', userId)
        mo.setResult('userPwd', newPassWord)
        mo.setResult('code', CODE_USER_SUCCESS)
        mo.setResult('info', 'ok')
        return

    # ---------------------------------------------------------------------------------
    # 用户绑定邮箱
    # ---------------------------------------------------------------------------------
    @classmethod
    def doBindByEmail(cls, msg, mo):
        # 当前登录信息检查
        authInfo = cls.getStringParam(msg, 'authInfo')
        userId, userName, userTime = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        chkUserId = cls.getIntegerParam(msg, 'userId')
        if userId <= 0 or chkUserId != userId:
            mo.setResult('code', 1)
            mo.setResult('info', 'authInfo incorrect')
            return

        # 设备CLIENT ID检查
        isOK = cls.checkClientId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'client error')
            return

        # 检查密码参数
        newPassWord = cls.checkPassword(msg)
        if not newPassWord:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'password is empty')
            return
        # 检查玩家是否已绑定
        userOldEmail, isbind = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'email', 'isbind')
        if userOldEmail != None and userOldEmail != '' and str(isbind) == '1':
            # 邮件已经被绑定
            mo.setResult('code', CODE_USER_MAIL_BINDED)
            mo.setResult('info', 'mail is binded')
            return
        userEmail = msg.getParam('email')
        userIdByMap = cls.findUserIdByMail(userEmail)
        if userIdByMap == 0:
            TyContext.ftlog.info('sdkUserBindEmail in userId=', userId, 'email=', userEmail, 'clientId=',
                                 msg.getParamStr('clientId', 'unknow'))

            TyContext.RedisUserKeys.execute('SET', 'mailmap:' + userEmail, userId)
            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), 'email', userEmail, 'password',
                                        newPassWord, 'isbind', USER_TYPE_REGISTER)
            mo.setResult('userPwd', newPassWord)
            mo.setResult('userEmail', userEmail)
            cls.fillUserLoginInfoNew(msg, mo, userId, True, False)
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_REGISTER], userId, msg.getParamInt('appId'),
                msg.getParamStr('clientId'), userEmail, 0, devId=msg.getParamStr('deviceId'))
            return
        else:
            # 邮件已经被绑定
            mo.setResult('code', CODE_USER_MAIL_BINDED)
            mo.setResult('info', '该邮箱已被使用，请绑定其它邮箱')
            return


            # mo.setResult('code', CODE_USER_SUCCESS)
            # mo.setResult('info', 'ok')
            # return

    # ---------------------------------------------------------------------------------
    # 用户绑定手机号
    # ---------------------------------------------------------------------------------
    @classmethod
    def doBindByMobile(cls, msg, mo):
        # 当前登录信息检查
        authInfo = cls.getStringParam(msg, 'authInfo')
        userId, userName, userTime = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        chkUserId = cls.getIntegerParam(msg, 'userId')
        if userId <= 0 or chkUserId != userId:
            mo.setResult('code', 1)
            mo.setResult('info', 'authInfo incorrect')
            return

        # 检查密码参数
        newPassWord = cls.checkPassword(msg)
        if not newPassWord:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'password is empty')
            return

        chkMobile = msg.getParam('mobile')
        if chkMobile == None or len(str(chkMobile)) != 11:
            mo.setResult('code', 2)
            mo.setResult('info', 'mobile num is empty or not correct')
            return

        userIdByMap = cls.findUserIdByMobile(chkMobile)
        if userIdByMap == 0:
            TyContext.RedisUserKeys.execute('SET', 'mobilemap:' + chkMobile, userId)
            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), 'bindMobile', chkMobile, 'password',
                                        newPassWord, 'isbind', USER_TYPE_MOBILE)
        else:
            # 邮件已经被绑定
            mo.setResult('code', CODE_USER_MOBILE_BINDED)
            mo.setResult('info', 'mobile is binded')
            return

        mo.setResult('code', CODE_USER_SUCCESS)
        mo.setResult('info', 'ok')
        return

    # ---------------------------------------------------------------------------------
    # 根据deviceId获取玩家账号及密码信息
    # ---------------------------------------------------------------------------------
    @classmethod
    def getAccountByDevId(cls, msg, mo):
        TyContext.ftlog.info('doGetAccountByDevId', msg.packJson())

        appId = cls.checkAppId(msg)
        # 设备ID检查
        isOK = cls.checkDeviceId(msg)
        if not isOK:
            mo.setResult('code', 1)
            mo.setResult('info', 'deviceId error')
            return

        devId = cls.getStringParam(msg, 'deviceId')
        if devId == '528c8e6cd4a3c6598999a0e9df15ad32':
            ids = []
        else:
            ids = TyContext.RedisUserKeys.execute('LRANGE', 'devidmap:' + str(devId), 0, -1)
        userPwd = ''
        userId = None
        if ids:
            for uid in ids:
                TyContext.MySqlSwap.checkUserDate(uid)
                AccountHelper.restore_avatar_verify_set(uid)
                mail, snsId, userPwd = TyContext.RedisUser.execute(uid, 'HMGET', 'user:' + str(uid), 'email', 'snsId',
                                                                   'password')
                if (not mail or len(mail) <= 0) and (not snsId or len(snsId) <= 0):
                    userId = uid;
                    break
        # 补丁，到新的结构当中继续查找
        if userId == None:
            if devId != '528c8e6cd4a3c6598999a0e9df15ad32':
                userId = TyContext.RedisUserKeys.execute('GET', 'newdevidmap:' + str(devId))
                if userId == None:
                    userId = TyContext.RedisUserKeys.execute('GET', 'devidmap3:' + str(devId))
                if userId != None:
                    userId = int(userId)
                    TyContext.MySqlSwap.checkUserDate(userId)
                    AccountHelper.restore_avatar_verify_set(userId)
                    userPwd = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'password')

        # 如果玩家密码为空，随机给个密码
        # if userId != '' and userPwd =='' : 
        if userId != None:
            if userPwd == None or userPwd == '':
                userPwd = 'ty' + str(random.randint(100000, 999999))
                TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId),
                                            'password', userPwd,
                                            'userSignature', AccountVerify.md5(userPwd))
                # TyContext.ftlog.info('HSET', 'user:' , str(userId), 'password:', userPwd)
            mo.setResult('userId', userId)
            mo.setResult('userPwd', userPwd)
            mo.setResult('code', CODE_USER_SUCCESS)
            mo.setResult('info', 'ok')
            TyContext.ftlog.info('sdkV2ToV3 in userId=', userId, 'deviceId=', devId, 'appId=', appId)
        else:
            mo.setResult('code', 1)
            mo.setResult('info', 'deviceId error')
        return

    # ---------------------------------------------------------------------------------
    # 通过SNS ID查找一个用户的系统ID
    # 没有找到,返回0,即系统当中的用户ID一定是1开始的
    # ---------------------------------------------------------------------------------
    @classmethod
    def findUserIdBySnsId(self, snsId):
        uid = TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + str(snsId))
        if uid and uid > 0:
            return uid
        return 0

    # ---------------------------------------------------------------------------------
    # 通过新deviceId查找一个用户的系统ID
    # 没有找到,返回0,即系统当中的用户ID一定是1开始的
    # ---------------------------------------------------------------------------------
    @classmethod
    def findUserIdByNewDeviceId(self, deviceId):
        if deviceId == '528c8e6cd4a3c6598999a0e9df15ad32':
            return 0
        uid = TyContext.RedisUserKeys.execute('GET', 'newdevidmap:' + str(deviceId))
        if uid and uid > 0:
            return uid
        return 0

    # ---------------------------------------------------------------------------------
    # 通过账户查找一个用户的系统ID
    # 没有找到,返回0
    # 密码不正确，返回-1
    # ---------------------------------------------------------------------------------
    @classmethod
    def findUserIdByAccountPwd(self, account, passWord):
        uid = TyContext.RedisUserKeys.execute('GET', 'accountmap:' + str(account))
        if uid and uid > 0:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            pwd = TyContext.RedisUser.execute(uid, 'HGET', 'user:' + str(uid), 'password')
            m = md5()
            m.update(str(passWord))
            pwdmd5 = m.hexdigest()
            if str(pwd) == str(passWord) or str(pwd) == pwdmd5:
                return uid
            else:
                return -1
        return 0

    # ---------------------------------------------------------------------------------
    # 通过email及密码查找一个用户的系统ID
    # 没有找到,返回0
    # 密码不正确，返回-1
    # ---------------------------------------------------------------------------------
    @classmethod
    def findUserIdByEmailPwd(self, email, passWord):
        uid = TyContext.RedisUserKeys.execute('GET', 'mailmap:' + str(email))
        if uid and uid > 0:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            pwd = TyContext.RedisUser.execute(uid, 'HGET', 'user:' + str(uid), 'password')
            m = md5()
            m.update(str(passWord))
            pwdmd5 = m.hexdigest()
            if str(pwd) == str(passWord) or pwdmd5 == str(pwd):
                return uid
            else:
                return -1
        return 0

    # ---------------------------------------------------------------------------------
    # 通过手机号及密码查找一个用户的系统ID
    # 没有找到,返回0
    # 密码不正确，返回-1
    # ---------------------------------------------------------------------------------
    @classmethod
    def findUserIdByMobilePwd(self, userMobile, passWord):
        uid = TyContext.RedisUserKeys.execute('GET', 'mobilemap:' + str(userMobile))
        if uid and uid > 0:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            pwd = TyContext.RedisUser.execute(uid, 'HGET', 'user:' + str(uid), 'password')
            m = md5()
            m.update(str(passWord))
            pwdmd5 = m.hexdigest()
            if str(pwd) == str(passWord) or pwdmd5 == str(pwd):
                return uid
            else:
                return -1
        return 0

    # ---------------------------------------------------------------------------------
    # 通过账户查找一个用户的系统ID
    # 没有找到,返回0
    # ---------------------------------------------------------------------------------
    @classmethod
    def findUserIdByAccount(self, account):
        uid = TyContext.RedisUserKeys.execute('GET', 'accountmap:' + str(account))
        if uid and uid > 0:
            return uid
        return 0

    # ---------------------------------------------------------------------------------
    # 通过邮件查找一个用户的系统ID
    # 没有找到,返回0,即系统当中的用户ID一定是1开始的
    # ---------------------------------------------------------------------------------
    @classmethod
    def findUserIdByMail(self, mail):
        uid = TyContext.RedisUserKeys.execute('GET', 'mailmap:' + str(mail))
        if uid and uid > 0:
            return uid
        return 0

    # ---------------------------------------------------------------------------------
    # 通过手机号查找一个用户的系统ID
    # 没有找到,返回0,即系统当中的用户ID一定是1开始的
    # ---------------------------------------------------------------------------------
    @classmethod
    def findUserIdByMobile(self, userMobile):
        uid = TyContext.RedisUserKeys.execute('GET', 'mobilemap:' + str(userMobile))
        if uid and uid > 0:
            return uid
        return 0

    @classmethod
    def getIntegerParam(self, msg, key, dvalue=0):
        value = msg.getParam(key)
        if type(value) == int:
            return value
        if value != None and len(value) > 0:
            return int(value)
        return dvalue

    @classmethod
    def getStringParam(self, msg, key):
        value = msg.getParam(key)
        if value:
            value = strip(unicode(value))
            if len(value) > 0:
                return value
        return ''

    # ---------------------------------------------------------------------------------
    # 使用邮件在平台当中注册一个正式身份的用户,
    # 如果有设备,那么同当前的mail进行自动绑定
    # 如果有SNS,那么同当前的mail进行绑定
    # 正式用户注册成功,返回系统用户ID
    # 正式用户册失败,返回 0
    # ---------------------------------------------------------------------------------
    @classmethod
    def createNewUser(self, msg, userType):
        TyContext.ftlog.debug('createNewUser msg=', msg.packJson())
        # 创建用户并准备udata
        deviceId = msg.getParamStr('deviceId')
        clientId = msg.getParamStr('clientId')
        appId = msg.getParamStr('appId')
        userAccount = msg.getParamStr('userAccount')
        userPwd = msg.getParamStr('userPwd')
        nickName = msg.getParamStr('name')
        snsId = msg.getParamStr('snsId')
        mail = msg.getParamStr('email')
        sex = msg.getParamInt('sex')
        address = msg.getParamStr('address')
        source = msg.getParamStr('source')
        purl = msg.getParamStr('purl')
        idcardno = msg.getParamStr('idcardno')
        phonenumber = msg.getParamStr('phonenumber')
        detect_phonenumber = msg.getParamStr('detect_phonenumber')
        truename = msg.getParamStr('truename')
        snsinfo = msg.getParamStr('snsinfo')
        createTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # 把手机注册的手机号存到user表的bindMobile里
        mobile = msg.getParamStr('mobile')
        if mobile != None or len(str(mobile)) == 11:
            bindMobile = mobile
        else:
            bindMobile = ''

        if clientId.startswith('robot'):
            uid = TyContext.RedisMix.execute('INCR', 'global.robotid')
            if uid > 9999:
                TyContext.ftlog.error('ERROR toomuch robot users !!!!')
                return 0
            uid = str(uid)
        else:
            uid = str(TyContext.RedisMix.execute('INCR', 'global.userid'))

        if Account360.isDefault360Username(nickName):
            genUsername = UsernameGenerator.getInstance().generate(sex)
            if genUsername:
                nickName = genUsername

            # USER_DATA_KEYS = ['password',  'mdevid', 'isbind', 'snsId', 'name', \
            #                   'source', 'purl', 'address', 'sex', \
            #                   'state',  'payCount', 'snsinfo', 'vip', 'dayang',\
            #                   'idcardno', 'phonenumber', 'truename', 'detect_phonenumber', 'email', \
            #                   'createTime', 'userAccount', 'clientId', 'appId', 'bindMobile']
        udata = [userPwd, deviceId, 0, snsId, nickName, \
                 source, purl, address, sex, \
                 0, 0, snsinfo, 0, 0, \
                 idcardno, phonenumber, truename, detect_phonenumber, mail, \
                 createTime, userAccount, clientId, appId, bindMobile]

        # 设置用户数据
        udict = zip(USER_DATA_KEYS, udata)
        udkv = ['userId', uid]
        for k, v in udict:
            udkv.append(k)
            udkv.append(v)
        #         TyContext.ftlog.debug('createNewUser->values=', udkv)

        TyContext.RedisUser.execute(uid, 'HMSET', 'user:' + uid, *udkv)
        TyContext.UserProps.incr_coin(int(uid), int(appId), 0, TyContext.ChipNotEnoughOpMode.NOOP, 0, clientId=clientId)
        TyContext.MySqlSwap.updateUserDataAliveTime(uid)

        # 设置反查索引, SNS ID
        if len(snsId) > 0:
            TyContext.RedisUserKeys.execute('SET', 'snsidmap:' + snsId, uid)

        # 设置反查索引, MAIL
        if len(mail) > 0:
            TyContext.RedisUserKeys.execute('SET', 'mailmap:' + mail, uid)

        # 设置反查索引, userName
        if len(userAccount) > 0:
            TyContext.RedisUserKeys.execute('SET', 'accountmap:' + userAccount, uid)

        # 设置反查索引, mobile
        if len(mobile) > 0:
            TyContext.RedisUserKeys.execute('SET', 'mobilemap:' + mobile, uid)

        # 设置反查索引, DevId
        if len(deviceId) > 0 and deviceId != '528c8e6cd4a3c6598999a0e9df15ad32':
            TyContext.RedisUserKeys.execute('SET', 'newdevidmap:' + deviceId, uid)

        self.updateUserSessionInfo(appId, uid, msg)

        TyContext.BiReport.report_bi_sdk_login(
            AccountConst.CREATE_SUCC_EVENTIDS[userType], uid, appId, clientId,
            ['', mail, snsId, mobile][userType], 0, devId=deviceId)
        TyContext.BiReport.user_register(appId, uid, userType,
                                         clientId, TyContext.RunHttp.get_client_ip(),
                                         deviceId, params=TyContext.RunHttp.convertArgsToDict(),
                                         rpath=TyContext.RunHttp.get_request_path())
        #         Report.recoderUserNew( appId, uid, userType)
        TyContext.UserProps.check_data_update_hall(int(uid), appId, True)
        return int(uid)

    @classmethod
    def updateUserSessionInfo(cls, gameId, userId, msg):
        datas = []
        devId = msg.getParamStr('deviceId', '')
        clientId = msg.getParamStr('clientId', '')
        phoneType = msg.getParamStr('phoneType', '')
        detect_phonenumber = msg.getParamStr('detect_phonenumber', '')
        #         TyContext.ftlog.info('updateUserSessionInfo->userId=', userId, 'gameId=', gameId, 'clientId=', clientId, 'phoneType=', phoneType, 'devId=', devId)

        datas.append('showNoticeUrl')
        datas.append('1')
        datas.append('sessionAppId')
        datas.append(gameId)

        if len(devId) > 0:
            datas.append('sessionDevId')
            datas.append(devId)

        if len(clientId) > 0:
            datas.append('sessionClientId')
            datas.append(clientId)

        if len(phoneType) > 0:
            datas.append('sessionPhoneType')
            datas.append(phoneType)

        clientIP = TyContext.RunHttp.get_client_ip()
        if clientIP and len(clientIP) > 0:
            datas.append('sessionClientIP')
            datas.append(clientIP)

        if detect_phonenumber and len(detect_phonenumber) > 10:
            datas.append('detect_phonenumber')
            datas.append(detect_phonenumber)

        TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), *datas)

    # ---------------------------------------------------------------------------------
    # 填充用户的登录信息
    # ---------------------------------------------------------------------------------
    @classmethod
    def fillUserLoginInfo(cls, msg, mo, userId, isLogin, isCreate):
        appId = msg.getParamInt('appId')
        clientIp = TyContext.RunHttp.get_client_ip()

        # IMPORTANT!! used by GDSS statistics
        TyContext.ftlog.info('fillUserLoginInfo in userId=', userId, 'isLogin=', isLogin,
                             'isCreate=', isCreate,
                             'clientId=', msg.getParamStr('clientId', 'unknow'),
                             'gameId=', appId, 'clientIp=', clientIp)

        # 查询用户基本信息
        uname, authCode = TyContext.AuthorCode.creatUserAuthorCode(userId)
        mo.setResult('code', 0)
        mo.setResult('userId', userId)
        mo.setResult('appId', appId)
        mo.setResult('authorCode', authCode)
        mo.setResult('userName', uname)
        mo.setResult('account', cls.checkUserAccount(msg))

        ainfo = {'authcode': authCode, 'account': cls.checkUserAccount(msg), 'uid': userId}
        ainfo = json.dumps(ainfo)
        mo.setResult('authInfo', ainfo)

        if isCreate == True:
            mo.setResult('isCreate', 1)
        else:
            mo.setResult('isCreate', 0)
        mo.setResult('usercode', TyContext.AuthorCode.makeLoginCode(userId, appId, authCode))

        if appId < 10000:
            # 途游自己的游戏
            cls.appendTcpInfos(appId, userId, mo, msg)
            clientId = msg.getParamStr('clientId', 'unknow')
            AccountHelper.append_ios_idfa_flg(userId, appId, clientId, mo)
        else:
            pass

        cls.updateUserSessionInfo(appId, userId, msg)

        #         TyContext.ftlog.debug('fillUserLoginInfo out userId=', userId, 'info=', mo.packJson())
        return

    @classmethod
    def appendTcpInfos(cls, gameId, userId, mo, mi):
        mo.setResult('connectTimeOut', TyContext.Configure.get_global_item_int('client.connect.timeouts', 35))
        mo.setResult('heartBeat', TyContext.Configure.get_global_item_int('client.heart.beat.times', 6))

        clientId = mi.getParamStr('clientId')
        tcpip, tcpport = TyContext.ServerControl.findUserTcpAddress(gameId, clientId, userId)
        assert (tcpip)
        assert (tcpport)
        mo.setResult('tcpsrv', {'ip': tcpip, 'port': tcpport})

    # ---------------------------------------------------------------------------------
    # 新填充用户的登录信息
    # ---------------------------------------------------------------------------------
    @classmethod
    def fillUserLoginInfoNew(cls, msg, mo, userId, isLogin, isCreate):
        appId = cls.checkAppId(msg)
        clientIp = TyContext.RunHttp.get_client_ip()
        # IMPORTANT!! used by GDSS statistics
        TyContext.ftlog.info('fillUserLoginInfo in userId=', userId, 'isLogin=', isLogin,
                             'isCreate=', isCreate,
                             'clientId=', msg.getParamStr('clientId', 'unknow'),
                             'gameId=', appId, 'clientIp=', clientIp)
        #         TyContext.ftlog.debug('fillUserLoginInfo in msg=', msg.packJson())
        mo.setResult('code', CODE_USER_SUCCESS)
        mo.setResult('userId', userId)
        mo.setResult('appId', appId)

        # 查询用户基本信息

        if appId < 10000:
            # 途游自己的游戏
            cls.appendTcpInfos(appId, userId, mo, msg)
            clientId = msg.getParamStr('clientId', 'unknow')
            AccountHelper.append_ios_idfa_flg(userId, appId, clientId, mo)
        else:
            pass

        # 查询用户基本信息
        if isLogin:
            uname, authStr, email = TyContext.AuthorCode.creatUserAuthorCodeNew(userId)
            mo.setResult('authorCode', authStr)
            mo.setResult('userName', uname)
            mo.setResult('userEmail', email)

            if isCreate:
                mo.setResult('isCreate', 1)
            else:
                mo.setResult('isCreate', 0)

            cls.updateUserSessionInfo(appId, userId, msg)

            # 获取玩家绑定手机号
            bindMobile = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'bindMobile')

            if bindMobile != None and len(str(bindMobile)) == 11:
                mo.setResult('mobile', bindMobile)

            # 获取玩家绑定类型
            # isbind = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'isbind')
            userType = 0
            isbind, userEmail, userSnsInfo, userDBPwd = TyContext.RedisUser.execute(userId, 'HMGET',
                                                                                    'user:' + str(userId), 'isbind',
                                                                                    'email', 'snsId', 'password')
            userEmail = strip(unicode(userEmail)).lower()
            if len(userEmail) > 0:
                userType = 1
            elif userSnsInfo != None and len(str(userSnsInfo)) > 0:
                userType = 2
            elif bindMobile != None and len(str(bindMobile)) == 11:
                userType = 3
            else:
                if isbind != None and str(isbind) != '':
                    userType = int(isbind)
            mo.setResult('userType', userType)
            mo.setResult('userPwd', userDBPwd)

            checkcode = ''
            if appId > 10000:
                # code= md5(str(userId)+str(appId)+str(appKey) + str(authorCode))
                appKey = TyContext.Configure.get_game_item_str(appId, 'appKey', '')
                checkstr = str(userId) + str(appId) + str(appKey) + str(authStr)
                #                 TyContext.ftlog.debug('checkstr====>', checkstr)
                m = md5()
                m.update(checkstr)
                checkcode = m.hexdigest()
                mo.setResult('usercode', checkcode)

            ainfo = {'authcode': authStr, 'account': email, 'uid': userId, 'usercode': checkcode}
            ainfo = json.dumps(ainfo)
            mo.setResult('authInfo', ainfo)
        else:
            pass

        #         TyContext.ftlog.debug('fillUserLoginInfo out userId=', userId, 'info=', mo.packJson())
        return

    # ---------------------------------------------------------------------------------
    # 获取玩家信息接口
    # ---------------------------------------------------------------------------------
    @classmethod
    def doGetUserInfo(cls, msg, mo):
        TyContext.ftlog.info('doGetUserInfo', msg.packJson())

        appId = cls.checkAppId(msg)
        if appId <= 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'appId error')
            return

        isOK = cls.checkUserId(msg)
        if isOK:
            userId = cls.getIntegerParam(msg, 'userId')
            if userId > 0:
                TyContext.MySqlSwap.checkUserDate(userId)
                AccountHelper.restore_avatar_verify_set(userId)
                # 获取玩家基本信息
                userEmail, userName, coin, createTime, authorTime, chargeTotal = TyContext.RedisUser.execute(userId,
                                                                                                             'HMGET',
                                                                                                             'user:' + str(
                                                                                                                 userId),
                                                                                                             'email',
                                                                                                             'name',
                                                                                                             'coin',
                                                                                                             'createTime',
                                                                                                             'authorTime',
                                                                                                             'chargeTotal')
                baseinfo = {'userEmail': userEmail, 'userName': userName, 'coin': coin, 'createTime': createTime,
                            'authorTime': authorTime, 'chargeTotal': chargeTotal}
                baseinfo = json.dumps(baseinfo)
                mo.setResult('baseinfo', baseinfo)
                # 获取玩家游戏数据
                nslogin, lastlogin, level = TyContext.RedisGame.execute(userId, 'HMGET',
                                                                        'gamedata:' + str(appId) + ':' + str(userId),
                                                                        'nslogin', 'lastlogin', 'level')
                exp = TyContext.UserProps.get_exp(userId, appId)
                chip = TyContext.UserProps.get_chip(userId, appId)
                gameinfo = {'nslogin': nslogin, 'chip': chip, 'exp': exp, 'lastlogin': lastlogin, 'level': level}
                gameinfo = json.dumps(gameinfo)
                mo.setResult('gameinfo', gameinfo)
                return
            else:
                mo.setResult('code', CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'userId incorrect')
                return
        else:
            mo.setResult('code', CODE_USER_PARAM_ERROR)
            mo.setResult('info', 'userId not empty')
            return

    @classmethod
    def __do_login_double_check__(cls, tuyooId, msg, mo):
        doubleUsers = TyContext.Configure.get_global_item_hashset('doublue.user.list', []);
        if tuyooId in doubleUsers:
            msg.setParam('passwd', 'ty' + str(random.randint(100000, 999999)))
            userId = cls.createNewUser(msg, USER_TYPE_DEVICE)
            TyContext.ftlog.info('__do_login_double_check__ old uerid=', tuyooId, ' new userid=', userId)
            cls.fillUserLoginInfoNew(msg, mo, userId, True, True)
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_SUCC_EVENTIDS[USER_TYPE_DEVICE], userId, msg.getParamInt('appId'),
                msg.getParamStr('clientId'), '', 0, devId=msg.getParamStr('deviceId'))
            return True
        return False

    @classmethod
    def __checkForbidden(cls, userId, msg, mo):
        TyContext.ftlog.debug('Account->__checkForbidden begin', userId)
        if userId <= 0:
            return False

        if cls.__do_login_double_check__(userId, msg, mo):
            return True

        isForbidden = TyContext.RedisForbidden.execute('EXISTS', 'forbidden:uid:%d' % (userId))

        deviceId = msg.getParamStr('deviceId')
        isForbidden3 = False
        if deviceId:
            isForbidden3 = TyContext.RedisForbidden.execute('EXISTS', 'forbidden:cid:' + str(deviceId))

        appId = cls.checkAppId(msg)
        isForbidden2 = AccountHelper.check_user_forbidden_chip(userId, appId)

        if isForbidden or isForbidden2 or isForbidden3:
            mo.setResult('code', CODE_USER_LOGIN_FORBID)
            mo.setResult('info', '登录被禁止,客服电话：4008-098-000')
            TyContext.ftlog.debug('Account->__checkForbidden forbidden', userId)
            return True

        return False
