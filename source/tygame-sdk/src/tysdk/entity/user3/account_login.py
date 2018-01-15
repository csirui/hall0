# -*- coding=utf-8 -*-

import random
import re
import time

from tyframework.context import TyContext
from tysdk.entity.report4.report_ios import ReportIOS
from tysdk.entity.user3.account_info import AccountInfo
from tysdk.entity.user_common.account_360 import Account360
from tysdk.entity.user_common.account_aisi import AccountAiSi
from tysdk.entity.user_common.account_anzhi import AccountAnZhi
from tysdk.entity.user_common.account_bdgame import AccountBDGame
from tysdk.entity.user_common.account_changba import AccountChangba
from tysdk.entity.user_common.account_coolpad import AccountCoolpad
from tysdk.entity.user_common.account_fb import AccountFaceBook
from tysdk.entity.user_common.account_haimawan import AccountHaiMaWan
from tysdk.entity.user_common.account_hejiaoyu import AccountHejiaoyu
from tysdk.entity.user_common.account_helper import AccountHelper
from tysdk.entity.user_common.account_huabeidianhua import AccountHuabeidianhua
from tysdk.entity.user_common.account_iTools import AccountiTools
from tysdk.entity.user_common.account_iiapple import AccountIIApple
from tysdk.entity.user_common.account_jolo import AccountJolo
from tysdk.entity.user_common.account_jrtt import AccountJRTT
from tysdk.entity.user_common.account_jusdk import AccountJusdk
from tysdk.entity.user_common.account_kuaiwan import AccountKuaiwan
from tysdk.entity.user_common.account_kuaiyongpingguo import AccountKuaiYongPingGuo
from tysdk.entity.user_common.account_lenovo import AccountLenovo
from tysdk.entity.user_common.account_letv import AccountLetv
from tysdk.entity.user_common.account_liebao import AccountLiebao
from tysdk.entity.user_common.account_lizi import AccountLizi
from tysdk.entity.user_common.account_m4399 import AccountM4399
from tysdk.entity.user_common.account_meizu import AccountMeizu
from tysdk.entity.user_common.account_momo import AccountMomo
from tysdk.entity.user_common.account_mumayi import AccountMumayi
from tysdk.entity.user_common.account_mzwonline import AccountMZWOnline
from tysdk.entity.user_common.account_nubia import AccountNubia
from tysdk.entity.user_common.account_papa import AccountPapa
from tysdk.entity.user_common.account_pengyouwan import AccountPengyouwan
from tysdk.entity.user_common.account_qtld import AccountQtld
from tysdk.entity.user_common.account_uc import AccountUC
from tysdk.entity.user_common.account_vivo import AccountVivo
from tysdk.entity.user_common.account_vivounion import AccountVivounion
from tysdk.entity.user_common.account_weixin import AccountWeixin
from tysdk.entity.user_common.account_xy import AccountXY
from tysdk.entity.user_common.account_yiwan import AccountYiwan
from tysdk.entity.user_common.account_youku_h5 import AccountYouku
from tysdk.entity.user_common.account_ysdk import AccountYsdk
from tysdk.entity.user_common.account_yygame import AccountYYgame
from tysdk.entity.user_common.account_zhangyue import AccountZhangyue
from tysdk.entity.user_common.account_zhuoyi import AccountZhuoyi
from tysdk.entity.user_common.constants import AccountConst
from tysdk.entity.user_common.verify import AccountVerify


