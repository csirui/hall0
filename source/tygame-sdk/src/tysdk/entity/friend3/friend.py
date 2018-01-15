# -*- coding=utf-8 -*-

import random
import time

from tyframework.context import TyContext

'''
好友模块

'''


class Friend():
    MAX_FRIEND_COUNT = 100
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
    }

    # game_names = {
    #     1: u"扎金花",
    #     3: u"象棋",
    #     5: u"斗牛",
    #     6: u"斗地主",
    #     7: u"麻将",
    #     8: u"德州",
    # }
    #
    # game_urls = {
    #     1: u"",
    #     3: u"http://www.tuyoo.com",
    #     5: u"http://www.tuyoo.com",
    #     6: u"http://www.tuyoo.com",
    #     7: u"http://www.tuyoo.com",
    #     8: u"http://www.tuyoo.com",
    # }
    #
    # config_reward = {
    #     '7': 20000,
    # }

    # @classmethod
    # def _checkAlreadyFriend(self, gameId, userId, friendId, mo):
    #     if userId == friendId :
    #         mo.setResult("code", 1)
    #         mo.setResult("info", 'self cannot be friends')
    #         return False
    #     if not self._isFriends(gameId, userId, friendId):
    #         return False
    #     else:
    #         mo.setResult("code", 2)
    #         mo.setResult("info", 'already friends')
    #         return True

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
    def _isFriendsSizeExceed(cls, gameId, userId, mo):
        size = cls._getMyFriendSize(gameId, userId)
        if size > cls.MAX_FRIEND_COUNT:
            mo.setResult('code', 102)
            mo.setResult('info', cls.err_codes[102])
            return True
        return False

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
    def addFriendRequest(self, gameId, uid, friend_uid, mo):
        # friendId = mi.getParamInt('friend', 0)
        # mo.setResult('fromUserId', userId)
        # mo.setResult('toUserId', friendId)
        gameId = 0
        uid = str(uid)
        friend_uid = str(friend_uid)
        ret = self._isFriends(gameId, uid, friend_uid)
        if not ret:
            is_size_exceed = self._isFriendsSizeExceed(gameId, uid, mo)
            if not is_size_exceed:
                # self.onAddRequest(gameId, userId, friendUid, mi, mo)
                # if not mo.isError() : # friend:0:invite
                # TyContext.RedisUser.execute(userId, 'LPUSH', 'friend_request:' + str(gameId) + ':' + userId, friendUid)
                timestamp = int(time.time())
                TyContext.RedisUser.execute(friend_uid, 'ZADD', 'friend_request:' + str(gameId) + ':' + friend_uid,
                                            timestamp, uid)
                mo.setResult('info', u"好友请求发送成功！")
                mo.setResult('code', 0)
                mo.setResult('friend_uid', friend_uid)
        else:
            mo.setResult('code', 101)
            mo.setResult('info', self.err_codes[101])
        return True

    @classmethod
    def getFriendRequests(self, gameId, userId, mo):
        gameId = 0
        userId = str(userId)
        requests = TyContext.RedisUser.execute(userId, 'zrevrange', 'friend_request:' + str(gameId) + ':' + userId,
                                               0, -1, "WITHSCORES")
        pageList = []
        if requests != None:
            for i in xrange(len(requests) / 2):
                fuid = requests[2 * i]
                ftime = requests[2 * i + 1]
                TyContext.MySqlSwap.checkUserDate(fuid)
                name, sex, pic = TyContext.RedisUser.execute(fuid, 'HMGET', 'user:' + str(fuid), 'name', 'sex', 'purl')
                infos = {}
                infos['uid'] = fuid
                infos['nick'] = unicode(name)
                infos['avatar'] = pic
                infos['sex'] = sex
                infos['time'] = int(ftime)
                pageList.append(infos)
        mo.setResult('data', pageList)
        mo.setResult('code', 0)

    # @classmethod
    # def onAddRequest(self, gameId, userId, friendId, mi, mo):
    #     return True

    @classmethod
    def confirmFriendRequest(self, gameId, uid, friend_uid, is_agree, mo):
        gameId = 0
        friend_uid = str(friend_uid)
        uid = str(uid)
        if is_agree:
            is_size_exceed = self._isFriendsSizeExceed(gameId, uid, mo)
            if is_size_exceed:
                return
            self._addFriend(gameId, uid, friend_uid)
        TyContext.RedisUser.execute(uid, 'zrem', 'friend_request:' + str(gameId) + ':' + uid, friend_uid)
        mo.setResult('code', 0)
        info = u"成功添加好友！"
        if not is_agree:
            info = u"您已拒绝好友请求！"
        mo.setResult('info', info)

    # @classmethod
    # def onAddConfirm(self, gameId, userId, friendId, mi, mo, isYes):
    #     return True

    @classmethod
    def delFriend(self, gameId, userId, friendUid, mo):
        gameId = 0
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
        name, sex, purl = TyContext.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId), 'name', 'sex', 'purl')
        infos = {}
        infos['uid'] = userId
        infos['sex'] = sex
        infos['nick'] = unicode(name)
        # infos['phone'] = phonenumber
        infos['avatar'] = purl
        return infos

    @classmethod
    # isAddSelf: 是否加上自己
    def getMyFriends(self, gameId, uid, mo=None, is_add_self=False):
        gameId = 0
        friends = TyContext.RedisUser.execute(uid, 'SMEMBERS', 'friend:' + str(gameId) + ':' + str(uid))
        if is_add_self:
            if not friends: friends = []
            friends.append(uid)
        pagelist = []
        if friends:
            for fuid in friends:
                finfo = self.getUserInfo(gameId, fuid)
                pagelist.append(finfo)
        if mo:
            mo.setResult('data', pagelist)
            mo.setResult('code', 0)
        return pagelist

    # @classmethod
    # def referRequest(cls, gameid, uid, mo):
    #     mo.setError(1, 'pls override me')
    #     return [uid]

    @classmethod
    def addContactFriendInvite(self, gameId, userId, friend_phone, mo):
        gameId = 0
        friend_phone = str(friend_phone)
        userId = str(userId)
        TyContext.RedisUser.execute(userId, 'SADD', 'friend_sms_request:' + str(gameId) + ':' + str(userId),
                                    friend_phone)
        TyContext.RedisFriendMix.execute('SADD', 'friend_sms_request_from:' + str(gameId) + ':' + friend_phone, userId)
        mo.setResult('info', "success")
        mo.setResult('code', 0)

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
        gameId = self.gameid_hall
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
                self._isFriends(gameId, userId, friend_uid)
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
        mo.setResult('sms', u"我在途游游戏玩《" + gameName + u"》，你也来玩吧。" + url + u" 来自：" + name)
        return data

    @classmethod
    def getGameNameAndUrl(self, game_id, clientId):
        # 根据clientid获取游戏真是ID
        if clientId and clientId.find('hall') >= 0:
            try:
                game_id = clientId.split('hall')[1].split('.')[0]
            except:
                game_id = str(game_id)
        else:
            game_id = str(game_id)
        game_names = TyContext.Configure.get_global_item_json('game_names')
        game_urls = TyContext.Configure.get_global_item_json('friend.invite.game_urls')
        name = ''
        url = ''
        if game_names and game_id in game_names:
            name = game_names[game_id]
        if game_urls and game_id in game_urls:
            url = game_urls[game_id]
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
