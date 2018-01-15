# -*- coding=utf-8 -*-

# Author:        zhaoqinghui@hoolai.com
# Company:       Hoolai.Inc
# Created:       2013年01月25日 星期六 00时34分53秒
# FileName:      account.py
# Class:         Account

from tyframework.context import TyContext


class AccountHelper():
    @classmethod
    def restore_avatar_verify_set(cls, userId):
        purl, purlVerify = TyContext.RedisUser.execute(
            userId, 'HMGET', 'user:' + str(userId), 'purl', 'purl_verifying')
        if not purlVerify or not purl or 'head_verifying.png' not in purl:
            return
        from tysdk.entity.beautycertify3.avatarverify import AvatarVerifyService
        AvatarVerifyService.create(userId)

    @classmethod
    def append_ios_idfa_flg(cls, userId, appId, clientId, mo):
        ids = TyContext.Configure.get_game_item_json(appId, 'ios.idfa.show.clientids', ['IOS_2.82_happy'])
        if TyContext.strutil.reg_matchlist(ids, clientId):
            mo.setResult('showAd', 1)

    @classmethod
    def check_user_forbidden_chip(cls, userId, gameId):
        return False