class AccountLogin():
    @classmethod
    def doLoginByDevId(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doLoginByDevId->rparams=', rparams)

        userId = cls.__find_userid_by_devid_map_v3__(rparams['deviceId'])
        TyContext.ftlog.info(cls.__name__, 'doLoginByDevIdAfter1 userid=', userId, '->rparams=', rparams)
        if userId <= 0 and rparams.get('mac', ''):
            macmd5 = rparams.get('macmd5', '')
            if macmd5:
                userId = cls.__find_userid_by_devid_map_v2__(macmd5)

        loginType = AccountConst.USER_TYPE_DEVICE
        TyContext.ftlog.info(cls.__name__, 'doLoginByDevIdAfter2 userid=', userId, '->rparams=', rparams)

        if userId > 0:
            cls._do_check_login(rparams, userId, mo, loginType)
        else:
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
            else:
                if userId == -1:
                    mo.setResult('code', AccountConst.CODE_USER_DEV_REG_FAILE)
                    mo.setResult('info', '您的IP地址异常，暂时无法注册新账号，请电话联系客服：400-8098-000')
                    # 由于客户端没有正确读取info内容，临时加上tips，等新包上线后删掉tips参数
                    mo.setResult('tips', '您的IP地址异常，暂时无法注册新账号')
                    return
                mo.setResult('code', AccountConst.CODE_USER_GUEST_REG_FAILE)
                mo.setResult('info', '设备用户注册失败')
        clientIp = TyContext.UserSession.get_session_client_ip(int(userId))
        TyContext.ftlog.info("UNIVERSAL_LOG_LOGIN", "userId=", userId, 'clientIp=', clientIp, 'version=', 'v3', 'type=',
                             'doLoginByDevId', 'login_params=', rparams)

    @classmethod
    def doCreateAccount(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doCreateAccount->rparams=', rparams)
        rparams['passwd'] = 'ty' + str(random.randint(100000, 999999))
        loginType = AccountConst.USER_TYPE_DEVICE
        userId = AccountInfo.createNewUser(rparams, loginType, False)
        if userId > 0:
            AccountInfo.fillUserLoginInfoV3(rparams, mo, userId, True, True)
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_SUCC_EVENTIDS[loginType], userId,
                rparams['appId'], rparams['clientId'],
                str(rparams.get(AccountConst.LOGIN_BINDID_KEY[loginType], '')),
                0, devId=rparams.get('deviceId', ''))
        else:
            mo.setResult('code', AccountConst.CODE_USER_GUEST_REG_FAILE)
            mo.setResult('info', '用户账号建立失败')

    @classmethod
    def doLoginByMobile(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doLoginByMobile->rparams=', rparams)
        chkMobile = rparams['mobile']
        userId = cls.__find_userid_by_mobile__(chkMobile, rparams=rparams)

        #         TyContext.ftlog.info(cls.__name__, 'doLoginByMobile->userId=', userId, 'rparams=', rparams)
        cls._do_check_login(rparams, userId, mo, AccountConst.USER_TYPE_MOBILE)

    @classmethod
    def doLoginByTyID(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doLoginByTyID->rparams=', rparams)
        tuyooId = int(rparams['tuyooId'])

        # tuyouId必须需要密码登录
        if not 'passwd' in rparams:
            mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            return

        userId = cls.__find_userid_by_tyid__(tuyooId, rparams=rparams)
        if not userId or userId < 0:
            mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
            mo.setResult('info', '我们发现您的途游帐号存在安全隐患，为了保障您的帐号安全，请联系客服电话:4008098000')
            return

        '''
        #临时处理德州盗号情况，针对已绑定第三方账号的玩家，并且剩余金币大于50w的用户禁止通过途游ID进行登录
        forbidden, info, extinfo = cls.__check_snsid_by_tyid__(userId)
        if forbidden:
            mo.setResult('code', AccountConst.CODE_USER_LOGIN_FORBID)
            mo.setResult('info', info)
            mo.setResult('extinfo', extinfo)
            return
        '''
        cls._do_check_login(rparams, userId, mo, AccountConst.USER_TYPE_DEVICE)
        clientIp = TyContext.UserSession.get_session_client_ip(int(userId))
        TyContext.ftlog.info("UNIVERSAL_LOG_LOGIN", "userId=", userId, 'clientIp=', clientIp, 'version=', 'v3', 'type=',
                             'doLoginByTyID', 'login_params=', rparams)

    @classmethod
    def doRenewAuthorCodeByTyId(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doRenewAuthorCodeByTyId->rparams=', rparams)
        tuyooId = rparams['tuyooId']
        userId = cls.__find_userid_by_tyid__(tuyooId)
        _, author_code, _ = TyContext.AuthorCode.creatUserAuthorCodeNew(userId)
        if not author_code:
            mo.setResult('code', AccountConst.CODE_USER_AUTHORCODE_RENEW_FAIL)
            mo.setResult('info', '刷新authorcode失败')
            return
        mo.setResult('code', AccountConst.CODE_USER_SUCCESS)
        mo.setResult('authorCode', author_code)

    @classmethod
    def doLoginByMail(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doLoginByMail->rparams=', rparams)
        mail = rparams['mail']
        userId = cls.__find_userid_by_mail__(mail, rparams=rparams)
        if userId <= 0:
            # 补丁:重度游戏那边的邮箱用户
            userId = cls.__find_userid_by_account__(mail, rparams=rparams)

        #         TyContext.ftlog.info(cls.__name__, 'doLoginByMail->userId=', userId, 'rparams=', rparams)
        cls._do_check_login(rparams, userId, mo, AccountConst.USER_TYPE_DEVICE)

    # deprecated api. use doProcessSnsID now
    @classmethod
    def doLoginBySnsID(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doLoginBySnsID->rparams=', rparams)
        snsId = rparams['snsId']
        # 360SDKv1.0.4版本上传的是access_token区分以前360版本上传的code
        # 长度判断是为了兼容360社交登录
        if snsId.startswith('360'):
            if Account360.doGetUserInfo(rparams, snsId) != True:
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '360登录验证失败！')
                return
            else:
                snsId = rparams['snsId']
        userId = cls.__find_userid_by_snsid__(snsId)
        #         TyContext.ftlog.info(cls.__name__, 'doLoginBySnsID->userId=', userId, 'rparams=', rparams)
        cls._do_check_login(rparams, userId, mo, AccountConst.USER_TYPE_SNS)

    @classmethod
    def doProcessSnsID(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doProcessSnsID->rparams=', rparams)
        snsId = rparams['snsId']
        # 360SDKv1.0.4版本上传的是access_token区分以前360版本上传的code
        # 长度判断是为了兼容360社交登陆
        if snsId.startswith('360'):
            if Account360.doGetUserInfo(rparams, snsId) != True:
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '360登录验证失败！')
                #                TyContext.BiReport.report_bi_sdk_login(
                #                    TyContext.BIEventId.SDK_LOGIN_BY_SNSID_FAIL, 0,
                #                    rparams['appId'], rparams['clientId'], snsId,
                #                    AccountConst.CODE_USER_SNS_GETINFO_ERROR)
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('ucsid'):
            if AccountUC.doGetUserInfo(rparams, snsId) != True:
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'UC登录验证失败！')
                #                TyContext.BiReport.report_bi_sdk_login(
                #                    TyContext.BIEventId.SDK_LOGIN_BY_SNSID_FAIL, 0,
                #                    rparams['appId'], rparams['clientId'], snsId,
                #                    AccountConst.CODE_USER_SNS_GETINFO_ERROR)
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('qtld:'):
            if not AccountQtld.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'qtld登录验证失败！')
                #                TyContext.BiReport.report_bi_sdk_login(
                #                    TyContext.BIEventId.SDK_LOGIN_BY_SNSID_FAIL, 0,
                #                    rparams['appId'], rparams['clientId'], snsId,
                #                    AccountConst.CODE_USER_SNS_GETINFO_ERROR)
                return
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
        elif snsId.startswith('yy'):
            if not AccountYYgame.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'yy 登陆验证失败！')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('meizu'):
            if not AccountMeizu.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'meizu 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('JRTT'):
            if not AccountJRTT.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'jinritoutiao 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith("fb"):
            if not AccountFaceBook.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'facebook 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith("xy"):
            if not AccountXY.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'XY苹果助手 登录验证失败！')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('aisi'):
            if not AccountAiSi.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'AiSi 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('haimawan'):
            if not AccountHaiMaWan.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '海马玩 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('youkuh5'):
            if not AccountYouku.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '优酷登陆验证失败！')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('huabeidianhua'):
            if not AccountHuabeidianhua.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '华北电话 登录验证失败！')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('itools'):
            if not AccountiTools.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'iTools 登陆验证失败！')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('kuaiyongpingguo'):
            if not AccountKuaiYongPingGuo.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'kuaiyongpingguo 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('anzhi'):
            if not AccountAnZhi.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '安智 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('iiapple'):
            if not AccountIIApple.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'iiapple 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('mumayi'):
            if not AccountMumayi.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'mumayi 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('pyw'):
            # 朋友玩没有账号验证接口，所有id都认为合法
            if not AccountPengyouwan.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'pengyouwan 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('m4399'):
            # 朋友玩没有账号验证接口，所有id都认为合法
            if not AccountM4399.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '4399 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('coolpad'):
            if not AccountCoolpad.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'coolpad 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('zhuoyi'):
            if not AccountZhuoyi.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'zhuoyi 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('jolo'):
            if not AccountJolo.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'jolo 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('papa'):
            if not AccountPapa.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'papa 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('kuaiwan'):
            if not AccountKuaiwan.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'kuaiwan 登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('changba'):
            if not AccountChangba.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'changba 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('nubia'):
            if not AccountNubia.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'nubia 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('ysdk'):
            if not AccountYsdk.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '应用宝YSDK 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('letv'):
            if not AccountLetv.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'Letv 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('bdgame'):
            if not AccountBDGame.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'bdgame 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('yiwan'):
            if not AccountYiwan.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '益玩 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('jusdk'):
            if not AccountJusdk.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'Jusdk 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('lizi'):
            if not AccountLizi.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '口袋栗子 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('vivo'):
            if not AccountVivo.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'Vivo 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('lenovo'):
            if not AccountLenovo.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'Lenovo 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('hejiaoyu'):
            if not AccountHejiaoyu.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '和教育 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('muzhiwan'):
            if not AccountMZWOnline.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '拇指玩 登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('zhangyue'):
            if not AccountZhangyue.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '掌阅登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('vivounion'):
            if not AccountVivounion.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', 'vivo union登录验证失败!')
                return
        elif snsId.startswith('momo'):
            if not AccountMomo.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '陌陌登录验证失败!')
                return
            else:
                snsId = rparams['snsId']
        elif snsId.startswith('liebao'):
            if not AccountLiebao.doGetUserInfo(rparams, snsId):
                mo.setResult('code', AccountConst.CODE_USER_PARAM_ERROR)
                mo.setResult('info', '猎豹登陆验证失败!')
                return
            else:
                snsId = rparams['snsId']

        userId = cls.__find_userid_by_snsid__(snsId)
        is_create = False
        if userId <= 0:
            # 效验该deviceId是否存在第三方sns刷号嫌疑
            isFlag, retMsg = cls._check_deviceid_sns_forbidden(rparams)
            if isFlag:
                mo.setResult('code', AccountConst.CODE_USER_SNS_REG_FAILE)
                mo.setResult('info', retMsg)
                return
            rparams['passwd'] = 'ty' + str(random.randint(100000, 999999))
            if snsId.startswith('360'):
                rparams['lang'] = "zh_hans"
            is_create = True
            userId = AccountInfo.createNewUser(rparams, AccountConst.USER_TYPE_SNS, False)
            if userId <= 0:
                mo.setResult('code', AccountConst.CODE_USER_GUEST_REG_FAILE)
                mo.setResult('info', '用户账号建立失败')
                return
            appId = rparams['appId']
            cls.__newaccount_success_callback_(appId, 'newsnsid',
                                               {'appId': appId, 'userId': userId, 'snsId': snsId})
        else:
            rparams['userId'] = userId
            # 2015/2/10 only set name on creating new user
            try:
                del rparams['name']
            except:
                pass
            AccountInfo.doSetUserInfo(rparams, mo, False)
        # 补丁：保存微信openid到用户信息
        # 已经在AccountWeixin中将openid对于的用户信息保存到UserKey数据库中
        if snsId.startswith('wx:'):
            wxopenid = rparams['wxopenid']
            TyContext.RedisUser.execute(userId, 'HSET', 'user:%d' % userId, 'wxopenid', wxopenid)
            TyContext.RedisUserKeys.execute('HSET', 'wxopenid:%s' % wxopenid, 'userId', userId)
        cls._do_check_login(rparams, userId, mo, AccountConst.USER_TYPE_SNS, is_create)
        clientIp = TyContext.UserSession.get_session_client_ip(int(userId))
        TyContext.ftlog.info("UNIVERSAL_LOG_LOGIN", "userId=", userId, 'clientIp=', clientIp, 'version=', 'v3', 'type=',
                             'doProcessSnsID', 'login_params=', rparams)

    @classmethod
    def doLoginByAccount(cls, rparams, mo):
        TyContext.ftlog.info(cls.__name__, 'doLoginByAccount->rparams=', rparams)
        account = rparams['account']

        # tuyouId必须需要密码登录
        if not 'passwd' in rparams:
            mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            return

        userId = cls.__find_userid_by_account__(account, rparams=rparams)
        #         TyContext.ftlog.info(cls.__name__, 'doLoginByAccount->userId=', userId, 'rparams=', rparams)
        cls._do_check_login(rparams, userId, mo, AccountConst.USER_TYPE_DEVICE)

    @classmethod
    def __do_login_done__(cls, rparams, userId, mo, loginType, is_create=False):
        if userId <= 0:
            TyContext.ftlog.error('__do_login_done__ error: userId', userId,
                                  'loginType', loginType, 'is_create', is_create,
                                  'rparams', rparams, 'mo', mo)
            mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            #            TyContext.BiReport.report_bi_sdk_login(
            #                AccountConst.LOGIN_FAIL_EVENTIDS[loginType], userId,
            #                rparams['appId'], rparams['clientId'],
            #                str(rparams.get(AccountConst.LOGIN_BINDID_KEY[loginType], '')),
            #                AccountConst.CODE_USER_NOT_FOUND, devId=rparams.get('deviceId', ''))
            return

        if 'passwd' in rparams and not cls.__check_user_passwd__(userId, rparams['passwd']):
            mo.setResult('code', AccountConst.CODE_USER_PWD_ERROR)
            mo.setResult('info', '通行证或密码错误，请重新输入！')
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_FAIL_EVENTIDS[loginType], userId,
                rparams['appId'], rparams['clientId'],
                str(rparams.get(AccountConst.LOGIN_BINDID_KEY[loginType], '')),
                AccountConst.CODE_USER_PWD_ERROR, devId=rparams.get('deviceId', ''))
            return
        TyContext.UserProps.check_data_update_hall(userId, rparams['appId'])
        AccountInfo.fillUserLoginInfoV3(rparams, mo, userId, True, is_create)
        TyContext.BiReport.report_bi_sdk_login(
            AccountConst.LOGIN_SUCC_EVENTIDS[loginType], userId,
            rparams['appId'], rparams['clientId'],
            str(rparams.get(AccountConst.LOGIN_BINDID_KEY[loginType], '')),
            0, devId=rparams.get('deviceId', ''))
        TyContext.BiReport.user_login(
            rparams['appId'], userId, loginType, rparams['clientId'],
            TyContext.RunHttp.get_client_ip(), rparams.get('deviceId', ''),
            params=TyContext.RunHttp.convertArgsToDict(),
            rpath=TyContext.RunHttp.get_request_path())
        try:
            ReportIOS().on_user_login(userId, rparams)
        except:
            TyContext.ftlog.exception()

    @classmethod
    def _check_deviceid_sns_forbidden(cls, rparams):
        deviceId = rparams.get('deviceId', '')
        snsId = rparams.get('snsId', '')
        if deviceId == '' or snsId == '' or snsId.find('robot_') >= 0:
            return False, None

        deviceid_sns_config = TyContext.Configure.get_global_item_json('deviceid_sns_config', {})
        try:
            new_user_numbers = deviceid_sns_config.get('new_user_numbers', 0)
            new_limit_msg = deviceid_sns_config.get('new_limit_msg', '对不起，您的设备注册已达上限')
            snsid_num = TyContext.RedisUserKeys.execute('LLEN', 'devidtosnsidmap:' + str(deviceId))
            if snsid_num > 0 and snsid_num >= new_user_numbers:
                TyContext.ftlog.info('_check_deviceid_sns_forbidden forbiddendeviceId:'
                                     ' deviceId', deviceId, 'snsId', snsId)
                return True, new_limit_msg

            TyContext.RedisUserKeys.execute('LPUSH', 'devidtosnsidmap:' + str(deviceId), snsId)
            # set expire at next 00:00...
            nt = time.localtime()
            ntsec = 86400 - nt[3] * 3600 + nt[4] * 60 + nt[5]
            TyContext.RedisUserKeys.execute('EXPIRE', 'devidtosnsidmap:' + str(deviceId), ntsec)

        except Exception as e:
            TyContext.ftlog.error('_check_deviceid_sns_forbidden failed:', ' rparams', rparams)

        return False, None

    @classmethod
    def __do_login_double_check__(cls, tuyooId, rparams, mo):
        doubleUsers = TyContext.Configure.get_global_item_hashset('doublue.user.list', [])
        devid = rparams.get('deviceId', '')
        if devid and devid.find('monitor_') >= 0 or devid.find('robot') >= 0:
            return False
        if tuyooId in doubleUsers:
            rparams['passwd'] = 'ty' + str(random.randint(100000, 999999))
            loginType = AccountConst.USER_TYPE_DEVICE
            userId = AccountInfo.createNewUser(rparams, loginType)
            TyContext.ftlog.info('__do_login_double_check__ old uerid=', tuyooId, ' new userid=', userId)
            AccountInfo.fillUserLoginInfoV3(rparams, mo, userId, True, True)
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_SUCC_EVENTIDS[loginType], userId,
                rparams['appId'], rparams['clientId'],
                str(rparams.get(AccountConst.LOGIN_BINDID_KEY[loginType], '')),
                0, devId=rparams.get('deviceId', ''))
            return True
        return False

    @classmethod
    def _do_check_login(cls, rparams, userId, mo, loginType, is_create=False):
        TyContext.ftlog.debug('AccountLogin->_do_check_login begin', userId, loginType)

        if cls.__do_login_double_check__(userId, rparams, mo):
            return

        clientId = rparams.get('clientId', '')
        deviceId = rparams.get('deviceId', '')
        # 检查是否禁止登录
        forbidden, info, extinfo = cls._check_userid_forbidden(
            userId, rparams, loginType)
        if not forbidden:
            forbidden, info, extinfo = cls._check_winpc_devid_login(
                userId, clientId, deviceId, loginType)

        if forbidden:
            mo.setResult('code', AccountConst.CODE_USER_LOGIN_FORBID)
            mo.setResult('info', info)
            mo.setResult('extinfo', extinfo)
            TyContext.BiReport.report_bi_sdk_login(
                AccountConst.LOGIN_FAIL_EVENTIDS[loginType], userId,
                rparams['appId'], rparams['clientId'],
                str(rparams.get(AccountConst.LOGIN_BINDID_KEY[loginType], '')),
                AccountConst.CODE_USER_LOGIN_FORBID,
                devId=deviceId)
            return

        return cls.__do_login_done__(rparams, userId, mo, loginType, is_create)

    @classmethod
    def _check_winpc_devid_login(cls, userId, clientId, deviceId, loginType):
        if loginType != AccountConst.USER_TYPE_DEVICE or not clientId \
                or 'winpc' not in clientId.lower():
            return False, None, None
        isbind, snsId = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%d' % userId,
                                                    'isbind', 'snsId')
        if int(isbind) == AccountConst.USER_TYPE_DEVICE:
            return False, None, None
        TyContext.ftlog.info('_check_winpc_devid_login forbidden: clientId',
                             clientId, 'userId', userId, 'deviceId', deviceId,
                             'isbind', isbind, 'snsId', snsId)
        info = TyContext.Configure.get_global_item_str('winpc_guest_forbidden_info')
        # info = info.format(userId=userId)
        tips = TyContext.Configure.get_global_item_str('winpc_guest_forbidden_tips')
        return True, (info + tips).encode('utf8'), \
               {'info': info.encode('utf8'), 'tips': tips.encode('utf8')}

    @classmethod
    def __check_snsid_by_tyid__(cls, userId):
        if userId <= 0:
            return False, None, None

        user_chip_limited = TyContext.Configure.get_global_item_int('user.chip.limit', 500000)
        snsId, chip = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'snsId', 'chip')
        if snsId == None or chip == None or int(chip) < int(user_chip_limited):
            return False, None, None

        check_user_id = cls.__find_userid_by_snsid__(snsId)

        if check_user_id > 0 and check_user_id == userId:
            TyContext.ftlog.info('__check_snsid_by_tyid__', ' userId', userId, 'chip', chip, 'snsId', snsId)
            info = TyContext.Configure.get_global_item_str('tyId_forbidden_info')
            tips = TyContext.Configure.get_global_item_str('tyId_forbidden_tips')
            return True, (info + tips).encode('utf8'), {'info': info.encode('utf8'), 'tips': tips.encode('utf8')}

        return False, None, None

    @classmethod
    def _check_userid_forbidden(cls, userId, rparams, loginType):
        if userId <= 0:
            return False, None, None
        deviceName = rparams.get('deviceName', '')  # '[0-9a-f]{8}
        phoneType = rparams.get('phoneType', '')  # '3'
        clientSystem = rparams.get('clientSystem', '')  # 'IOS'
        createTime = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId),
                                                 'createTime')  # 2014-10-11 23:25:46.960885
        if clientSystem == 'IOS' and re.match('[0-9a-f]{8}', deviceName) and createTime:
            begTime = time.mktime(time.strptime('2016-01-01 0:0:0.0', '%Y-%m-%d %H:%M:%S.%f'))
            endTime = time.mktime(time.strptime('2016-04-30 23:59:59.0', '%Y-%m-%d %H:%M:%S.%f'))
            try:
                createTime = time.mktime(time.strptime(createTime, '%Y-%m-%d %H:%M:%S.%f'))
            except:
                begTime, createTime, endTime = 0, 0, 0
            if begTime < createTime < endTime:
                TyContext.ftlog.info('_check_userid_forbidden deviceName failed:', 'userId', userId, 'rparams', rparams)
                raise Exception("forbidden userid")

        clientId = rparams.get('clientId', '')
        deviceId = rparams.get('deviceId', '')
        appId = rparams.get('appId')
        try:
            # 获取白名单的clientid
            is_check_waived = TyContext.Configure.get_global_item_int('clientid.waived.confirm', 1)
            if is_check_waived:
                all_waived_clientids = TyContext.Configure.get_configure_json('clientid.number.map', {})
                # TyContext.ftlog.debug('_check_userid_forbidden all_waived_clientids ', all_waived_clientids)
                if all_waived_clientids:
                    clientIdNum = all_waived_clientids.get(clientId)
                    if clientIdNum is None:
                        TyContext.ftlog.info('_check_userid_forbidden not waived:', ' clientId', clientId, 'userId',
                                             userId)
                        # raise Exception("forbidden clientid")
                        info = TyContext.Configure.get_global_item_str('clientid_forbidden_info')
                        tips = TyContext.Configure.get_global_item_str('clientid_forbidden_tips')
                        return True, (info + tips).encode('utf8'), {'info': info.encode('utf8'),
                                                                    'tips': tips.encode('utf8')}
            if clientId and TyContext.RedisForbidden.execute(
                    'EXISTS', 'forbidden:cid:' + str(clientId)):
                TyContext.ftlog.info('_check_userid_forbidden forbiddenuser:'
                                     ' clientId', clientId, 'userId', userId)
                raise Exception("forbidden clientid")

            if TyContext.RedisForbidden.execute('EXISTS', 'forbidden:uid:%d' % (userId)):
                TyContext.ftlog.info('_check_userid_forbidden forbiddenuser: userId', userId)
                raise Exception("forbidden userid")

            if deviceId and TyContext.RedisForbidden.execute('EXISTS', 'forbidden:devid:' + str(deviceId)):
                TyContext.ftlog.info('_check_userid_forbidden forbiddendevice:'
                                     ' deviceId', deviceId, 'userId', userId)
                raise Exception("forbidden deviceid")

            if appId and AccountHelper.check_user_forbidden_chip(userId, appId):
                TyContext.ftlog.info('_check_userid_forbidden forbidden chip:'
                                     ' appId', appId, 'userId', userId)
                raise Exception("forbidden too much chip")

        except Exception as e:
            info = TyContext.Configure.get_global_item_str('user_forbidden_info')
            info = info.format(userId=userId)
            tips = TyContext.Configure.get_global_item_str('user_forbidden_tips')
            return True, (info + tips).encode('utf8'), \
                   {'info': info.encode('utf8'), 'tips': tips.encode('utf8')}

        return False, None, None

    '''
    devidmap 最老版，值为uid的列表
    newdevidmap 第二版，值为uid
    devidmap3 第三版 值为uid
    '''

    @classmethod
    def __find_userid_by_devid_map_v2__(cls, deviceId):
        if deviceId == '528c8e6cd4a3c6598999a0e9df15ad32':
            return 0
        uid = TyContext.RedisUserKeys.execute('GET', 'newdevidmap:' + str(deviceId))
        if not uid or uid <= 0:
            return 0
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('__find_userid_by_devid_map_v2__ failed get cold data')
            return 0

    @classmethod
    def __find_userid_by_devid_map_v3__(cls, deviceId):
        if deviceId == '528c8e6cd4a3c6598999a0e9df15ad32':
            return 0
        uid = TyContext.RedisUserKeys.execute('GET', 'devidmap3:' + str(deviceId))
        if not uid or uid <= 0:
            return 0
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('__find_userid_by_devid_map_v3__ failed get cold data')
            return 0

    @classmethod
    def __find_userid_by_mobile__(cls, userMobile, rparams=None):
        uid = TyContext.RedisUserKeys.execute('GET', 'mobilemap:' + str(userMobile))
        if not uid or uid <= 0:
            return 0
        return cls.__find_userid_by_tyid__(uid, rparams=rparams)
        # try:
        #     TyContext.MySqlSwap.checkUserDate(uid)
        #     AccountHelper.restore_avatar_verify_set(uid)
        #     return uid
        # except:
        #     TyContext.ftlog.error('__find_userid_by_mobile__ failed get cold data')
        #     return 0

    @classmethod
    def __find_userid_by_account__(cls, account, rparams=None):
        uid = TyContext.RedisUserKeys.execute('GET', 'accountmap:' + str(account))
        if not uid or uid <= 0:
            return 0
        return cls.__find_userid_by_tyid__(uid, rparams=rparams)
        # try:
        #     TyContext.MySqlSwap.checkUserDate(uid)
        #     AccountHelper.restore_avatar_verify_set(uid)
        #     return uid
        # except:
        #     TyContext.ftlog.error('__find_userid_by_account__ failed get cold data')
        #     return 0

    @classmethod
    def __find_userid_by_mail__(cls, email, rparams=None):
        uid = TyContext.RedisUserKeys.execute('GET', 'mailmap:' + str(email))
        if not uid or uid <= 0:
            return 0
        return cls.__find_userid_by_tyid__(uid, rparams=rparams)
        # try:
        #     TyContext.MySqlSwap.checkUserDate(uid)
        #     AccountHelper.restore_avatar_verify_set(uid)
        #     return uid
        # except:
        #     TyContext.ftlog.error('__find_userid_by_mail__ failed get cold data')
        #     return 0

    @classmethod
    def __check_forbid_device(cls, userId, forbid_data, rparams):
        # forbid_device_data = TyContext.Configure.get_global_item_json("forbid_device_data", {})
        forbid_userList = forbid_data.get('userList', [])
        forbid_iccid = forbid_data.get('iccid', [])
        forbid_imsi = forbid_data.get('imsi', [])
        forbid_androidId = forbid_data.get('androidId', [])
        forbid_idfa = forbid_data.get('idfa', [])
        forbid_devId = forbid_data.get('deviceId', [])
        # TyContext.ftlog.warn("checkForbidDevice forbid_iccid=", forbid_iccid,
        #                      'forbid_imsi=', forbid_imsi,
        #                      'forbid_androidId=', forbid_androidId,
        #                      'forbid_idfa=', forbid_idfa,
        #                      'params=', rparams)
        return int(userId) in forbid_userList or \
               rparams.get('iccid', '!') in forbid_iccid or \
               rparams.get('imsi', '@') in forbid_imsi or \
               rparams.get('androidId', '#') in forbid_androidId or \
               rparams.get('idfa', '$') in forbid_idfa or \
               rparams.get('deviceId', '%') in forbid_devId

    @classmethod
    def __find_userid_by_tyid__(cls, tuyooId, rparams=None):
        if tuyooId and tuyooId > 0:
            if rparams:
                # 黑名单
                forbid_data = TyContext.Configure.get_global_item_json("forbid_device_info", {})
                if cls.__check_forbid_device(tuyooId, forbid_data, rparams):
                    TyContext.ftlog.error("AccountLogin->checkLoginDevice failed userId=", tuyooId, 'rparams=', rparams,
                                          'forbid_data=', forbid_data)
                    return 0
                # 白名单
                forbid_data = TyContext.Configure.get_global_item_json("forbid_device_whitelist", {})
                if cls.__check_forbid_device(tuyooId, forbid_data, rparams):
                    rparams = None
            if not TyContext.MySqlSwap.checkUserDate(tuyooId, rparams=rparams):
                return 0
            AccountHelper.restore_avatar_verify_set(tuyooId)
            if False and rparams:
                chip, _mdevid, _sessionDevId, _sessionIccid, _sessionIdfa, _uuid, _mac = \
                    TyContext.RedisUser.execute(tuyooId, 'HMGET', 'user:' + str(tuyooId),
                                                'chip', 'mdevid', 'sessionDevId', 'sessionIccid', 'sessionIdfa', 'uuid',
                                                'mac')
                if chip and chip >= 10000000:
                    result = []
                    deviceId = rparams.get('deviceId', '')
                    iccid = rparams.get('iccid')
                    idfa = rparams.get('idfa')
                    uuid = rparams.get('uuid')
                    mac = rparams.get('mac')
                    result.append(deviceId and deviceId == _mdevid)
                    result.append(deviceId and deviceId == _sessionDevId)
                    result.append(iccid and iccid == str(_sessionIccid))
                    result.append(idfa and idfa == _sessionIdfa)
                    result.append(uuid and uuid == _uuid)
                    result.append(mac and mac == _mac)
                    if not reduce(lambda x, y: x or y, result):
                        TyContext.ftlog.error("AccountLogin->checkLoginDevice failed userId=", tuyooId, 'rparams=',
                                              rparams,
                                              '_mdevid=', _mdevid,
                                              '_sessionDevId=', _sessionDevId,
                                              '_sessionIccid=', _sessionIccid,
                                              '_sessionIdfa=', _sessionIdfa,
                                              '_uuid=', _uuid,
                                              '_mac=', _mac)
                        return 0
            return tuyooId
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
    def __check_user_passwd__(cls, userId, passWord):
        dbPassword, userSignature = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'password',
                                                                'userSignature')
        # 补救password没设置值的bug
        # if (dbPassword == None or dbPassword == '') and passWord != None and len(passWord) > 0:
        #     TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'password', passWord)
        #     dbPassword = passWord
        #             TyContext.ftlog.info('__check_user_passwd__ dbPassword is empty', 'userId=', userId, 'dbPassword=', passWord)

        try:
            if str(dbPassword) == str(passWord):
                ### alert here
                if userSignature and AccountVerify.md5(passWord) != userSignature:
                    TyContext.ftlog.warn("AccountLogin->checkUserSignature failed", userId, passWord, userSignature)
                return True

            if str(dbPassword) == AccountVerify.md5(passWord):
                return True
            ### check userSignature
            if userSignature and str(userSignature) == AccountVerify.md5(passWord):
                return True
        except:
            TyContext.ftlog.info('__check_user_passwd__ error: userId', userId, 'failed password', passWord,
                                 'db password', dbPassword)
            return False

        #         TyContext.ftlog.info('doLoginByTyId->password incorrect', 'userId=', userId, 'dbPassword=', dbPassword, 'passWord=', passWord)
        return False

    @classmethod
    def __newaccount_success_callback_(cls, appid, newstr, data):
        TyContext.ftlog.debug('AccountLogin->__newaccount_success_callback_ begin', appid, newstr, data)
        conf = TyContext.Configure.get_global_item_json(newstr + '.reward.callback', {})
        if conf and str(appid) in conf:
            url = conf[str(appid)]
            response, requestUrl = TyContext.WebPage.webget(url, data)
            TyContext.ftlog.debug('AccountLogin->__newaccount_success_callback_ success', response)


            # 360SDKv1.0.4版本
