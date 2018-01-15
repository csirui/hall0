# -*- coding=utf-8 -*-

import time

from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst
from tyframework.decorator.globallocker import global_lock_method
from tyframework.decorator.structdataitem import struct_data_item


@struct_data_item(sformat='3iB', attrs=['reserve', 'last_time', 'vip_days', 'vip_level'])
class _ItemVip(object):
    def __init__(self):
        self.reserve = 0
        self.last_time = 0
        self.vip_days = -1  # >=0表示剩余几天(0是最后一天)，< 0表示非会员或者已经过期
        self.vip_level = 0


class UserVip(DaoConst, DaoBase):
    def _init_singleton_(self):
        self.hall_game_id = self.__ctx__.TYGlobal.gameid()
        pass

    @global_lock_method(lock_name_head='userprops.update.vip', lock_name_tails=['uid'])
    def incr_vip_days(self, uid, gameid, detalVipDays, vipLevel=1):
        '''
        增加用户VIP的有效天数,调整级别
        '''
        assert (detalVipDays >= 0)
        self.__ctx__.ftlog.debug('incr_vip_days', 'uid=', uid, 'gameid=', gameid, 'detalVipDays=', detalVipDays,
                                 'vipLevel=', vipLevel)

        itemvip = self.get_item_by_id(uid, self.hall_game_id, self.VIP_ITEMID, _ItemVip)
        if itemvip.vip_days < 0:  # 非vip
            itemvip.vip_days = detalVipDays
        else:
            itemvip.vip_days = itemvip.vip_days + detalVipDays
        itemvip.vipLevel = vipLevel
        itemvip.last_time = int(time.time())
        self.update_item_by_id(uid, self.hall_game_id, self.VIP_ITEMID, itemvip)
        return itemvip.vip_days, itemvip.vipLevel

    @global_lock_method(lock_name_head='userprops.update.vip', lock_name_tails=['uid'])
    def calculate_vip_days(self, uid, gameid):
        '''
        每日登录时，重新计算用户的VIP剩余天数和级别, 返回(detalDays, leftDays, level)
        detalDays: 表示减少的天数
        leftDays: 表示剩余天数, 0表示最后一天, < 0表示没有了
        level: 级别
        if (leftDays >= 0 and detalDays > 0) 表示当天第一次vip消耗
        '''
        self.__ctx__.ftlog.debug('calculate_vip_days', 'uid=', uid, 'gameid=', gameid, self.hall_game_id)

        itemvip = self.get_item_by_id(uid, self.hall_game_id, self.VIP_ITEMID, _ItemVip)
        if itemvip.vip_days < 0:  # 非vip
            self.__ctx__.ftlog.debug('calculate_vip_days', 'uid=', uid, 'gameid=', self.hall_game_id, 0, -1, 0)
            return 0, -1, 0

        nowtime = int(time.time())
        dcount = int((nowtime - time.timezone) / 86400) - int((itemvip.last_time - time.timezone) / 86400)
        ncount = itemvip.vip_days - dcount
        if dcount < 0:
            dcount = 0
            ncount = 0
        if ncount >= 0:
            if itemvip.vip_days != ncount:
                itemvip.last_time = nowtime
                itemvip.vip_days = ncount
                self.update_item_by_id(uid, self.hall_game_id, self.VIP_ITEMID, itemvip)
        else:
            itemvip.vip_level = 0
            self.remove_item_by_id(uid, self.hall_game_id, self.VIP_ITEMID)
        self.__ctx__.ftlog.debug('calculate_vip_days', 'uid=', uid, 'gameid=', self.hall_game_id, dcount, ncount,
                                 itemvip.vip_level)
        return dcount, ncount, itemvip.vip_level

    def get_vip_info(self, uid, gameid=0):
        '''
        获取vip信息(days, level)
        days: >=0表示剩余几天(0是最后一天)，< 0表示非会员或者已经过期
        level: 级别
        '''
        vipinfo = self.get_item_by_id(uid, self.hall_game_id, self.VIP_ITEMID, _ItemVip)
        self.__ctx__.ftlog.debug('get_vip_info', 'uid=', uid, vipinfo.vip_days, vipinfo.vip_level)
        return vipinfo.vip_days, vipinfo.vip_level
