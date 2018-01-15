# -*- coding=utf-8 -*-

# import datetime
# import time

from tyframework._private_.dao.userprops_.daobase import DaoBase
from tyframework._private_.dao.userprops_.daoconst import DaoConst


# import struct
class CheckHallData(DaoConst, DaoBase):
    def _init_singleton_(self):
        pass

    def check_data_update_hall(self, uid, gameid, isnewuser=False):
        # 20150416 ZQH MYSQL DATA COVERT, 所有的冷数据均已经转换为新版大厅数据, 此处仅仅对新用户的4各关键金额值进行初始化
        '''
        检查用户数据的大厅升级
        '''
        self.__ctx__.ftlog.debug('check_data_update_hall', 'uid=', uid, 'gameid=', gameid, 'isnewuser=', isnewuser)
        if isnewuser:
            #             self.set_attr(uid, '_dataver_', 9999)
            self.incr_chip(uid, gameid, 0, self.__ctx__.ChipNotEnoughOpMode.NOOP, self.__ctx__.BIEventId.USER_CREATE)
            self.incr_coin(uid, gameid, 0, self.__ctx__.ChipNotEnoughOpMode.NOOP,
                           self.__ctx__.BIEventId.COIN_HALL_USER_CREATE)
            self.incr_diamond(uid, gameid, 0, self.__ctx__.ChipNotEnoughOpMode.NOOP,
                              self.__ctx__.BIEventId.DIAMOND_HALL_USER_CREATE)
            self.incr_coupon(uid, gameid, 0, self.__ctx__.BIEventId.COUPON_HALL_USER_CREATE)
            return

