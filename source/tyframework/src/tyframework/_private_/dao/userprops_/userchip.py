# -*- coding=utf-8 -*-

from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst
from tyframework._private_.lua_scripts.chip_scripts import INCR_CHIP_LUA_SCRIPT, \
    MOVE_CHIP_TO_TABLE_LUA_SCRIPT


class UserChip(DaoConst, DaoBase):
    def _init_singleton_(self):
        self.__buyin__ = 0
        self.INCR_CHIP_ALIAS = 'UserChip.incr_chip_lua_script'
        self.MOVE_CHIP_TO_TABLE_ALIAS = 'UserChip.move_chip_to_table_lua_script'
        self.__ctx__.RedisUser.load_lua_script(self.INCR_CHIP_ALIAS, INCR_CHIP_LUA_SCRIPT)
        self.__ctx__.RedisUser.load_lua_script(self.MOVE_CHIP_TO_TABLE_ALIAS, MOVE_CHIP_TO_TABLE_LUA_SCRIPT)
        self.__ctx__.RedisTableData.load_lua_script(self.INCR_CHIP_ALIAS, INCR_CHIP_LUA_SCRIPT)

    def get_chip(self, uid, gameid=0):
        return self._get_user_attr_int_(uid, self.ATT_CHIP)

    def get_coin(self, uid):
        return self._get_user_attr_int_(uid, self.ATT_COIN)

    def get_diamond(self, uid):
        return self._get_user_attr_int_(uid, self.ATT_DIAMOND)

    def get_coupon(self, uid, gameid):
        return self._get_user_attr_int_(uid, self.ATT_COUPON)

    def get_user_chip_all(self, uid):
        allchip = self._get_user_attr_int_(uid, self.ATT_CHIP)
        for gid in (1, 6, 8, 10):
            allchip += self._get_game_attr_int_(uid, gid, self.ATT_TABLE_CHIP)
        tchips = self.__ctx__.RedisUser.execute(uid, 'HVALS', self.HKEY_TABLECHIP + str(uid))
        if tchips:
            for x in tchips:
                if isinstance(x, (int, float)):
                    allchip += int(x)
        return allchip

    def get_table_chip(self, uid, gameid, *arglist, **argdict):
        '''
        取得用户的table_chip
        返回:
            如果**argdict当中含有tableId参数,那么返回playerdata中的tablechip
            否则返回gamedata中的tablechip
        '''
        tableId = argdict.get(self.ATT_TABLE_ID, None)
        if tableId != None and self.__buyin__ == 1:
            mkey = self.HKEY_TABLECHIP + str(uid)
            mfield = str(tableId)
        else:
            mkey = self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid)
            mfield = self.ATT_TABLE_CHIP
        value = self.__ctx__.RedisUser.execute(uid, 'HGET', mkey, mfield)
        self.__ctx__.ftlog.debug('UserChip->get_table_chip', uid, gameid, argdict, 'result->', value)
        if not isinstance(value, (int, float)):
            return 0
        return int(value)

    def move_all_chip_to_tablechip(self, uid, gameid, eventId, *arglist, **argdict):
        '''
        转移用户所有的chip至tablechip
        参考: set_tablechip_to_range
        '''
        return self.__set_tablechip_to_range__(uid, gameid, -1, -1, eventId, *arglist, **argdict)

    def move_all_tablechip_to_chip(self, uid, gameid, eventId, *arglist, **argdict):
        '''
        转移用户所有的tablechip至chip
        参考: set_tablechip_to_range
        '''
        return self.__set_tablechip_to_range__(uid, gameid, 0, 0, eventId, *arglist, **argdict)

    def set_tablechip_to_n(self, uid, gameid, tablechip, eventId, *arglist, **argdict):
        '''
        设置用户的tablechip至传入的值
        参考: set_tablechip_to_range
        '''
        return self.__set_tablechip_to_range__(uid, gameid, tablechip, tablechip, eventId, *arglist, **argdict)

    def set_tablechip_to_big_than_n(self, uid, gameid, tablechip, eventId, *arglist, **argdict):
        '''
        设置用户的tablechip大于等于传入的值
        参考: set_tablechip_to_range
        '''
        return self.__set_tablechip_to_range__(uid, gameid, tablechip, -1, eventId, *arglist, **argdict)

    def set_tablechip_to_n_if_little_than(self, uid, gameid, tablechip, eventId, *arglist, **argdict):
        '''
        如果用户的tablechip小于传入的值, 至那么设置tablechip至传入的值(不足时会失败)
        参考: set_tablechip_to_range
        '''
        return self.__set_tablechip_to_range__(uid, gameid, tablechip, -2, eventId, *arglist, **argdict)

    def set_tablechip_near_to_n_if_little_than(self, uid, gameid, tablechip, eventId, *arglist, **argdict):
        '''
        tablechip 小于 n 时, 让 tablechip 尽量接近 n
        参考: set_tablechip_to_range
        '''
        return self.__set_tablechip_to_range__(uid, gameid, -2, tablechip, eventId, *arglist, **argdict)

    def set_tablechip_to_range(self, uid, gameid, _min, _max, eventId, *arglist, **argdict):
        '''
        chip与tablechip转换
        使得tablechip在 [_min, _max] 范围内尽量大。
        _min, _max 正常取值范围：>= 0
        特殊取值，代表redis中的当前值：
            -1: chip+tablechip
            -2: tablechip
            -3: chip
        如果**argdict当中含有tableId参数,那么设置playerdata中的tablechip
        否则设置gamedata中的tablechip
        返回: (table_chip_final, user_chip_final, delta_chip)
            table_chip_final 最终的tablechip数量
            user_chip_final 最终的userchip数量
            delta_chip 操作变化的数量
        '''
        return self.__set_tablechip_to_range__(uid, gameid, _min, _max, eventId, *arglist, **argdict)

    def __set_tablechip_to_range__(self, uid, gameid, _min, _max, eventId, *arglist, **argdict):
        assert (isinstance(_min, int) and (_min >= 0 or _min in (-1, -2, -3)) and
                isinstance(_max, int) and (_max >= 0 or _max in (-1, -2, -3)))

        clientId, numberClientId = self.__ctx__.BiUtils.getClientIdNum(None, argdict, gameid, uid, check_msg=0)
        if clientId == None:
            clientId = self.__ctx__.UserSession.get_session_clientid(uid)
        appId = self.__ctx__.UserSession.get_session_gameid(uid)

        tableId = argdict.get(self.ATT_TABLE_ID, None)
        if tableId != None and self.__buyin__ == 1:
            rfield = str(tableId)
            rhashkey = self.HKEY_TABLECHIP + str(uid)
        else:
            rfield = self.ATT_TABLE_CHIP
            rhashkey = self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid)

        tdelta, tfinal, tfixed, delta, final, fixed = \
            self.__ctx__.RedisUser.exec_lua_alias(uid, self.MOVE_CHIP_TO_TABLE_ALIAS, 6,
                                                  uid, gameid, _min, _max,
                                                  rhashkey, rfield)

        self.__ctx__.ftlog.debug('UserChip->set_tablechip_to_range', uid, gameid, _min, _max,
                                 eventId, arglist, argdict, rhashkey,
                                 'result->', tdelta, tfinal, tfixed, delta, final, fixed)

        args = dict(argdict)
        args['clientId'] = clientId
        args['appId'] = appId
        args['_min'] = _min
        args['_max'] = _max
        args.update(argdict)

        eventParam = self.__ctx__.BIEventId.getEventParam(eventId, self.__ctx__.BIEventId.UNKNOWN, **argdict)
        if tfixed != 0:
            self.__ctx__.BiReport.report_bi_chip_update(uid, tfixed, tfixed, 0, self.__ctx__.BIEventId.SYSTEM_REPAIR,
                                                        numberClientId, gameid, appId, eventParam,
                                                        self.__ctx__.BiReport.CHIP_TYPE_TABLE_CHIP)
            self.__ctx__.BiReport.tablechip_update(gameid, uid, tfixed, 0, eventId, *arglist, **args)

        if fixed != 0:
            self.__ctx__.BiReport.report_bi_chip_update(uid, fixed, fixed, 0, self.__ctx__.BIEventId.SYSTEM_REPAIR,
                                                        numberClientId, gameid, appId, eventParam,
                                                        self.__ctx__.BiReport.CHIP_TYPE_CHIP)
            self.__ctx__.BiReport.chip_update(gameid, uid, fixed, 0, eventId, *arglist, **args)

        if tdelta != 0:
            self.__ctx__.BiReport.report_bi_chip_update(uid, tdelta, tdelta, tfinal, eventId,
                                                        numberClientId, gameid, appId, eventParam,
                                                        self.__ctx__.BiReport.CHIP_TYPE_TABLE_CHIP)
            self.__ctx__.BiReport.tablechip_update(gameid, uid, tdelta, tfinal, eventId, *arglist, **args)

        if delta != 0:
            self.__ctx__.BiReport.report_bi_chip_update(uid, delta, delta, final, eventId,
                                                        numberClientId, gameid, appId, eventParam,
                                                        self.__ctx__.BiReport.CHIP_TYPE_CHIP)
            self.__ctx__.BiReport.chip_update(gameid, uid, delta, final, eventId, *arglist, **args)

        return tfinal, final, delta

    def __incr_user_chip_filed__(self, uid, gameid, deltaCount, lowLimit, highLimit, chipNotEnoughOpMode, eventId,
                                 chipType, *arglist, **argdict):
        assert (isinstance(uid, int))
        assert (isinstance(gameid, int))
        assert (isinstance(deltaCount, int))
        assert (isinstance(lowLimit, int))
        assert (isinstance(highLimit, int))
        assert (isinstance(chipNotEnoughOpMode, int))
        assert (isinstance(eventId, int))
        assert (isinstance(chipType, int))

        clientId, numberClientId = self.__ctx__.BiUtils.getClientIdNum(None, argdict, gameid, uid, check_msg=0)

        appId = self.__ctx__.UserSession.get_session_gameid(uid)
        assert (isinstance(appId, int))

        if chipType == self.__ctx__.BiReport.CHIP_TYPE_CHIP:
            filed = self.ATT_CHIP
            mkey = self.HKEY_USERDATA + str(uid)
        elif chipType == self.__ctx__.BiReport.CHIP_TYPE_COIN:
            filed = self.ATT_COIN
            mkey = self.HKEY_USERDATA + str(uid)
        elif chipType == self.__ctx__.BiReport.CHIP_TYPE_DIAMOND:
            filed = self.ATT_DIAMOND
            mkey = self.HKEY_USERDATA + str(uid)
        elif chipType == self.__ctx__.BiReport.CHIP_TYPE_COUPON:
            filed = self.ATT_COUPON
            mkey = self.HKEY_USERDATA + str(uid)
        elif chipType == self.__ctx__.BiReport.CHIP_TYPE_TABLE_CHIP:
            filed = self.ATT_TABLE_CHIP
            mkey = self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid)
            tableId = argdict.get(self.ATT_TABLE_ID, None)
            if tableId != None and self.__buyin__ == 1:
                mkey = self.HKEY_TABLECHIP + str(uid)
                filed = str(tableId)
        else:
            raise Exception('UserChip unknow chipType of ' + str(chipType))

        trueDelta, finalCount, fixed = \
            self.__ctx__.RedisUser.exec_lua_alias(uid, self.INCR_CHIP_ALIAS,
                                                  6, deltaCount, lowLimit, highLimit,
                                                  chipNotEnoughOpMode, mkey, filed)

        self.__ctx__.ftlog.debug('UserChip->incr_user_chip_filed', uid, gameid, deltaCount, lowLimit, highLimit,
                                 chipNotEnoughOpMode, eventId, chipType, mkey, filed,
                                 'result->', trueDelta, finalCount, fixed)

        args = dict(argdict)
        args['clientId'] = clientId
        args['appId'] = appId
        args['deltaCount'] = deltaCount
        args['lowLimit'] = lowLimit
        args['highLimit'] = highLimit
        args['chipType'] = chipType
        args['mode'] = chipNotEnoughOpMode
        args.update(argdict)

        eventParam = self.__ctx__.BIEventId.getEventParam(eventId, self.__ctx__.BIEventId.UNKNOWN, **argdict)

        if fixed != 0:
            self.__ctx__.BiReport.report_bi_chip_update(uid, fixed, fixed, 0, self.__ctx__.BIEventId.SYSTEM_REPAIR,
                                                        numberClientId, gameid, appId, eventParam, chipType)
            if chipType == self.__ctx__.BiReport.CHIP_TYPE_CHIP:
                self.__ctx__.BiReport.chip_update(gameid, uid, fixed, 0, eventId, *arglist, **args)
            elif chipType == self.__ctx__.BiReport.CHIP_TYPE_COIN:
                self.__ctx__.BiReport.coin_update(gameid, uid, fixed, 0, eventId, *arglist, **args)
            elif chipType == self.__ctx__.BiReport.CHIP_TYPE_DIAMOND:
                self.__ctx__.BiReport.diamond_update(gameid, uid, fixed, 0, eventId, *arglist, **args)
            elif chipType == self.__ctx__.BiReport.CHIP_TYPE_TABLE_CHIP:
                self.__ctx__.BiReport.tablechip_update(gameid, uid, fixed, 0, eventId, *arglist, **args)
            elif chipType == self.__ctx__.BiReport.CHIP_TYPE_COUPON:
                self.__ctx__.BiReport.coupon_update(gameid, uid, fixed, 0, eventId, *arglist, **args)

        if trueDelta != 0 or deltaCount == 0:
            self.__ctx__.BiReport.report_bi_chip_update(uid, deltaCount, trueDelta, finalCount, eventId,
                                                        numberClientId, gameid, appId, eventParam, chipType)
            if chipType == self.__ctx__.BiReport.CHIP_TYPE_CHIP:
                self.__ctx__.BiReport.chip_update(gameid, uid, trueDelta, finalCount, eventId, *arglist, **args)
            elif chipType == self.__ctx__.BiReport.CHIP_TYPE_COIN:
                self.__ctx__.BiReport.coin_update(gameid, uid, trueDelta, finalCount, eventId, *arglist, **args)
            elif chipType == self.__ctx__.BiReport.CHIP_TYPE_DIAMOND:
                self.__ctx__.BiReport.diamond_update(gameid, uid, trueDelta, finalCount, eventId, *arglist, **args)
            elif chipType == self.__ctx__.BiReport.CHIP_TYPE_TABLE_CHIP:
                self.__ctx__.BiReport.tablechip_update(gameid, uid, trueDelta, finalCount, eventId, *arglist, **args)
            elif chipType == self.__ctx__.BiReport.CHIP_TYPE_COUPON:
                self.__ctx__.BiReport.coupon_update(gameid, uid, trueDelta, finalCount, eventId, *arglist, **args)

        return trueDelta, finalCount

    def incr_tablechip(self, uid, gameid, deltaCount, chipNotEnoughOpMode, eventId, *arglist, **argdict):
        '''
        对用户的tablechip进行INCR操作
        如果**argdict当中含有tableId参数,那么设置playerdata中的tablechip
        否则设置gamedata中的tablechip
        参考: incr_chip
        '''
        return self.__incr_user_chip_filed__(uid, gameid, deltaCount, -1, -1,
                                             chipNotEnoughOpMode, eventId, self.__ctx__.BiReport.CHIP_TYPE_TABLE_CHIP,
                                             *arglist, **argdict)

    def incr_tablechip_limit(self, uid, gameid, deltaCount, lowLimit, highLimit, chipNotEnoughOpMode, eventId, *arglist,
                             **argdict):
        '''
        对用户的tablechip进行INCR操作
        如果**argdict当中含有tableId参数,那么设置playerdata中的tablechip
        否则设置gamedata中的tablechip
        参考: incr_chip_limit
        '''
        return self.__incr_user_chip_filed__(uid, gameid, deltaCount, lowLimit, highLimit,
                                             chipNotEnoughOpMode, eventId, self.__ctx__.BiReport.CHIP_TYPE_TABLE_CHIP,
                                             *arglist, **argdict)

    def incr_chip_limit(self, uid, gameid, deltaCount, lowLimit, highLimit, chipNotEnoughOpMode, eventId, *arglist,
                        **argdict):
        '''
        对用户的金币进行INCR操作
        @param uid: userId
        @param gameid: 游戏ID
        @param deltaCount: 变化的值可以是负数
        @param lowLimit 用户最低金币数，-1表示没有最低限制
        @param highLimit 用户最高金币数，-1表示没有最高限制
        @param mode: 当INCR动作会变成负数时的处理模式, 0表示不进行操作; 1会给金币清零
        @param eventId: 触发INCR的事件ID
        @param argdict: 需要根据事件传入eventParam
        @return (trueDelta, final) trueDelta表示实际变化的值, final表示变化后的最终数量

        地主收房间服务费示例
        地主每玩完一局需要收服务费, 对用户金币没有上下限，如果用户的金币不够服务费就收取用户所有金币, 所以mode=self.__ctx__.ChipNotEnoughOpMode.CLEAR_ZERO
        用户10001当前金币为100, 在地主601房间(服务费为500)玩了一局, 收服务费代码为
        trueDelta, final = self.__ctx__.UserProps.incr_chip_limit(10001, 6, -500, -1, -1,
                                                                self.__ctx__.ChipNotEnoughOpMode.CLEAR_ZERO,
                                                                self.__ctx__.BIEvent.ROOM_GAME_FEE, roomId=601)
        此时trueDelta=-100, final=0

        地主收报名费示例
        用户10001当前金币为100, 报名610房间的比赛(需要报名费1000金币), 对用户金币没有上下限, 报名费不足则不处理，所以mode=self.__ctx__.ChipNotEnoughOpMode.NOOP
        trueDelta, final = self.__ctx__.UserProps.incr_chip_limit(10001, 6, -1000, -1, -1,
                                                                self.__ctx__.ChipNotEnoughOpMode.NOOP,
                                                                self.__ctx__.BIEvent.MATCH_SIGNIN_FEE, roomId=610)
        if trueDelta == -1000:
            # 收取报名费成功进行报名操作
            pass
        else:
            # 报名费不足，给客户端返回错误
            pass

        有上下限的示例
        在地主601房间最低准入为1000金币，扔鸡蛋价格为10金币，用户10001的当前金币为1000, 此时的delta为10下限为1010, 没有上限
        trueDelta, final = self.__ctx__.UserProps.incr_chip_limit(10001, 6, -10, 1010, -1,
                                                                self.__ctx__.ChipNotEnoughOpMode.NOOP,
                                                                self.__ctx__.BIEvent.EMOTICON_EGG_CONSUME, roomId=610)
        if trueDelta == -10:
            # 收取扔鸡蛋金币成功
            pass
        else:
            # 扔鸡蛋金币不足，给客户端返回错误
            pass
        '''
        return self.__incr_user_chip_filed__(uid, gameid, deltaCount, lowLimit, highLimit,
                                             chipNotEnoughOpMode, eventId, self.__ctx__.BiReport.CHIP_TYPE_CHIP,
                                             *arglist, **argdict)

    def incr_chip(self, uid, gameid, deltaCount, chipNotEnoughOpMode, eventId, *arglist, **argdict):
        '''
        对用户的金币进行INCR操作
        @param uid: userId
        @param gameid: 游戏ID
        @param deltaCount: 变化的值可以是负数
        @param chipNotEnoughOpMode: 当INCR动作会变成负数时的处理模式, 0表示不进行操作; 1会给金币清零
        @param eventId: 触发INCR的事件ID
        @param argdict: 需要根据事件传入eventParam
        @return (trueDelta, final) trueDelta表示实际变化的值, final表示变化后的最终数量
        参考incr_chip_limit的调用，此方法相当于用lowLimit, highLimit都是-1去调用incr_chip_limit
        '''
        return self.__incr_user_chip_filed__(uid, gameid, deltaCount, -1, -1,
                                             chipNotEnoughOpMode, eventId, self.__ctx__.BiReport.CHIP_TYPE_CHIP,
                                             *arglist, **argdict)

    def incr_coin(self, uid, gameid, deltaCount, chipNotEnoughOpMode, eventId, *arglist, **argdict):
        '''
        对用户的COIN进行INCR操作
        参考: incr_chip
        '''
        return self.__incr_user_chip_filed__(uid, gameid, deltaCount, -1, -1,
                                             chipNotEnoughOpMode, eventId, self.__ctx__.BiReport.CHIP_TYPE_COIN,
                                             *arglist, **argdict)

    def incr_diamond(self, uid, gameid, deltaCount, chipNotEnoughOpMode, eventId, *arglist, **argdict):
        '''
        对用户的钻石进行INCR操作
        参考: incr_chip
        '''
        return self.__incr_user_chip_filed__(uid, gameid, deltaCount, -1, -1,
                                             chipNotEnoughOpMode, eventId, self.__ctx__.BiReport.CHIP_TYPE_DIAMOND,
                                             *arglist, **argdict)

    #     def incr_coupon(self, uid, gameid, detalCount, updateEventTag, *arglist, **argdict):
    #         '''
    #         调整用户的兑换券的数量
    #         '''
    #         self.__ctx__.ftlog.debug('incr_coupon', 'uid=', uid, 'gameid=', gameid, 'detalCount=', detalCount, 'updateEventTag=', updateEventTag, arglist, argdict)
    #         finalCount = self.__ctx__.RedisUser.execute(uid, 'HINCRBY', 'user:' + str(uid), self.ATT_COUPON, detalCount)
    #
    #         clientId = self.__ctx__.UserSession.get_session_clientid(uid)
    #         appId = self.__ctx__.UserSession.get_session_gameid(uid)
    #
    #         args = dict(argdict)
    #         args['clientId'] = clientId
    #         args['appId'] = appId
    #
    #         if finalCount > 1000000 or finalCount < 0 :
    #             try:
    #                 self.__ctx__.ftlog.error('ATTENTION the user coupon may be error uid=' + str(uid) + ' detal=' + str(detalCount) + ' final=' + str(finalCount) + ' gameid=' + str(gameid))
    #                 self.__ctx__.ftlog.exception()
    #             except:
    #                 self.__ctx__.ftlog.exception()
    #         self.__ctx__.BiReport.coupon_update(gameid, uid, detalCount, finalCount, updateEventTag, *arglist, **args)
    #         return finalCount

    def incr_coupon(self, uid, gameid, deltaCount, eventId, *arglist, **argdict):
        '''
        对用户的兑换券进行INCR操作
        参考: incr_chip
        '''
        return self.__incr_user_chip_filed__(uid, gameid, deltaCount, -1, -1,
                                             self.__ctx__.ChipNotEnoughOpMode.NOOP,
                                             eventId, self.__ctx__.BiReport.CHIP_TYPE_COUPON,
                                             *arglist, **argdict)
