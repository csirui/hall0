import random

from tyframework.context import TyContext
from tysdk.entity.sns4.decorator.snsv4_login import snsv4_login_map
from tysdk.entity.user3.account_info import AccountInfo
from tysdk.entity.user3.account_login import AccountLogin
from tysdk.entity.user4.account_model import AccountModel
from tysdk.entity.user_common.constants import AccountConst
from tysdk.entity.user_common.verify import AccountVerify

__author__ = 'tuyou'


class AccountSnsV4(object):
    @classmethod
    def doSnsLogin(cls, rpath):
        # todo 验签
        mo = TyContext.Cls_MsgPack()
        rparams = TyContext.RunHttp.convertArgsToDict()
        rparams['snsId'] = AccountVerify.decode_item(rparams['snsId'])
        snsId = rparams.get('snsId')
        prefix = snsId.split(':')[0]
        isOk = None
        try:
            method = snsv4_login_map.get(prefix)
            if not method:
                isOk = True
            else:
                isOk = method(rparams, snsId)
        except:
            isOk = False
        if not isOk:
            mo.setResult('info', '三方登陆失败')
            mo.setResult('code', 1)
            return mo
        userId = AccountLogin.__find_userid_by_snsid__(snsId)
        is_create = False
        if userId <= 0:
            # 效验该deviceId是否存在第三方sns刷号嫌疑
            isFlag, retMsg = AccountLogin._check_deviceid_sns_forbidden(rparams)
            if isFlag:
                mo.setResult('code', AccountConst.CODE_USER_SNS_REG_FAILE)
                mo.setResult('info', retMsg)
                return mo
            rparams['passwd'] = 'ty' + str(random.randint(100000, 999999))
            if snsId.startswith('360'):
                rparams['lang'] = "zh_hans"
            is_create = True
            userId = AccountInfo.createNewUser(rparams, AccountConst.USER_TYPE_SNS, False)
            if userId <= 0:
                mo.setResult('code', AccountConst.CODE_USER_GUEST_REG_FAILE)
                mo.setResult('info', '用户账号建立失败')
                return mo
            appId = rparams['appId']
        else:
            rparams['userId'] = userId
            try:
                del rparams['name']
            except:
                pass
            AccountInfo.doSetUserInfo(rparams, mo, False)
        AccountLogin._do_check_login(rparams, userId, mo, AccountConst.USER_TYPE_SNS, is_create)
        # add to userBindSet
        snsId = rparams.get('snsId')
        AccountModel.add_snsid_to_userbind_set(userId, snsId)
        retMsg = TyContext.Cls_MsgPack()
        if mo.getErrorInfo():
            retMsg.setResult('info', mo.getErrorInfo())
            retMsg.setResult('code', mo.getErrorCode())
            return retMsg
        token = AccountModel.reset_user_token(userId, 'sns')
        retMsg.setResult('token', token)
        retMsg.setResult('code', 0)
        return retMsg

    @classmethod
    def doUserBind(cls, mo, rpath):
        if not AccountVerify.sing_verify(rpath) and False:
            mo.setResult('info', '验签失败')
            mo.setResult('code', -1)
            return
        rparams = TyContext.RunHttp.convertArgsToDict()
        snsId = rparams.get('snsId')
        snsId = AccountVerify.decode_item(snsId)
        prefix = snsId.split(':')[0]
        isOk = None
        try:
            method = snsv4_login_map.get(prefix)
            if not method:
                isOk = True
            else:
                isOk = method(rparams, snsId)
        except:
            isOk = False
        if not isOk:
            mo.setResult('info', '账号验证失败')
            mo.setResult('code', 1)
            return
        uid = AccountModel.get_uid_by_snsid(snsId)
        if uid and int(uid) > 0:
            mo.setResult('info', '用户已经绑定过其他途游账号了')
            mo.setResult('code', 3)
            return
        uid = rparams.get('userId')
        snsId = rparams.get('snsId')
        AccountModel.set_snsid_for_userid(uid, snsId)
        AccountModel.add_snsid_to_userbind_set(uid, snsId)
        AccountModel.set_user_info(uid, snsId=snsId)
        mo.setResult('info', '绑定成功')
        mo.setResult('code', 0)

    @classmethod
    def unbindSnsId(cls, mo, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        loginName = rparams.get('loginName')
        if loginName:
            uid = AccountModel.get_uid_by_login_name(loginName)
        else:
            uid = rparams.get('userId')
        dataIn = AccountModel.get_user_info(uid, 'snsId')
        snsId = dataIn.get('snsId')
        uid = AccountModel.get_uid_by_snsid(snsId)
        if uid and uid > 0:
            AccountModel.unbind_snsid_for_user(uid, snsId)
            mo.setResult('info', 'userId->%s解绑成功' % uid)
            return
