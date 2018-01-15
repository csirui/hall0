# -*- coding=utf-8 -*-
"""
好友模块
"""
import random
import time

from tyframework.context import TyContext


class Friend(object):
    MAX_FRIEND_COUNT = 500
    MAX_FRIEND_REQUEST_COUNT = 200
    gameid_hall = 0

    _is_set_gift_recv_expire = False

    err_codes = {
        101: u"已经是好友了哦！",
        102: u'好友数量超过限制啦！',
        103: u'今天已经加了太多好朋友，明天再加吧！',
        104: u'对方的好朋友太多了，您现在不能加他为好友了！',

        105: u'该好友您今天已经赠送过一次了哦！',
        106: u'您今天的赠送次数已经用完了哦！',
        107: u'对方今天收到的礼物太多了哦！',
        108: u'对方已经屏蔽好友请求！',

        109: u'加好友需要升级为正式账户哦！',
    }

    praise_limit_conf = {
        0: 10,
        1: 11,
        2: 13,
        3: 16,
        4: 20,
        5: 25,
        6: 30,
        7: 40,
        8: 50
    }

    ERROR_PRAISE_LIMIT_OUT = u'点赞次数超过限制！'
    ERROR_PRAISE_ALREADY = u'已经点过赞了哦'

    @classmethod
    def _isFriends(cls, gameId, userId, friendId):
        rkey = 'friend:' + str(gameId) + ':' + str(userId)
        exist = TyContext.RedisUser.execute(userId, 'SISMEMBER', rkey, friendId)
        return exist

    @classmethod
    def _getMyFriendSize(cls, gameId, userId):
        rkey = 'friend:' + str(gameId) + ':' + str(userId)
        return TyContext.RedisUser.execute(userId, 'SCARD', rkey)

    @classmethod
    def _isFriendsSizeExceed(cls, gameId, userId, mo=None):
        size = cls._getMyFriendSize(gameId, userId)
        if size > cls.MAX_FRIEND_COUNT:
            if mo:
                mo.setResult('code', 102)
                mo.setResult('info', cls.err_codes[102])
            return True
        return False

    @classmethod
    def _isFriendRequestSizeExceed(cls, gameId, userId):
        rkey = 'friend_request:' + str(gameId) + ':' + str(userId)
        num = TyContext.RedisUser.execute(userId, 'ZCARD', rkey)
        return num > cls.MAX_FRIEND_REQUEST_COUNT

    @classmethod
    def addFriend(self, gameId, userId, friendId):
        is_friend = self._isFriends(gameId, userId, friendId)
        if not is_friend:
            self._addFriend(gameId, userId, friendId)

    @classmethod
    def _addFriend(self, gameId, userId, friendId):
        TyContext.RedisUser.execute(userId, 'SADD', 'friend:' + str(gameId) + ':' + str(userId), friendId)
        TyContext.RedisUser.execute(friendId, 'SADD', 'friend:' + str(gameId) + ':' + str(friendId), userId)

    @classmethod
    def _removeFriend(self, gameId, userId, friendId):
        rkey1 = 'friend:' + str(gameId) + ':' + str(userId)
        rkey2 = 'friend:' + str(gameId) + ':' + str(friendId)
        TyContext.RedisUser.execute(userId, 'SREM', rkey1, friendId)
        TyContext.RedisUser.execute(friendId, 'SREM', rkey2, userId)

    @classmethod
    # 请求添加好友
    def addFriendRequest(self, gameId, clientId, uid, friend_uid, mo=None):
        # friendId = mi.getParamInt('friend', 0)
        # mo.setResult('fromUserId', userId)
        # mo.setResult('toUserId', friendId)
        # gameId = 0
        TyContext.ftlog.debug('addFriendRequest', uid, friend_uid, mo)
        if str(friend_uid) == str(uid):
            TyContext.ftlog.debug('addFriendRequest isself')
            if mo:
                mo.setResult('code', 3)
                mo.setResult('info', "不能加自己")
            return False
        uid = str(uid)
        friend_uid = str(friend_uid)

        ret = self._isFriends(gameId, uid, friend_uid)
        TyContext.ftlog.debug('_isFriends ret=' + str(ret))

        if ret:
            if mo:
                mo.setResult('code', 4)
                mo.setResult('info', '你们已经是好友了哦')
            return False

        is_block = self.get_request_block_state(gameId, friend_uid)
        if is_block:
            if mo:
                mo.setResult('info', "对方已经屏蔽了好友请求！")
                mo.setResult('code', 6)
            return False

        is_size_exceed = self._isFriendRequestSizeExceed(gameId, friend_uid)
        if is_size_exceed:
            if mo:
                mo.setResult('info', "对方好友请求太多了哦！")
                mo.setResult('code', 5)
            return False

        rkey = 'friend_request:' + str(gameId) + ':' + str(friend_uid)
        score = TyContext.RedisUser.execute(uid, 'ZSCORE', rkey, uid)

        timestamp = int(time.time())
        TyContext.RedisUser.execute(friend_uid, 'ZADD',
                                    'friend_request:' + str(gameId) + ':' + friend_uid,
                                    timestamp, uid)
        if mo:
            mo.setResult('info', "好友请求发送成功！")
            mo.setResult('code', 0)
            mo.setResult('friend_uid', friend_uid)

        # send notify message to friend if online
        if not score:
            my_info = self.getUserInfo(gameId, uid)
            ext = {'friend_uid': uid, 'friend_name': my_info['nick_name']}
            self.notify_game_server(gameId, clientId, friend_uid, 'add_friend',
                                    my_info['nick_name'] + '加你为好友', ext)
        return True

    @classmethod
    def getFriendRequestsCount(self, gameId, userId):
        userId = str(userId)
        num = TyContext.RedisUser.execute(userId, 'zcard', 'friend_request:' + str(gameId) + ':' + userId)
        return num

    @classmethod
    def getFriendRequests(self, gameId, userId, mo=None, count=-1):
        userId = str(userId)
        requests = TyContext.RedisUser.execute(userId, 'zrevrange', 'friend_request:' + str(gameId) + ':' + userId,
                                               0, count, "WITHSCORES")
        pageList = []
        if requests != None:
            for i in xrange(len(requests) / 2):
                fuid = requests[2 * i]
                ftime = requests[2 * i + 1]
                infos = self.getUserInfo(gameId, fuid)
                # TyContext.MySqlSwap.checkUserDate(fuid)
                # name, sex, pic = TyContext.RedisUser.execute(fuid, 'HMGET', 'user:' + str(fuid), 'name', 'sex', 'purl')
                # infos = {}
                # infos['uid'] = fuid
                # infos['nick_name'] = unicode(name)
                # infos['avatar'] = pic
                # infos['sex'] = sex
                if infos:
                    infos['time'] = int(ftime)
                    pageList.append(infos)
        if mo:
            mo.setResult('data', pageList)
            mo.setResult('code', 0)
        self.setup_friends_game_info(pageList, 1, 1, 1)
        return pageList

    # @classmethod
    # def onAddRequest(self, gameId, userId, friendId, mi, mo):
    #     return True

    @classmethod
    def confirmFriendRequest(self, gameId, uid, friend_uid, is_agree, mo=None):
        friend_uid = str(friend_uid)
        uid = str(uid)
        if is_agree:
            is_size_exceed = self._isFriendsSizeExceed(gameId, uid, mo)
            if is_size_exceed:
                return False
            self._addFriend(gameId, uid, friend_uid)
        TyContext.RedisUser.execute(uid, 'zrem', 'friend_request:' + str(gameId) + ':' + uid, friend_uid)

        info = u"成功添加好友！"
        if not is_agree:
            info = u"您已拒绝好友请求！"

        my_info = self.getUserInfo(gameId, uid)
        if mo:
            mo.setResult('nick_name', my_info['nick_name'])
            mo.setResult('code', 0)
            mo.setResult('info', info)

        http_params = self.get_common_http_params()

        ext = {'friend_uid': uid, 'friend_name': my_info['nick_name']}

        if is_agree:
            self.notify_game_server(gameId, http_params['clientId'], friend_uid, 'accept_friend',
                                    my_info['nick_name'] + '已同意您的好友邀请', ext)
        return True

    # @classmethod
    # def onAddConfirm(self, gameId, userId, friendId, mi, mo, isYes):
    #     return True

    @classmethod
    def delFriend(self, gameId, userId, friendUid, mo):
        friendUid = str(friendUid)
        userId = str(userId)
        self._removeFriend(gameId, userId, friendUid)
        mo.setResult('code', 0)
        mo.setResult('info', u"删除成功！")
        return True

    # @classmethod
    # def onDelFriend(self, gameId, userId, friendId, mo):
    #     return True

    @classmethod
    def getUserInfo(self, gameId, userId):
        if userId == None:
            return {}
        userId = str(userId)
        TyContext.MySqlSwap.checkUserDate(userId)
        name, sex, purl, phone = TyContext.RedisUser.execute(
            userId, 'HMGET', 'user:' + str(userId), 'name', 'sex', 'purl', 'bindMobile')
        if not name:
            return None
        infos = {}
        infos['uid'] = userId
        infos['sex'] = sex
        infos['nick_name'] = TyContext.KeywordFilter.replace(unicode(name))
        # infos['phone'] = phonenumber
        infos['head_url'] = purl
        infos['phone'] = phone
        return infos

    @classmethod
    def getMyFriendIds(cls, uid, gameId):
        friends = TyContext.RedisUser.execute(uid, 'SMEMBERS', 'friend:' + str(gameId) + ':' + str(uid))
        return friends

    @classmethod
    # isAddSelf: 是否加上自己
    def getMyFriends(self, gameId, uid, mo=None, is_add_self=False):
        friends = TyContext.RedisUser.execute(uid, 'SMEMBERS', 'friend:' + str(gameId) + ':' + str(uid))
        if not isinstance(friends, list):
            friends = []
        if is_add_self:
            friends.append(uid)
        pagelist = []
        for fuid in friends:
            finfo = self.getUserInfo(gameId, fuid)
            if not finfo:
                continue
            pagelist.append(finfo)
        pagelist = pagelist[:self.MAX_FRIEND_COUNT]
        self.setup_friends_game_info(pagelist, 1, 1, 1)
        if mo:
            mo.setResult('data', pagelist)
            mo.setResult('code', 0)
        return pagelist

    @classmethod
    def getMaxPraiseNumInfo(cls, userId):
        TyContext.MySqlSwap.checkUserDate(userId)
        # my_vip = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'vip')
        my_vip = TyContext.RunHttp.getRequestParamInt('vip', 0)
        # if not my_vip:
        #     my_vip = 0
        # else:
        #     my_vip = my_vip[0]
        max_praise_num = 10
        try:
            max_praise_num = cls.praise_limit_conf[my_vip]
        except:
            pass
        return my_vip, max_praise_num

    @classmethod
    def get_friend_yes_win_chip(cls, friend_uid):
        # TyContext.MySqlSwap.checkUserDate(friend_uid)
        # friend_winchip = TyContext.UserProps.get_user_chip_all(friend_uid)
        friend_winchip = 0
        try:
            friendIds = [str(friend_uid)]
            friends_info = Friend.get_users_winchip(friendIds)
            friend_winchip = friends_info[0].get('winchip', 0)
        except:
            pass
        return friend_winchip

    @classmethod
    def praise(cls, appId, userId, friend_uid, mo):
        if friend_uid == userId:
            mo.setResult('code', 3)
            mo.setResult('info', "不能给自己点赞")
            return

        if not cls._isFriends(appId, userId, friend_uid):
            mo.setResult('code', 4)
            mo.setResult('info', "非好友不能点赞")
            return

        friend_winchip = cls.get_friend_yes_win_chip(friend_uid)
        if friend_winchip <= 0:
            mo.setResult('code', 5)
            mo.setResult('info', "好友金币为0，不能点赞")
            return

        add_charm = 0
        my_vip, max_praise_num = cls.getMaxPraiseNumInfo(userId)

        day1st_datas_mine = TyContext.Day1st.get_datas(userId, appId)
        day1st_datas_friend = TyContext.Day1st.get_datas(friend_uid, appId)

        praise_num = day1st_datas_mine.get('praise_num', 0)
        day_charm_mine = day1st_datas_mine.get('charm', 0)
        praise_friends = day1st_datas_mine.get('praise_friends', [])

        praised_num = day1st_datas_friend.get('praised_num', 0)
        day_charm_friend = day1st_datas_friend.get('charm', 0)

        mo.setResult('vip', my_vip)

        if praise_num >= max_praise_num:
            mo.setResult('code', 2)
            mo.setResult('info', cls.ERROR_PRAISE_LIMIT_OUT)
            return

        if friend_uid in praise_friends:
            mo.setResult('code', 1)
            mo.setResult('info', cls.ERROR_PRAISE_ALREADY)
            return

        if friend_winchip > 1000000:
            add_charm = 1200
        elif friend_winchip > 200000:
            add_charm = 600
        elif friend_winchip > 50000:
            add_charm = 300
        elif friend_winchip > 10000:
            add_charm = 150
        elif friend_winchip > 0:
            add_charm = 50

        friend_add_charm = 10  # 被点赞方

        my_final_charm = TyContext.UserProps.incr_charm(userId, appId, add_charm)
        friend_final_charm = TyContext.UserProps.incr_charm(friend_uid, appId, friend_add_charm)

        # 注意下面的Day1st.set_datas写法有并发性问题,有时间要改掉 todo
        day1st_datas_mine['praise_num'] = praise_num + 1
        day1st_datas_mine['charm'] = day_charm_mine + add_charm
        praise_friends.append(friend_uid)
        day1st_datas_mine['praise_friends'] = praise_friends

        TyContext.ftlog.debug('day1st_datas_mine=', day1st_datas_mine)
        TyContext.Day1st.set_datas(userId, appId, day1st_datas_mine)

        praised_num += 1
        day1st_datas_friend['praised_num'] = praised_num
        day1st_datas_friend['charm'] = day_charm_friend + friend_add_charm
        TyContext.Day1st.set_datas(friend_uid, appId, day1st_datas_friend)

        user_info = cls.getUserInfo(appId, userId)
        friend_user_info = cls.getUserInfo(appId, friend_uid)
        mo.setResult('nick_name', user_info.get('nick_name'))
        mo.setResult('friend_nick_name', friend_user_info.get('nick_name'))

        mo.setResult('my_add_charm', add_charm)
        mo.setResult('friend_add_charm', friend_add_charm)

        mo.setResult('my_charm', my_final_charm)
        mo.setResult('friend_charm', friend_final_charm)

        mo.setResult('praised_num', praised_num)
        mo.setResult('code', 0)
        mo.setResult('info', '点赞成功')

    @classmethod
    def canPraiseFriend(cls, userId, friend_uid, friends_info_map):
        # friend_winchip = cls.get_friend_yes_win_chip(friend_uid)
        friend_winchip = friends_info_map[friend_uid]
        if friend_winchip == 0:
            return False
        return True

    # @classmethod
    # def get_user_left_praise_num(cls, userId, day1st_datas):
    #     friend_praise_num = day1st_datas['praise_num']
    #     if not friend_praise_num:
    #         friend_praise_num = 0
    #
    #     TyContext.MySqlSwap.checkUserDate(userId)
    #     my_vip = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'vip')
    #     my_praise_num = 10 + my_vip*5
    #     return my_praise_num - friend_praise_num

    @classmethod
    def get_common_http_params(cls):
        appId = TyContext.RunHttp.getRequestParamInt('appId', 0)
        userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
        clientId = TyContext.RunHttp.getRequestParam('clientId', '')
        return {'appId': appId, 'uid': userId, 'clientId': clientId}

    @classmethod
    def get_users_winchip(cls, uids):
        uids_str = ','.join(uids)
        http_params = cls.get_common_http_params()
        url = cls._get_game_server_info_url(http_params['appId'], http_params['clientId'])
        result = cls.http_request(url, {
            'uids': uids_str,
            'for_winchip': 1,
            'for_dashifen': 0,
            'for_online_info': 0,
            'gameids': '6'
        })
        TyContext.ftlog.debug('result---', result)
        try:
            import json
            retjson = json.loads(result)
        except:
            return None
        return retjson

    @classmethod
    # 在线、段位、游戏等数据获取
    def setup_friends_game_info(cls, users, for_online_info=1, for_winchip=0, for_level_info=1):
        if not users:
            return
        uids = []
        for user in users:
            uids.append(str(user['uid']))
        uids_str = ','.join(uids)

        http_params = cls.get_common_http_params()
        url = cls._get_game_server_info_url(http_params['appId'], http_params['clientId'])
        result = cls.http_request(url, {
            'uids': uids_str,
            'for_winchip': for_winchip,
            'for_level_info': for_level_info,
            'for_online_info': for_online_info,
            'gameids': '3,6,8,7,1,10,18,17'  # 斗地主--德州扑克--麻将--三张--斗牛--三顺--保皇
        })

        TyContext.ftlog.debug('result---', result)
        try:
            import json
            retjson = json.loads(result)
            for i in xrange(len(users)):
                user = users[i]
                user_game_info = retjson[i]
                uid = user['uid']
                # gid - 表示用户在哪个游戏中
                gid = user_game_info['gid']
                # 表示用户所在的房间是否支持加入游戏
                rid = user_game_info['rid']
                tid = user_game_info['tid']
                sid = user_game_info['sid']

                # 是否在线, 0 offline 1 online
                user['online'] = user_game_info['state']

                # 是否可加入游戏，用户在线，且在游戏中，可加入游戏
                if gid and (user['online'] != 0) and ((rid + tid + sid) != 0):
                    user['can_join_game'] = 1
                else:
                    user['can_join_game'] = 0

                if for_level_info:
                    user['level'] = user_game_info.get('level', 0)
                    user['level_desc'] = str(user['level']) + "段"
                    level_gid = user_game_info.get('level_game_id')
                    level_pic = user_game_info.get('level_pic')
                    if level_gid > 0:
                        level_game_name = cls.get_sub_game_name(level_gid, http_params['clientId'])
                        user['level_game'] = level_game_name
                        user['level_pic'] = level_pic

                user['chip'] = TyContext.UserProps.get_user_chip_all(uid)
                user['charm'] = TyContext.UserProps.get_charm(uid, 0)

                user['from'] = 1  # 好友来源
                if for_winchip:
                    user['winchip'] = user_game_info['winchip']
                    user['total_winchip'] = user_game_info.get('winchips', 0)

                if for_online_info:
                    user['play_game_id'] = gid  # 正在玩的游戏ID
                    if gid > 0:
                        play_game_name = cls.get_sub_game_name(gid, http_params['clientId'])
                        user['play_game_name'] = play_game_name  # 正在玩的游戏名称
                        user['user_status'] = '正在' + play_game_name + user_game_info.get('room_name', "")  #
                    elif user['online'] > 0:
                        user['user_status'] = '当前在线'
                    else:
                        user['user_status'] = '当前不在线'
                        user['offline_time'] = user_game_info['offline_time']  # 离线时间,分钟
                    user['play_room'] = user_game_info['rid']  #
                    user['play_table'] = user_game_info['tid']

        except Exception, e:
            TyContext.ftlog.debug('setup_friends_game_info error', e.message)
        return users

    # @classmethod
    # def referRequest(cls, gameid, uid, mo):
    #     mo.setError(1, 'pls override me')
    #     return [uid]

    @classmethod
    def get_friend_rank(cls, gameId, uid, mo=None, page=1):
        page = max(1, page)  # 分页请求,数据太大,超63k了
        friends = TyContext.RedisUser.execute(uid, 'SMEMBERS', 'friend:' + str(gameId) + ':' + str(uid))
        if not isinstance(friends, list):
            friends = []
        friends.append(uid)
        begin_idx = (page - 1) * 100
        pagelist = []
        day1st_datas = TyContext.Day1st.get_datas(uid, gameId)
        if len(friends) > begin_idx:
            for fuid in friends:
                finfo = cls.getUserInfo(gameId, fuid)
                if not finfo:
                    continue
                pagelist.append(finfo)
            # pagelist = pagelist[:cls.MAX_FRIEND_COUNT]
            cls.setup_friends_game_info(pagelist, 0, 1, 0)
            praise_friends = day1st_datas.get('praise_friends', [])
            try:
                for i in xrange(len(pagelist)):
                    friend = pagelist[i]
                    yest_winchip = friend.get('winchip', 0)
                    friend_uid = friend['uid']
                    if yest_winchip == 0 or uid == friend_uid or friend_uid in praise_friends:
                        friend['can_praise'] = 0
                    else:
                        friend['can_praise'] = 1
                    # friend['rank'] = i + 1
                    day1st_datas = TyContext.Day1st.get_datas(friend_uid, gameId)
                    friend['praised_num'] = day1st_datas.get('praised_num', 0)
                if pagelist:
                    rank_key = 'winchip'
                    pagelist = sorted(pagelist, key=lambda friendinfo: friendinfo.get(rank_key, 0), reverse=True)
                    for i, user in enumerate(pagelist):
                        # 按用户所在的位置排行
                        user['rank'] = i + 1
            except:
                import traceback
                traceback.print_exc()
            for user in pagelist:
                if int(user['uid']) == int(uid):
                    pagelist.remove(user)
                    pagelist.insert(0, user)
                    break
            pagelist = pagelist[begin_idx:begin_idx + 100]
        if mo:
            mo.setResult('friend_cnt', len(friends))
            _, max_praise_num = cls.getMaxPraiseNumInfo(uid)
            mo.setResult('today_charm', day1st_datas.get('charm', 0))
            mo.setResult('praise_num', day1st_datas.get('praise_num', 0))
            mo.setResult('max_praise_num', max_praise_num)
            mo.setResult('data', pagelist)
            mo.setResult('code', 0)
        return pagelist

    @classmethod
    def addContactFriendInvite(self, gameId, userId, friend_phone, mo):
        gameId = 0
        friend_phone = str(friend_phone)
        userId = str(userId)
        TyContext.RedisUser.execute(userId, 'SADD', 'friend_sms_request:' + str(gameId) + ':' + str(userId),
                                    friend_phone)
        TyContext.RedisFriendMix.execute('SADD', 'friend_sms_request_from:' + str(gameId) +
                                         ':' + friend_phone, userId)
        mo.setResult('info', "success")
        mo.setResult('code', 0)

    @classmethod
    def set_block_friend_request(cls, gameId, uid, is_block=0):
        key = "friend:" + str(gameId) + "setting:" + str(uid)
        TyContext.RedisFriendMix.execute('hset', key, 'is_block_request', is_block)
        return

    @classmethod
    def get_request_block_state(cls, gameId, uid):
        key = "friend:" + str(gameId) + "setting:" + str(uid)
        ret = TyContext.RedisFriendMix.execute('hget', key, 'is_block_request')
        if ret is None:
            ret = 0
        return ret

    @classmethod
    # 新手机注册用户时调用
    def onUserRegisterMobile(self, gameId, userId, phone):
        TyContext.ftlog.debug('onUserRegisterMobile', gameId, userId, phone)
        gameId_hall = 0
        rkey = 'friend_sms_request_from:' + str(gameId_hall) + ':' + str(phone)
        users = TyContext.RedisFriendMix.execute('SMEMBERS', rkey)
        if users == None or len(users) == 0:
            return

        for fuid in users:
            self._addFriend(gameId_hall, userId, fuid)
            rkey1 = 'friend_sms_request:' + str(gameId_hall) + ':' + str(fuid)
            TyContext.RedisUser.execute(fuid, 'SREM', rkey1, phone)
        TyContext.RedisMix.execute('DEL', rkey)

        size = len(users)
        gameId = str(gameId)
        # 奖励邀请者游戏金币
        config_reward = TyContext.Configure.get_global_item_json('friend.smsinvite.reward')
        TyContext.ftlog.debug('config_reward', config_reward, users)
        if config_reward.has_key(gameId):
            TyContext.ftlog.debug('config_reward.has_key')
            chips = int(config_reward[gameId] / size)
            TyContext.ftlog.debug('config_reward.chips', chips)
            for fuid in users:
                TyContext.ftlog.debug('onUserRegisterMobile reward uid=', fuid, 'chips=', chips)
                TyContext.UserProps.incr_chip2(userId, int(gameId), chips, TyContext.ChipNotEnoughOpMode.NOOP,
                                               TyContext.BIEventId.UNKNOWN)
                TyContext.BiReport.gcoin('in.chip.smsinvite', gameId, chips)
                #                 Report.recoderGcoin('in.chip.smsinvite', gameId, chips)
                #                 Report.recoderGcoinDaily('in.chip.smsinvite', gameId, chips)

    @classmethod
    def getContactsForInvite(self, gameId, userId, clientId, contacts, mo):
        data = []
        orig_gameid = gameId
        # gameId = self.gameid_hall
        for contact in contacts:
            item = {}
            if not 'phone' in contact or not 'nick' in contact:
                continue
            nick = contact['nick']
            phone = str(contact['phone'])
            phone = phone.replace(' ', '')

            if phone == '':
                continue
            rkey = 'friend_sms_request:' + str(gameId) + ':' + str(userId)
            is_invite = TyContext.RedisUser.execute(userId, 'SISMEMBER', rkey, phone)

            friend_uid = TyContext.RedisUserKeys.execute('GET', 'mobilemap:' + phone)

            if not friend_uid:
                friend_uid = ''
            else:
                self._addFriend(gameId, userId, friend_uid)
                continue
            item['uid'] = friend_uid
            item['nick'] = nick
            item['phone'] = phone
            item['is_invited'] = is_invite
            data.append(item)
        mo.setResult('data', data)
        mo.setResult('code', 0)
        gameName, url = self.getGameNameAndUrl(orig_gameid, clientId)

        TyContext.MySqlSwap.checkUserDate(userId)
        name = TyContext.RedisUser.execute(userId, 'hget', 'user:' + str(userId), 'name')
        import numbers
        if isinstance(name, numbers.Number):
            name = str(name)
        elif not isinstance(name, unicode):
            name = unicode(name, encoding='utf8')

        sub_game_name = ""
        users = [{'uid': userId}]
        users = self.setup_friends_game_info(users, 0, 0, 1)
        if users:
            sub_game_name = users[0].get('level_game', '')

        '''
        mo.setResult('sms', u"我在\"" + gameName + "\"玩" + sub_game_name
                     + u"，来和我一起玩吧。我的ID是：" + str(userId)
                     + "。" + url + u" 来自：" + name)
        '''
        mo.setResult('sms', u"我在\"" + gameName + "\"玩"
                     + u"，来和我一起玩吧。我的ID是：" + str(userId)
                     + "。" + url + u" 来自：" + name)

        return data

    @classmethod
    def get_sub_game_name(cls, game_id, clientId):
        game_names = TyContext.Configure.get_global_item_json('game_names')

        name = ''
        game_id = str(game_id)
        if game_names:
            name = game_names.get(game_id, '')
        return name

    @classmethod
    def getGameNameAndUrl(self, game_id, clientId):
        game_id = str(game_id)
        # game_names = TyContext.Configure.get_global_item_json('game_names')
        game_urls = TyContext.Configure.get_global_item_json('sns.invite.game_urls')
        name = ''
        url = ''
        # if game_names and game_id in game_names:
        #     name = game_names[game_id]
        # if game_urls and game_id in game_urls:
        #     url = game_urls[game_id]
        import re
        for item in game_urls:
            TyContext.ftlog.debug('item', item)
            patten, name, url = item
            TyContext.ftlog.debug('patten', patten)
            pattenmod = patten.replace('.', '\\.').replace('*', '.*')
            if re.match(re.compile(pattenmod, re.I), clientId):
                break
        return name, url

    @classmethod
    def getNeighborsForInvite(self, gameid, userid, mo):
        """ 获取某个用户的neighbors
        """
        userid = str(userid)
        if not (userid and gameid):
            TyContext.ftlog.error('handle_get_neighbors failed, not enough params',
                                  'user_id =', userid, 'game_id =', gameid)
            return

        # find online_geo value of user_id from online_geo table
        geohash_int = TyContext.RedisOnlineGeo.execute('zscore', 'online_geo:' + str(gameid), userid)
        neighbors = []
        TyContext.ftlog.debug("user geohash_int:", geohash_int)
        neighbors_count = 0
        if geohash_int:
            # geohash_int = geohash_int[0]
            # step = self.msg.getParamInt('step')
            # if not step or step < 0 or step > GeoHash.DEFAULT_STEP:
            step = TyContext.GeoHash.QUERY_STEP
            # calculate neighbors' block using GeoHash
            shift_count = (TyContext.GeoHash.DEFAULT_STEP - TyContext.GeoHash.QUERY_STEP) * 2
            geohash_int = geohash_int >> shift_count

            neighbors_geohash_int = TyContext.GeoHash.get_neighbors(geohash_int, step)
            neighbors_geohash_int.insert(0, geohash_int)
            TyContext.ftlog.debug('neighbors_geohash_int:', neighbors_geohash_int)
            if neighbors_geohash_int:
                # minval = min(neighbors_geohash_int)
                # maxval = max(neighbors_geohash_int)
                # find his neighbors for online_geo table
                for geohash_int_val in neighbors_geohash_int:
                    # geohash_int_val = neighbors_geohash_int[0]
                    # geohash_int_query = geohash_int_val >> shift_count
                    geohash_int_min = geohash_int_val << shift_count
                    geohash_int_max = (geohash_int_val + 1) << shift_count

                    TyContext.ftlog.debug("geohash_int_min:", geohash_int_min, 'geohash_int_max:', geohash_int_max)
                    neighborList = TyContext.RedisOnlineGeo.execute('zrangebyscore', 'online_geo:' + str(gameid),
                                                                    geohash_int_min, geohash_int_max)
                    TyContext.ftlog.debug('neighborList:', neighborList)
                    if neighborList and len(neighborList) > 0:
                        neighbors.extend(neighborList)

            neighbors_count = TyContext.Configure.get_global_item_int('friend.invite.neighbors_count')
            TyContext.ftlog.debug('neighbors:', neighbors)
            if len(neighbors) > 0:
                neighbors.remove(int(userid))
            if len(neighbors) > neighbors_count:
                # neighbors = neighbors[:20]
                if neighbors_count * 3 < len(neighbors):
                    neighbors = random.sample(neighbors, neighbors_count * 3)
                    # mo.setResult('neighbors', neighbors)
        else:
            TyContext.ftlog.error('not found online geo value for', userid)
        infos = []
        infos2 = []
        for uid in neighbors:
            if self._isFriends(0, userid, uid):
                continue
            info = self.getUserInfo(gameid, uid)
            if info:
                infos.append(info)
                rkey = 'friend_request:' + str(self.gameid_hall) + ':' + str(uid)
                is_invited = TyContext.RedisUser.execute(uid, 'zrank', rkey, userid)
                if is_invited is None:
                    is_invited = 0
                    if len(infos2) < neighbors_count:
                        infos2.append(info)
                else:
                    is_invited = 1
                info['is_invited'] = is_invited

        if len(infos) <= neighbors_count:
            infos2 = infos
        elif len(infos2) < neighbors_count:
            size = neighbors_count - len(infos2)
            i = 0
            for info in infos:
                if not info['is_invited']: continue
                infos2.append(info)
                i += 1
                if i >= size: break

        mo.setResult('data', infos2)
        mo.setResult('code', 0)

    @classmethod
    def mergeSnsFriends(self, gameId, uid, sns_type, sns_friends, mo):
        gameId = self.gameid_hall
        for sns_user in sns_friends:
            sns_uid = sns_user['uid']
            sns_id = str(sns_type) + ':' + str(sns_uid)
            userIdBound = TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + sns_id)
            if not userIdBound:
                continue
            Friend.addFriend(gameId, uid, userIdBound)

    @classmethod
    def sendGift(self, gameid, userId, friend_uid, giftId, clientId, mo):
        send_uri = '/v2/game/friend/sendGift'
        delivery_url = ''

        rkey = 'friend:gift:day_send:' + userId  # set
        rkey_recv = 'friend:gift:day_recv_count'  # hash

        exist = TyContext.RedisUser.execute(userId, 'SISMEMBER', rkey, friend_uid)
        if exist:
            mo.setResult('code', 105)
            mo.setResult('info', Friend.err_codes[105])
            return mo
        send_count = TyContext.RedisUser.execute(userId, 'SCARD', rkey)
        if send_count >= 10:
            mo.setResult('code', 106)
            mo.setResult('info', Friend.err_codes[106])
            return mo
        recv_count = TyContext.RedisUser.execute(userId, 'HGET', rkey_recv, friend_uid)
        if recv_count >= 10:
            mo.setResult('code', 107)
            mo.setResult('info', Friend.err_codes[107])
            return mo

        control = TyContext.ServerControl.findServerControl(gameid, clientId)
        TyContext.ftlog.debug('sendGift.control', control)
        if control:
            delivery_url = control['http'] + send_uri
        else:
            mo.setError(3, '系统服务配置错误')
            return True

        params = {'appId': gameid, 'userId': userId, 'clientId': clientId,
                  'giftId': giftId, 'friend_uid': friend_uid}
        datas, httpurl = TyContext.WebPage.webget_json(delivery_url, params)
        try:
            if int(datas['result']['code']) > 0:
                info = datas['result']['info']
                mo.setResult('code', 2)
                mo.setResult('info', info)
                return mo
        except:
            mo.setResult('code', 1)
            mo.setResult('info', "server error")
            return mo

        TyContext.RedisUser.execute(userId, 'SADD', rkey, friend_uid)
        TyContext.RedisMix.execute('hincrby', rkey_recv, friend_uid)
        TyContext.ftlog.info('friend.sendGift from=', userId, 'to=', friend_uid, 'giftId=', giftId)

        if send_count == 0 or not self._is_set_gift_recv_expire:
            nt = time.localtime()
            ntsec = 86400 - (nt[3] * 3600 + nt[4] * 60 + nt[5])
            if send_count == 0:
                TyContext.RedisUser.execute(userId, 'EXPIRE', rkey, ntsec)
            if not self._is_set_gift_recv_expire:
                TyContext.RedisMix.execute('EXPIRE', rkey_recv, ntsec)
        return

    @classmethod
    def _get_game_server_notify_url(cls, appId, clientId):
        control = TyContext.ServerControl.findServerControl(appId, clientId)
        if not control:
            TyContext.ftlog.error('notify_game_server can not find server control, clientId', clientId)
            return None
        return str(control['http']) + '/v2/game/sdk/notify'

    @classmethod
    def _get_game_server_info_url(cls, appId, clientId):
        control = TyContext.ServerControl.findServerControl(appId, clientId)
        if not control:
            TyContext.ftlog.error('notify_game_server can not find server control, clientId', clientId)
            return None
        return str(control['http']) + '/v2/game/sdk/getGameInfo'

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

    @classmethod
    def notify_game_server(cls, appId, clientId, uid, notify_type, notify_msg, notify_ext=None):
        notify_url = cls._get_game_server_notify_url(appId, clientId)
        if not notify_url:
            return
        import json
        params = {
            'appId': appId,
            'clientId': clientId,
            'userId': uid,
            'type': notify_type,
            'message': notify_msg,
        }
        if not notify_ext is None:
            params['ext'] = json.dumps(notify_ext)
        cls.http_request(notify_url, params)
