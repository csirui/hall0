# -*- coding=utf-8 -*-
'''
Created on 2014年12月12日

@author: zhaojiangang
'''

'''
TODO 将这些定义移动到配置文件中, 使用 __get_attr__进行替换封装
'''


class ActivityId(object):
    def __setattr__(self, *args, **kwargs):
        if len(args) == 2 and len(kwargs) == 0:
            name = args[0]
            val = args[1]
            if isinstance(val, int):
                if not hasattr(self, '__all_eventids'):
                    self.__all_eventids = set()
                    self.__all_eventnames = set()
                if name in self.__all_eventnames:
                    raise Exception('the activity name already exits ! ' + name)
                self.__all_eventnames.add(name)

                if val in self.__all_eventids:
                    raise Exception('the activity id already exits ! ' + name + '=' + str(val))
                self.__all_eventids.add(name)

                return object.__setattr__(self, name, val)
        return object.__setattr__(self, *args, **kwargs)

    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.UNKNOWN = 0
        self.CHRISTMAS_RAFFLE = 10001
        self.EXCHANGE_CODE = 10002
        self.FIVE_STAR_RATING = 10003
        self.NOVICE_REWARD = 10004
        self.NSLOGIN_REWARD = 10005
        self.THANKS_GIVING = 10006
        self.TURN_TABLE_RAFFLE = 10007
        self.UPGRADE_REWARD = 10008
        self.VALENTINE_DAY_GUESS = 10009
        self.WORLDCUP_SHOOT = 10010
        self.ZHONGQIU_MAKE_YUEBING = 10011
        self.FLIP_CARD_REWARD = 10013
        self.BIND_SNS_360 = 10014
        self.BIND_PHONE = 10015
        self.FRIEND_GIFTS = 10016
        self.PAWN_GIFTS = 10017
        self.LOTTERY = 10018
        self.NEWYEAR_CHECKIN = 10019
        self.FIXED_INTERVAL = 10020
        self.COMPLETE_GAME = 10021
        self.EVALUATION_REWARD = 10022
        self.LOGIN_RAFFLE = 10023
        self.BAND_TEL = 10023
        self.DOUBLE_ELEVEN = 10024
        self.UPGRADE_165 = 10025
        self.TREE_REWARD = 10026
        self.INPUT_TY_ID = 10027
        self.LOGIN_REWARD = 10028
        self.BOMB_COUNT_REWARD = 10029
        self.PAY_REWARD = 10030
        self.FIRST_PAY_REWARD = 10031
        self.DEGREE_REWARD = 10032
        self.INNINGS_REWARD = 10033
        self.LUCK_NUMBER = 10034
        self.NEI_TUI_GUANG = 10035
        self.SHARE_URL = 10036
        self.PAY_REWARDS = 10037
        self.HUI_YUAN_JIA_ZENG = 10038
        self.SHARE_PROMOTE = 10039
        self.FAN_PAI = 10040
        self.TE_HUI_LI_BAO = 10041
        self.BUY_MEMBER_SEND = 10042
        self.MOMO_FIRST_RECHARGE = 10043
        self.UPGRADE_TO_TEXAS_3_6 = 10044


ActivityId = ActivityId()