#
#         chip, coupon, _dataver_ = self.get_attrs(uid, [self.ATT_CHIP, self.ATT_COUPON, '_dataver_'], False)
#         self.__ctx__.ftlog.debug('check_data_update_hall uid=', uid, 'gameid=', gameid, 'chip=', chip, 'coupon=', coupon, '_dataver_=', _dataver_)
# 
#         if _dataver_ == None:
# 
#             if gameid >= 10000 :
#                 self.set_attr(uid, '_dataver_', 10000)
#                 self.incr_chip(uid, gameid, 0,
#                                self.__ctx__.ChipNotEnoughOpMode.NOOP,
#                                self.__ctx__.BIEventId.MERGE_TO_HALL)
#                 self.incr_coupon(uid, gameid, 0, self.__ctx__.BIEventId.USER_CREATE)
#                 self.__ctx__.ftlog.info('check_data_update_hall uid=', uid, '_dataver_=', _dataver_, 'update done of gameid 10000 !!')
#                 return
# 
#             allgames = (1, 6, 7, 8, 10)  # 1金花、2方块、3象棋、4无、5老斗牛、6地主、7麻将、8德州、9跑得快、10斗牛
#             self.incr_attr(uid, '_dataver_', 1)
#             self.__ctx__.ftlog.info('check_data_update_hall uid=', uid, 'chip=', chip, 'coupon=', coupon, '_dataver_=', _dataver_, 'update begin !!')
#             chip, coupon, exp, charm, vipdays = 0, 0, 0, 0, 0
#             for gid in allgames :
#                 gchip, gcoupon, gexp, gcharm, gvipdays = self.__get_game_datas__(uid, gid)
#                 self.__ctx__.ftlog.debug('check_data_update_hall uid=', uid, 'gchip=', gchip, 'gcoupon=', gcoupon, 'gexp=', gexp, 'gcharm=', gcharm, 'gvipdays=', gvipdays)
#                 chip += gchip
#                 coupon = max(gcoupon, coupon)
#                 exp += gexp
#                 charm += gcharm
#                 vipdays += gvipdays
# 
#             self.incr_chip(uid, gameid, chip, self.__ctx__.ChipNotEnoughOpMode.NOOP, self.__ctx__.BIEventId.USER_CREATE)
#             self.incr_coupon(uid, gameid, coupon, self.__ctx__.BIEventId.USER_CREATE)
#             self.incr_charm(uid, gameid, charm)
#             self.incr_exp(uid, gameid, exp)
#             self.incr_attr(uid, '_dataver_', 1)
#             if vipdays > 0 :
#                 itime = int(time.time()) - 86500
#                 self.incr_vip_days(uid, gameid, vipdays, itime)
# 
#             for gid in allgames :
#                 self.__del_game_datas__(uid, gid)
# 
#             self.__ctx__.ftlog.info('check_data_update_hall uid=', uid, 'chip=', chip, 'coupon=', coupon, 'exp=', exp, 'charm=', charm, '_dataver_=', _dataver_, 'update done !!')
#         else:
#             self.__ctx__.ftlog.debug('check_data_update_hall uid=', uid, 'chip=', chip, 'coupon=', coupon, '_dataver_=', _dataver_, ' its new versions !!')
# 
#     def __get_game_datas__(self, uid, gameid):
#         try:
#             self.__ctx__.MySqlSwap.checkUserGameDate(uid, gameid)
#             coupon = self.__get_item_info(uid, gameid, self.OLD_COUPON_ITEMID)
#             chip, tablechip, exp, charm, \
#             vip_info_normal, vip_info_supper, ios_supper_gift_info, \
#             member, try_member, vipLevel, vipExpire, \
#             vip_info = self.__ctx__.RedisGame.execute(uid, 'HMGET', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid),
#                                           'chip', 'tablechip', 'exp', 'charm',
#                                           'vip_info_normal', 'vip_info_supper', 'ios_supper_gift_info',  # 金花VIP
#                                           'member', 'try_member',  # 麻将VIP
#                                           'vipLevel', 'vipExpire',  # 德州VIP
#                                           'vip_info',  # 斗牛
#                                         )
#             if chip == None :
#                 chip = 0
#             if tablechip == None :
#                 tablechip = 0
#             if exp == None :
#                 exp = 0
#             if charm == None :
#                 charm = 0
#             if chip < 0 :
#                 chip = 0
#             if tablechip < 0 :
#                 tablechip = 0
#             if exp < 0 :
#                 exp = 0
#             if charm < 0 :
#                 charm = 0
#             chip += tablechip
# 
#             vipdays = 0
#             if gameid == 1 :
#                 for vipInfo in (vip_info_normal, vip_info_supper, ios_supper_gift_info):
#                     self.__ctx__.ftlog.debug('vipInfo=', vipInfo)
#                     if vipInfo :
#                         try:
#                             vipInfo = eval(vipInfo)
#                             if vipInfo['status'] == 1 :
#                                 days = int(vipInfo['remain_reward_day'])
#                                 if days > 0 :
#                                     vipdays += days
#                         except:
#                             self.__ctx__.ftlog.exception()
# 
#             elif gameid == 6 :
#                 vipdays1 = self.__get_item_info(uid, gameid, '130')
#                 vipdays2 = self.__get_item_info(uid, gameid, '131')
#                 vipdays3 = self.__get_item_info(uid, gameid, '132')
#                 self.__ctx__.ftlog.debug('vipdays=', vipdays1, vipdays2, vipdays3)
#                 if vipdays1 > 0 :
#                     vipdays = int(vipdays1)
#                 if vipdays2 > 0 :
#                     vipdays = int(vipdays2)
#                 if vipdays3 > 0 :
#                     vipdays = int(vipdays3)
# 
#             elif gameid == 7 :
#                 for memberinfo in (member, try_member) :
#                     self.__ctx__.ftlog.debug('memberinfo=', memberinfo)
#                     if memberinfo :
#                         try:
#                             memberinfo = self.__ctx__.strutil.loads(memberinfo)
#                             end_ts = memberinfo['end_ts']
#                             days = int((end_ts - time.time()) / 86400)
#                             if days > 0 :
#                                 vipdays += days
#                         except:
#                             self.__ctx__.ftlog.exception()
# 
#             elif gameid == 8 :
#                 try:
#                     self.__ctx__.ftlog.debug('vipLevel=', vipLevel, 'vipExpire=', vipExpire)
#                     if vipLevel and vipLevel >= 1 and vipExpire and len(vipExpire) == 10:
#                         datas = vipExpire.split(' ')
#                         now = datetime.datetime.now()
#                         days = (now - datetime.datetime(int(datas[0]), int(datas[1]), int(datas[2]))).days
#                         if days >= 0 :
#                             vipdays += days + 1
#                 except:
#                     self.__ctx__.ftlog.exception()
# 
#             elif gameid == 10 :
#                 self.__ctx__.ftlog.debug('vip_info=', vip_info)
#                 if vip_info :
#                     try:
#                         vip_info = self.__ctx__.strutil.loads(vip_info)
#                     except:
#                         vip_info = eval(vip_info)
#                     try:
#                         days = int(vip_info['remain_reward_day'])
#                         if days > 0 :
#                             vipdays += days
#                     except:
#                         self.__ctx__.ftlog.exception()
# 
#             self.__ctx__.ftlog.debug('__get_game_datas__->uid=', uid, 'gameid=', gameid, 'coupon=', coupon, 'chip=', chip)
#             return chip, coupon, exp, charm, vipdays
#         except:
#             self.__ctx__.ftlog.exception('__get_game_datas__uid=', uid, 'gameid=', gameid)
#         return 0, 0, 0, 0, 0
# 
#     def __del_game_datas__(self, uid, gameid):
#         self.__ctx__.RedisGame.execute(uid, 'HDEL', 'item:' + str(gameid) + ':' + str(uid),
#                                     self.OLD_COUPON_ITEMID, '130', '131', '132')
#         self.__ctx__.RedisGame.execute(uid, 'HDEL', self.HKEY_GAMEDATA + str(gameid) + ':' + str(uid),
#                                     'chip', 'exp', 'charm',
#                                     'vip_info_normal', 'vip_info_supper', 'ios_supper_gift_info',  # 金花VIP
#                                     'member', 'try_member',  # 麻将VIP
#                                     'vipLevel', 'vipExpire',  # 德州VIP
#                                     'vip_info',  # 斗牛
#                                     )
# 
#     def __get_item_info(self, uid, gameid, itemid):
#         itdata = self.__ctx__.RedisGame.execute(uid, 'HGET', 'item:' + str(gameid) + ':' + str(uid), itemid)
#         if itdata:
#             try:
#                 itdata = itdata.encode('utf-8')
#             except:
#                 pass
#             try:
#                 _, _, count, _ = struct.unpack("3iB", itdata)
#                 return count
#             except:
#                 self.__ctx__.ftlog.debug('__get_item_info__ error')
#                 pass
#         return -1
