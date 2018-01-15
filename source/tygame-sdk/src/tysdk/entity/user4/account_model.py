#! encoding=utf-8
import uuid

from tyframework.context import TyContext
from tysdk.entity.user_common.account_helper import AccountHelper
from tysdk.entity.user_common.constants import AccountConst
from tysdk.entity.user_common.verify import AccountVerify

__author__ = 'yuejianqiang'


class AccountModel(object):
    @classmethod
    def unbind_user_from_externId(cls, userId):
        externId = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%s' % userId, 'bindExternId')
        externId = externId[0]
        if not externId:
            return
        TyContext.RedisUser.execute(userId, 'HDEL', 'user:%s' % userId, 'bindExternId', '')
        TyContext.RedisUserKeys.execute('DEL', 'externIdmap:%s' % externId)

    @classmethod
    def get_user_by_externId(cls, externId):
        # 获取出来userId
        return TyContext.RedisUserKeys.execute('GET', 'externIdmap:%s' % externId)

    @classmethod
    def bind_user_to_externId(cls, externId, userId):
        '''

        :param externId: 外部ID
        :param userId: 要绑定的账号
        :return:
        '''
        bindUser = cls.get_user_by_externId(externId)
        if bindUser == userId:
            return
        TyContext.RedisUser.execute(userId, 'HMSET', 'user:%s' % userId, 'bindExternId', externId)
        TyContext.RedisUserKeys.execute('SET', 'externIdmap:%s' % externId, userId)

    @classmethod
    def is_valid_mobile(cls, mobile):
        return mobile and len(mobile) == 11

    @classmethod
    def checkUserByToken(cls, userId, token):
        return cls.get_user_by_token(token) == userId

    @classmethod
    def get_mobile_bind_user(cls, mobile):
        """
        获取手机号绑定的用户（默认绑定账号)
        :param mobile:
        :return:
        """
        userId = TyContext.RedisUserKeys.execute('GET', 'mobilemap:%s' % mobile)
        return userId

    @classmethod
    def get_mobile_client_bind_user(cls, mobile, clientId):
        userId = TyContext.RedisUserKeys.execute('GET', 'mobileclientmap:%s:%s' % (clientId, mobile))
        return userId

    @classmethod
    def bind_user_to_mobile_client(cls, userId, mobile, clientId):
        TyContext.RedisUserKeys.execute('SET', 'mobileclientmap:%s:%s' % (clientId, mobile), userId)
        TyContext.RedisUserKeys.execute('SADD', 'appleUserList', userId)

    @classmethod
    def is_apple_user(cls, userId):
        return TyContext.RedisUserKeys.execute('SISMEMBER', 'appleUserList', userId)

    @classmethod
    def is_user_bind_mobile(cls, userId, mobile):
        """
        检查用户是否已经绑定过手机号，（v3之前的绑定不算)
        :param userId:
        :param mobile:
        :return:
        """
        userSet = cls.get_mobile_user_set(mobile)
        return userId in userSet

    @classmethod
    def set_mobile_default_user(cls, userId):
        """
        设置用户为手机默认用户
        :param userId:
        :return:
        """
        mobile = cls.get_user_mobile(userId)
        if not mobile:
            return
        TyContext.RedisUserKeys.execute('SET', 'mobilemap:%s' % mobile, userId)

    @classmethod
    def bind_user_to_mobile(cls, user_id, mobile):
        """
        绑定用户到手机号
        :param user_id:
        :param mobile:
        :return:
        """
        # 手机号是否已经绑定了其他账号
        old_user_id = cls.get_mobile_bind_user(mobile)
        if old_user_id and old_user_id != user_id:
            cls.bind_user_to_mobile(old_user_id, mobile)
        # 解除原有的绑定手机号
        old_mobile = cls.get_user_mobile(user_id)
        if str(old_mobile) != str(mobile):
            cls.unbind_user_mobile(user_id, old_mobile)
        TyContext.RedisUser.execute(user_id, 'HMSET', 'user:%d' % user_id, 'bindMobile', mobile, 'isbind',
                                    AccountConst.USER_TYPE_MOBILE)
        TyContext.RedisUserKeys.execute('SET', 'mobilemap:%s' % mobile, user_id)
        TyContext.RedisUserKeys.execute('SADD', 'mobileset:%s' % mobile, user_id)

    @classmethod
    def unbind_user_mobile(cls, user_id, mobile):
        """
        解除用户手机号绑定
        :param user_id:用户Id
        :param mobile: 需要解除绑定的手机号
        :return:
        """
        # 删除用户手机信息
        TyContext.RedisUser.execute(user_id, 'HSET', 'user:' + str(user_id), 'bindMobile', '')
        # 用户从手机绑定账号列表中删除
        TyContext.RedisUserKeys.execute('SREM', 'mobileset:%s' % mobile, user_id)
        # 如果当前用户为此手机号默认用户，则更换默认用户
        if user_id == cls.get_mobile_bind_user(mobile):
            TyContext.RedisUserKeys.execute('SET', 'mobilemap:%s' % mobile, '')
            user_list = cls.get_mobile_user_set(mobile)
            TyContext.ftlog.debug('unbind user->userlist,', user_list, 'mobile', mobile)
            if user_list:
                TyContext.RedisUserKeys.execute('SET', 'mobilemap:%s' % mobile, list(user_list)[0])
            else:
                TyContext.RedisUserKeys.execute('SET', 'mobilemap:%s' % mobile, '')

    @classmethod
    def get_mobile_user_set(cls, mobile):
        """
        获取手机绑定的用户列表
        :param mobile:
        :return:
        """
        result = TyContext.RedisUserKeys.execute('SMEMBERS', 'mobileset:%s' % mobile)
        if not result:
            result = []
        result = set(result)
        user_id = cls.get_mobile_bind_user(mobile)
        if user_id:
            result.add(user_id)
        return result

    @classmethod
    def get_user_mobile(cls, userId):
        """
        获取用户的手机号
        :param userI:
        :return:
        """
        if not userId:
            return None
        bindMobile = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'bindMobile')
        return str(bindMobile)

    @classmethod
    def reset_user_token(cls, user_id, loginType='device', loginMobile=''):
        # 删除老的Token
        token = TyContext.RedisUserKeys.execute('GET', 'user2token:%s' % user_id)
        if token:
            TyContext.RedisUserKeys.execute('DEL', 'token2user:%s' % token)
        # 重新绑定新的Token
        token = str(uuid.uuid4())
        TyContext.RedisUserKeys.execute('SET', 'user2token:%s' % user_id, token)
        TyContext.RedisUserKeys.execute('EXPIRE', 'user2token:%s' % user_id, 90 * 86400)
        TyContext.RedisUserKeys.execute('SET', 'token2user:%s' % token, user_id)
        TyContext.RedisUserKeys.execute('EXPIRE', 'token2user:%s' % token, 90 * 86400)
        # set token
        TyContext.RedisUserKeys.execute('HMSET', 'token_info:%s' % token,
                                        'userId', user_id,
                                        'loginType', loginType,
                                        'loginMobile', loginMobile)
        TyContext.RedisUserKeys.execute('EXPIRE', 'token_info:%s' % token, 90 * 86400)
        return token

    @classmethod
    def set_user_password(cls, userId, password):
        dbPassword, changePwdCount = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'password',
                                                                 'changePwdCount')
        # 更新玩家密码及更改密码次数
        if changePwdCount == None:
            changePwdCount = 0
        changePwdCount = int(changePwdCount) + 1
        TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId),
                                    'password', password,
                                    'userSignature', AccountVerify.md5(password),
                                    'changePwdCount', changePwdCount)

    @classmethod
    def set_mobile_password(cls, mobile, password):
        md5Password = AccountVerify.md5('tuyoo:%s:%s' % (mobile, password))
        TyContext.RedisUserKeys.execute('SET', 'mobilepassword:' + str(mobile), md5Password)

    @classmethod
    def check_mobile_password(cls, mobile, password):
        mobilePassword = TyContext.RedisUserKeys.execute('GET', 'mobilepassword:' + str(mobile))
        if mobilePassword == password:
            return True
        if mobilePassword == AccountVerify.md5('tuyoo:%s:%s' % (mobile, password)):
            return True
        return False

    @classmethod
    def get_user_by_token(cls, token):
        return TyContext.RedisUserKeys.execute('GET', 'token2user:' + str(token))

    @classmethod
    def get_token_info(cls, token):
        userId, loginType, loginMobile = TyContext.RedisUserKeys.execute('HMGET', 'token_info:%s' % token, 'userId',
                                                                         'loginType', 'loginMobile')
        if not userId:
            userId = cls.get_user_by_token(token)
        return userId, loginType, loginMobile

    @classmethod
    def get_user_by_device(cls, deviceId):
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
    def get_user_token(cls, userId):
        """
        获取用户的登陆token
        :param userId:
        :return:
        """
        token = TyContext.RedisUserKeys.execute('GET', 'user2token:%s' % userId)
        if not token:
            token = cls.reset_user_token(userId)
        return token

    @classmethod
    def get_user_brief_info(cls, userId):
        userKeys = ['name', 'chip', 'createTime', 'email', 'bindMobile', 'purl', 'coupon']
        userName, chip, createTime, email, bindMobile, purl, coupon = TyContext.RedisUser.execute(userId, 'HMGET',
                                                                                                  'user:' + str(userId),
                                                                                                  *userKeys)
        return {
            'id': userId,
            'userName': TyContext.KeywordFilter.replace(unicode(userName)),
            'purl': purl,
            'mobile': bindMobile,
            'userEmail': unicode(email),
            'coins': chip,
            'coupon': coupon,
            'token': cls.get_user_token(userId),
        }

    @classmethod
    def get_user_info(cls, userId, *args):
        values = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), *args)
        return dict(zip(args, values))

    @classmethod
    def set_user_info(cls, userId, **args):
        TyContext.RedisUser.execute(userId, 'HMSET', 'user:' + str(userId),
                                    *list(reduce(lambda x, y: x + y, args.items())))

    @classmethod
    def bind_user_by_wxopenId(cls, userId, openId):
        TyContext.RedisUserKeys.execute('SET', 'wxOpenIdmap:%s' % openId, userId)
        TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'wxOpenId', openId)

    @classmethod
    def is_user_bind_with_wxopenId(cls, userId):
        _bindedId = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'wxOpenId')
        if not _bindedId:
            return False
        return True

    @classmethod
    def add_snsid_to_userbind_set(cls, userId, snsId):
        TyContext.RedisUserKeys.execute('SADD', 'snsidset:' + str(userId), snsId)

    @classmethod
    def get_snsidset_for_user(cls, userId):
        return TyContext.RedisUserKeys.execute('SMEMBERS', 'snsidset:' + str(userId))

    @classmethod
    def get_uid_by_snsid(cls, snsId):
        return TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + str(snsId))

    @classmethod
    def set_snsid_for_userid(cls, userId, snsId):
        TyContext.RedisUserKeys.execute('SET', 'snsidmap:' + snsId, userId)

    @classmethod
    def unbind_snsid_for_user(cls, userId, snsId):
        TyContext.RedisUserKeys.execute('DEL', 'snsidmap:' + str(snsId))
        TyContext.RedisUserKeys.execute('SREM', 'snsidset:' + str(userId), snsId)
        TyContext.RedisUser.execute(userId, 'HSET', 'user:' + str(userId), 'snsId', '')
