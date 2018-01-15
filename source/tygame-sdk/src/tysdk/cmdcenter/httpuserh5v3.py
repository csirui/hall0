# -*- coding=utf-8 -*-
import base64
import json

from tyframework.context import TyContext
from tysdk.entity.pay_common.paysll import TuYouSLL
from tysdk.entity.user3.account_bind import AccountBind
from tysdk.entity.user3.account_check_h5 import AccountCheck
from tysdk.entity.user3.account_info_h5 import AccountInfo
from tysdk.entity.user3.account_login import AccountLogin
from tysdk.entity.user3.account_sms import AccountSms
from tysdk.entity.user_common.verify_h5 import AccountVerify


class HttpUserH5V3(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/h5v3/user/createAccount': cls.doCreateAccount,
                '/open/h5v3/user/loginByDevId': cls.doLoginByDevId,
                '/open/h5v3/user/loginByMobile': cls.doLoginByMobile,
                '/open/h5v3/user/loginByTyID': cls.doLoginByTyID,
                '/open/h5v3/user/loginByMail': cls.doLoginByMail,
                '/open/h5v3/user/loginBySnsID': cls.doLoginBySnsID,
                '/open/h5v3/user/loginByAccount': cls.doLoginByAccount,

                '/open/h5v3/user/processSnsId': cls.doProcessSnsID,

                '/open/h5v3/user/getSmsBindCode': cls.doGetSmsBindCode,
                '/open/h5v3/user/checkSmsBind': cls.doCheckSmsBind,

                '/open/h5v3/user/getSmsVerifyCode': cls.doGetSmsVerifyCode,
                '/open/h5v3/user/bindMobileByVerifyCode': cls.doBindMobileByVerifyCode,

                '/open/h5v3/user/bindBySnsId': cls.doBindBySnsId,
                '/open/h5v3/user/bindByEmail': cls.doBindByEmail,

                '/open/h5v3/user/renewAuthorCodeByTyId': cls.doRenewAuthorCodeByTyId,

                '/open/h5v3/user/getUserInfo': cls.doGetUserInfo,
                '/open/h5v3/user/setUserInfo': cls.doSetUserInfo,

                '/open/h5v3/user/setPasswd': cls.doSetPasswd,
                '/open/h5v3/user/setPasswdByVerifyCode': cls.doSetPasswdByVerifyCode,

                '/open/h5v3/user/setUserAvatar': cls.doSetUserAvatar,
                '/open/h5v3/user/reportContacts': cls.doReportContacts,

                '/open/h5v3/user/queryForbidden': cls.doQueryForbidden,
                '/open/h5v3/user/setForbidden': cls.doSetForbidden,

                '/open/h5v3/user/youkuLoginCallback': cls.doYoukuLoginCallback,

                '/open/h5v3/customtable/notify': cls.doCustomTableNotify
            }
            AccountCheck.__init_checker__()
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                # '/open/h5vc/user/smsCallback': cls.doManDaoSmsBindCallBack,
                # '/open/h5vc/user/smsCallback/baifen': cls.doBaiFenSmsBindCallBack,

                # for ty/360 http api
                # '/open/h5v3/user/gettyid' : TuYouSLL.get_tyid,
                '/open/h5v3/user/gid2qid': TuYouSLL.gid2qid,
                '/open/h5v3/user/revokeqid': TuYouSLL.revoke_qid,

                # for pc qipai (360 kaiping)
                '/open/h5v3/user/kaiping/login': TuYouSLL.kp_login,
                '/open/h5v3/user/kaiping/code': TuYouSLL.kp_code,
                '/open/h5v3/user/kaiping/checkuser': TuYouSLL.kp_checkuser,
                '/open/h5v3/user/kaiping/exchange': TuYouSLL.kp_exchange,
            }
            AccountCheck.__init_checker__()
        return cls.HTMLPATHS

    @classmethod
    def doLoginByDevId(cls, rpath):
        isReturn, params = AccountCheck.login_check(rpath, 1, False)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountLogin.doLoginByDevId(params, mo)
        return mo

    @classmethod
    def doLoginByMobile(cls, rpath):
        isReturn, params = AccountCheck.login_check(rpath, 2)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountLogin.doLoginByMobile(params, mo)
        return mo

    @classmethod
    def doLoginByTyID(cls, rpath):
        isReturn, params = AccountCheck.login_check(rpath, 3)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountLogin.doLoginByTyID(params, mo)
        return mo

    @classmethod
    def doRenewAuthorCodeByTyId(cls, rpath):
        isReturn, params = AccountCheck.login_check(rpath, 3)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountLogin.doRenewAuthorCodeByTyId(params, mo)
        return mo

    @classmethod
    def doLoginByMail(cls, rpath):
        isReturn, params = AccountCheck.login_check(rpath, 4)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountLogin.doLoginByMail(params, mo)
        return mo

    @classmethod
    def doLoginBySnsID(cls, rpath):
        isReturn, params = AccountCheck.login_check(rpath, 5)
        if isReturn:
            return params

        AccountCheck.set_user_check(rpath, params)
        mo = TyContext.Cls_MsgPack()
        AccountLogin.doProcessSnsID(params, mo)
        return mo

    @classmethod
    def doProcessSnsID(cls, rpath):

        isReturn, params = AccountCheck.login_check(rpath, 5, False)
        if isReturn:
            return params
        AccountCheck.set_user_check(rpath, params)

        mo = TyContext.Cls_MsgPack()
        AccountLogin.doProcessSnsID(params, mo)
        return mo

    @classmethod
    def doLoginByAccount(cls, rpath):
        isReturn, params = AccountCheck.login_check(rpath, 6)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountLogin.doLoginByAccount(params, mo)
        return mo

    @classmethod
    def doCreateAccount(cls, rpath):
        isReturn, params = AccountCheck.login_check(rpath, 7)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountLogin.doCreateAccount(params, mo)
        return mo

    @classmethod
    def doGetSmsBindCode(cls, rpath):
        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        if userId > 0:
            isReturn, params = AccountCheck.normal_check(rpath)
            if isReturn:
                return params
        else:
            isReturn, params = AccountCheck.onekeylogin_check(rpath)
            if isReturn:
                return params
        mo = TyContext.Cls_MsgPack()
        AccountSms.doGetSmsBindCode(params, mo)
        return mo

    @classmethod
    def doManDaoSmsBindCallBack(cls, rpath):
        try:
            args = TyContext.RunHttp.getRequestParam('args', '')
            params = {}
            if args and len(args) > 0:
                datas = args.split(',')
                if len(datas) > 3:
                    params['mobile'] = datas[2]
                    params['sms'] = datas[3]
            AccountSms.doSmsBindCallBack(params)
        except:
            TyContext.ftlog.exception()
        return '0'

    @classmethod
    def doBaiFenSmsBindCallBack(cls, rpath):
        try:
            params = {}
            params['mobile'] = TyContext.RunHttp.getRequestParam('Up_UserTel', '')
            params['sms'] = TyContext.RunHttp.getRequestParam('Up_UserMsg', '')
            AccountSms.doSmsBindCallBack(params)
        except:
            TyContext.ftlog.exception()
        return '0'

    @classmethod
    def doCheckSmsBind(cls, rpath):
        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        if userId > 0:
            isReturn, params = AccountCheck.normal_check(rpath)
            if isReturn:
                return params
        else:
            isReturn, params = AccountCheck.onekeylogin_check(rpath)
            if isReturn:
                return params
        mo = TyContext.Cls_MsgPack()
        AccountSms.doCheckSmsBind(params, mo)
        return mo

    @classmethod
    def doGetSmsVerifyCode(cls, rpath):
        # isReturn, params = AccountCheck.normal_check( rpath)
        # if isReturn :
        #     return params
        params = {}
        isReturn, mobile = AccountCheck.check_param_mobile(rpath)
        if isReturn:
            return mobile
        params['mobile'] = mobile
        params['whatfor'] = TyContext.RunHttp.getRequestParam('whatfor', '')

        mo = TyContext.Cls_MsgPack()
        AccountSms.doGetSmsVerifyCode(params, mo)
        return mo

    @classmethod
    def doBindMobileByVerifyCode(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params

        isReturn, mobile = AccountCheck.check_param_mobile(rpath)
        if isReturn:
            return mobile
        params['mobile'] = mobile

        isReturn, vcode = AccountCheck.check_param_verify_code(rpath)
        if isReturn:
            return vcode
        params['vcode'] = vcode

        mo = TyContext.Cls_MsgPack()
        AccountSms.doBindMobileByVerifyCode(params, mo)
        return mo

    @classmethod
    def doBindBySnsId(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params

        isReturn, snsId = AccountCheck.check_param_snsid(rpath)
        if isReturn:
            return snsId
        params['snsId'] = snsId
        params['snsToken'] = TyContext.RunHttp.getRequestParam('snsToken')

        mo = TyContext.Cls_MsgPack()
        AccountBind.doBindBySnsId(params, mo)
        return mo

    @classmethod
    def doBindByEmail(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params
        appId = params['appId']
        clientId = params['clientId']
        if (appId == 6 and (clientId.find('Android_2.8_') >= 0 or clientId.find('Android_2.81_') >= 0)) or \
                (appId == 7 and (clientId.find('Android_2.28_') >= 0)):
            mo = TyContext.Cls_MsgPack()
            mo.setResult('code', 1)
            mo.setResult('info', '暂未开通此功能')
            return mo

        isReturn, mail = AccountCheck.check_param_mail(rpath)
        if isReturn:
            return mail
        params['mail'] = mail

        mo = TyContext.Cls_MsgPack()
        AccountBind.doBindByEmail(params, mo)
        return mo

    @classmethod
    def doGetUserInfo(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        AccountInfo.doGetUserInfo(params, mo)
        return mo

    @classmethod
    def doSetUserInfo(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params

        isReturn, params = AccountCheck.set_user_check(rpath, params)
        if isReturn:
            return params

        mo = TyContext.Cls_MsgPack()
        AccountInfo.doSetUserInfo(params, mo)
        return mo

    @classmethod
    def doSetUserAvatar(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params

        url = TyContext.RunHttp.getRequestParam('url', '').strip()
        data = TyContext.RunHttp.getRequestParam('data', '')
        mo = TyContext.Cls_MsgPack()

        is_url_error = len(url) > 0 and (len(url) > 125 or url.find('"') >= 0 or url.find("'") >= 0)
        if (len(url) == 0 and len(data) == 0) or is_url_error:
            mo.setResult('code', 1)
            mo.setResult('info', '输入参数错误')
            return mo
        if len(data) > 0:
            try:
                data = base64.b64decode(data)
            except:
                mo.setResult('code', 1)
                mo.setResult('info', '图像数据错误')
                return mo
        params['url'] = url
        params['data'] = data
        AccountInfo.doSetUserAvatar(params, mo)
        return mo

    @classmethod
    def doSetPasswd(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params

        # 获取玩家修改密码次数
        userId = params['userId']
        changePwdCount = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'changePwdCount')
        #         TyContext.ftlog.info(cls.__name__, 'doSetPasswd->changePwdCount=', changePwdCount)
        if changePwdCount == None:
            changePwdCount = 0
        if int(changePwdCount) > 0:
            isReturn, oldpasswd = AccountCheck.check_param_password(rpath, 'oldpasswd')
            if isReturn:
                return oldpasswd
            params['oldpasswd'] = oldpasswd

        isReturn, newpasswd = AccountCheck.check_param_password(rpath, 'newpasswd', isSet=True)
        if isReturn:
            return newpasswd
        params['newpasswd'] = newpasswd

        mo = TyContext.Cls_MsgPack()
        AccountInfo.doSetPasswd(params, mo)
        return mo

    @classmethod
    def doSetPasswdByVerifyCode(cls, rpath):
        # isReturn, params = AccountCheck.normal_check( rpath)
        # if isReturn :
        #     return params
        params = {}
        isReturn, mobile = AccountCheck.check_param_mobile(rpath)
        if isReturn:
            return mobile
        params['mobile'] = mobile

        isReturn, vcode = AccountCheck.check_param_verify_code(rpath)
        if isReturn:
            return vcode
        params['vcode'] = vcode

        isReturn, newpasswd = AccountCheck.check_param_password(rpath, 'newpasswd', isSet=True)
        if isReturn:
            return newpasswd
        params['newpasswd'] = newpasswd

        mo = TyContext.Cls_MsgPack()
        AccountSms.doSetPasswordByVerifyCode(params, mo)
        return mo

    @classmethod
    def doReportContacts(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        contacts = TyContext.RunHttp.getRequestParam('contacts', '')
        if contacts != '':
            contacts = AccountVerify.decode_item(contacts)

        TyContext.ftlog.info('doReportContacts appId=', params['appId'], 'userId=', params['userId'], 'contacts=',
                             contacts)
        mo.setResult('code', 0)
        mo.setResult('info', 'success')
        return mo

    @classmethod
    def doQueryForbidden(cls, rpath):
        '''获取禁止登录用户列表'''
        byid = TyContext.RunHttp.getRequestParam('byid', 'userId')
        mo = TyContext.Cls_MsgPack()
        if byid == 'userId':
            members = TyContext.RedisMix.execute('SMEMBERS', 'forbiddenuser')
        elif byid == 'deviceId':
            members = TyContext.RedisMix.execute('SMEMBERS', 'forbiddendevice')
        if not members:
            members = []
        mo.setResult('lock_users', members)
        return mo

    @classmethod
    def doSetForbidden(cls, rpath):
        '''设置禁止登录用户'''
        mo = TyContext.Cls_MsgPack()
        lock_users = TyContext.RunHttp.getRequestParam('lock_users', '[]')
        unlock_users = TyContext.RunHttp.getRequestParam('unlock_users', '[]')

        try:
            locked = json.loads(lock_users)
            unlocked = json.loads(unlock_users)
        except:
            mo.setResult('code', 1)
            mo.setResult('info', 'error args')
            return mo

        byid = TyContext.RunHttp.getRequestParam('byid', 'userId')
        TyContext.ftlog.debug('doSetForbidden byid', byid, 'locked', locked,
                              'unlocked', unlocked)
        if byid == 'userId':
            return cls._set_forbidden_ids('forbiddenuser', locked, unlocked, locked, mo)
        elif byid == 'deviceId':
            lock_users = []
            for devid in locked:
                userid = AccountLogin.__find_userid_by_devid_map_v3__(devid)
                if userid > 0:
                    lock_users.append(userid)
            return cls._set_forbidden_ids('forbiddendevice', locked, unlocked, lock_users, mo)

    @classmethod
    def _set_forbidden_ids(cls, key, locked, unlocked, lock_users, mo):
        TyContext.ftlog.debug('_set_forbidden_ids key', key, 'locked', locked,
                              'unlocked', unlocked, 'lock_users', lock_users,
                              'mo', mo)
        if len(locked) > 0:
            TyContext.RedisMix.execute('SADD', key, *locked)

        conf = TyContext.Configure.get_global_item_json('forbidden.login.callback', {})
        if conf:
            userids = ','.join([str(i) for i in lock_users])
            postdata = 'userids=' + userids
            for key_, value_ in conf.items():
                if not value_: continue
                TyContext.ftlog.debug('HttpUserV3->doSetForbidden call game', key_, value_, postdata)
                TyContext.WebPage.webget(httpurl=value_, postdata_=postdata)

        if len(unlocked) > 0:
            TyContext.RedisMix.execute('SREM', key, *unlocked)

        members = TyContext.RedisMix.execute('SMEMBERS', key)
        if not members:
            members = []
        mo.setResult('lock_users', members)
        return mo

    @classmethod
    def doGetGameServerMode(cls, rpath):
        """
        ios需要在登录之前判断是否正式服，以便选择是否游客登录
        """
        mo = TyContext.Cls_MsgPack()
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        if appId <= 0 or clientId == '':
            mo.setResult('code', 1)
            mo.setResult('info', 'error')
            return mo
        server_control = TyContext.ServerControl.findServerControl(appId, clientId)
        TyContext.ftlog.debug('server_control:', server_control)
        mo.setResult('code', 0)
        mo.setResult('mode', server_control['mode'])
        return mo

    @classmethod
    def doYoukuLoginCallback(cls, rpath):
        mo = TyContext.Cls_MsgPack()

        loginkey = "8MY0XXTQacV2BqOy"
        qid = TyContext.RunHttp.getRequestParam('qid', '')
        server_id = TyContext.RunHttp.getRequestParam('server_id', '')
        time = TyContext.RunHttp.getRequestParam('time', '')
        sign = TyContext.RunHttp.getRequestParam('sign', '')
        isAdult = TyContext.RunHttp.getRequestParamInt('isAdult', 1)

        from tysdk.entity.user_common.verify_h5 import AccountVerify
        sign_str = "qid=%s&time=%s&server_id=%s%s" % (qid, time, server_id, loginkey)
        my_sign = AccountVerify.md5(sign_str)

        if not my_sign or my_sign != sign_str:
            mo.setResult('code', 1)
            mo.setResult('info', 'sign error')
            return mo

    @classmethod
    def doCustomTableNotify(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params

        # mo = TyContext.Cls_MsgPack()
        appId = params['appId']
        userId = params['userId']
        clientId = params['clientId']
        msg = params['msg']
        customTableId = TyContext.RunHttp.getRequestParam('customTableId', '')

        url = cls._get_game_server_callback_url(appId, clientId, '/v2/game/h5/customtable/chat')
        cls.http_request(url, {'userId': userId, 'appId': appId,
                               'customTableId': customTableId, 'msg': msg})

    @classmethod
    def _get_game_server_callback_url(cls, appId, clientId, url):
        control = TyContext.ServerControl.findServerControl(appId, clientId)
        if not control:
            TyContext.ftlog.error('notify_game_server can not find server control, clientId', clientId)
            return None
        return str(control['http']) + url

    @classmethod
    def http_request(cls, url, params, ispost=False):
        from urllib import urlencode
        method = 'GET'
        params_data = ''
        if ispost:
            method = 'POST'
            params_data = urlencode(params)
        else:
            url = url + '?' + urlencode(params)
        TyContext.ftlog.debug('friend http_request params=', params_data, 'url=', url)
        try:
            from twisted.web import client
            result = TyContext.getTasklet().waitForPage(url, params_data, method)
            TyContext.ftlog.debug('friend http_request reuslt=', result)
            return result
        except Exception as e:
            TyContext.ftlog.error('friend http_request error', e, 'url', url)
