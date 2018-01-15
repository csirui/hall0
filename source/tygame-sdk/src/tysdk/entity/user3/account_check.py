# -*- coding=utf-8 -*-

import re
import string

from tyframework.context import TyContext
from tysdk.entity.user_common.verify import AccountVerify


def is_valid_iccid(iccid):
    # return re.match('^[0-9]{10,20}$', iccid)
    if len(str(iccid)) >= 10 and len(str(iccid)) <= 30:
        return True
    return False


class AccountCheck():
    error_sing = None

    @classmethod
    def __init_checker__(cls):

        if cls.error_sing != None:
            return

        mo = TyContext.Cls_MsgPack()
        mo.setError(1, '参数校验失败')
        cls.error_sing = mo.packJson()

        mo.setError(2, 'appId参数错误')
        cls.error_param_appid = mo.packJson()

        mo.setError(3, 'clientId参数错误')
        cls.error_param_clientid = mo.packJson()

        mo.setError(4, '手机号输入错误')
        cls.error_param_mobile = mo.packJson()

        mo.setError(5, '途游通行证输入错误')
        cls.error_param_tuyooid = mo.packJson()

        mo.setError(6, '途游通行证输入错误')
        cls.error_param_account = mo.packJson()

        mo.setError(7, '邮箱输入错误')
        cls.error_param_mail = mo.packJson()

        mo.setError(8, 'SNSID输入错误')
        cls.error_param_snsid = mo.packJson()

        mo.setError(9, '密码输入错误')
        cls.error_param_password = mo.packJson()

        mo.setError(10, 'userId参数错误')
        cls.error_param_userid = mo.packJson()

        mo.setError(11, '登录超时，请重新登录')
        cls.error_param_authorcode = mo.packJson()

        mo.setError(12, '昵称格式错误')
        cls.error_param_nickname = mo.packJson()

        mo.setError(13, '性别格式错误')
        cls.error_param_sex = mo.packJson()

        mo.setError(14, '头像格式')
        cls.error_param_headurl = mo.packJson()

        mo.setError(15, '设备信息错误')
        cls.error_param_device = mo.packJson()

        mo.setError(16, '地址信息错误')
        cls.error_param_address = mo.packJson()

        mo.setError(17, '身份证信息错误')
        cls.error_param_idcardno = mo.packJson()

        mo.setError(18, '姓名信息错误')
        cls.error_param_truename = mo.packJson()

        mo.setError(19, '手机号码信息错误')
        cls.error_param_phonenumber = mo.packJson()

        mo.setError(20, '密码格式错误，须6-20位英文、数字组合')
        cls.error_param_setpassword = mo.packJson()

    @classmethod
    def check_param_mobile(cls, rpath):
        mobile = TyContext.RunHttp.getRequestParam('mobile', '')
        mobile = AccountVerify.decode_item(mobile)
        try:
            mobile = int(mobile)
        except:
            pass
        if len(str(mobile)) != 11:
            return True, cls.error_param_mobile
        return False, mobile

    @classmethod
    def check_param_verify_code(cls, rpath):
        vcode = TyContext.RunHttp.getRequestParamInt('vcode', 0)
        if vcode <= 100000 or vcode > 999999:
            return True, cls.error_param_mobile
        return False, vcode

    @classmethod
    def check_param_snsid(cls, rpath):
        snsId = TyContext.RunHttp.getRequestParam('snsId', '')
        snsId = AccountVerify.decode_item(snsId)
        if len(snsId.split(':')) != 2:
            return True, cls.error_param_snsid
        return False, snsId

    @classmethod
    def check_param_account(cls, rpath):
        account = TyContext.RunHttp.getRequestParam('account', '')
        account = AccountVerify.decode_item(account)
        if len(account) <= 0 or len(account) > 32:
            return True, cls.error_param_account
        return False, account

    @classmethod
    def check_param_mail(cls, rpath):
        mail = TyContext.RunHttp.getRequestParam('mail', '')
        mail = AccountVerify.decode_item(mail)
        mail = mail.strip().lower()
        if len(mail.split('@')) != 2:
            return True, cls.error_param_mail
        return False, mail

    @classmethod
    def check_param_password(cls, rpath, key='passwd', isSet=False):
        password = TyContext.RunHttp.getRequestParam(key, '')
        if password == '':  # hack - 没有创建密码问题 liubo
            return False, password
        password = AccountVerify.decode_item(password)
        if len(password) < 6:
            return True, cls.error_param_password
        if isSet and not re.match(r'^[A-Za-z0-9@#$%^&+=]{6,20}$', password):
            return True, cls.error_param_setpassword
        return False, password

    @classmethod
    def login_check(cls, rpath, loginType):

        # cls.__init_checker__()

        # 输入参数校验
        if AccountVerify.sing_verify(rpath) != True:
            return True, cls.error_sing

        # 检查是否可以登录
        loginForbid = TyContext.ServerControl.checkLoginForbid(rpath)
        if loginForbid != False:
            return True, loginForbid

        params = TyContext.RunHttp.convertArgsToDict()
        # params = {}
        # 检查登录参数
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        if appId <= 0:
            return True, cls.error_param_appid
        params['appId'] = appId

        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        try:
            datas = clientId.split('_')
            clientSystem = datas[0]
            clientVersion = TyContext.ClientUtils.getVersionFromClientId(clientId)
            clientChannel = datas[2]
        except:
            return True, cls.error_param_clientid

        check_clientid_number = TyContext.Configure.get_global_item_int(
            'check_clientid_num_before_login', 0)
        if appId < 10000 and check_clientid_number:
            if not TyContext.BiUtils.clientIdToNumber(appId, clientId):
                return True, cls.error_param_clientid

        params['clientId'] = clientId
        params['clientSystem'] = clientSystem
        params['clientVersion'] = clientVersion
        params['clientChannel'] = clientChannel

        imei = TyContext.RunHttp.getRequestParam('imei', '')
        #         TyContext.ftlog.debug('imei=', imei)
        imei = AccountVerify.decode_item(imei)
        #         TyContext.ftlog.debug('imei=', imei)
        if len(imei) < 12 or len(imei) > 32:
            imei = ''
        #         TyContext.ftlog.debug('imei=', imei)

        imsi = TyContext.RunHttp.getRequestParam('imsi', '')
        #         TyContext.ftlog.debug('imsi=', imsi)
        imsi = AccountVerify.decode_item(imsi)
        #         TyContext.ftlog.debug('imsi=', imei)
        if len(imsi) == 0 or len(imsi) > 15:
            imsi = ''
        #        TyContext.ftlog.debug('imsi=', imsi)

        androidId = TyContext.RunHttp.getRequestParam('androidId', '')
        #         TyContext.ftlog.debug('androidId=', androidId)
        androidId = AccountVerify.decode_item(androidId)
        #         TyContext.ftlog.debug('androidId=', androidId)
        if len(androidId) < 12 or len(androidId) > 32:
            androidId = ''
        #         TyContext.ftlog.debug('androidId=', androidId)

        idfa = AccountVerify.decode_item(
            TyContext.RunHttp.getRequestParam('idfa', ''))
        params['idfa'] = idfa
        TyContext.ftlog.debug('idfa=', idfa)

        mac = TyContext.RunHttp.getRequestParam('mac', '')
        #         TyContext.ftlog.debug('mac=', mac)
        mac = AccountVerify.decode_item(mac)
        #         TyContext.ftlog.debug('mac=', mac)

        params['macmd5'] = AccountVerify.md5(mac)

        # 获取不到时，mac可能为00:00:00:00:00:00或02:00:00:00:00:00
        # 下面的判断似有问题，但不能改，否则用户下次登录会生成不同的deviceId
        # 而丢失老账户
        mac = mac.replace(':', '')
        badmacs_an = TyContext.Configure.get_global_item_json('badmacs_android', ['000000000000'])
        badmacs_ios = TyContext.Configure.get_global_item_json('badmacs_ios', ['020000000000'])
        if mac in badmacs_ios:  # 如果IOS的mac取不到或者变化020000000000，那么需要加到badmacs_ios集合中
            params['macmd5'] = ''
        else:
            if mac != "" and mac not in badmacs_an:  # 如果安卓的mac取值出现问题，那么需要将错误值加入badmacs_an
                mac = mac.replace(':', '')
                if len(mac) != 12:
                    TyContext.ftlog.info('the mac is error ! [', mac, ']')
                    mac = ''
            else:
                TyContext.ftlog.info('the mac is error ! [', mac, ']')
                mac = ''
            #         TyContext.ftlog.debug('mac=', mac)

        uuid = TyContext.RunHttp.getRequestParam('uuid', '')
        #         TyContext.ftlog.debug('uuid=', uuid)
        if len(uuid) != 32:
            uuid = ''

        if mac in badmacs_ios:
            uuid = uuid.lower()

        svninfo = TyContext.RunHttp.getRequestParam('svninfo', '')
        if svninfo:
            params['svninfo'] = svninfo

        iccid = TyContext.RunHttp.getRequestParam('iccid', '')
        TyContext.ftlog.debug('paramiccid=', iccid)
        iccid = AccountVerify.decode_item(iccid)
        TyContext.ftlog.debug('iccid=', iccid)

        params['mac'] = mac
        if is_valid_iccid(iccid):
            params['iccid'] = iccid
        else:
            try:
                del params['iccid']
            except:
                pass
        # params['macmd5'] = AccountVerify.md5(mac)
        params['imei'] = imei
        params['imsi'] = imsi
        params['androidId'] = androidId
        params['uuid'] = uuid
        id_str = mac + '|' + imei + '|' + androidId + '|' + uuid
        TyContext.ftlog.info('deviceId str=', id_str)
        _devid = AccountVerify.md5(id_str)
        params['deviceId'] = _devid
        TyContext.ftlog.debug('login_check mac', mac, 'imei', imei,
                              'androidId', androidId, 'uuid', uuid,
                              'calculated deviceId', _devid)
        params['phoneType'] = TyContext.RunHttp.getRequestParam('phoneType', '')
        params['detect_phonenumber'] = TyContext.RunHttp.getRequestParam('detect_phonenumber', '')
        params['lang'] = TyContext.RunHttp.getRequestParam('lang', '')
        password = None

        if loginType == 1:
            '''
            游客登录
            '''
            password = None
            if len(mac) + len(imei) + len(androidId) + len(uuid) == 0:
                return True, cls.error_param_device
            params['deviceName'] = TyContext.RunHttp.getRequestParam('deviceName', '')

        elif loginType == 2:
            '''
            手机号登录
            '''
            isReturn, mobile = cls.check_param_mobile(rpath)
            if isReturn:
                return True, mobile
            params['mobile'] = mobile

            password = 1
        elif loginType == 3:
            '''
            tuyooid登录
            '''
            tuyooId = TyContext.RunHttp.getRequestParam('tuyooId', '')
            tuyooId = AccountVerify.decode_item(tuyooId)
            try:
                tuyooId = int(tuyooId)
            except:
                pass
            if tuyooId <= 10000:
                return True, cls.error_param_tuyooid
            params['tuyooId'] = tuyooId

            password = 1
        elif loginType == 4:
            '''
            邮箱登录
            '''
            isReturn, mail = cls.check_param_mail(rpath)
            if isReturn:
                return True, mail
            params['mail'] = mail

            password = 1
        elif loginType == 5:
            '''
            snsid登录
            '''
            isReturn, snsId = cls.check_param_snsid(rpath)
            if isReturn:
                return True, snsId
            params['snsId'] = snsId
            params['snsToken'] = TyContext.RunHttp.getRequestParam('snsToken')
            params['snsAppId'] = TyContext.RunHttp.getRequestParam('snsAppId')

            password = None
        elif loginType == 6:
            '''
            Account登录
            '''
            isReturn, account = cls.check_param_account(rpath)
            if isReturn:
                return True, account
            params['account'] = account

            password = 1
        elif loginType == 7:
            '''
            新建账户
            '''
            pass

        if password != None:
            isReturn, passwd = cls.check_param_password(rpath)
            if isReturn:
                return True, passwd
            params['passwd'] = passwd

        return False, params

    @classmethod
    def normal_check(cls, rpath, check_sign=True):

        # cls.__init_checker__()

        # 输入参数校验
        if check_sign and AccountVerify.sing_verify(rpath) != True:
            return True, cls.error_sing

        params = {}

        # 检查登录参数
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        if appId <= 0:
            return True, cls.error_param_appid
        params['appId'] = appId

        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        if userId <= 0:
            return True, cls.error_param_userid
        params['userId'] = userId

        authorCode = TyContext.RunHttp.getRequestParam('authorCode', '')
        if check_sign and not TyContext.AuthorCode.checkUserAuthorCode(userId, authorCode):
            return True, cls.error_param_authorcode

        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        try:
            datas = clientId.split('_')
            clientSystem = datas[0]
            clientVersion = TyContext.ClientUtils.getVersionFromClientId(clientId)
            clientChannel = datas[2]
        except:
            return True, cls.error_param_clientid

        params['clientId'] = clientId
        params['clientSystem'] = clientSystem
        params['clientVersion'] = clientVersion
        params['clientChannel'] = clientChannel

        return False, params

    @classmethod
    def onekeylogin_check(cls, rpath):
        # cls.__init_checker__()
        params = {}

        # 检查登录参数
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        if appId <= 0:
            return True, cls.error_param_appid
        params['appId'] = appId

        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        params['userId'] = userId

        bindOrderId = TyContext.RunHttp.getRequestParam('bindOrderId')
        if bindOrderId is not None:
            params['bindOrderId'] = bindOrderId

        params['loginFlag'] = TyContext.RunHttp.getRequestParamInt('loginFlag', 0)
        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        try:
            datas = clientId.split('_')
            clientSystem = datas[0]
            clientVersion = TyContext.ClientUtils.getVersionFromClientId(clientId)
            clientChannel = datas[2]
        except:
            return True, cls.error_param_clientid

        params['clientId'] = clientId
        params['clientSystem'] = clientSystem
        params['clientVersion'] = clientVersion
        params['clientChannel'] = clientChannel

        return False, params

    @classmethod
    def check_userv4(cls, rpath):
        # cls.__init_checker__()

        if not AccountVerify.sing_verify(rpath):
            return True, cls.error_sing

        params = TyContext.RunHttp.convertArgsToDict()
        # 检查登录参数
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        if appId <= 0:
            return True, cls.error_param_appid
        params['appId'] = appId

        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        params['userId'] = userId

        # bindOrderId = TyContext.RunHttp.getRequestParam('bindOrderId')
        # if bindOrderId is not None:
        #    params['bindOrderId'] = bindOrderId

        params['loginFlag'] = TyContext.RunHttp.getRequestParamInt('loginFlag', 0)
        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        try:
            datas = clientId.split('_')
            clientSystem = datas[0]
            clientVersion = TyContext.ClientUtils.getVersionFromClientId(clientId)
            clientChannel = datas[2]
        except:
            return True, cls.error_param_clientid

        params['clientId'] = clientId
        params['clientSystem'] = clientSystem
        params['clientVersion'] = clientVersion
        params['clientChannel'] = clientChannel

        imei = TyContext.RunHttp.getRequestParam('imei', '')
        #         TyContext.ftlog.debug('imei=', imei)
        imei = AccountVerify.decode_item(imei)
        #         TyContext.ftlog.debug('imei=', imei)
        if len(imei) < 12 or len(imei) > 32:
            imei = ''
        # TyContext.ftlog.debug('imei=', imei)

        imsi = TyContext.RunHttp.getRequestParam('imsi', '')
        #         TyContext.ftlog.debug('imsi=', imsi)
        imsi = AccountVerify.decode_item(imsi)
        #         TyContext.ftlog.debug('imsi=', imei)
        if len(imsi) == 0 or len(imsi) > 15:
            imsi = ''
        # TyContext.ftlog.debug('imsi=', imsi)

        androidId = TyContext.RunHttp.getRequestParam('androidId', '')
        #         TyContext.ftlog.debug('androidId=', androidId)
        androidId = AccountVerify.decode_item(androidId)
        #         TyContext.ftlog.debug('androidId=', androidId)
        if len(androidId) < 12 or len(androidId) > 32:
            androidId = ''
        # TyContext.ftlog.debug('androidId=', androidId)
        idfa = AccountVerify.decode_item(
            TyContext.RunHttp.getRequestParam('idfa', ''))
        params['idfa'] = idfa
        mac = TyContext.RunHttp.getRequestParam('mac', '')
        #         TyContext.ftlog.debug('mac=', mac)
        mac = AccountVerify.decode_item(mac)
        #         TyContext.ftlog.debug('mac=', mac)

        # 获取不到时，mac可能为00:00:00:00:00:00或02:00:00:00:00:00
        # 下面的判断似有问题，但不能改，否则用户下次登录会生成不同的deviceId
        # 而丢失老账户
        mac = mac.replace(':', '')
        badmacs_an = TyContext.Configure.get_global_item_json('badmacs_android', ['000000000000'])
        badmacs_ios = TyContext.Configure.get_global_item_json('badmacs_ios', ['020000000000'])
        if mac in badmacs_ios:  # 如果IOS的mac取不到或者变化020000000000，那么需要加到badmacs_ios集合中
            params['macmd5'] = ''
        else:
            if mac != "" and mac not in badmacs_an:  # 如果安卓的mac取值出现问题，那么需要将错误值加入badmacs_an
                mac = mac.replace(':', '')
                if len(mac) != 12:
                    TyContext.ftlog.info('the mac is error ! [', mac, ']')
                    mac = ''
            else:
                TyContext.ftlog.info('the mac is error ! [', mac, ']')
                mac = ''
                #         TyContext.ftlog.debug('mac=', mac)

        uuid = TyContext.RunHttp.getRequestParam('uuid', '')
        #         TyContext.ftlog.debug('uuid=', uuid)
        if len(uuid) != 32:
            uuid = ''

        if mac in badmacs_ios:
            uuid = uuid.lower()

        id_str = mac + '|' + imei + '|' + androidId + '|' + uuid
        TyContext.ftlog.info('deviceId str=', id_str)
        _devid = AccountVerify.md5(id_str)
        params['deviceId'] = _devid
        TyContext.ftlog.debug('after check user params-->', params)
        return False, params

    @classmethod
    def set_user_check(cls, rpath, params):

        # 检查登录参数
        name = TyContext.RunHttp.getRequestParam('name', None)
        if name != None:
            if len(name) > 21 or name.find('"') >= 0 or name.find("'") >= 0:
                return True, cls.error_param_nickname
            params['name'] = name
        else:
            params['name'] = ''

        sex = TyContext.RunHttp.getRequestParamInt('sex', -1)
        if sex != -1:
            if not (sex == 0 or sex == 1):
                return True, cls.error_param_sex
            params['sex'] = sex
        else:
            params['sex'] = ''

        headurl = TyContext.RunHttp.getRequestParam('headurl', None)
        if headurl != None:
            if len(headurl) > 256 or headurl.find('"') >= 0 or headurl.find("'") >= 0:
                return True, cls.error_param_headurl
            params['headurl'] = headurl
        else:
            params['headurl'] = ''

        address = TyContext.RunHttp.getRequestParam('address', None)
        if address != None:
            if len(address) > 125 or address.find('"') >= 0 or address.find("'") >= 0:
                return True, cls.error_param_address
            params['address'] = address
        else:
            params['address'] = ''

        idcardno = TyContext.RunHttp.getRequestParam('idcardno', None)
        if idcardno != None:
            if len(idcardno) > 32 or idcardno.find('"') >= 0 or idcardno.find("'") >= 0:
                return True, cls.error_param_idcardno
            params['idcardno'] = idcardno
        else:
            params['idcardno'] = ''

        truename = TyContext.RunHttp.getRequestParam('truename', None)
        if truename != None:
            if len(truename) > 12 or truename.find('"') >= 0 or truename.find("'") >= 0:
                return True, cls.error_param_truename
            params['truename'] = truename
        else:
            params['truename'] = ''

        phonenumber = TyContext.RunHttp.getRequestParam('phonenumber', None)
        if phonenumber != None:
            if len(phonenumber) > 12 or phonenumber.find('"') >= 0 or phonenumber.find("'") >= 0:
                return True, cls.error_param_phonenumber
            params['phonenumber'] = phonenumber
        else:
            params['phonenumber'] = ''

        lang = TyContext.RunHttp.getRequestParam('lang', None)
        if lang != None:
            params['lang'] = lang

        country = TyContext.RunHttp.getRequestParam('country', None)
        if country != None:
            params['country'] = country

        signature = TyContext.RunHttp.getRequestParam('signature', None)
        if signature != None:
            params['signature'] = signature

        agreeAddFriend = TyContext.RunHttp.getRequestParam('agreeAddFriend', None)
        if agreeAddFriend != None:
            params['agreeAddFriend'] = agreeAddFriend

        email = TyContext.RunHttp.getRequestParam('email', None)
        if email != None:
            email = string.strip(unicode(email))
            if len(email) > 0:
                params['email'] = email

        return False, params
