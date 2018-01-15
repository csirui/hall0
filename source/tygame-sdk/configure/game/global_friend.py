# -*- coding=utf-8 -*-
from pyscript._helper_config_ import add_global_item
from collections import OrderedDict

add_global_item('friend.invite.neighbors_count', 3)

add_global_item('friend.invite.game_urls', {
        '1': u"",
        '3': u"http://www.tuyoo.com",
        '5': u"http://www.tuyoo.com",
        '6': u"http://www.tuyoo.com",
        '7': u"http://www.tuyoo.com/tuyoomahjong/index.html",
        '8': u"http://www.tuyoo.com",
})

add_global_item('friend.smsinvite.reward', {
        '1': 20000,
        '3': 20000,
        '5': 20000,
        '6': 20000,
        '7': 20000,
        '8': 20000,
})

add_global_item('friend.rank.title', {
    '7':{
        'week_master_point': {
            'title': u'好友雀神榜',
            'item_prefix':u'本周雀神分:',
            'item_suffix':u'分',
            }
    }
})

# Android_3.70_360.360.0-hall6.360.day

# add_global_item('sns.invite.game_urls', OrderedDict({
#     'Android_3.7*hall3*': ("途游象棋", "http://zhushou.360.cn/detail/index/soft_id/917916"),
#     'Android_3.7*': ("途游斗地主大厅", "http://openbox.mobilem.360.cn/index/d/sid/1754136"),
#     'IOS_3.7*': ("途游斗地主大厅", "http://openbox.mobilem.360.cn/index/d/sid/1754136")
# }))

add_global_item('sns.invite.game_urls', [

    ('Android_3.7*hall3*', "途游象棋", "http://zhushou.360.cn/detail/index/soft_id/917916"),

    # ('Android_3.7*hall6*(huawei|mi|oppo|91new|baidunew|bdtiebanew|duokunew|lenovo'
    #  '|ppzhushou|ali|coolpad|jinligame|jinli|qq|qqas|qqcustomizedas|qqcustomizedgc'
    #  '|qqexplorer|qqgc|qqic02|qqtmsas|qqtmsgc|qqvideo|huabeidianhua)*', "途游斗地主大厅", "http://www.tuyoo.com"),
    ('Android_3.711_YDJD.YDJD.0-hall6.ydjd.dj', "途游斗地主大厅", ""),
    ('Android_3.711_tyOneKey,tyAccount,tyGuest.woStore.0-hall6.ltwo.dj', "途游斗地主大厅", ""),
    ('Android_3.71_tyOneKey,tyAccount,tyGuest.YDJD.0-hall17*', "途游保皇", ""),

    ('Android_3.7*hall8*', "途游德州扑克", "http://a.app.qq.com/o/simple.jsp?pkgname=com.tuyoo.texas.main"),
    ('IOS_3.7*hall8*', "途游德州扑克", "http://a.app.qq.com/o/simple.jsp?pkgname=com.tuyoo.texas.main"),
    ('IOS_3.711_tyGuest,tyAccount,weixin.appStore.0-hall7.appStore.kuaile', "途游麻将大厅", "https://itunes.apple.com/cn/app/id831385890"),
    ('IOS_3.71_tyGuest,tyAccount.appStore.0-hall21.appStore.paohuzi', "途游跑胡子", ""),
    ('Android_3.7*0-hall6*(91new|bdtiebanew|baidunew|duokunew)*', "途游斗地主大厅", ""),
    ('IOS_3.711_tyGuest,tyAccount,weixin.appStore.0-hall1.appStore.t3card', "途游三张牌", "https://itunes.apple.com/cn/app/id853543134"),
    ('Android_3.7*hall17*', "青岛棋牌", "http://www.tuyoo.com/bh/index.html"),
    ('*3.7*hall17*', "青岛棋牌", "http://www.tuyoo.com/bh/index.html"),
    ('Android_3.7*hall21*', "途游跑胡子", "http://openbox.mobilem.360.cn/index/d/sid/1754136"),
    ('Android_3.7*', "途游斗地主大厅", "http://openbox.mobilem.360.cn/index/d/sid/1754136"),
    ('IOS_3.7*hall6*', "途游斗地主大厅", "http://a.app.qq.com/o/simple.jsp?pkgname=com.tuyoo.doudizhu.maintu")
])

add_global_item('sns.friend.guide',
                '''1、“好友排行”是昨日金币收益（只算赢的）排行榜，为收益高的好友点赞即得大量魅力值~
                2、普通用户每日只能为好友点赞10次，开通（升级）VIP即提高上限~
                3、魅力值高到一定程度即可在“魅力商城”购买专属的炫酷道具，快去逛逛吧~
                4、通过“短信”功能邀请朋友来玩，双方自动成为好友，亲朋好友一起玩~''')
