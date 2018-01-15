# -*- coding=utf-8 -*-
'''
Created on 2014年12月12日

@author: zhaojiangang
'''

'''
TODO 将这些定义移动到配置文件中, 使用 __get_attr__进行替换封装
'''


class BIEventId(object):
    def __setattr__(self, *args, **kwargs):
        if len(args) == 2 and len(kwargs) == 0:
            name = args[0]
            val = args[1]
            if isinstance(val, int):
                if not hasattr(self, '__all_eventids'):
                    self.__all_eventids = set()
                    self.__all_eventnames = set()
                if name in self.__all_eventnames:
                    raise Exception('the event name already exits ! ' + name)
                self.__all_eventnames.add(name)

                if val in self.__all_eventids:
                    raise Exception('the event id already exits ! ' + name + '=' + str(val))
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
        self.SYSTEM_REPAIR = 1
        self.TEST_ADJUST = 2

        self.GM_ADJUST = 3  # 事件拆分具化

        self.ACTIVITY_CONSUME = 10001
        self.ACTIVITY_REWARD = 10002
        self.BEAUTYCERT_INSURANCE = 10003
        self.BENE_SEND = 10004
        self.BUY_PRODUCT = 10005
        self.DTASK_CHANGE = 10006
        self.DTASK_REWARD = 10007  # 事件拆分具化
        self.EMOTICON_CONSUME = 10008
        self.EXCHANGE_COUPON = 10009
        self.EXCHANGE_PURPLE_CARD = 10010  # 换紫卡
        self.GAME_BANKER_ABDICATE = 10011
        self.GAME_COMPLAIN_INSURANCE = 10012
        self.GAME_WINLOSE = 10013
        self.GAME_WINLOSE_BR = 10014  # 百人牛牛玩家金币输赢
        self.ITEM_USE = 10015
        self.LED_PUBLIC = 10016
        self.LOTTERYPOOL_REWARD = 10017
        self.MATCH_REWARD = 10018  # 事件拆分具化
        self.MATCH_SIGNIN_FEE = 10019
        self.MEDAL2_REWARD = 10020  # 事件拆分具化
        self.MEDAL_REWARD = 10021
        self.MEMBER_DAY_REWARD = 10022
        self.MEMBER_LOGIN_REWARD = 10023
        self.MERGE_TO_HALL = 10024
        self.NSLOGIN_REWARD = 10025
        self.NSLOGIN_REWARD2 = 10026
        self.ROOM_GAME_FEE = 10027
        self.SYSTEM_ADJUST_ROBOT_CHIP = 10028
        self.TABLE_SITDOWN_SET_TCHIP = 10029
        self.TABLE_STANDUP_TCHIP_TO_CHIP = 10030
        self.TABLE_SUPPLIES = 10031
        self.TABLE_TCHIP_TO_CHIP = 10032
        self.TASK_MASTER_SCORE_UP_LEVEL_REWARD = 10033
        self.TASK_ONLINE_REWARD = 10034
        self.TASK_OPEN_TBOX_REWARD = 10035
        self.TASK_REWARD = 10036
        self.USER_STARTUP = 10037
        self.REFERRER_REWARD = 10038
        #         self.DATA_FROM_MYSQL_2_REDIS = 10039 事件拆分具化
        #         self.DATA_FROM_REDIS_2_MYSQL = 10040 事件拆分具化
        self.MATCH_RETURN_FEE = 10041
        self.FRUIT_BETS = 10042
        self.FRUIT_REWARDS = 10043
        self.BEAUTYCERT_RETURN_INSURANCE = 10044
        self.BEAUTYCERT_REWARDS = 10045
        self.BIG_WIN_FEE = 10046
        self.EMOTICON_EGG_CONSUME = 10047
        self.EMOTICON_FLOWER_CONSUME = 10048
        self.EMOTICON_BOMB_CONSUME = 10049
        self.EMOTICON_DIAMOND_CONSUME = 10050
        self.USER_CREATE = 10051  # 事件拆分具化
        self.GIFT_SEND_CONSUME = 10052
        self.GIFT_PAWN_REWARD = 10053
        self.ROOM_BAICAISHEN = 10054
        self.BUY_IN = 10055
        self.XIJIN_OUT = 10056
        self.XIJIN_IN = 10057
        self.DO_BET = 10058
        self.PK_FEE = 10059
        self.GDSS_ADJUST_CHIP = 10060
        self.RETURN_TABLECHIP = 10061  # 德州边池退钱
        self.SLOT_MACHINE = 10062  # 三张老单包AAA
        self.FIREWORK_BUY = 10063  # 大丰收购买礼花
        self.FIREWORK_BASEFEE = 10064  # 大丰收礼花基础抽水
        self.FIREWORK_OTHERFEE = 10065  # 大丰收礼花额外抽水
        self.FIREWORK_PRIZE = 10066  # 大丰收礼花奖励
        self.ACTIVITY_EXCHANGE = 10067  # 兑换码活动
        self.TEXAS_FLIP_CARD_GAME_IN = 10068  # 德州牌桌翻牌游戏：用户下注
        self.TEXAS_FLIP_CARD_GAME_OUT = 10069  # 德州牌桌翻牌游戏：用户获得奖励
        self.FIRST_RECHARGE = 10070  # 首充大礼包道具赠送
        self.GAOBEI_SERVER_FEE = 10071  # 高倍服务费（抽水费）
        self.LOTTERYPOOL_REWARD_BR = 10072  # 百人彩池奖励

        self.VIP_REWARD = 10073  # 升级为VIP时给的奖励
        self.VIP_GIFT_REWARD = 10074  # 领取VIP礼包的奖励

        self.BENE_SEND_VIP_EXT = 10075  # VIP特权多送的救济金
        self.BENE_SEND_VIP_EXT_TIMES = 10076  # VIP特权多送的救济金次数

        self.VIP_GOT_ASSISTANCE = 10077  # VIP江湖救急

        self.DATA_FROM_MYSQL_2_REDIS_CHIP = 10078
        self.DATA_FROM_REDIS_2_MYSQL_CHIP = 10082
        self.FIRST_RECHARGE_REWARD = 10086  # 首充大礼包道具使用
        self.ACTIVITY_FAN_PAI = 10087  # 地主翻牌活动
        self.GM_ADJUST_CHIP = 10088  # GM工具调整金币
        self.DTASK_REWARD_CHIP = 10089  # 任务奖励
        self.TE_HUI_LI_BAO = 10090  # 特惠礼包加赠
        self.T3FLUSH_TUTORIAL_REWARD = 10097  # 金三顺新手引导奖励
        self.RANDOM_LOTTERY_PRIZE = 10098  # 喷喷喷彩池奖励
        self.MEDAL2_REWARD_CHIP = 10099  # 勋章奖励
        self.WINNER_TAX = 10100  # 赢家收税(劫富济贫)
        self.TUTORIAL_AWARD = 10101  # 新手引导奖励
        self.PRESENT_MATCH_TICKET = 10102  # 赠送参赛券
        self.RANK_REWARD = 10103  # 排行榜奖励
        self.ACTIVITY_LOGIN = 10104  # 地主登录赠送活动
        self.GAME_WINLOSE_RETURN_CHIP = 10105  # pineapple 返还多扣的金币
        self.DEALER_SPARE = 10106  # 海外德州 荷官打赏
        self.AVATAR_PURCHASE = 10107  # 海外德州 人物购买
        self.CALABASH_PURCHASE = 10108  # 海外德州 葫芦娃购买
        self.MATCH_REBUY = 10109  # 比赛重购（金币->筹码）
        self.MATCH_ADDON = 10110  # 比赛增购（金币->筹码）
        self.TABLE_GAME_FLOP_REWARD = 10111  # 桌面游戏翻牌奖励
        self.TABLE_GAME_FLOP_FEE = 10112  # 桌面游戏翻牌消费
        self.MOMO_FIRST_RECHARGE = 10113  # 陌陌斗地主首充奖励
        self.GAME_ROBOT_WINLOSE_BR = 10114  # 百人牛牛机器人的输赢统计
        self.UPDATE_CLIENT_ACT_REWARD = 10115  # 客户端升级活动奖励
        self.FRUIT_TASK_REWARD = 15315  # 大丰收每日成就
        self.FRUIT_GIVEBACK = 15318  # 大丰收彩池基金

        ##### !!!! 从11000开始预留给SDK登录事件，请注意!!!!
        self.SDK_LOGIN_BY_MAIL_SUCC = 11000
        self.SDK_LOGIN_BY_DEVID_SUCC = 11001
        self.SDK_LOGIN_BY_MOBILE_SUCC = 11002
        self.SDK_LOGIN_BY_SNSID_SUCC = 11003
        self.SDK_LOGIN_BY_MAIL_FAIL = 11004
        self.SDK_LOGIN_BY_DEVID_FAIL = 11005
        self.SDK_LOGIN_BY_MOBILE_FAIL = 11006
        self.SDK_LOGIN_BY_SNSID_FAIL = 11007
        self.SDK_CREATE_BY_DEVID_SUCC = 11008
        self.SDK_CREATE_BY_SNSID_SUCC = 11009
        self.SDK_CREATE_BY_MOBILE_SUCC = 11010
        self.SDK_CREATE_BY_DEVID_FAIL = 11011
        self.SDK_CREATE_BY_SNSID_FAIL = 11012
        self.SDK_CREATE_BY_MOBILE_FAIL = 11013
        self.SDK_CREATE_BY_MAIL_SUCC = 11014
        self.SDK_CREATE_BY_MAIL_FAIL = 11015
        self.SDK_BIND_USER_MOBILE_SUCC = 11016
        self.SDK_SEND_SMS_VERIFY_CODE = 11017
        ##### !!!! 从12000开始预留给SDK支付事件，请注意!!!!
        self.SDK_BUY_CREATE = 12000
        self.SDK_BUY_CLIENT_FINISHED = 12001
        self.SDK_BUY_CLIENT_CANCELED = 12002
        self.SDK_BUY_REQUEST_OK = 12003
        self.SDK_BUY_REQUEST_RETRY = 12004
        self.SDK_BUY_REQUEST_ERROR = 12005
        self.SDK_BUY_CALLBACK_OK = 12006
        self.SDK_BUY_CALLBACK_FAIL = 12007
        self.SDK_BUY_DELIVER_OK = 12008
        self.SDK_BUY_DELIVER_FAIL = 12009
        self.SDK_BUY_INTERNAL_ERR = 12010
        self.SDK_SUBSCRIBE_MONTHLY_VIP = 12011
        self.SDK_UNSUBSCRIBE_MONTHLY_VIP_TEMP = 12012
        self.SDK_UNSUBSCRIBE_MONTHLY_VIP = 12013
        self.SDK_RENEW_SUBSCRIBE_MONTHLY_VIP = 12014
        self.SDK_MOBILE_OUT_OF_SERVEICE = 12015
        self.SDK_SUBSCRIBE_MONTHLY_VIP_ALIPAY = 12016
        self.SDK_SUBSCRIBE_MONTHLY_VIP_WEIXIN = 12017
        ##### !!!! 11000和12000段预留给SDK事件，请注意!!!!

        ##### !!!! 13000段为兑换券事件，请注意!!!!
        self.COUPON_TEST_ADJUST = 13001  # 测试调整
        self.COUPON_TEXAS_TBOX = 13002  # 6局宝箱奖励
        self.COUPON_TEXAS_NEW_USER = 13003  # 创建用户gamedata赠送
        self.COUPON_TEXAS_MATCH_REWARD = 13004  # 比赛奖励发放
        self.COUPON_TEXAS_REWARD_CODE = 13005  # 兑换码

        self.COUPON_TEXAS_PURPLE = 13002  # 测试调整
        self.COUPON_TEXAS_ADMIN = 13003  # 测试调整
        self.COUPON_TEXAS_SNG_MATCH = 13004  # 测试调整
        self.COUPON_TEXAS_LINER_MATCH = 13005  # 测试调整

        self.COUPON_T3CARD_MONTHCHARGE = 13006  # 测试调整
        self.COUPON_T3CARD_MEDAL = 13007  # 测试调整
        self.COUPON_T3CARD_UNKNOW = 13008  # 测试调整
        self.COUPON_MAJIANG_TASK = 13009  # 麻将任务奖券
        self.COUPON_MAJIANG_MATCH = 13010  # 麻将比赛奖券
        self.COUPON_HALL_USER_CREATE = 13011  # 用户初始化
        self.COUPON_DOUNIU_UNKNOW = 13012  # 测试调整
        self.COUPON_DIZHU_GAME_WIN = 13013  # 地主牌局结算
        self.COUPON_DIZHU_PAY100 = 13014  # 地主充值登陆奖励
        self.COUPON_DIZHU_UNKNOW = 13015  # 地主奖券商品
        self.COUPON_DIZHU_MOONBOX = 13016  # 地主使用月光之钥
        self.COUPON_DIZHU_NEWR_RAFFLE = 13017  # 地主新手福利抽奖大礼包
        self.COUPON_DIZHU_NEWER_GIFTS = 13018  # 地主新手大礼包
        self.COUPON_DIZHU_PAY = 13019  # 地主20张奖券商品
        self.COUPON_MEDAL_REWARD = 13020  # 测试调整
        self.COUPON_RAFFLE = 13021  # 购买抽奖商品获得奖券
        self.COUPON_BUY_BY_COIN = 13022  # 测试调整
        self.COUPON_ADD_ITEM = 13023  # 奖券添加
        self.COUPON_USE = 13024  # 奖券兑换
        self.COUPON_BANK_UNKNOW = 13025  # 测试调整
        self.COUPON_T3CARD_TURNTABLE = 13026  # 抽奖赠送
        self.COUPON_T3CARD_NEWYEAR = 13027  # 新年活动赠送
        self.COUPON_T3CARD_DOUBLE_ELEVEN = 13028  # 双11活动赠送
        self.COUPON_T3CARD_XMAS13_CHIPS = 13029  # 圣诞铃铛兑换定制筹码附赠
        self.COUPON_T3CARD_XMAS13_POKER = 13030  # 圣诞铃铛兑换扑克附赠
        self.COUPON_T3CARD_XMAS13_5WINS = 13031  # 圣诞节5胜
        self.COUPON_DOUNIU_BAOSHI = 13032  # 测试调整
        self.COUPON_DOUNIU_ACTIVITY = 13033  # 测试调整
        self.COUPON_DIZHU_TURN_TABLE = 13034  # 地主翻牌活动
        self.COUPON_DIZHU_ACT_OLDUSER = 13035  # 地主老用户奖励活动
        self.COUPON_DIZHU_NOVICE_REWARD = 13036  # 地主新手场奖励活动
        self.COUPON_DIZHU_ACT_NEWYEAR = 13037  # 地主新年活动
        self.COUPON_DIZHU_NEI_TUI_GUANG = 13038  # 地主红包内推广活动
        self.COUPON_DIZHU_MONTHER_DAY = 13039  # 地主母亲节活动
        self.COUPON_DIZHU_CHRISTMAS = 13040  # 地主圣诞节活动
        self.DATA_FROM_MYSQL_2_REDIS_COUPON = 13041  # 冷用户转热用户
        self.DATA_FROM_REDIS_2_MYSQL_COUPON = 13042  # 热用户转冷用户
        self.GM_ADJUST_COUPON = 13043
        self.DTASK_REWARD_COUPON = 13044  # 任务奖励
        self.MEDAL2_REWARD_COUPON = 13045  # 勋章奖励
        self.COUPON_T3FLUSH_BOX = 13046  # 金三顺宝箱领取
        self.COUPON_T3CARD_BOX = 13047  # 三张新宝箱
        self.COUPON_DIZHU_MEDAL_BAIRENWIN = 13048  # 地主百人斩勋章奖券奖励
        self.COUPON_DIZHU_MEDAL_GAME100 = 13049  # 地主游戏100局勋章奖券奖励
        self.COUPON_DIZHU_TREASUREBOX = 13050  # 地主游戏100局勋章奖券奖励
        self.COUPON_DIZHU_FLIP_CARD = 13051  # 地主翻奖奖券奖励
        self.COUPON_DIZHU_MATCH_REWARD = 13052  # 地主比赛奖券奖励
        self.COUPON_DIZHU_UPGRADE = 13053  # 地主升级奖励

        ##### !!!! 14000段为游戏转换 牌桌 比赛 事件，请注意!!!!
        self.CREATE_GAME_DATA = 14001  # 创建新进用户数据
        self.BIND_USER = 14002  # 游戏大厅登录用户
        self.BIND_GAME = 14003  # 游戏插件登录用户
        self.TABLE_START = 14004  # 游戏每局开始(每局每个玩家汇报一次)
        self.TABLE_CARD = 14005  # 游戏每局出牌(每局每个玩家汇报一次)
        self.TABLE_WIN = 14006  # 游戏每局结束(每局每个玩家汇报一次)
        self.MATCH_SIGN_UP = 14007  # 比赛报名
        self.MATCH_SIGN_OUT = 14008  # 比赛退赛
        self.MATCH_START = 14009  # 比赛开始(每比赛每个玩家汇报一次)
        self.MATCH_FINISH = 14010  # 比赛结束(每比赛每个玩家汇报一次)
        self.ENTER_ROOM = 14011  # 进入房间
        self.LEAVE_ROOM = 14012  # 离开房间

        ##### !!!! 15000段为COIN DIAMOND 其他ITEM 事件，请注意!!!!
        self.GM_ADJUST_COIN = 15001
        self.DATA_FROM_MYSQL_2_REDIS_COIN = 15002
        self.DATA_FROM_REDIS_2_MYSQL_COIN = 15003
        self.COIN_HALL_USER_CREATE = 15004  # 用户初始化

        self.GM_ADJUST_DIAMOND = 15101
        self.DATA_FROM_MYSQL_2_REDIS_DIAMOND = 15102
        self.DATA_FROM_REDIS_2_MYSQL_DIAMOND = 15103
        self.DIAMOND_HALL_USER_CREATE = 15104  # 用户初始化

        self.ITEM_USER_CREATE = 15201  # 事件拆分具化

        self.REWARD_DOG_MAX = 15319  # 跑狗王获取金币事件

        self.PARAM_NAME_MAP = {
            self.ACTIVITY_CONSUME: 'activityId',
            self.ACTIVITY_REWARD: 'activityId',
            self.BUY_PRODUCT: 'productId',
            self.DTASK_REWARD: 'taskId',
            self.EMOTICON_CONSUME: 'emoticonId',
            self.GAME_BANKER_ABDICATE: 'roomId',
            self.GAME_COMPLAIN_INSURANCE: 'roomId',
            self.GAME_WINLOSE: 'roomId',
            self.GAME_WINLOSE_BR: 'roomId',
            self.WINNER_TAX: 'roomId',
            self.ITEM_USE: 'itemId',
            self.MATCH_REWARD: 'roomId',
            self.COUPON_DIZHU_MATCH_REWARD: 'roomId',
            self.MATCH_SIGNIN_FEE: 'roomId',
            self.MEDAL2_REWARD: 'medalId',
            self.MEDAL_REWARD: 'medalId',
            self.NSLOGIN_REWARD: 'nlogin',
            self.NSLOGIN_REWARD2: 'nlogin',
            self.ROOM_GAME_FEE: 'roomId',
            self.TABLE_SITDOWN_SET_TCHIP: 'roomId',
            self.TABLE_STANDUP_TCHIP_TO_CHIP: 'roomId',
            self.TABLE_SUPPLIES: 'roomId',
            self.TASK_REWARD: 'taskId',
            self.BIG_WIN_FEE: 'roomId',
            self.GIFT_SEND_CONSUME: 'giftId',
            self.GIFT_PAWN_REWARD: 'giftId',
            self.REFERRER_REWARD: 'referrerUserId',
            self.ROOM_BAICAISHEN: 'roomId',
            self.TASK_OPEN_TBOX_REWARD: 'roomId',
            self.BUY_IN: 'roomId',
            self.XIJIN_OUT: 'roomId',
            self.XIJIN_IN: 'roomId',
            self.DO_BET: 'roomId',
            self.PK_FEE: 'roomId',
            self.TEXAS_FLIP_CARD_GAME_IN: 'roomId',
            self.TEXAS_FLIP_CARD_GAME_OUT: 'roomId',
            self.LOTTERYPOOL_REWARD: 'roomId',
            self.GAOBEI_SERVER_FEE: 'roomId',
            self.VIP_REWARD: 'vipLevel',
            self.VIP_GIFT_REWARD: 'vipLevel',
            self.TUTORIAL_AWARD: 'awardType',
            self.RANK_REWARD: 'rankingId',
            self.COUPON_T3FLUSH_BOX: 'roomId',
            self.RANDOM_LOTTERY_PRIZE: 'roomId',
        }

    def getEventParam(self, eventId, defaultParam, **argdict):
        name = self.PARAM_NAME_MAP.get(eventId, None)
        if name is None:
            return defaultParam
        param = argdict.get(name)
        if param is None:
            return defaultParam
        return param


BIEventId = BIEventId()
