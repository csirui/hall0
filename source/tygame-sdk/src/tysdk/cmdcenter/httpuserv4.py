#! encoding=utf-8
from tyframework.context import TyContext
from tysdk.entity.sns4.account_snsv4 import AccountSnsV4
from tysdk.entity.user3.account_check import AccountCheck
from tysdk.entity.user4.account_model import AccountModel
from tysdk.entity.user4.account_universal import AccountUniversal

__author__ = 'yuejianqiang'


class HttpUserV4(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v4/user/checkBindStateByMobile': cls.checkBindStateByMobile,  # 根据手机号判定是否绑定用户
                '/open/v4/user/getLoginType': cls.getLoginType,  # 根据配置 提供客户端登陆方式
                '/open/v4/user/loginByToken': cls.loginByToken,  # 根据token获取用户信息，登录的统一入口
                '/open/v4/user/createGuest': cls.createGuest,  # 创建游客账号
                '/open/v4/user/getGuestBindCode': cls.getGuestBindCode,  # 一键绑定游客接口
                '/open/v4/user/getSmsBindCode': cls.getSmsBindCode,  # 获取短信网关
                '/open/v4/user/checkSmsBindCode': cls.checkSmsBindCode,  # 检查发送短信结果
                '/open/v4/user/sendSmsVerifyCode': cls.sendSmsVerifyCode,  # 发送验证码到手机号
                '/open/v4/user/checkSmsVerifyCode': cls.checkSmsVerifyCode,  # 验证手机收到的验证码
                '/open/v4/user/checkPassword': cls.checkPassword,  # 根据手机号密码获取登录token
                '/open/v4/user/changePassword': cls.changePassword,  # 修改密码
                '/open/v4/user/bindByDevice': cls.bindByDevice,  # 老账号绑定到手机号
                '/open/v4/user/bindByTyID': cls.bindByTyID,  # 老账号绑定到手机号
                '/open/v4/user/bindByMail': cls.bindByMail,  # 老账号绑定到手机号
                '/open/v4/user/listUser': cls.listUser,  # 列举所有绑定过此手机的账号
                '/open/v4/user/getInfo': cls.getUserInfo,  # 获取用户的信息
                '/open/v4/user/setInfo': cls.setUserInfo,  # 设置用户的信息
                '/open/v4/user/unbind': cls.unbindUserMobile,  # 手机号解绑
                '/open/v4/user/getInfoByToken': cls.getUserInfoByToken,  # 通过token获取用户信息
                '/open/v4/user/setUserSex': cls.setUserSex,  # 设置用户性别
                '/open/v4/user/sendSms2User': cls.sendSms2User,  # 发送短信给用户
                '/open/v4/user/userCheck': cls.checkUserByToken,  # 验证用户
                '/open/v4/user/verifyAuthorCode': cls.doVerifyAuthorCode,  # HALL5功能，用户登录，检查用户的authorCode
                '/open/v4/user/checkUserData': cls.doCheckUserData,  # HALL5功能，用户登录，检查用户是否是冷用户，冷转热
                '/open/v4/user/extern/sendSmsVerifyCode': cls.sendSmsVerifyCodeExternal,  # 外部合作 调用发送验证码的接口
                '/open/v4/user/extern/checkSmsBindCode': cls.checkSmsBindCodeExternal,  # 外部合作 调用发送验证码的接口
                '/open/v4/user/extern/loginByToken': cls.loginByTokenExternal,  # 外部合作 调用发送验证码的接口
                '/open/v4/user/extern/bindByExternId': cls.bindByExternId,  # 外部合作 调用发送验证码的接口
                '/open/v4/user/extern/loginByExternId': cls.getUserByExternId,  # 外部合作 调用发送验证码的接口
                '/open/v4/user/extern/unBindByExternId': cls.unbindUserExternId,  # 外部合作 调用发送验证码的接口
                '/open/v4/sdk/update': cls.checkSdkUpdate,  # 外部合作 调用发送验证码的接口
                '/open/v4/user/sendEmaiToUser': cls.sendEmailToUser,  # 给用户发送邮件
                '/open/v4/user/act/wx/bindOpenId': cls.wxActBindByOpenId,  # 微信红包绑定ID
                '/open/v4/user/act/wx/checkBindStateByUid': cls.wxActCheckBindState,  # 检查绑定状态
                '/open/v4/user/act/wx/sendHBToUser': cls.wxActSendHBToUser,  # 发送指定红包到
                '/open/v4/1shang/sendAwardToUser': cls.sendAwardToUser,  # 兑换指定的话费、流量包、影票、优惠券接口
                '/open/v4/1shang/queryChargeStatus': cls.queryChargeStatus,  # 查询兑换状态
                '/open/v4/user/changeName': cls.doChangeUserName,  # 修改用户名接口
                '/open/v4/user/bindBySnsId': cls.doBindBySnsId,  # snsID绑定
                '/open/v4/sdk/util/wxshare/getWxShareConfig': cls.getWxShareConfig,
                '/open/v4/sdk/util/login/getLoginType': cls.getGameLoginType,
            }
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                '/open/v4/user/verifyEmail': cls.verifyEmail,
            }
            AccountCheck.__init_checker__()
        return cls.HTMLPATHS

    @classmethod
    def queryChargeStatus(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doQuery1ShangStatus(mo, rpath)
        return mo

    @classmethod
    def sendAwardToUser(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.sendAwardToUser(mo, rpath)
        return mo

    @classmethod
    def wxActBindByOpenId(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doWxActBindByOpenId(mo, rpath)
        return mo

    @classmethod
    def wxActCheckBindState(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doWxActCheckBindState(mo, rpath)
        return mo

    @classmethod
    def wxActSendHBToUser(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doWxActSendHBToUser(mo, rpath)
        return mo

    @classmethod
    def checkBindStateByMobile(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doCheckBindStateByMobile(mo, rpath)
        return mo

    @classmethod
    def getLoginType(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        # if isReturn :
        #    return params
        params = TyContext.RunHttp.convertArgsToDict()
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.getLoginType(mo, params)
        return mo

    @classmethod
    def getGameLoginType(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        # if isReturn :
        #    return params
        params = TyContext.RunHttp.convertArgsToDict()
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.getGameLoginType(mo, params)
        return mo

    @classmethod
    def checkSdkUpdate(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        rparam = TyContext.RunHttp.convertArgsToDict()
        clientVersion = rparam.get('clientVer', "")
        package = rparam.get('package', "")
        if not clientVersion or not package:
            mo.setResult('code', -1)
            mo.setResult('info', 'clientVer or package 参数错误')
            return mo
        updateConfig = TyContext.Configure.get_global_item_json('sdk_update_config', {})
        packageConfig = updateConfig.get(package, {})
        if not packageConfig:
            mo.setResult('code', 1)
            mo.setResult('info', '包%s更新内容未配置' % package)
            return mo
        destVersion = packageConfig.get('destVersion', '')
        needUpdate = packageConfig.get('needUpdate', True)
        if cmp(clientVersion, destVersion) >= 0:
            mo.setResult('code', 2)
            mo.setResult('info', '更新包版本号过低')
            return mo
        if not needUpdate:
            mo.setResult('code', 3)
            mo.setResult('info', '更新包不需要强制更新')
            return mo
        destUrl = packageConfig.get('destUrl', '')
        mo.setResult('destUrl', destUrl)
        mo.setResult('destVer', destVersion)
        mo.setResult('code', 0)
        return mo

    @classmethod
    def unbindUserExternId(cls, rpath):
        return AccountUniversal.unbindUserExternId(rpath)

    @classmethod
    def getUserByExternId(cls, rpath):
        return AccountUniversal.getUserByExternId(rpath)

    @classmethod
    def bindByExternId(cls, rpath):
        return AccountUniversal.bindByExternId(rpath)

    @classmethod
    def sendSmsVerifyCodeExternal(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doSendSmsVerifyCodeExternal(mo, rpath)
        return mo

    @classmethod
    def checkSmsBindCodeExternal(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doCheckSmsVerifyCodeExternal(mo, rpath)
        return mo

    @classmethod
    def loginByTokenExternal(cls, rpath):
        mo = AccountUniversal.doLoginByTokenExternal(rpath)
        return mo

    @classmethod
    def checkUserByToken(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        userId = int(params.get('userId', 0))
        token = params.get('token', '')
        mo = TyContext.Cls_MsgPack()

        if not userId or not token:
            mobile = AccountModel.get_user_mobile(userId)
            mo.setResult('error', "参数错误")
            mo.setResult('code', 1)
            return mo
        if not AccountModel.checkUserByToken(userId, token):
            mo.setResult('error', "验证失败")
            mo.setResult('code', 2)
            return mo
        mo.setResult('info', 'success')
        mo.setResult('code', 0)
        return mo

    @classmethod
    def createGuest(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.createGuest(params, mo)
        return mo

    @classmethod
    def getSmsBindCode(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.getSmsBindCode(params, mo)
        return mo

    @classmethod
    def getGuestBindCode(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.getSmsBindCode(params, mo)
        return mo

    @classmethod
    def checkSmsBindCode(cls, rpath):
        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        if userId > 0:
            isReturn, params = AccountCheck.check_userv4(rpath)
            if isReturn:
                return params
        else:
            isReturn, params = AccountCheck.check_userv4(rpath)
            if isReturn:
                return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doCheckSmsBindInfo(params, mo)
        return mo

    @classmethod
    def loginByToken(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doLoginByToken(params, mo)
        mo = AccountUniversal.doCheckLoginStrategy(mo)
        return mo

    @classmethod
    def sendSmsVerifyCode(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doSendSmsVerifyCode(params, mo)
        return mo

    @classmethod
    def checkSmsVerifyCode(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doCheckSmsVerifyCode(params, mo)
        return mo

    @classmethod
    def checkPassword(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.checkPassword(params, mo)
        return mo

    @classmethod
    def changePassword(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.changePassword(params, mo)
        return mo

    # @classmethod
    # def bindByMobile(cls, rpath):
    #     isReturn, params = AccountCheck.check_userv4(rpath)
    #     if isReturn :
    #         return params
    #     mo = TyContext.Cls_MsgPack()
    #     AccountLogin.bindMobile(params, mo)
    #     return mo

    @classmethod
    def bindByDevice(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.bindByDevice(params, mo)
        return mo

    @classmethod
    def bindByTyID(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.bindByTyId(params, mo)
        return mo

    @classmethod
    def bindByMail(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.bindByMail(params, mo)
        return mo

    @classmethod
    def listUser(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.listUser(params, mo)
        return mo

    @classmethod
    def getUserInfo(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        userId = int(params.get('userId', 0))
        attrs = params.get('attrs')
        info = AccountModel.get_user_info(userId, *filter(lambda x: x.strip(), attrs.split(',')))
        mo = TyContext.Cls_MsgPack()
        for k, v in info.items():
            mo.setKey(k, v)
        return mo

    @classmethod
    def setUserSex(cls, rpath):
        from tysdk.entity.user_common.verify import AccountVerify
        mo = TyContext.Cls_MsgPack()
        if not AccountVerify.sing_verify(rpath):
            mo.setKey('code', 1)
            return mo
        param = TyContext.RunHttp.convertArgsToDict()
        userId = int(param.get('userId', 0))
        params = {}
        params['sex'] = param.get('sex', 0)
        AccountModel.set_user_info(userId, **params)
        mo.setKey('code', 0)
        return mo

    @classmethod
    def setUserInfo(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        userId = int(params.get('userId', 0))
        del params['userId']
        AccountModel.set_user_info(userId, **params)
        mo = TyContext.Cls_MsgPack()
        mo.setKey('code', 0)
        return mo

    @classmethod
    def unbindUserMobile(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        userId = int(params.get('userId', 0))
        mobile = params.get('mobile')
        if not mobile:
            mobile = AccountModel.get_user_mobile(userId)
        AccountModel.unbind_user_mobile(userId, mobile)
        mo = TyContext.Cls_MsgPack()
        mo.setResult('code', 0)
        return mo

    @classmethod
    def sendSms2User(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        userId = int(params.get('userId', 0))
        mobile = params.get('mobile')
        content = params.get('content')
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.sendSms2user(userId, mobile, content, mo)
        return mo

    @classmethod
    def doCheckUserData(cls, rpath):
        '''
        检查是否是冷用户，冷转热
        '''
        mo = TyContext.Cls_MsgPack()
        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        ret = 0
        if userId > 0:
            ret = TyContext.MySqlSwap.checkUserDate(userId)
        return mo.setResult('check', ret)

    @classmethod
    def doVerifyAuthorCode(cls, rpath):
        '''
        判定是否是禁止登陆用户
        检查用户的token
        返回 客户端IP、cityCode、cityName、deviceId
        '''
        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        authorCode = TyContext.RunHttp.getRequestParam('authorCode', '')
        mo = TyContext.Cls_MsgPack()
        if userId <= 0 or not authorCode:
            mo.setResult('verify', 'params error')
            return mo

        mo.setResult('userId', userId)
        isForbidden = TyContext.RedisForbidden.execute('EXISTS', 'forbidden:uid:%d' % (userId))
        if isForbidden:
            mo.setResult('verify', 'forbidden user')
        else:
            check = TyContext.MySqlSwap.checkUserDate(userId)
            if check != 1:
                mo.setResult('verify', 'data swap false')
            else:
                verify = TyContext.AuthorCode.checkUserAuthorCode(userId, authorCode)
                if isinstance(verify, dict):
                    if verify.get('uid') == userId:
                        mo.setResult('verify', 'ok')
                        mo.setResult('city_code', TyContext.UserSession.get_session_city_zip(userId))
                        mo.setResult('city_name', TyContext.UserSession.get_session_city_name(userId))
                        mo.setResult('devId', TyContext.UserSession.get_session_deviceid(userId))
                        mo.setResult('ip', TyContext.UserSession.get_session_client_ip(userId))
                    else:
                        mo.setResult('verify', 'authorCode uid error')
                else:
                    mo.setResult('verify', 'authorCode error')
        return mo

    @classmethod
    def getUserInfoByToken(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        userId = int(params.get('userId', 0))
        token = params.get('token')
        mo = TyContext.Cls_MsgPack()
        from tysdk.entity.user_common.verify import AccountVerify
        if not AccountVerify.sing_verify(rpath):
            mo.setKey('code', 1)
            return mo
        if not AccountModel.checkUserByToken(userId, token):
            mo.setKey('code', 1)
            return mo
        attrs = params.get('attrs')
        info = AccountModel.get_user_info(userId, *filter(lambda x: x.strip(), attrs.split(',')))
        resultInfo = {}
        keyfilter = ['name', 'sex', 'purl', 'bindMobile', 'snsId']
        for k, v in info.items():
            if k in keyfilter:
                resultInfo[k] = v
        mo.setKey('code', 0)
        mo.setKey('info', resultInfo)
        return mo

    @classmethod
    def sendEmailToUser(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doSendEmailToUser(mo, rpath)
        return mo

    @classmethod
    def verifyEmail(cls, rpath):
        return AccountUniversal.verifyEmail(rpath)

    @classmethod
    def doChangeUserName(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.doChangeUserName(mo, rpath)
        return mo

    @classmethod
    def doBindBySnsId(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountSnsV4.doUserBind(mo, rpath)
        return mo

    @classmethod
    def getWxShareConfig(cls, rpath):
        mo = TyContext.Cls_MsgPack()
        AccountUniversal.getWxShareConfig(rpath, mo)
        return mo
