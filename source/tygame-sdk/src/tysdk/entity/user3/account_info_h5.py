# -*- coding=utf-8 -*-

import json
from hashlib import md5

import datetime

from tyframework.context import TyContext
from tysdk.entity.ads.advertise import AdvertiseService
from tysdk.entity.beautycertify3.beautycertify import BeautyCertifyService
from tysdk.entity.beautycertify3.userphotov3 import UserPhotoService, UserPhoto
from tysdk.entity.pay_common.clientrevision import ClientRevision
from tysdk.entity.user_common.account_360 import Account360
from tysdk.entity.user_common.account_helper import AccountHelper
from tysdk.entity.user_common.constants import AccountConst
from tysdk.entity.user_common.username import UsernameGenerator


class AccountInfo():
    DEFAULT_LOGCLIENT_INFO = None

    @classmethod
    def __filter_qhimg__(cls, headurl):
        headurl = unicode(headurl)
        if headurl.find('qhimg.com') > 0:
            return ''
        return headurl

    @classmethod
    def doGetUserInfo(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doGetUserInfo->rparams=', rparams)
        userId = rparams['userId']
        if userId > 0:
            TyContext.MySqlSwap.checkUserDate(userId)
            AccountHelper.restore_avatar_verify_set(userId)
            # 获取玩家基本信息
            userEmail, userName, coin, userPurl, userSex, userSnsId, bindMobile = \
                TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId),
                                            'email', 'name', 'diamond', 'purl', 'sex', 'snsId', 'bindMobile')
            # 获取玩家绑定类型
            userType = 0
            if bindMobile != None and len(str(bindMobile)) == 11:
                userType = userType | 1
            if userEmail != None and len(userEmail) > 0:
                userType = userType | 2
            if userSnsId != None and len(str(userSnsId)) > 0:
                userType = userType | 4
            mo.setResult('userType', userType)

            baseinfo = {'userId': userId, 'userName': TyContext.KeywordFilter.replace(unicode(userName)), 'coin': coin,
                        'userPurl': cls.__filter_qhimg__(userPurl),
                        'userSex': userSex, 'userType': userType}
            baseinfo = json.dumps(baseinfo)
            mo.setResult('code', 0)
            mo.setResult('info', baseinfo)
        else:
            mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
            mo.setResult('info', '参数错误')
        return

    @classmethod
    def __set_user_info_return__(cls, rparams, mo):
        userId = rparams['userId']
        nickname, sex, headurl, phonenumber = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId),
                                                                          'name', 'sex', 'purl', 'phonenumber')
        mo.setResult('code', 0)
        mo.setResult('name', TyContext.KeywordFilter.replace(unicode(nickname)))
        mo.setResult('sex', sex)
        mo.setResult('purl', cls.__filter_qhimg__(headurl))
        mo.setResult('phonenumber', unicode(phonenumber))
        TyContext.ftlog.debug(cls.__name__, '__set_user_info_return__ mo=', mo.packJson())

    @classmethod
    def doSetUserInfo(cls, rparams, mo, needReturn=True):
        TyContext.ftlog.info(cls.__name__, 'doSetUserInfo->rparams=', rparams, 'needReturn=', needReturn)
        userId = rparams.get('userId', 0)
        if userId <= 0:
            return

        nickname = rparams.get('name', '')
        sex = str(rparams.get('sex', ''))
        headurl = rparams.get('headurl', '')
        address = rparams.get('address', '')
        idcardno = rparams.get('idcardno', '')
        truename = rparams.get('truename', '')
        phonenumber = rparams.get('phonenumber', '')
        lang = rparams.get('lang', None)
        country = rparams.get('country', None)
        signature = rparams.get('signature', None)
        agreeAddFriend = rparams.get('agreeAddFriend', None)
        email = rparams.get('email', None)

        datas = []

        if len(address) > 0:
            datas.append('address')
            datas.append(address)

        if len(idcardno) > 0:
            datas.append('idcardno')
            datas.append(idcardno)

        if len(truename) > 0:
            datas.append('truename')
            datas.append(truename)

        if len(phonenumber) > 0:
            datas.append('phonenumber')
            datas.append(phonenumber)

        if lang != None:
            datas.append('lang')
            datas.append(lang)

        if country != None:
            datas.append('country')
            datas.append(country)

        if signature != None:
            datas.append('signature')
            datas.append(TyContext.KeywordFilter.replace(signature))

        if agreeAddFriend != None:
            if agreeAddFriend == '0' or agreeAddFriend == '1':
                datas.append('agreeAddFriend')
                datas.append(int(agreeAddFriend))

        if email != None:
            datas.append('email')
            datas.append(email)

        if len(sex) > 0 and sex in ('0', '1'):
            datas.append('sex')
            datas.append(sex)
            oldSex = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sex')
            if oldSex == None:
                oldSex = sex
            if int(oldSex) != int(sex):
                BeautyCertifyService.onUserSexChanged(userId, oldSex, sex)

        TyContext.ftlog.debug('nickname=[', nickname, ']')

        if nickname == "LikaiAndZengxinxin" and TyContext.TYGlobal.corporation() == "pineapple":
            pass
        elif len(nickname) > 0:
            newNameIs360Default = Account360.isDefault360Username(nickname)
            if newNameIs360Default:
                oldname = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'name')
                TyContext.ftlog.debug('nickname=[', nickname, '] oldname=[', oldname, '] sex=[', sex, ']')
                if not oldname or Account360.isDefault360Username(oldname):
                    if sex not in ('0', '1'):
                        sex = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sex')
                        TyContext.ftlog.debug('nickname=[', nickname, '] oldname=[', oldname, '] oldsex=[', sex, ']')
                    nickname = UsernameGenerator.getInstance().generate(sex)
                    # 设定
                else:
                    # 保持原名字
                    nickname = None
            else:
                # 设定
                pass

            if nickname != None:
                # 需要根据不同的游戏ID做屏蔽是否不再允许再次更改.(appId 1-19)appId 为 12和15仍可以通过此接口修改名称(大菠萝,海外德州)
                appId = int(rparams.get('appId', '0'))
                accessAppId = [1, 2, 3, 4, 5, 6, 7, 8, 12, 15]  # h5mod
                if appId in accessAppId:
                    datas.append('name')
                    datas.append(nickname)
                    # 修改昵称次数
                    if needReturn:
                        setTimes = TyContext.RedisUser.execute(userId, 'HINCRBY', 'user:' + str(userId), 'set_name_sum',
                                                               1)
                        if TyContext.TYGlobal.corporation() == "pineapple":
                            if setTimes > 1:
                                mo.setResult('code', 1)
                                return
        if len(headurl) > 0:
            UserPhotoService.setUserPhoto(userId, UserPhoto.PHOTO_TYPE_AVATAR, headurl)

        TyContext.ftlog.debug('datas', datas, userId)
        if len(datas) > 0:
            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), *datas)

        if needReturn:
            clientSystem = rparams.get('clientSystem', '')
            oldname = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'name')
            newname = rparams.get('name', '')
            if clientSystem == 'Winpc' and oldname != newname:
                mo.setResult('code', 2)
                mo.setError(2, '老板，昵称不能随意修改哦。')
                TyContext.ftlog.debug(cls.__name__, 'doSetUserInfo->mo', mo)
            else:
                cls.__set_user_info_return__(rparams, mo)

    @classmethod
    def doSetUserAvatar(cls, rparams, mo):
        userId = rparams['userId']
        url = rparams['url']
        data = str(rparams['data'])

        TyContext.ftlog.info(cls.__name__, 'doSetUserAvatar->rparams=', userId, url, repr(data[0:125]))

        if len(url) > 0:
            UserPhotoService.setUserPhoto(userId, UserPhoto.PHOTO_TYPE_AVATAR, url)
        else:
            UserPhotoService.uploadUserPhoto(userId, UserPhoto.PHOTO_TYPE_AVATAR, data)

        cls.__set_user_info_return__(rparams, mo)

    @classmethod
    def doSetPasswd(cls, params, mo, checkOldPasswd=True):
        TyContext.ftlog.info(cls.__name__, 'doSetPasswd->rparams=', params)
        userId = cls.__get_param__(params, 'userId')
        oldpasswd = cls.__get_param__(params, 'oldpasswd')
        newpasswd = cls.__get_param__(params, 'newpasswd')

        dbPassword, changePwdCount = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'password',
                                                                 'changePwdCount')
        # 效验旧密码
        if checkOldPasswd and oldpasswd != '':
            m = md5()
            m.update(str(oldpasswd))
            oldPasswordmd5 = m.hexdigest()
            if str(dbPassword) != str(oldpasswd) and str(dbPassword) != oldPasswordmd5:
                mo.setResult('code', AccountConst.CODE_USER_OLD_PWD_ERROR)
                mo.setResult('info', '旧密码输入错误！')
                return
        # 更新玩家密码及更改密码次数
        if changePwdCount == None:
            changePwdCount = 0

        changePwdCount = int(changePwdCount) + 1
        TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), 'password', newpasswd, 'changePwdCount',
                                    changePwdCount)
        mo.setResult('code', 0)
        mo.setResult('info', '设置密码成功')
        mo.setResult('userId', userId)
        mo.setResult('userPwd', newpasswd)

        return

    @classmethod
    def _is_clientip_restricted(cls, clientid, fromip):
        TyContext.ftlog.debug('_is_clientip_restricted clientid', clientid,
                              'fromip', fromip)
        if fromip in TyContext.Configure.get_game_item_json(9998, 'clientip_restricted_white', []):
            return False
        if not clientid or not fromip:
            TyContext.ftlog.error('_is_clientip_restricted True '
                                  'clientid or fromip is blank')
            return True
        daily_limit = TyContext.Configure.get_global_item_int(
            'newuser.ip.count.limit')
        TyContext.ftlog.debug('_is_clientip_restricted daily_limit', daily_limit)
        if not daily_limit:
            return False
        today = datetime.date.today().isoformat()
        lastday = TyContext.RedisMix.execute(
            'HGET', 'newuser.ip.count', clientid + ':' + fromip + ':today')
        if not lastday or today != lastday:
            TyContext.RedisMix.execute('HMSET', 'newuser.ip.count',
                                       clientid + ':' + fromip, 1,
                                       clientid + ':' + fromip + ':today', today)
            return False
        count = TyContext.RedisMix.execute(
            'HINCRBY', 'newuser.ip.count', clientid + ':' + fromip, 1)
        if count > daily_limit:
            return True
        return False

    @classmethod
    def _is_networkip_restricted(cls, clientid, fromip):
        TyContext.ftlog.debug('_is_networkip_restricted clientid', clientid,
                              'fromip', fromip)
        if not clientid or not fromip:
            TyContext.ftlog.error('_is_networkip_restricted True '
                                  'clientid or fromip is blank')
            return True
        limit_ipnetworks_dict = TyContext.Configure.get_global_item_json('newuser.ipnetwork.limit', {})
        limit_ipnetworks = limit_ipnetworks_dict.get(clientid, [])
        TyContext.ftlog.debug('_is_networkip_restricted clientid', clientid, 'limit_ipnetworks', limit_ipnetworks)
        if not limit_ipnetworks:
            return False
        fromipAddr = TyContext.IPAddress(fromip)
        for ipnetwork in limit_ipnetworks:
            if fromipAddr in TyContext.IPNetwork(ipnetwork):
                TyContext.ftlog.info('_is_networkip_restricted clientid ', clientid, 'fromip', fromip,
                                     'ipnetwork', ipnetwork, 'restricted')
                return True

        return False

    @classmethod
    def createNewUser(cls, params, userType, setDevMap=True):
        TyContext.ftlog.info(cls.__name__, 'createNewUser start: userType=',
                             userType, 'params=', params)
        appId = cls.__get_param__(params, 'appId')
        deviceId = cls.__get_param__(params, 'deviceId')
        mail = cls.__get_param__(params, 'email')
        snsId = cls.__get_param__(params, 'snsId')
        userAccount = cls.__get_param__(params, 'userAccount')
        mobile = str(cls.__get_param__(params, 'mobile'))
        clientId = cls.__get_param__(params, 'clientId')

        if clientId.startswith('robot'):
            uid = TyContext.RedisMix.execute('INCR', 'global.robotid')
            if uid > 9999:
                TyContext.ftlog.error('ERROR toomuch robot users !!!!')
                uid = 0
            uid = str(uid)
        else:
            fromip = TyContext.RunHttp.get_client_ip()
            if cls._is_networkip_restricted(clientId, fromip):
                return -1
            if cls._is_clientip_restricted(clientId, fromip):
                TyContext.ftlog.info('createNewUser clientid', clientId,
                                     'ip', fromip, 'restricted')
                return -1

            uid = str(TyContext.RedisMix.execute('INCR', 'global.userid'))
        if int(uid) <= 0:
            #            TyContext.BiReport.report_bi_sdk_login(
            #                AccountConst.CREATE_FAIL_EVENTIDS[userType], 0, appId, clientId,
            #                ['', mail, snsId, mobile][userType],
            #                AccountConst.CODE_USER_NEW_UID_ERROR, devId=deviceId)
            return 0

        datas = {
            'password': cls.__get_param__(params, 'passwd'),
            'mdevid': deviceId,
            'isbind': 1 if userType else 0,
            'snsId': snsId,
            'name': cls.__get_param__(params, ['name', 'deviceName']),
            'source': cls.__get_param__(params, 'source'),
            'purl': cls.__get_param__(params, 'purl'),
            'address': cls.__get_param__(params, 'address'),
            'sex': cls.__get_param__(params, 'sex', '0'),
            'state': 0,
            'payCount': 0,
            'snsinfo': cls.__get_param__(params, 'snsinfo'),
            'vip': 0,
            'dayang': 0,
            'idcardno': cls.__get_param__(params, 'idcardno'),
            'phonenumber': cls.__get_param__(params, 'phonenumber'),
            'truename': cls.__get_param__(params, 'truename'),
            'detect_phonenumber': cls.__get_param__(params, 'detect_phonenumber'),
            'email': mail,
            'createTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'userAccount': userAccount,
            'clientId': clientId,
            'appId': appId,
            'bindMobile': mobile,
            'mac': cls.__get_param__(params, 'mac'),
            'idfa': cls.__get_param__(params, 'idfa'),
            'imei': cls.__get_param__(params, 'imei'),
            'imsi': cls.__get_param__(params, 'imsi', ''),
            'androidId': cls.__get_param__(params, 'androidId'),
            'uuid': cls.__get_param__(params, 'uuid'),
            'userId': uid,
            'sendMeGift': 1,
            "lang": cls.__get_param__(params, 'lang'),
            "country": "",
            "signature": "",
            "agreeAddFriend": 1,
            "email": "",
        }
        if datas['sex'] == '':
            datas['sex'] = '0'

        if datas['purl'] == '':
            datas['purl'] = UserPhotoService.getDefaultUserAvatar(int(uid), clientId)

        is_winpc = cls.__get_param__(params, 'clientSystem').lower() == 'winpc'
        name = datas['name']
        if not name or Account360.isDefault360Username(name) or is_winpc:
            genUsername = UsernameGenerator.getInstance().generate(datas['sex'])
            if genUsername:
                datas['name'] = genUsername

        # 设置用户数据
        udkv = []
        for k, v in datas.items():
            udkv.append(k)
            udkv.append(v)
        #         TyContext.ftlog.debug('createNewUser->values=', udkv)
        TyContext.RedisUser.execute(uid, 'HMSET', 'user:' + uid, *udkv)
        TyContext.UserProps.incr_coin(int(uid), int(appId), 0, TyContext.ChipNotEnoughOpMode.NOOP,
                                      TyContext.BIEventId.UNKNOWN, clientId=clientId)
        TyContext.UserProps.incr_diamond(int(uid), int(appId), 0, TyContext.ChipNotEnoughOpMode.NOOP,
                                         TyContext.BIEventId.UNKNOWN, clientId=clientId)
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
        if setDevMap and len(deviceId) > 0 and deviceId != '528c8e6cd4a3c6598999a0e9df15ad32':
            TyContext.RedisUserKeys.execute('SET', 'devidmap3:' + deviceId, uid)

        cls.updateUserSessionInfo(appId, uid, params)
        TyContext.BiReport.user_register(appId, uid, userType,
                                         clientId, TyContext.RunHttp.get_client_ip(),
                                         deviceId, params=TyContext.RunHttp.convertArgsToDict(),
                                         rpath=TyContext.RunHttp.get_request_path())
        TyContext.BiReport.report_bi_sdk_login(
            AccountConst.CREATE_SUCC_EVENTIDS[userType], uid, appId, clientId,
            ['', mail, snsId, mobile][userType], 0, devId=deviceId)
        #         Report.recoderUserNew( appId, uid, userType)
        TyContext.UserProps.check_data_update_hall(int(uid), appId, True)
        AdvertiseService.on_user_created(int(uid))
        return int(uid)

    @classmethod
    def __get_param__(cls, params, key, defaultValue=''):
        if isinstance(key, (str, unicode)):
            if key in params:
                return params[key]
        elif isinstance(key, (list, tuple)):
            for subkey in key:
                if subkey in params:
                    val = params[subkey]
                    if not isinstance(val, (str, unicode)):
                        val = str(val)
                    if len(val) > 0:
                        return val
        return defaultValue

    @classmethod
    def updateUserSessionInfo(cls, appId, userId, params):

        deviceId = cls.__get_param__(params, 'deviceId')
        clientId = cls.__get_param__(params, 'clientId')
        phoneType = cls.__get_param__(params, 'phoneType')
        detect_phonenumber = cls.__get_param__(params, 'detect_phonenumber')
        idfa = cls.__get_param__(params, 'idfa')
        iccid = cls.__get_param__(params, 'iccid')
        svninfo = cls.__get_param__(params, 'svninfo')
        snsInfo = cls.__get_param__(params, 'snsInfo')  # for h5

        datas = []
        if appId > 0:
            datas.append('sessionAppId')
            datas.append(appId)

        if len(deviceId) > 0:
            datas.append('sessionDevId')
            datas.append(deviceId)

        if len(clientId) > 0:
            datas.append('sessionClientId')
            datas.append(clientId)

        if svninfo:
            datas.append('sessionClientSdkRev')
            datas.append(ClientRevision.get_client_sdk_revision(svninfo))
        else:
            datas.append('sessionClientSdkRev')
            datas.append(3333)

        if len(idfa) > 0:
            datas.append('sessionIdfa')
            datas.append(idfa)

        if snsInfo:
            datas.append('sessionSnsInfo')
            datas.append(json.dumps(snsInfo))

        datas.append('sessionIccid')
        datas.append(iccid)

        clientIP = TyContext.RunHttp.get_client_ip()
        if clientIP and len(clientIP) > 0:
            datas.append('sessionClientIP')
            datas.append(clientIP)

        # 2014/12/5 客户端无卡时phoneType为空串，这时也要更新sessionPhoneType
        # 2015/2/27 客户端无卡时phoneType传other
        # 2015/2/27 绑定手机号时，客户端没有传输phoneType字段，此时不应更新sessionPhoneType
        is_check_bind = cls.__get_param__(params, 'bindOrderId')
        if not is_check_bind:
            datas.append('sessionPhoneType')
            datas.append(phoneType)

        if detect_phonenumber and len(detect_phonenumber) > 10:
            datas.append('detect_phonenumber')
            datas.append(detect_phonenumber)

        #         TyContext.ftlog.info('updateUserSessionInfo->userId=', userId, 'datas=', datas)
        if len(datas) > 0:
            TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId), *datas)

    @classmethod
    def fillUserLoginInfoV3(cls, params, mo, userId, isLogin, isCreate):

        # 兼容客户端之前的用户未能在创建时传入imsi
        imsi = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'imsi')
        if not imsi:
            if 'imsi' in params and params['imsi']:
                TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'imsi', params['imsi'])

                TyContext.ftlog.debug('fillUserLoginInfoV3 in imsi', imsi, 'params[imsi]', params['imsi'])

        clientIp = TyContext.RunHttp.get_client_ip()

        # IMPORTANT!! used by GDSS statistics
        TyContext.ftlog.info('fillUserLoginInfoV3 in userId=', userId, 'isLogin=', isLogin,
                             'isCreate=', isCreate, 'clientId=', params['clientId'],
                             'clientIp=', clientIp, 'gameId=', params['appId'], 'params=', params)

        appId = params['appId']
        cls.updateUserSessionInfo(appId, userId, params)

        # 查询用户基本信息
        mo.setResult('code', AccountConst.CODE_USER_SUCCESS)
        mo.setResult('userId', userId)
        mo.setResult('appId', appId)

        # 查询用户基本信息
        uname, authorCode, email = TyContext.AuthorCode.creatUserAuthorCodeNew(userId)
        mo.setResult('authorCode', authorCode)
        mo.setResult('userName', TyContext.KeywordFilter.replace(unicode(uname)))
        mo.setResult('userEmail', unicode(email))

        if isCreate:
            mo.setResult('isCreate', 1)
        else:
            mo.setResult('isCreate', 0)

        # 获取玩家绑定类型
        userType = 0
        bindMobile, userEmail, userSnsId, userDBPwd, changePwdCount, log_report, exception_report = TyContext.RedisUser.execute(
            userId, 'HMGET', 'user:' + str(userId),
            'bindMobile', 'email', 'snsId', 'password', 'changePwdCount',
            'log_report', 'exception_report')
        if log_report != 1:
            log_report = 0
        if exception_report != 1:
            exception_report = 0

        if bindMobile != None and len(str(bindMobile)) == 11:
            userType = userType | 1
        if userEmail != None and len(userEmail) > 0:
            userType = userType | 2
        if userSnsId != None and len(str(userSnsId)) > 0:
            userType = userType | 4
        mo.setResult('userType', userType)
        if userSnsId and len(userSnsId) > 0:
            mo.setResult('snsId', userSnsId)
        mo.setResult('userPwd', unicode(userDBPwd))
        mo.setResult('mobile', unicode(bindMobile))
        # 获取玩家修改密码次数
        if changePwdCount == None:
            changePwdCount = 0
        mo.setResult('changePwdCount', changePwdCount)
        mo.setResult('log_report', log_report)
        mo.setResult('exception_report', exception_report)

        checkcode = ''
        if appId < 10000:
            # 途游自己的游戏
            cls.__append_tcp_infos__(appId, userId, params['clientId'], mo)
            clientId = params.get('clientId', 'unknow')
            AccountHelper.append_ios_idfa_flg(userId, appId, clientId, mo)
            cls.__append_logclient_infos__(userId, clientId, mo)
        else:
            checkcode = TyContext.AuthorCode.makeLoginCode(userId, appId, authorCode)
            mo.setResult('usercode', checkcode)

        # 为了兼容使用新登录老支付，当这种结合过期后，删除authInfo字段
        ainfo = {'authcode': authorCode, 'account': email, 'uid': userId, 'usercode': checkcode}
        ainfo = json.dumps(ainfo)
        mo.setResult('authInfo', ainfo)

    @classmethod
    def __append_logclient_infos__(cls, userId, clientId, mo):
        try:
            datas = TyContext.RedisMix.execute('HGET', 'client.log.report.user.url', userId)
            if datas == None:
                datas = TyContext.RedisMix.execute('HGET', 'client.log.report.client.url', clientId)
            if datas == None:
                datas = TyContext.RedisMix.execute('HGET', 'client.log.report.client.url', 'default')
            if datas != None:
                datas = TyContext.strutil.loads(datas)
            else:
                datas = {'logreporturl': '', 'loguploadurl': ''}
        except:
            TyContext.ftlog.exception(userId, clientId)
            datas = {'logreporturl': '', 'loguploadurl': ''}
        mo.setResult('logclient', datas)
        pass

    @classmethod
    def __append_tcp_infos__(cls, gameId, userId, clientId, mo):
        mo.setResult('connectTimeOut', TyContext.Configure.get_global_item_int('client.connect.timeouts', 35))
        mo.setResult('heartBeat', TyContext.Configure.get_global_item_int('client.heart.beat.times', 6))
        tcpip, tcpport = TyContext.ServerControl.findUserTcpAddress(gameId, clientId, userId)
        # assert(tcpip)
        # assert(tcpport)
        mo.setResult('tcpsrv', {'ip': tcpip, 'port': tcpport})
