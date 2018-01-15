# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class AccountConst():
    CODE_USER_WRONG_STATE = -3  # 错误状态
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
    CODE_USER_SNS_BINDED = 11  # SNS ID已绑定
    CODE_USER_MOBILE_REG_FAILE = 12  # 手机注册失败
    CODE_USER_AUTHORCODE_RENEW_FAIL = 13  # 刷新authorcode失败
    CODE_USER_NOT_FOUND = 14  # 找不到用户
    CODE_USER_SNS_GETINFO_ERROR = 15  # 取三方SNS信息失败
    CODE_USER_NEW_UID_ERROR = 16  # 获取新uid失败
    CODE_USER_INVALID_TOKEN = 17  # 无效Token
    CODE_USER_MOBILE_INVALID = 18  # 用户未绑定手机号
    CODE_USER_MUST_CHANGE_PASSWORD = 19  # 用户必须修改密码才能登录

    USER_TYPE_DEVICE = 0  # 设备注册用户,试玩用户
    USER_TYPE_REGISTER = 1  # 正式注册用户,mail注册用户
    USER_TYPE_MAIL = 1  # 正式注册用户,邮件注册用户
    USER_TYPE_SNS = 2  # SNS用户,sns id注册用户
    USER_TYPE_MOBILE = 3  # 正式注册用户,手机注册用户

    MOBILE_BIND_PENDING = 0  # 手机绑定订单，进行中
    MOBILE_BIND_SUCCESS = 1  # 手机绑定订单，成功
    MOBILE_BIND_OCCUPIED = 2  # 手机绑定订单，被占用
    MOBILE_BIND_BOUND = 3  # 手机绑定订单，重复绑定
    MOBILE_BIND_FAILED = 4  # 手机绑定订单，失败

    MAC_00 = '00:00:00:00:00:00'
    MAC_02 = '02:00:00:00:00:00'
    MAC_00_MD5_LOWER = '528c8e6cd4a3c6598999a0e9df15ad32'
    MAC_00_MD5_UPPER = '528C8E6CD4A3C6598999A0E9DF15AD32'
    MAC_02_MD5_LOWER = '0f607264fc6318a92b9e13c65db7cd3c'
    MAC_02_MD5_UPPER = '0F607264FC6318A92B9E13C65DB7CD3C'

    LOGIN_SUCC_EVENTIDS = [
        TyContext.BIEventId.SDK_LOGIN_BY_DEVID_SUCC,
        TyContext.BIEventId.SDK_LOGIN_BY_MAIL_SUCC,
        TyContext.BIEventId.SDK_LOGIN_BY_SNSID_SUCC,
        TyContext.BIEventId.SDK_LOGIN_BY_MOBILE_SUCC,
    ]

    LOGIN_FAIL_EVENTIDS = [
        TyContext.BIEventId.SDK_LOGIN_BY_DEVID_FAIL,
        TyContext.BIEventId.SDK_LOGIN_BY_MAIL_FAIL,
        TyContext.BIEventId.SDK_LOGIN_BY_SNSID_FAIL,
        TyContext.BIEventId.SDK_LOGIN_BY_MOBILE_FAIL,
    ]

    CREATE_SUCC_EVENTIDS = [
        TyContext.BIEventId.SDK_CREATE_BY_DEVID_SUCC,
        TyContext.BIEventId.SDK_CREATE_BY_MAIL_SUCC,
        TyContext.BIEventId.SDK_CREATE_BY_SNSID_SUCC,
        TyContext.BIEventId.SDK_CREATE_BY_MOBILE_SUCC,
    ]

    CREATE_FAIL_EVENTIDS = [
        TyContext.BIEventId.SDK_CREATE_BY_DEVID_FAIL,
        TyContext.BIEventId.SDK_CREATE_BY_MAIL_FAIL,
        TyContext.BIEventId.SDK_CREATE_BY_SNSID_FAIL,
        TyContext.BIEventId.SDK_CREATE_BY_MOBILE_FAIL,
    ]

    LOGIN_BINDID_KEY = ['fakekey', 'mail', 'snsId', 'mobile']
