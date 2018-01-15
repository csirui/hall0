# -*- coding=utf-8 -*-
import json

import datetime

from tyframework.context import TyContext
from tysdk.entity.cross.cross import Cross
from tysdk.entity.friend3.friend import Friend
from tysdk.entity.user3.account_check import AccountCheck
from tysdk.entity.user3.account_check import AccountVerify

'''
  好友

  系统与用户校验错误： {cmd:” xx”, error: { code: 1, info: "xxx"  } }

  好友内部错误： {cmd:” xx”, result: { code: 1, info: "xxx"  } }
     参数问题：code : 1 ~ 100
     逻辑错误：code > 100
'''


class HttpFriendV3(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v3/friend/addContactFriendInvite': cls.addContactFriendInvite,
                '/open/v3/friend/getNeighborsForInvite': cls.getNeighborsForInvite,
                '/open/v3/friend/getContactsForInvite': cls.getContactsForInvite,
                '/open/v3/friend/getFriends': cls.getFriends,
                '/open/v3/friend/delFriend': cls.delFriend,
                '/open/v3/friend/confirmFriendRequest': cls.confirmFriendRequest,
                '/open/v3/friend/getFriendRequestList': cls.getFriendRequests,
                '/open/v3/friend/addFriend': cls.addFriendRequest,
                '/open/v3/friend/sendGift': cls.sendGift,
                '/open/v3/friend/mergeSnsFriends': cls.mergeSnsFriends,

                '/open/v3/user/setScore': cls.setScore,
                '/open/v3/user/getRank': cls.getRankList,

                '/open/v3/cross/getAppList': cls.getAppList,
                '/open/v3/cross/downapp': cls.downapp,
                # '/open/v3/cross/reward': cls.crossReward,
            }
            AccountCheck.__init_checker__()
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                # '/open/vc/user/smsCallback': cls.doSmsBindCallBack,
            }
            AccountCheck.__init_checker__()
        return cls.HTMLPATHS

    @classmethod
    def checkAccount(cls, rpath):
        # return AccountCheck.normal_check(rpath, False)
        return AccountCheck.normal_check(rpath)

    @classmethod
    def addContactFriendInvite(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('addContactFriendInvite')
        friend_phone = TyContext.RunHttp.getRequestParam('friend_phone')
        if friend_phone is None or len(friend_phone) != 11:
            mo.setResult('code', 2)
            mo.setResult('info', "phone number error")
        else:
            Friend.addContactFriendInvite(params['appId'], params['userId'], friend_phone, mo)
        return mo

    @classmethod
    def getContactsForInvite(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getContactsForInvite')
        contacts = TyContext.RunHttp.getRequestParam('contacts')
        if contacts is None or contacts == '':
            mo.setResult('code', 0)
            mo.setResult('data', [])
            return mo
        try:
            contactsList = json.loads(contacts)
        except:
            contacts = AccountVerify.decode_item(contacts)
            contactsList = json.loads(contacts)
        TyContext.ftlog.debug('getContactsForInvite.contacts', contacts)
        Friend.getContactsForInvite(params['appId'], params['userId'], params['clientId'], contactsList, mo)
        return mo

    @classmethod
    def getNeighborsForInvite(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getNeighborsForInvite')
        Friend.getNeighborsForInvite(params['appId'], params['userId'], mo)
        return mo

    @classmethod
    def delFriend(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('delFriend')
        friend_uid = TyContext.RunHttp.getRequestParam('friend_uid')
        if friend_uid is None or friend_uid == '':
            mo.setResult('code', 2)
            mo.setResult('info', u"好友ID为空！")
        else:
            Friend.delFriend(params['appId'], params['userId'], friend_uid, mo)
        return mo

    @classmethod
    def addFriendRequest(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('addFriend')
        friend_uid = TyContext.RunHttp.getRequestParamInt('friend_uid')
        if friend_uid <= 0:
            mo.setResult('code', 2)
            mo.setResult('info', u"好友ID为空！")
        else:
            Friend.addFriendRequest(params['appId'], params['userId'], friend_uid, mo)
        return mo

    @classmethod
    def confirmFriendRequest(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('confirmFriendRequest')
        friend_uid = TyContext.RunHttp.getRequestParam('friend_uid')
        isAgree = TyContext.RunHttp.getRequestParamInt('is_agree')
        if friend_uid is None or friend_uid == '':
            mo.setResult('code', 2)
            mo.setResult('info', u"好友ID为空！")
        else:
            Friend.confirmFriendRequest(params['appId'], params['userId'], friend_uid, isAgree, mo)
        return mo

    @classmethod
    def getFriendRequests(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getFriendRequestList')
        Friend.getFriendRequests(params['appId'], params['userId'], mo)
        return mo

    @classmethod
    def getFriends(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getFriends')
        Friend.getMyFriends(params['appId'], params['userId'], mo)
        return mo

    @classmethod
    def setScore(cls, rpath):
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        score = TyContext.RunHttp.getRequestParamInt('score', 0)
        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        infos = TyContext.RunHttp.getRequestParam('infos', '')  # user extra infos json string

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('setScore')

        if score == 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'score is zero')
            return mo

        rankName = TyContext.RunHttp.getRequestParam('rank_name', 'week_score')
        key = 'rank_scores:' + str(appId) + ":" + str(rankName) + ':' + str(userId)

        ret = TyContext.RedisUser.execute(userId, 'hmset', key, 'score', str(score), 'infos', infos)
        if ret:
            td = datetime.datetime.today()
            seconds = (7 - td.weekday()) * 86400 - td.hour * 3600 - td.minute * 60 - td.second
            TyContext.RedisUser.execute(userId, 'EXPIRE', key, seconds)
            mo.setResult('code', 0)
            mo.setResult('info', 'success')
        else:
            mo.setResult('code', 1)
            mo.setResult('info', 'fail')
        # TyContext.ftlog.info(cls.__name__, 'mo->', mo.packJson())
        return mo

    @classmethod
    # 周榜
    def getRankList(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        userId = str(params['userId'])
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getRank')

        rank_type = TyContext.RunHttp.getRequestParam('rank_type')
        if rank_type is None:
            mo.setResult('code', 1)
            mo.setResult('info', 'require rank_type')
            return mo
        else:
            rank_type = rank_type.lower()

        friends = []
        rank_name = TyContext.RunHttp.getRequestParam('rank_name', 'week_score')
        top_count = TyContext.RunHttp.getRequestParamInt('top_count', 0)
        if top_count == 0:
            if rank_type != 'friend':
                top_count = 50
        data = {}
        self_user = {}
        rank_users = []
        rank_title = u'排行榜'
        rank_item_prefix = ''
        rank_item_suffix = ''
        if rank_type == 'friend':
            appId = str(params['appId'])
            rank_titles = TyContext.Configure.get_global_item_json('friend.rank.title')
            rank_item_prefix = ''
            rank_item_suffix = ''
            rank_title = u'好友排行榜'
            try:
                rank_title_json = rank_titles[appId][rank_name]
                rank_item_prefix = rank_title_json['item_prefix']
                rank_item_suffix = rank_title_json['item_suffix']
                rank_title = rank_title_json['title']
            except Exception, e:
                pass

            # if rank_titles and rank_titles.has_key(appId):
            #     rank_title_list = rank_titles[appId]
            friends = Friend.getMyFriends(appId, params['userId'], None, True)
            # TyContext.ftlog.debug('users:', friends)
            if friends and len(friends) > 0:
                for user in friends:
                    fuid = str(user['uid'])
                    key = 'rank_scores:' + str(appId) + ":" + rank_name + ':' + str(fuid)
                    score = TyContext.RedisUser.execute(fuid, 'hmget', key, 'score', 'infos')
                    TyContext.ftlog.debug('score', score)
                    if fuid != userId and (score is None or score[0] is None):  # 必须玩过游戏
                        continue
                    if not score or not score[0]:
                        score = [0, '']
                    user['score'] = int(score[0])
                    if not score[1]: score[1] = ''
                    user['infos'] = score[1]
                    rank_users.append(user)
                    if fuid == userId:
                        self_user = user
                # TyContext.ftlog.debug('rank_users:', rank_users)
                rank_users.sort(key=lambda obj: obj.get('score'), reverse=True)
                for i in xrange(len(rank_users)):
                    user = rank_users[i]
                    user['rank'] = i + 1
            if top_count != 0 and len(rank_users) > top_count:
                rank_users = rank_users[:top_count]
            data['all'] = rank_users
            data['self'] = self_user
            data['title'] = rank_title
            data['item_prefix'] = rank_item_prefix
            data['item_suffix'] = rank_item_suffix
        mo.setResult('code', 0)
        mo.setResult('data', data)
        return mo

    @classmethod
    def sendGift(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        userId = str(params['userId'])
        mo = TyContext.Cls_MsgPack()

        giftId = TyContext.RunHttp.getRequestParam('gift_id', -1)
        friend_uid = TyContext.RunHttp.getRequestParam('friend_uid', 0)
        if giftId == -1 or friend_uid == 0:
            mo.setResult('code', 10)
            mo.setResult('info', u'缺少参数')
            return mo
        # 检查是否好友
        pass
        Friend.sendGift(params['appId'], userId, friend_uid, giftId, params['clientId'], mo)
        return mo

    @classmethod
    def getAppList(cls, rpath):
        # isReturn, params = cls.checkAccount(rpath)
        # if isReturn:
        #     return params
        # clientId = params['clientId']
        # appId = params['appId']
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getAppList')
        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        if appId == 0:
            mo.setResult('code', 1)
            mo.setResult('info', 'no appId')
        mo.setResult('data', Cross.getAppList(appId, clientId))
        mo.setResult('code', 0)
        return mo

    @classmethod
    def mergeSnsFriends(cls, rpath):
        isReturn, params = AccountCheck.normal_check(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        sns_type = TyContext.RunHttp.getRequestParam('sns_type', '')
        sns_friends_param = TyContext.RunHttp.getRequestParam('sns_friends', '')
        if sns_type == '' and sns_friends_param == '':
            mo.setResult('code', 1)
            mo.setResult('info', 'sns_type,sns_friends required')
            return mo
        TyContext.ftlog.info('mergeSnsFriends sns_type=', sns_type, 'appId=', params['appId'],
                             'userId=', params['userId'], 'sns_friends=', sns_friends_param);
        # if sns_friends != '':
        #     sns_friends = AccountVerify.decode_item(contacts)
        sns_friends = json.loads(sns_friends_param)
        Friend.mergeSnsFriends(params['appId'], params['userId'], sns_type, sns_friends, mo)
        mo.setResult('code', 0)
        mo.setResult('info', 'success')
        return mo

    @classmethod
    def downapp(cls, rpath):

        url = TyContext.RunHttp.getRequestParam('url')
        if url:
            TyContext.RunHttp.redirect(url)
        isReturn, params = AccountCheck.normal_check(rpath, False)
        if isReturn:
            return params
        clientId = params['clientId']
        appId = params['appId']
        pkg = TyContext.RunHttp.getRequestParam('pkg')
        down_app_id = TyContext.RunHttp.getRequestParam('down_app_id')
        url = TyContext.RunHttp.getRequestParam('url')

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('downapp')
        if not pkg or not down_app_id or not url:
            mo.setResult('code', 1)
            mo.setResult('info', 'lack parameters')
        else:
            Cross.downapp(appId, down_app_id, clientId, params['userId'], pkg, url)
            mo.setResult('code', 0)
            mo.setResult('url', url)

    @classmethod
    def crossReward(cls, rpath):
        userId = TyContext.RunHttp.getRequestParam('userId')
        appId = TyContext.RunHttp.getRequestParam('appId')
        Cross.reward(userId, appId)
        mo = TyContext.Cls_MsgPack()
        mo.setResult('code', 0)
        return mo
