# -*- coding=utf-8 -*-
import json

import datetime

from tyframework.context import TyContext
from tysdk.entity.cross.cross import Cross
from tysdk.entity.sns.friend import Friend
from tysdk.entity.user3.account_check import AccountCheck
from tysdk.entity.user3.account_check import AccountVerify

'''
  好友

  系统与用户校验错误： {cmd:” xx”, error: { code: 1, info: "xxx"  } }

  好友内部错误： {cmd:” xx”, result: { code: 1, info: "xxx"  } }
     参数问题：code : 1 ~ 100
     逻辑错误：code > 100
'''


class HttpSnsV3(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    FRIEND_RECOMMEND_CNT = 4

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/open/v3/sns/addContactFriendInvite': cls.addContactFriendInvite,
                '/open/v3/sns/getNeighborsForInvite': cls.getNeighborsForInvite,
                '/open/v3/sns/getContactsForInvite': cls.getContactsForInvite,

                '/open/v3/sns/getFriends': cls.getFriends,
                '/open/v3/sns/getFriendsAndRequests': cls.getFriendsAndRequests,

                '/open/v3/sns/delFriend': cls.delFriend,
                '/open/v3/sns/confirmFriendRequest': cls.confirmFriendRequest,
                '/open/v3/sns/getFriendRequestList': cls.getFriendRequests,

                '/open/v3/sns/readyInviteFriend': cls.readyInviteFriend,
                '/open/v3/sns/addFriend': cls.addFriendRequest,
                '/open/v3/sns/getFriendGuide': cls.getFriendGuide,
                '/open/v3/sns/getFriendTipInfo': cls.getFriendTipInfo,

                # '/open/v3/sns/agreeFriendRequest': cls.confirmFriendRequest,
                # '/open/v3/sns/disagreeFriendRequest': cls.confirmFriendRequest,

                '/open/v3/sns/sendGift': cls.sendGift,
                '/open/v3/sns/mergeSnsFriends': cls.mergeSnsFriends,

                '/open/v3/sns/setScore': cls.setScore,
                '/open/v3/sns/getFriendsRank': cls.getFriendsRank,
                '/open/v3/sns/blockFriendRequest': cls.blockFriendRequest,
                '/open/v3/sns/getRecommendList': cls.getRecommendList,
                '/open/v3/sns/praiseFriend': cls.praiseFriend,
                '/open/v3/sns/searchUser': cls.searchUser,

                '/open/v3/sns/cross/getAppList': cls.getAppList,
                '/open/v3/sns/cross/downapp': cls.downapp,
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
        return AccountCheck.normal_check(rpath, False)
        # return AccountCheck.normal_check(rpath)

    @classmethod
    def onResponse(cls, mo, params):
        tcp_params = TyContext.RunHttp.getRequestParam('tcp_params')
        if not tcp_params:
            return mo

        url = Friend._get_game_server_callback_url(params['appId'], params['clientId'],
                                                   '/v2/game/sdk/sns_callback')
        Friend.http_request(url, {'sdk_result': mo.packJson(), 'tcp_params': tcp_params}, True)
        return mo

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
        return cls.onResponse(mo, params)

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
            return cls.onResponse(mo, params)
        try:
            contactsList = json.loads(contacts)
        except:
            contacts = AccountVerify.decode_item(contacts)
            contactsList = json.loads(contacts)
        TyContext.ftlog.debug('getContactsForInvite.contacts', contacts)
        Friend.getContactsForInvite(params['appId'], params['userId'], params['clientId'], contactsList, mo)
        return cls.onResponse(mo, params)

    @classmethod
    def getNeighborsForInvite(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getNeighborsForInvite')
        Friend.getNeighborsForInvite(params['appId'], params['userId'], mo)
        return cls.onResponse(mo, params)

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
            friend_uids = friend_uid.split(',')
            for fid in friend_uids:
                Friend.delFriend(params['appId'], params['userId'], fid, mo)
        return cls.onResponse(mo, params)

    @classmethod
    def getFriendTipInfo(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        userId = params['userId']
        appId = params['appId']
        mo = TyContext.Cls_MsgPack()
        my_vip, max_praise_num = Friend.getMaxPraiseNumInfo(userId)
        day1st_datas_mine = TyContext.Day1st.get_datas(userId, appId)
        praise_num = day1st_datas_mine.get('praise_num', 0)
        praise_friends = day1st_datas_mine.get('praise_friends', [])

        if praise_num >= max_praise_num:
            is_show_rank_dot = 0
        else:
            is_show_rank_dot = 0
            friendIds = Friend.getMyFriendIds(userId, appId)
            if friendIds and len(friendIds) > 0:
                friendIds = [str(a) for a in friendIds]
                friends_info = Friend.get_users_winchip(friendIds)
                friends_info_map = {}
                if friends_info:
                    for info in friends_info:
                        if not info or 'uid' not in info:
                            continue
                        friends_info_map[str(info['uid'])] = info.get('winchip', 0)
                for fid in friendIds:
                    if fid not in praise_friends and Friend.canPraiseFriend(userId, fid, friends_info_map):
                        is_show_rank_dot = 1
                        break
        mo.setResult('can_praise_friend', is_show_rank_dot)
        requestCount = Friend.getFriendRequestsCount(appId, userId)

        mo.setResult('friend_request_num', requestCount)
        return cls.onResponse(mo, params)

    @classmethod
    def getFriendGuide(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getFriendGuide')
        guide = TyContext.Configure.get_global_item_str('sns.friend.guide')
        mo.setResult('content', guide)
        cls.onResponse(mo, params)

    @classmethod
    def readyInviteFriend(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        invite_type = TyContext.RunHttp.getRequestParam('invite_type')
        productName = TyContext.RunHttp.getRequestParam('productName')
        uid = params['userId']
        gameId = params['appId']  # todo
        subGameId = TyContext.RunHttp.getRequestParamInt('subGameId', 6)

        gameName, url = Friend.getGameNameAndUrl(subGameId, params['clientId'])
        if not productName:
            productName = gameName

        normal_user = 1
        if invite_type == 'sms':
            msg = "我在玩 " + productName + "，等你哦，不见不散！点此下载:" + url
            normal_user = cls._checkNormalAccount(uid)
        else:
            msg = "我在玩 " + productName + "，等你哦，不见不散！我的id是" + str(uid) + ", " \
                                                                        "在游戏中添加我为好友，一起玩吧～ 点击下载"
        code = 0
        if normal_user == 0:
            code = 1
        mo.setResult('code', code)
        mo.setResult('url', url)
        mo.setResult('content', msg)
        mo.setResult('info', "ok")
        return cls.onResponse(mo, params)

    @classmethod
    def _checkNormalAccount(cls, uid, send_task=True):
        userEmail, userSnsId, bindMobile = \
            TyContext.RedisUser.execute(uid, 'HMGET', 'user:' + str(uid), 'email', 'snsId', 'bindMobile')

        normal_user = 0
        # if bindMobile != None and len(str(bindMobile)) == 11 \
        #         or userEmail != None and len(userEmail) > 0 \
        #         or userSnsId != None and len(str(userSnsId)) > 0:
        if bindMobile != None and len(str(bindMobile)) == 11:
            normal_user = 1
        return normal_user

    @classmethod
    def addFriendRequest(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('addFriend')
        friend_uid = TyContext.RunHttp.getRequestParam('friend_uid')

        if friend_uid is None or friend_uid == '':
            mo.setResult('code', 2)
            mo.setResult('info', u"好友ID为空！")
            return cls.onResponse(mo, params)

        uid = params['userId']
        normal_user = cls._checkNormalAccount(uid)
        if normal_user == 0:
            mo.setResult('code', 109)
            mo.setResult('info', Friend.err_codes[109])
            # return mo   todo

        friend_uids = friend_uid.split(',')
        TyContext.ftlog.debug('friend_uids', friend_uids)

        if len(friend_uids) == 1:
            Friend.addFriendRequest(params['appId'], params['clientId'], params['userId'], friend_uid, mo)
        else:
            for fid in friend_uids:
                Friend.addFriendRequest(params['appId'], params['clientId'], params['userId'], fid, None)

            TyContext.ftlog.debug('friend_uids....')
            mo.setResult('code', 0)
            mo.setResult('info', u"好友请求发送成功！")
        return cls.onResponse(mo, params)

    @classmethod
    def confirmFriendRequest(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('confirmFriendRequest')
        friend_uid = TyContext.RunHttp.getRequestParam('friend_uid')
        isAgree = TyContext.RunHttp.getRequestParamInt('is_agree', 0)
        if friend_uid is None or friend_uid == '':
            mo.setResult('code', 2)
            mo.setResult('info', u"好友ID为空！")
            return cls.onResponse(mo, params)

        friend_uids = friend_uid.split(',')
        if len(friend_uids) == 1:
            Friend.confirmFriendRequest(params['appId'], params['userId'], friend_uid, isAgree, mo)
            return cls.onResponse(mo, params)

        for friend_uid in friend_uids:
            ret = Friend.confirmFriendRequest(params['appId'], params['userId'], friend_uid, isAgree, mo)
            if not ret:
                break

        mo.setResult('code', 0)
        mo.setResult('info', "ok")
        return cls.onResponse(mo, params)

    @classmethod
    def getFriendRequests(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getFriendRequestList')
        Friend.getFriendRequests(params['appId'], params['userId'], mo)
        return cls.onResponse(mo, params)

    @classmethod
    def getFriendsAndRequests(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getFriendsAndRequests')
        appId = str(params['appId'])
        userId = str(params['userId'])
        friends = Friend.getMyFriends(appId, userId)
        friend_requests = Friend.getFriendRequests(appId, userId, None, 20)
        for request in friend_requests:
            request['is_request'] = 1
            request['user_status'] = '请求加你为好友'
        friend_requests.extend(friends)
        # mo.setResult('friend_requests', friend_requests)
        mo.setResult('friend_list', friend_requests)

        is_block_request = Friend.get_request_block_state(appId, userId)
        mo.setResult('is_block_request', is_block_request)

        return cls.onResponse(mo, params)

    @classmethod
    def getFriends(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getFriends')
        Friend.getMyFriends(params['appId'], params['userId'], mo)
        return cls.onResponse(mo, params)

    @classmethod
    def praiseFriend(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        friend_uid = TyContext.RunHttp.getRequestParam('friend_uid')

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('praiseFriend')
        # mo.setResult('code', 0)
        # mo.setResult('info', '点赞成功')
        Friend.praise(params['appId'], params['userId'], friend_uid, mo)
        mo.setResult('friend_charm', 100)
        return cls.onResponse(mo, params)

    @classmethod
    def blockFriendRequest(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('blockFriendRequest')

        # friend_uid = TyContext.RunHttp.getRequestParam('friend_uid')
        is_block = TyContext.RunHttp.getRequestParamInt('is_block', -1)
        if is_block < 0:
            mo.setResult('code', 1)
            mo.setResult('info', '缺少参数')
            return mo
        Friend.set_block_friend_request(params['appId'], params['userId'], is_block)
        mo.setResult('code', 0)
        mo.setResult('info', 'ok')
        return cls.onResponse(mo, params)

    @classmethod
    def getRecommendList(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getRecommendList')

        uid = params['userId']
        friends = Friend.getMyFriendIds(uid, params['appId'])
        TyContext.ftlog.debug('getRecommendList friends', friends)

        if not friends:
            friends = [uid]
        friend_uids = ','.join([str(c) for c in friends])

        url = Friend._get_game_server_callback_url(params['appId'], params['clientId'],
                                                   '/v2/game/sdk/getRecommendFriends')
        result = Friend.http_request(url,
                                     {'count': cls.FRIEND_RECOMMEND_CNT, 'friend_uids': friend_uids, 'userId': uid})
        try:
            import json
            uids = json.loads(result)
        except:
            uids = set()
            pass

        datadict = {'male': [], 'female': []}
        for uid in uids:
            user = Friend.getUserInfo(params['appId'], uid)
            if not user:
                continue
            sex_field = 'male' if user['sex'] == 0 else 'female'
            datadict[sex_field].append(user)
        datalist = []
        if datadict['male']:  # 至少一个男的
            datalist.append(datadict['male'].pop())
        datalist.extend(datadict['female'])  # 然后优先女的
        datalist.extend(datadict['male'])
        datalist = datalist[:cls.FRIEND_RECOMMEND_CNT]
        Friend.setup_friends_game_info(datalist, 0, 0, 1)

        mo.setResult('code', 0)
        mo.setResult('info', 'ok')
        mo.setResult('recommend_list', datalist)
        return cls.onResponse(mo, params)

    @classmethod
    def searchUser(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('searchUser')

        search_uid = TyContext.RunHttp.getRequestParam('search_uid')
        if search_uid is None or search_uid == '' or not str(search_uid).isdigit():
            mo.setResult('code', 2)
            mo.setResult('info', '请输入正确ID')
            return cls.onResponse(mo, params)

        search_list = []
        user = Friend.getUserInfo(params['appId'], search_uid)
        if not user is None:
            search_list.append(user)
            Friend.setup_friends_game_info(search_list)

        # for user in search_list:
        #     user['level'] = 1
        #     user['level_game'] = '麻将'

        if len(search_list) == 0:
            mo.setResult('code', 2)
            mo.setResult('info', '请输入正确ID')
        else:
            mo.setResult('code', 0)
            mo.setResult('info', 'ok')
        mo.setResult('search_list', search_list)
        return cls.onResponse(mo, params)

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
    def getFriendsRank(cls, rpath):
        isReturn, params = cls.checkAccount(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('getFriendsRank')
        page = params.get('page', 1)
        Friend.get_friend_rank(params['appId'], params['userId'], mo, page)
        return cls.onResponse(mo, params)

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
            cls.onResponse(mo, params)
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
        cls.onResponse(mo, params)

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
            return cls.onResponse(mo, params)
        # 检查是否好友
        pass
        Friend.sendGift(params['appId'], userId, friend_uid, giftId, params['clientId'], mo)
        return cls.onResponse(mo, params)

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
