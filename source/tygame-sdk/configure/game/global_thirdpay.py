# -*- coding=utf-8 -*-

from pyscript._helper_config_ import add_global_item, add_client_item_old, \
    add_template_item

add_global_item('aigame_configs', {
        'client_id': '32767682',
        'ClientSecret': '93858fa21846485789e3ec8ec5221b27',
})

add_global_item('huabeidianhua_configs', {
    'client_id':'99226854',
    'client_secret':'380ec179c21843bc81bd59db73778ee1',
})

add_global_item('eft_telecom_msgcode', {
        # price: [paycode, orderphone]
        1  : ['az', '106605501'],
        2  : ['qz', '106605504'],
        5  : ['cz', '106605502'],
        6  : ['131000GR000001B000Uk001', '11802115060'],
        8  : ['131000GR000001B000Um001', '11802115080'],
        10 : ['170#HJ47#', '1066916504'],
        30 : ['142#HJ51#', '1066916508'],
})

add_global_item('eft_telecom_prod_prices', {
        'VOICE100'             :1,
        'T20K'                 :2,
        'CARDMATCH10'          :2,
        'MOONKEY'              :2,
        'C2'                   :2,
        'D20'                  :2,
        'T50K'                 :5,
        'MOONKEY3'             :5,
        'RAFFLE'               :5,
        'ZHUANYUN'             :5,
        'D50'                  :5,
        'T60K'                 :6,
        'C6_RAFFLE'            :6,
        'C6'                   :6,
        'TEXAS_COIN_LUCKY_R6'  :6,
        'TEXAS_COIN_R6'        :6,
        'RAFFLE_NEW'           :8,
        'T80K'                 :8,
        'ZHUANYUN_MEZZO'       :8,
        'ZHUANYUN_MXDDZ'       :8,
        'C8'                   :8,
        'C8_RAFFLE'            :8,
        'C8_LUCKY'             :8,
        'TEXAS_COIN_LUCKY_R8'  :8,
        'TEXAS_COIN_R8'        :8,
        'TGBOX9'               :8,
        'RAFFLE_8'             :8,
        'ZHUANYUN_8'           :8,
        'T100K'                :10,
        'C10'                  :10,
        'TEXAS_COIN2'          :10,
        'D100'                 :10,
        'T300K'                :30,
})

'''优酷配置
德州
APPID 690
APPKEY: fd2b34f2546974bf
APPSECRET: 932896ec4cd2e1e0cefa96e64fb6cf61
PAYKEY: 42a4e67ed166a358e76dd67c62edcc33
地主
APPID 691
APPKEY: 1814fe817d71731e
APPSECRET: 06292969c9d956857669a2d9157cdcb6
PAYKEY: 62d48da6995a90d7e82fbdb5af877300
麻将
APPID 692
APPKEY: 73686281ad200fc2
APPSECRET: bc11344dbffd1a77eb30fd8f5df7df82
PAYKEY: 58aefe49c89c2bc9451b87076f653f6d
优酷斗地主
AppID 2091
AppKey 5815a167a9dc03cc
AppSecret ef20f86bd79dde3bcb2f85fbe5ce3f2f
PayKey 8d457b2df37b8475b111de426d95ba97
'''
add_global_item('youku_paykeys', {
    6: '62d48da6995a90d7e82fbdb5af877300',
    7: '58aefe49c89c2bc9451b87076f653f6d',
    8: '42a4e67ed166a358e76dd67c62edcc33',
    '691': '62d48da6995a90d7e82fbdb5af877300',
    '1131': 'a5c1229e9e89bdabbb8ba4a3012c18da',
    '2091': '8d457b2df37b8475b111de426d95ba97',
})
add_global_item('youku_appkeys', {
    6: '1814fe817d71731e',
    7: '73686281ad200fc2',
    8: 'fd2b34f2546974bf',
    '691': '1814fe817d71731e',
    '2091': '5815a167a9dc03cc',
})
add_global_item('youkudizhu_config', {
    'AppID': '2091',
    'AppKey': '5815a167a9dc03cc',
    'AppSecret': 'ef20f86bd79dde3bcb2f85fbe5ce3f2f',
    'PayKey': '8d457b2df37b8475b111de426d95ba97'
})

add_global_item('youku_prodids', {
    6: { # price unit: rmb fen
        'T50K'          : {'price':'500',    'name':'50000金币'},
        'T60K'          : {'price':'600',    'name':'60000金币'},
        'T80K'          : {'price':'800',    'name':'80000金币'},
        'T100K'         : {'price':'1000',   'name':'110000金币'},
        'T300K'         : {'price':'3000',   'name':'400000金币'},
        'T500K'         : {'price':'5000',   'name':'700000金币'},
        'T1M'           : {'price':'10000',  'name':'1500000金币'},
        'T3M'           : {'price':'30000',  'name':'4500000金币'},
        'T10M'          : {'price':'100000', 'name':'12000000金币'},
        'RAFFLE'        : {'price':'500',    'name':'50000金币'},
        'RAFFLE_NEW'    : {'price':'800',    'name':'80000金币'},
        'VOICE100'      : {'price':'100',    'name':'语音小喇叭'},
        'MOONKEY'       : {'price':'200',    'name':'月光之钥'},
        'MOONKEY3'      : {'price':'500',    'name':'月光之钥X3'},
        'ZHUANYUN'      : {'price':'500',    'name':'转运礼包'},
        'ZHUANYUN_BIG'  : {'price':'600',    'name':'转运大礼包'},
        'ZHUANYUN_MEZZO': {'price':'800',    'name':'8元转运礼包'},
        'VIP30'         : {'price':'3000',   'name':'VIP（30天）'},
        'PRIVILEGE_30'  : {'price':'10000',  'name':'会员（30天）'},
        'PVIP'          : {'price':'3000',   'name':'VIP普通礼包'},
        'PVIP_BIG'      : {'price':'5000',   'name':'VIP豪华礼包'},
        'TEHUI1Y'       : {'price':'100',    'name':'1元特惠'},
        'CARDMATCH10'   : {'price':'200',    'name':'参赛券X10'},
        'TY9999D0001001': {'price':'100',    'name':'1元特惠礼包',},
        'TY9999D0002001': {'price':'200',    'name':'20000金币',},
        'TY9999D0006001': {'price':'600',    'name':'60000金币',},
        'TY9999D0030001': {'price':'3000',   'name':'300000金币',},
        'TY9999D0050001': {'price':'5000',   'name':'500000金币',},
        'TY9999D0100001': {'price':'10000',  'name':'1000000金币',},
        'TY9999D0300001': {'price':'30000',  'name':'3000000金币',},
        'TY9999D1000001': {'price':'100000', 'name':'1000万金币',},
        'TY0006D0030002': {'price':'3000',   'name':'7天会员卡',},
        'TY0006D0100002': {'price':'10000',  'name':'30天会员卡',},
        'TY9999R0008001': {'price':'800',    'name':'80钻石',},
        'TY9999R0050001': {'price':'5000',   'name':'500钻石',},
        'TY9999R0100001': {'price':'10000',  'name':'1000钻石',},
        'TY0006D0002001': {'price':'200',    'name':'月光之钥',},
        'TY0006D0005001': {'price':'500',    'name':'月光之钥x3',},
        'TY0006D0002002': {'price':'200',    'name':'参赛券x10',},
        'TY0006D0000201': {'price':'20',     'name':'小喇叭x10',},
        'TY0006D0050002': {'price':'5000',   'name':'广播喇叭',},
        'TY0006D0100003': {'price':'10000',  'name':'改名卡',},
        'TY0006D0010001': {'price':'1000',   'name':'记牌器x7',},
        'TY9999D0008001': {'price':'800',    'name':'超值礼包',},
        'TY9999D0006002': {'price':'600',    'name':'6元转运礼包',},
        'TY9999D0008002': {'price':'800',    'name':'8元转运礼包',},
        },
    8: {
        'TEXAS_COIN1'   : {'price' : '200',    'name' : u'2万筹码'},
        'TEXAS_COIN6'   : {'price' : '500',    'name' : u'5万筹码'},
        'TEXAS_COIN_R6' : {'price' : '600',    'name' : u'6万筹码'},
        'TEXAS_COIN_R8' : {'price' : '800',    'name' : u'8万筹码'},
        'TEXAS_COIN2'   : {'price' : '1000',   'name' : u'10万筹码'},
        'TEXAS_COIN_R12': {'price' : '1200',   'name' : u'12万筹码'},
        'TEXAS_COIN3'   : {'price' : '3000',   'name' : u"30万筹码+额外赠3万" },
        'TEXAS_COIN4'   : {'price' : '5000',   'name' : u"50万筹码+额外赠5万" },
        'TEXAS_COIN5'   : {'price' : '10000',  'name' : u"100万筹码+额外赠15万" },
        'TEXAS_COIN7'   : {'price' : '30000',  'name' : u"300万筹码+额外赠45万" },
        'TEXAS_COIN8'   : {'price' : '100000', 'name' : u"1000万筹码+额外赠200万" },
        'TEXAS_COIN_LUCKY_R6'   : {'price' : '600',    'name' : u"10万" },
        'TEXAS_COIN_LUCKY_R30'  : {'price' : '3000',   'name' : u"33万" },
        'TEXAS_COIN_LUCKY_R50'  : {'price' : '5000',   'name' : u"55万" },
        'TEXAS_COIN_LUCKY_R100' : {'price' : '10000',  'name' : u"115万" },
        'TEXAS_COIN_LUCKY_R300' : {'price' : '30000',  'name' : u"345万" },
        'TEXAS_COIN_LUCKY_R1000': {'price' : '100000', 'name' : u"1200万" },
        'TEXAS_VIP1' : {'price' : '3000',   'name' : '会员(30天)'},
        'TEXAS_VIP2' : {'price' : '10000',  'name' : '会员(30天)'},
        'TEXAS_VIP3' : {'price' : '30000',  'name' : '会员(30天)'},
        'TEXAS_VIP4' : {'price' : '100000', 'name' : '会员(30天)'},
        'TEXAS_ITEM_SEND_LED'    : {'price' : '5000', 'name' : '喇叭'},
        'TEXAS_ITEM_RENAME_CARD' : {'price' : '10000', 'name' : '改名卡'},
    },
    7: {
        "C2"    : {'name': u"2万金", 'price': "200"},
        "C6"    : {'name': u"6万金", 'price': "600"},
        "C5"    : {'name': u"5万金", 'price': "500"},
        "C8"    : {'name': u"8万金", 'price': "800"},
        "C10"   : {'name': u"10万金",   'price': "1000"},
        "C30"   : {'name': u"30万金",   'price': "3000"},
        "C50"   : {'name': u"50万金",   'price': "5000"},
        "C100"  : {'name': u"100万金",  'price': "10000"},
        "C300"  : {'name': u"300万金",  'price': "30000"},
        "C1000" : {'name': u"1000万金", 'price': "100000"},
        "C30_MEMBER" : {'name': u"周会员, 立得30万, 每天再送3万",  'price': "3000"},
        "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "10000"},
        "C5_RAFFLE"  : {'name': u"5元礼包", 'price': "500"},
        "C6_RAFFLE"  : {'name': u"6元礼包", 'price': "600"},
        "C8_RAFFLE"  : {'name': u"8元礼包", 'price': "800"},
        "C5_LUCKY"   : {'name': u"5元转运礼包",  'price': "500"},
        "C8_LUCKY"   : {'name': u"8元转运礼包",  'price': "800"},
        "C10_LUCKY"  : {'name': u"10元转运礼包", 'price': "1000"},
    }
})

'''百度多酷配置
地主 Key： NKPBtbkmvgYmfnk2gPWC6P7kQfNke8Yj '''
add_global_item('duoku_paykeys', {
    '3230030': 'NKPBtbkmvgYmfnk2gPWC6P7kQfNke8Yj',
    '7328977': 'VpPLGHYc7VculZG6jypGw52bAPP7kzvs',
    '6989306': 'gcLaNCXEQgTyAbb9Z8VeiRW2R5c39nxW',
    '6989420': 'eLDCK6maW1WNgK4crpajr56LQZ8WDTfG',
    '7454600': 'Dw9BHWGcNgDpUvTohm1N9w7h2sInVxQl',#天天德州
    '7117112': 'byzrXE0G57uNwMALGy3mUlmjGs98uEvU',#欢乐途游麻将
    '7117106': 'Taen66GIvnDSnz1XDTfRXDjtlwZ0QLiM',#途游麻将
    '6989810': 'g0LodDWpwcQDT8X0kpT6QwfUsvEu6IL3',#四川麻将
    '6989707': 'l293eQwh3ZSGTTSZo1ATCgx5AgqhYA37',#单机麻将
    '7498964': 'tKKvnReRGPr2qjR6EBjTipFV7GTv3d2H',#跑胡子
    '7566568': 'iVVCyVgbpD3meSrHzf7GtHKeZQlk7nqO',#途游斗地主
    '8296115': '9LEhLMyTERyB891bRjyZ2SN9o6XZgstn',#青岛棋牌
})

add_global_item('duoku_prodids', {
    6: {
        'TY9999D0006001': {
                            'mPropsId':'3327',
                            'ydmm':{'paycode':'30000845198512'},
                          },
        'TY9999D0008002': {
                            'mPropsId':'3330',
                            'ydmm':{'paycode':'30000845198510'},
                          },
        'TY9999D0008001': {
                            'mPropsId':'3329',
                            'ydmm':{'paycode':'30000845198511'},
                          },
        'TY9999R0008001': {
                            'mPropsId':'3328',
                            'ydmm':{'paycode':'30000845198513'},
                          },
        'TY9999D0030001': {
                            'mPropsId':'3583',
                          },

        'TY9999D0050001': {
                            'mPropsId':'3584',
                          },
        'TY9999D0100001': {
                            'mPropsId':'3585',
                          },
        'TY9999D0300001': {
                            'mPropsId':'3586',
                          },
        'TY9999D1000001': {
                            'mPropsId':'3587',
                          },
        'TY0006D0030002': {
                            'mPropsId':'3588',
                          },
        'TY0006D0100002': {
                            'mPropsId':'3589',
                          },
        'TY9999R0100001': {
                            'mPropsId':'5856',
                          },
        'T60K'         : {'price':'6',    'name':'60000金币'},
        'T80K'         : {'price':'8',    'name':'80000金币',     'feecode':'002'},
        'T100K'        : {'price':'10',   'name':'110000金币',    'feecode':'003'},
        'T300K'        : {'price':'30',   'name':'400000金币'},
        'T500K'        : {'price':'50',   'name':'700000金币'},
        'T1M'          : {'price':'100',  'name':'1500000金币'},
        'T3M'          : {'price':'300',  'name':'4500000金币'},
        'T10M'         : {'price':'1000', 'name':'12000000金币'},
        'RAFFLE'       : {'price':'5',    'name':'50000金币'},
        'RAFFLE_NEW'   : {'price':'8',    'name':'80000金币',     'feecode':'009'},
        'VOICE100'     : {'price':'1',    'name':'语音小喇叭',    'feecode':'006'},
        'MOONKEY'      : {'price':'2',    'name':'月光之钥',      'feecode':'004'},
        'MOONKEY3'     : {'price':'5',    'name':'月光之钥X3',    'feecode':'005'},
        'ZHUANYUN'     : {'price':'5',    'name':'转运礼包'},
        'ZHUANYUN_BIG' : {'price':'6',    'name':'转运大礼包',    'feecode':'008'},
        'VIP30'        : {'price':'30',   'name':'VIP（30天）'},
        'PRIVILEGE_30' : {'price':'100',  'name':'会员（30天）'},
        'PVIP'         : {'price':'30',   'name':'VIP普通礼包'},
        'PVIP_BIG'     : {'price':'50',   'name':'VIP豪华礼包'},
        'TEHUI1Y'      : {'price':'1',    'name':'1元特惠'},
        'CARDMATCH10'  : {'price':'2',    'name':'参赛券X10',     'feecode':'007'},
    },
    8: {
        'TEXAS_COIN1'   : {'price' : '2',    'name' : u'2万筹码'},
        'TEXAS_COIN6'   : {'price' : '5',    'name' : u'5万筹码'},
        'TEXAS_COIN_R6' : {'price' : '6',    'name' : u'6万筹码'},
        'TEXAS_COIN_R8' : {'price' : '8',    'name' : u'8万筹码'},
        'TEXAS_COIN2'   : {'price' : '10',   'name' : u'10万筹码'},
        'TEXAS_COIN_R12': {'price' : '10',   'name' : u'12万筹码'},
        'TEXAS_COIN3'   : {'price' : '30',   'name' : u"30万筹码+额外赠3万" },
        'TEXAS_COIN4'   : {'price' : '50',   'name' : u"50万筹码+额外赠5万" },
        'TEXAS_COIN5'   : {'price' : '100',  'name' : u"100万筹码+额外赠15万" },
        'TEXAS_COIN7'   : {'price' : '300',  'name' : u"300万筹码+额外赠45万" },
        'TEXAS_COIN8'   : {'price' : '1000', 'name' : u"1000万筹码+额外赠200万" },
        'TEXAS_COIN_LUCKY_R6'   : {'price' : '6',    'name' : u"10万" },
        'TEXAS_COIN_LUCKY_R30'  : {'price' : '30',   'name' : u"33万" },
        'TEXAS_COIN_LUCKY_R50'  : {'price' : '50',   'name' : u"55万" },
        'TEXAS_COIN_LUCKY_R100' : {'price' : '100',  'name' : u"115万" },
        'TEXAS_COIN_LUCKY_R300' : {'price' : '300',  'name' : u"345万" },
        'TEXAS_COIN_LUCKY_R1000': {'price' : '1000', 'name' : u"1200万" },
        'TEXAS_VIP1' : {'price' : '30',   'name' : '会员(30天)'},
        'TEXAS_VIP2' : {'price' : '100',  'name' : '会员(30天)'},
        'TEXAS_VIP3' : {'price' : '300',  'name' : '会员(30天)'},
        'TEXAS_VIP4' : {'price' : '1000', 'name' : '会员(30天)'},
        'TEXAS_ITEM_SEND_LED'    : {'price' : '50', 'name' : '喇叭'},
        'TEXAS_ITEM_RENAME_CARD' : {'price' : '100', 'name' : '改名卡'},
    },
    7: {
        "C2"    : {'name': u"2万金", 'price': "2"},
        "C6"    : {'name': u"6万金", 'price': "6"},
        "C5"    : {'name': u"5万金", 'price': "5"},
        "C8"    : {'name': u"8万金", 'price': "8"},
        "C10"   : {'name': u"10万金",   'price': "10"},
        "C30"   : {'name': u"30万金",   'price': "30"},
        "C50"   : {'name': u"50万金",   'price': "50"},
        "C100"  : {'name': u"100万金",  'price': "100"},
        "C300"  : {'name': u"300万金",  'price': "300"},
        "C1000" : {'name': u"1000万金", 'price': "1000"},
        "C30_MEMBER" : {'name': u"周会员, 立得30万, 每天再送3万",  'price': "30"},
        "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "100"},
        "C5_RAFFLE"  : {'name': u"5元礼包", 'price': "5"},
        "C6_RAFFLE"  : {'name': u"6元礼包", 'price': "6"},
        "C8_RAFFLE"  : {'name': u"8元礼包", 'price': "8"},
        "C5_LUCKY"   : {'name': u"5元转运礼包",  'price': "5"},
        "C8_LUCKY"   : {'name': u"8元转运礼包",  'price': "8"},
        "C10_LUCKY"  : {'name': u"10元转运礼包", 'price': "10"},
    },
    '7566568': {
        'TY9999R0000101':{'mPropsId':14839, 'name':'1钻石'},
        'TY9999D0001003':{'mPropsId':14841, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':14842, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':14843, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':14844, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':14845, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':14845, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':14846, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':14847, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':14847, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':14848, 'name':'转运限量特价礼包'},
        'TY9999D0008025':{'mPropsId':14849, 'name':'高手限量特价礼包'},
        'TY9999D0012003':{'mPropsId':14851, 'name':'30天会员'},
        'TY9999D0030001':{'mPropsId':14852, 'name':'36万金币'},
        'TY9999D0030011':{'mPropsId':14853, 'name':'30元转运礼包'},
        'TY9999D0030012':{'mPropsId':14854, 'name':'30元高手礼包'},
        'TY9999R0050001':{'mPropsId':14855, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':14856, 'name':'65万金币'},
        'TY9999D0050007':{'mPropsId':14857, 'name':'50元转运礼包'},
        'TY9999D0050008':{'mPropsId':14858, 'name':'50元高手礼包'},
        'TY9999D0100001':{'mPropsId':14859, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':14860, 'name':'1000钻石'},
        'TY9999D0100011':{'mPropsId':14861, 'name':'100元转运礼包'},
        'TY9999D0100012':{'mPropsId':14862, 'name':'100元高手礼包'},
        'TY9999D0300001':{'mPropsId':14863, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':14864, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':14865, 'name':'100000金币'},
        'TY9999R0010001':{'mPropsId':14866, 'name':'100钻石'},
        'TY9999R0030001':{'mPropsId':14867, 'name':'300钻石'},
    },
    'com.tuyoo.doudizhu.bd': {
        'TY9999R0000101':{'mPropsId':10426, 'name':'1钻石'},
        'TY9999D0001003':{'mPropsId':10427, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10428, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10429, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10430, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10431, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':10431, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':10432, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':10433, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':10433, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10434, 'name':'转运限量特价礼包'},
        'TY9999D0008025':{'mPropsId':10435, 'name':'高手限量特价礼包'},
        'TY9999D0012003':{'mPropsId':10436, 'name':'30天会员'},
        'TY9999D0030001':{'mPropsId':10437, 'name':'36万金币'},
        'TY9999D0030011':{'mPropsId':10438, 'name':'30元转运礼包'},
        'TY9999D0030012':{'mPropsId':10439, 'name':'30元高手礼包'},
        'TY9999R0050001':{'mPropsId':10440, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':10441, 'name':'65万金币'},
        'TY9999D0050007':{'mPropsId':10442, 'name':'50元转运礼包'},
        'TY9999D0050008':{'mPropsId':10443, 'name':'50元高手礼包'},
        'TY9999D0100001':{'mPropsId':10444, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':10445, 'name':'1000钻石'},
        'TY9999D0100011':{'mPropsId':10446, 'name':'100元转运礼包'},
        'TY9999D0100012':{'mPropsId':10447, 'name':'100元高手礼包'},
        'TY9999D0300001':{'mPropsId':10448, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10449, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':10450, 'name':'100000金币'},
        'TY9999R0010001':{'mPropsId':10532, 'name':'100钻石'},
        'TY9999R0030001':{'mPropsId':10531, 'name':'300钻石'},
        'TY9999R0200001':{'mPropsId':16773, 'name':'2000钻石'},
        'TY9999R0300001':{'mPropsId':16775, 'name':'3000钻石'},
        'TY9999R0600001':{'mPropsId':16776, 'name':'6000钻石'},
    },
    'com.tuyoo.doudizhu.main': {
        'TY9999R0000101':{'mPropsId':10426, 'name':'1钻石'},
        'TY9999D0001003':{'mPropsId':10427, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10428, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10429, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10430, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10431, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':10431, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':10432, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':10433, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':10433, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10434, 'name':'转运限量特价礼包'},
        'TY9999D0008025':{'mPropsId':10435, 'name':'高手限量特价礼包'},
        'TY9999D0012003':{'mPropsId':10436, 'name':'30天会员'},
        'TY9999D0030001':{'mPropsId':10437, 'name':'36万金币'},
        'TY9999D0030011':{'mPropsId':10438, 'name':'30元转运礼包'},
        'TY9999D0030012':{'mPropsId':10439, 'name':'30元高手礼包'},
        'TY9999R0050001':{'mPropsId':10440, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':10441, 'name':'65万金币'},
        'TY9999D0050007':{'mPropsId':10442, 'name':'50元转运礼包'},
        'TY9999D0050008':{'mPropsId':10443, 'name':'50元高手礼包'},
        'TY9999D0100001':{'mPropsId':10444, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':10445, 'name':'1000钻石'},
        'TY9999D0100011':{'mPropsId':10446, 'name':'100元转运礼包'},
        'TY9999D0100012':{'mPropsId':10447, 'name':'100元高手礼包'},
        'TY9999D0300001':{'mPropsId':10448, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10449, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':10450, 'name':'100000金币'},
        'TY9999R0010001':{'mPropsId':10532, 'name':'100钻石'},
        'TY9999R0030001':{'mPropsId':10531, 'name':'300钻石'},
        'TY9999D0006001':{'mPropsId':14820, 'name':'60000金币'},
        'TY9999D0008039':{'mPropsId':14828, 'name':'8元VIP特惠礼包'},
        'TY9999D0050012':{'mPropsId':14833, 'name':'50元VIP特惠礼包'},
        'TY9999D0100022':{'mPropsId':14837, 'name':'100元VIP特惠礼包'},
        'TY9999R0200001':{'mPropsId':16779, 'name':'2000钻石'},
        'TY9999R0300001':{'mPropsId':16780, 'name':'3000钻石'},
        'TY9999R0600001':{'mPropsId':16781, 'name':'6000钻石'},
    },
    'com.doudizhu.mainhuanle.baidu': {
        'TY9999R0000101':{'mPropsId':10451,'name':'1钻石', },
        'TY9999D0001003':{'mPropsId':10452, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10453, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10454, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10455, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10456, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':10456, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':10457, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':10458, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':10458, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10459, 'name':'转运限量特价礼包'},
        'TY9999D0008025':{'mPropsId':10460, 'name':'高手限量特价礼包'},
        'TY9999D0012003':{'mPropsId':10461, 'name':'30天会员'},
        'TY9999D0030001':{'mPropsId':10462, 'name':'36万金币'},
        'TY9999D0030011':{'mPropsId':10463, 'name':'30元转运礼包'},
        'TY9999D0030012':{'mPropsId':10464, 'name':'30元高手礼包'},
        'TY9999R0050001':{'mPropsId':10465, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':10466, 'name':'65万金币'},
        'TY9999D0050007':{'mPropsId':10467, 'name':'50元转运礼包'},
        'TY9999D0050008':{'mPropsId':10468, 'name':'50元高手礼包'},
        'TY9999D0100001':{'mPropsId':10469, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':10470, 'name':'1000钻石'},
        'TY9999D0100011':{'mPropsId':10471, 'name':'100元转运礼包'},
        'TY9999D0100012':{'mPropsId':10472, 'name':'100元高手礼包'},
        'TY9999D0300001':{'mPropsId':10473, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10474, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':10475, 'name':'100000金币'},
        'TY9999R0200001':{'mPropsId':16782, 'name':'2000钻石'},
        'TY9999R0300001':{'mPropsId':16783, 'name':'3000钻石'},
        'TY9999R0600001':{'mPropsId':16784, 'name':'6000钻石'},
    },
    "com.tuyoo.baohuang.baidu": {
        'TY9999D0001003':{'mPropsId':10507, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10511, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10512, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10513, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10514, 'name':'80000金币'},
        'TY9999D0008001':{'mPropsId':10515, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10516, 'name':'转运限量特价礼包'},
        'TY9999R0008005':{'mPropsId':10517, 'name':'80钻石'},
        'TY9999R0050001':{'mPropsId':10518, 'name':'500钻石'},
        'TY9999R0100001':{'mPropsId':10519, 'name':'1000钻石'},
        'TY9999D0010001':{'mPropsId':10520, 'name':'100000金币'},
        'TY9999D0030001':{'mPropsId':10521, 'name':'36万金币 '},
        'TY9999D0050001':{'mPropsId':10522, 'name':'65万金币'},
        'TY9999D0100001':{'mPropsId':10523, 'name':'150万金币'},
        'TY9999D0300001':{'mPropsId':10524, 'name':'650万金币'},
        'TY9999D1000001':{'mPropsId':10525, 'name':'2000万金币'},
        'TY9999D0008025':{'mPropsId':14433, 'name':'高手限量特价礼包'},
    },
    'com.tiantian.dezhoupoker.baidu': {
        'TY9999R0000101':{'mPropsId':10294,'name':'1钻石', },
        'TY9999D0001003':{'mPropsId':10295, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10296, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10297, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10298, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10299, 'name':'80000金币'},
        'TY9999D0008001':{'mPropsId':10300, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10301, 'name':'转运限量特价礼包'},
        'TY9999R0008005':{'mPropsId':10302, 'name':'80钻石'},
        'TY9999D0010001':{'mPropsId':10303, 'name':'100000金币'},
        'TY9999D0030001':{'mPropsId':10304, 'name':'36万金币'},
        'TY9999D0030024':{'mPropsId':10304, 'name':'36万金币'},
        'TY9999D0050001':{'mPropsId':10305, 'name':'65万金币'},
        'TY9999D0100001':{'mPropsId':10306, 'name':'150万金币'},
        'TY9999D0300001':{'mPropsId':10307, 'name':'500万金币'},
        'TY9999D0300004':{'mPropsId':10307, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10308, 'name':'2000万金币'},
        'TY9999D1000012':{'mPropsId':10308, 'name':'2000万金币'},
        'TY9999R0050001':{'mPropsId':10309, 'name':'500钻石'},
        'TY9999D5000001':{'mPropsId':10310, 'name':'1亿金币'},
        'TY9999D0100019':{'mPropsId':10311, 'name':'德州至尊月卡'},
        'TY9999D1000011':{'mPropsId':12519, 'name':'1000万金币'},
        'TY9999D0300003':{'mPropsId':12520, 'name':'300万金币'},
        'TY9999D0100020':{'mPropsId':12521, 'name':'100万金币'},
        'TY9999D0050010':{'mPropsId':12522, 'name':'50万金币'},
        'TY9999D0030023':{'mPropsId':12523, 'name':'30万金币'},
        'TY9999D0008038':{'mPropsId':14630, 'name':'80000金币+500魅力值'},
        'TY9999D0030024':{'mPropsId':14631, 'name':'36万金币+千万金币赛门票'},
        'TY9999D0050011':{'mPropsId':14632, 'name':'65万金币'},
        'TY9999D0100021':{'mPropsId':14633, 'name':'150万金币'},
        'TY9999D0300004':{'mPropsId':14634, 'name':'500万金币+2亿猎人赛门票'},
        'TY9999D1000012':{'mPropsId':14635, 'name':'2000万金币+豪华门票礼包'},
        'TY9999D1000013':{'mPropsId':15031, 'name':'德州超级月卡'},
    },
    #单机麻将
    'com.mahjong.danji.baidu': {
        'TY9999R0000101':{'mPropsId':10788,'name':'1钻石', },
        'TY9999D0001003':{'mPropsId':10790, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10792, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10794, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10795, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10797, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':10797, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':10799, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':10802, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':10802, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10803, 'name':'转运限量特价礼包'},
        'TY9999D0008025':{'mPropsId':10804, 'name':'高手限量特价礼包'},
        'TY9999D0012003':{'mPropsId':10805, 'name':'30天会员'},
        'TY9999D0030001':{'mPropsId':10806, 'name':'36万金币'},
        'TY9999D0030011':{'mPropsId':10808, 'name':'30元转运礼包'},
        'TY9999D0030012':{'mPropsId':10807, 'name':'30元高手礼包'},
        'TY9999R0050001':{'mPropsId':10809, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':10810, 'name':'65万金币'},
        'TY9999D0050007':{'mPropsId':10811, 'name':'50元转运礼包'},
        'TY9999D0050008':{'mPropsId':10812, 'name':'50元高手礼包'},
        'TY9999D0100001':{'mPropsId':10813, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':10814, 'name':'1000钻石'},
        'TY9999D0100011':{'mPropsId':10815, 'name':'100元转运礼包'},
        'TY9999D0100012':{'mPropsId':10816, 'name':'100元高手礼包'},
        'TY9999D0300001':{'mPropsId':10817, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10818, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':10819, 'name':'100000金币'},
    },
     #四川麻将
    'com.tuyoo.scmahjong.baidu': {
        'TY9999R0000101':{'mPropsId':10820,'name':'1钻石', },
        'TY9999D0001003':{'mPropsId':10821, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10822, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10823, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10824, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10825, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':10825, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':10826, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':10827, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':10827, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10828, 'name':'转运限量特价礼包'},
        'TY9999D0008025':{'mPropsId':10829, 'name':'高手限量特价礼包'},
        'TY9999D0012003':{'mPropsId':10830, 'name':'30天会员'},
        'TY9999D0030001':{'mPropsId':10831, 'name':'36万金币'},
        'TY9999D0030011':{'mPropsId':10832, 'name':'30元转运礼包'},
        'TY9999D0030012':{'mPropsId':10833, 'name':'30元高手礼包'},
        'TY9999R0050001':{'mPropsId':10834, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':10835, 'name':'65万金币'},
        'TY9999D0050007':{'mPropsId':10836, 'name':'50元转运礼包'},
        'TY9999D0050008':{'mPropsId':10837, 'name':'50元高手礼包'},
        'TY9999D0100001':{'mPropsId':10838, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':10839, 'name':'1000钻石'},
        'TY9999D0100011':{'mPropsId':10840, 'name':'100元转运礼包'},
        'TY9999D0100012':{'mPropsId':10841, 'name':'100元高手礼包'},
        'TY9999D0300001':{'mPropsId':10842, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10843, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':10845, 'name':'100000金币'},
    },
    #途游麻将
    'com.tuyoo.mahjong.baidu': {
        'TY9999R0000101':{'mPropsId':10886,'name':'1钻石', },
        'TY9999D0001003':{'mPropsId':10887, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10888, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10889, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10890, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10891, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':10891, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':10892, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':10893, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':10893, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10894, 'name':'转运限量特价礼包'},
        'TY9999D0008025':{'mPropsId':10895, 'name':'高手限量特价礼包'},
        'TY9999D0012003':{'mPropsId':10896, 'name':'30天会员'},
        'TY9999D0030001':{'mPropsId':10897, 'name':'36万金币'},
        'TY9999D0030011':{'mPropsId':10931, 'name':'30元转运礼包'},
        'TY9999D0030012':{'mPropsId':10932, 'name':'30元高手礼包'},
        'TY9999R0050001':{'mPropsId':10933, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':10934, 'name':'65万金币'},
        'TY9999D0050007':{'mPropsId':10935, 'name':'50元转运礼包'},
        'TY9999D0050008':{'mPropsId':10936, 'name':'50元高手礼包'},
        'TY9999D0100001':{'mPropsId':10937, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':10938, 'name':'1000钻石'},
        'TY9999D0100011':{'mPropsId':10939, 'name':'100元转运礼包'},
        'TY9999D0100012':{'mPropsId':10940, 'name':'100元高手礼包'},
        'TY9999D0300001':{'mPropsId':10941, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10942, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':10943, 'name':'100000金币'},
    },
    #欢乐途游麻将
    'com.mahjong.majiang.baidu': {
        'TY9999R0000101':{'mPropsId':10944,'name':'1钻石', },
        'TY9999D0001003':{'mPropsId':10945, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10946, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10947, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10948, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10949, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':10949, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':10950, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':10951, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':10951, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10952, 'name':'转运限量特价礼包'},
        'TY9999D0008025':{'mPropsId':10953, 'name':'高手限量特价礼包'},
        'TY9999D0012003':{'mPropsId':10954, 'name':'30天会员'},
        'TY9999D0030001':{'mPropsId':10955, 'name':'36万金币'},
        'TY9999D0030011':{'mPropsId':10956, 'name':'30元转运礼包'},
        'TY9999D0030012':{'mPropsId':10957, 'name':'30元高手礼包'},
        'TY9999R0050001':{'mPropsId':10958, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':10959, 'name':'65万金币'},
        'TY9999D0050007':{'mPropsId':10960, 'name':'50元转运礼包'},
        'TY9999D0050008':{'mPropsId':10961, 'name':'50元高手礼包'},
        'TY9999D0100001':{'mPropsId':10962, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':10963, 'name':'1000钻石'},
        'TY9999D0100011':{'mPropsId':10964, 'name':'100元转运礼包'},
        'TY9999D0100012':{'mPropsId':10965, 'name':'100元高手礼包'},
        'TY9999D0300001':{'mPropsId':10966, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10967, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':10968, 'name':'100000金币'},
    },
    #跑胡子
    'com.tuyoo.paohuzi.baidu': {
        'TY9999D0001003':{'mPropsId':10626, 'name':'1天会员'},
        'TY9999D0002001':{'mPropsId':10627, 'name':'20000金币'},
        'TY9999D0005003':{'mPropsId':10628, 'name':'50000金币'},
        'TY9999D0006016':{'mPropsId':10629, 'name':'60000金币'},
        'TY9999D0006001':{'mPropsId':10629, 'name':'60000金币'},
        'TY9999D0008005':{'mPropsId':10630, 'name':'80000金币'},
        'TY9999D0008027':{'mPropsId':10630, 'name':'80000金币'},
        'TY9999R0008005':{'mPropsId':10633, 'name':'80钻石'},
        'TY9999D0008001':{'mPropsId':10631, 'name':'8元超值礼包'},
        'TY9999D0008034':{'mPropsId':10631, 'name':'8元超值礼包'},
        'TY9999D0008026':{'mPropsId':10632, 'name':'转运限量特价礼包'},
        'TY9999D0030001':{'mPropsId':10637, 'name':'36万金币'},
        'TY9999D0030024':{'mPropsId':10437, 'name':'36万金币'},
        'TY9999R0050001':{'mPropsId':10634, 'name':'500钻石'},
        'TY9999D0050001':{'mPropsId':10638, 'name':'65万金币'},
        'TY9999D0100001':{'mPropsId':10639, 'name':'150万金币'},
        'TY9999R0100001':{'mPropsId':10635, 'name':'1000钻石'},
        'TY9999D0300001':{'mPropsId':10640, 'name':'500万金币'},
        'TY9999D1000001':{'mPropsId':10641, 'name':'2000万金币'},
        'TY9999D0010001':{'mPropsId':10636, 'name':'100000金币'},
    },
    #青岛棋牌
    'com.tuyoo.qingdaoqipai.bd': {
        'TY9999D0002001':{'mPropsId':17097, 'name': '20000金币'},
        'TY9999D0005003':{'mPropsId':17098, 'name': '50000金币'},
        'TY9999D0006016':{'mPropsId':17099, 'name': '60000金币'},
        'TY9999D0008001':{'mPropsId':17100, 'name': '8元超值礼包'},
        'TY9999D0008005':{'mPropsId':17101, 'name': '80000金币'},
        'TY9999D0008025':{'mPropsId':17102, 'name': '高手限量特价礼包'},
        'TY9999D0008026':{'mPropsId':17103, 'name': '转运限量特价礼包'},
        'TY9999D0010001':{'mPropsId':17104, 'name': '100000金币'},
        'TY9999D0030001':{'mPropsId':17105, 'name': '36万金币'},
        'TY9999D0030011':{'mPropsId':17106, 'name': '30元转运礼包'},
        'TY9999D0030012':{'mPropsId':17107, 'name': '30元高手礼包'},
        'TY9999D0050001':{'mPropsId':17108, 'name': '65万金币'},
        'TY9999D0050007':{'mPropsId':17109, 'name': '50元转运礼包'},
        'TY9999D0050008':{'mPropsId':17110, 'name': '50元高手礼包'},
        'TY9999D0100001':{'mPropsId':17111, 'name': '150万金币'},
        'TY9999D0100011':{'mPropsId':17112, 'name': '100元转运礼包'},
        'TY9999D0100012':{'mPropsId':17113, 'name': '100元高手礼包'},
        'TY9999D0300001':{'mPropsId':17114, 'name': '500万金币'},
        'TY9999D1000001':{'mPropsId':17115, 'name': '2000万金币'},
        'TY9999R0008005':{'mPropsId':17116, 'name': '80钻石'},
        'TY9999R0030001':{'mPropsId':17117, 'name': '300钻石'},
        'TY9999R0050001':{'mPropsId':17118, 'name': '500钻石'},
        'TY9999R0100001':{'mPropsId':17119, 'name': '1000钻石'},
    },
    #中国象棋
    'com.example.chinesechess.baidu': {
        'TY9999D0002001':{'mPropsId':18161, 'name': '20000金币'},
        'TY9999D0005003':{'mPropsId':18162, 'name': '50000金币'},
        'TY9999D0006016':{'mPropsId':18163, 'name': '60000金币'},
        'TY9999D0008001':{'mPropsId':18179, 'name': '8元超值礼包'},
        'TY9999D0008005':{'mPropsId':18164, 'name': '80000金币'},
        'TY9999D0008025':{'mPropsId':18180, 'name': '高手限量特价礼包'},
        'TY9999D0008026':{'mPropsId':18181, 'name': '转运限量特价礼包'},
        'TY9999D0010001':{'mPropsId':18165, 'name': '100000金币'},
        'TY9999D0030001':{'mPropsId':18166, 'name': '36万金币'},
        'TY9999D0030011':{'mPropsId':18182, 'name': '30元转运礼包'},
        'TY9999D0030012':{'mPropsId':18183, 'name': '30元高手礼包'},
        'TY9999D0050001':{'mPropsId':18167, 'name': '65万金币'},
        'TY9999D0050007':{'mPropsId':18184, 'name': '50元转运礼包'},
        'TY9999D0050008':{'mPropsId':18185, 'name': '50元高手礼包'},
        'TY9999D0100001':{'mPropsId':18168, 'name': '150万金币'},
        'TY9999D0100011':{'mPropsId':18186, 'name': '100元转运礼包'},
        'TY9999D0100012':{'mPropsId':18187, 'name': '100元高手礼包'},
        'TY9999D0300001':{'mPropsId':18169, 'name': '500万金币'},
        'TY9999D1000001':{'mPropsId':18170, 'name': '2000万金币'},
        'TY9999R0008005':{'mPropsId':18172, 'name': '80钻石'},
        'TY9999R0030001':{'mPropsId':18188, 'name': '300钻石'},
        'TY9999R0050001':{'mPropsId':18173, 'name': '500钻石'},
        'TY9999R0100001':{'mPropsId':18189, 'name': '1000钻石'},
        },

})



'''豆盟配置
地主 Key： DdtyMUIWJ4BpdCKJxKFF0 '''
add_global_item('doumeng_paykeys', {
    6: 'DdtyMUIWJ4BpdCKJxKFF0',
})

add_global_item('doumeng_prodids', {
    6: {
        'T50K'         : {'price':'5',    'name':'50000金币',     'feecode':'001'},
        'T60K'         : {'price':'6',    'name':'60000金币',     'feecode':'015'},
        'T80K'         : {'price':'8',    'name':'80000金币',     'feecode':'002'},
        'T100K'        : {'price':'10',   'name':'110000金币',    'feecode':'003'},
        'T300K'        : {'price':'30',   'name':'400000金币',    'feecode':'010'},
        'T500K'        : {'price':'50',   'name':'700000金币',    'feecode':'011'},
        'T1M'          : {'price':'100',  'name':'1500000金币',   'feecode':'012'},
        'T3M'          : {'price':'300',  'name':'4500000金币',   'feecode':'013'},
        'T10M'         : {'price':'1000', 'name':'12000000金币',  'feecode':'014'},
        'RAFFLE'       : {'price':'5',    'name':'50000金币',     'feecode':'016'},
        'RAFFLE_NEW'   : {'price':'8',    'name':'80000金币',     'feecode':'009'},
        'VOICE100'     : {'price':'1',    'name':'语音小喇叭',    'feecode':'006'},
        'MOONKEY'      : {'price':'2',    'name':'月光之钥',      'feecode':'004'},
        'MOONKEY3'     : {'price':'5',    'name':'月光之钥X3',    'feecode':'005'},
        'ZHUANYUN'     : {'price':'5',    'name':'转运礼包',      'feecode':'017'},
        'ZHUANYUN_BIG' : {'price':'6',    'name':'转运大礼包',    'feecode':'008'},
        'ZHUANYUN_MEZZO':{'price':'8',    'name':'8元转运礼包',   'feecode':'023'},
        'VIP30'        : {'price':'30',   'name':'VIP（30天）',   'feecode':'018'},
        'PRIVILEGE_30' : {'price':'100',  'name':'会员（30天）',  'feecode':'019'},
        'PVIP'         : {'price':'30',   'name':'VIP普通礼包',   'feecode':'020'},
        'PVIP_BIG'     : {'price':'50',   'name':'VIP豪华礼包',   'feecode':'021'},
        'TEHUI1Y'      : {'price':'1',    'name':'1元特惠',       'feecode':'022'},
        'CARDMATCH10'  : {'price':'2',    'name':'参赛券X10',     'feecode':'007'},
    },
    8: {
        'TEXAS_COIN1'   : {'price' : '2',    'name' : u'2万筹码'},
        'TEXAS_COIN6'   : {'price' : '5',    'name' : u'5万筹码'},
        'TEXAS_COIN_R6' : {'price' : '6',    'name' : u'6万筹码'},
        'TEXAS_COIN_R8' : {'price' : '8',    'name' : u'8万筹码'},
        'TEXAS_COIN2'   : {'price' : '10',   'name' : u'10万筹码'},
        'TEXAS_COIN_R12': {'price' : '10',   'name' : u'12万筹码'},
        'TEXAS_COIN3'   : {'price' : '30',   'name' : u"30万筹码+额外赠3万" },
        'TEXAS_COIN4'   : {'price' : '50',   'name' : u"50万筹码+额外赠5万" },
        'TEXAS_COIN5'   : {'price' : '100',  'name' : u"100万筹码+额外赠15万" },
        'TEXAS_COIN7'   : {'price' : '300',  'name' : u"300万筹码+额外赠45万" },
        'TEXAS_COIN8'   : {'price' : '1000', 'name' : u"1000万筹码+额外赠200万" },
        'TEXAS_COIN_LUCKY_R6'   : {'price' : '6',    'name' : u"10万" },
        'TEXAS_COIN_LUCKY_R30'  : {'price' : '30',   'name' : u"33万" },
        'TEXAS_COIN_LUCKY_R50'  : {'price' : '50',   'name' : u"55万" },
        'TEXAS_COIN_LUCKY_R100' : {'price' : '100',  'name' : u"115万" },
        'TEXAS_COIN_LUCKY_R300' : {'price' : '300',  'name' : u"345万" },
        'TEXAS_COIN_LUCKY_R1000': {'price' : '1000', 'name' : u"1200万" },
        'TEXAS_VIP1' : {'price' : '30',   'name' : '会员(30天)'},
        'TEXAS_VIP2' : {'price' : '100',  'name' : '会员(30天)'},
        'TEXAS_VIP3' : {'price' : '300',  'name' : '会员(30天)'},
        'TEXAS_VIP4' : {'price' : '1000', 'name' : '会员(30天)'},
        'TEXAS_ITEM_SEND_LED'    : {'price' : '50', 'name' : '喇叭'},
        'TEXAS_ITEM_RENAME_CARD' : {'price' : '100', 'name' : '改名卡'},
    },
    7: {
        "C2"    : {'name': u"2万金", 'price': "2"},
        "C6"    : {'name': u"6万金", 'price': "6"},
        "C5"    : {'name': u"5万金", 'price': "5"},
        "C8"    : {'name': u"8万金", 'price': "8"},
        "C10"   : {'name': u"10万金",   'price': "10"},
        "C30"   : {'name': u"30万金",   'price': "30"},
        "C50"   : {'name': u"50万金",   'price': "50"},
        "C100"  : {'name': u"100万金",  'price': "100"},
        "C300"  : {'name': u"300万金",  'price': "300"},
        "C1000" : {'name': u"1000万金", 'price': "1000"},
        "C30_MEMBER" : {'name': u"周会员, 立得30万, 每天再送3万",  'price': "30"},
        "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "100"},
        "C5_RAFFLE"  : {'name': u"5元礼包", 'price': "5"},
        "C6_RAFFLE"  : {'name': u"6元礼包", 'price': "6"},
        "C8_RAFFLE"  : {'name': u"8元礼包", 'price': "8"},
        "C5_LUCKY"   : {'name': u"5元转运礼包",  'price': "5"},
        "C8_LUCKY"   : {'name': u"8元转运礼包",  'price': "8"},
        "C10_LUCKY"  : {'name': u"10元转运礼包", 'price': "10"},
    }
})

'''奇天乐地配置
地主 GemeID：2014   Key： aa412ff1c3f9a751597f5ed7d7926dd8 '''
add_global_item('qtld_paykeys', {
    6: 'aa412ff1c3f9a751597f5ed7d7926dd8',
})

add_global_item('qtld_prodids', {
    6: {
        'T50K'           : {'price':'5',    'name':'50000金币'},
        'T60K'           : {'price':'6',    'name':'60000金币'},
        'T80K'           : {'price':'8',    'name':'80000金币'},
        'T100K'          : {'price':'10',   'name':'110000金币'},
        'T300K'          : {'price':'30',   'name':'400000金币'},
        'T500K'          : {'price':'50',   'name':'700000金币'},
        'T1M'            : {'price':'100',  'name':'1500000金币'},
        'T3M'            : {'price':'300',  'name':'4500000金币'},
        'T10M'           : {'price':'1000', 'name':'12000000金币'},
        'RAFFLE'         : {'price':'5',    'name':'50000金币'},
        'RAFFLE_NEW'     : {'price':'8',    'name':'80000金币'},
        'VOICE100'       : {'price':'1',    'name':'语音小喇叭'},
        'MOONKEY'        : {'price':'2',    'name':'月光之钥'},
        'MOONKEY3'       : {'price':'5',    'name':'月光之钥X3'},
        'ZHUANYUN'       : {'price':'5',    'name':'转运礼包'},
        'ZHUANYUN_BIG'   : {'price':'6',    'name':'转运大礼包'},
        'ZHUANYUN_MEZZO' : {'price':'8',    'name':'8元转运礼包'},
        'VIP30'          : {'price':'30',   'name':'VIP（30天）'},
        'PRIVILEGE_30'   : {'price':'100',  'name':'会员（30天）'},
        'PVIP'           : {'price':'30',   'name':'VIP普通礼包'},
        'PVIP_BIG'       : {'price':'50',   'name':'VIP豪华礼包'},
        'TEHUI1Y'        : {'price':'1',    'name':'1元特惠'},
        'CARDMATCH10'    : {'price':'2',    'name':'参赛券X10'},
    },
    8: {
        'TEXAS_COIN1'   : {'price' : '2',    'name' : u'2万筹码'},
        'TEXAS_COIN6'   : {'price' : '5',    'name' : u'5万筹码'},
        'TEXAS_COIN_R6' : {'price' : '6',    'name' : u'6万筹码'},
        'TEXAS_COIN_R8' : {'price' : '8',    'name' : u'8万筹码'},
        'TEXAS_COIN2'   : {'price' : '10',   'name' : u'10万筹码'},
        'TEXAS_COIN_R12': {'price' : '10',   'name' : u'12万筹码'},
        'TEXAS_COIN3'   : {'price' : '30',   'name' : u"30万筹码+额外赠3万" },
        'TEXAS_COIN4'   : {'price' : '50',   'name' : u"50万筹码+额外赠5万" },
        'TEXAS_COIN5'   : {'price' : '100',  'name' : u"100万筹码+额外赠15万" },
        'TEXAS_COIN7'   : {'price' : '300',  'name' : u"300万筹码+额外赠45万" },
        'TEXAS_COIN8'   : {'price' : '1000', 'name' : u"1000万筹码+额外赠200万" },
        'TEXAS_COIN_LUCKY_R6'   : {'price' : '6',    'name' : u"10万" },
        'TEXAS_COIN_LUCKY_R30'  : {'price' : '30',   'name' : u"33万" },
        'TEXAS_COIN_LUCKY_R50'  : {'price' : '50',   'name' : u"55万" },
        'TEXAS_COIN_LUCKY_R100' : {'price' : '100',  'name' : u"115万" },
        'TEXAS_COIN_LUCKY_R300' : {'price' : '300',  'name' : u"345万" },
        'TEXAS_COIN_LUCKY_R1000': {'price' : '1000', 'name' : u"1200万" },
        'TEXAS_VIP1' : {'price' : '30',   'name' : '会员(30天)'},
        'TEXAS_VIP2' : {'price' : '100',  'name' : '会员(30天)'},
        'TEXAS_VIP3' : {'price' : '300',  'name' : '会员(30天)'},
        'TEXAS_VIP4' : {'price' : '1000', 'name' : '会员(30天)'},
        'TEXAS_ITEM_SEND_LED'    : {'price' : '50', 'name' : '喇叭'},
        'TEXAS_ITEM_RENAME_CARD' : {'price' : '100', 'name' : '改名卡'},
    },
    7: {
        "C2"    : {'name': u"2万金", 'price': "2"},
        "C6"    : {'name': u"6万金", 'price': "6"},
        "C5"    : {'name': u"5万金", 'price': "5"},
        "C8"    : {'name': u"8万金", 'price': "8"},
        "C10"   : {'name': u"10万金",   'price': "10"},
        "C30"   : {'name': u"30万金",   'price': "30"},
        "C50"   : {'name': u"50万金",   'price': "50"},
        "C100"  : {'name': u"100万金",  'price': "100"},
        "C300"  : {'name': u"300万金",  'price': "300"},
        "C1000" : {'name': u"1000万金", 'price': "1000"},
        "C30_MEMBER" : {'name': u"周会员, 立得30万, 每天再送3万",  'price': "30"},
        "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "100"},
        "C5_RAFFLE"  : {'name': u"5元礼包", 'price': "5"},
        "C6_RAFFLE"  : {'name': u"6元礼包", 'price': "6"},
        "C8_RAFFLE"  : {'name': u"8元礼包", 'price': "8"},
        "C5_LUCKY"   : {'name': u"5元转运礼包",  'price': "5"},
        "C8_LUCKY"   : {'name': u"8元转运礼包",  'price': "8"},
        "C10_LUCKY"  : {'name': u"10元转运礼包", 'price': "10"},
    }
})

'''114配置
斗地主
appKey : CD1391C579F8405099CCD4F89B5FAE40
appSecret : 6E159B80D11E441F8DD78C1DDFD86ED1
UpayKey: 9d14bbde4cab89a51525797569bff63a
'''
add_global_item('114_paykeys', {
    6: {'appkey' : 'CD1391C579F8405099CCD4F89B5FAE40',
        'appsecret' : '6E159B80D11E441F8DD78C1DDFD86ED1', },
})

add_global_item('114_prodids', { # price unit: rmb yuan
    6: {
        'T50K'          : {'price':'5',    'name':'50000金币'},
        'T60K'          : {'price':'6',    'name':'60000金币'},
        'T80K'          : {'price':'8',    'name':'80000金币'},
        'T100K'         : {'price':'10',   'name':'110000金币'},
        'T300K'         : {'price':'30',   'name':'400000金币'},
        'T500K'         : {'price':'50',   'name':'700000金币'},
        'T1M'           : {'price':'100',  'name':'1500000金币'},
        'T3M'           : {'price':'300',  'name':'4500000金币'},
        'T10M'          : {'price':'1000', 'name':'12000000金币'},
        'RAFFLE'        : {'price':'5',    'name':'50000金币'},
        'RAFFLE_NEW'    : {'price':'8',    'name':'80000金币'},
        'VOICE100'      : {'price':'1',    'name':'语音小喇叭'},
        'MOONKEY'       : {'price':'2',    'name':'月光之钥'},
        'MOONKEY3'      : {'price':'5',    'name':'月光之钥X3'},
        'ZHUANYUN'      : {'price':'5',    'name':'转运礼包'},
        'ZHUANYUN_BIG'  : {'price':'6',    'name':'转运大礼包'},
        'ZHUANYUN_MEZZO': {'price':'8',    'name':'8元转运礼包'},
        'VIP30'         : {'price':'30',   'name':'VIP（30天）'},
        'PRIVILEGE_30'  : {'price':'100',  'name':'会员（30天）'},
        'PVIP'          : {'price':'30',   'name':'VIP普通礼包'},
        'PVIP_BIG'      : {'price':'50',   'name':'VIP豪华礼包'},
        'TEHUI1Y'       : {'price':'1',    'name':'1元特惠'},
        'CARDMATCH10'   : {'price':'2',    'name':'参赛券X10'},
    },
    8: {
        'TEXAS_COIN1'   : {'price' : '2',    'name' : u'2万筹码'},
        'TEXAS_COIN6'   : {'price' : '5',    'name' : u'5万筹码'},
        'TEXAS_COIN_R6' : {'price' : '6',    'name' : u'6万筹码'},
        'TEXAS_COIN_R8' : {'price' : '8',    'name' : u'8万筹码'},
        'TEXAS_COIN2'   : {'price' : '10',   'name' : u'10万筹码'},
        'TEXAS_COIN_R12': {'price' : '10',   'name' : u'12万筹码'},
        'TEXAS_COIN3'   : {'price' : '30',   'name' : u"30万筹码+额外赠3万" },
        'TEXAS_COIN4'   : {'price' : '50',   'name' : u"50万筹码+额外赠5万" },
        'TEXAS_COIN5'   : {'price' : '100',  'name' : u"100万筹码+额外赠15万" },
        'TEXAS_COIN7'   : {'price' : '300',  'name' : u"300万筹码+额外赠45万" },
        'TEXAS_COIN8'   : {'price' : '1000', 'name' : u"1000万筹码+额外赠200万" },
        'TEXAS_COIN_LUCKY_R6'   : {'price' : '6',    'name' : u"10万" },
        'TEXAS_COIN_LUCKY_R30'  : {'price' : '30',   'name' : u"33万" },
        'TEXAS_COIN_LUCKY_R50'  : {'price' : '50',   'name' : u"55万" },
        'TEXAS_COIN_LUCKY_R100' : {'price' : '100',  'name' : u"115万" },
        'TEXAS_COIN_LUCKY_R300' : {'price' : '300',  'name' : u"345万" },
        'TEXAS_COIN_LUCKY_R1000': {'price' : '1000', 'name' : u"1200万" },
        'TEXAS_VIP1' : {'price' : '30',   'name' : '会员(30天)'},
        'TEXAS_VIP2' : {'price' : '100',  'name' : '会员(30天)'},
        'TEXAS_VIP3' : {'price' : '300',  'name' : '会员(30天)'},
        'TEXAS_VIP4' : {'price' : '1000', 'name' : '会员(30天)'},
        'TEXAS_ITEM_SEND_LED'    : {'price' : '50', 'name' : '喇叭'},
        'TEXAS_ITEM_RENAME_CARD' : {'price' : '100', 'name' : '改名卡'},
    },
    7: {
        "C2"    : {'name': u"2万金", 'price': "2"},
        "C6"    : {'name': u"6万金", 'price': "6"},
        "C5"    : {'name': u"5万金", 'price': "5"},
        "C8"    : {'name': u"8万金", 'price': "8"},
        "C10"   : {'name': u"10万金",   'price': "10"},
        "C30"   : {'name': u"30万金",   'price': "30"},
        "C50"   : {'name': u"50万金",   'price': "50"},
        "C100"  : {'name': u"100万金",  'price': "100"},
        "C300"  : {'name': u"300万金",  'price': "300"},
        "C1000" : {'name': u"1000万金", 'price': "1000"},
        "C30_MEMBER" : {'name': u"周会员, 立得30万, 每天再送3万",  'price': "30"},
        "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "100"},
        "C5_RAFFLE"  : {'name': u"5元礼包", 'price': "5"},
        "C6_RAFFLE"  : {'name': u"6元礼包", 'price': "6"},
        "C8_RAFFLE"  : {'name': u"8元礼包", 'price': "8"},
        "C5_LUCKY"   : {'name': u"5元转运礼包",  'price': "5"},
        "C8_LUCKY"   : {'name': u"8元转运礼包",  'price': "8"},
        "C10_LUCKY"  : {'name': u"10元转运礼包", 'price': "10"},
    },
})

'''
卓望配置
'''
add_global_item('zwmdo_configs', {
    'smscodes' : {
               #'1'  : 'YX,258736,1,ff3f,1800529,{orderId}',
               '6'  : 'YX,264236,1,9ccd,1800529,611001,{orderId}',
               '8'  : 'YX,264236,3,e94e,1800529,611001,{orderId}',
               #'10' : 'YX,258736,5,9f1f,1800529,{orderId}',
               },
    'spnumber' : '10658077696611',
})

'''
朗天配置
'''
add_global_item('Langtian_configs', {
    'smscodes' : {
               '1'  : 'w#1039#{orderId}',
               '2'  : 'a#1039#{orderId}',
               '3'  : 'y#1039#{orderId}',
               '4'  : 'l#1039#{orderId}',
               '5'  : 'f#1039#{orderId}',
               '6'  : '1#1039#{orderId}',
               '8'  : '8#1039#{orderId}',
               '10' : '9#1039#{orderId}',
               '12' : '1#1039#{orderId}',
               '15' : '0#1039#{orderId}',
               '16' : '0#1039#{orderId}',
               '18' : '1#1039#{orderId}',
               '20' : '1#1039#{orderId}',
               '25' : '1#1039#{orderId}',
               '30' : '1#1039#{orderId}',},
     'smsports' : {
                 '1'  : '10661025',
                 '2'  : '10661025',
                 '3'  : '10661025',
                 '4'  : '10661025',
                 '5'  : '10661025',
                 '6'  : '106598725',
                 '8'  : '1065987215',
                 '10' : '1065987216',
                 '12' : '106598726',
                 '15' : '1065987218',
                 '16' : '106598728',
                 '18' : '106598727',
                 '20' : '106598723',
                 '25' : '1065987217',
                 '30' : '106598724',
                 },
     'key'      : '3J91j10M'
})

'''凌云IDO配置
'''
add_global_item('IDO_smscodes', {
    '2'  : '28 795132 613216016745 20120101000000 41008000 000000000000 '
           'aa32909892a5e5c5fea64313b0a9c3051dbecf52 0 000000000 006043163001 0 '
           '{orderId}9802',
    '3'  : '28 795132 613216016746 20120101000000 41008000 000000000000 '
           '5eeab01e3a52a2e9ca814546aa758adb5a57e5d4 0 000000000 006043164001 0 '
           '{orderId}9803',
    '8'  : '28 710267 626716016829 20120101000000 40254006 000000000000 '
           '2badadbcc662053456f8b147d0221872ec363141 0 000000000 006043345003 0 '
           '09{orderId}98',
    '10' : '28 795132 613216016747 20120101000000 41008000 000000000000 '
           '82f1bf33f24b5104a76d5902c8215a2b18d3182c 0 000000000 006043168001 0 '
           '{orderId}9810',
})

add_global_item('IDO_orderid', {
    '200'   :[0, 6],
    '300'   :[0, 6],
    '800'   :[0, 6],
    '1000'  :[0, 6],
})


add_global_item('IDO_prodids', { # price unit: rmb yuan
    6: {
        'T50K'          : {'price':'5',    'name':'50000金币'},
        'T60K'          : {'price':'6',    'name':'60000金币'},
        'T80K'          : {'price':'8',    'name':'80000金币'},
        'T100K'         : {'price':'10',   'name':'110000金币'},
        'T300K'         : {'price':'30',   'name':'400000金币'},
        'T500K'         : {'price':'50',   'name':'700000金币'},
        'T1M'           : {'price':'100',  'name':'1500000金币'},
        'T3M'           : {'price':'300',  'name':'4500000金币'},
        'T10M'          : {'price':'1000', 'name':'12000000金币'},
        'RAFFLE'        : {'price':'5',    'name':'50000金币'},
        'RAFFLE_NEW'    : {'price':'8',    'name':'80000金币'},
        'VOICE100'      : {'price':'1',    'name':'语音小喇叭'},
        'MOONKEY'       : {'price':'2',    'name':'月光之钥'},
        'MOONKEY3'      : {'price':'5',    'name':'月光之钥X3'},
        'ZHUANYUN'      : {'price':'5',    'name':'转运礼包'},
        'ZHUANYUN_BIG'  : {'price':'6',    'name':'转运大礼包'},
        'ZHUANYUN_MEZZO': {'price':'8',    'name':'8元转运礼包'},
        'ZHUANYUN_MXDDZ': {'price':'8',    'name':'8元转运礼包'},
        'VIP30'         : {'price':'30',   'name':'VIP（30天）'},
        'PRIVILEGE_30'  : {'price':'100',  'name':'会员（30天）'},
        'PVIP'          : {'price':'30',   'name':'VIP普通礼包'},
        'PVIP_BIG'      : {'price':'50',   'name':'VIP豪华礼包'},
        'TEHUI1Y'       : {'price':'1',    'name':'1元特惠'},
        'CARDMATCH10'   : {'price':'2',    'name':'参赛券X10'},
        'TY9999D0006001' : {'price':'6',   'name':'60000金币',},
        'TY9999D0008001' : {'price':'8',   'name':'80000金币',},
        'TY0006D0002001' : {'price':'2',   'name':'月光之钥',},
    },
    8: {
        'TEXAS_COIN1'   : {'price' : '2',    'name' : u'2万筹码'},
        'TEXAS_COIN6'   : {'price' : '5',    'name' : u'5万筹码'},
        'TEXAS_COIN_R6' : {'price' : '6',    'name' : u'6万筹码'},
        'TEXAS_COIN_R8' : {'price' : '8',    'name' : u'8万筹码'},
        'TEXAS_COIN2'   : {'price' : '10',   'name' : u'10万筹码'},
        'TEXAS_COIN_R12': {'price' : '10',   'name' : u'12万筹码'},
        'TEXAS_COIN3'   : {'price' : '30',   'name' : u"30万筹码+额外赠3万" },
        'TEXAS_COIN4'   : {'price' : '50',   'name' : u"50万筹码+额外赠5万" },
        'TEXAS_COIN5'   : {'price' : '100',  'name' : u"100万筹码+额外赠15万" },
        'TEXAS_COIN7'   : {'price' : '300',  'name' : u"300万筹码+额外赠45万" },
        'TEXAS_COIN8'   : {'price' : '1000', 'name' : u"1000万筹码+额外赠200万" },
        'TEXAS_COIN_LUCKY_R6'   : {'price' : '6',    'name' : u"10万" },
        'TEXAS_COIN_LUCKY_R30'  : {'price' : '30',   'name' : u"33万" },
        'TEXAS_COIN_LUCKY_R50'  : {'price' : '50',   'name' : u"55万" },
        'TEXAS_COIN_LUCKY_R100' : {'price' : '100',  'name' : u"115万" },
        'TEXAS_COIN_LUCKY_R300' : {'price' : '300',  'name' : u"345万" },
        'TEXAS_COIN_LUCKY_R1000': {'price' : '1000', 'name' : u"1200万" },
        'TEXAS_VIP1' : {'price' : '30',   'name' : '会员(30天)'},
        'TEXAS_VIP2' : {'price' : '100',  'name' : '会员(30天)'},
        'TEXAS_VIP3' : {'price' : '300',  'name' : '会员(30天)'},
        'TEXAS_VIP4' : {'price' : '1000', 'name' : '会员(30天)'},
        'TEXAS_ITEM_SEND_LED'    : {'price' : '50', 'name' : '喇叭'},
        'TEXAS_ITEM_RENAME_CARD' : {'price' : '100', 'name' : '改名卡'},
    },
    7: {
        "C2"    : {'name': u"2万金", 'price': "2"},
        "C6"    : {'name': u"6万金", 'price': "6"},
        "C5"    : {'name': u"5万金", 'price': "5"},
        "C8"    : {'name': u"8万金", 'price': "8"},
        "C10"   : {'name': u"10万金",   'price': "10"},
        "C30"   : {'name': u"30万金",   'price': "30"},
        "C50"   : {'name': u"50万金",   'price': "50"},
        "C100"  : {'name': u"100万金",  'price': "100"},
        "C300"  : {'name': u"300万金",  'price': "300"},
        "C1000" : {'name': u"1000万金", 'price': "1000"},
        "C30_MEMBER" : {'name': u"周会员, 立得30万, 每天再送3万",  'price': "30"},
        "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "100"},
        "C5_RAFFLE"  : {'name': u"5元礼包", 'price': "5"},
        "C6_RAFFLE"  : {'name': u"6元礼包", 'price': "6"},
        "C8_RAFFLE"  : {'name': u"8元礼包", 'price': "8"},
        "C5_LUCKY"   : {'name': u"5元转运礼包",  'price': "5"},
        "C8_LUCKY"   : {'name': u"8元转运礼包",  'price': "8"},
        "C10_LUCKY"  : {'name': u"10元转运礼包", 'price': "10"},
    },
})

'''xiaomi配置
'''
add_global_item('xiaomi_paykeys', {
    '12724' : '2277c367-455b-abaa-af54-5189b218b080', # 斗地主
    '19528' : '4d880058-3a9c-e3ea-658c-52283e8b1c83', # 赢三张
    '2882303761517263673' : 'zdpHc9yzprQMS58KW2jNWA==', # 麻将
    '2882303761517270039' : 'S54fksyPOf9x4Y3EmBqFAg==', #途游斗地主
    '2882303761517420714' : 'fkKOmsAWVJLZ83PJSX24nQ==', # 跑胡子
    '2882303761517433265' : 'ZUbIn4ILIXlEyiWAFGBdEA==', # 军旗
    '2882303761517444424' : 'gacjHXQ+MHzc14GGdDRC/w==', # 德州
    '2882303761517442824' : 'p27vT3y/WX8sSRWYWu6gZQ==', # 四川麻将
    '2882303761517483902' : '4e21OmvByzmK76jOiT0GbA==', # 青岛棋牌


})

add_global_item('xiaomidanji_prodids', {
    6: {
        'T50K'          : {'price':'5',    'name':'50000金币',     },
        'T60K'          : {'price':'6',    'name':'60000金币',     },
        'T80K'          : {'price':'8',    'name':'80000金币',     },
        'T100K'         : {'price':'10',   'name':'110000金币',    },
        'T300K'         : {'price':'30',   'name':'400000金币',    },
        'T500K'         : {'price':'50',   'name':'700000金币',    },
        'T1M'           : {'price':'100',  'name':'1500000金币',   },
        'T3M'           : {'price':'300',  'name':'4500000金币',   },
        'T10M'          : {'price':'1000', 'name':'12000000金币',  },
        'RAFFLE'        : {'price':'5',    'name':'50000金币',     },
        'RAFFLE_NEW'    : {'price':'8',    'name':'80000金币',     },
        'VOICE100'      : {'price':'1',    'name':'语音小喇叭',    },
        'MOONKEY'       : {'price':'2',    'name':'月光之钥',      },
        'MOONKEY3'      : {'price':'5',    'name':'月光之钥X3',    },
        'ZHUANYUN'      : {'price':'5',    'name':'转运礼包',      },
        'ZHUANYUN_BIG'  : {'price':'6',    'name':'转运大礼包',    },
        'ZHUANYUN_MEZZO': {'price':'8',    'name':'8元转运礼包'},
        'VIP30'         : {'price':'30',   'name':'VIP（30天）',   },
        'PRIVILEGE_30'  : {'price':'100',  'name':'会员（30天）',  },
        'PVIP'          : {'price':'30',   'name':'VIP普通礼包',   },
        'PVIP_BIG'      : {'price':'50',   'name':'VIP豪华礼包',   },
        'TEHUI1Y'       : {'price':'1',    'name':'1元特惠',       },
        'CARDMATCH10'   : {'price':'2',    'name':'参赛券X10',     },
        'TY9999R00020DJ' : {'price':'2',        'name':'银币',     },
        'TY9999D0001001' : {'price':'1',        'name':'1元特惠礼包',     },
        'TY9999D0002001' : {'price':'6',        'name':'20000金币',     },
        'TY9999D0006001' : {'price':'6',        'name':'60000金币',     },
        'TY9999D0030001' : {'price':'30',        'name':'360000金币',     },
        'TY9999D0050001' : {'price':'50',        'name':'650000金币',    },
        'TY9999D0100001' : {'price':'100',        'name':'1500000金币',    },
        'TY9999D0300001' : {'price':'300',        'name':'5000000金币',    },
        'TY9999D1000001' : {'price':'1000',        'name':'2000万金币',   },
        'TY0006D0030002' : {'price':'30',        'name':'7天会员卡',   },
        'TY0006D0100002' : {'price':'100',       'name':'30天会员卡',  },
        'TY9999R0008001' : {'price':'8',       'name':'80钻石',     },
        'TY9999R0050001' : {'price':'50',       'name':'500钻石',     },
        'TY9999R0100001' : {'price':'100',      'name':'1000钻石',    },
        'TY0006D0002001' : {'price':'2',       'name':'月光之钥',    },
        'TY0006D0005001' : {'price':'5',       'name':'月光之钥x3',      },
        'TY0006D0002002' : {'price':'2',       'name':'参赛券x10',    },
        'TY0006D0000201' : {'price':'0.20',       'name':'小喇叭x10',      },
        'TY0006D0050002' : {'price':'50',       'name':'广播喇叭',    },
        'TY0006D0100003' : {'price':'100',       'name':'改名卡'},
        'TY0006D0010001' : {'price':'10',       'name':'记牌器x7',   },
        'TY9999D0008001' : {'price':'8',       'name':'超值礼包',  },
        'TY9999D0006002' : {'price':'6',        'name':'6元转运礼包',   },
        'TY9999D0008002' : {'price':'8',       'name':'8元转运礼包',   },

    },
    8: {
        'TEXAS_COIN1'   : {'price' : '2',    'name' : u'2万筹码',               },
        'TEXAS_COIN6'   : {'price' : '5',    'name' : u'5万筹码',               },
        'TEXAS_COIN_R6' : {'price' : '6',    'name' : u'6万筹码',               },
        'TEXAS_COIN_R8' : {'price' : '8',    'name' : u'8万筹码',               },
        'TEXAS_COIN2'   : {'price' : '10',   'name' : u'10万筹码',              },
        'TEXAS_COIN_R12': {'price' : '10',   'name' : u'12万筹码',              },
        'TEXAS_COIN3'   : {'price' : '30',   'name' : u"30万筹码+额外赠3万",    },
        'TEXAS_COIN4'   : {'price' : '50',   'name' : u"50万筹码+额外赠5万",    },
        'TEXAS_COIN5'   : {'price' : '100',  'name' : u"100万筹码+额外赠15万",  },
        'TEXAS_COIN7'   : {'price' : '300',  'name' : u"300万筹码+额外赠45万",  },
        'TEXAS_COIN8'   : {'price' : '1000', 'name' : u"1000万筹码+额外赠200万",},
        'TEXAS_COIN_LUCKY_R6'   : {'price' : '6',    'name' : u"10万",          },
        'TEXAS_COIN_LUCKY_R30'  : {'price' : '30',   'name' : u"33万",          },
        'TEXAS_COIN_LUCKY_R50'  : {'price' : '50',   'name' : u"55万",          },
        'TEXAS_COIN_LUCKY_R100' : {'price' : '100',  'name' : u"115万",         },
        'TEXAS_COIN_LUCKY_R300' : {'price' : '300',  'name' : u"345万",         },
        'TEXAS_COIN_LUCKY_R1000': {'price' : '1000', 'name' : u"1200万",        },
        'TEXAS_VIP1' : {'price' : '30',   'name' : '会员(30天)',                },
        'TEXAS_VIP2' : {'price' : '100',  'name' : '会员(30天)',                },
        'TEXAS_VIP3' : {'price' : '300',  'name' : '会员(30天)',                },
        'TEXAS_VIP4' : {'price' : '1000', 'name' : '会员(30天)',                },
        'TEXAS_ITEM_SEND_LED'    : {'price' : '50', 'name' : '喇叭',            },
        'TEXAS_ITEM_RENAME_CARD' : {'price' : '100', 'name' : '改名卡',         },
    },
    7: {
        "C2"    : {'name': u"2万金", 'price': "2",                                 },
        "C6"    : {'name': u"6万金", 'price': "6" ,                                },
        "C5"    : {'name': u"5万金", 'price': "5",                                 },
        "C8"    : {'name': u"8万金", 'price': "8",                                 },
        "C10"   : {'name': u"10万金",   'price': "10",                             },
        "C30"   : {'name': u"30万金",   'price': "30",                             },
        "C50"   : {'name': u"50万金",   'price': "50",                             },
        "C100"  : {'name': u"100万金",  'price': "100",                            },
        "C300"  : {'name': u"300万金",  'price': "300",                            },
        "C1000" : {'name': u"1000万金", 'price': "1000",                           },
        "C30_MEMBER" : {'name': u"周会员, 立得30万, 每天再送3万",  'price': "30",  },
        "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "100", },
        "C5_RAFFLE"  : {'name': u"5元礼包", 'price': "5",                          },
        "C6_RAFFLE"  : {'name': u"6元礼包", 'price': "6",                          },
        "C8_RAFFLE"  : {'name': u"8元礼包", 'price': "8",                          },
        "C5_LUCKY"   : {'name': u"5元转运礼包",  'price': "5",                     },
        "C8_LUCKY"   : {'name': u"8元转运礼包",  'price': "8",                     },
        "C10_LUCKY"  : {'name': u"10元转运礼包", 'price': "10",                    },
        'TY0007D0006001' : {'price':'6',        'name':'60000金币',     },
        'TY0007D0008001' : {'price':'8',        'name':'80000金币',     },
        'TY0007D0010001' : {'price':'10',        'name':'100000金币',     },
        'TY9999D0006001' : {'price':'6',        'name':'60000金币',     },
        'TY9999D0030001' : {'price':'30',        'name':'300000金币',     },
        'TY9999D0100001' : {'price':'100',        'name':'1000000金币',    },
        'TY0007D0030001' : {'price':'30',        'name':'300000金币',     },
        'TY0007D0050001' : {'price':'50',        'name':'500000金币',    },
        'TY0007D0100001' : {'price':'100',        'name':'1000000金币',    },
        'TY0007D0300001' : {'price':'300',        'name':'3000000金币',    },
        'TY0007D1000001' : {'price':'1000',        'name':'1000万金币',   },
        'TY0007D0030002' : {'price':'30',        'name':'7天会员卡',   },
        'TY0007D0030003' : {'price':'30',        'name':'7天会员卡',   },
        'TY0007D0100002' : {'price':'100',       'name':'30天会员卡',  },
        'TY0007D0100003' : {'price':'100',       'name':'30天会员卡',  },
        'TY9999R0008001' : {'price':'8',       'name':'80钻石',     },
        'TY9999R0050001' : {'price':'50',       'name':'500钻石',     },
        'TY9999D0008001' : {'price':'8',       'name':'超值礼包',  },
        'TY9999D0006002' : {'price':'6',        'name':'6元转运礼包',   },
        'TY9999D0008002' : {'price':'8',       'name':'8元转运礼包',   },


    }
})

'''360支付配置
'''
add_global_item('360pay_prodids', {
    6: { # price unit: rmb fen
        'T50K'         : {'price':'500',    'name':'50000金币'},
        'T60K'         : {'price':'600',    'name':'60000金币'},
        'T80K'         : {'price':'800',    'name':'80000金币'},
        'T100K'        : {'price':'1000',   'name':'110000金币'},
        'T300K'        : {'price':'3000',   'name':'400000金币'},
        'T500K'        : {'price':'5000',   'name':'700000金币'},
        'T1M'          : {'price':'10000',  'name':'1500000金币'},
        'T3M'          : {'price':'30000',  'name':'4500000金币'},
        'T10M'         : {'price':'100000', 'name':'12000000金币'},
        'RAFFLE'       : {'price':'500',    'name':'50000金币'},
        'RAFFLE_NEW'   : {'price':'800',    'name':'80000金币'},
        'VOICE100'     : {'price':'100',    'name':'语音小喇叭'},
        'MOONKEY'      : {'price':'200',    'name':'月光之钥'},
        'MOONKEY3'     : {'price':'500',    'name':'月光之钥X3'},
        'ZHUANYUN'     : {'price':'500',    'name':'转运礼包'},
        'ZHUANYUN_BIG' : {'price':'600',    'name':'转运大礼包'},
        'ZHUANYUN_MEZZO':{'price':'800',    'name':'8元转运礼包'},
        'VIP30'        : {'price':'3000',   'name':'VIP（30天）'},
        'PRIVILEGE_30' : {'price':'10000',  'name':'会员（30天）'},
        'PVIP'         : {'price':'3000',   'name':'VIP普通礼包'},
        'PVIP_BIG'     : {'price':'5000',   'name':'VIP豪华礼包'},
        'TEHUI1Y'      : {'price':'100',    'name':'1元特惠'},
        'CARDMATCH10'  : {'price':'200',    'name':'参赛券X10'},
        'TY9999D0006001' : {'price':'600',  'name':'60000金币',},
        },
    8: {
        'TEXAS_COIN1'   : {'price' : '200',    'name' : u'2万筹码'},
        'TEXAS_COIN6'   : {'price' : '500',    'name' : u'5万筹码'},
        'TEXAS_COIN_R6' : {'price' : '600',    'name' : u'6万筹码'},
        'TEXAS_COIN_R8' : {'price' : '800',    'name' : u'8万筹码'},
        'TEXAS_COIN2'   : {'price' : '1000',   'name' : u'10万筹码'},
        'TEXAS_COIN_R12': {'price' : '1200',   'name' : u'12万筹码'},
        'TEXAS_COIN3'   : {'price' : '3000',   'name' : u"30万筹码+额外赠3万" },
        'TEXAS_COIN4'   : {'price' : '5000',   'name' : u"50万筹码+额外赠5万" },
        'TEXAS_COIN5'   : {'price' : '10000',  'name' : u"100万筹码+额外赠15万" },
        'TEXAS_COIN7'   : {'price' : '30000',  'name' : u"300万筹码+额外赠45万" },
        'TEXAS_COIN8'   : {'price' : '100000', 'name' : u"1000万筹码+额外赠200万" },
        'TEXAS_COIN_LUCKY_R6'   : {'price' : '600',    'name' : u"10万" },
        'TEXAS_COIN_LUCKY_R30'  : {'price' : '3000',   'name' : u"33万" },
        'TEXAS_COIN_LUCKY_R50'  : {'price' : '5000',   'name' : u"55万" },
        'TEXAS_COIN_LUCKY_R100' : {'price' : '10000',  'name' : u"115万" },
        'TEXAS_COIN_LUCKY_R300' : {'price' : '30000',  'name' : u"345万" },
        'TEXAS_COIN_LUCKY_R1000': {'price' : '100000', 'name' : u"1200万" },
        'TEXAS_VIP1' : {'price' : '3000',   'name' : '会员(30天)'},
        'TEXAS_VIP2' : {'price' : '10000',  'name' : '会员(30天)'},
        'TEXAS_VIP3' : {'price' : '30000',  'name' : '会员(30天)'},
        'TEXAS_VIP4' : {'price' : '100000', 'name' : '会员(30天)'},
        'TEXAS_ITEM_SEND_LED'    : {'price' : '5000', 'name' : '喇叭'},
        'TEXAS_ITEM_RENAME_CARD' : {'price' : '10000', 'name' : '改名卡'},
    },
    7: {
        "C2"    : {'name': u"2万金", 'price': "200"},
        "C6"    : {'name': u"6万金", 'price': "600"},
        "C5"    : {'name': u"5万金", 'price': "500"},
        "C8"    : {'name': u"8万金", 'price': "800"},
        "C10"   : {'name': u"10万金",   'price': "1000"},
        "C30"   : {'name': u"30万金",   'price': "3000"},
        "C50"   : {'name': u"50万金",   'price': "5000"},
        "C100"  : {'name': u"100万金",  'price': "10000"},
        "C300"  : {'name': u"300万金",  'price': "30000"},
        "C1000" : {'name': u"1000万金", 'price': "100000"},
        "C30_MEMBER" : {'name': u"周会员, 立得30万, 每天再送3万",  'price': "3000"},
        "C100_MEMBER": {'name': u"月会员，立得100万, 每天再赠3万", 'price': "10000"},
        "C5_RAFFLE"  : {'name': u"5元礼包", 'price': "500"},
        "C6_RAFFLE"  : {'name': u"6元礼包", 'price': "600"},
        "C8_RAFFLE"  : {'name': u"8元礼包", 'price': "800"},
        "C5_LUCKY"   : {'name': u"5元转运礼包",  'price': "500"},
        "C8_LUCKY"   : {'name': u"8元转运礼包",  'price': "800"},
        "C10_LUCKY"  : {'name': u"10元转运礼包", 'price': "1000"},
    },
    10019: {
        "diamond5"     : {'name': u"5钻石", 'price': "500"},
        "diamond10"    : {'name': u"10钻石", 'price': "1000"},
        "diamond30"    : {'name': u"30钻石", 'price': "3000"},
        "diamond50"    : {'name': u"50钻石", 'price': "5000"},
        "diamond100"   : {'name': u"100钻石",   'price': "10000"},
        "diamond500"   : {'name': u"500钻石",   'price': "50000"},
    },

})

'''小米单机配置
'''
add_global_item('xiaomidanji_paykeys', {
    '2882303761517263673' : 'zdpHc9yzprQMS58KW2jNWA==', # 疯狂麻将
    '2882303761517271823' : 'O8W+mOiqowREUs4KKnlveQ==', #德州
    '2882303761517272414' : 'Z+tvt2k1ITL6hmdKIzxxng==', #KK欢乐斗地主
    '2882303761517307128' : 'dQVfBlCGi3bQik8+bqSapA==', #KK欢乐麻将
    '2882303761517373625' : 'aU/BgPRDFUOllXGI9y2mZQ==', #中国象棋
    '2882303761517409220' : '4p/7zpeFq3347H5tllzPrg==',#途游五子棋（旧）
    '2882303761517419917' : '63VdygyHglwFUH9dk8OPHA==',#途游五子棋 (新）
    '2882303761517415024' : 'p8BSBkaMEoRha/9YIBy0vg==', # 保皇
    '2882303761517307128' : 'dQVfBlCGi3bQik8+bqSapA==', # 麻将

})

'''oppo配置
'''
add_global_item('oppo_prodids', {
    3: {
        'TY9999D0001001'          : {'count':'1',        'name':'元特惠礼包',     },
        'TY9999D0002001'          : {'count':'20000',    'name':'金币',     },
        'TY9999D0006001'          : {'count':'60000',    'name':'金币',     },
        'TY9999D0030001'          : {'count':'360000',   'name':'金币',     },
        'TY9999D0050001'          : {'count':'650000',   'name':'金币',    },
        'TY9999D0100001'          : {'count':'1500000',  'name':'金币',    },
        'TY9999D0300001'          : {'count':'5000000',  'name':'金币',    },
        'TY9999D1000001'          : {'count':'20000000', 'name':'金币',   },
        'TY0006D0030002'          : {'count':'7',        'name':'天会员卡',   },
        'TY0006D0100002'          : {'count':'30',       'name':'天会员卡',  },
        'TY9999R0008001'          : {'count':'80',       'name':'钻石',     },
        'TY9999R0050001'          : {'count':'500',      'name':'钻石',     },
        'TY0006D0002001'          : {'count':'1',        'name':'月光之钥',    },
        'TY0006D0005001'          : {'count':'3',        'name':'月光之钥',      },
        'TY0006D0002002'          : {'count':'10',       'name':'参赛券',    },
        'TY0006D0000201'          : {'count':'10',       'name':'小喇叭',      },
        'TY0006D0050002'          : {'count':'1',        'name':'广播喇叭',    },
        'TY0006D0100003'          : {'count':'1',        'name':'改名卡'},
        'TY0006D0010001'          : {'count':'7',        'name':'记牌器',   },
        'TY9999D0008001'          : {'count':'1',        'name':'超值礼包',  },
        'TY9999D0006002'          : {'count':'6',        'name':'元转运礼包',   },
        'TY9999D0008002'          : {'count':'8',        'name':'元转运礼包',   },
    },
    6: {
        'TY9999R00020DJ'          : {'count':'0',        'name':'银币',     },
        'TY9999D0001001'          : {'count':'1',        'name':'元特惠礼包',     },
        'TY9999D0002001'          : {'count':'20000',    'name':'金币',     },
        'TY9999D0006001'          : {'count':'60000',    'name':'金币',     },
        'TY9999D0030001'          : {'count':'360000',   'name':'金币',     },
        'TY9999D0050001'          : {'count':'650000',   'name':'金币',    },
        'TY9999D0100001'          : {'count':'1500000',  'name':'金币',    },
        'TY9999D0300001'          : {'count':'5000000',  'name':'金币',    },
        'TY9999D1000001'          : {'count':'20000000', 'name':'金币',   },
        'TY0006D0030002'          : {'count':'7',        'name':'天会员卡',   },
        'TY0006D0100002'          : {'count':'30',       'name':'天会员卡',  },
        'TY9999R0008001'          : {'count':'80',       'name':'钻石',     },
        'TY9999R0050001'          : {'count':'500',      'name':'钻石',     },
        'TY9999R0100001'          : {'count':'1000',     'name':'钻石',     },
        'TY0006D0002001'          : {'count':'1',        'name':'月光之钥',    },
        'TY0006D0005001'          : {'count':'3',        'name':'月光之钥',      },
        'TY0006D0002002'          : {'count':'10',       'name':'参赛券',    },
        'TY0006D0000201'          : {'count':'10',       'name':'小喇叭',      },
        'TY0006D0050002'          : {'count':'1',        'name':'广播喇叭',    },
        'TY0006D0100003'          : {'count':'1',        'name':'改名卡'},
        'TY0006D0010001'          : {'count':'7',        'name':'记牌器',   },
        'TY9999D0008001'          : {'count':'1',        'name':'超值礼包',  },
        'TY9999D0006002'          : {'count':'6',        'name':'元转运礼包',   },
        'TY9999D0008002'          : {'count':'8',        'name':'元转运礼包',   },
    },
    7: {
        'TY0007D0008001'          : {'count':'80000',    'name':'金币',     },
        'TY0007D0010001'          : {'count':'100000',   'name':'金币',     },
        'TY0007D0030001'          : {'count':'300000',   'name':'金币',    },
        'TY0007D0050001'          : {'count':'500000',   'name':'金币',    },
        'TY0007D0100001'          : {'count':'1000000',  'name':'金币',    },
        'TY0007D0300001'          : {'count':'3000000',  'name':'金币',   },
        'TY0007D1000001'          : {'count':'1000',     'name':'万金币',   },
        'TY0007D0030002'          : {'count':'7',        'name':'天会员卡',   },
        'TY0007D0100002'          : {'count':'30',        'name':'天会员卡',  },
        'TY9999R0008001'          : {'count':'80',       'name':'钻石',     },
        'TY9999R0100001'          : {'count':'1000',     'name':'钻石',     },
        'TY9999R0050001'          : {'count':'500',      'name':'钻石',     },
        'TY9999D0008001'          : {'count':'1',        'name':'超值礼包',  },
        'TY9999D0008002'          : {'count':'8',        'name':'元转运礼包',   },
    },
    8: {
        'TY0008D0008001'          : {'count':'80000',    'name':'金币',     },
        'TY0008D0010001'          : {'count':'100000',   'name':'金币',     },
        'TY0008D0030001'          : {'count':'300000',   'name':'金币',    },
        'TY0008D0050001'          : {'count':'500000',   'name':'金币',    },
        'TY0008D0100001'          : {'count':'1000000',  'name':'金币',    },
        'TY0008D0300001'          : {'count':'3000000',  'name':'金币',   },
        'TY0008D1000001'          : {'count':'10000000',   'name':'金币',   },
        'TY0008D0100002'          : {'count':'30',        'name':'天会员卡',  },
        'TY9999R0008001'          : {'count':'80',       'name':'钻石',     },
        'TY9999R0050001'          : {'count':'500',      'name':'钻石',     },
        'TY9999D0008001'          : {'count':'1',        'name':'超值礼包',  },
        'TY9999D0008002'          : {'count':'8',        'name':'元转运礼包',   },
        'TY9999R0000101'          : {'count':'1',    'name':'钻石',     },
        'TY9999D0002001'          : {'count':'20000',    'name':'金币',     },
        'TY9999D0005003'          : {'count':'50000',    'name':'金币',     },
        'TY9999D0006016'          : {'count':'60000',    'name':'金币',     },
        'TY9999R0008005'          : {'count':'80',      'name':'钻石',     },
        'TY9999D0001003'          : {'count':'1',    'name':'天会员',     },
        'TY9999D0012003'          : {'count':'30',    'name':'天会员',     },
        'TY9999D0030001'          : {'count':'36',   'name':'万金币',     },
        'TY9999D0030011'          : {'count':'30',   'name':'元转运礼包',    },
        'TY9999D0030012'          : {'count':'30',   'name':'元高手礼包',    },
        'TY9999R0050001'          : {'count':'500',  'name':'钻石',    },
        'TY9999D0050001'          : {'count':'65',  'name':'万金币',   },
        'TY9999D0050007'          : {'count':'50',   'name':'元转运礼包',   },
        'TY9999D0050008'          : {'count':'50',        'name':'元高手礼包',  },
        'TY9999D0100001'          : {'count':'150',       'name':'万金币',     },
        'TY9999R0100001'          : {'count':'1000',      'name':'钻石',     },
        'TY9999D0100011'          : {'count':'100',        'name':'元转运礼包',  },
        'TY9999D0100012'          : {'count':'100',        'name':'元高手礼包',   },
        'TY9999D0300001'          : {'count':'500',        'name':'万金币',   },
        'TY9999D1000001'          : {'count':'2000',        'name':'万金币',   },
        'TY9999D0008027'          : {'count':'80000',        'name':'金币',   },
        'TY9999D0008005'          : {'count':'80000',        'name':'金币',   },
        'TY9999D0008025'          : {'count':'8',        'name':'元高手限量特价礼包',     },
        'TY9999D0008026'          : {'count':'8',        'name':'元转运限量特价礼包',     },
        'TY9999D0008001'          : {'count':'8',        'name':'元超值礼包',     },
        'TY9999D0100001'          : {'count':'1500000',  'name':'金币',    },
        'TY9999D0010001'          : {'count':'100000',  'name':'金币',    },
        'TY9999D5000001'          : {'count':'1',        'name':'亿金币',   },
        'TY9999D0100019'          : {'count':'100',        'name':'元月卡',   },
    },
    9999: {
        'TY9999R0000101'          : {'count':'1',    'name':'钻石',     },
        'TY9999D0002001'          : {'count':'20000',    'name':'金币',     },
        'TY9999D0005003'          : {'count':'50000',    'name':'金币',     },
        'TY9999D0006016'          : {'count':'60000',    'name':'金币',     },
        'TY9999D0006001'          : {'count':'60000',    'name':'金币',     },
        'TY9999R0008005'          : {'count':'80',      'name':'钻石',     },
        'TY9999D0001003'          : {'count':'1',    'name':'天会员',     },
        'TY9999D0012003'          : {'count':'30',    'name':'天会员',     },
        'TY9999D0030001'          : {'count':'36',   'name':'万金币',     },
        'TY9999D0030011'          : {'count':'30',   'name':'元转运礼包',    },
        'TY9999D0030012'          : {'count':'30',   'name':'元高手礼包',    },
        'TY9999R0050001'          : {'count':'500',  'name':'钻石',    },
        'TY9999D0050001'          : {'count':'65',  'name':'万金币',   },
        'TY9999D0050007'          : {'count':'50',   'name':'元转运礼包',   },
        'TY9999D0050008'          : {'count':'50',        'name':'元高手礼包',  },
        'TY9999D0100001'          : {'count':'150',       'name':'万金币',     },
        'TY9999R0100001'          : {'count':'1000',      'name':'钻石',     },
        'TY9999D0100011'          : {'count':'100',        'name':'元转运礼包',  },
        'TY9999D0100012'          : {'count':'100',        'name':'元高手礼包',   },
        'TY9999D0300001'          : {'count':'500',        'name':'万金币',   },
        'TY9999D1000001'          : {'count':'2000',        'name':'万金币',   },
        'TY9999D0008027'          : {'count':'80000',        'name':'金币',   },
        'TY9999D0008005'          : {'count':'80000',        'name':'金币',   },
        'TY9999D0008025'          : {'count':'8',        'name':'元高手限量特价礼包',     },
        'TY9999D0008026'          : {'count':'8',        'name':'元转运限量特价礼包',     },
        'TY9999D0008001'          : {'count':'8',        'name':'元超值礼包',     },
        'TY9999D0008034'          : {'count':'8',        'name':'元超值礼包',     },
        'TY9999D0100001'          : {'count':'1500000',  'name':'金币',    },
        'TY9999D0010001'          : {'count':'100000',  'name':'金币',    },
        'TY9999D5000001'          : {'count':'1',        'name':'亿金币',   },
        'TY9999D0100019'          : {'count':'100',        'name':'元月卡',   },
        'TY9999R0010001'          : {'count':'100',      'name':'钻石',     },
        'TY9999D0008038'          : {'count':'80000',      'name':'金币',     },
        'TY9999D0030024'          : {'count':'36',      'name':'万金币',     },
        'TY9999D0050011'          : {'count':'65',      'name':'万金币',     },
        'TY9999D0100021'          : {'count':'150',      'name':'万金币',     },
        'TY9999D0300004'          : {'count':'500',      'name':'万金币',     },
        'TY9999D1000012'          : {'count':'2000',      'name':'万金币',     },
        'TY9999D1000013'          : {'count':'1000',      'name':'元月卡',     },
        'TY9999R0030001'          : {'count':300, 'name':'钻石'},
        'TY9999R0200001'          : {'count':'2000',      'name':'钻石',     },
        'TY9999R0300001'          : {'count':'3000',      'name':'钻石',     },
        'TY9999R0600001'          : {'count':'6000',      'name':'钻石',     },
        'TY9999D0328016'          : {'count':'1',      'name':'3280钻VIP礼包',     },
        'TY9999D0300006'          : {'count':'1',      'name':'3000钻VIP礼包',     },
        'TY9999R0128001'          : {'count':'1280',      'name':'钻石',     },
        #2016年12月29日15:16:47 德州新增
        'TY9999D2000001'          : {'count':'4000',      'name':'万金币',     },
        'TY9999R0328001'          : {'count':'3280',      'name':'钻石',     },
        'TY9999D0008031'          : {'count':'4',      'name':'月光之钥',     },
    },
    20: {
        'TY9999D0001001'          : {'count':'1',        'name':'元特惠礼包',     },
        'TY9999D0002001'          : {'count':'20000',    'name':'金币',     },
        'TY9999D0006001'          : {'count':'60000',    'name':'金币',     },
        'TY9999D0030001'          : {'count':'360000',   'name':'金币',     },
        'TY9999D0050001'          : {'count':'650000',   'name':'金币',    },
        'TY9999D0100001'          : {'count':'1500000',  'name':'金币',    },
        'TY9999D0300001'          : {'count':'5000000',  'name':'金币',    },
        'TY9999D1000001'          : {'count':'20000000', 'name':'金币',   },
        'TY0006D0030002'          : {'count':'7',        'name':'天会员卡',   },
        'TY0006D0100002'          : {'count':'30',       'name':'天会员卡',  },
        'TY9999R0008001'          : {'count':'80',       'name':'钻石',     },
        'TY9999R0050001'          : {'count':'500',      'name':'钻石',     },
        'TY0006D0002001'          : {'count':'1',        'name':'月光之钥',    },
        'TY0006D0005001'          : {'count':'3',        'name':'月光之钥',      },
        'TY0006D0002002'          : {'count':'10',       'name':'参赛券',    },
        'TY0006D0000201'          : {'count':'10',       'name':'小喇叭',      },
        'TY0006D0050002'          : {'count':'1',        'name':'广播喇叭',    },
        'TY0006D0100003'          : {'count':'1',        'name':'改名卡'},
        'TY0006D0010001'          : {'count':'7',        'name':'记牌器',   },
        'TY9999D0008001'          : {'count':'1',        'name':'超值礼包',  },
        'TY9999D0006002'          : {'count':'6',        'name':'元转运礼包',   },
        'TY9999D0008002'          : {'count':'8',        'name':'元转运礼包',   },
    },
    21: {
        'TY9999R0000101'          : {'count':'1',    'name':'钻石',     },
        'TY9999D0002001'          : {'count':'20000',    'name':'金币',     },
        'TY9999D0005003'          : {'count':'50000',    'name':'金币',     },
        'TY9999D0006016'          : {'count':'60000',    'name':'金币',     },
        'TY9999R0008005'          : {'count':'80',      'name':'钻石',     },
        'TY9999D0001003'          : {'count':'1',    'name':'天会员',     },
        'TY9999D0012003'          : {'count':'30',    'name':'天会员',     },
        'TY9999D0030001'          : {'count':'36',   'name':'万金币',     },
        'TY9999D0030011'          : {'count':'30',   'name':'元转运礼包',    },
        'TY9999D0030012'          : {'count':'30',   'name':'元高手礼包',    },
        'TY9999R0050001'          : {'count':'500',  'name':'钻石',    },
        'TY9999D0050001'          : {'count':'65',  'name':'万金币',   },
        'TY9999D0050007'          : {'count':'50',   'name':'元转运礼包',   },
        'TY9999D0050008'          : {'count':'50',        'name':'元高手礼包',  },
        'TY9999D0100001'          : {'count':'150',       'name':'万金币',     },
        'TY9999R0100001'          : {'count':'1000',      'name':'钻石',     },
        'TY9999D0100011'          : {'count':'100',        'name':'元转运礼包',  },
        'TY9999D0100012'          : {'count':'100',        'name':'元高手礼包',   },
        'TY9999D0300001'          : {'count':'500',        'name':'万金币',   },
        'TY9999D1000001'          : {'count':'2000',        'name':'万金币',   },
        'TY9999D0008027'          : {'count':'80000',        'name':'金币',   },
        'TY9999D0008005'          : {'count':'80000',        'name':'金币',   },
        'TY9999D0008025'          : {'count':'8',        'name':'元高手限量特价礼包',     },
        'TY9999D0008026'          : {'count':'8',        'name':'元转运限量特价礼包',     },
        'TY9999D0008001'          : {'count':'8',        'name':'元超值礼包',     },
        'TY9999D0100001'          : {'count':'1500000',  'name':'金币',    },
        'TY9999D0010001'          : {'count':'100000',  'name':'金币',    },
        'TY9999D5000001'          : {'count':'1',        'name':'亿金币',   },
        'TY9999D0100019'          : {'count':'100',        'name':'元月卡',   },
    },
})

'''豌豆荚配置
'''
add_global_item('wannew_appkeys', {
    '100000293' : '83d78966187e4bea916552a61927bf62', # 斗地主
    '100000297' : 'f8f8dead01d59e8a19515b517107f182', # 赢三张
    '100035968' : '8baf6cbd68ace4b6b95539a58adf28d2', # 斗地主  
    '100036122' : '7a59015533375bef3807c3183e84940e', # 天天德州
    '100036124' : 'a640f84a264f3b7d42e20759d7dcd7ec', # 中国象棋
    '100036132' : 'd9bb08acafee3e05495b51eb8275a79a', # 保皇
    '100036112' : '555e547d0958f5989fadfa5824b5e5c4', # 途游斗地主
    '100037186' : '4de5dcb2eaf7d0eba528d38750acc6b7', # 军旗
    '100036130' : '3b9ce0a032222ccb84d3f9adbda33617', #五子棋
    '100036116' : 'f962b06fe1834a47ea3a5333e563ae18', #麻将
})

'''lenovo配置
'''
add_global_item('lenovo_appkeys', {
    '20017200000001200172' : 'RDNCMjAyOTlFQkU1NzdCMDI1NDRBRUIwMTc0NjlCNjM0NkZDNzM5QU1UQTJORFExTVRjeU9ERTNPRFl5T1RjNE5ERXJNVFUwTnpNek9EVTNNekV6TkRNd01UZzRORFkzTWpZeE5EZzVOamcyTnpBNE9UQTNPVFF6', #单机斗地主
    '1411021094360.app.ln' : 'RDEwQkE4NkQxNTY3N0M2MkM3MEM0NEZFNkIxMEEwNEZEOTJEMTdGM01UYzNNVE00TWprMU16STNNalUxTkRVek1Ua3JNakEwTURjNE5EazRNekF5TnpBeU9EQTNOell6TXpRNU5UWXpOell3TWpFeE5qSTROemM1', #大厅斗地主
    '1502060656046.app.ln' : 'b994ec75c94734f4', #大厅斗地主
    '1502110514680.app.ln' : 'b994ec75c94734f4', #大厅单机斗地主
    '20017200000003200172' : 'NjA1NDhGOEQ4RkIyMDIxOUNBNzcwNzZDOERGMzU0NUQ2MjQwQ0IwNU1UZ3pORGd6TXpVM09UTXpNREl6TVRBME1qRXJNVGM1T1RJME9UazNPVFUyTURBeE5EWXlOemMwTnpFME5EQTJPRFV3TURnMk9ETTJNVGM1', #单机麻将
    '1511120379045.app.ln' : 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAI0ufKZWkGPmZlhX156KCizxE0hWyWJQ7AtCxNcLLUGzIyYLDVu1CKMh4iwInoHXGHhNdtTZ4DNCj37ElXlo+4V87+9aNjFncEQE164R9FySli/HP65nXHzmz1u3gkbsGpunRMGs6Q9R8qmoNsvAlS4ya+k3PpMdzvHfTUMN3UgDAgMBAAECgYBdjlGx1KlIWjS2FDfham5Fy9dQV5qKGT/iUnOoYVKzN+dx3V8Tx4qat+ht76RCPGyNxB+b+2lz7oaypci7tNL/bWv0GKkYP2ZPWypI4lmkDjGPr4m5872U4v0pxq387lcggqmY6/T3ovVZ8wHeBx8W8IBvNiaHQ/wp/hJEl9u7MQJBAMRbURxnr6epojq3lKRoEq32iw/Njwrj56jF3dqUZmi+pDgnlK50PPplph1nU3H9iw0n+fzSDYngIR8sStH23hkCQQC4EMHLZU4XVQl96MiLFUjTvNQlA36Cp1L3EJod+/k1u1xqwdWSlxuE238Ckt3WRn2j3/3tFNSBLGi4RonWc2J7AkEAp7FdKicbCtOCqybRmT8QhOWDifGB8kkFNUwW1m/ariXyVcrn3b2Dvk1FeuMdjsJ8GLZFdzdlPJTfdKH9HCf7MQJAcEuQ3/UzOlrgCpftWaUnpD5MszQ5h55rqF3RmL90YAqprFwLX36fBGQhTcGqY6Ln3gW21mBh8VjVnq8yQspsZwJAekbw+qLJ5hqm/6xLY1/x3nDcyUhpZhaB8E4NELOdE0yZ0hkozZ9qzTgOuFjnb+zoLeXxQWpkRNeDvdrIP8JLyg==', #五子棋
    '1511261750466.app.ln' : 'MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALU7iBvcVVsQozfyPxC9OT94pBto',#保皇
    # 跑胡子
    '3003374445': 'MIICXgIBAAKBgQCNlcKjHEFcbbi6ipP02OtZ9LFcyqHhxMRT5Wp0Cnrgwj2u0WJvwRmenzMwBTEVAjYcSgtWZWVf4DArv6kzrP4TIr6rnQ9x0l95OuFRdFFlUEuTQERU1RhYeigH5XNIIVy/AAhrzyZiI2D5NJqVUUT3a0OnHTDROLNSwM/2Uhjr0wIDAQABAoGBAITL66QLU2665uHoKoAjmRNlg5mR4SYd5Tr/Wcp/LeNzrGE0uMwy5LG3hk5LAE9BJLmB5YJiViQH5YaTHMOARUkORTMJWIJv8Bq9V5+VNKCLWq9RFfC2uC3CdJfNudaYLdGiZ0C0qlikhtf11mq02GnWEwTF2qQKLAs0TyMZk08BAkEAwYphyTktVzRWwIse4CrVtSxzLxxxcR/9pZA6oBtc6BpTplkclpt4eayW19k5PdXOpdtdngm9miUYlSqtJToxgQJBALtG/8XNx98U4k96/SV0x3zsIT8f7RmPU89ucw7WWomoQ4KHS2gGL8Win7jhjxJTbpgu+R5ViMkhhudUpJ3cX1MCQGgGUgLO2aDqf8pjvEeunkkPyCVFO3AbSsDnYatWqbwTEmzxrp0AmWOEsVr45Xxn4/dfjdT41VD5qVnbo07EFYECQQCH5eSS4FnqqtfyvxfVx2E/aIZTrVI7mwNBYi/CE5BNljmvDYiNqvednf3zhlJxBPQbIPMLrRv+gALJ+WUfXJwbAkEAjtjQveztCpj4sE0Zwuk9qRZHUrP1hZqyiBd1xc8af1jcRE9aAng/D8GKeBZpU2Bejm58Csw6lIrU2re517hefQ==',
    #青岛棋牌
    '3005843213': 'MIICXgIBAAKBgQCPL+8V8tvksv/zAGRf4R0O1r2KZ9UH36HyKsAOYwKWxWo48oT47rmPX3ScfH83K8sd6N4mx2oqWNZrvkE0DfsM7bbcxih/jtPeVrlwbEULkbrP2ycMmHBsf/WZS+DCddQEUKAfsDVI4COJ8xJjNW3cJUbEV5TMRLNYxEZQyCFRewIDAQABAoGBAIdFh5+6sh',
})

add_global_item('lenovo_prodids', {
    6: {
        'TY9999R00020DJ'          : {'feecode':'9999',     'name':'银币',     },
        'TY9999D0001001'          : {'feecode':'2',        'name':'1元特惠礼包',     },
        'TY9999D0002001'          : {'feecode':'24',       'name':'20000金币',     },
        'TY9999D0006001'          : {'feecode':'3',        'name':'60000金币',     },
        'TY9999D0030001'          : {'feecode':'4',        'name':'360000金币',     },
        'TY9999D0050001'          : {'feecode':'5',        'name':'650000金币',    },
        'TY9999D0100001'          : {'feecode':'6',        'name':'1500000金币',    },
        'TY9999D0300001'          : {'feecode':'7',        'name':'5000000金币',    },
        'TY9999D1000001'          : {'feecode':'8',        'name':'2000万金币',   },
        'TY0006D0030002'          : {'feecode':'9',        'name':'7天会员卡',   },
        'TY0006D0100002'          : {'feecode':'10',       'name':'30天会员卡',  },
        'TY9999R0008001'          : {'feecode':'11',       'name':'80钻石',     },
        'TY9999R0050001'          : {'feecode':'12',       'name':'500钻石',     },
        'TY0006D0002001'          : {'feecode':'14',       'name':'月光之钥',    },
        'TY0006D0005001'          : {'feecode':'15',       'name':'月光之钥x3',      },
        'TY0006D0002002'          : {'feecode':'16',       'name':'参赛券x10',    },
        'TY0006D0000201'          : {'feecode':'17',       'name':'小喇叭x10',      },
        'TY0006D0050002'          : {'feecode':'18',       'name':'广播喇叭',    },
        'TY0006D0100003'          : {'feecode':'19',       'name':'改名卡'},
        'TY0006D0010001'          : {'feecode':'20',       'name':'记牌器x7',   },
        'TY9999D0008001'          : {'feecode':'21',       'name':'超值礼包',  },
        #'TY9999D0006002'          : {'feecode':'1',        'name':'6元转运礼包',   },
        'TY9999D0008002'          : {'feecode':'22',       'name':'8元转运礼包',   },
        'TY9999R0100001'          : {'feecode':'25',       'name':'1000钻石',     },
    },
    7: {
        'TY0007D0030001'          : {'feecode':'2',        'name':'300000金币',     },
        'TY0007D0050001'          : {'feecode':'3',        'name':'500000金币',    },
        'TY0007D0100001'          : {'feecode':'4',        'name':'1000000金币',    },
        'TY0007D0300001'          : {'feecode':'5',        'name':'3000000金币',    },
        'TY0007D1000001'          : {'feecode':'6',        'name':'1000万金币',   },
        'TY0007D0030002'          : {'feecode':'1',        'name':'7天会员卡',   },
        'TY0007D0100002'          : {'feecode':'7',       'name':'30天会员卡',  },
        'TY9999R0050001'          : {'feecode':'8',       'name':'500钻石',     },
        'TY0007D0008001'          : {'feecode':'9',       'name':'80000金币',     },
        'TY0007D0010001'          : {'feecode':'10',       'name':'100000金币',     },
        'TY9999R0008001'          : {'feecode':'11',       'name':'80钻石',     },
        'TY9999D0008001'          : {'feecode':'12',       'name':'超值礼包',     },
        'TY9999D0008002'          : {'feecode':'13',       'name':'8元转运礼包',     },
        'TY9999R0100001'          : {'feecode':'24',       'name':'1000钻石',     },
    },
    9999: {
        'TY9999D0006001'          : {'feecode':'3',        'name':'60000金币',     },
        'TY9999D0006016'          : {'feecode':'3',        'name':'60000金币',     },
        'TY9999R0000101'          : {'feecode':'26',    'name':'钻石',     },
        'TY9999D0001003'          : {'feecode':'27',    'name':'天会员',     },
        'TY9999D0012003'          : {'feecode':'34',    'name':'天会员',     },
        'TY9999D0002001'          : {'feecode':'24',       'name':'20000金币', },
        'TY9999R0008001'          : {'feecode':'11',       'name':'80钻石',     },
        'TY9999D0030001'          : {'feecode':'4',   'name':'万金币',     },
        'TY9999D0030011'          : {'feecode':'35',   'name':'元转运礼包',    },
        'TY9999D0030012'          : {'feecode':'36',   'name':'元高手礼包',    },
        'TY9999R0050001'          : {'feecode':'12',  'name':'钻石',    },
        'TY9999D0050001'          : {'feecode':'5',  'name':'万金币',   },
        'TY9999D0050007'          : {'feecode':'37',   'name':'元转运礼包',   },
        'TY9999D0050008'          : {'feecode':'38',        'name':'元高手礼包',  },
        'TY9999D0100001'          : {'feecode':'6',       'name':'万金币',     },
        'TY9999R0100001'          : {'feecode':'25',      'name':'钻石',     },
        'TY9999D0100011'          : {'feecode':'39',        'name':'元转运礼包',  },
        'TY9999D0100012'          : {'feecode':'40',        'name':'元高手礼包',   },
        'TY9999D0300001'          : {'feecode':'7',        'name':'万金币',   },
        'TY9999D1000001'          : {'feecode':'8',        'name':'万金币',   },
        'TY9999D0008027'          : {'feecode':'30',        'name':'金币',   },
        'TY9999D0008005'          : {'feecode':'30',        'name':'金币',   },
        'TY9999D0010001'          : {'feecode':'41',        'name':'100000金币',    },
        'TY9999D0008026'          : {'feecode':'32',        'name':'转运限量特价礼包',   },
        'TY9999D0008025'          : {'feecode':'33',        'name':'高手限量特价礼包',   },
        'TY9999D0008001'          : {'feecode':'31',        'name':'8元超值礼包',   },
        'TY9999D0005003'          : {'feecode':'29',       'name':'50000金币',     },
        'TY9999R0008005'          : {'feecode':'11',       'name':'80钻石',     },
    },
    #象棋lenovo配置
    '5000013955': {
        'TY9999D0002001'          : {'feecode':'29201',       'name':'20000金币',     },
        'TY9999D0300001'          : {'feecode':'10981',        'name':'5000000金币',    },
        'TY9999D1000001'          : {'feecode':'10982',        'name':'2000万金币',   },
        'TY9999R0050001'          : {'feecode':'10984',       'name':'500钻石',     },
        'TY9999D0005003'          : {'feecode':'29195',       'name':'50000金币',     },
        'TY9999R0100001'          : {'feecode':'29202',       'name':'1000钻石',     },
        'TY9999R0000101'          : {'feecode':'29193',    'name':'1钻石',     },
        'TY9999D0001003'          : {'feecode':'29194',    'name':'1天会员',     },
        'TY9999D0012003'          : {'feecode':'29206',    'name':'30天会员',     },
        'TY9999D0030001'          : {'feecode':'10978',   'name':'36万金币',     },
        'TY9999D0030011'          : {'feecode':'29203',   'name':'转运礼包',    },
        'TY9999D0030012'          : {'feecode':'29207',   'name':'高手礼包',    },
        'TY9999D0050001'          : {'feecode':'10979',  'name':'65万金币',   },
        'TY9999D0050007'          : {'feecode':'29204',   'name':'转运礼包',   },
        'TY9999D0050008'          : {'feecode':'29208',        'name':'高手礼包',  },
        'TY9999D0100001'          : {'feecode':'10980',       'name':'150万金币',     },
        'TY9999D0100011'          : {'feecode':'29205',        'name':'转运礼包',  },
        'TY9999D0100012'          : {'feecode':'29209',        'name':'高手礼包',   },
        'TY9999D0008025'          : {'feecode':'29198',        'name':'高手限量特价礼包',     },
        'TY9999D0008026'          : {'feecode':'29199',        'name':'转运限量特价礼包',     },
        'TY9999D0006016'          : {'feecode':'10977',        'name':'60000金币',     },
        'TY9999R0008005'          : {'feecode':'10983',       'name':'80钻石',     },
        'TY9999D0008027'          : {'feecode':'29196',       'name':'80000金币',     },
        'TY9999D0008001'          : {'feecode':'29197',       'name':'8元超值礼包',     },
        'TY9999D0010001'          : {'feecode':'29200',        'name':'100000金币',    },
    },
    '20017200000003200172': {
        'TY0007D0030001'          : {'feecode':'2',        'name':'300000金币',     },
        'TY0007D0050001'          : {'feecode':'3',        'name':'500000金币',    },
        'TY0007D0100001'          : {'feecode':'4',        'name':'1000000金币',    },
        'TY0007D0300001'          : {'feecode':'5',        'name':'3000000金币',    },
        'TY0007D1000001'          : {'feecode':'6',        'name':'1000万金币',   },
        'TY0007D0030002'          : {'feecode':'1',        'name':'7天会员卡',   },
        'TY0007D0100002'          : {'feecode':'7',       'name':'30天会员卡',  },
        'TY9999R0050001'          : {'feecode':'8',       'name':'500钻石',     },
        'TY0007D0008001'          : {'feecode':'9',       'name':'80000金币',     },
        'TY0007D0010001'          : {'feecode':'10',       'name':'100000金币',     },
        'TY9999R0008001'          : {'feecode':'11',       'name':'80钻石',     },
        'TY9999D0008001'          : {'feecode':'12',       'name':'超值礼包',     },
        'TY9999D0008002'          : {'feecode':'13',       'name':'8元转运礼包',     },
        'TY9999R0100001'          : {'feecode':'25',       'name':'1000钻石',     },
    },
    '20017200000001200172': {
        'TY9999R00020DJ'          : {'feecode':'9999',     'name':'银币',     },
        'TY9999D0001001'          : {'feecode':'2',        'name':'1元特惠礼包',     },
        'TY9999D0002001'          : {'feecode':'24',       'name':'20000金币',     },
        'TY9999D0006001'          : {'feecode':'3',        'name':'60000金币',     },
        'TY9999D0030001'          : {'feecode':'4',        'name':'360000金币',     },
        'TY9999D0050001'          : {'feecode':'5',        'name':'650000金币',    },
        'TY9999D0100001'          : {'feecode':'6',        'name':'1500000金币',    },
        'TY9999D0300001'          : {'feecode':'7',        'name':'5000000金币',    },
        'TY9999D1000001'          : {'feecode':'8',        'name':'2000万金币',   },
        'TY0006D0030002'          : {'feecode':'9',        'name':'7天会员卡',   },
        'TY0006D0100002'          : {'feecode':'10',       'name':'30天会员卡',  },
        'TY9999R0008001'          : {'feecode':'11',       'name':'80钻石',     },
        'TY9999R0050001'          : {'feecode':'12',       'name':'500钻石',     },
        'TY0006D0002001'          : {'feecode':'14',       'name':'月光之钥',    },
        'TY0006D0005001'          : {'feecode':'15',       'name':'月光之钥x3',      },
        'TY0006D0002002'          : {'feecode':'16',       'name':'参赛券x10',    },
        'TY0006D0000201'          : {'feecode':'17',       'name':'小喇叭x10',      },
        'TY0006D0050002'          : {'feecode':'18',       'name':'广播喇叭',    },
        'TY0006D0100003'          : {'feecode':'19',       'name':'改名卡'},
        'TY0006D0010001'          : {'feecode':'20',       'name':'记牌器x7',   },
        'TY9999D0008001'          : {'feecode':'21',       'name':'超值礼包',  },
        #'TY9999D0006002'          : {'feecode':'1',        'name':'6元转运礼包',   },
        'TY9999D0008002'          : {'feecode':'22',       'name':'8元转运礼包',   },
        'TY9999D0006016'          : {'feecode':'3',        'name':'60000金币',     },
        'TY9999R0100001'          : {'feecode':'25',       'name':'1000钻石',     },
        'TY9999R0000101'          : {'feecode':'26',    'name':'钻石',     },
        'TY9999D0001003'          : {'feecode':'27',    'name':'天会员',     },
        'TY9999D0012003'          : {'feecode':'34',    'name':'天会员',     },
        'TY9999D0030001'          : {'feecode':'4',   'name':'万金币',     },
        'TY9999D0030011'          : {'feecode':'35',   'name':'元转运礼包',    },
        'TY9999D0030012'          : {'feecode':'36',   'name':'元高手礼包',    },
        'TY9999R0050001'          : {'feecode':'12',  'name':'钻石',    },
        'TY9999D0050001'          : {'feecode':'5',  'name':'万金币',   },
        'TY9999D0050007'          : {'feecode':'37',   'name':'元转运礼包',   },
        'TY9999D0050008'          : {'feecode':'38',        'name':'元高手礼包',  },
        'TY9999D0100001'          : {'feecode':'6',       'name':'万金币',     },
        'TY9999R0100001'          : {'feecode':'25',      'name':'钻石',     },
        'TY9999D0100011'          : {'feecode':'39',        'name':'元转运礼包',  },
        'TY9999D0100012'          : {'feecode':'40',        'name':'元高手礼包',   },
        'TY9999D0300001'          : {'feecode':'7',        'name':'万金币',   },
        'TY9999D1000001'          : {'feecode':'8',        'name':'万金币',   },
        'TY9999D0008027'          : {'feecode':'30',        'name':'金币',   },
        'TY9999D0008005'          : {'feecode':'30',        'name':'金币',   },
        'TY9999D0008026'          : {'feecode':'32',        'name':'转运限量特价礼包',   },
        'TY9999D0008025'          : {'feecode':'33',        'name':'高手限量特价礼包',   },
        'TY9999D0008001'          : {'feecode':'31',        'name':'8元超值礼包',   },
        'TY9999D0005003'          : {'feecode':'29',       'name':'50000金币',     },
        'TY9999R0008005'          : {'feecode':'11',       'name':'80钻石',     },
    },
    '1411021094360.app.ln': {
        'TY9999D0001001'          : {'feecode':'2',        'name':'1元特惠礼包',     },
        'TY9999D0002001'          : {'feecode':'24',       'name':'20000金币',     },
        'TY9999D0006001'          : {'feecode':'3',        'name':'60000金币',     },
        'TY9999D0030001'          : {'feecode':'4',        'name':'360000金币',     },
        'TY9999D0050001'          : {'feecode':'5',        'name':'650000金币',    },
        'TY9999D0100001'          : {'feecode':'6',        'name':'1500000金币',    },
        'TY9999D0300001'          : {'feecode':'7',        'name':'5000000金币',    },
        'TY9999D1000001'          : {'feecode':'8',        'name':'2000万金币',   },
        'TY0006D0030002'          : {'feecode':'9',        'name':'7天会员卡',   },
        'TY0006D0100002'          : {'feecode':'10',       'name':'30天会员卡',  },
        'TY9999R0008001'          : {'feecode':'11',       'name':'80钻石',     },
        'TY9999R0050001'          : {'feecode':'12',       'name':'500钻石',     },
        'TY0006D0002001'          : {'feecode':'14',       'name':'月光之钥',    },
        'TY0006D0005001'          : {'feecode':'15',       'name':'月光之钥x3',      },
        'TY0006D0002002'          : {'feecode':'16',       'name':'参赛券x10',    },
        'TY0006D0000201'          : {'feecode':'17',       'name':'小喇叭x10',      },
        'TY0006D0050002'          : {'feecode':'18',       'name':'广播喇叭',    },
        'TY0006D0100003'          : {'feecode':'19',       'name':'改名卡'},
        'TY0006D0010001'          : {'feecode':'20',       'name':'记牌器x7',   },
        'TY9999D0008001'          : {'feecode':'21',       'name':'超值礼包',  },
        #'TY9999D0006002'          : {'feecode':'1',        'name':'6元转运礼包',   },
        'TY9999D0005003'          : {'feecode':'30',       'name':'50000金币',     },
        'TY9999D0008002'          : {'feecode':'22',       'name':'8元转运礼包',   },
        'TY9999R0100001'          : {'feecode':'25',       'name':'1000钻石',     },
        'TY9999R0000101'          : {'feecode':'28',    'name':'1钻石',     },
        'TY9999D0001003'          : {'feecode':'26',    'name':'1天会员',     },
        'TY9999D0012003'          : {'feecode':'34',    'name':'30天会员',     },
        'TY9999D0030001'          : {'feecode':'4',   'name':'36万金币',     },
        'TY9999D0030011'          : {'feecode':'35',   'name':'转运礼包',    },
        'TY9999D0030012'          : {'feecode':'36',   'name':'高手礼包',    },
        'TY9999R0050001'          : {'feecode':'12',  'name':'500钻石',    },
        'TY9999D0050001'          : {'feecode':'5',  'name':'65万金币',   },
        'TY9999D0050007'          : {'feecode':'37',   'name':'转运礼包',   },
        'TY9999D0050008'          : {'feecode':'38',        'name':'高手礼包',  },
        'TY9999D0100001'          : {'feecode':'6',       'name':'150万金币',     },
        'TY9999R0100001'          : {'feecode':'25',      'name':'1000钻石',     },
        'TY9999D0100011'          : {'feecode':'39',        'name':'转运礼包',  },
        'TY9999D0100012'          : {'feecode':'40',        'name':'高手礼包',   },
        'TY9999D0300001'          : {'feecode':'7',        'name':'500万金币',   },
        'TY9999D1000001'          : {'feecode':'8',        'name':'2000万金币',   },
        'TY9999D0008025'          : {'feecode':'33',        'name':'高手限量特价礼包',     },
        'TY9999D0008026'          : {'feecode':'34',        'name':'转运限量特价礼包',     },
        'TY9999D0006016'          : {'feecode':'3',        'name':'60000金币',     },
        'TY9999R0008005'          : {'feecode':'11',       'name':'80钻石',     },
        'TY9999D0008005'          : {'feecode':'31',       'name':'80000金币',     },
        'TY9999D0008027'          : {'feecode':'31',       'name':'80000金币',     },
        'TY9999D0008001'          : {'feecode':'32',       'name':'8元超值礼包',     },
        'TY9999D0010001'          : {'feecode':'41',        'name':'100000金币',    },
    },
    #五子棋
    '1511120379045.app.ln': {
        'TY9999D0006001'          : {'feecode':'31020',        'name':'60000金币',     },
        'TY9999D0030001'          : {'feecode':'31021',        'name':'360000金币',     },
        'TY9999D0050001'          : {'feecode':'31022',        'name':'650000金币',    },
        'TY9999D0100001'          : {'feecode':'31023',        'name':'1500000金币',    },
        'TY9999D0300001'          : {'feecode':'31024',        'name':'5000000金币',    },
        'TY9999D1000001'          : {'feecode':'31025',        'name':'2000万金币',   },
        'TY9999R0008001'          : {'feecode':'31026',       'name':'80钻石',     },
        'TY9999R0050001'          : {'feecode':'31027',       'name':'500钻石',     },
        'TY9999R0100001'          : {'feecode':'31028',       'name':'1000钻石',     },
        'TY9999D0008001'          : {'feecode':'31029',       'name':'8元超值礼包',     },
    },
    #跑胡子
    '3003374445': {
        'TY9999D0002001'          : {'feecode':'1',        'name':'20000金币',     },
        'TY9999D0006001'          : {'feecode':'2',        'name':'60000金币',     },
        'TY9999D0030001'          : {'feecode':'3',        'name':'36万金币',    },
        'TY9999D0050001'          : {'feecode':'4',        'name':'65万金币',    },
        'TY9999D0100001'          : {'feecode':'5',        'name':'150万金币',    },
        'TY9999D0300001'          : {'feecode':'6',        'name':'500万金币',   },
        'TY9999D1000001'          : {'feecode':'10',       'name':'2000万金币',     },
        'TY9999R0008005'          : {'feecode':'7',       'name':'80钻石',     },
        'TY9999R0050001'          : {'feecode':'8',       'name':'500钻石',     },
        'TY9999R0100001'          : {'feecode':'9',       'name':'1000钻石',     },
    },
    # 永恒
    '10049':{
        '1'          : {'feecode':'1',        'name':'60钻',     },
        '2'          : {'feecode':'2',        'name':'300钻',     },
        '3'          : {'feecode':'3',        'name':'680钻',    },
        '4'          : {'feecode':'4',        'name':'1280钻',    },
        '5'          : {'feecode':'5',        'name':'3280钻',    },
        '6'          : {'feecode':'6',        'name':'6480钻',   },
    }
})
add_global_item('jinli_config', [
                {
                    'appKey' : '8DA906030BCC4DA5912005B351EF0E09',
                    'publicKey' : '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkU9fQ+jFROqSXgNt79bdFNEQn
Jb1xSmQWEwCY7jw8xmHe+PLZ0DeOahT0obMwI7Bu6tcN1xD8m91nD2AEZ5nQYB2Q
ywI33OaRIe5DMb614+7mhEK1SMdZbrxw7TF/W8ajsW8HEOIw6kv8qZOMnwVk3G2z
FIvUhzhY+zptdAsUowIDAQAB
-----END PUBLIC KEY-----'''
                },#象棋
                {
                    'appKey' : 'CCF2C1015F86408EA4227C96125C34AB',
                    'publicKey' : '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCeJl4Tb7mYtQb9u7/q9n4EjfM9
qZZdD7Uy4ME5gQ6P4oUZOXqWNCY/If5JNt9zppPfkmcTMCBOkkRPAnTinyh/nLft
dDClMaK2xbVgX5RBS178YQzlq7iGcGs7uLSu9Fg/BDeFgJopnt0jbaBfAYeTWCBa
mDYkFQxpv2CN0O6DeQIDAQAB
-----END PUBLIC KEY-----'''
                },#地主
                {
                    'appKey' : 'D52DA2FAC8BE41068836A7D6CF34A8A7',
                    'publicKey' : '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkRdK/11kVXK2A2lEK05WJBI21
VwTdULyqC2NzqfVZ6aRny7ewlBM8Y0GxXMXaesyo1paYg2FbNigAj1Y15/x0mxpm
kio6HKUMyeSLKdbyC20SZEINAiNXY0fgahDYCsqLl7n1CiLAIUJ6W0Dpe8fsdvZz
0Htk+EwhojxrKehlIQIDAQAB
-----END PUBLIC KEY-----'''
                },#军旗
                {
                    'appKey' : 'E45324F8D86742E096839BDD014969C4',
                    'publicKey' : '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkFmk4kG7Cvb8ny7SZSeW+rrz6
778yKrleJ7yeJNjbJf4f9xZI7SypGMd85oOXw/tPpbVo0STxIMsb3ng1WqIEvxZP
BRo36zNfTO2/IJQ2hNcyz3IuEG7R9Bu7pqMfPRT8Z8sqWSdKzTMYBa9SHIa/nTjk
Lwy9j3Pe2kV33/VASQIDAQAB
-----END PUBLIC KEY-----'''
                },#五子棋
])
                
add_global_item('lenovodanji_config', [
                {
                    'appId' : '1411021094360.app.ln',
                    'appKey' : '''-----BEGIN PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBANGy3VqetHXO7XERUog+lVDFMyKT
EaS4mhUjSzXq77bsEUzpdClq9NRbGQHsnJEavcJJPBLaFPGXMEBsEl2qCwaQfCZk3Cz5pV2ylCUB
ZxUprONHqFt9YB4/eM4RlyGYhJoQuo6WOyDdTODzrqszR6IJ6plxinviEsTw6PrtvqHbAgMBAAEC
gYEAxT4Ez1QwUg+Nb6jnhJe5Qvv6GS9UjSfGZtOHzvNo/xoVO87rIHomSAhYAWNZ8XLBwpm4E9Nl
l8ip7i65J7jmHFSlOMh8Zkkl9adCkb6YVeaOLxJI22IpySRKd5CsIB/2iOp7CAK/hZMkKv/uCuoT
9TNXgN37Jz0/4WMBvYJPyAECQQD/VJbTbL81xA5Cgr1wyT/QG1es7rrGJmS2qccGf4ncLajLxoww
ij6077uAbCXmaPN0IAfqhKdOAceCgyNXIK8BAkEA0j+kPgpi1A8HuIbG/kKvGSHTfz/9y0mO81LG
JU5wzEaPUttye/xMYJHpg/d5ha+XYbpWkSfcv+QlASXE93Ts2wJBAKbNXhMVEf1P7Xjp7FSIRNXx
Zt+kvgPBBT6Hv2uxWiCq+4DUXrU/OyP9EWMeQ8w4eAM/AazlqF6/rtTGUwoSYgECQQCQVPwtUvfx
V7gXJv7ogWKuwBfu3UEfEwo9Y+9+oNCyiyXM3bVEBDlyefhyjasw6Q/lGQRgdZsHaFk25nTG48/N
AkAjKBKJBQyfadjYOdNc8sW5JeSBF44i4MT4SrXAkFo7Tx4IQdmdpndHQXLOgepVKV7MVLVso0pw
o2igUdQppwDN
-----END PRIVATE KEY-----'''
                },
                {
                    'appId' : '1511100892459.app.ln',
                    'appKey' : '''-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAJmC3eu0k2dn27lIBFJ9CHrdY3jf
HFBaNZERQB4RqtZ9ua5COrnzVjPSfGRx1nbHPpeY/2TlHxQS41vZ885T1p6vPGeV5HiBff0AscyP
dm9KWCrdO9r1gj5uXA5LHZkrdopv1XzfV631CtU5Nr55H49IPyR5wa0V0+oCIcYyksJ9AgMBAAEC
gYADpaVKFUcvPLtuonRf1VKfQKU9WOeeTRZatPM2A6twXxpLNo2Yn1xb7NNBu6ahucgV5++hYQQl
APHf28S8ESfXIbj+wHWrdJOYQN/gHwRLcJoeUW3KTNkiHaT0XJqzOUiLuTMBR0zyzp59Upi7uSvZ
CxpzUC+nMAAz+dBb/PUEzQJBAOu7SWQZVz90oWhYEEWcI8fwHmaCyo7ukPHMHyz4VTADZ9BLwZEt
6qFU5q1If9J338GB64N/egb/aYr63QJpfPsCQQCmtdGAJuO5j40sJEzUjcPhg1r3R9L3r/awgcsE
pobnQ536q7ATGXfD9bxifOhYyoHTcQcz69FzOcmhBg9IADTnAkB9D7qK+Yq5JpYvNnFDjOfKvhBS
0FbIZ7bMIT/06ra/Jz9fWaGS9SpCdzl+ezUdIu25ysR42huSNNT4n8i6694bAkEAoN/2Eq/0s93G
guFozvkbHOVQhC5odKL28O/fhVZZ+pQywHKr0FKUU6Mwru4QnZaWX//DzqPzlDkgzOX3Gykv4wJA
d7dn+SzYKZH/aJqt+Zx0fQ3p3+YOctYB5NpJlS+XhKVkhylwo5aY/GWJVVCpsqcUrfNjvh4gYqKO
H3pcYyzLLA==
-----END PRIVATE KEY-----'''
                },
                {
                    'appId' : '1508240756765.app.ln',
                    'appKey' : '''-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAMUgNw5kLoE/EG5BsqgVLukySMLM
sc9g3G/JqXOlePkwsavgF0Euu2vbFias1Sl315ytgQTP+zynHJSiCJeM/uj19kE1n+DUTgB3LZY1
Yo01NPG5d/Q4sJ3NG2pPoxz+xuaunJhOdlL+i0BDxHLebyya2k4ZUrli7bgSp4sJiv2fAgMBAAEC
gYA3XyI396ocggNyhR/TGQgxVv+bQHZd4z5oZEQmCQAfNy9hMTQ3ChJ5bHQfbwL9f/1ftFj+ahGP
av2bPpydPWzIsww3Dtr16/+h02bag3YEIRtHXtsnDamoTV4HPI7k4+NHzYHWpZ/6e4gFkspgvMJb
b1hSfDrsUszY80nkUVxogQJBAO4GU+cpvDyhWggMBggXTFBbRxaSIvuJIkmLYJ7UPhiz5l+hJSPX
cd6XogwVLlz2ORLo4256qBdxLctRvjQxX18CQQDUAzMWR69u1oY2ftViSIUIZyDLuBvZMz9lmqBC
YHZ607C9bjrW+tNyqLCTjMlkUtwBfKmHoLL5AZWqfSV34EnBAkARZocFtChdqlIBmpdqSgG7MiEN
RlumVc0a4USL9+oeNjCWNxqW9y4M3rrq9TVxeFKNzlaqAe993zlAztX/zMgzAkBvU4LG5ztyewkc
onsP0b6xS93Hu1Q8OBHJG2mdkSOFmZUL007oRes0IOofgGTb3jqSOVCX3EU+RZu+W1qKWObBAkEA
0qcmJzfoiotoETkDMY6mo9YuBg3xO8FhEJ9ZGNr1mpSAl3nQYf1EIriAhAGy/oEkCMTQZdG7UzzN
EiiDBNylRA==
-----END PRIVATE KEY-----'''
                },
                {
                    'appId' : '1511261750466.app.ln',
                    'appKey' : '''-----BEGIN PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBALU7iBvcVVsQozfyPxC9OT94pBto
VzMaJinLhO3OI538MdpKN+/wPDD4bMTFqslfGREGauWkoksZUQeMXfPZSn0kWUuKNXhsDcjy9dnE
0J7NXrJQE4iy/NuwUhE3odjk6rTc3kixgB397DqlPL3YJTD4blY2J0y2V6zumn5SS/wnAgMBAAEC
gYEArWrsv/Qi/QO7mxJDxIm8mP6g0dUS88RG1mF3rnI9ZLRpI783LXJMtnNQ6S1YUl6cRs1ERsA1
x/TOs5FeabL38YzyxG1mgS1j1uIoA6L3MPtQZ9nalKl32VmkKU0T+lXVVlqN/qTO/JDPrFa0J6uC
kumb9jSKcvzZU3TtMbQazhkCQQD4uPOiPcMKx86em1Kpovi/ZBSdTb0ACUGmJc+/u4yO1Ve2Ze+m
8r/7+EWaSFlPQC8tFF1AekH1pOlrTTb115IlAkEAuokMeFoUV0nF8DaQc1BpvN4nc6S5Og8ExXu+
s6El1m8Ov2SGFMWCKRvOpNcMVvv/EAXmZEXXY5gHLLUKxpYVWwJBAKBD5NE1BNmMeAnhQbmHBsuk
fFgEAHXmgQPDN4NvIRnkRHmGY47qumRszMSmO84CKKPejFwAq0HSeommnnR47HUCQEs2YVHRuGvt
siMGTT5ByTC/PpcRbyIq1hiuqZkSPAh3ZTHk3W9Yp//dV3f9wdr85r5WMqxxwMRGk3YCVaL29wsC
QQCfqyXOmGB58GH7wHYqe2kjtfrEJxPy/0mEc8js7eVKks+ggDOm62h+V0P5ASzNTtETkplGIxGy
FikIkh2cN2oQ
-----END PRIVATE KEY-----'''
                },
])

add_global_item('lenovodanji_prodids', {
    '6': {
        'TY9999R00020DJ' : {'feecode':'9999', 'name':'银币',  'bgname':'bg1.png', 'okname':'', 'cancelname':''  },
        'TY9999D0008003' : {'feecode':'1',  'name':'超值豪华礼包', 'bgname':'bg1.png', 'okname':'', 'cancelname':''   },
        'TY9999D0008004' : {'feecode':'2',  'name':'转运大礼包', 'bgname':'bg2.png', 'okname':'', 'cancelname':''  },
        'TY9999D0006006' : {'feecode':'3',   'name':'60000金币',   'bgname':'bg3.png', 'okname':'', 'cancelname':''  },
        'TY9999D0030002' : {'feecode':'4',   'name':'300000金币',  'bgname':'bg4.png', 'okname':'', 'cancelname':''  },
        'TY9999R0008001' : {'feecode':'8',   'name':'80钻石',      'bgname':'bg5.png', 'okname':'', 'cancelname':'' },
    },
    '1502060656046.app.ln': {
        'TY9999R00020DJ' : {'feecode':'9999', 'name':'银币',  'bgname':'bg1.png', 'okname':'', 'cancelname':''  },
        'TY9999D0008003' : {'feecode':'1',  'name':'超值豪华礼包', 'bgname':'bg1.png', 'okname':'', 'cancelname':''   },
        'TY9999D0008004' : {'feecode':'2',  'name':'转运大礼包', 'bgname':'bg2.png', 'okname':'', 'cancelname':''  },
        'TY9999D0006006' : {'feecode':'3',   'name':'60000金币',   'bgname':'bg3.png', 'okname':'', 'cancelname':''  },
        'TY9999D0030002' : {'feecode':'4',   'name':'300000金币',  'bgname':'bg4.png', 'okname':'', 'cancelname':''  },
        'TY9999R0008001' : {'feecode':'8',   'name':'80钻石',      'bgname':'bg5.png', 'okname':'', 'cancelname':'' },
    },
    '1502110514680.app.ln': {
        'TY9999R00020DJ' : {'feecode':'9999', 'name':'银币',  'bgname':'bg1.png', 'okname':'', 'cancelname':''  },
        'TY9999D0008003' : {'feecode':'1',  'name':'超值豪华礼包', 'bgname':'bg1.png', 'okname':'', 'cancelname':''   },
        'TY9999D0008004' : {'feecode':'2',  'name':'转运大礼包', 'bgname':'bg2.png', 'okname':'', 'cancelname':''  },
        'TY9999D0006006' : {'feecode':'3',   'name':'60000金币',   'bgname':'bg3.png', 'okname':'', 'cancelname':''  },
        'TY9999D0030002' : {'feecode':'4',   'name':'300000金币',  'bgname':'bg4.png', 'okname':'', 'cancelname':''  },
        'TY9999R0008001' : {'feecode':'8',   'name':'80钻石',      'bgname':'bg5.png', 'okname':'', 'cancelname':'' },
    },
    '1511100892459.app.ln': {
        'TY9999R0000101' : {'feecode':'29165' },
        'TY9999D0001003' : {'feecode':'29166' },
        'TY9999D0002001' : {'feecode':'29167' },
        'TY9999D0005003' : {'feecode':'29168' },
        'TY9999D0006016' : {'feecode':'29169' },
        'TY9999D0008005' : {'feecode':'29170' },
        'TY9999D0008027' : {'feecode':'29170' },
        'TY9999R0008005' : {'feecode':'29171' },
        'TY9999D0008001' : {'feecode':'29172' },
        'TY9999D0008026' : {'feecode':'29173' },
        'TY9999D0008025' : {'feecode':'29174' },
        'TY9999D0012003' : {'feecode':'29175' },
        'TY9999D0030001' : {'feecode':'29176' },
        'TY9999D0030011' : {'feecode':'29177' },
        'TY9999D0030012' : {'feecode':'29178' },
        'TY9999R0050001' : {'feecode':'29179' },
        'TY9999D0050001' : {'feecode':'29180' },
        'TY9999D0050007' : {'feecode':'29181' },
        'TY9999D0050008' : {'feecode':'29182' },
        'TY9999D0100001' : {'feecode':'29183' },
        'TY9999R0100001' : {'feecode':'29184' },
        'TY9999D0100011' : {'feecode':'29185' },
        'TY9999D0100012' : {'feecode':'29186' },
        'TY9999D0300001' : {'feecode':'29187' },
        'TY9999D1000001' : {'feecode':'29188' },
        'TY9999D0010001' : {'feecode':'29189' },
    },
    '1508240756765.app.ln': {
        'TY9999R0000101' : {'feecode':'29193' },
        'TY9999D0001003' : {'feecode':'29194' },
        'TY9999D0002001' : {'feecode':'29201' },
        'TY9999D0005003' : {'feecode':'29195' },
        'TY9999D0006016' : {'feecode':'10977' },
        'TY9999D0008005' : {'feecode':'10983' },
        'TY9999D0008027' : {'feecode':'29196' },
        'TY9999R0008005' : {'feecode':'29171' },
        'TY9999D0008001' : {'feecode':'29197' },
        'TY9999D0008026' : {'feecode':'29199' },
        'TY9999D0008025' : {'feecode':'29198' },
        'TY9999D0012003' : {'feecode':'29175' },
        'TY9999D0030001' : {'feecode':'10978' },
        'TY9999D0030011' : {'feecode':'29203' },
        'TY9999D0030012' : {'feecode':'29207' },
        'TY9999R0050001' : {'feecode':'10979' },
        'TY9999D0050001' : {'feecode':'29180' },
        'TY9999D0050007' : {'feecode':'29204' },
        'TY9999D0050008' : {'feecode':'29208' },
        'TY9999D0100001' : {'feecode':'10980' },
        'TY9999R0100001' : {'feecode':'29184' },
        'TY9999D0100011' : {'feecode':'29205' },
        'TY9999D0100012' : {'feecode':'29209' },
        'TY9999D0300001' : {'feecode':'10981' },
        'TY9999D1000001' : {'feecode':'10982' },
        'TY9999D0010001' : {'feecode':'29189' },
        'TY9999R0050001' :  {'feecode':'10984' },
        'TY9999R0100001 ' :  {'feecode':'29202' },
        'TY9999D0012003 ' :  {'feecode':'29206' },
    },
     #保皇
    '1511261750466.app.ln': {
        'TY9999R0050001'          : {'feecode':'34126',       'name':'500钻石',     },
        'TY9999D0002001'          : {'feecode':'34127',       'name':'20000金币',     },
        'TY9999D0005003'          : {'feecode':'34128',       'name':'50000金币',     },
        'TY9999D0006016'          : {'feecode':'34129',       'name':'60000金币',     },
        'TY9999D0008005'          : {'feecode':'34130',       'name':'80000金币',     },
        'TY9999D0008027'          : {'feecode':'34131',       'name':'80000金币',     },
        'TY9999D0010001'          : {'feecode':'34132',        'name':'10万金币',     },
        'TY9999D0030001'          : {'feecode':'34133',        'name':'36万金币',     },
        'TY9999D0050001'          : {'feecode':'34134',        'name':'65万金币',    },
        'TY9999D0100001'          : {'feecode':'34135',        'name':'150万金币',    },
        'TY9999D0300001'          : {'feecode':'34136',        'name':'500万金币',    },
        'TY9999D1000001'          : {'feecode':'34137',        'name':'2000万金币',   },
        'TY9999R0000101'          : {'feecode':'34138',        'name':'1钻石',   },
        'TY9999R0008005'          : {'feecode':'34139',       'name':'80钻石',     },
        'TY9999R0100001'          : {'feecode':'34140',       'name':'1000钻石',     },
        'TY9999D0008026'          : {'feecode':'34141',       'name':'8元转运礼包',     },
        'TY9999D0030011'          : {'feecode':'34142',       'name':'30元转运礼包',     },
        'TY9999D0050007'          : {'feecode':'34143',       'name':'50元转运礼包',     },
        'TY9999D0100011'          : {'feecode':'34144',       'name':'100元转运礼包 ',     },
        'TY9999D0001003'          : {'feecode':'34145',       'name':'1天会员',     },
        'TY9999D0012003'          : {'feecode':'34146',       'name':'30天会员',     },
        'TY9999D0008001'          : {'feecode':'34147',       'name':'超值礼包',     },
    },
})

'''vivo配置
大厅途游斗地主
cpid: 20141031202336653475
appid: f0858d747d822695f335b0c3a3e78b74
cpkey: 074f40824807c7b5050c7831d7cb54ad
'''
add_global_item('vivo_appkeys', {
    #途游斗地主
    'f0858d747d822695f335b0c3a3e78b74':
        {'cpid' : '20141031202336653475',
         'appid' : 'f0858d747d822695f335b0c3a3e78b74',
         'cpkey' : '074f40824807c7b5050c7831d7cb54ad',
        },
    '71532d03613e7bc1f9098cf4e7cc597b':
        {'cpid' : '20141031202336653475',
         'appid' : '71532d03613e7bc1f9098cf4e7cc597b',
         'cpkey' : '074f40824807c7b5050c7831d7cb54ad',
        },
    #途游斗地主
    'f0858d747d822695f335b0c3a3e78b74':
        {'cpid' : '20141031202336653475',
         'appid' : 'f0858d747d822695f335b0c3a3e78b74',
         'cpkey' : '074f40824807c7b5050c7831d7cb54ad',
        },
    '71532d03613e7bc1f9098cf4e7cc597b':
        {'cpid' : '20141031202336653475',
         'appid' : '71532d03613e7bc1f9098cf4e7cc597b',
         'cpkey' : '074f40824807c7b5050c7831d7cb54ad',
        },
    #途游斗地主 单机斗地主
    '20141031202336653475' :
       {
        'appid' : 'f0858d747d822695f335b0c3a3e78b74',
        'cpkey' : '074f40824807c7b5050c7831d7cb54ad'
       },
       #途游斗地主
    '6cc5e0db21fdbe37ed0f6902e8b68080':
        {'cpid' : '20141031202336653475',
         'appid' : '6cc5e0db21fdbe37ed0f6902e8b68080',
         'cpkey' : '074f40824807c7b5050c7831d7cb54ad',
        },
     #中国象棋
    '0a5187139f5ee6b8d2a285485a842d78':
        {'cpid' : '20141031202336653475',
         'appid' : '0a5187139f5ee6b8d2a285485a842d78',
         'cpkey' : '074f40824807c7b5050c7831d7cb54ad',
        },
})
#支付宝参数配置
add_global_item('alipay_config',{
    'partnerId':{
        '9999': "2088901481292394",
        '10042': "2088211680098179",
        '10062': "2088011439630081",
    },
    'partnerParam':{
        '2088901481292394':{
            'partnerId': '2088901481292394',
            'sellerId' : '2088901481292394',
            'rsaPrivateKey':'''-----BEGIN RSA PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAOIc0bKk2wj6nA2Fzd59LDfhXJGlurRs+GzYPKtKKjyMLVxq/PDLOahkiYNzaOBeWFa4smtdFZdd39sgHCyqoMkVTSR1KGZHiiPrlUEoIdwYI+iS7vRvwPk4RkN7C/gL1OKZ1P6/EhCb/R5wJ1zfymiRd1iv3ztDL+0dLOlOcbklAgMBAAECgYEAtSPNQkYbSugpmBO3RyQUBng+Blg0aFJb+iaJA9gYWgUaWc1D8Ut9V0+jcnFEdWpfbqnsFWKu52JG8W6Z45aV0sADvoMHe0DzB+OD4nqgObG/lFZif3vSWEyN+UIxmW+Eu+nOyR/PHUD6W0Etg5B47W2rqzpXEzU2zfknwM7uWsECQQDytNtBxeMg2Y5w82WU+GuMtaFNIAe6g+YreEKEn6TmbU266x8HCktXsSP1jKSt4GpvkLDUB5zOa+HZobnuVkmZAkEA7n9J+iP7JcMPU+X8O1nxzsMe103gfzQaGyiIVtPLoHHkZU/2kJ8O3WBAcS4glJ8ZBoqQJs3yel+GNSar
2MNbbQJBAKondVgFXhjXrW8ulNb92pjJdY5WmFSAyEtNgoTsT3VkyAv1bslGxE90
Vxt9QK7OGJCixfXAaISnSa2EHpAjWnECQGzeNgq1OgO20txdc5I0MKlNcFqf9gaa
5f/XtMTN0XngA34rzkWeFc8ADOqdP8oYBfhyb/MGt9UcncrNaEx+gNECQQDXYEhX
ZEptZMm3nb2tj0u//kOEgfnVqu18/pfFbJOyXjRqoIya46hMvzEcEvq0dND5bdhP
8mIud7No5ZelmAPn
-----END RSA PRIVATE KEY-----''',
            'rsaPubKey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRA
FljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQE
B/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5Ksi
NG9zpgmLCUYuLkxpLQIDAQAB
-----END PUBLIC KEY-----''',
            'alipayAppId': "2016012101112179",
            'alipayMD5': 'p6pyopwqnt3589w9w0ycbcmu1swmuu4u'
            },
        #萍乡射雕参数
        '2088011439630081':{
            'partnerId': '2088011439630081',
            'sellerId' : '2088011439630081',
            'rsaPrivateKey':'''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQCu2Y63GNUU754IwkFXgjLraksMLbg1hgljmmAf+EZUfRkCEZLq
pyEff+p4/QJKcXfCOYV3WM9v1v6CdILWXcmADpEHy1YAlyQHISL4qJTCcfueY0qj
gJ+CDpoPdl+GNlIGPRPSaLRjUIf0fCGsI3zd7U1yKyAezgSnbcsefvhnQQIDAQAB
AoGAGp5CLLuaDMLhwyGXgvPuPoqC/EqlhXhvS3t/8L4CLvCQcxEr1Y816q61ik+y
HpUhjy7kk6OwiK0pN8D2/h1vBFA9Cqt+atpuTCq0fxyPJQlmU0B7njj3u1sGcn/T
n67PiTFOCkt4XGME+Bb+dlIvCqJPvqbYhfr2HKrL/wuz/bUCQQDbn0w3/s1CZFeJ
ICeOtVDSCgzdNq1zQtDwQl0O2jVe64n8W7jdsqgiQqKrcmWCxngYOBi+gFwERh76
+skb7n07AkEAy8/DNUxP60lON788VCNL8YEdKj9oz1hslutZ363EWN6/xAk32939
6Pt4WyBl/f/Wq/E47MK9FE6XnYTf2cMVswJBAMPdvcvyonyjoK3az2ymp/2qmO5w
5R/2ZwDfLr8gPJj614UJCEYwH2LuqsTcsUuAVXrEDM1ZDLeDEf4jy1ftyiECQQDJ
48GUD0bvZEsl77p8AgbdcS+JxQw2sHnIudPqPcBM5EIDl7oMgwdc/ZVId3xwsjhd
VHM2HOWdswh/EbuIg7X/AkBAPMk2tLivO4vGQuQOK966HAOQ1neOe+bxwH3bN355
QMMj/TiojyeC5WNKAu4qFa+VoWnuUeym15EMnTaR/w9x
-----END RSA PRIVATE KEY-----''',
            'rsaPubKey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRA
FljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQE
B/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5Ksi
NG9zpgmLCUYuLkxpLQIDAQAB
-----END PUBLIC KEY-----''',
            'alipayAppId': "2088011439630081",
            'alipayMD5': '4w36m9rhyenrbcrbf11rapoza3p9zrif'
        },
        '2088211680098179':{
            'partnerId': '2088211680098179',
            'sellerId' : 'yuanjun.cui@shediao.com',
            'rsaPrivateKey':'''-----BEGIN RSA PRIVATE KEY-----
MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAMN5SBghXWFZG/ZA
pJW3IsVsHIvl2+QsOmqEtaIkru7JKvvpJq9o1ylpjQiIB1kJXmow9zugsV40Q522
ApVDheF05bM7Z+y1ORvLATuC/7rr4zB4/cEqLQKFb/cTC5RT8BGMg3UCvZ4AYUX9
OsutcXHNGD/Q9vA3tNkau7EJtv6/AgMBAAECgYEAkxVSQx3v5s0nNh8j+KeJmWWl
ATtfPwxslDPxe+UAYBqspkqkWj6YD8glX/MDHGLpURwxHAPpEkpfSm9m+CuLs21j
FS6zsH9OYQAX7E+QXEBEzBHaJbJL5pVwE2GwEW+/+Rgb/g+vxu8mcT9MdJdvuJYm
4+egCXSReTpb89oEQlECQQDu5/6SBuwCFfwPVM4aYDV1ii1AXpquyxTUD49OGu7p
nOZjOrZSvWcjEu5dZBUV3pdwRqOpZBwq11ftSiTEH7B3AkEA0XW96ehlkTpj0J72
02kUsWdtWW4ESMzhgHsxjA5pn195DTGEmnfRvjKXsnTU0Qo/jCP1sSONQMIVxmUN
Iug9+QJAMgOvb7KzRdyEYFFItIzfpDPBNXCYwW8SdTKstZU93vpR4QQxlzC/nsAf
1r1VDLcEzSR8rsGeg/mBFtQmzkg0EQJBAIhOLsBA05emf74LNGRvRWANBkPkLDWT
3ktV3/BckK992bCUQM6kmoFDOySOks9V8/SmkgQsNoelxbXNnLbSm0ECQQCOBuDR
rK0sjO8+J1g3GH5Do//pf76DJsuxuRhgum9ioYlmLQ0DkrLSIvKl69j0NAVaZ1UP
wXZIVMvFzQp7HxNz
-----END RSA PRIVATE KEY-----''',
            'rsaPubKey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRA
FljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQE
B/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5Ksi
NG9zpgmLCUYuLkxpLQIDAQAB
-----END PUBLIC KEY-----''',
            'alipayAppId': "2088211680098179",
            'alipayMD5': 'n4y3j358igeatgyr2sdvzvjjahnrfoee'
        },
    #广州特游兔网络科技有限公司
    '2088121857137870':{
        'partnerId': '2088121857137870',
        'sellerId' : '2088121857137870',
        'rsaPrivateKey':'''-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQC9/MIkoVq+rO7QF5m+C0KxFSI5JDaAsnLlCGoo4VMw81H2AyKd
FTVgNupa2a+aGJ5C4l9X5j/JuC0gGzRNgMmmerDXV5Sr9aLgkEgcjgHI5AnTw2cr
AV2hsTDhNoezWBdhdbVu9OeN8jVKppJUImalAWANTu3br66p/cJScVwVjwIDAQAB
AoGBAK0YYtH46LKc4KBbQEnz/HlWpe2l3rp221NszTwdvyv0JJKd3KV9sznMDs1j
VChzkY2irfdp4mgpE4QTBR4v3ofrl29qHI6VDrxQApY4g7nxxxGO7x3Gb6ZmEMSd
sEgPQpdA9Xnxc53J9U6T9OnSe/gIOS0mcsE8gh9g3TvNdAkRAkEA3L8hawtVh6qH
fhxYRZMI3QCPWU3u4OD+3UUH5n7n9ygz9kdHDI0Oql2+fy0DJOpGDxT1ziRWD+a0
FpvIY3EICwJBANxUFbKWl1wEd3/qatfhW86/PEbnoHH1Uo1NkGqe8s60r9yvu19o
WUU9N2DSv6Z4SX3VhpUVh7g0bpa1OrNPJw0CQCJ83fy6XZd/hgGm7geYrDbTApJi
QaLyo/7v7QcO5rDPoCanBiuo0hS95qg54RbgXye2D50wQh3j3lj1573Zh/cCQQCV
yuTlgdRtzuufn7P8CU7thL5qRleionL5dl5U3rOdLOLTWvY8qyjmFfRsc1uwxd7R
GjZhbT3UUnFNLPE3rvyRAkARDdQHrEDIzNcV9nC3snYWSWFbxl76CaoVT0KdQ/W0
DeAyQBv7qiL+LFhJ/yoNuVCTqvl6RFp8J4/acoMwReGI
-----END RSA PRIVATE KEY-----''',
        'rsaPubKey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC9/MIkoVq+rO7QF5m+C0KxFSI5
JDaAsnLlCGoo4VMw81H2AyKdFTVgNupa2a+aGJ5C4l9X5j/JuC0gGzRNgMmmerDX
V5Sr9aLgkEgcjgHI5AnTw2crAV2hsTDhNoezWBdhdbVu9OeN8jVKppJUImalAWAN
Tu3br66p/cJScVwVjwIDAQAB
-----END PUBLIC KEY-----''',
        'alipayAppId': "2088121857137870",
        'alipayMD5': 'tnr90lxk1ogc4a4dazc50dn6sw9kozgf'
    },
    #广州特游兔网络科技有限公司
    '2088502710358739':{
        'partnerId': '2088502710358739',
        'sellerId' : '2088502710358739',
        'rsaPrivateKey':'''-----BEGIN RSA PRIVATE KEY-----
MIICXgIBAAKBgQD8zh1MJPuhhs/4cJvnI3hyp6D4JMnzWSspG+xlWqhuzci/Vm3h
B/D5Dz/nh3awmuyUaIM37khNhj6J1kiCBHz5jA3rsPkX42LgI0hbubuFnbO8cxSA
uVnKevCseQrsRUHc1fELDsT3Ytgd1cSj6mMazvA790Ao2unQxbm7HHNQeQIDAQAB
AoGAXU++5KIp9v8JuIvoH7Kp/Lf+5Fi/6gCZu7zAztBdpzhxxp4iRJNn0KZeUhlg
J+OnO0gwVu6u5V6NqtbbQJJjhgTsKCE+6F6BtDI+yALPBwsHtpzda3kt7duZ0neY
sS9codILmKmvNQg5UOMOSGj+tsOfOG64RL3/HgfD5pNIwTkCQQD/x7ZissOBzWSb
DX0mIHmfZ42oanqnkq1xGpNrhcOhgteMfX4Jtja7vq4I+HgdFrJ3emw6RxGHRmyv
nc4T7X0rAkEA/QW/UBrsNZ8wsMXybzXwhQJ8wp7t5EyCo5vplYpQnwc0X6OnNZ0A
B3E4d/695U9J5tZZFWABOhJMoBbn8OM+6wJBAMKFbsZ270qbGqT0yDWjwvsgtNHd
ULR6T19R98Vw8Eu3hxf4JE9cfRmhNRfrZuWwaj+FIiPcAo+fVm7kk2ICXgsCQQCn
sClsw4sMtqYkYewcfFkdLdrVeVMcXQCvweL68qIf4zx4rhNhWt3sEMNl83STBwtp
a2G64tetTvdtmgC6C0FlAkEAucryVjtEFdT6yLg8WXisGD146ifaaqmgpujSu8kD
IEE12CSKpdTwXxfmHuoED7NXtD8536vlR36CZUChXsWLVg==
-----END RSA PRIVATE KEY-----''',
        'rsaPubKey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD8zh1MJPuhhs/4cJvnI3hyp6D4
JMnzWSspG+xlWqhuzci/Vm3hB/D5Dz/nh3awmuyUaIM37khNhj6J1kiCBHz5jA3r
sPkX42LgI0hbubuFnbO8cxSAuVnKevCseQrsRUHc1fELDsT3Ytgd1cSj6mMazvA7
90Ao2unQxbm7HHNQeQIDAQAB
-----END PUBLIC KEY-----''',
        'alipayAppId': "2088502710358739",
        'alipayMD5': 't8vefd0j5whbwov5ob4k5izh9m0a179s'
    },
    }

})
#银联支付配置
add_global_item('unionpay_config',{
    'merId':{
      '9999':'802130059620501',
      '10040':'802130059620501',
    },
    'merParam':{
        '802130059620501':{
            "certId":"69812453430",
            "certKey":'''-----BEGIN CERTIFICATE-----
MIIEIDCCAwigAwIBAgIFEDRVM3AwDQYJKoZIhvcNAQEFBQAwITELMAkGA1UEBhMC
Q04xEjAQBgNVBAoTCUNGQ0EgT0NBMTAeFw0xNTEwMjcwOTA2MjlaFw0yMDEwMjIw
OTU4MjJaMIGWMQswCQYDVQQGEwJjbjESMBAGA1UEChMJQ0ZDQSBPQ0ExMRYwFAYD
VQQLEw1Mb2NhbCBSQSBPQ0ExMRQwEgYDVQQLEwtFbnRlcnByaXNlczFFMEMGA1UE
Aww8MDQxQDgzMTAwMDAwMDAwODMwNDBA5Lit5Zu96ZO26IGU6IKh5Lu95pyJ6ZmQ
5YWs5Y+4QDAwMDE2NDkzMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA
tXclo3H4pB+Wi4wSd0DGwnyZWni7+22Tkk6lbXQErMNHPk84c8DnjT8CW8jIfv3z
d5NBpvG3O3jQ/YHFlad39DdgUvqDd0WY8/C4Lf2xyo0+gQRZckMKEAId8Fl6/rPN
HsbPRGNIZgE6AByvCRbriiFNFtuXzP4ogG7vilqBckGWfAYaJ5zJpaGlMBOW1Ti3
MVjKg5x8t1/oFBkpFVsBnAeSGPJYrBn0irfnXDhOz7hcIWPbNDoq2bJ9VwbkKhJq
Vz7j7116pziUcLSFJasnWMnp8CrISj52cXzS/Y1kuaIMPP/1B0pcjVqMNJjowooD
OxID3TZGfk5V7S++4FowVwIDAQABo4HoMIHlMB8GA1UdIwQYMBaAFNHb6YiC5d0a
j0yqAIy+fPKrG/bZMEgGA1UdIARBMD8wPQYIYIEchu8qAQEwMTAvBggrBgEFBQcC
ARYjaHR0cDovL3d3dy5jZmNhLmNvbS5jbi91cy91cy0xNC5odG0wNwYDVR0fBDAw
LjAsoCqgKIYmaHR0cDovL2NybC5jZmNhLmNvbS5jbi9SU0EvY3JsMjI3Mi5jcmww
CwYDVR0PBAQDAgPoMB0GA1UdDgQWBBTEIzenf3VR6CZRS61ARrWMto0GODATBgNV
HSUEDDAKBggrBgEFBQcDAjANBgkqhkiG9w0BAQUFAAOCAQEAHMgTi+4Y9g0yvsUA
p7MkdnPtWLS6XwL3IQuXoPInmBSbg2NP8jNhlq8tGL/WJXjycme/8BKu+Hht6lgN
Zhv9STnA59UFo9vxwSQy88bbyui5fKXVliZEiTUhjKM6SOod2Pnp5oWMVjLxujkk
WKjSakPvV6N6H66xhJSCk+Ref59HuFZY4/LqyZysiMua4qyYfEfdKk5h27+z1MWy
nadnxA5QexHHck9Y4ZyisbUubW7wTaaWFd+cZ3P/zmIUskE/dAG0/HEvmOR6CGlM
55BFCVmJEufHtike3shu7lZGVm2adKNFFTqLoEFkfBO6Y/N6ViraBilcXjmWBJNE
MFF/yA==
-----END CERTIFICATE-----''',
            "merId":"802130059620501",
            "privateKey":'''-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCbqN3354qu9RWX
naHoU7xIKc9zPXh5hv22GmwsgZdsPD9rbboqX//itB7a/qBpXZ7ZT82RXN0yj6DW
B81Bf2tgzMG2wg8C8KDF/aX0nLD49M9IMPU+a/sCvPpBUApgQt/62J1c9282Vn/N
gWyZGOZbSLdH43f3g9T7KVGYkNgnRQdbOWMt4U26XYMqjwaX+yvJFquzJ3zYc9D/
j8GloPy8WMbjnigN4hFhuJtOWO/PIW2gJwS4bPcQKBXg+f/zzFmBQ6k96ojdJKTh
OaO0nO6SFHdwVt3BXwBpFd0QUITsSWhZ6gPcTkmWa0c1KIGi+IWuH3n99uuLjD1C
0yzZM+BDAgMBAAECggEAUmfQsvgiREM9Xhm2aC9EQxPXXlPRnsynLivIzrsAde1j
SbU6VEqkRdlDaH5aX82PVc5Yrrbx512AMS7KK/2P1BwyBVWw6saG5qpEnD4Dtpir
z7UTcCtsJGP1PHRqOdHNj5fznw7jEmoymJIG8vnqobLaTLWQgjmJnDmgl9s+g3LE
w9yLrU4qLdHX5ekjftBj9wREXfdZud5BsgByAg30D6dcEGFxHpygZPgbaJA9a096
DR3tEublQnMgwnz6FIamyVhMFSiK5euRfQYz4MftVpG0n2za4yfCcjuatyoIEyZn
3XlzRqotHzHuqERcYN3sgnpUFGcfjj4Cd6UVi4wusQKBgQDYoKozK1n89fGvk706
QIOVTbzwQrxGJ57dwnmNTdHAlJcZT5eNXeMhUWpGK9RDhVejfoH8uHRFkPe5+7DW
mphPU41z1Y0iZD5JaNohwmxFxvvOfCYm1AMS2WROE6nSbBXnFHFc/++s9TEbnSBY
GMoXOqtnrq7v5XnlVFGC+whOSQKBgQC383XvHcdjNr6s4+kkHDuScVfr7fID6OMX
Or1DT3q4RfvHcw/acghJT4eFbDfY6OxGP+WjAMprye5dBSBWyDVstG/MjBg/bcMZ
cxtna4/Vt8dkDTrMfMHSYO9kNwhKw5BqfpvVsRzr/50ae0FZUmHdYpKImQdVB7r9
lVybXUDqKwKBgHrs6MfykLT3xzbPyjA1DbX6j/1ykS3qK79BLQKfJyh16SwmuyQw
I8PzVDAPjPrnvqx7DD4hWXFkav6xsU6GGWniSsFxbA4Y/jNf+W/wyMnruVYZovij
lD7s93tKszJBvUgMlKumXBY0aLJ3vjPflUYLN9q1CHX/LOWSrFJ8KuFpAoGAEoRC
WdiQio8nMHYcsNLauEoKhKhGFVirC1qRVKY6fzQkPRZ7AQ07gk2sIaUcFgyURBoI
fpkEx0bjZJ+weqvanN+o5Vkw06mz2ur4VjfAmc3PF2YxhgYE6K1zS44ymnwHHIE0
JJWYiLUJVnITyO7/BO74OyHUWB3YF9CiKs1/TFMCgYBD071Fqmnvtl4gfQWa9TSG
TvCGeJt5s99JxL2h87X1NjJfg0d/QHOIQzcBybuffFHpRJLs6uW2ZwHSquJvwQZj
WTqQgyZfqi/xcQCSy3/jihPJxgF9FKTbgRdrGgxbWqbOrO/Gxwzrp9dRDmn+mKux
R4laPJuBO5SGI4b0M1008g==
-----END PRIVATE KEY-----''',
            },
    }
})


'''华为配置
'''
add_global_item('huawei_config', {

    'Android_3.731_huawei.huawei.0-hall25.huawei.tu':
        {'userName' : 'tuyou',
         'hw_appid' : '10444414',
         'pay_id' : '900086000020107980',
         'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eW
YHYxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
         'pay_ras_privat_key' : '''-----BEGIN PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4Cob
zFsRb10tJ0suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWS
M/4k+Wy8Tz6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRR
MI97FvQVUNOrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIW
RbCKZ1TF/p8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9
UnsCIQCoXxZ1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOW
RxixsNe/odBnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3n
mzXEXBITsjk=
-----END RSA PRIVATE KEY-----''',
         },

    'Android_3.36_tuyoo.weakChinaMobile,woStore.0-hall6.huawei.tu':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10157892',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eW
YHYxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10t
J0suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+W
y8Tz6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97
FvQVUNOrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRb
CKZ1TF/p8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9
UnsCIQCoXxZ1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFS
OWRxixsNe/odBnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmW
gM3nmzXEXBITsjk=
-----END RSA PRIVATE KEY-----''',},
    'Android_3.363_huawei.huawei,weakChinaMobile,woStore.0-hall6.huawei.dj':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10179513',
                  'pay_id' : '10086000000680944',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJQNHmiSC2cyVzo3zY0WfjQcn5nPl+uk
AjXo0syHc+T2okBrub619vHfe1xa5Zru01nbi/PLUONh51dMQwIWmnkCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAlA0eaJILZzJXOjfN
jRZ+NByfmc+X66QCNejSzIdz5PaiQGu5vrX28d97XFrlmu7TWduL88tQ42HnV0xD
AhaaeQIDAQABAkA8vcUkEgcrp7Ox5wMmR3wv1S6F5G3n97oQdB1IXKpn3UiIpMiV
Hyz9inlztjeNYjVD2WnAJzkNwDjgLglEJAABAiEAygq1kdbVgNJhJyhxWwQnoJvm
hmyXiR2YA3psVppdrAECIQC7lyfc3MIz42b0eiRjVAnR4ARHK3ypVZTQb6kRoWhO
eQIgUAQLwrVlmv42sc5njldH5mi31Hb/ULNit8XtUCMUhAECIQCC2Bvl4dVTe/oD
7G4VGjj/OtHBEoQRWLBD8p5qvbqTgQIhALHzMHK8iBKLYlvrSNKWPZGQt8ohWe6U
5+hSNc9aosOM
-----END RSA PRIVATE KEY-----''',},
    'Android_3.37_huawei.huawei,weakChinaMobile,woStore,aigame.0-hall6.huawei.dj':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10179513',
                  'pay_id' : '10086000000680944',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJQNHmiSC2cyVzo3zY0WfjQcn5nPl+uk
AjXo0syHc+T2okBrub619vHfe1xa5Zru01nbi/PLUONh51dMQwIWmnkCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAlA0eaJILZzJXOjfN
jRZ+NByfmc+X66QCNejSzIdz5PaiQGu5vrX28d97XFrlmu7TWduL88tQ42HnV0xD
AhaaeQIDAQABAkA8vcUkEgcrp7Ox5wMmR3wv1S6F5G3n97oQdB1IXKpn3UiIpMiV
Hyz9inlztjeNYjVD2WnAJzkNwDjgLglEJAABAiEAygq1kdbVgNJhJyhxWwQnoJvm
hmyXiR2YA3psVppdrAECIQC7lyfc3MIz42b0eiRjVAnR4ARHK3ypVZTQb6kRoWhO
eQIgUAQLwrVlmv42sc5njldH5mi31Hb/ULNit8XtUCMUhAECIQCC2Bvl4dVTe/oD
7G4VGjj/OtHBEoQRWLBD8p5qvbqTgQIhALHzMHK8iBKLYlvrSNKWPZGQt8ohWe6U
5+hSNc9aosOM
-----END RSA PRIVATE KEY-----''',},
    'Android_3.71_huawei.huawei,yisdkpay4.0-hall6.huawei.dj':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10179513',
                  'pay_id' : '10086000000680944',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJQNHmiSC2cyVzo3zY0WfjQcn5nPl+uk
AjXo0syHc+T2okBrub619vHfe1xa5Zru01nbi/PLUONh51dMQwIWmnkCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAlA0eaJILZzJXOjfN
jRZ+NByfmc+X66QCNejSzIdz5PaiQGu5vrX28d97XFrlmu7TWduL88tQ42HnV0xD
AhaaeQIDAQABAkA8vcUkEgcrp7Ox5wMmR3wv1S6F5G3n97oQdB1IXKpn3UiIpMiV
Hyz9inlztjeNYjVD2WnAJzkNwDjgLglEJAABAiEAygq1kdbVgNJhJyhxWwQnoJvm
hmyXiR2YA3psVppdrAECIQC7lyfc3MIz42b0eiRjVAnR4ARHK3ypVZTQb6kRoWhO
eQIgUAQLwrVlmv42sc5njldH5mi31Hb/ULNit8XtUCMUhAECIQCC2Bvl4dVTe/oD
7G4VGjj/OtHBEoQRWLBD8p5qvbqTgQIhALHzMHK8iBKLYlvrSNKWPZGQt8ohWe6U
5+hSNc9aosOM
-----END RSA PRIVATE KEY-----''',},
    '10179513':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10179513',
                  'pay_id' : '10086000000680944',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJQNHmiSC2cyVzo3zY0WfjQcn5nPl+uk
AjXo0syHc+T2okBrub619vHfe1xa5Zru01nbi/PLUONh51dMQwIWmnkCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAlA0eaJILZzJXOjfN
jRZ+NByfmc+X66QCNejSzIdz5PaiQGu5vrX28d97XFrlmu7TWduL88tQ42HnV0xD
AhaaeQIDAQABAkA8vcUkEgcrp7Ox5wMmR3wv1S6F5G3n97oQdB1IXKpn3UiIpMiV
Hyz9inlztjeNYjVD2WnAJzkNwDjgLglEJAABAiEAygq1kdbVgNJhJyhxWwQnoJvm
hmyXiR2YA3psVppdrAECIQC7lyfc3MIz42b0eiRjVAnR4ARHK3ypVZTQb6kRoWhO
eQIgUAQLwrVlmv42sc5njldH5mi31Hb/ULNit8XtUCMUhAECIQCC2Bvl4dVTe/oD
7G4VGjj/OtHBEoQRWLBD8p5qvbqTgQIhALHzMHK8iBKLYlvrSNKWPZGQt8ohWe6U
5+hSNc9aosOM
-----END RSA PRIVATE KEY-----''',},
    'Android_3.71_huawei.huawei,yisdkpay4.0-hall6.huawei.tu':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10250613',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eW
YHYxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ
0suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8
Tz6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQ
VUNOrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1
TF/p8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQ
CoXxZ1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsN
e/odBnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXB
ITsjk=
-----END RSA PRIVATE KEY-----''',},
    '10250613':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10250613',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eW
YHYxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ
0suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8
Tz6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQ
VUNOrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1
TF/p8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQ
CoXxZ1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsN
e/odBnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXB
ITsjk=
-----END RSA PRIVATE KEY-----''',},
    '10249866':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10249866',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eW
YHYxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ
0suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8
Tz6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQ
VUNOrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1
TF/p8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQ
CoXxZ1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsN
e/odBnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXB
ITsjk=
-----END RSA PRIVATE KEY-----''',},
    '10249817':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10249817',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eW
YHYxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ
0suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8
Tz6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQ
VUNOrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1
TF/p8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQ
CoXxZ1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsN
e/odBnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXB
ITsjk=
-----END RSA PRIVATE KEY-----''',},
    'Android_3.71_huawei.huawei,yisdkpay4.0-hall6.huawei.happy':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10321692',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eWYH
YxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ0
suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8Tz
6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQVUN
OrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1TF/p
8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQCoXx
Z1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsNe/od
BnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXBITsj
k=
-----END RSA PRIVATE KEY-----''',},
    '10321692':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10321692',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eWYH
YxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ0
suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8Tz
6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQVUN
OrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1TF/p
8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQCoXx
Z1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsNe/od
BnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXBITsj
k=
-----END RSA PRIVATE KEY-----''',},
    '10330875':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10330875',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eWYH
YxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ0
suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8Tz
6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQVUN
OrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1TF/p
8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQCoXx
Z1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsNe/od
BnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXBITsj
k=
-----END RSA PRIVATE KEY-----''',},
    '10383352':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10383352',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eWYH
YxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ0
suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8Tz
6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQVUN
OrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1TF/p
8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQCoXx
Z1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsNe/od
BnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXBITsj
k=
-----END RSA PRIVATE KEY-----''',},
    '10397846':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10397846',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eWYH
YxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ0
suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8Tz
6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQVUN
OrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1TF/p
8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQCoXx
Z1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsNe/od
BnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXBITsj
k=
-----END RSA PRIVATE KEY-----''',},
    '10406971':
                 {'userName' : 'tuyou',
                  'hw_appid' : '10406971',
                  'pay_id' : '900086000020107980',
                  'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eWYH
YxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
                  'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ0
suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8Tz
6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQVUN
OrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1TF/p
8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQCoXx
Z1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsNe/od
BnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXBITsj
k=
-----END RSA PRIVATE KEY-----''',},

    '10412222':
        {'userName' : 'tuyou',
         'hw_appid' : '10412222',
         'pay_id' : '900086000020107980',
         'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eWYH
YxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
         'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10tJ0
suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+Wy8Tz
6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97FvQVUN
OrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRbCKZ1TF/p
8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9UnsCIQCoXx
Z1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOWRxixsNe/od
BnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3nmzXEXBITsj
k=
-----END RSA PRIVATE KEY-----''',},
                                  
    '10444414':
        {'userName' : 'tuyou',
         'hw_appid' : '10444414',
         'pay_id' : '900086000020107980',
         'pay_ras_pub_key' : '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eWYH
YxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----''',
         'pay_ras_privat_key' : '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4Cob
zFsRb10tJ0suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWS
M/4k+Wy8Tz6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRR
MI97FvQVUNOrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIW
RbCKZ1TF/p8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9
UnsCIQCoXxZ1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFSOW
RxixsNe/odBnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmWgM3n
mzXEXBITsjk=
-----END RSA PRIVATE KEY-----''',},


})

'''PPS配置
'''
add_global_item('pps_paykeys', {
    '816': 'TYDDZ895993d90b7e83db722bbJ816',
})

'''mo9支付配置
'''
add_global_item('mo9_config', {
    '10003': {'account' : 'yuanjun.cui@shediao.com',
              'paykey' : 'e4ea135eac5a4ae98e6e6400b2b5e03c'},
})

'''易宝银联卡支付配置
'''
add_global_item('yee2_config', {
    'test': ['YB01000000144', 10],
    'tuyoo': ['YB01000000275', 20],
    'shediao': ['10012424968', 30],
    '': ['YB01000000275', 20],
})

add_global_item('yee2_rpath2account', {
    'callback1': 'YB01000000144',
    'callback2': 'YB01000000275',
    'callback3': '10012424968',
})

add_global_item('yee2_paykeys', {
    'YB01000000144': ['''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCxnYJL7fH7DVsS920LOqCu8Zze
bCc78MMGImzW8MaP/cmBGd57Cw7aRTmdJxFD6jj6lrSfprXIcT7ZXoGL5EYxWUTQ
GRsl4HZsr1AlaOKxT5UnsuEhA/K1dN1eA4lBpNCRHf9+XDlmqVBUguhNzy6nfNjb
2aGE+hkxPP99I1iMlQIDAQAB
-----END PUBLIC KEY-----
''', '''-----BEGIN PRIVATE KEY-----
MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBAPGE6DHyrUUAgqep
/oGqMIsrJddJNFI1J/BL01zoTZ9+YiluJ7I3uYHtepApj+Jyc4Hfi+08CMSZBTHi
5zWHlHQCl0WbdEkSxaiRX9t4aMS13WLYShKBjAZJdoLfYTGlyaw+tm7WG/MR+VWa
kkPX0pxfG+duZAQeIDoBLVfL++ihAgMBAAECgYAw2urBV862+5BybA/AmPWy4SqJ
bxR3YKtQj3YVACTbk4w1x0OeaGlNIAW/7bheXTqCVf8PISrA4hdL7RNKH7/mhxoX
3sDuCO5nsI4Dj5xF24CymFaSRmvbiKU0Ylso2xAWDZqEs4Le/eDZKSy4LfXA17mx
HpMBkzQffDMtiAGBpQJBAPn3mcAwZwzS4wjXldJ+Zoa5pwu1ZRH9fGNYkvhMTp9I
9cf3wqJUN+fVPC6TIgLWyDf88XgFfjilNKNz0c/aGGcCQQD3WRxwots1lDcUhS4d
pOYYnN3moKNgB07Hkpxkm+bw7xvjjHqI8q/4Jiou16eQURG+hlBZlZz37Y7P+PHF
2XG3AkAyng/1WhfUAfRVewpsuIncaEXKWi4gSXthxrLkMteM68JRfvtb0cAMYyKv
r72oY4Phyoe/LSWVJOcW3kIzW8+rAkBWekhQNRARBnXPbdS2to1f85A9btJP454u
dlrJbhxrBh4pC1dYBAlz59v9rpY+Ban/g7QZ7g4IPH0exzm4Y5K3AkBjEVxIKzb2
sPDe34Aa6Qd/p6YpG9G6ND0afY+m5phBhH+rNkfYFkr98cBqjDm6NFhT7+CmRrF9
03gDQZmxCspY
-----END PRIVATE KEY-----
'''
],
    'YB01000000275': ['''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC30JBSQWkBTikuPoeboEo6gd2K
G+AuSPuya9nn4Ik7yYZABydSGvw7dBcwJFUV6pAXtiNXdTvX60rRW79MXDa7yI+G
u3PikTTHPGtd5M6HrTaKox2WKIirkjbpi3Y0D4Bxk/yV+AUQcVANewejuKkNB3We
FQcPi/tw3Uy2hzGJwwIDAQAB
-----END PUBLIC KEY-----
''', '''-----BEGIN PRIVATE KEY-----
MIICXgIBAAKBgQC7KtqCotyDv4JTLXWJBJQIExj9yBiijezT3pRCarSS6r+HH/Fo
5yvtPWA93SF5Apm0P6rEhtAizjplHiSp2kvYEnXp/V8p+dHm1smBZjCLbJPM3RjG
GwRWgiE+EXqzd15ztuVeKOCr6QvPbeS5zLt+3gNAasbizYnrnzoMWuhtQwIDAQAB
AoGBAI6YZYWloq9VVmscdTGApW9JbX7b1bjyu/3m07mOJijQZD8EXR35EYRbgFlh
gcD59DRZVTcJJsV9rQug3XnycFjM3W0j1VSuXxmvyyXQUJtAxnnv3a5r06251BSK
7CxcRt2StSLET+3MPgtiMdFfgLguMv9Imu/kO5qDdJPLWc+hAkEA8oESF3mVqO5K
j4wU900Q4b4jUHZvsuOa7/GpbL/GTT8My+O5/CVnf6UxkDQVG9hypfL7P+97XlR5
aN9yqN/OKQJBAMWVZ/HceInXyXGy7iSs9/9OE1d/feN3fKHgQuP+8n6Xfday+5sw
GDRN+jSJyrJ0kaTbMkAGmi/+Rhz4AjKtNYsCQQDRj4xM0Prtww6XwdwUYXqnOaJW
1CJumpW3qERa/9ajxkqOnzqHlOM9wUl1biyXpZJdqf5JH/CicamBYSc6nD0RAkAr
SwlznXNsALRLDYHQ13Wfo2PpkC3tYYkVjyYY/wvzYQ5ZtO4cmvUywMNKL8cSQyiG
juD71naCfZyvTEhvAjTxAkEAsWvsnxRNR9fgt+D4HPCA0wloujjqQLmDotBTKWu9
AiyYb6YAxdiKTjEdaO4qPrd0A6BvFJeaI0hMohfJG0DyAw==
-----END PRIVATE KEY-----
'''],
    '10012424968': ['''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDBzJmzLOivGC/V2P/2KihP8j+d8
JBYEGLpn2h3PybPlqLyP2bIgs4ISeLUQyIAMesLBGqmuaGc6Rl3Rk3UltxD2UyrpD
rqILMVrhFJT3rCibafZQk8MsmjBE7EPWjKBEYcBMGTVRtv0ghcpSkd3yNvyBunXMk
mRfxPqASio/bEhwIDAQAB
-----END PUBLIC KEY-----
''', '''-----BEGIN PRIVATE KEY-----
MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIIscaalV7zRXSj9o
hI6RmJnovcVpakIk+eL0xQN88CrZnH0b/X6r82Igjl/DwWMU3RKJfe6rOqBfxbrFb
hWEvn8i/uucXxVqom2AvcMExD9MsBAATrcx6qwy8vHfaUKeAmqyOxc4BHwLh1TLLr
L51ih2POn9R/eTMT2OarLMy79AgMBAAECgYBtlYKbmoew8cNuVY6Rr7M+9iXvwa5z
DUCN5Vztfg1cfi5A8lkqhz5mVWvjgT4hGo/Kzv0FfoZA6IEXxxHC29seme0OORXNd
5VV//XtkoigSxdTwQhM7QRfh+CX8oH7CjYXj8snH3PqnmX3d2TPSLTHs7IM2Wa4m7
WONIxC9MS+4QJBAMKGcnHo7n2HxBUkvLAAF6760p+RPl4Cf9+P1LGXaryENdyOacR
+VhYnDnUmlleRzmj3xs5KIheeu0saGJ0dHZUCQQCrT8ztBS0DMnGP3fTUeZmkOr7Z
FqG5RXuJIX+uTxsW64b5mw/nEZgOa8ux+7xxmv74UqDSw/NR5YUjC4crO+HJAkBEr
76XdD1J+/eD074Ak3fJZG2cxGd2QIGwihP7RVD+Ed0G7Q5xwH5bQh07xo1NjIGK1P
rQ+qJBHt5ZbXSFfbNlAkEAqBIFojBmxfEyewwujFq0wuwjm0ZZ6jPiDFrCMphHoof
2h2J7Cp83SEa3tGmeqvJ+3c/rGnzGdn2wzf4cYe1BCQJAVa1LNBWWixuhqlji7qyN
Mf+C+oNQmKFzR8MUCkx4iQi6b+KlAtZTcT2UTeIvj0lAMKWM4dBRZAkwjDsekV8tY
g==
-----END PRIVATE KEY-----
'''],
})

'''优易付支付配置
'''
add_global_item('yipay_appkey_config', {
    '2000024': 'fda8c042c87f2fdb031110c9eadc8dec', # tuyou
    '2000042': 'a3d3394d5f4a867dcb60ffcad7ffca7e', # muzhiwan
    '2000050': 'f261e33340832b4715626269f6225664', # jinri
    '2000084': '3eef887fd8cfa49bee3afb38d00fa72f', # yisdkpay new sdk (include YDJD,YDMM,woStore,aigame)
})

add_global_item('yipay_config', {
    'merc_id' : '2000024',
    'app_id':'5969fac8a69c11e49758c6a10b512583',
    'yipay_key':'fda8c042c87f2fdb031110c9eadc8dec',
    'createorder_url':'http://fee.aiyuedu.cn:23000/sdkfee/api2/create_order',
    'paycode_config':{
                       '2' :'2',
                       '4' :'9',
                       '5' :'3',
                       '6' :'4',
                       '8' :'5',
                       '10':'6',
                       '12':'6',
                       '20':'1',
                     },
    'monthly_prods':['TY9999D0020001'],
})

add_global_item('yisdkpay_prodids', {
    # 二次确认窗口时间阈值
    'confirm_threshold': 600,
    'confirm_channel':['mi', 'huawei', 'oppo'],
    6: {
        'TY9999D0001001'          : {'feecode':'10',        'name':'1元特惠礼包',     },
        'TY9999D0002001'          : {'feecode':'3',        'name':'60000金币',     },
        'TY9999D0006001'          : {'feecode':'4',        'name':'60000金币',     },
        'TY9999D0010001'          : {'feecode':'5',        'name':'100000金币',     },
        'TY9999D0030001'          : {'feecode':'6',        'name':'300000金币',     },
        'TY9999D0050001'          : {'feecode':'5',        'name':'500000金币',    },
        'TY9999D0100001'          : {'feecode':'5',        'name':'1000000金币',    },
        'TY9999D0300001'          : {'feecode':'6',        'name':'3000000金币',    },
        'TY9999D1000001'          : {'feecode':'8',        'name':'1000万金币',   },
        'TY0006D0030002'          : {'feecode':'9',        'name':'7天会员卡',   },
        'TY0006D0100002'          : {'feecode':'10',       'name':'30天会员卡',  },
        'TY9999R0008001'          : {'feecode':'1',       'name':'80钻石',     },
        'TY9999R0050001'          : {'feecode':'12',       'name':'500钻石',     },
        'TY0006D0002001'          : {'feecode':'7',       'name':'月光之钥',    },
        'TY9999D0002002'          : {'feecode':'7',       'name':'月光之钥',    },
        'TY0006D0005001'          : {'feecode':'8',       'name':'月光之钥x3',      },
        'TY9999D0005001'          : {'feecode':'8',       'name':'月光之钥x3',      },
        'TY0006D0002002'          : {'feecode':'16',       'name':'参赛券x10',    },
        'TY0006D0000201'          : {'feecode':'17',       'name':'小喇叭x10',      },
        'TY0006D0050002'          : {'feecode':'18',       'name':'广播喇叭',    },
        'TY0006D0100003'          : {'feecode':'19',       'name':'改名卡'},
        'TY0006D0010001'          : {'feecode':'20',       'name':'记牌器x7',   },
        'TY9999D0008001'          : {'feecode':'1',       'name':'超值礼包',  },
        #'TY9999D0006002'          : {'feecode':'1',        'name':'6元转运礼包',   },
        'TY9999D0008002'          : {'feecode':'2',       'name':'8元转运礼包',   },
        'TY9999D0008013'          : {'feecode':'1',       'name':'80000金币',   },
        'TY9999R0008002'          : {'feecode':'2',       'name':'80钻石',},
        'TY9999D0008014'          : {'feecode':'3',       'name':'超值礼包',},
        'TY9999D0008015'          : {'feecode':'4',       'name':'转运礼包',},
    },
    10: {
        'TY9999D0006001'          : {'feecode':'1',        'name':'60000金币',     },
        'TY9999R0008001'          : {'feecode':'2',       'name':'80钻石',     },
        'TY9999D0008001'          : {'feecode':'3',       'name':'超值礼包',  },
    },
    9999: {
        'TY9999R0000101'          : {'feecode':'1',        'name':'1钻石',     },
        'TY9999D0001003'          : {'feecode':'2',        'name':'1天钻石',     },
        'TY9999D0002001'          : {'feecode':'3',        'name':'20000金币',     },
        'TY9999D0008005'          : {'feecode':'4',        'name':'80000金币',     },
        'TY9999D0008001'          : {'feecode':'5',        'name':'8元超值礼包',     },
        'TY9999D0008025'          : {'feecode':'6',        'name':'高手限量特价礼包',     },
        'TY9999D0008026'          : {'feecode':'7',        'name':'转运限量特价礼包',     },
        'TY9999R0008005'          : {'feecode':'8',        'name':'80钻石',     },
        'TY9999D0010001'          : {'feecode':'9',        'name':'100000金币',     }, 
        'TY9999D0005003'          : {'feecode':'10',       'name':'50000金币',     },
        'TY9999D0006016'          : {'feecode':'11',       'name':'60000金币',     },
        'TY9999D0006001'          : {'feecode':'11',       'name':'60000金币',     },
        'TY9999D0008027'          : {'feecode':'4',        'name':'80000金币',     },
        'TY9999D0012002'          : {'feecode':'12',       'name':'会员订阅',     "alternativeProdId":"TY9999D0012005", "alternativeProdName":"30天会员"},
        'TY9999D0012003'          : {'feecode':'12',       'name':'会员订阅',     "alternativeProdId":"TY9999D0012005", "alternativeProdName":"30天会员"},
        'TY9999D0012004'          : {'feecode':'12',       'name':'会员订阅',     },
        'TY9999D0010006'          : {'feecode':'13',       'name':'30天会员',     },
        'TY9999R00021DJ'          : {'feecode':'14',        'name':'60000银币',     },
        'TY9999R0010001'          : {'feecode':'15',        'name':'100钻石',     },
        'TY9999D0008034'          : {'feecode':'16',        'name':'8元超值礼包',     },
    },
})
add_global_item('muzhiwan_prodids', {
    6: {
        'TY9999D0002001'          : {'feecode':'1',  'name':'20000金币',     },
        'TY9999D0006001'          : {'feecode':'2',  'name':'60000金币',     },
        'TY9999D0008002'          : {'feecode':'3',  'name':'8元转运礼包',   },
        'TY9999D0008001'          : {'feecode':'4',  'name':'超值礼包',  },
        'TY9999R0008001'          : {'feecode':'5',  'name':'80钻石',     },
    },
})

add_global_item('yygame_config', {
    'app_key':'d5e0c8e926214d40c7363a7e26ebda6d',
})
add_global_item('iappay_config',{
                    '3003062109':{
                            'appkey':'''
MIICXAIBAAKBgQCdZ2MxJgXLw8qlGzOIHQxGBAOCJcX2Z8WCw36kvteVUvd5MDYjV
RhRABpPR9PSjrShoBCu25H8oGbvWMxTMZnN7TPatawd3LzuIbqNuE+JvOhb8Io5J5
2/eesKlbh9osBXos3Cccksnjo1RcWQ8/xD83nffZuXWU53dw04v049pwIDAQABAoG
AYFWcYcIxneowpiglu9J7ZoaiVw8jP5F3UnavlcivTNbAW01kdO9puHlloMwHGkD4
0EqUq0/64zCQj0A7nVcoF+iWd1adwMKZ3+ImlSF781rL8dARtCGfe3qsv+a7kLmkb
YHf3oAJq/l0RCktGy8gxDk2dGe3XrFTI59ngwaqapECQQDO/VnVeGPv1I96FPqThA
uoOIKXLhCFCRfDC0ya8Z2AhuXKw+sASyl2MsiyukRjERHApMeS0KEfq1oOBR6rgxo
dAkEAwqxmhaqcF3L0g7x0PU8yApCy42paHbniICHCK3cwD0ypSu0ulwHV2LgbAqB0
YNiw7bgK/3x0gPszCxZol9MLkwJAZ4CyYhdQScXNdOt2nTsjJRwU2Qn0wsFYO3Sz+
qqk6ncKAwlSwpPTCMK+LvkLZ0pKyTzceuKOHyrs3iPbQUJOVQJBAJMECYTGfI0E5n
2aU5p9dYIUbtRp29Z5K7kiZXXX0/ap6WvJRRcLbsj0+Ij6TglZe/x6seuRvJYvnrO
v35tQ6XsCQA3Q6ce4KrBP1MhOS7s5qmcyzkRq7qm+r8DMsA//R0J8wqOT04M6KVe3
eZbNStu8LaMrhIG048jMxUp5xO8W0RY=
''',
                            'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCdhYnSlaXX+aDImKLwhajKVTmF
HN0thzkGjb/OJ4vAf7GWFqOqGDkUf6i/7TNvVGPZ58/Qks/Z8jT9qvCdDjf4H6I1
3HMOX27/xke1L/cYhwjGKw2j0ncZEZ5aJiobgp7JjG7NdDtYJJ859y4QiRRvK5Ng
PvKbKiGwregrEIDPOQIDAQAB
-----END PUBLIC KEY-----''',
                            'payConfig':
                            {
                                'TY9999R0000101':'1',
                                'TY9999D0001003':'2',
                                'TY9999D0002001':'3',
                                'TY9999D0005003':'4',
                                'TY9999D0006016':'5',
                                'TY9999D0008005':'6',
                                'TY9999D0008027':'6',
                                'TY9999R0008005':'7',
                                'TY9999D0008001':'8',
                                'TY9999D0008026':'9',
                                'TY9999D0008025':'10',
                                'TY9999D0012003':'11',
                                'TY9999D0030001':'12',
                                'TY9999D0030024':'12',
                                'TY9999D0030011':'13',
                                'TY9999D0030012':'14',
                                'TY9999R0050001':'15',
                                'TY9999D0050001':'16',
                                'TY9999D0050007':'17',
                                'TY9999D0050008':'18',
                                'TY9999D0100001':'19',
                                'TY9999R0100001':'20',
                                'TY9999D0100011':'21',
                                'TY9999D0100012':'22',
                                'TY9999D0300001':'23',
                                'TY9999D0300004':'23',
                                'TY9999D1000001':'24',
                                'TY9999D1000012':'24',
                                'TY9999D0010001':'25',
                                'TY9999R0010001':'26',
                                'TY9999R0030001':'26',
                            }
                    },
                    #天天途游德州
                    '3003399687':{
                            'appkey':'''
MIICXAIBAAKBgQCPm8ZcVWwvRuac2lvyudnkj2ZS7lgk0a88Negs5l8/SbYcvdY5
c+dJ5FYGt/Bcl9W1o3dNo8HSeHIfP73iw1l0aK/YXaK2DWvcg+M5M59BQF2DVXai
pq+8KuOhuTMtUDMdohebYdMphHSZ7GVh6lim9XlQ0MU8NWBADL1qFuXunQIDAQAB
AoGAAJ4w+lC7yHBLqb0ezCqUj3E2hYDVDEOCt4Wb3CWZn1IX4IPImjKvehfrbtf3
xs44czGi38immts90niZvpIMnnv0ExdFd+PluOErKOawEPopa7lJ48LST4aJt5DG
qNDhETbehmHYsvv3jeQR+17npD8WE9ZStz+xV7nCtippP0ECQQDU/ZM1+8SXGicm
A8Kdl/mHEpKmudLKDpwdkaJ+Ouc9DEoKeQTW0UI4+2gCRMHx7R/1cik9eXRIdyU7
cvHWMq7pAkEArJuI7QuP/tdbl++9iHDjqJdMomEUNYdkRkqkAKqSv71vyrFscmxF
GfaZvqseQfDWOdVLhhWzlTmE78Jd0Kp5lQJAWGDoBsxzpKdrezCwPqhjGBMy2w/c
UY+CZBqcLHjQntpMls/knCa0reRUIizZtUNJsZUvW5zcDX2y61ok01awkQJASWZW
ot7g2/D+nSywv32qAf5c80wvCNhLVuzUswfWIb1P9bTfNgU+mVzZYlBoLIhawPso
A5vk4xczpbVUqbBkxQJBAJiyYHBZiDpENyrdTpuQRHSdemoZ7A8Bs+LcRCvzt/g7
/JPk/Rb7DiTCgx7YTvc+qSIu8l0JfZoqnV9gCUu1ODM=
''',
                            'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDnFSPfYvGNgWOvuq5WOUODVBDjj
qGhKsL+1NnIX+5pbstl65uNmZpJrtQ4wK6LImwDTeyVFU4Mr0zHVtHxlYESRv8vY2
KzK2FxHJjbGNYlFBAjt7m41TLMSBtS/LUnYPLlDy95i9ozpF2eVSF5yo+Nlzz8qVY
4gVFHT2EktnaYNwIDAQAB
-----END PUBLIC KEY-----''',
                            'payConfig':
                            {
                                'TY9999R0000101':'1',
                                'TY9999D0001003':'2',
                                'TY9999D0002001':'3',
                                'TY9999D0005003':'4',
                                'TY9999D0006016':'5',
                                'TY9999D0008005':'6',
                                'TY9999D0008001':'7',
                                'TY9999D0008026':'8',
                                'TY9999R0008005':'9',
                                'TY9999D0010001':'10',
                                'TY9999D0030001':'11',
                                'TY9999D0050001':'12',
                                'TY9999D0100001':'13',
                                'TY9999D0300001':'14',
                                'TY9999D1000001':'15',
                                'TY9999D0008038':'1',
                                'TY9999R0050001':'16',
                                'TY9999D0030024':'11',
                                'TY9999D0050011':'12',
                                'TY9999D0100021':'13',
                                'TY9999D0300004':'14',
                                'TY9999D1000012':'15',
                                'TY9999D1000011':'23',
                                'TY9999D0300003':'22',
                                'TY9999D0100020':'21',
                                'TY9999D0050010':'20',
                                'TY9999D0030023':'19',
                                'TY9999D0100019':'18',
                                'TY9999R0006001':'46',
                                'TY9999R0030001':'47',
                                'TY9999R0128001':'48',
                            }
                    },
                                       #单机斗地主
                    '3003313137':{
                            'appkey':'''
MIICXAIBAAKBgQCpZmUow/eTbafUf5iE0IdXw/KHGJl31pflFGCxpP5qiOOxIuQi
4j2zaoNxSWPwdIbIvqzBKILRVD8GYynIpcQCePflZjdli6p0K9QUNEmsdUZkULJW
CUxIcyPoADDS5WTgUqV9LGDszyTb+7MGfZF9uDUNwa94Y0BGuRP69qio1QIDAQAB
AoGAPtlxsLU8VqN5gBqzAJvJiyN1CPB0iATDKEfuNBqOFgKhz6etUs/zqmxbRh2/
iYgCNdqgh627E2UZWQpTh1ERLmrsqEn4jFLYnSm2oy97cpNaDNIInVIzyDa7X8yS
hHF6qP6yiuqc0W8w+DIQLHWTNrKflY8ZKT6+ZkInYQB8n4ECQQDbaOBp/IXHaZ7g
6sHZC+OYAWNynhu/AErB3EikZmJxBlw7NWrCIvduiaHdNrOahO97j4QkcgofEm11
l9xSz0I1AkEAxaZ8NrT1kSNdJhBXYJKXRv1t0LltJQvF/c4bkvpNNItiJNseeqCL
9KHt+g2fMH//XfzDm8ImLcc6QbWX0FCgIQJANBU4OFCGXSjYWyG+9EvbMekad0nK
4lMqa8xjvgrD0XqmCDQM7JqqS6YGM2HZzpNB2f3ea1xaxLd2HlT3Kv0iBQJAWpTR
KnVGcazGXNJyaQTlpZgxws2oMqkxpP7XbkWeKm2Snhd54XNAkO3BVa72fNC8ZQOZ
VgHlY2eB0Gl72PGKYQJBANQDowFxccl3h8ERT+xsK2B4Bozt1vT0HPWl+GlabHo6
LpjHtDZp0rJXTVO8KhG8CWnqb85MKICecdiW/iBdxmY=
''',
                            'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCBpmrSeHEbu6UTx/bSj5nytX+T
FUe7rQj7MUkrHnYIad5ME3zLmJ9eFVUkI1pDhrTM5VlXoNjXpGtY+xK6aRVX1QsT
BypolOTND6rc/l0jZWD0H7G9Uw7XRS2K56B5KZDfSey19EILGjRgL4oMCj12d6Ex
soca4fORWaV0+1VcOQIDAQAB
-----END PUBLIC KEY-----''',
                              'payConfig':
                            {
                                'TY9999R0000101':'1',
                                'TY9999D0001003':'2',
                                'TY9999D0002001':'3',
                                'TY9999D0005003':'4',
                                'TY9999D0006016':'5',
                                'TY9999D0008005':'6',
                                'TY9999D0008027':'6',
                                'TY9999R0008005':'7',
                                'TY9999D0008001':'8',
                                'TY9999D0008034':'8',
                                'TY9999D0008026':'9',
                                'TY9999D0008025':'10',
                                'TY9999D0012003':'11',
                                'TY9999D0030001':'12',
                                'TY9999D0030011':'13',
                                'TY9999D0030012':'14',
                                'TY9999R0050001':'15',
                                'TY9999D0050001':'16',
                                'TY9999D0050007':'17',
                                'TY9999D0050008':'18',
                                'TY9999D0100001':'19',
                                'TY9999R0100001':'20',
                                'TY9999D0100011':'21',
                                'TY9999D0100012':'22',
                                'TY9999D0300001':'23',
                                'TY9999D1000001':'24',
                                'TY9999D0010001':'25',
                                'TY9999R0010001':'26',
                                'TY9999R0030001':'27',
                                'TY9999R0200001':'33',
                                'TY9999R0300001':'34',
                                'TY9999R0600001':'35',
                            }
                    },
                                 #途游斗地主
                    '3003425922':{
                            'appkey':'''
MIICXgIBAAKBgQC5jCcqZbpuf7nVDsmCWFnzCSfUexlPe0rjDraFVZN7Ixni62ny
NcumippNRSFs6vZbo4uUQ3iwD9G5c057XKeGmRVqjJzl+8MIjqxPqlyoQpHS1xJE
d0AhM88hUtLhn92KcmiPF7w9nQlzJJiJ0XuEJ66avMq4QGcgkGx5zm8e+wIDAQAB
AoGBAJkgp3n/9noXAwBocbkWvTUryyk6ZksID2ePzuX/F/W5pDV33zm7V9Sb8nfu
o4VF7Ab408qKXGHAzG5mUNDSSJYNhCvINZTB1A2lwLfOJSjJ2KBz7Qt75+pENQcw
uHUhGVhbA9kvDxp+5xz5JgyaL4Wk7tNjYawJNajYWcihzCwxAkEA7AL89KATYitC
a/OkBqOc8H6eFMJ8bDDtBGTL5AoeQrnnkgxCUE5mYQp1iHHmw9RX1309jkhLfas6
svngQBlIrQJBAMlDCpoJDHYgvITIOdIkOlhOgv8Kf+UtfG6nf7+vkHSh8Il+78IA
4nFLNI0+934YKjgR+MyG89oA+8Uuqgxns0cCQCeruOlFnvx5WQjcQ036Yn7qSZgj
uNZWwwBiEQObz8pXhV0/QkZNZ1gYcfklbCyunLVUD+zCqi3NgmhjKBaeKWECQQCJ
MTwO2FA4TgRz9xEDIFLtU0eUlxGrpaAGxgMdJY4xExqmf3LsKjIxzHQcPGn0+H//
DLEuqmebmcQGG9Mq9Z2NAkEAtxuhngGQht++Lw9xBUuVpMxOn+or2mWsqQOZ7yxr
Zu5w9shED98J+qu2rMYBS6C0Yg+9MI4j7/lchKgPOrlPmw==
''',
                            'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCbmqNFSTIAQph5fU1SDZ6Km3xQ
3Lgk5hznxnW1b8kujvsqGJRXSABb9ZXJHvhwuNWIfRvNp6z1V4uzl0QXibqCf3qQ
N6zrFzRgf3hq6FzG5A+eiWeI/S0YlJ5TYJEQSpInUCWKzEjZY2F+5CyI7Ut+LxfJ
vvcn1zziSsD5iiaOrwIDAQAB
-----END PUBLIC KEY-----''',
                              'payConfig':
                            {
                                'TY9999D0100001':'1',
                                'TY9999D0030011':'2',
                                'TY9999D0030012':'3',
                                'TY9999R0050001':'4',
                                'TY9999D0050001':'5',
                                'TY9999D0050007':'6',
                                'TY9999D0050008':'7',
                                'TY9999D0012003':'8',
                                'TY9999D0012004':'8',
                                'TY9999D0030001':'9',
                                'TY9999D0100011':'10',
                                'TY9999R0100001':'11',
                                'TY9999D0100012':'12',
                                'TY9999D0300001':'13',
                                'TY9999D1000001':'14',
                                'TY9999D0010001':'15',
                                'TY9999D0002001':'16',
                                'TY9999D0001003':'17',
                                'TY9999D0008025':'18',
                                'TY9999R0000101':'19',
                                'TY9999R0008005':'20',
                                'TY9999D0008005':'21',
                                'TY9999D0008027':'21',
                                'TY9999D0006016':'22',
                                'TY9999D0005003':'23',
                                'TY9999D0008026':'24',
                                'TY9999D0008001':'25',
                                'TY9999D0008034':'25',
                                'TY9999R0010001':'26',
                                'TY9999R0030001':'27',
                                'TY9999R0200001':'33',
                                'TY9999R0300001':'34',
                                'TY9999R0600001':'35',
                            }
                    },
                                        #中国象棋
                    '300306495':{
                            'appkey':'''
MIICXQIBAAKBgQC8EpyyF0ghSXUP/4mOhJHHVYSOpJIQGP75R/1QIZ5XewMdFrw/
OMFu2GumqIEwCgvzz4ok+0k+LthApBb+IdP27rDhqdo8TTpwSJ7mooFREp/4i67R
nLYPneMx85+GQoRSaoQdlTTgtRETANLPVv/XbTHPyKYpE8/J+Dk5ay/5CwIDAQAB
AoGBALgVc6BxX12Ne/JbybVglxvH3caM2Ja/EJrI1u3e6hBwTDzlqv4qvFKVrNDk
cAaoXsiW5H2MJEWkLnEe6451Z/TGUMvF2UW3eyvsJeErr0IMV9+7EgDSnpJw4GPl
Nd+yASfG9SwjzOsBpgOWnoNojP1uce8W+KaBB7wlKYxIkOkJAkEA332xi4EpZSHA
eDyi1dEiK5cIZ5kMKNa2rET8HjAvrFzxH1T/H93RkZ1Ni8gVkF+req9PGkO1Muqq
aaRwmNht1QJBANduBT4RIPu4RUcFKEzrgxMiSZuRUu3e42Rb8H2X9he4iBJ5ec3+
Ail6cnD7ma5sdWGCZZJj0dHrordTKExC218CQQCCOg+2pnCkiWJJrauEw/QRSlSP
aVL4iQSwpRHz1UgyO4YVJ8Xxn6N6IhsJlHFcSyL0viptt35iSPM706H4rkRxAkA5
SCXYtRFCHWM+WR64JT87DTjpRqD4YvWvr8qoeomTERwNXYOHxGyqvsZDSIM6n9gu
T0/WtvgJi1A+0ru6W2SdAkAeTkeCy20MaStfJesBmgsoJcc28DF7EPIPYKO97Wli
CqFGaOCzXSaqofeveWdCXfvlF/X6YEr1DAHfBNG0HqGN
''',
                            'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCHroIW6g/pHv0X4oF8Cj7cXf8M
SRfYV8GNDb2clXEd7Qzm8rfBfDPcvhh38il3uGnjpi3wapwZLUBWl2XQc+Itkfeh
DVTbQUFTUjU76TdNiNE5xNwGuz88bjUEtPDoXEYjaR1YEZRbIcoK+Z1a4gIOCE5m
390/ySDSiQA5gU6rjwIDAQAB
-----END PUBLIC KEY-----''',
                            'payConfig':
                            {
                                'TY9999D0012003':'1',
                                'TY9999D0008012':'2',
                                'TY9999D1000001':'3',
                                'TY9999D0001003':'4',
                                'TY9999D0002001':'5',
                                'TY9999D0005003':'6',
                                'TY9999D0006016':'7',
                                'TY9999D0008027':'8',
                                'TY9999D0010001':'9',
                                'TY9999D0030001':'10',
                                'TY9999D0050001':'11',
                                'TY9999D0100001':'12',
                                'TY9999D0300001':'13',
                                'TY9999D0008030':'14',
                                'TY9999D0000102':'15',
                                'TY9999R0000101':'16',
                                'TY9999R0008005':'17',
                                'TY9999R0050001':'18',
                                'TY9999R0100001':'19',
                                'TY0006D0002001':'20',
                                'TY9999C0003001':'21',
                                'TY9999C0006001':'22',
                                'TY9999C0001501':'23',
                                'TY9999C0003002':'24',
                                'TY9999D0012001':'25',
                                'TY9999D0002003':'26',
                                'TY9999D0006008':'27',
                                'TY9999D0006009':'28',
                                'TY9999D0030004':'29',
                                'TY9999D0030005':'30',
                                'TY9999D0100002':'31',
                                'TY9999D0100003':'32',
                                'TY9999D0100004':'33',
                                'TY9999D0008026':'34',
                                'TY9999D0030011':'45',
                                'TY9999D0050007':'47',
                                'TY9999D0100011':'37',
                                'TY9999D0008025':'38',
                                'TY9999D0030012':'46',
                                'TY9999D0050008':'49',
                                'TY9999D0100012':'50',
                                'TY9999D0008001':'43',
                                #2016年07月18日18:35:22新增
                                'TY9999D0008005':'8',
                                'TY9999D0012004':'44',
                                'TY9999R0030001':'51',

                            }
                    },
                    '3003374445':{
                        'appkey':'''
MIICXgIBAAKBgQCNlcKjHEFcbbi6ipP02OtZ9LFcyqHhxMRT5Wp0Cnrgwj2u0WJv
wRmenzMwBTEVAjYcSgtWZWVf4DArv6kzrP4TIr6rnQ9x0l95OuFRdFFlUEuTQERU
1RhYeigH5XNIIVy/AAhrzyZiI2D5NJqVUUT3a0OnHTDROLNSwM/2Uhjr0wIDAQAB
AoGBAITL66QLU2665uHoKoAjmRNlg5mR4SYd5Tr/Wcp/LeNzrGE0uMwy5LG3hk5L
AE9BJLmB5YJiViQH5YaTHMOARUkORTMJWIJv8Bq9V5+VNKCLWq9RFfC2uC3CdJfN
udaYLdGiZ0C0qlikhtf11mq02GnWEwTF2qQKLAs0TyMZk08BAkEAwYphyTktVzRW
wIse4CrVtSxzLxxxcR/9pZA6oBtc6BpTplkclpt4eayW19k5PdXOpdtdngm9miUY
lSqtJToxgQJBALtG/8XNx98U4k96/SV0x3zsIT8f7RmPU89ucw7WWomoQ4KHS2gG
L8Win7jhjxJTbpgu+R5ViMkhhudUpJ3cX1MCQGgGUgLO2aDqf8pjvEeunkkPyCVF
O3AbSsDnYatWqbwTEmzxrp0AmWOEsVr45Xxn4/dfjdT41VD5qVnbo07EFYECQQCH
5eSS4FnqqtfyvxfVx2E/aIZTrVI7mwNBYi/CE5BNljmvDYiNqvednf3zhlJxBPQb
IPMLrRv+gALJ+WUfXJwbAkEAjtjQveztCpj4sE0Zwuk9qRZHUrP1hZqyiBd1xc8a
f1jcRE9aAng/D8GKeBZpU2Bejm58Csw6lIrU2re517hefQ==
''',
                        'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEnqgRelWr1IO9MD7oCebt1ZRa
FUQCZBdCm4nAbZdWPSaKi/BV8HGrbN0c6zUSkSLpdCbTxQEbZUM3OMX3hLauNWCf
q2VrF0Rk5k1WddonihDGj+q/+Wg5dyNRXm6VdKYWShAATBgbf8koebOLxFevwEzm
Hn/LZRdCoLRjn7RauQIDAQAB
-----END PUBLIC KEY-----''',
                        'payConfig':
                            {
                                'TY9999D0002001':'1',
                                'TY9999D0006001':'2',
                                'TY9999D0030001':'3',
                                'TY9999D0050001':'4',
                                'TY9999D0100001':'5',
                                'TY9999D0300001':'6',
                                'TY9999R0008005':'7',
                                'TY9999R0050001':'8',
                                'TY9999R0100001':'9',
                                'TY9999D1000001':'10',
                                'TY9999D0000102':'11',
                                }
                    },
                    #保皇
                    '30034076':{
                        'appkey':'''
MIICXAIBAAKBgQCAfdZGldXQkYnzd8RWqrZ9AScNV8CrVzEofSSeVPfn+FIgxTUt
8MRwcXby6nFoqsmTsRaP/MSrLeIVr4P9DrvCpw/PK6Tptew+UX4FHDX5QgxQwnl0
WCql/bZkISC1GXSNjUgBVcgPMGMrV1u1jkX7eWKFp+YpUtkcypK5Ep3g+QIDAQAB
AoGAN3caggm37HqGtCRlCoxSjg9rTiUtNElFHRc4MWi4Qtg8i4zVcelWwrsX/7AY
GHhw32I4PRt9we7igz3qmdg8UBtYnBGUptZzzY6OQmFTMKMsQuEskNEtgsBSqAUf
a3CdVVAv9KzalCkWzUubfiEZsI25G8BTzE60fhykcutDp+kCQQD7QEniS05Vdcry
B4CG3r8BhKdJ0BVh4zZJ/FbIeGIYDNP3qkvYrG2nB2eS9/QbWSgewPXc7DqQNLlX
NLj7LN6nAkEAguuPZtf7vXbCHX8WiBQemDnbaNlG8qytvpKvb7hDg1f/ieB71qDz
psJqJAzLvdE/OZrVee+zjmvg1+FAwl/XXwJBAI3LWGcnzMuaMLCq3zQ+XVmD/c1A
a/DUg/z5NhjpJ6MfCjlJmIhtt2x+V0uwN8l/ZY8FozvM7bgYqUi37nWCex0CQHU/
i4UaZ0zt/7i06bPi+Odx4WsMM/r/5PZong+a4XPOqn+LeLzmFm/Ba5dvkkQkEtB/
NzJmFtO1D3+nLv0lIlcCQG3QWAOMt99eLfBMGnXu19HhguZfrzflaNFoK2kHCmPn
FU5RXD0YxW6j89cgVU0Bhh8EBIlYw8FbNOH/x6k08Vk=
''',
                        'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCfvLhOt5stVonfAkAlUbv+yD5c
d32DBgXqI6UWEVkLGWpnFJBpPI5qJjouIGGVWBOdvF8TCg1WTaXfuOaoGt4/I998
d3/iM18D0JzwW99Svy66QLNg9mhoN6Osa37FZ1QRMc8+a6M1lbWibQV/zZ5ytN9O
TzVbZgR/lSnkFVt77wIDAQAB
-----END PUBLIC KEY-----''',
                        'payConfig':
                            {
                                #'TY9999D0012003':'1',
                                'TY9999D0008012':'2',
                                #'TY9999R0050001':'3',
                                'TY9999D0002001':'4',
                                'TY9999D0005003':'5',
                                'TY9999D0006016':'6',
                                'TY9999D0008005':'7',
                                'TY9999D0008027':'8',
                                'TY9999D0010001':'9',
                                'TY9999D0030001':'10',
                                'TY9999D0050001':'11',
                                'TY9999D0100001':'12',
                                'TY9999D0300001':'13',
                                'TY9999D1000001':'14',
                                'TY9999D0000102':'15',
                                'TY9999R0000101':'16',
                                'TY9999R0008005':'17',
                                'TY9999R0050001':'18',
                                'TY9999R0100001':'19',
                                'TY0006D0002001':'20',
                                'TY0006D0010001':'21',
                                'TY9999D0008006':'22',
                                'TY9999C0003001':'23',
                                'TY9999C0006001':'24',
                                'TY9999C0001501':'25',
                                'TY9999C0003002':'26',
                                'TY9999D0012001':'27',
                                'TY9999D0002003':'28',
                                'TY9999D0006008':'29',
                                'TY9999D0006009':'30',
                                'TY9999D0030004':'31',
                                'TY9999D0030005':'32',
                                'TY9999D0100002':'33',
                                'TY9999D0100003':'34',
                                'TY9999D0100004':'35',
                                'TY9999D0008026':'36',
                                'TY9999D0030011':'37',
                                'TY9999D0050007':'38',
                                'TY9999D0100011':'39',
                                'TY9999D0001003':'40',
                                'TY9999D0012003':'41',
                                'TY9999D0008001':'42',
                                }
                    },
                    #单机麻将
                    '3004282241':{
                        'appkey':'''
MIICXAIBAAKBgQDHZSnAxfAM7ZRbti8PashLvJopmuDHj8lU9O0G3ziHn3D0KOKJ
UACdy98LweWFwnclKYLQ92jMUg5qhjcSnfBCPNTJy7C0A1c3wRJzU5sFpqa1ij19
Nc6TDntrvn+wj0a41/tAxEFbqlkDX9hdg9JxENtJSkZ27YCzyEf7i8iEpwIDAQAB
AoGAF9jTe4iwwvsPCUDqs+9TcStnTJ6HT5a0v4JjbrT3r9Cz05+oKD/3MugVDvTr
nGm7kig6yv8r+3O84aSXpZRaDXu3oT+zwWJcyTUORIdBtRkTESOhEDIkWCa7a//q
LW5lCWtTNqvSlrDsRsEd+9oeudeZXKdZ+EEufBr8in08PMECQQD2GB7eqrpeNeSy
1MOs10MU+JF5k8FH8JFzjvYYEXwDPysTfpjTjB3rGPhk0JGqkzszCHADXEdCwphn
d4kEuZWXAkEAz2vU80LzgDedEk7hLn9rusNMaW4ZoMTIN3N1NuswabhCC+3tBJcc
UVh78YjXqyzr2FzNXW5IIBp/JLI4VRALcQJAFzqLn2TqFn5ryd1/Ys8my9HymVEz
C0FP2WKDJB5yYDQUMtDeSAmPwWMn/wwY08r16YlAWXDaYRjRHeMQkduanQJAJyjv
kmHAgSN+xxcXUmUCHMeEZJ9BvWWJe1aT+aNbh4ofBguMZQJ2eTEgbVBtj0ay3C1h
JFOO0GjQOkhfdEfMMQJBAKp+8EmVDwv+P2ns3PCyNhXLSmsZROrIRpNwdrsr1VPF
M31y9feV9P8YWNAacOhGKWjbMNE/gF/hE392ps/AsM0=
''',
                        'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCDqtvVhI43Cbcr+enyFKY34HnJ
mud8S6fnyQO/g7t4408u9gEfogPyhWnWuFTnj/a0hftt3+fXZABiUgjTZKEyAU4u
JtDgZ9VPVZXu/ABJTqujnuU04U0Z/a0koaylyrb9HbeFLxFmaYx1l/UM/p+p+Tqn
ZxD0lWfQ83lYz/r3WwIDAQAB
-----END PUBLIC KEY-----''',
                        'payConfig':
                            {
                                'TY9999R0000101':'1',
                                'TY9999D0001003':'2',
                                'TY9999D0002001':'3',
                                'TY9999D0005003':'4',
                                'TY9999D0006016':'5',
                                'TY9999D0008005':'6',
                                'TY9999D0008027':'6',
                                'TY9999R0008005':'7',
                                'TY9999D0008001':'8',
                                'TY9999D0008026':'9',
                                'TY9999D0008025':'10',
                                'TY9999D0012003':'11',
                                'TY9999D0030001':'12',
                                'TY9999D0030011':'13',
                                'TY9999D0030012':'14',
                                'TY9999R0050001':'15',
                                'TY9999D0050001':'16',
                                'TY9999D0050007':'17',
                                'TY9999D0050008':'18',
                                'TY9999D0100001':'19',
                                'TY9999R0100001':'20',
                                'TY9999D0100011':'21',
                                'TY9999D0100012':'22',
                                'TY9999D0300001':'23',
                                'TY9999D1000001':'24',
                                'TY9999D0010001':'25',
                                'TY9999R0010001':'26',
                                'TY9999R0030001':'27',
                                }
                    },
                    #四川麻将
                    '3004675591':{
                        'appkey':'''
MIICWwIBAAKBgQCTIwZ9kFJrvtqkKc4hMzFNro4jjTErZxItLLkQhIfbB0c0Fj00
+D2Q3eva0F9x+SSshQk53YrINb4u7u1Kp6T2KvDF0DWxor1Xn+a5uCNr/TlF8PGJ
Vn4L01GhncPDk5h5L9Cy8vMHHCa4bka6aCvWn+Pnb5VYe/1VTCc88NMxJwIDAQAB
AoGARiFKpayVbF+ijN6ULkTdOh56Bz3z8rEE+902NEZHDsGwUYZMFCRCC/uKwFfT
Nlq+/S/HzvnmfTkIdgxRs+Sl/inUcHEBagfroq9lqRTn7+YxsyrvVX9EjTzdzPlP
crKbGykU0KvG9VsBPPvwFDc/sRj5tB6eyWCLSFhi+Ac/YDECQQDP4woCaaGWBkHg
9qXYuWV8T8s/EDBlglGqxuth+qhqaxlYPscsv8BMlIRTL+DMRNs2uV6sGv0112ui
YSg0SqUvAkEAtTCk0gCm/4gQG22o//uJV5otcqo60XrRRBgwxTgYsY8EMxBSIUmA
YCya6nDXsl/1udXPLyAb1KT7xQEohs8liQJAVEmtqUTC610mINxgafrhlwGTWsJp
nP61thRpI5TJ7Dv4TrtFbnNguKwO6tuiva+9YfbO1+EpgUcSsQfLkUgiqQJAP8X2
TUATh19BpBXN5QOIzL+kfXZzK2YaH+iPyeq7rktTRBHbhoHTYIZypE/Ba7Qgzh72
RHT9trO3Nhj5RbHFWQJATt8osE5AxWcOq1klWVkghK+GiakhTSuUXaJ1zrCC3x8t
H0eQJZvpR3kalDVor68XsVEWiBeU8Q+4nOfvNSeQcg==
''',
                        'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCpKRQxZdnyjvdiYQmqPq/GN9vL
3xpBmhHw+bTdC1gGEY15R0i5z5A2xmX6aczan0czYW8j8Z9fzCA6wCD65aXlDtC1
P4tCAdu2fcEe8cQWZNcFmQmWNNLEip0CXh0MV2WaBSJzi6IzksPELZj87v2roS6P
JbDeTFAAUJ5FOuqdeQIDAQAB
-----END PUBLIC KEY-----''',
                        'payConfig':
                            {
                                'TY9999R0000101':'1',
                                'TY9999D0001003':'2',
                                'TY9999D0002001':'3',
                                'TY9999D0005003':'4',
                                'TY9999D0006016':'5',
                                'TY9999D0008005':'6',
                                'TY9999D0008027':'6',
                                'TY9999R0008005':'7',
                                'TY9999D0008001':'8',
                                'TY9999D0008026':'9',
                                'TY9999D0008025':'10',
                                'TY9999D0012003':'11',
                                'TY9999D0030001':'12',
                                'TY9999D0030011':'13',
                                'TY9999D0030012':'14',
                                'TY9999R0050001':'15',
                                'TY9999D0050001':'16',
                                'TY9999D0050007':'17',
                                'TY9999D0050008':'18',
                                'TY9999D0100001':'19',
                                'TY9999R0100001':'20',
                                'TY9999D0100011':'21',
                                'TY9999D0100012':'22',
                                'TY9999D0300001':'23',
                                'TY9999D1000001':'24',
                                'TY9999D0010001':'25',
                                'TY9999R0010001':'26',
                                'TY9999R0030001':'27',
                                }
                    },
                    #天天途游德州
                    '3003063115':{
                        'appkey':'''
MIICXgIBAAKBgQCYVxC7QbrtloyoIY+Xc3w+8ijrkEwEycZNfyMlid46/PwO+V/E
0MMXGtr38JBHsFNvM5K0BSGIU/kCTuh/agUIrfOWaH1QGkAjLIkyKU6rESXSQJLD
0RapTxJWPZbCoB5FMov2S8Ivvt/TnipVCHvWPIEyMkYlq9bq4ENdo8PP9wIDAQAB
AoGAB72Uyg8C8oONzhU2eJmTnJctYRrJ4gxmmRV2sbeZpSGppREivptk7k2dBrAg
hKP++U2DjMYd+BFcO7PKuH6olr429vYmQ/1WhQF4M4l7xrefImvQJ/0OlwD3milz
fZXWPfkp4X5GT5GnvpNebSJ3Y3bJ/3Z99ANUA74mZdKzRXECQQDQYCbplh7bxAow
C0yQ380yaaKQg9rJNzS4/HUPr4kLR937q02NmYlswDJnptSOAv7VbTEVUmvz3lbR
TCmoKpqjAkEAuyhVHkBb3UXzKej8YA7ordpRmC6ZSwTQGpMaJBb2cVVrGpkc9/w6
FKzCB9lpWMJ+rE8Gw6p/9mSVvLJSzYq+nQJBAMuVha8mSpPwnvt9rprE7dhZOMj0
6ic5Vrt9fGmM2No6pvkhzq2P2qJzzUtTxcvRxWSEQDZSxsIG8s+eF/0DUv0CQQC4
Dx5GtfyiTFyr5tnsjjz+XSrJg2p2gLE4sVqQC5UqOFswuUvoBkIIey4HEiWsiPqS
8tUwMMnPw3QPM0CDq+NxAkEAsj/ggY17vg5uR3N4xYXyP16Wp6a2pVJBH/iB6m+D
LfcrN3qEe4cfOiFSqUZVkc8y3daCKzb9LTUenktqxDqpBw==
''',
                        'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCdR/ZyIjmREKeoxaun563QRyem
lGgKoNU/d+BG3Stf6aohLeH/Unfj1y/FEV2PqrUx3o6/Cf/0PR/wGabwuJYVgMRU
yIyXq0b6beWNRwddr5yuX0/EjeGCWa7CsihUwYCntVabTwIDZMekiChTLUlz1SgY
L4zunUPEmDX/ATmrEQIDAQAB
-----END PUBLIC KEY-----''',
                        'payConfig':
                            {
                                'TY9999R0000101':'1',
                                'TY9999D0001003':'2',
                                'TY9999D0002001':'3',
                                'TY9999D0005003':'4',
                                'TY9999D0006016':'5',
                                'TY9999D0008005':'6',
                                'TY9999D0008001':'7',
                                'TY9999D0008026':'8',
                                'TY9999R0008005':'9',
                                'TY9999D0010001':'10',
                                'TY9999D0030024':'11',
                                'TY9999D0050011':'12',
                                'TY9999D0100021':'13',
                                'TY9999D0300004':'18',
                                'TY9999D1000012':'15',
                                'TY9999R0050001':'16',
                                'TY9999D0008038':'17',
                                'TY9999D5000001':'19',
                                'TY9999D0100019':'20',
                                'TY9999D1000013':'21',
                                'TY9999D1000011':'22',
                                'TY9999D0300003':'23',
                                'TY9999D0100020':'24',
                                'TY9999D0050010':'25',
                                'TY9999D0030023':'26',
                                'TY9999R0006001':'47',
                                'TY9999R0030001':'48',
                                'TY9999R0128001':'49',
                                }
                    },
                    #青岛棋牌
                    '3005843213':{
                        'appkey':'''
MIICXgIBAAKBgQCPL+8V8tvksv/zAGRf4R0O1r2KZ9UH36HyKsAOYwKWxWo48oT4
7rmPX3ScfH83K8sd6N4mx2oqWNZrvkE0DfsM7bbcxih/jtPeVrlwbEULkbrP2ycM
mHBsf/WZS+DCddQEUKAfsDVI4COJ8xJjNW3cJUbEV5TMRLNYxEZQyCFRewIDAQAB
AoGBAIdFh5+6shbbLIaLxkf2Shdss9//u/gWQ86eqJZu31FE69ck9o6eKVvTmD0G
OMEMdHWrO8Ry/E9JYjijosHku1jDOzYk6f/FM/vwRDr85Rq9alFBY6iSUOFsFy7T
yuxIVBYmBG+m5qm5MRidJt5DcYpaJc4ZeadeF2yp8xn87rXRAkEA+L8XEREMNTrq
s8L5Hx9cCoUmLIXBWoz/8Q+U25YNIeIEoXoJ+sFjicfCC8xlrvEgfkIg1VMkHeg0
wgpJXJxDBwJBAJNc1jzX/MKH1lplmnePr6IuM2/xdX2sbsdYBo9UE895XnxWnJ7o
niVAKVNmU55BM5QYxiUEu1AnipQPeRWpnO0CQDtx/2M2vcIi2GApYjvL1MU22M6f
EHxBYhEL9jkb/Ptx9kVY0vW4Lb+Jm5gSOuK6AVfrGcmhWupCygjtSGb3eRUCQQCD
pA5aQhQw70nkbRllLz2VorIekVQE1XIMsC0EAvbDg8eNSY4WQvVrj3qbXzDZkaNy
7AKt9SEjxH7+Lyha2q8tAkEAt6332cl3Dwuchzb1pJJUoUPSV01a7OG0dRYZV8nS
a+aFGr1vI+Y4WJTmWdOXZlg3A/nQavACH4zGtJLZwH+6dA==
''',
                        'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCUEfHy7EmmNSEoaMEvzWeWk/IY
8k7Hp6J8JA812YzSWEXFnl0OFmATp/vcKWpDKGcKr34xsP9VbcZqvrH3dJIG1gEY
fn74PkKy1knIdJteDllf2VLBbe1EYBpwcuwPmIlPC3t1u9lcQGeUQKPgW/3R+WTI
H584Xyw+myN12tw5wQIDAQAB
-----END PUBLIC KEY-----''',
                        'payConfig':
                            {
                                'TY9999D0002001':'1',
                                'TY9999D0030011':'10',
                                'TY9999D0030012':'11',
                                'TY9999D0050001':'12',
                                'TY9999D0050007':'13',
                                'TY9999D0050008':'14',
                                'TY9999D0100001':'15',
                                'TY9999D0100011':'16',
                                'TY9999D0100012':'17',
                                'TY9999D0300001':'18',
                                'TY9999D1000001':'19',
                                'TY9999D0005003':'2',
                                'TY9999R0008005':'20',
                                'TY9999R0030001':'21',
                                'TY9999R0050001':'22',
                                'TY9999R0100001':'23',
                                'TY9999D0006016':'3',
                                'TY9999D0008001':'4',
                                'TY9999D0008005':'5',
                                'TY9999D0008025':'6',
                                'TY9999D0008026':'7',
                                'TY9999D0010001':'8',
                                'TY9999D0030001':'9',
                            }
                    },
                    #五子棋
                    '3004491175':{
                        'appkey':'''
MIICXAIBAAKBgQCqnGsff7ixoYzVW8409TRGdaSwGnfZPEpM68y9COrjOiZtwqaI
uUPeBsTDRZijCk+SgrN7/hvOCGwBMK4lxNretoC9kxXJ1pvlfMiEUP0qaElKOG2t
iXabsuXQJayQhF5Pk7fxvjm00kOOJOJ4WcQtmIF3ltyH2vt1GPg6Lv5zQQIDAQAB
AoGBAIk6AOu4Bm1RnH5sNkLgSyi1LT68O1POq5CNRQNzLcKQniJAo0Rrh4wI87CA
xRG2lGQqnoUH0YN5wK2AY0JbwRJ5GUJYL/hqUgLlUaKuorPI+JMajTh+UWuAY82e
HDpf84QTB3+LosNWJQ1sC+iQ+GrhofrCxROeN6zDLvgyfUp1AkEA6/oKlU6yKAfy
+i4lIAfgErP5x+myTam6fV2Zqs+lZDAi9crVX0f3YUN/eA+Bm/8POkliXYczIBEZ
3vuWaHh08wJBALkWe6jA77iq6Z8GhB5gGNfrf0Al8evMwRvQxMj+sChJT+z/K1fA
FmDymOUkpZ+80JOba6G9Jqy1dGm2fuNjU/sCQE37seepvCKSje+ztD0jnR9RLuis
CGq1/pVTi2bxfDzh04va3izAwbX48nUg2rpMziF7AvDZr0GXpS8VgZ1AwZUCQDcJ
mHv141Lmf9Hp/h+KM9kBDjXlEqsrl8DNs7aRBZD1O+8dcaYGWKE7gnuhCh8V5m/+
J2NQ+88fph5JRjIXt0ECQGn49LMfEOk+uao+pYtyf0NqvPn2SHwZzRT61b320frS
088+fiyaMUG/Lakl4+CbZu+IfaVf8CDswvtj0Kfy57E=
''',
                        'pubkey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCvMjEa2KajabiXsMDTKgjHaBxM
EF8jieQYaWGLL0WB4FpTU5TWwKDBEFjUqpcNbvbN+nXsHoJImj1K6EjRdRsH6JIo
uDcWoQ2j0qG0VvL38XPVvoKzjz8k+ypRKdHqbcKxsYpTsTGKGRZeHm83pOWD6wff
QH927/dMNbc06myhKwIDAQAB
-----END PUBLIC KEY-----''',
                        'payConfig':
                            {
                                "TY9999R0000101":1,
                                "TY9999D0001003":2,
                                "TY9999D0002001":3,
                                "TY9999D0005003":4,
                                "TY9999D0006016":5,
                                "TY9999D0008027":6,
                                "TY9999D0008001":7,
                                "TY9999D0008025":8,
                                "TY9999D0008026":9,
                                "TY9999R0008005":10,
                                "TY9999D0010001":11,
                                "TY9999D0008005":6,
                                "TY9999D0012004":17,
                                "TY9999D0030001":18,
                                "TY9999D0030011":19,
                                "TY9999D0030012":20,
                                "TY9999D0050001":21,
                                "TY9999D0050007":22,
                                "TY9999D0050008":23,
                                "TY9999D0100001":24,
                                "TY9999D0100011":25,
                                "TY9999D0100012":26,
                                "TY9999D0300001":27,
                                "TY9999D1000001":28,
                                "TY9999R0030001":29,
                                "TY9999R0050001":30,
                                "TY9999R0100001":31,
                            }
                    },
                    #三星 电玩捕鱼
                    '5000166162': {
                        'appkey': '''
MIICXgIBAAKBgQDZse7FTJkRQ2wryukZ0Lz5c00QdJkW68ZW7gC/Jk7PP9ucfjCb
cZibSSR/UyaMsXkDtuirDjxJky95+gG6yNelp+53zyqOfytq4cAxXVx132e15/sc
lNLBW5UzuWDvopfhGGK4tz6/i1Fg6i1e/vch/SaAoIyk7BB4iuTD6+DDCwIDAQAB
AoGBAIS8UXJLuikkixhIqMjs1czj2OFnttCbAlyO0jW7DeKgdS9+YfTl1r8YYgCg
mqi+raLuK//gtjHGZPRi1BsnyxQ+kOn7HGJke+ZFxIzdnWJxFzY1WgixC5tlVmfi
+Nq7eU8m57NfaIU4gMJ9vgaR0qaDXdAschDKro3G3JVboi0BAkEA97NE1ooVMkhj
DzrQIwzQB/toajJDGAEYkSGzn7qVfh3XNaxchfsDlcMFZmMcRX8NgswOlhPuJKos
RczVXH4tewJBAOD9SLopfALW+Aa6W1HsbM8B27xPPi0ywIOcQ06wqxd7+Ca66CpS
Gy1u0Zt3AECpe+ppfZv1oYfNDcKKmuqqo7ECQQDxuJT91CSZPEDHNPq2qaM9lt8v
ezs0aqVhxAS5ZGjMeSxyaXClIu89r+JOJ3wIadNyh9XYKTzltNediiXQrCWPAkB+
qTjrTPV6p8jkCL/mZAJxm6s33Si0y1CkBzHBOCZpxynRrAGN6cFRF4U7T4g93uxa
8F59kZAJYsAvWFaUa9JRAkEAsGDacyepdWwskYkW/XcdmXauTkonqHXdckkcgEnh
FvCgfSKrl/r4MzL+nlAkdVDfcgI7BOGOUqMiSi9QhnHOhA==''',
                        'pubkey': '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCK3zAkS4iYT9PMNNlReWhijRX5
nDIihzCE+cIKOVd6ZVILTBXnATPYoEofhI6UA1oTeeTd9UrTlggF+pxwdCaK1vrx
MzeUqwER16qr8bFKjHCsbwTByYjKIRXe2L9PSnz+hQsbXFB4AEU5pSosnYUUO67z
u0iISsMNCY6rZ8de3wIDAQAB
-----END PUBLIC KEY-----''',
                        'payConfig':  {
                            "p4": 1,
                            "p1": 2,
                            "p6": 3,
                            "p7": 4,
                            "p8": 5,
                            "p9": 6,
                            "p10": 7,
                            "p11": 8,
                            "p12": 9,
                            "p13": 10,
                            "p14": 11,
                            "p15": 12,
                            "p16": 13,
                            "p17": 14,
                            "p18": 15,
                            "p19": 1
                        }
                    }

})
add_global_item('jinri_prodids', {
    6: {
        'TY9999D0002001'          : {'feecode':'1',  'name':'20000金币',     },
        'TY9999D0006001'          : {'feecode':'2',  'name':'60000金币',     },
        'TY9999D0008002'          : {'feecode':'3',  'name':'8元转运礼包',   },
        'TY9999D0008001'          : {'feecode':'4',  'name':'超值礼包',  },
        'TY9999R0008001'          : {'feecode':'5',  'name':'80钻石',     },
        'TY9999R0100001'          : {'feecode':'6',  'name':'1000钻',     },
    },
})


'''E付通api支付配置
'''
add_global_item('eftapi_config', {
    'KeyWords' : 'ZT',
    'paykey':'8E26F8C036DB449D',
    'yd_support_fee':[],
    'lt_support_fee':[1, 2, 3, 5, 6, 8, 10, 30],
    'dx_support_fee':[1, 2, 3, 5, 6, 8, 10, 30],
    'createorder_url':'http://mh.5151pay.com/GetChannel/ReturnChannel.aspx',
})


'''掌阅配置
'''
add_global_item('zhangyue_paykeys', {
    'b70815013ace905a0c43': '375d9b3e9',
    '3e02f7a3e7fd2ca62cc3': '94066bcff',
    'eedad56c4eb919e42542': 'f02825465',
})

#今日头条配置
add_global_item('jinritoutiao_config',{
    '115dec0fd036088f': {
    'url': 'https://open.snssdk.com/partner_sdk/check_user/?',
    'pay_ras_pub_key':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDOZZ7iAkS3oN970+yDONe5TPhP
rLHoNOZOjJjackEtgbptdy4PYGBGdeAUAz75TO7YUGESCM+JbyOz1YzkMfKl2HwY
doePEe8qzfk5CPq6VAhYJjDFA/M+BAZ6gppWTjKnwMcHVK4l2qiepKmsw6bwf/kk
LTV9l13r6Iq5U+vrmwIDAQAB
-----END PUBLIC KEY-----
''',
      },
    })

# uc支付方式配置
add_global_item('uc_config', {
    '551961': {'apiKey': 'de364d504a8a520d3f2100231939d265',
               'cpId': '30574',}
})

#ucdj支付方式配置
add_global_item('ucdj_config', {
    '524526': {'apiKey': '03c6b06952c750899bb03d998e631860'},
    '551961': {'apiKey': 'de364d504a8a520d3f2100231939d265'},
    '540844': {'apiKey': '9ff453d4191f35daff514ac0961bafa9'},
    '617605': {'apiKey': '6c37fabfacfdbb6ae76267a1f97c1528'},
    '617602': {'apiKey': 'cb0b0ea80178b4798cee91a8206ccc81'},
    '617524': {'apiKey': 'b8419949f32405a8fab47533f4310c05'},
    '610905': {'apiKey': 'ad16779ced343dee91b207393228c90d'},
    '619475': {'apiKey': '1729f6061f2fb9df87a9928063266954'},
    '632102': {'apiKey': 'ae38f7c40a16673afc0c8df7fc429d16'},
    '622374': {'apiKey': '2c9d6e521bb15699500efbd487a75a09'},#途游斗地主
    '640381': {'apiKey': '7f9ad50fbc947318a696852b8c41572a'},#途游跑胡子
    '661936': {'apiKey': 'fc20eeaaddf2c1872a2b6d3527b273e5'},#途游四国军棋
    '726907': {'apiKey': '8504e1380d3ea08ad7d410746930f5f7'},#四川麻将-HD
    })


#oppo配置
add_global_item('oppo_config',{
    'url':'http://thapi.nearme.com.cn/account/GetUserInfoByGame'
    })

# meizu appkey 此处appkey 对应打包需求中得appSecret
add_global_item('meizu_config', {
    '2509046':{ 'appkey': 'V5vmjicitlU5UDL1sLe0dVKzdKbpEAsc'} ,
    '2509044':{ 'appkey':'I3PkC5SVgX1Q1atP0jdGDZNqHrshRtZu'},
    '2509045':{ 'appkey':'g9UGgv01xMxkZbOpcUZxNjrBrRLM6mek'},
    '1826261':{ 'appkey':'BiD1GcCxPU7AD5hhg7vuWJUhydDvIdEk'},
    '2586353':{ 'appkey':'crk0M0gdE8AgQ6qvGuWm5B5X1d2dCvzQ'},
    '2578615':{ 'appkey':'wp4dYVGvYd4EzHNkiC4kmFSIBfvk9ccr'},
    '2722200':{ 'appkey':'lcYiT0Y4dRLaJZ5Y2ydpg9mCchSGaMFZ'},#象棋appsecret
    '2866133':{ 'appkey':'1nk1342Zg69XefMoygJQElQAjJYFdR2v'},#象棋appsecret
    '2998925':{ 'appkey':'vwOip7F3l0jAsNBCOf91KFx9jwNry23S'},
    '1892314':{ 'appkey':'LYDfHWcEigeKVJwaMeQDKxE0bipHZAbx'},
    '2509054':{ 'appkey':'ajoCG6NinBcqxMJx1yM08DHe7Z802Vls'}})

# daodao 配置
add_global_item('daodao_prodids',{
    '64eb3d23f0183178e4f6ee7645c7dd55' :
        {
        'TY9999D0002001': {'price':'200',    'name':'20000金币', 'feecode':'game_item_EftU6j'},
        'TY9999D0006001': {'price':'600',    'name':'60000金币', 'feecode':'game_item_3XS4Qr'},
        'TY9999D0100001': {'price':'10000',  'name':'1000000金币', 'feecode':'game_item_2fBpwl'},
        'TY9999R0008001': {'price':'800',    'name':'80钻石', 'feecode':'game_item_aStvyN'},
        'TY0006D0002001': {'price':'200',    'name':'月光之钥', 'feecode':'game_item_qy6k2B'},
        'TY0006D0005001': {'price':'500',    'name':'月光之钥x3', 'feecode':'game_item_MdiSWw'},
        'TY9999D0008002': {'price':'800',    'name':'8元转运礼包', 'feecode':'game_item_sp0OAS'},
        }
    })

# yygame 配置
add_global_item('yy_config',{ 
    'MTUYOU':{ 'appkey': 'ac8bb8c3612a4d808755a2f325876c75'},#地主
    'MTYBH':{ 'appkey': 'WGB8W3TABCY902Z2M48I8Z88BGWXZEXG'}#保皇
})
# 9秀支付方式配置
add_global_item('9xiu_config', {
    '4003': 'tuniur8*nv'
})

# iiapple配置appKey:secretKey
add_global_item('iiapple_config', {
    '9086fffa143ec3761622d7ce39887e2e':'75b04253979851fd7d828ce70d9644fb' ,
    '97ae5c8a3c8b4becd56db6c8eaf48ec2':'5e8ec6eab613f4bce8f696f0590e9073' ,
    })

'''数字天域支付配置
'''
add_global_item('shuzitianyu_config', {
    'createorder_url':'http://rdo.lianluo.com/rdo_mo.php',
    'callback_ip':'58.215.184.145',
    'paycode_config':{
                       '2'  :{'feecode':'23000002', 'channelid':'00528', 'oid':'110106', 'port':'10658421018'},
                       '5'  :{'feecode':'23000005', 'channelid':'00536', 'oid':'110106', 'port':'10658421018'},
                       '6'  :{'feecode':'23000006', 'channelid':'00529', 'oid':'110106', 'port':'10658421018'},
                       '8'  :{'feecode':'23000008', 'channelid':'00533', 'oid':'110106', 'port':'10658421018'},
                       '10' :{'feecode':'23000010', 'channelid':'00530', 'oid':'110106', 'port':'10658421018'},
                       '30' :{'feecode':'23000013', 'channelid':'00531', 'oid':'110106', 'port':'10658421018'},
                     },
})


'''数字天域h5支付配置
'''
add_global_item('shuzitianyu_h5_config', {
    'createorder_url':'http://112.25.15.148:8081/proxy/syncorder',
    'callback_ip':'125.39.218.101',
    'paycode_config':{
                       '4'  :{'port':'106584221','scid':'89'},
                       '6'  :{'port':'106584221','scid':'90'},
                       '8'  :{'port':'106584221','scid':'91'},
                     },
})


# momo支付方式配置
add_global_item('momo_paykeys', {
    'ex_ddz_8nTFeiGK': 'EDE4378B-B0AD-09FA-8941-356DF6D90342'
})

add_global_item('momo_prodids', {
    6: {
        'TY9999D0002050':{'feecode':'com.wemomo.game.ddz.68', 'name':'地主小礼包' },
        'TY9999D0006050':{'feecode':'com.wemomo.game.ddz.48', 'name':'地主体验礼包' },
        'TY9999D0012050':{'feecode':'com.wemomo.game.ddz.21', 'name':'地主特惠礼包' },
        'TY9999D0030050':{'feecode':'com.wemomo.game.ddz.22', 'name':'地主豪华礼包' },
        'TY9999D0068050':{'feecode':'com.wemomo.game.ddz.23', 'name':'顺发大礼包' },
        'TY9999D0128050':{'feecode':'com.wemomo.game.ddz.24', 'name':'聚财大礼包' },
        'TY9999D0328050':{'feecode':'com.wemomo.game.ddz.25', 'name':'土豪大礼包' },
        'TY9999D0006051':{'feecode':'com.wemomo.game.ddz.36', 'name':'月光宝盒礼包' },
        #'TY9999D0006052':{'feecode':'com.wemomo.game.ddz.26', 'name':'语音小喇叭100个' },
        'TY9999D0006053':{'feecode':'com.wemomo.game.ddz.37', 'name':'参赛券x30' },
        'TY9999D0012052':{'feecode':'com.wemomo.game.ddz.27', 'name':'7天记牌器' },
        'TY9999D0006054':{'feecode':'com.wemomo.game.ddz.38', 'name':'转运礼包' },
        'TY9999D0030051':{'feecode':'com.wemomo.game.ddz.39', 'name':'转运大礼包' },
        'TY9999D0030052':{'feecode':'com.wemomo.game.ddz.42', 'name':'VIP普通礼包' },
        'TY9999D0068051':{'feecode':'com.wemomo.game.ddz.43', 'name':'VIP豪华礼包' },
        'TY9999D0006055':{'feecode':'com.wemomo.game.ddz.28', 'name':'50000金币' },
        'TY9999D0012051':{'feecode':'com.wemomo.game.ddz.29', 'name':'100000金币' },
        'TY9999D0018051':{'feecode':'com.wemomo.game.ddz.30', 'name':'170000金币' },
        'TY9999D0030053':{'feecode':'com.wemomo.game.ddz.31', 'name':'300000金币' },
        'TY9999D0068052':{'feecode':'com.wemomo.game.ddz.32', 'name':'700000金币' },
        'TY9999D0128051':{'feecode':'com.wemomo.game.ddz.33', 'name':'1500000金币' },
        'TY9999D0006056':{'feecode':'com.wemomo.game.ddz.35', 'name':'月光之钥x3' },
        #'TY9999D0006057':{'feecode':'com.wemomo.game.ddz.34', 'name':'语音小喇叭100个' },
        'TY9999D0006058':{'feecode':'com.wemomo.game.ddz.40', 'name':'转运礼包' },
        'TY9999D0030054':{'feecode':'com.wemomo.game.ddz.41', 'name':'转运大礼包' },
        'TY9999D0012053':{'feecode':'com.wemomo.game.ddz.45', 'name':'记牌器7天' },
        'TY9999D0030055':{'feecode':'com.wemomo.game.ddz.46', 'name':'普通VIP礼包' },
        'TY9999D0068053':{'feecode':'com.wemomo.game.ddz.47', 'name':'豪华VIP礼包' },
        #
        #         #momo temp
        #         'TY9999D0006050':{'feecode':'com.wemomo.game.ddz.58', 'name':'地主体验礼包' },
        #         'TY9999D0012050':{'feecode':'com.wemomo.game.ddz.49', 'name':'地主特惠礼包' },
        #         'TY9999D0030050':{'feecode':'com.wemomo.game.ddz.50', 'name':'地主豪华礼包' },
        #         'TY9999D0006051':{'feecode':'com.wemomo.game.ddz.53', 'name':'月光宝盒礼包' },
        #         'TY9999D0006053':{'feecode':'com.wemomo.game.ddz.54', 'name':'参赛券x30' },
        #         'TY9999D0012052':{'feecode':'com.wemomo.game.ddz.52', 'name':'7天记牌器' },
        #         'TY9999D0006054':{'feecode':'com.wemomo.game.ddz.55', 'name':'转运礼包' },
        #         'TY9999D0030052':{'feecode':'com.wemomo.game.ddz.57', 'name':'VIP普通礼包' },
        #         'TY9999D0030051':{'feecode':'com.wemomo.game.ddz.56', 'name':'转运大礼包' },
    },
})

'''pp钱包支付配置
'''
add_global_item('palm_config', {
    #test
    'merc_id':'1000002395',
    'createorder_url':'http://124.193.184.92:8000/bfsmob/http',
    'key':'xyWM4as64gUVXoh4k9+62xVn8pl+PC3K',
    #'merc_id':'2015041717',
    #'createorder_url':'https://www.paypalm.cn/bfsmob/http',
    #'key':'8Em453/4zebgCWFWNefJgxK7UeyJp8jA',
})

'''
个付平台，区分 移动，联通，电信 url , 第三方接入号码, 第三方md5key
'''
add_global_item('gefupay_config', {
    # thirdPartyId -> {}
    '32': {
        'chinaMobile':'http://pay.imread.com:8083/cmcc/sms',
        'chinaUnion':'http://pay.imread.com:8081/cnet/sms',
        'chinaTelecom':'http://pay.imread.com:8081/union/sms',
        'md5key':'ljziuzpg4dqvnlb',
    },
    '43': {
        'md5key':'ljziuzpg4dqvnlb',
        'chinaMobile':'http://pay.imread.com:8081/cmcc/sms',
        'chinaUnion':'http://pay.imread.com:8081/cnet/sms',
        'chinaTelecom':'http://pay.imread.com:8081/union/sms',
    }
})

'''
个付平台大额,个付平台大额走的第三方支付通道,爱贝微支付
'''
add_global_item('geFuBigSdk_config',{
        'appId':'3002540736',
        'appName':'单机斗地主',
        'waresId':'1',
        'createOrderUrl':'http://ipay.iapppay.com:9999/payapi/order'
    }
)

'''mopo 平台秘钥 计费点信 http://dev.mopo.com/home/app-list ZIMON 中心 
'''
add_global_item('maopao_config', {
    'md5key':'sdajdlkajld3u-1234',
    'paysms':[2,4,6,8,10],
    '7011337':{'TY9999D0002001':'1',
               'TY9999D0006016':'2',
               'TY9999D0008026':'3',
               'TY9999D0008001':'4',
               'TY9999R0008005':'5',
               'TY9999D0010004':'6',
               'TY9999D0008025':'7',
               'TY9999D0008005':'8',
               'TY9999D0010001':'9',

    },
    '7012185':{'TY9999D0002001':'1',
               'TY9999D0006016':'2',
               'TY9999D0008005':'3',
               'TY9999D0008001':'4',
               'TY9999D0008025':'5',
               'TY9999D0008026':'6',
               'TY9999R0008005':'7',
               'TY9999D0010001':'8',
    },
    '7011338':{'TY0008D0008001':'1',
               'TY9999R0008001':'2',
               'TY9999D0008001':'3',
               'TY9999D0008002':'4',
    },
    '7011339':{'TY0007D0008001':'1',
               'TY9999R0008001':'2',
               'TY9999D0008001':'3',
               'TY9999D0008002':'4',
    },

    '7011340':{'TY9999D0002001':'1',
               'TY9999D0006001':'2',
               'TY9999D0008002':'3',
               'TY9999D0008001':'4',
               'TY9999R0008001':'5'
    }
    
})

add_global_item('aidongmanpay_config', {
        'createorderUrl':'http://114.113.155.232:8888/sync/32',
        '3des':
              {'iv':'12345678',
               'encryptKey':'B97FED4E9994E33353F2A65A063DFAA8A31428E11BD7AE59'
              }
})

#按游戏区分的 APPID 用来区分不同游戏--6
add_global_item('aidongmanpay_prodids', {
        '6': {
        'channelId':'131000MO000001',
        'TY9999D0002001': {'smscodes':'131000MO000001B001WE001',
                           'smsports':'11802115020'},
        'TY9999D0006001': {'smscodes':'131000MO000001B001WF001',
                           'smsports':'11802115060'},
        'TY9999R0008001': {'smscodes':'131000MO000001B001WG001',
                           'smsports':'11802115080'},
        'TY9999D0008001': {'smscodes':'131000MO000001B001WH001',
                           'smsports':'11802115080'},
        'TY9999D0008002': {'smscodes':'131000MO000001B001WI001',
                           'smsports':'11802115080'},
    }
})

add_global_item('mingtiandongli_config', {
        'createorderUrl':'http://121.43.235.32:8080/zh_order_platform/CommandApiAction',
        'channelNum':'B2'
})

add_global_item('ppzhushou_config', {
        #'md5key':'nstjae9dPzYLQM8EZE1ZLvHMmpeB7D8ab56IOaEpBXZsxnsMeiaKGHH4jgG0JDF2'
        'md5key':'Aa24F0NBTvnpBSdDNcwuNPfIdyKkBaGfwYm71W68R5ZjdUEAVdBD4NmeL3sgZUJX'
})
'''
XY手机助手平台支付
'''
add_global_item('XYSdk_config',{
        #途游斗地主
        '100021742':{
            'appkey':'rZkmaFD1f9DYmNLzz9zJOFO5BjTAcDFg',
            'paykey':'S3xdvxzNHqc1brCBwiRjLGAa54C2PX1P'
            },
        #途游麻将
        '100027361':{
            'appkey':'CGNqpJeJZjvTY3N5u2Sv5uIQXiormIc5',
            'paykey':'xcArJWZHR8ljxhW4XnRAz2rYWoPyILfT'
            },
    }
)
add_global_item('XYDJSdk_config',{
        #途游单机斗地主
        '100024022':{
            'appkey':'JNPqJoH1v90evunMcRTZf4WpQbeGJNnQ',
            'paykey':'g0bLItqgsMxpK5W6s3r9yvyJd05s322e'
            },
    }
)

'''
海马玩平台
'''
add_global_item('haimawan_config', [
    {
        "appid":"6bc3e34f73ae74e20525f7e5d3c81ee2",
        "appkey":"4c3f0c7a9754cd996c26854e8ba9652f"
    },
    {
        "appid":"25cb17c8c1acbc63d856f09466e9e0d3",
        "appkey":"5045fc01687c529d972f5d97984e987b"
    },
    {
        "appid":"a7d956c17e998ac09e0d80cb8fd7c03c",
        "appkey":"609474372177de3fbfb336bb103bb451"
    },
    {
        "appid":"16eaebeab35ab4a7af144402d8aad821",
        "appkey":"22f14f821e399922337697fe1f31c8cd"
    }
])
'''
优易付,wap支付,音乐基地
'''
add_global_item('yipaywap_config:Android_3.501_tuyoo.yisdkpay.0-hall6.youyifu.happy', {
    'merc_id' : '2000024',
    'app_id':'9ea5900282ab11e5a9bf3ab47144b7ab',
    'yipay_key':'fda8c042c87f2fdb031110c9eadc8dec',
    'createorder_url':'http://fee.aiyuedu.cn:23000/sdkfee/api2/create_order',
    'verconfirmurl':'http://fee.aiyuedu.cn:23000/sdkfee/api2/ver_confirm',
    'clientId':'Android_3.501_tuyoo.yisdkpay.0-hall6.youyifu.happy',
    #coins
    'TY9999D0008001': {'price':'80','des':'80000金币', 'scheme':2, 'feecode':5},
    'TY9999D0002001': {'price':'20','des':'20000金币', 'scheme':2,'feecode':2},
    'TY9999D0005003': {'price':'50','des':'途游斗地主5元充值', 'scheme':2,'feecode':3},
    'TY9999D0006016': {'price':'60','des':'途游斗地主6元充值', 'scheme':2,'feecode':4},
    'TY9999D0008027': {'price':'80','des':'途游斗地主8元充值', 'scheme':2,'feecode':5},
    'TY9999D0012002': {'price':'120', 'des':'会员订阅', 'scheme':2, 'feecode':6},
    'TY9999D0012003': {'price':'120', 'des':'会员订阅', 'scheme':2, 'feecode':6},
    'TY9999D0012004': {'price':'120', 'des':'会员订阅', 'scheme':2,'feecode':6},
    'TY9999D0001001': {'price':'10', 'des':'途游斗地主1元充值', 'scheme':2, 'feecode':1},
    #diamond
    'TY9999R0000101':{'price' : 1,     'des':'钻石x1',     'scheme':2,   'feecode':1,},
    'TY9999R0001001':{'price' : 10,    'des':'钻石x10',    'scheme':2,   'feecode':2},
    'TY9999R0002001':{'price' : 20,    'des':'钻石x20',    'scheme':2,   'feecode':3},
    'TY9999R0003001':{'price' : 30,    'des':'钻石x30',    'scheme':2,   'feecode':4},
    'TY9999R0004001':{'price' : 40,    'des':'钻石x40',    'scheme':2,   'feecode':5},
    'TY9999R0005001':{'price' : 50,    'des':'钻石x50',    'scheme':2,   'feecode':6},
    'TY9999R0006001':{'price' : 60,    'des':'钻石x60',    'scheme':2,   'feecode':7},
    'TY9999R0007001':{'price' : 70,    'des':'钻石x70',    'scheme':2,   'feecode':8},
    'TY9999R0008001':{'price' : 80,    'des':'钻石x80',    'scheme':2,   'feecode':9},
    'TY9999R0009001':{'price' : 90,    'des':'钻石x90',    'scheme':2,   'feecode':10},
    'TY9999R0010001':{'price' : 100,   'des':'钻石x100',   'scheme':2,   'feecode':11},
    'TY9999R0011001':{'price' : 110,   'des':'钻石x110',   'scheme':2,   'feecode':12},
    'TY9999R0012001':{'price' : 120,   'des':'钻石x120',   'scheme':2,   'feecode':13},
    'TY9999R0013001':{'price' : 130,   'des':'钻石x130',   'scheme':2,   'feecode':14},
    'TY9999R0014001':{'price' : 140,   'des':'钻石x140',   'scheme':2,   'feecode':15},
    'TY9999R0015001':{'price' : 150,   'des':'钻石x150',   'scheme':2,   'feecode':16},
    'TY9999R0016001':{'price' : 160,   'des':'钻石x160',   'scheme':2,   'feecode':17},
    'TY9999R0017001':{'price' : 170,   'des':'钻石x170',   'scheme':2,   'feecode':18},
    'TY9999R0018001':{'price' : 180,   'des':'钻石x180',   'scheme':2,   'feecode':19},
    'TY9999R0019001':{'price' : 190,   'des':'钻石x190',   'scheme':2,   'feecode':20},
    'TY9999R0020001':{'price' : 200,   'des':'钻石x200',   'scheme':2,   'feecode':21},
    'TY9999R0021001':{'price' : 210,   'des':'钻石x210',   'scheme':2,   'feecode':22},
    'TY9999R0022001':{'price' : 220,   'des':'钻石x220',   'scheme':2,   'feecode':23},
    'TY9999R0023001':{'price' : 230,   'des':'钻石x230',   'scheme':2,   'feecode':24},
    'TY9999R0024001':{'price' : 240,   'des':'钻石x240',   'scheme':2,   'feecode':25},
    'TY9999R0025001':{'price' : 250,   'des':'钻石x250',   'scheme':2,   'feecode':26},
    'TY9999R0026001':{'price' : 260,   'des':'钻石x260',   'scheme':2,   'feecode':27},
    'TY9999R0027001':{'price' : 270,   'des':'钻石x270',   'scheme':2,   'feecode':28},
    'TY9999R0028001':{'price' : 280,   'des':'钻石x280',   'scheme':2,   'feecode':29},
    'TY9999R0029001':{'price' : 290,   'des':'钻石x290',   'scheme':2,   'feecode':30},
    'TY9999R0030001':{'price' : 300,   'des':'钻石x300',   'scheme':2,   'feecode':31},
    'paycode_config':{
        '1' :'1',
        '2' :'2',
        '4' :'9',
        '5' :'3',
        '6' :'4',
        '8' :'5',
        '10':'6',
        '12':'6',
        '20':'1',
    },
    'monthly_prods':['TY9999D0020001', 'TY9999D0012002', 'TY9999D0012003', 'TY9999D0012004'],
})

'''
优易付,wap支付,DDO
'''
add_global_item('yipaywap_config:Android_3.701_tuyoo.yisdkpay.0-hall6.youyifu.happy', {
    'merc_id' : '2000084',
    'app_id':'2ca2283e942211e5b6cfbe3c3fd80617',
    'yipay_key':'3eef887fd8cfa49bee3afb38d00fa72f',
    'createorder_url':'http://fee.aiyuedu.cn:23000/sdkfee/api2/create_order',
    'verconfirmurl':'http://fee.aiyuedu.cn:23000/sdkfee/api2/ver_confirm',
    'clientId':'Android_3.501_tuyoo.yisdkpay.0-hall6.youyifu.happy',
    #diamond
    'TY9999R0000101':{'price' : 1,     'des':'钻石x1',     'scheme':2,   'feecode':1,},
    'TY9999R0001001':{'price' : 10,    'des':'钻石x10',    'scheme':2,   'feecode':2},
    'TY9999R0002001':{'price' : 20,    'des':'钻石x20',    'scheme':2,   'feecode':3},
    'TY9999R0003001':{'price' : 30,    'des':'钻石x30',    'scheme':2,   'feecode':4},
    'TY9999R0004001':{'price' : 40,    'des':'钻石x40',    'scheme':2,   'feecode':5},
    'TY9999R0005001':{'price' : 50,    'des':'钻石x50',    'scheme':2,   'feecode':6},
    'TY9999R0006001':{'price' : 60,    'des':'钻石x60',    'scheme':2,   'feecode':7},
    'TY9999R0007001':{'price' : 70,    'des':'钻石x70',    'scheme':2,   'feecode':8},
    'TY9999R0008001':{'price' : 80,    'des':'钻石x80',    'scheme':2,   'feecode':9},
    'TY9999R0009001':{'price' : 90,    'des':'钻石x90',    'scheme':2,   'feecode':10},
    'TY9999R0010001':{'price' : 100,   'des':'钻石x100',   'scheme':2,   'feecode':11},
    'TY9999R0011001':{'price' : 110,   'des':'钻石x110',   'scheme':2,   'feecode':12},
    'TY9999R0012001':{'price' : 120,   'des':'钻石x120',   'scheme':2,   'feecode':13},
    'TY9999R0013001':{'price' : 130,   'des':'钻石x130',   'scheme':2,   'feecode':14},
    'TY9999R0014001':{'price' : 140,   'des':'钻石x140',   'scheme':2,   'feecode':15},
    'TY9999R0015001':{'price' : 150,   'des':'钻石x150',   'scheme':2,   'feecode':16},
    'TY9999R0016001':{'price' : 160,   'des':'钻石x160',   'scheme':2,   'feecode':17},
    'TY9999R0017001':{'price' : 170,   'des':'钻石x170',   'scheme':2,   'feecode':18},
    'TY9999R0018001':{'price' : 180,   'des':'钻石x180',   'scheme':2,   'feecode':19},
    'TY9999R0019001':{'price' : 190,   'des':'钻石x190',   'scheme':2,   'feecode':20},
    'TY9999R0020001':{'price' : 200,   'des':'钻石x200',   'scheme':2,   'feecode':21},
    'TY9999R0021001':{'price' : 210,   'des':'钻石x210',   'scheme':2,   'feecode':22},
    'TY9999R0022001':{'price' : 220,   'des':'钻石x220',   'scheme':2,   'feecode':23},
    'TY9999R0023001':{'price' : 230,   'des':'钻石x230',   'scheme':2,   'feecode':24},
    'TY9999R0024001':{'price' : 240,   'des':'钻石x240',   'scheme':2,   'feecode':25},
    'TY9999R0025001':{'price' : 250,   'des':'钻石x250',   'scheme':2,   'feecode':26},
    'TY9999R0026001':{'price' : 260,   'des':'钻石x260',   'scheme':2,   'feecode':27},
    'TY9999R0027001':{'price' : 270,   'des':'钻石x270',   'scheme':2,   'feecode':28},
    'TY9999R0028001':{'price' : 280,   'des':'钻石x280',   'scheme':2,   'feecode':29},
    'TY9999R0029001':{'price' : 290,   'des':'钻石x290',   'scheme':2,   'feecode':30},
    'TY9999R0030001':{'price' : 300,   'des':'钻石x300',   'scheme':2,   'feecode':31},
    'paycode_config':{
        '1' :'1',
        '2' :'2',
        '4' :'9',
        '5' :'3',
        '6' :'4',
        '8' :'5',
        '10':'6',
        '12':'6',
        '20':'1',
        },
    'monthly_prods':['TY9999D0020001', 'TY9999D0012002'],
    })

'''
youku h5
'''
add_global_item('youkuh5_config', {
    'loginKey': 'DzgHPkXKlRiNfmYP',
    'payKey': 'zRCrBK2reDU5wYjS',
    'gkey': 'ykddz'
})

add_global_item('yipay_passthrough_address',{
    '/v1/pay/liantongw/callback':'http://113.31.25.51:21000/feegate/third/tuyoo_wooshop/check_or_notify',
    '/v1/pay/ydmm/callback'     :'http://113.31.25.51:21000/feegate/third/tuyoo_mm/notify',
    '/v1/pay/ydjd/callback'     :'http://113.31.25.51:21000/feegate/third/tuyoo_mobile_game/notify',
    '/v1/pay/aigame/all/callback'   :'http://113.31.25.51:21000/feegate/third/tuyoo_tel_i_game/notify',
    '/v1/pay/aiyouxi/callback/dizhu/happy': 'http://113.31.25.51:21000/feegate/third/tuyoo_tel_i_game/notify',
    '/v1/pay/aiyouxi/callback/dizhu/tyhall': 'http://113.31.25.51:21000/feegate/third/tuyoo_tel_i_game/notify',
    '/v1/pay/aiyouxi/callback/dizhu/kugou': 'http://113.31.25.51:21000/feegate/third/tuyoo_tel_i_game/notify',
    '/v1/pay/aiyouxi/callback/dizhu/huabei': 'http://113.31.25.51:21000/feegate/third/tuyoo_tel_i_game/notify',
    '/v1/pay/aiyouxi/callback/dizhustar/zszh/wf': 'http://113.31.25.51:21000/feegate/third/tuyoo_tel_i_game/notify',
    '/v1/pay/aiyouxi/callback/dizhustar/zszh/pt': 'http://113.31.25.51:21000/feegate/third/tuyoo_tel_i_game/notify',
    '/v1/pay/gefu/callback': 'http://113.31.25.56:21000/feegate/third/gefu/notify'
})

add_global_item('payfail_returnconfig', {
    'CAT_LIST_360':'more_categories_360',
    'CAT_LIST_TUYOU':'more_categories_tuyou',
    'CAT_LIST_360_DEZHOU':'more_categories_360dezhou',
    'CAT_LIST_TUYOU_WEIXIN':'more_categories_tuyou_weixin',
    'TY9999R0000101':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0001003':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0002001':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0008005':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0008001':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0008025':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0008026':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999R0008005':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0010001':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0005003':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0006016':{'des':'支付失败,请尝试支付宝支付吧'},
    'TY9999D0008027':{'des':'支付失败,请尝试支付宝支付吧'},
    #测试用
    'TY9999R0050001':{'des':'支付失败,请尝试支付宝支付吧'},
})

add_global_item('kuaiyongpingguo_config', {
    'appKey':'059d5f10c7aca1af2e1716732628cefd'
})

add_global_item('ucdj_paycode_config', {
    "ydjd":{
        "appid": "621216015822",
        "cpid": "772212",
        "paydata": [
            {"prodid": "TY9999R0000101", "msgOrderCode": "015" },
            {"prodid": "TY9999D0001003", "msgOrderCode": "016" },
            {"prodid": "TY9999D0002001", "msgOrderCode": "019" },
            {"prodid": "TY9999D0005003", "msgOrderCode": "020" },
            {"prodid": "TY9999D0006016", "msgOrderCode": "021" },
            {"prodid": "TY9999D0008027", "msgOrderCode": "022" },
            {"prodid": "TY9999D0008001", "msgOrderCode": "023" },
            {"prodid": "TY9999D0008025", "msgOrderCode": "017" },
            {"prodid": "TY9999D0008026", "msgOrderCode": "018" },
            {"prodid": "TY9999R0008005", "msgOrderCode": "012" },
            {"prodid": "TY9999D0010001", "msgOrderCode": "024" }
        ]
    },
    "ydmm":{
        "appid": "300007728518",
        "appkey": "06E2A01050F52F6B",
        "paydata": [
            {"prodid": "TY9999D0001003", "msgOrderCode": "30000772851823" },
            {"prodid": "TY9999D0002001", "msgOrderCode": "30000772851824" },
            {"prodid": "TY9999D0005003", "msgOrderCode": "30000772851825" },
            {"prodid": "TY9999D0006016", "msgOrderCode": "30000772851826" },
            {"prodid": "TY9999D0008027", "msgOrderCode": "30000772851827" },
            {"prodid": "TY9999D0008001", "msgOrderCode": "30000772851819" },
            {"prodid": "TY9999D0008025", "msgOrderCode": "30000772851829" },
            {"prodid": "TY9999D0008026", "msgOrderCode": "30000772851830" },
            {"prodid": "TY9999R0008005", "msgOrderCode": "30000772851820" },
            {"prodid": "TY9999D0010001", "msgOrderCode": "30000772851828" }
        ]
    },
    "liantongwo":{
        "appid": "9014273345620140519164257493800",
        "paydata": [
            {"prodid": "TY9999R0000101", "msgOrderCode": "018" },
            {"prodid": "TY9999D0001003", "msgOrderCode": "019" },
            {"prodid": "TY9999D0002001", "msgOrderCode": "022" },
            {"prodid": "TY9999D0005003", "msgOrderCode": "024" },
            {"prodid": "TY9999D0006016", "msgOrderCode": "026" },
            {"prodid": "TY9999D0008027", "msgOrderCode": "023" },
            {"prodid": "TY9999D0008001", "msgOrderCode": "027" },
            {"prodid": "TY9999D0008025", "msgOrderCode": "020" },
            {"prodid": "TY9999D0008026", "msgOrderCode": "021" },
            {"prodid": "TY9999R0008005", "msgOrderCode": "016" },
            {"prodid": "TY9999D0010001", "msgOrderCode": "025" }
        ]
    }
})

add_global_item('Android_3.71_meizu.meizu,yisdkpay4.0-hall6.meizu.dj', {
        'youyifu':{
            'curPlugVersion':1,
            'curPlugUrl':'',
            'compatibleVesion':1
             }
})

'''
安智配置文件
'''
add_global_item('anzhi_config', [
    {
        'appId':'1443432421LG25c848pw8iFVlQ0Kv3',
        'appsecret':'a77GhxRa8iblJ27x8Qncct8E'
    },
    #欢乐途游斗地主
    {
        'appId':'1444356279NAa457uy9e93jQU42lf8',
        'appsecret':'3K67iH3fWbuN9qY6pjq4dIRe'
    },
    {   'appId': '1462774052NcuNcurVzO72CefxhIAc',
        'appsecret': 'EeAn2EU26Kah08xKl988vUVs',
        '3desKey': 'lzBIQbbjAFyj972hpGwL62ks'
    }
])

'''
同步推配置文件
'''
add_global_item('tongbutui_config', [
    {
        "appid":"150918",
        "appkey":"rBODan#VKXuF8He2B4Olyn@KhXu8RG2q"
    }
])

add_global_item('360_keys',
                {
                    "package":{"com.test.keys":"d5a750de321fc72a13b6fbf14327706f"},
                    "keys":{
                        "d5a750de321fc72a13b6fbf14327706f":"517d4750af306e4a4d0176e49d02e529",
                        "a17b6027130158ae929080a46ff73474":"2af9bf95c4f229995d0e201d74f5b17d",
                        "1b9454c45c83694a2f40d398a9f562dd":"31033078d172daa2df13ebb2155b86c0",
                        "489ba0b056dc391e3d58153da124c65e":"4217ef9098222dc4070f1303318295a5",
                        "87f0b97a1d7b03481b5fa4f782b6828f":"c888b45affe3c49275a732b9cec07b3e",
                        "211c90541f6a46002de31587dec28427":"3c516ce7abd55d13716288f8a882e9cc",
                        "c20e2c2403a8d16ea2b00df78cf6b852":"b966fc0b779fd0608c792b51e7adc7fa",
                        "b0ccd12da2f2334fe096c07a8cf21b52":"ce2d2c04ebf6240027d40cdd8554812b",
                        "eb245dd0ca027a4f3a1736055d9476c4":"512eb27dc4f0ea5ac4cb8f27a687413d",
                        "c25febc9038cd1e438ac38706bf0f857":"13d5fe653d9579a06999e5e4e5599bbe",
                        "c9a6a4713f0d03e63b35360fd793c991":"4e065323f3d5ca8506d1fb174d2cde6a",
                        "48ce7ff5b616bf5a9b5eb411c96a316f":"9b4a1d01ea00cf9229250716961dc28f",
                        "35e15d0507abe5b735544ca75684ff49":"1166349b975cd965b2207f372231ae82",
                        "35e15d0507abe5b735544ca75684ff49":"f022e2060ffe652b4679ee5c35d55013",
                        "959b87e60ea94757ba24e7c89cc9270b":"1dcf1758ff58ca42fc868a74d57401bf",
                        "df5df93d1d25abafd0174d79d0f8e068":"276ca9700ceab60d169984a7a4d63a44",
                        "16b319efe4917b058a456fa5019c931b":"cff9c5d5bc9862f66facb4c4c4b1d176",
                        "3ac03ea5a4af2d11f1a99a8a534701ae":"6cc46a310c92479d44435702d6d5dc33",
                        "765df43db63bd07acbc443c57f30c00a":"7f6e12a895ebdcb045b103ab6f3f603c",
                        "ca537e56d5bc82f57b73358702f39e44":"fc77fb632d9714e4b23f0e5e3f04494a",
                        "45c696c85ceb9e0edec62c05c00439fd":"a4035ba2d613351fafee1ae31ae77313",
                        "90f63d69803e09b447cddc98ed9a117c":"2f254f6f7eb97628c11a1d78f51639bc",
                        "7f3f2d5a4e81daf54e04ebdc9b5f1947":"3def88560b0ef44beb999035d18ee618",
                        "341815d5b878601565f27c1eb7847bfa":"e9d12b6dd6c58950f0116f216f909604",
                        "497f1496ccf0dd09b04e65dc98195c2a":"3dd65e4ef1a5abb983d4335bcb8d28cd",
                        "382acd5f94154a1a25708c3c64e52986":"a56a1a7398ee684a823baec4a72c95ac",
                        "e3236e278904afbedf1bfe19c3597574":"f511ccd45ad48e02c8df301e93891397",
                        "a3f3d2abfab58d273a38c9ead8d7268f":"a06cbb9acac8fdce02ba9f0a0fabf1dc",
                        "fa2fc165fee786d3fefb0b11f0e15312":"c2f12613e505fe7e459df4e97ce81f40",
                        "6660ce9d0b7453981a97f0dee6f6e3cb":"28e8652d63b2b2d41689209733f8afa4",
                        "da82c6c5aa930c5b8f96a0323471056f":"295db2dc4f43c26ac5b3a24492601390",
                        "b06a71d8a4064c2d3ec287d8f502b374":"9cda383f56846fb834172edc4324da71",
                        "7fc7c8e18220e870eed6268bb62b098e":"37c99184a503b2cd7c1023a23f5f5d52",
                        "fd2a4c7c70ad5043b7fc32664ae800cc":"a5d574c7d5fd17fc10cc6fc70545f6de",
                        "bc48c401fb78a526c1d5d0a21c0b4054":"d71d11a511ed0ad34919701b5cc562eb",
                        "58eb3045b7b1f01cf86bfe50880fcac2":"bc93157c143ed0988271a78abb139990",
                        "8be5e9d8f70ddaf4f27fc8c4ae82e4a5":"3c3c9575b9f9de7a7d6d8e5248dccc40",
                        "7b969b1665a1d7157b2c76a4a9ad66bd":"557daf115e62cdc16f59c220a5a0fce1",
                        "e9de9024219cc9027ad3de033f02c22b":"a6eb4efe5544720972497f49f154d7ec",
                        "c129244525d76817e0fde5441495fc51":"866e703563875ca7d8ce2d35773dca4b",
                        "c03fb309e6d07cd9f279c6b20521287d":"21ad7b81098d869f4873c0881f52db82",
                        "fb4616a5cb7ecd3c7644edf9a90d99ab":"a5a6401a12bdb68a534eb2abe5435feb",
                        "f4a06ef85f9fd1a9a66a18b01c9b3d08":"129b4b9749b52efbdb92bce930be154b",
                        "13aecb0cd5c11df5416e46cd4519388a":"f01a56261a5a54b25bef2e62a8ac9a0a",
                        "7f309114ed247ffcb6cc6cec43cb2276":"bfa879d30a64d9ba5d3fea7f4f262e07",
                        "7779f95cff8c29ce7e4ccf7b67b83d9d":"8d4eaa19e5c58d910ed042c65a39bff3",
                        "0f831ef273ebefd94edeaa99038cf22e":"1fddd4cf639230a3ce241eb5d918102d",
                        "19b25445f3d7d3a07b444b40d86c061c":"019ff054a7cd2875ab1a08124c121e79",
                        "7abc137399ca099c2a2530781040cf8c":"5aebf07270841a22149c3faa36e8155d",
                        "e1f20fc31a851a32e3238972095339cc":"3907ba9a1c02bd03b94a441b7ee44b12",
                        "959b87e60ea94757ba24e7c89cc9270b":"1dcf1758ff58ca42fc868a74d57401bf",
                        "255efd90ffe0d0a2b7d773b8f3c2af99":"87cdd0a4a2ed9806d3f415ee652e418d",
                        "409f4aefa053f26595e1a85cdc827f33":"f022e2060ffe652b4679ee5c35d55013",
                        "ed382fca85ff638d1e57df0389ed8b1a":"c6828b52ffddd0eb81c7ac36f95b68d6",
                        "e5eea788cfde23d3a7681a1eb58d6256":"ecf8fd018390596da05d7c97a61449f4",
                        "e843f761013d8dddcca8c9cc18f30fef":"c7d7db1a1b841fab0867278857a62ed8",
                        "e33fecfc77ab9fa4fe89792422f0f135":"f53ee31477ebd1f32bb89145ee95335f",
                        "2280a5fac6f4979704943024f690fe30":"14a57276ad900a912166c08e01282490",
                        "cf368ce51b634e9ca8ce67d2b47b68ea":"eba1e228ec25ff97447d650589ec8b86",
                        "792907e3c2402946679c38c32bf32c11":"00556b8e0c522386ff426301729ec8f1",
                        "57dc9cf332f34d1d58ddd1bd038840f3":"5a6f9422c2904965abddad64fcab9555",
                        "7bfbfa519a2366b19f9e4de8674fc9c8":"03f35ee47c533e6e4039cc56a71099ce",
                        "0f831ef273ebefd94edeaa99038cf22e":"1fddd4cf639230a3ce241eb5d918102d",
                        "7abc137399ca099c2a2530781040cf8c":"5aebf07270841a22149c3faa36e8155d",
                        "c129244525d76817e0fde5441495fc51":"866e703563875ca7d8ce2d35773dca4b",
                        "c3bbd19e4a8cece2c93effeec655e77a":"a8f1f602dd59a68f7728a6240ae6cfac",
                        "e1f20fc31a851a32e3238972095339cc":"3907ba9a1c02bd03b94a441b7ee44b12",
                        "fd5629d9469c4073bee45f0097ea719b":"d0c1b577b89639366d8b345d99801942",
                        "d4431b09af191f4ca191b1d3d2ed4f2f":"b6548f2010fd6eb8c985448750eb9686",
                        "5ea3a4929afb696c07ae7a8be3d18399":"85f6ade8f4af77060b62045700582f75",
                        "a342b9b1e6e7361959a0de511a0b4503":"33d7665e78176bc4894baa31b2362c3f",
                        "673bb47db9f1ede2aa174cfe3a8fc115":"2011b3f138e418de5b0f171f28ffc52a",
                        "6c4a450a6ecf9ab73b5458c66df01e35":"a993a42fdaa4035556d1759c3637ab11",
                        "d00e5ed436332c8863f49a8f0883d7d8":"f0aa2ae16287f148c613921c1e696246",
                        "15c423baa7da60ef95616febbbb6d327":"08f3733876565d843b110ad28e4b9c93",
                        "765df43db63bd07acbc443c57f30c00a":"7f6e12a895ebdcb045b103ab6f3f603c",
                        "ca537e56d5bc82f57b73358702f39e44":"fc77fb632d9714e4b23f0e5e3f04494a",
                        "45c696c85ceb9e0edec62c05c00439fd":"a4035ba2d613351fafee1ae31ae77313",
                        "90f63d69803e09b447cddc98ed9a117c":"2f254f6f7eb97628c11a1d78f51639bc",
                        "7f3f2d5a4e81daf54e04ebdc9b5f1947":"3def88560b0ef44beb999035d18ee618",
                        "341815d5b878601565f27c1eb7847bfa":"e9d12b6dd6c58950f0116f216f909604",
                        "497f1496ccf0dd09b04e65dc98195c2a":"3dd65e4ef1a5abb983d4335bcb8d28cd",
                        "382acd5f94154a1a25708c3c64e52986":"a56a1a7398ee684a823baec4a72c95ac",
                        "e3236e278904afbedf1bfe19c3597574":"f511ccd45ad48e02c8df301e93891397",
                        "a3f3d2abfab58d273a38c9ead8d7268f":"a06cbb9acac8fdce02ba9f0a0fabf1dc",
                        "fa2fc165fee786d3fefb0b11f0e15312":"c2f12613e505fe7e459df4e97ce81f40",
                        "6660ce9d0b7453981a97f0dee6f6e3cb":"28e8652d63b2b2d41689209733f8afa4",
                        "da82c6c5aa930c5b8f96a0323471056f":"295db2dc4f43c26ac5b3a24492601390",
                        "b06a71d8a4064c2d3ec287d8f502b374":"9cda383f56846fb834172edc4324da71",
                        "7fc7c8e18220e870eed6268bb62b098e":"37c99184a503b2cd7c1023a23f5f5d52",
                        "fd2a4c7c70ad5043b7fc32664ae800cc":"a5d574c7d5fd17fc10cc6fc70545f6de",
                        "bc48c401fb78a526c1d5d0a21c0b4054":"d71d11a511ed0ad34919701b5cc562eb",
                        "58eb3045b7b1f01cf86bfe50880fcac2":"bc93157c143ed0988271a78abb139990",
                        "8be5e9d8f70ddaf4f27fc8c4ae82e4a5":"3c3c9575b9f9de7a7d6d8e5248dccc40",
                        "7b969b1665a1d7157b2c76a4a9ad66bd":"557daf115e62cdc16f59c220a5a0fce1",
                        "e1f20fc31a851a32e3238972095339cc":"3907ba9a1c02bd03b94a441b7ee44b12",
                        "e9de9024219cc9027ad3de033f02c22b":"a6eb4efe5544720972497f49f154d7ec",
                        "c03fb309e6d07cd9f279c6b20521287d":"21ad7b81098d869f4873c0881f52db82",
                        "fb4616a5cb7ecd3c7644edf9a90d99ab":"a5a6401a12bdb68a534eb2abe5435feb",
                        "f4a06ef85f9fd1a9a66a18b01c9b3d08":"129b4b9749b52efbdb92bce930be154b",
                        "13aecb0cd5c11df5416e46cd4519388a":"f01a56261a5a54b25bef2e62a8ac9a0a",
                        "7f309114ed247ffcb6cc6cec43cb2276":"bfa879d30a64d9ba5d3fea7f4f262e07",
                        "7779f95cff8c29ce7e4ccf7b67b83d9d":"8d4eaa19e5c58d910ed042c65a39bff3",
                        "19b25445f3d7d3a07b444b40d86c061c":"019ff054a7cd2875ab1a08124c121e79",
                        "57dc9cf332f34d1d58ddd1bd038840f3":"5a6f9422c2904965abddad64fcab9555",
                        "854150871053380d4099f47dff8518b8":"9c2f484bd673c74bed84dd5343b7783b",
                        "0cdf4ed06c33046cdf6cf1c5ffa0e8d0":"7753ce175e78b0908d37f763e8a217f0",
                        "08244a2d9fd694bdb4f145987eb1ecf6":"5cb062d59444f92ae38ee48766f7fce6"}
                }
)


'''
包月会员短信指令
'''
add_global_item('chinaMobile_monthly_smsContent', {
    # "350000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"福建"
    "570000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"海南"
    "430000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"湖北"
    "200000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"上海"
    #"610000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"四川"
    "300000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"天津"
    "650000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["00000", "10660145"], "auto_reply" : "是"}, #"云南"
    # "310000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"浙江"
    # "810000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"青海"
    "10000": {"subscribe" : ["XW", "10660145"], "unsubscribe" : ["000000", "10660145"], "auto_reply" : "是"},#"内蒙"
    "450000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["000000", "10660145"], "auto_reply" : "是"},#"河南"
    "250000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["000000", "10660672"], "auto_reply" : "是"},#"山东"
    "30000": {"subscribe" : ["XW", "10660145"], "unsubscribe" : ["000000", "10660145"], "auto_reply" : "是"},#"山西"
    "710000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["000000", "10660145"], "auto_reply" : "是"},#"陕西"
    # "400000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"重庆"
    "230000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["00000", "10660145"], "auto_reply" : "是"}, #"安徽"
    # "100000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"北京"
    # "730000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"甘肃"
    # "510000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"广东"
    # "530000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"广西"
    "550000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["00000", "10660145"], "auto_reply" : "是"}, #"贵州"
    # "50000" :{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"河北"
    "150000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["00000", "10660145"], "auto_reply" : "是"}, #"黑龙江"
    # "410000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"湖南"
    # "130000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"吉林"
    "210000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["00000", "10660145"], "auto_reply" : "是"}, #"江苏"
    # "330000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"江西"
    # "110000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"辽宁"
    # "750000":{"subscribe" : ["10", "10660672"], "unsubscribe" : ["00000", "10660672"], "auto_reply" : "是"}, #"宁夏"
    "850000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["00000", "10660145"], "auto_reply" : "是"}, #"西藏"
    "830000":{"subscribe" : ["XW", "10660145"], "unsubscribe" : ["00000", "10660145"], "auto_reply" : "是"}  #"新疆"
})

add_global_item('chinaUnion_monthly_smsContent', {
    "350000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"福建"
    "570000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"海南"
    "430000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"湖北"
    "200000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"上海"
    "610000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"四川"
    "300000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"天津"
    "310000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"浙江"
    "810000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"青海"
    "10000": {"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"内蒙"
    "450000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"河南"
    "30000": {"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"山西"
    "230000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"安徽"
    "100000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"北京"
    "530000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"广西"
    "50000" :{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"河北"
    "210000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"江苏"
    "330000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"江西"
    "110000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"辽宁"
    "750000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"宁夏"
    "850000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"西藏"
    "830000":{"subscribe" : ["dg10#as*1125", "10669202"], "unsubscribe" : ["QX10", "10669202"], "auto_reply" : "y"}, #"新疆"
    # "400000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"重庆"
    # "730000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"甘肃"
    # "510000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"广东"
    # "550000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"贵州"
    # "150000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"黑龙江"
    # "410000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"湖南"
    # "130000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"吉林"
    # "650000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"云南"
    # "250000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"山东"
    # "710000":{"subscribe" : ["", ""], "unsubscribe" : ["", ""], "auto_reply" : ""}, #"陕西"
})

add_global_item('chinaTelecom_monthly_smsContent', {
    "subscribe"   : ['m', '10661016'],
    "unsubscribe" : ['tdm', '10661016'],
    "auto_reply"  : "1"
})

add_global_item('monthly_vip_sms_auto_reply_listen_content', {
    "chinaMobile":["回复\'是\'确认订购", "回复‘是’确认订购", "回复\"是\"确认订购", "回复“是”确认订购", "回复“是”或者“1”确认订购", "回复“1” 或“是”确认订购", "回复任意短信确认", "确认订购", "确认定制"],
    "chinaUnion":["回复Y生效", "回复y生效"],
    "chinaTelecom":["回复任意内容", "任意内容"],
})

add_global_item('monthly_vip_subscribe_error_info', {
    '0' : '对不起，支付遇到问题，请检查...',
    '1' : '请检查是否插卡或者开启飞行模式',
    '2' : '您所在的地区不支持，已经提交客服，敬请期待',
})

add_global_item('monthly_vip_params', {
    'orderIdPhonenum' : '10690387000215',
    'key' : 'HFXLNQGFH621NWK',
    'alternativeProdId':'TY9999D0010006',
})


'''
米大师appkey
'''
add_global_item('midashi_sdk_config', [
    {
        "appid":"1450005084",
        "appkey":"Ffb0vdSFJ2qcgwfHuYlUHpwagNXg0wSI"
    },
    {
        "appid":"1450005301",
        "appkey":"9X3z6hkvqhtDYLtwIAiJPyR7H2N5xJBT"
    },
    {
        "appid":"1450005302",
        "appkey":"Oo4rSW4qJdieWwqURU0Mq7rwluAlo13U"
    },
    {
        "appid":"1450005303",
        "appkey":"IjQ6ujs79repxf4YodJAZXILcJxsdcFC"
    },
    {
        "appid":"1450005468",
        "appkey":"tcRNUKV0iQyS4Mv3LqXo6yvvq1iwCJAN"
    },
    {
        "appid":"1450005469",
        "appkey":"QB8CJjmIQOIKyfIrdsVahTdMzz0iwSsD"
    },
	{
        "appid":"1450006362",
        #"appkey":"zQLKCJExMhhyo8VO8fEthDzh8ZOZl1u2"
        "appkey":"1iJMsjDzPyk3lb1jYSnS4eDacxdynH0d",
    },
    {
        "appid":"1450006296",
        "appkey":"r9Rc4ZsCRPXp3L667M4mxnpLRoo3bxgs"
    },
    {
        "appid":"1101977575",
        "appkey":"a6njxFG8v7Srxr8Q",
    }
])

'''
    IIApple（爱苹果)（iOS）
'''
add_global_item('iiapple_paykeys', {
    'gameKey': '9086fffa143ec3761622d7ce39887e2e',
    'secretKey': '75b04253979851fd7d828ce70d9644fb',
    'tokenUrl': 'http://ucenter.iiapple.com/foreign/oauth/verification.php',
})

add_global_item('iiapple_paykeys_new', {
    '0-hall6.iiapple.huanle':{
        'gameKey': '9086fffa143ec3761622d7ce39887e2e',
        'secretKey': '75b04253979851fd7d828ce70d9644fb',
        'tokenUrl': 'http://ucenter.iiapple.com/foreign/oauth/verification.php',
        },
    '0-hall6.iiapple.gougou':{
        'gameKey': '97ae5c8a3c8b4becd56db6c8eaf48ec2',
        'secretKey': '5e8ec6eab613f4bce8f696f0590e9073',
        'tokenUrl': 'http://ucenter.iiapple.com/foreign/oauth/verification.php',
        },
})


add_global_item('ios-products-v2', {
    "9":[
        {
        'products' : [
            {'tyid':'DI60',  'price': 6,    'name':'60钻石',   'iosid' : 'com.tencent.paodekuai_60'},
            {'tyid':'DI300',  'price': 30,  'name':'300钻石',  'iosid' : 'com.tencent.paodekuai_300'},
            {'tyid':'DI980',  'price': 98,  'name':'980钻石',  'iosid' : 'com.tencent.paodekuai_980'},
            {'tyid':'DI1980', 'price': 198, 'name':'1980钻石', 'iosid' : 'com.tencent.paodekuai_1980'},
            {'tyid':'DI3280', 'price': 328, 'name':'3280钻石', 'iosid' : 'com.tencent.paodekuai_3280'},
            {'tyid':'DI6480', 'price': 648, 'name':'6480钻石', 'iosid' : 'com.tencent.paodekuai_6480'},
        ],
        'clientIds' : '^IOS.*$'
        },
    ],
    "9999": [
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'1万金币', 'price':10,
             'iosid': 'cn.com.doudizhu.happy.hall.a', },
            {'tyid': 'TY9999D0003001', 'name':'3万金币', 'price':30,
             'iosid': 'cn.com.doudizhu.happy.hall.b', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币', 'price':60,
             'iosid': 'cn.com.doudizhu.happy.1', },
            {'tyid': 'TY9999D0030003', 'name':'30万金币', 'price':300,
             'iosid': 'cn.com.doudizhu.happy.4', },
            {'tyid': 'TY9999D0030001', 'name':'33万金币', 'price':300,
             'iosid': 'cn.com.doudizhu.happy.4', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.doudizhu.happy.hall.1', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.doudizhu.happy.hall.2', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'cn.com.doudizhu.happy.hall.c', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.doudizhu.happy.hall.3', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.doudizhu.happy.hall.4', },
            {'tyid': 'TY0006D0030004', 'name':'7天会员卡（立得28万金币，每日登录可得3万金币（7天））',
             'price':300, 'iosid': 'cn.com.doudizhu.happy.hall.5', },
            {'tyid': 'TY0006D0098002', 'name':'30天会员卡（立得100万金币，每日登录可得3万金币（30天））',
             'price':980, 'iosid': 'cn.com.doudizhu.happy.hall.6', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.doudizhu.happy.hall.7', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.doudizhu.happy.hall.8', },
            {'tyid': 'TY9999D0006004', 'name':'超值礼包',
             'price':60, 'iosid': 'cn.com.doudizhu.happy.9', },
            {'tyid': 'TY9999D0006005', 'name':'6元转运礼包',
             'price':60, 'iosid': 'cn.com.doudizhu.happy.10', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'1万金币', 'price':10,
             'iosid': 'cn.com.doudizhu.zhafantian.c1', },
            {'tyid': 'TY9999D0003001', 'name':'3万金币', 'price':30,
             'iosid': 'cn.com.doudizhu.zhafantian.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币', 'price':60,
             'iosid': 'cn.com.doudizhu.zhafantian.c6', },
            {'tyid': 'TY9999D0030003', 'name':'36万金币', 'price':300,
             'iosid': 'cn.com.doudizhu.zhafantian.c30', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币', 'price':300,
             'iosid': 'cn.com.doudizhu.zhafantian.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.doudizhu.zhafantian.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.doudizhu.zhafantian.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.doudizhu.zhafantian.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.doudizhu.zhafantian.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.doudizhu.zhafantian.d60', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.doudizhu.zhafantian.d300', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'cn.com.doudizhu.zhafantian.d1280', },
            {'tyid': 'TY9999D0006004', 'name':'超值礼包',
             'price':60, 'iosid': 'cn.com.doudizhu.zhafantian.chaozhi', },
            {'tyid': 'TY9999D0006005', 'name':'6元转运礼包',
             'price':60, 'iosid': 'cn.com.doudizhu.zhafantian.zhuanyun', },
            ],
         'clientIds' : '^IOS_3.*zhafantian$',
         },
        {'products' : [
            {'tyid': 'TY9999D0006003', 'iosid': 'cn.com.doudizhu.wushuang.1',    'price': 60,   'name': '6万金币' },
            {'tyid': 'TY9999D0030003', 'iosid': 'cn.com.doudizhu.wushuang.4',    'price': 300,  'name': '30万金币' },
            {'tyid': 'TY9999D0098001', 'iosid': 'cn.com.doudizhu.wushuang.c98',  'price': 980,  'name': '98万金币' },
            {'tyid': 'TY9999D0198001', 'iosid': 'cn.com.doudizhu.wushuang.c198', 'price': 1980, 'name': '198万金币' },
            {'tyid': 'TY9999D0328001', 'iosid': 'cn.com.doudizhu.wushuang.c328', 'price': 3280, 'name': '328万金币' },
            {'tyid': 'TY9999D0648001', 'iosid': 'cn.com.doudizhu.wushuang.c648', 'price': 6480, 'name': '648万金币' },
            {'tyid': 'TY9999D0001002', 'iosid': 'cn.com.doudizhu.wushuang.c1',   'price': 10,   'name': '1万金币' },
            {'tyid': 'TY9999D0003001', 'iosid': 'cn.com.doudizhu.wushuang.c3',   'price': 30,   'name': '3万金币' },
            {'tyid': 'TY9999R0006001', 'iosid': 'cn.com.doudizhu.wushuang.d6',   'price': 60,   'name': '60钻石' },
            {'tyid': 'TY9999R0030001', 'iosid': 'cn.com.doudizhu.wushuang.d30',  'price': 300,  'name': '300钻石' },
            {'tyid': 'TY9999D0030001', 'iosid': 'cn.com.doudizhu.wushuang.4',  'price': 300,  'name': '300钻石' },
            {'tyid': 'TY9999R0128001', 'iosid': 'cn.com.doudizhu.wushuang.d128', 'price': 1280, 'name': '1280钻石' },
            ],
         'clientIds' : '^IOS_3.7.*hall6.appStore.cherry$',
         },
        {'products' : [
            {'tyid': 'TY9999D0002050', 'iosid': 'com.wemomo.game.ddz.68', 'price': 10,   'name': '地主小礼包' },
            {'tyid': 'TY9999D0006050', 'iosid': 'com.wemomo.game.ddz.48', 'price': 30,   'name': '地主体验礼包' },
            {'tyid': 'TY9999D0012050', 'iosid': 'com.wemomo.game.ddz.21', 'price': 60,   'name': '地主特惠礼包' },
            {'tyid': 'TY9999D0030050', 'iosid': 'com.wemomo.game.ddz.22', 'price': 300,  'name': '地主豪华礼包' },
            {'tyid': 'TY9999D0068050', 'iosid': 'com.wemomo.game.ddz.23', 'price': 980,  'name': '顺发大礼包' },
            {'tyid': 'TY9999D0128050', 'iosid': 'com.wemomo.game.ddz.24', 'price': 1980, 'name': '聚财大礼包' },
            {'tyid': 'TY9999D0328050', 'iosid': 'com.wemomo.game.ddz.25', 'price': 3280, 'name': '土豪大礼包' },
            {'tyid': 'TY9999D0006051', 'iosid': 'com.wemomo.game.ddz.36', 'price': 6480, 'name': '月光宝盒礼包' },
            {'tyid': 'TY9999D0006052', 'iosid': 'com.wemomo.game.ddz.26', 'price': 60,   'name': '语音小喇叭100个' },
            {'tyid': 'TY9999D0006053', 'iosid': 'com.wemomo.game.ddz.37', 'price': 300,  'name': '参赛券x30' },
            {'tyid': 'TY9999D0012052', 'iosid': 'com.wemomo.game.ddz.27', 'price': 60,   'name': '7天记牌器' },
            {'tyid': 'TY9999D0006054', 'iosid': 'com.wemomo.game.ddz.38', 'price': 60,   'name': '转运礼包' },
            {'tyid': 'TY9999D0030051', 'iosid': 'com.wemomo.game.ddz.56', 'price': 10,   'name': '转运大礼包' },
            {'tyid': 'TY9999D0030052', 'iosid': 'com.wemomo.game.ddz.42', 'price': 30,   'name': 'VIP普通礼包' },
            {'tyid': 'TY9999D0068051', 'iosid': 'com.wemomo.game.ddz.43', 'price': 60,   'name': 'VIP豪华礼包' },

            {'tyid': 'TY9999D0006055', 'iosid': 'com.wemomo.game.ddz.28', 'price': 60,   'name': '50000金币' },
            {'tyid': 'TY9999D0012051', 'iosid': 'com.wemomo.game.ddz.29', 'price': 120,  'name': '100000金币' },
            {'tyid': 'TY9999D0018051', 'iosid': 'com.wemomo.game.ddz.30', 'price': 180,  'name': '170000金币' },
            {'tyid': 'TY9999D0030053', 'iosid': 'com.wemomo.game.ddz.31', 'price': 300,  'name': '300000金币' },
            {'tyid': 'TY9999D0068052', 'iosid': 'com.wemomo.game.ddz.32', 'price': 680,  'name': '700000金币' },
            {'tyid': 'TY9999D0128051', 'iosid': 'com.wemomo.game.ddz.33', 'price': 1280, 'name': '1500000金币' },
            {'tyid': 'TY9999D0006056', 'iosid': 'com.wemomo.game.ddz.35', 'price': 60,   'name': '月光之钥x3' },
            #{'tyid': 'TY9999D0006057', 'iosid': 'com.wemomo.game.ddz.34', 'price': 60,   'name': '语音小喇叭100个' },
            {'tyid': 'TY9999D0006058', 'iosid': 'com.wemomo.game.ddz.40', 'price': 60,   'name': '转运礼包' },
            {'tyid': 'TY9999D0030054', 'iosid': 'com.wemomo.game.ddz.41', 'price': 300,  'name': '转运大礼包' },
            {'tyid': 'TY9999D0012053', 'iosid': 'com.wemomo.game.ddz.45', 'price': 120,  'name': '记牌器7天' },
            {'tyid': 'TY9999D0030055', 'iosid': 'com.wemomo.game.ddz.46', 'price': 300,  'name': '普通VIP礼包' },
            {'tyid': 'TY9999D0068053', 'iosid': 'com.wemomo.game.ddz.47', 'price': 680,  'name': '豪华VIP礼包' },
            ],
         'clientIds' : '^IOS_3.*momo$',
         },
        {'products' : [
            {'tyid':'DI60', 'price': 6, 'name':'钻石x60', 'iosid' : 'com.tuyoo.sdk.product1'},
            {'tyid':'DI120', 'price': 12, 'name':'钻石x120', 'iosid' : 'com.tuyoo.sdk.product2'},
            {'tyid':'DI180', 'price': 18, 'name':'钻石x180', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI300', 'price': 30 , 'name':'钻石x300', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI680', 'price': 68, 'name':'钻石x680', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI1280', 'price': 128, 'name':'钻石x1280', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI3280', 'price': 328, 'name':'钻石x3280', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI6480', 'price': 648, 'name':'钻石x6480', 'iosid' : 'com.tuyoo.sdk.product3'},
            ],
         'clientIds' : 'IOS_1.03_tuyou'
        },
        {'products' : [
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.majiang.mac.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.majiang.mac.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.majiang.mac.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.majiang.mac.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.majiang.mac.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.majiang.mac.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石',
             'price':60, 'iosid': 'com.tuyoo.majiang.mac.d_6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石',
             'price':300, 'iosid': 'com.tuyoo.majiang.mac.d_30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'com.tuyoo.majiang.mac.d_128', },
            ],
         'clientIds' : '^MAC_.*hall7.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'cn.com.majiang.hall.1', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'cn.com.majiang.hall.2', },
            {'tyid': 'TY9999D0030003', 'name':'36万金币', 'price':300,
             'iosid': 'cn.com.majiang.hall.2', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.majiang.hall.3', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.majiang.hall.4', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.majiang.hall.5', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.majiang.hall.6', },
            {'tyid': 'TY0006D0030004', 'name':'7天会员卡（立得28万金币，每日再赠3万，雀神分翻倍）',
             'price':300, 'iosid': 'cn.com.majiang.hall.7', },
            {'tyid': 'TY0006D0098002', 'name':'30天会员卡（立得100万金币，每日再赠3万，雀神分翻倍）',
             'price':980, 'iosid': 'cn.com.majiang.hall.8', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.majiang.hall.9', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.majiang.hall.10', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'cn.com.majiang.hall.d1280', },
            {'tyid': 'TY9999D0006004', 'name':'6元超值礼包',
             'price':60, 'iosid': 'cn.com.majiang.hall.11', },
            {'tyid': 'TY9999D0006005', 'name':'6元转运礼包',
             'price':60, 'iosid': 'cn.com.majiang.hall.12', },
            ],
         'clientIds' : '^IOS_.*hall7.*$'
        },

        {'products' : [
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.cherrygame.majiang.product.11', },
            {'tyid': 'TY9999D0030003', 'name':'36万金币',
             'price':300, 'iosid': 'com.cherrygame.majiang.product.3', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.cherrygame.majiang.product.3', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.cherrygame.majiang.product.a', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.cherrygame.majiang.product.6', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.cherrygame.majiang.product.b', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.cherrygame.majiang.product.c', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.cherrygame.majiang.product.d', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.cherrygame.majiang.product.e', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'com.cherrygame.majiang.product.f', },
            {'tyid': 'TY9999D0006004', 'name':'6元超值礼包',
             'price':60, 'iosid': 'com.cherrygame.majiang.product.g', },
            {'tyid': 'TY9999D0006005', 'name':'6元转运礼包',
             'price':60, 'iosid': 'com.cherrygame.majiang.product.h', },
            ],
         'clientIds' : '^IOS_3.7.*hall7.appStore.cherry$'
        },

        {'products' : [
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.majiang.huanle.c6', },
            {'tyid': 'TY9999D0006001', 'name':'6万金币',
             'price':60, 'iosid': 'com.majiang.huanle.c6', },
            {'tyid': 'TY9999R0006001', 'name':'60钻',
             'price':60, 'iosid': 'com.majiang.huanle.d6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.majiang.huanle.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.majiang.huanle.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.majiang.huanle.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.majiang.huanle.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.majiang.huanle.c648', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石',
             'price':300, 'iosid': 'com.majiang.huanle.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'com.majiang.huanle.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall7.appStore.huanle$'
        },

        {'products' : [
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.majiang.zhenren.c6', },
            {'tyid': 'TY9999D0006001', 'name':'6万金币',
             'price':60, 'iosid': 'com.majiang.zhenren.c6', },
            {'tyid': 'TY9999R0006001', 'name':'60钻',
             'price':60, 'iosid': 'com.majiang.zhenren.d6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.majiang.zhenren.c30', },
            {'tyid': 'TY9999D0030003', 'name':'36万金币',
             'price':300, 'iosid': 'com.majiang.zhenren.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.majiang.zhenren.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.majiang.zhenren.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.majiang.zhenren.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.majiang.zhenren.c648', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石',
             'price':300, 'iosid': 'com.majiang.zhenren.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'com.majiang.zhenren.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall7.appStore.zhenren$'
        },

        {'products' : [
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.ddz.mac.c6', },
            {'tyid': 'TY9999D0006001', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.ddz.mac.c6', },
            {'tyid': 'TY9999R0006001', 'name':'60钻',
             'price':60, 'iosid': 'com.tuyoo.ddz.mac.d6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.ddz.mac.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.ddz.mac.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.ddz.mac.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.ddz.mac.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.ddz.mac.c648', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石',
             'price':300, 'iosid': 'com.tuyoo.ddz.mac.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'com.tuyoo.ddz.mac.d128', },
            ],
         'clientIds' : '^MAC_.*hall6.*$'

        },
        {'products' : [
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.texas.mac.c6', },
            {'tyid': 'TY9999R0006001', 'name':'60钻',
             'price':60, 'iosid': 'com.tuyoo.texas.mac.d6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.texas.mac.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.texas.mac.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.texas.mac.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.texas.mac.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.texas.mac.c648', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石',
             'price':300, 'iosid': 'com.tuyoo.texas.mac.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'com.tuyoo.texas.mac.d128', },
            ],
         'clientIds' : '^MAC_.*hall8.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.tuyoo.chinesechess.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.tuyoo.chinesechess.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.chinesechess.1', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.chinesechess.2', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.chinesechess.3', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.chinesechess.4', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.chinesechess.5', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.chinesechess.6', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.tuyoo.chinesechess.7', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.tuyoo.chinesechess.8', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.tuyoo.chinesechess.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall3.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'cn.com.gomoku.tuyoo.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'cn.com.gomoku.tuyoo.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'cn.com.gomoku.tuyoo.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'cn.com.gomoku.tuyoo.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.gomoku.tuyoo.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.gomoku.tuyoo.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.gomoku.tuyoo.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.gomoku.tuyoo.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.gomoku.tuyoo.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.gomoku.tuyoo.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'cn.com.gomoku.tuyoo.d128', },
            ],
         'clientIds' : '^IOS_3.*hall20.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.tuyoo.junqi.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.tuyoo.junqi.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.junqi.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.junqi.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.junqi.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.junqi.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.junqi.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.junqi.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.tuyoo.junqi.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.tuyoo.junqi.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.tuyoo.junqi.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall25.appStore.tuyoo$'
        },
        {'products' : [
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.chess.mac.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.chess.mac.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.chess.mac.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.chess.mac.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.chess.mac.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.chess.mac.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石',
             'price':60, 'iosid': 'com.tuyoo.chess.mac.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石',
             'price':300, 'iosid': 'com.tuyoo.chess.mac.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'com.tuyoo.chess.mac.d128', },
            ],
         'clientIds' : '^MAC_.*hall3.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.tuyoo.baohuang.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.tuyoo.baohuang.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.baohuang.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.baohuang.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.baohuang.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.baohuang.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.baohuang.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.baohuang.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.tuyoo.baohuang.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.tuyoo.baohuang.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.tuyoo.baohuang.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall17.*baohuang$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'cn.com.3card.meinv.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'cn.com.3card.meinv.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'cn.com.3card.meinv.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'cn.com.3card.meinv.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.3card.meinv.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.3card.meinv.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.3card.meinv.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.3card.meinv.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.3card.meinv.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.3card.meinv.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'cn.com.3card.meinv.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall1.*t3card$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.tuyoo.paohuzi.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.tuyoo.paohuzi.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.paohuzi.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.paohuzi.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.paohuzi.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.paohuzi.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.paohuzi.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.paohuzi.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.tuyoo.paohuzi.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.tuyoo.paohuzi.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.tuyoo.paohuzi.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall21.*paohuzi$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.eapoker.ddz.single.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.eapoker.ddz.single.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.eapoker.ddz.single.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.eapoker.ddz.single.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.eapoker.ddz.single.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.eapoker.ddz.single.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.eapoker.ddz.single.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.eapoker.ddz.single.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.eapoker.ddz.single.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.eapoker.ddz.single.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.eapoker.ddz.single.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall6.appStore.single$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.eapoker.ddz.single.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.eapoker.ddz.single.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.eapoker.ddz.single.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.eapoker.ddz.single.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.eapoker.ddz.single.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.eapoker.ddz.single.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.eapoker.ddz.single.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.eapoker.ddz.single.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.eapoker.ddz.single.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.eapoker.ddz.single.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.eapoker.ddz.single.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall6.appStore.qipaiheji$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.ddz.huanle.zhenren.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.ddz.huanle.zhenren.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.ddz.huanle.zhenren.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.ddz.huanle.zhenren.c30', },
            {'tyid': 'TY9999D0030003', 'name':'36万金币',
             'price':300, 'iosid': 'com.ddz.huanle.zhenren.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.ddz.huanle.zhenren.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.ddz.huanle.zhenren.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.ddz.huanle.zhenren.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.ddz.huanle.zhenren.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.ddz.huanle.zhenren.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.ddz.huanle.zhenren.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.ddz.huanle.zhenren.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall6.appStore.zhenren$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.ddz.huanle.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.ddz.huanle.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.ddz.huanle.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.ddz.huanle.c30', },
            {'tyid': 'TY9999D0030003', 'name':'36万金币',
             'price':300, 'iosid': 'com.ddz.huanle.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.ddz.huanle.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.ddz.huanle.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.ddz.huanle.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.ddz.huanle.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.ddz.huanle.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.ddz.huanle.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.ddz.huanle.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall6.appStore.happyplay$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.ddz.tiantian.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.ddz.tiantian.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.ddz.tiantian.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.ddz.tiantian.c30', },
            {'tyid': 'TY9999D0030003', 'name':'36万金币',
             'price':300, 'iosid': 'com.ddz.tiantian.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.ddz.tiantian.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.ddz.tiantian.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.ddz.tiantian.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.ddz.tiantian.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.ddz.tiantian.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.ddz.tiantian.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.ddz.tiantian.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall6.appStore.tiantian$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'10000金币',
             'price':10, 'iosid': 'com.ddz.tiantian2.c1', },
            {'tyid': 'TY9999D0003001', 'name':'30000金币',
             'price':30, 'iosid': 'com.ddz.tiantian2.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币',
             'price':60, 'iosid': 'com.ddz.tiantian2.c6', },
            {'tyid': 'TY9999D0030001', 'name':'36万金币',
             'price':300, 'iosid': 'com.ddz.tiantian2.c30', },
            {'tyid': 'TY9999D0030003', 'name':'36万金币',
             'price':300, 'iosid': 'com.ddz.tiantian2.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'com.ddz.tiantian2.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'com.ddz.tiantian2.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'com.ddz.tiantian2.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.ddz.tiantian2.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.ddz.tiantian2.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.ddz.tiantian2.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'com.ddz.tiantian2.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall6.appStore.tiantian2$'
        },
        {'products' : [
            #付费德州
            {'tyid': 'TY9999D0006007', 'name': '6万金币',    'price': 6,   'iosid': 'cn.com.dezhou.luxury.c6', },
            {'tyid': 'TY9999D0030007', 'name': '36万金币',   'price': 30,  'iosid': 'cn.com.dezhou.luxury.c30', },
            {'tyid': 'TY9999D0098007', 'name': '140万金币',  'price': 98,  'iosid': 'cn.com.dezhou.luxury.c98', },
            {'tyid': 'TY9999D0198007', 'name': '300万金币',  'price': 198, 'iosid': 'cn.com.dezhou.luxury.c198', },
            {'tyid': 'TY9999D0328007', 'name': '550万金币',  'price': 328, 'iosid': 'cn.com.dezhou.luxury.c328', },
            {'tyid': 'TY9999D0648007', 'name': '1200万金币', 'price': 648, 'iosid': 'cn.com.dezhou.luxury.c648', },
            {'tyid': 'TY9999R0006001', 'name': '60钻石',     'price': 6,   'iosid': 'cn.com.dezhou.luxury.d6', },
            {'tyid': 'TY9999R0030001', 'name': '300钻石',    'price': 30,  'iosid': 'cn.com.dezhou.luxury.d30', },
            {'tyid': 'TY9999R0128001', 'name': '1280钻石',    'price': 128,  'iosid': 'cn.com.dezhou.luxury.d128', },
            ],
         'clientIds' : '^IOS_3.7.*hall8.appStore.luxury$'
        },
        {'products' : [
            #IOS_3.x
            {'tyid': 'TY9999D0006007', 'name': '6万金币',    'price': 6,   'iosid': 'cn.com.dezhou.crazy.product.1', },
            {'tyid': 'TY9999D0030007', 'name': '36万金币',   'price': 30,  'iosid': 'cn.com.dezhou.crazy.product.2', },
            {'tyid': 'TY9999D0098007', 'name': '140万金币',  'price': 98,  'iosid': 'cn.com.dezhou.crazy.product.3', },
            {'tyid': 'TY9999D0198007', 'name': '300万金币',  'price': 198, 'iosid': 'cn.com.dezhou.crazy.product.4', },
            {'tyid': 'TY9999D0328007', 'name': '550万金币',  'price': 328, 'iosid': 'cn.com.dezhou.crazy.product.5', },
            {'tyid': 'TY9999D0648007', 'name': '1200万金币', 'price': 648, 'iosid': 'cn.com.dezhou.crazy.product.6', },
            {'tyid': 'TY9999D0006005', 'name': '6元转运礼包','price': 6,   'iosid': 'TEXAS_IOS_COIN_LUCKY_R6', },
            {'tyid': 'TY9999R0006001', 'name': '60钻石',     'price': 6,   'iosid': 'cn.com.dezhou.crazy.diamonds.60', },
            {'tyid': 'TY9999R0030001', 'name': '300钻石',    'price': 30,  'iosid': 'cn.com.dezhou.crazy.diamonds.300', },
            {'tyid': 'TY9999R0128001', 'name': '1280钻石',    'price': 128,  'iosid': 'cn.com.dezhou.crazy.diamonds.1280', },
            {'tyid': 'TY9999D0006004', 'name': '超值礼包',   'price': 6,   'iosid': 'cn.com.dezhou.crazy.raffle.6', },
            ],
         'clientIds' : '^IOS_3.7.*hall8.appStore.fk$'
        },
    ],
    "6":[
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'1万金币', 'price':10,
             'iosid': 'cn.com.doudizhu.happy.hall.a', },
            {'tyid': 'TY9999D0003001', 'name':'3万金币', 'price':30,
             'iosid': 'cn.com.doudizhu.happy.hall.b', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币', 'price':60,
             'iosid': 'cn.com.doudizhu.happy.1', },
            {'tyid': 'TY9999D0030003', 'name':'30万金币', 'price':300,
             'iosid': 'cn.com.doudizhu.happy.4', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.doudizhu.happy.hall.1', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.doudizhu.happy.hall.2', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'cn.com.doudizhu.happy.hall.c', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.doudizhu.happy.hall.3', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.doudizhu.happy.hall.4', },
            {'tyid': 'TY0006D0030004', 'name':'7天会员卡（立得28万金币，每日登录可得3万金币（7天））',
             'price':300, 'iosid': 'cn.com.doudizhu.happy.hall.5', },
            {'tyid': 'TY0006D0098002', 'name':'30天会员卡（立得100万金币，每日登录可得3万金币（30天））',
             'price':980, 'iosid': 'cn.com.doudizhu.happy.hall.6', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.doudizhu.happy.hall.7', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.doudizhu.happy.hall.8', },
            {'tyid': 'TY9999D0006004', 'name':'超值礼包',
             'price':60, 'iosid': 'cn.com.doudizhu.happy.9', },
            {'tyid': 'TY9999D0006005', 'name':'6元转运礼包',
             'price':60, 'iosid': 'cn.com.doudizhu.happy.10', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0001002', 'name':'1万金币', 'price':10,
             'iosid': 'cn.com.doudizhu.zhafantian.c1', },
            {'tyid': 'TY9999D0003001', 'name':'3万金币', 'price':30,
             'iosid': 'cn.com.doudizhu.zhafantian.c3', },
            {'tyid': 'TY9999D0006003', 'name':'6万金币', 'price':60,
             'iosid': 'cn.com.doudizhu.zhafantian.c6', },
            {'tyid': 'TY9999D0030003', 'name':'30万金币', 'price':300,
             'iosid': 'cn.com.doudizhu.zhafantian.c30', },
            {'tyid': 'TY9999D0098001', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.doudizhu.zhafantian.c98', },
            {'tyid': 'TY9999D0198001', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.doudizhu.zhafantian.c198', },
            {'tyid': 'TY9999D0328001', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.doudizhu.zhafantian.c328', },
            {'tyid': 'TY9999D0648001', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.doudizhu.zhafantian.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.doudizhu.zhafantian.d60', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.doudizhu.zhafantian.d300', },
            {'tyid': 'TY9999D0006004', 'name':'超值礼包',
             'price':60, 'iosid': 'cn.com.doudizhu.zhafantian.chaozhi', },
            {'tyid': 'TY9999D0006005', 'name':'6元转运礼包',
             'price':60, 'iosid': 'cn.com.doudizhu.zhafantian.zhuanyun', },
            ],
         'clientIds' : '^IOS_3.*zhafantian$',
         },
        {'products' : [
            {'tyid': 'TY9999D0006003', 'iosid': 'cn.com.doudizhu.wushuang.1',    'price': 60,   'name': '6万金币' },
            {'tyid': 'TY9999D0030003', 'iosid': 'cn.com.doudizhu.wushuang.4',    'price': 300,  'name': '30万金币' },
            {'tyid': 'TY9999D0098001', 'iosid': 'cn.com.doudizhu.wushuang.c98',  'price': 980,  'name': '98万金币' },
            {'tyid': 'TY9999D0198001', 'iosid': 'cn.com.doudizhu.wushuang.c198', 'price': 1980, 'name': '198万金币' },
            {'tyid': 'TY9999D0328001', 'iosid': 'cn.com.doudizhu.wushuang.c328', 'price': 3280, 'name': '328万金币' },
            {'tyid': 'TY9999D0648001', 'iosid': 'cn.com.doudizhu.wushuang.c648', 'price': 6480, 'name': '648万金币' },
            {'tyid': 'TY9999D0001002', 'iosid': 'cn.com.doudizhu.wushuang.c1',   'price': 10,   'name': '1万金币' },
            {'tyid': 'TY9999D0003001', 'iosid': 'cn.com.doudizhu.wushuang.c3',   'price': 30,   'name': '3万金币' },
            {'tyid': 'TY9999R0006001', 'iosid': 'cn.com.doudizhu.wushuang.d6',   'price': 60,   'name': '60钻石' },
            {'tyid': 'TY9999R0030001', 'iosid': 'cn.com.doudizhu.wushuang.d30',  'price': 300,  'name': '300钻石' },
            {'tyid': 'TY9999R0128001', 'iosid': 'cn.com.doudizhu.wushuang.d128', 'price': 1280, 'name': '1280钻石' },
            ],
         'clientIds' : '^IOS_.*cherry$',
         },
        {'products' : [
            {'tyid': 'TY9999D0002050', 'iosid': 'com.wemomo.game.ddz.68', 'price': 10,   'name': '地主小礼包' },
            {'tyid': 'TY9999D0006050', 'iosid': 'com.wemomo.game.ddz.48', 'price': 30,   'name': '地主体验礼包' },
            {'tyid': 'TY9999D0012050', 'iosid': 'com.wemomo.game.ddz.21', 'price': 60,   'name': '地主特惠礼包' },
            {'tyid': 'TY9999D0030050', 'iosid': 'com.wemomo.game.ddz.22', 'price': 300,  'name': '地主豪华礼包' },
            {'tyid': 'TY9999D0068050', 'iosid': 'com.wemomo.game.ddz.23', 'price': 980,  'name': '顺发大礼包' },
            {'tyid': 'TY9999D0128050', 'iosid': 'com.wemomo.game.ddz.24', 'price': 1980, 'name': '聚财大礼包' },
            {'tyid': 'TY9999D0328050', 'iosid': 'com.wemomo.game.ddz.25', 'price': 3280, 'name': '土豪大礼包' },
            {'tyid': 'TY9999D0006051', 'iosid': 'com.wemomo.game.ddz.36', 'price': 6480, 'name': '月光宝盒礼包' },
            {'tyid': 'TY9999D0006052', 'iosid': 'com.wemomo.game.ddz.26', 'price': 60,   'name': '语音小喇叭100个' },
            {'tyid': 'TY9999D0006053', 'iosid': 'com.wemomo.game.ddz.37', 'price': 300,  'name': '参赛券x30' },
            {'tyid': 'TY9999D0012052', 'iosid': 'com.wemomo.game.ddz.27', 'price': 60,   'name': '7天记牌器' },
            {'tyid': 'TY9999D0006054', 'iosid': 'com.wemomo.game.ddz.38', 'price': 60,   'name': '转运礼包' },
            {'tyid': 'TY9999D0030051', 'iosid': 'com.wemomo.game.ddz.56', 'price': 10,   'name': '转运大礼包' },
            {'tyid': 'TY9999D0030052', 'iosid': 'com.wemomo.game.ddz.42', 'price': 30,   'name': 'VIP普通礼包' },
            {'tyid': 'TY9999D0068051', 'iosid': 'com.wemomo.game.ddz.43', 'price': 60,   'name': 'VIP豪华礼包' },

            {'tyid': 'TY9999D0006055', 'iosid': 'com.wemomo.game.ddz.28', 'price': 60,   'name': '50000金币' },
            {'tyid': 'TY9999D0012051', 'iosid': 'com.wemomo.game.ddz.29', 'price': 120,  'name': '100000金币' },
            {'tyid': 'TY9999D0018051', 'iosid': 'com.wemomo.game.ddz.30', 'price': 180,  'name': '170000金币' },
            {'tyid': 'TY9999D0030053', 'iosid': 'com.wemomo.game.ddz.31', 'price': 300,  'name': '300000金币' },
            {'tyid': 'TY9999D0068052', 'iosid': 'com.wemomo.game.ddz.32', 'price': 680,  'name': '700000金币' },
            {'tyid': 'TY9999D0128051', 'iosid': 'com.wemomo.game.ddz.33', 'price': 1280, 'name': '1500000金币' },
            {'tyid': 'TY9999D0006056', 'iosid': 'com.wemomo.game.ddz.35', 'price': 60,   'name': '月光之钥x3' },
            #{'tyid': 'TY9999D0006057', 'iosid': 'com.wemomo.game.ddz.34', 'price': 60,   'name': '语音小喇叭100个' },
            {'tyid': 'TY9999D0006058', 'iosid': 'com.wemomo.game.ddz.40', 'price': 60,   'name': '转运礼包' },
            {'tyid': 'TY9999D0030054', 'iosid': 'com.wemomo.game.ddz.41', 'price': 300,  'name': '转运大礼包' },
            {'tyid': 'TY9999D0012053', 'iosid': 'com.wemomo.game.ddz.45', 'price': 120,  'name': '记牌器7天' },
            {'tyid': 'TY9999D0030055', 'iosid': 'com.wemomo.game.ddz.46', 'price': 300,  'name': '普通VIP礼包' },
            {'tyid': 'TY9999D0068053', 'iosid': 'com.wemomo.game.ddz.47', 'price': 680,  'name': '豪华VIP礼包' },
            ],
         'clientIds' : '^IOS_3.*momo$',
         },
        {'products' : [
            {'tyid':'DI60', 'price': 6, 'name':'钻石x60', 'iosid' : 'com.tuyoo.sdk.product1'},
            {'tyid':'DI120', 'price': 12, 'name':'钻石x120', 'iosid' : 'com.tuyoo.sdk.product2'},
            {'tyid':'DI180', 'price': 18, 'name':'钻石x180', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI300', 'price': 30 , 'name':'钻石x300', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI680', 'price': 68, 'name':'钻石x680', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI1280', 'price': 128, 'name':'钻石x1280', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI3280', 'price': 328, 'name':'钻石x3280', 'iosid' : 'com.tuyoo.sdk.product3'},
            {'tyid':'DI6480', 'price': 648, 'name':'钻石x6480', 'iosid' : 'com.tuyoo.sdk.product3'},
            ],
         'clientIds' : 'IOS_1.03_tuyou'
        },
    ],
    '7':[
        {'products' : [
            {'tyid': 'TY9999D0006007', 'name':'6万金币',
             'price':60, 'iosid': 'cn.com.majiang.hall.1', },
            {'tyid': 'TY9999D0030007', 'name':'36万金币',
             'price':300, 'iosid': 'cn.com.majiang.hall.2', },
            {'tyid': 'TY9999D0098007', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.majiang.hall.3', },
            {'tyid': 'TY9999D0198007', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.majiang.hall.4', },
            {'tyid': 'TY9999D0328007', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.majiang.hall.5', },
            {'tyid': 'TY9999D0648007', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.majiang.hall.6', },
            {'tyid': 'TY0007D0030007', 'name':'7天会员卡（立得28万金币，每日再赠3万，雀神分翻倍）',
             'price':300, 'iosid': 'cn.com.majiang.hall.7', },
            {'tyid': 'TY0007D0098007', 'name':'30天会员卡（立得100万金币，每日再赠3万，雀神分翻倍）',
             'price':980, 'iosid': 'cn.com.majiang.hall.8', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.majiang.hall.9', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.majiang.hall.10', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'cn.com.majiang.hall.d1280', },
            {'tyid': 'TY9999D0006004', 'name':'6元超值礼包',
             'price':60, 'iosid': 'cn.com.majiang.hall.11', },
            {'tyid': 'TY9999D0006005', 'name':'6元转运礼包',
             'price':60, 'iosid': 'cn.com.majiang.hall.12', },
            #重复定义，因为大厅的item配置限制
            {'tyid': 'TY0007D0030008', 'name':'7天会员卡（立得28万金币，每日再赠3万，雀神分翻倍）',
             'price':300, 'iosid': 'cn.com.majiang.hall.7', },
            {'tyid': 'TY0007D0098008', 'name':'30天会员卡（立得100万金币，每日再赠3万，雀神分翻倍）',
             'price':980, 'iosid': 'cn.com.majiang.hall.8', },
            ],
         'clientIds' : '^IOS_.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0006007', 'name':'6万金币',
             'price':60, 'iosid': 'com.cherrygame.majiang.product.11', },
            {'tyid': 'TY9999D0030007', 'name':'36万金币',
             'price':300, 'iosid': 'com.cherrygame.majiang.product.3', },
            {'tyid': 'TY9999D0098007', 'name':'140万金币',
             'price':980, 'iosid': 'com.cherrygame.majiang.product.a', },
            {'tyid': 'TY9999D0198007', 'name':'300万金币',
             'price':1980, 'iosid': 'com.cherrygame.majiang.product.6', },
            {'tyid': 'TY9999D0328007', 'name':'550万金币',
             'price':3280, 'iosid': 'com.cherrygame.majiang.product.b', },
            {'tyid': 'TY9999D0648007', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.cherrygame.majiang.product.c', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.cherrygame.majiang.product.d', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.cherrygame.majiang.product.e', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石',
             'price':1280, 'iosid': 'com.cherrygame.majiang.product.f', },
            {'tyid': 'TY9999D0006004', 'name':'6元超值礼包',
             'price':60, 'iosid': 'com.cherrygame.majiang.product.g', },
            {'tyid': 'TY9999D0006005', 'name':'6元转运礼包',
             'price':60, 'iosid': 'com.cherrygame.majiang.product.h', },
            ],
         'clientIds' : '^IOS_.*cherry$'
        },
        {'products' : [
            {'tyid': 'TY9999D0006007', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.majiang.mac.d6', },
            {'tyid': 'TY9999D0030007', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.majiang.mac.d30', },
            {'tyid': 'TY9999D0098007', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.majiang.mac.d98', },
            {'tyid': 'TY9999D0198007', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.majiang.mac.d198', },
            {'tyid': 'TY9999D0328007', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.majiang.mac.d328', },
            {'tyid': 'TY9999D0648007', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.majiang.mac.d648', },
            ],
         'clientIds' : '^MAC_.*$'
        },
    ],
    '15':[
        {'products' : [
            {'tyid': 'TY9999D0006015', 'name':'6万金币', 'price':60, 'iosid': 'com.tuyoo.pineapple.c6', },
            {'tyid': 'TY9999D0030015', 'name':'30万金币', 'price':300, 'iosid': 'com.tuyoo.pineapple.c30', },
            {'tyid': 'TY9999D0098015', 'name':'98万金币', 'price':980, 'iosid': 'com.tuyoo.pineapple.c98', },
            {'tyid': 'TY9999D0198015', 'name':'198万金币', 'price':1980, 'iosid': 'com.tuyoo.pineapple.c198', },
            {'tyid': 'TY9999D0328015', 'name':'328万金币', 'price':3280, 'iosid': 'com.tuyoo.pineapple.c328', },
            {'tyid': 'TY9999D0648015', 'name':'648万金币', 'price':6480, 'iosid': 'com.tuyoo.pineapple.c648', },

            {'tyid': 'PA_VIP01', 'name':'1个月', 'price':350, 'iosid': 'com.tuyoo.pineapple.v6', },
            {'tyid': 'PA_VIP02', 'name':'3个月', 'price':980, 'iosid': 'com.tuyoo.pineapple.v15', },
            {'tyid': 'PA_VIP03', 'name':'6个月', 'price':1980, 'iosid': 'com.tuyoo.pineapple.v30', },
            {'tyid': 'PA_VIP04', 'name':'12个月', 'price':3280, 'iosid': 'com.tuyoo.pineapple.v50', },
            {'tyid': 'PA_AVATAR1501', 'name':'动态头像男(时尚)', 'price':600, 'iosid': 'com.tuyoo.pineapple.bh1', },
            {'tyid': 'PA_AVATAR1502', 'name':'动态头像男(职场)', 'price':600, 'iosid': 'com.tuyoo.pineapple.bh2', },
            {'tyid': 'PA_AVATAR1503', 'name':'动态头像女(时尚)', 'price':600, 'iosid': 'com.tuyoo.pineapple.gh1', },
            {'tyid': 'PA_AVATAR1504', 'name':'动态头像女(职场)', 'price':600, 'iosid': 'com.tuyoo.pineapple.gh2', },
            {'tyid': 'PA_TABLETYPE01', 'name':'羊皮纸(复古)牌桌', 'price':1200, 'iosid': 'com.tuyoo.pineapple.tableparchment', },

            ],
         'clientIds' : '^IOS_.*$'
        },
    ],
    '8':[
        {'products' : [
            #IOS_1.x 2.x
            {'tyid':'TEXAS_IOS_COIN1', 'price': 6,   'name':'6万金币',   'iosid' : 'cn.com.dezhou.crazy.product.1'},
            {'tyid':'TEXAS_IOS_COIN2', 'price': 30,  'name':'33万金币',  'iosid' : 'cn.com.dezhou.crazy.product.2'},
            {'tyid':'TEXAS_IOS_COIN3', 'price': 98,  'name':'113万金币', 'iosid' : 'cn.com.dezhou.crazy.product.3'},
            {'tyid':'TEXAS_IOS_COIN4', 'price': 198, 'name':'228万金币', 'iosid' : 'cn.com.dezhou.crazy.product.4'},
            {'tyid':'TEXAS_IOS_COIN5', 'price': 328, 'name':'378万金币', 'iosid' : 'cn.com.dezhou.crazy.product.5'},
            {'tyid':'TEXAS_IOS_COIN6', 'price': 648, 'name':'778万金币', 'iosid' : 'cn.com.dezhou.crazy.product.6'},
            # wangt says these have been abandoned
            {'tyid':'TEXAS_IOS_VIP2',  'price': 98,  'name':'778万金币', 'iosid' : 'cn.com.dezhou.crazy.product.7'},
            {'tyid':'TEXAS_IOS_COIN_LUCKY_R6',  'price': 6,  'name':'10万金币', 'iosid' : 'TEXAS_IOS_COIN_LUCKY_R6'},
            {'tyid':'TEXAS_IOS_ITEM_SEND_LED',  'price': 50,  'name':'喇叭', 'iosid' : 'TEXAS_IOS_ITEM_SEND_LED'},
            {'tyid':'TEXAS_IOS_ITEM_RENAME_CARD',  'price': 98,  'name':'改名卡', 'iosid' : 'TEXAS_IOS_ITEM_RENAME_CARD'},
            #IOS_3.x
            {'tyid': 'TY9999D0006007', 'name': '6万金币',                 'price': 6,   'iosid': 'cn.com.dezhou.crazy.product.1', },
            {'tyid': 'TY9999D0030007', 'name': '36万金币',    'price': 30,  'iosid': 'cn.com.dezhou.crazy.product.2', },
            {'tyid': 'TY9999D0098007', 'name': '140万金币',   'price': 98,  'iosid': 'cn.com.dezhou.crazy.product.3', },
            {'tyid': 'TY9999D0198007', 'name': '300万金币',  'price': 198, 'iosid': 'cn.com.dezhou.crazy.product.4', },
            {'tyid': 'TY9999D0328007', 'name': '550万金币',  'price': 328, 'iosid': 'cn.com.dezhou.crazy.product.5', },
            {'tyid': 'TY9999D0648007', 'name': '1200万金币', 'price': 648, 'iosid': 'cn.com.dezhou.crazy.product.6', },
            {'tyid': 'TY9999D0006005', 'name': '6元转运礼包',             'price': 6,   'iosid': 'TEXAS_IOS_COIN_LUCKY_R6', },
            {'tyid': 'TY9999R0006001', 'name': '60钻石',                  'price': 6,   'iosid': 'cn.com.dezhou.crazy.diamonds.60', },
            {'tyid': 'TY9999R0030001', 'name': '300钻石',                 'price': 30,  'iosid': 'cn.com.dezhou.crazy.diamonds.300', },
            {'tyid': 'TY9999D0006004', 'name': '超值礼包',                'price': 6,   'iosid': 'cn.com.dezhou.crazy.raffle.6', },
            ],
         'clientIds' : '^IOS.*$'
        },
    ],
    '3':[
        {'products' : [
            {'tyid': 'TY9999D0006007', 'name':'6万金币',
             'price':60, 'iosid': 'com.tuyoo.chinesechess.1', },
            {'tyid': 'TY9999D0030007', 'name':'36万金币',
             'price':300, 'iosid': 'com.tuyoo.chinesechess.2', },
            {'tyid': 'TY9999D0098007', 'name':'140万金币',
             'price':980, 'iosid': 'com.tuyoo.chinesechess.3', },
            {'tyid': 'TY9999D0198007', 'name':'300万金币',
             'price':1980, 'iosid': 'com.tuyoo.chinesechess.4', },
            {'tyid': 'TY9999D0328007', 'name':'550万金币',
             'price':3280, 'iosid': 'com.tuyoo.chinesechess.5', },
            {'tyid': 'TY9999D0648007', 'name':'1200万金币',
             'price':6480, 'iosid': 'com.tuyoo.chinesechess.6', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'com.tuyoo.chinesechess.7', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'com.tuyoo.chinesechess.8', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
    ],
    '20':[
        {'products' : [
            {'tyid': 'TY9999D0006007', 'name':'6万金币',
             'price':60, 'iosid': 'cn.com.gomoku.tuyoo.c6', },
            {'tyid': 'TY9999D0030007', 'name':'36万金币',
             'price':300, 'iosid': 'cn.com.gomoku.tuyoo.c30', },
            {'tyid': 'TY9999D0098007', 'name':'140万金币',
             'price':980, 'iosid': 'cn.com.gomoku.tuyoo.c98', },
            {'tyid': 'TY9999D0198007', 'name':'300万金币',
             'price':1980, 'iosid': 'cn.com.gomoku.tuyoo.c198', },
            {'tyid': 'TY9999D0328007', 'name':'550万金币',
             'price':3280, 'iosid': 'cn.com.gomoku.tuyoo.c328', },
            {'tyid': 'TY9999D0648007', 'name':'1200万金币',
             'price':6480, 'iosid': 'cn.com.gomoku.tuyoo.c648', },
            {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
             'price':60, 'iosid': 'cn.com.gomoku.tuyoo.d6', },
            {'tyid': 'TY9999R0030001', 'name':'300钻石（可以用来兑换金币或购买道具）',
             'price':300, 'iosid': 'cn.com.gomoku.tuyoo.d30', },
            {'tyid': 'TY9999R0128001', 'name':'1280钻石（可以用来兑换金币或购买道具）',
             'price':1280, 'iosid': 'cn.com.gomoku.tuyoo.d128', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
    ],
    '10020':[
        {'products' : [
            {'tyid': 'IOS_PA6', 'name':'钻石x6',
             'price':60, 'iosid': 'com.cn.3cards.papa.product.6', },
            {'tyid': 'IOS_PA13', 'name':'钻石x13',
             'price':120, 'iosid': 'com.cn.3cards.papa.product.13', },
            {'tyid': 'IOS_PA33', 'name':'钻石x33',
             'price':300, 'iosid': 'com.cn.3cards.papa.product.33', },
            {'tyid': 'IOS_PA58', 'name':'钻石x58',
             'price':500, 'iosid': 'com.cn.3cards.papa.product.58', },
            {'tyid': 'IOS_PA118', 'name':'钻石x118',
             'price':980, 'iosid': 'com.cn.3cards.papa.product.118', },
            {'tyid': 'IOS_PA638', 'name':'钻石x638',
             'price':4880, 'iosid': 'com.cn.3cards.papa.product.638', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
    ],
    '10039':[
        {'products' : [
            {'tyid': 'product_1', 'name':'木宝箱，60000筹码',
             'price':60, 'iosid': 'product_1', },
            {'tyid': 'product_2', 'name':'铁宝箱，380000筹码 ',
             'price':300, 'iosid': 'product_2', },
            {'tyid': 'product_2_limit', 'name':'特惠礼包1，760000筹码',
             'price':300, 'iosid': 'product_2_limit', },
            {'tyid': 'product_3', 'name':'银宝箱，1380000筹码',
             'price':980, 'iosid': 'product_3', },
            {'tyid': 'product_3_limit', 'name':'特惠礼包2，2760000筹码',
             'price':980, 'iosid': 'product_3_limit', },
            {'tyid': 'product_4', 'name':'金宝箱，5380000筹码',
             'price':3280, 'iosid': 'product_4', },
            {'tyid': 'product_first', 'name':'首冲，380000筹码',
             'price':60, 'iosid': 'product_first', },
            {'tyid': 'product_vip', 'name':'直购vip礼包，1000000筹码 ',
             'price':680, 'iosid': 'product_vip', },
            {'tyid': 'single_product_2', 'name':' 限时特惠，1000000筹码 ',
             'price':500, 'iosid': 'single_product_2', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
    ],
    '10037':[
        {'products' : [
            {'tyid': 'com.naughtycat.jellymaniacn.gold1', 'name':'少量金币',
             'price':60, 'iosid': 'com.naughtycat.jellymaniacn.gold1', },
            {'tyid': 'com.naughtycat.jellymaniacn.gold5', 'name':'较多金币',
             'price':300, 'iosid': 'com.naughtycat.jellymaniacn.gold5', },
            {'tyid': 'com.naughtycat.jellymaniacn.gold50', 'name':'一大堆金币',
             'price':3280, 'iosid': 'com.naughtycat.jellymaniacn.gold50', },
            {'tyid': 'com.naughtycat.jellymaniacn.gold10', 'name':'很多金币',
             'price':680, 'iosid': 'com.naughtycat.jellymaniacn.gold10', },
            {'tyid': 'com.naughtycat.jellymaniacn.gold100', 'name':'一箱金币',
             'price':6480, 'iosid': 'com.naughtycat.jellymaniacn.gold100', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
    ],
    '10040':[
        {'products' : [
            {'tyid': 'com.xingai.tutu.coin70', 'name':'70柠檬',
             'price':10, 'iosid': 'com.xingai.tutu.coin70',},
            {'tyid': 'com.xingai.tutu.coin560', 'name':'560柠檬',
             'price':80, 'iosid': 'com.xingai.tutu.coin560', },
            {'tyid': 'com.xingai.tutu.coin3500', 'name':'3500柠檬',
             'price':500, 'iosid': 'com.xingai.tutu.coin3500', },
            {'tyid': 'com.xingai.tutu.coin6860', 'name':'6860柠檬',
             'price':980, 'iosid': 'com.xingai.tutu.coin6860', },
            {'tyid': 'com.xingai.tutu.coin13160', 'name':'13160柠檬',
             'price':1880, 'iosid': 'com.xingai.tutu.coin13160', },
            {'tyid': 'com.xingai.tutu.coin20860', 'name':'20860柠檬',
             'price':3880, 'iosid': 'com.xingai.tutu.coin20860', },
            {'tyid': 'com.xingai.tutu.coin139860', 'name':'139860柠檬',
             'price':19980, 'iosid': 'com.xingai.tutu.coin139860', },
            {'tyid': 'com.xingai.tutu.coint1', 'name':'139860柠檬',
             'price':1, 'iosid': 'com.xingai.tutu.coin139860', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
        ],
    '10':[
        {'products' : [
            {'tyid':'DI60', 'price': 6, 'name':'钻石x60', 'iosid' : 'com.cn.douniu.tuyoo.product.d60'},
            {'tyid':'DI120', 'price': 12, 'name':'钻石x120', 'iosid' : 'com.cn.douniu.tuyoo.product.d120'},
            {'tyid':'DI180', 'price': 18, 'name':'钻石x180', 'iosid' : 'com.cn.douniu.tuyoo.product.d180'},
            {'tyid':'DI300', 'price': 30 , 'name':'钻石x300', 'iosid' : 'com.cn.douniu.tuyoo.product.d300'},
            {'tyid':'DI680', 'price': 68, 'name':'钻石x680', 'iosid' : 'com.cn.douniu.tuyoo.product.d680'},
            {'tyid':'DI1280', 'price': 128, 'name':'钻石x1280', 'iosid' : 'com.cn.douniu.tuyoo.product.d1280'},
            {'tyid':'DI3280', 'price': 328, 'name':'钻石x3280', 'iosid' : 'com.cn.douniu.tuyoo.product.d3280'},
            {'tyid':'DI6480', 'price': 648, 'name':'钻石x6480', 'iosid' : 'com.cn.douniu.tuyoo.product.d6480'},
            #to be removed
            {'tyid':'COIN_6', 'price': 6, 'name':'钻石x60', 'iosid' : 'com.cn.douniu.tuyoo.product.d60'},
            {'tyid':'IOS_LOGIN_RAFFLE_6', 'price': 6, 'name':'钻石x60', 'iosid' : 'com.cn.douniu.tuyoo.product.d60'},
            {'tyid':'COIN_12', 'price': 12, 'name':'钻石x120', 'iosid' : 'com.cn.douniu.tuyoo.product.d120'},
            {'tyid':'COIN_18', 'price': 18, 'name':'钻石x180', 'iosid' : 'com.cn.douniu.tuyoo.product.d180'},
            {'tyid':'COIN_30', 'price': 30 , 'name':'钻石x300', 'iosid' : 'com.cn.douniu.tuyoo.product.d300'},
            {'tyid':'VIP_30', 'price': 30 , 'name':'钻石x300', 'iosid' : 'com.cn.douniu.tuyoo.product.d300'},
            {'tyid':'ZHUANYUN_30', 'price': 30 , 'name':'钻石x300', 'iosid' : 'com.cn.douniu.tuyoo.product.d300'},
            {'tyid':'COIN_68', 'price': 68, 'name':'钻石x680', 'iosid' : 'com.cn.douniu.tuyoo.product.d680'},
            {'tyid':'COIN_128', 'price': 128, 'name':'钻石x1280', 'iosid' : 'com.cn.douniu.tuyoo.product.d1280'},
            {'tyid':'COIN_328', 'price': 328, 'name':'钻石x3280', 'iosid' : 'com.cn.douniu.tuyoo.product.d3280'},
            {'tyid':'COIN_648', 'price': 648, 'name':'钻石x6480', 'iosid' : 'com.cn.douniu.tuyoo.product.d6480'},
            ],
         'clientIds' : '^IOS.*$'
        },
        {'products' : [
            {'tyid': 'TY9999D0006003', 'iosid': 'com.cn.douniu.tuyoo.product.c6',    'price': 60,   'name': '6万金币' },
            {'tyid': 'TY9999D0030003', 'iosid': 'com.cn.douniu.tuyoo.product.c30',   'price': 300,  'name': '30万金币' },
            {'tyid': 'TY9999D0098001', 'iosid': 'com.cn.douniu.tuyoo.product.c98',   'price': 980,  'name': '98万金币' },
            {'tyid': 'TY9999D0198001', 'iosid': 'com.cn.douniu.tuyoo.product.c198',  'price': 1980, 'name': '198万金币' },
            {'tyid': 'TY9999D0328001', 'iosid': 'com.cn.douniu.tuyoo.product.c328',  'price': 3280, 'name': '328万金币' },
            {'tyid': 'TY9999D0648001', 'iosid': 'com.cn.douniu.tuyoo.product.c648',  'price': 6480, 'name': '648万金币' },
            {'tyid': 'TY9999D0001002', 'iosid': 'com.cn.douniu.tuyoo.product.c1',    'price': 10,   'name': '1万金币' },
            {'tyid': 'TY9999D0003001', 'iosid': 'com.cn.douniu.tuyoo.product.c3',    'price': 30,   'name': '3万金币' },
            {'tyid': 'TY9999R0006001', 'iosid': 'com.cn.douniu.tuyoo.product.d60',   'price': 60,   'name': '60钻石' },
            {'tyid': 'TY9999R0030001', 'iosid': 'com.cn.douniu.tuyoo.product.d300',  'price': 300,  'name': '300钻石' },
            {'tyid': 'TY9999R0128001', 'iosid': 'com.cn.douniu.tuyoo.product.d1280', 'price': 1280, 'name': '1280钻石' },
            ],
         'clientIds' : '^IOS.*hall10.*crazy$'
        },
    ],
    '12':[
        {'products' : [
            #套餐0 美国  美元
            {'tyid':'products0_sea_texas_chip_1', 'price': 100, 'name':'chipx10000', 'iosid' : 'com.cn.sea.tuyoo.product.chip_1'},
            {'tyid':'products0_sea_texas_chip_2', 'price': 500, 'name':'chipx55000', 'iosid' : 'com.cn.sea.tuyoo.product.chip_2'},
            {'tyid':'products0_sea_texas_chip_3', 'price': 2000, 'name':'chipx225000', 'iosid' : 'com.cn.sea.tuyoo.product.chip_3'},
            {'tyid':'products0_sea_texas_chip_4', 'price': 5000, 'name':'chipx575000', 'iosid' : 'com.cn.sea.tuyoo.product.chip_4'},
            {'tyid':'products0_sea_texas_chip_5', 'price': 10000, 'name':'chipx1170000', 'iosid' : 'com.cn.sea.tuyoo.product.chip_5'},
            {'tyid':'products0_sea_texas_chip_6', 'price': 20000, 'name':'chipx2400000', 'iosid' : 'com.cn.sea.tuyoo.product.chip_6'},

            {'tyid':'products0_sea_texas_coin_1', 'price': 100, 'name':'coinx100', 'iosid' : 'com.cn.sea.tuyoo.product.coin_1'},
            {'tyid':'products0_sea_texas_coin_2', 'price': 500, 'name':'coinx500', 'iosid' : 'com.cn.sea.tuyoo.product.coin_2'},
            {'tyid':'products0_sea_texas_coin_3', 'price': 2000, 'name':'coinx2000', 'iosid' : 'com.cn.sea.tuyoo.product.coin_3'},
            {'tyid':'products0_sea_texas_coin_4', 'price': 5000 , 'name':'coinx5000', 'iosid' : 'com.cn.sea.tuyoo.product.coin_4'},
            {'tyid':'products0_sea_texas_coin_5', 'price': 10000, 'name':'coinx10000', 'iosid' : 'com.cn.sea.tuyoo.product.coin_5'},
            {'tyid':'products0_sea_texas_coin_6', 'price': 20000, 'name':'coinx20000', 'iosid' : 'com.cn.sea.tuyoo.product.coin_6'},
            #
            #套餐4  中国  人民币
            {'tyid':'products4_sea_texas_chip_1', 'price': 60, 'name':'6万筹码', 'iosid' : 'com.cn.sea.tuyoo.product4.chip_1'},
            {'tyid':'products4_sea_texas_chip_2', 'price': 300, 'name':'33万筹码', 'iosid' : 'com.cn.sea.tuyoo.product4.chip_2'},
            {'tyid':'products4_sea_texas_chip_3', 'price': 600, 'name':'68万筹码', 'iosid' : 'com.cn.sea.tuyoo.product4.chip_3'},
            {'tyid':'products4_sea_texas_chip_4', 'price': 1280, 'name':'150万筹码', 'iosid' : 'com.cn.sea.tuyoo.product4.chip_4'},
            {'tyid':'products4_sea_texas_chip_5', 'price': 3280, 'name':'388万筹码', 'iosid' : 'com.cn.sea.tuyoo.product4.chip_5'},
            {'tyid':'products4_sea_texas_chip_6', 'price': 6480, 'name':'777万筹码', 'iosid' : 'com.cn.sea.tuyoo.product4.chip_6'},

            {'tyid':'products4_sea_texas_coin_1', 'price': 60, 'name':'60金币', 'iosid' : 'com.cn.sea.tuyoo.product4.coin_1'},
            {'tyid':'products4_sea_texas_coin_2', 'price': 300, 'name':'300金币', 'iosid' : 'com.cn.sea.tuyoo.product4.coin_2'},
            {'tyid':'products4_sea_texas_coin_3', 'price': 600, 'name':'600金币', 'iosid' : 'com.cn.sea.tuyoo.product4.coin_3'},
            {'tyid':'products4_sea_texas_coin_4', 'price': 1280 , 'name':'1280金币', 'iosid' : 'com.cn.sea.tuyoo.product4.coin_4'},
            {'tyid':'products4_sea_texas_coin_5', 'price': 3280, 'name':'3280金币', 'iosid' : 'com.cn.sea.tuyoo.product4.coin_5'},
            {'tyid':'products4_sea_texas_coin_6', 'price': 6480, 'name':'6480金币', 'iosid' : 'com.cn.sea.tuyoo.product4.coin_6'},
            ],
         'clientIds' : '^IOS.*$'
        },
    ],
    '10038':[
        {'products' : [
            {'tyid': 'yhzs006', 'name':'60钻石',
             'price':60, 'iosid': 'yhzs006', },
            {'tyid': 'yhzs030', 'name':'300钻石',
             'price':300, 'iosid': 'yhzs030', },
            {'tyid': 'yhzs068', 'name':'680钻石',
             'price':680, 'iosid': 'yhzs068', },
            {'tyid': 'yhzs128', 'name':'1280钻石',
             'price':1280, 'iosid': 'yhzs128', },
            {'tyid': 'yhzs328', 'name':'3280钻石',
             'price':3280, 'iosid': 'yhzs328', },
            {'tyid': 'yhzs648', 'name':'6480钻石',
             'price':6480, 'iosid': 'yhzs648', },
            ],
         'clientIds' : '^IOS_3.*$'
        },
    ]
})

'''博瑞Now支付（iOS）
'''
add_global_item('borui_paykeys', {
    'appId' : '1448952896154635', # 应用编号
    'appSecret' : 'ZPePYKRi6RQwUsgyrN1tfGI5JLrE2KsB', # 应用秘钥
    'notifyUrl':'http://api.adwan.cn:8088/ming/api/notify_puke.php',
    'mhtReserved':'dzpk001',

    # 欢乐JJ斗地主
    '1451035182189979':{
        'appId':'1451035182189979',
        'appSecret':'8DlS6tFiU8q9AgqdLw9uFfWKIr6O2d11',
        'notifyUrl':'http://open.touch4.me/v1/pay/now/callback',
        'mhtReserved':'',
    },

    # 开心斗地主
    '1451296893973044':{
        'appId':'1451296893973044',
        'appSecret':'dxbXA48lS0NLl9xVMT0FRoamToVgVlIN',
        'notifyUrl':'http://open.touch4.me/v1/pay/now/callback',
        'mhtReserved':'',
    },
    
    ###
    'IOS_3.730_tyGuest,tyAccount.ipaynow.0-hall6.appStore.single': '1451296893973044',
    'IOS_3.762_tyGuest,tyAccount,weixin.ipaynow.0-hall6.appStore.single': '1451035182189979',
})


"""
    木蚂蚁appKey配置
"""
add_global_item('mumayi_keys', {
    'com.tuyoo.doudizhu.mumayi':'b626b6307849bdde9MhztvphLbM6JjUCCs09tdKKkUEHKNRnzGVQLl5iLPijKew5nuY', # 斗地主
    'com.tuyoo.texas.mumayi':'8029d91caaaa12fcLnRsLsRwVgPcvKpvEMzvezqXFv0ZKmmfrXsvdkIhk3hje6Y0dR4', # 德州
})

"""
    朋友玩gameKey和apiSecret映射表
"""
add_global_item('pengyouwan_keys', {
    '287022eb':'c94427e45bb0477e', # 斗地主

})


"""
    4399 appKey配置
"""
add_global_item('m4399_keys', {
    'com.doudizhu.mainhuanle.m4399': {
        'appKey':'110721',
        'appSecret':'eec64872bc816a981c80aaea2bc2bc6b',
    }, # 斗地主
    'com.example.chinesechess.m4399': {
        'appKey':'110723',
        'appSecret':'312db76cef720f61de5554c844c0b0cb',
    }, # 象棋
})

"""
    IOS微信支付控制参数
"""
###
### 4月4日需要将主包和德州策略 当天恢复成45分钟
add_global_item('ios_weinxin_pay_control', {
    'weixin_totaltime_threshold':1800, # 超过半小时开始弹微信支付
    'weixin_products':['TY9999R0328001', 'TY9999D0328001', 'TY9999R0648001', 'TY9999D0648001'],
    'wxpay_limit_count':3,
    # 策略1 当日超过10分钟或累计超过1小时
    'default_strategy': {
        'total':5*3600,
        'today':1800,
        'day7':2*3600,
        'vip':3,
        'operator':'or',
    },
    "main_strategy": {
        'total':5*3600,
        'today':1800,
        'day7':2*3600,
        'vip':3,
        'operator':'or',
    },
    "texas_strategy": {
        'total':5*3600,
        'today':1800,
        'day7':2*3600,
        'vip':3,
        'operator':'or',
    },
    "amfy_strategy": { # 澳门风云策略(10039)
        'total':1800,
        'today':300,
        'operator':'and',
    },
    "testing_strategy": { # 测试策略，随时可以弹出
        "total":1,
        "today":1,
        "operator":'or',
    }
})


"""
    卓易 appKey配置
"""
add_global_item('zhuoyi_keys', {
    'com.example.chinesechess.zy': {
        'appId':'2235',
        'appKey':'79460bcab6153758dfeb8a1b0f7bf3dc',
        'paySecret':'3a0d9efddf167a8d1419512bfc5c01c5',
        'appChannel':'2235_01',
        'codes': {
            'TY9999R0000101'          : '1',
            'TY9999D0001003'          : '1',
            'TY9999D0002001'          : '2',
            'TY9999D0008005'          : '5',
            'TY9999D0008001'          : '6',
            'TY9999D0008025'          : '7',
            'TY9999D0008026'          : '8',
            'TY9999R0008005'          : '9',
            'TY9999D0010001'          : '10',
            'TY9999D0005003'          : '3',
            'TY9999D0006016'          : '4',
            'TY9999D0006001'          : '4',
            'TY9999D0008027'          : '5',
            #'TY9999D0012002'          : {'feecode':'12',       'name':'会员订阅',     "alternativeProdId":"TY9999D0012005", "alternativeProdName":"30天会员"},
            #'TY9999D0012003'          : {'feecode':'12',       'name':'会员订阅',     "alternativeProdId":"TY9999D0012005", "alternativeProdName":"30天会员"},
            #'TY9999D0012004'          : {'feecode':'12',       'name':'会员订阅',     },
            #'TY9999D0010006'          : {'feecode':'13',       'name':'30天会员',     },
            #'TY9999R00021DJ'          : {'feecode':'14',        'name':'60000银币',     },
            #'TY9999R0010001'          : {'feecode':'15',        'name':'100钻石',     },
            'TY9999D0008034'          : '6',

            '1天会员' :'1',
            '20000金币' :'2',
            '50000金币' :'3',
            '60000金币' :'4',
            '80000金币' :'5',
            '8元超值礼包' :'6',
            '高手限量特价礼包' :'7',
            '转运限量特价礼包' :'8',
            '80钻石' :'9',
            '100000金币' :'10',
        }
    }, # 象棋
})


"""
    搜狗 appKey配置
"""
add_global_item('sougou_keys', {
    '1510': { # 途游斗地主（支持单机）
        'package':'com.tuyoo.tudoudizhu.sougou',
        'appKey':'2f0be9a8a5bbf9c3f7668fa09d659fa0524d66e18232de284072eb1db7d3cfbf',
        'appSecret':'3ca69938b08a7e7c00a38a853142e174b0137339fd7abcb4a7dca56cfb18548a',
        'paySecret':'{881A82BC-80ED-4704-AEA6-806B8C3C7650}',
    },
    '1511': { # 途游德州扑克（美女竞技）
        'package':'com.tuyoo.texas.sougou',
        'appKey':'8d6551e53154dbbf8c47266672962e1cda3d3aa287b25ecf68252d25e7412504',
        'appSecret':'f06865a65a19fdc05272ab02daabb38b220a6fe65cdfab68ffd01d42926d9695',
        'paySecret':'{66661557-8AEF-412E-9B0B-A7CACE2328DD}',
    },
})


"""
    酷派 appKey配置
"""
add_global_item('coolpad_keys', {
    # 平台公钥
    '5000003083': { # 途游四国军旗
        'package':'com.tuyoo.junqi.coolpad',
        'appId':'5000003083',
        'appKey':'b50d655b203b482ea28487001ea21444',
        'publicKey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCHxOwiGMjPiAdVfzj/7PxOlu2B
U7w8vEtTlbRzhC96EegjpfuIBZ4s2gTVvPxofc/fi/ZIYCCplRYtkHe3+T5x5hSV
KH4r1LtWQahRtvqSfFuVxXWT8DO5zzpKbxxxOPqdIg6gLl3f028g9KnqyUSBX9Uo
prFE0WSHr6+vYQw34wIDAQAB
-----END PUBLIC KEY-----''',
        'privateKey':'MIICXQIBAAKBgQCMGp95RY2QaTVnuMLtpfcLlXa0uhMJk4+kmW9E5A26COvdHlQPe6TJ6rEOlzOJcochFYpDy8586IKu7e/BliM6rTo4Xzv9k43lp5JLU7M+b/0VBgudPnlo3r86mSZ2KUC9APAFvkkzJKc0A+puNH/lHcpfZHTpIW2q5VgkLXoRCQIDAQABAoGAWvVd26ngQoVLes9lHkzFmuuqaaL0gR8f/sjuiFdW4hSwrJnoETVAwyZvVP2tI+sK99u4LFPA9y8syM0I/zGuJIW5yBZJgJ2VsZVllAVLanO0EGcY6xetSQexzOEnNlB3r2Er15n/wLPIlvzQHYWX1CkVkZag8XuR3cFO12eycBECQQD9SuLeIF5mAqvuloYUXYkz7MIssNI4PzxitGCAG7HRVn9dXCu4ETaig613Vyfqbqm2o+20JOcBs2q8wgj4FIlfAkEAjZoBfHo8Stfuiv8hn4J5VlqRygQdZuC2dFLt0J/EwSXOr2xUP8pq26j1xy8FkCRg90bSde9a1OIfHp56L302lwJBAJhyPeEa8jXLXdeXWNNhCHbsBGIJejzIMnvlvD7ebENmH/n8w4NhONTPE9RD7I44VITMXQCTRUXMym0ZC3TkR1kCQHss+Zf/eM0eMwpET0pDJCujE2jo1W61kOF1dhvhrzTZH4bntA3dlcDIpCwFUlCF5LeVquQeNyQyIyHud5kx0bcCQQDo5eQoh4zi65WQi72mOgC1b2FJuguk5tHwkLSZtr0zMH6vR5aKDVmkS9clnTH2zq/q02ETkgzdnVq0G611Zetk',
        'products': {
            'TY9999D0001003': '1',
            'TY9999D0002001': '2',
            'TY9999D0005003': '3',
            'TY9999D0006016': '4',
            'TY9999D0008027': '5',
            'TY9999D0008005': '5',
            'TY9999D0008001': '6',
            'TY9999D0008034': '6',
            'TY9999D0008025': '7',
            'TY9999D0008026': '8',
            'TY9999R0008005': '9',
            'TY9999D0010001': '10',
            'TY9999D0030001': '11',
            'TY9999D0050001': '12',
            'TY9999D0100001': '13',
            'TY9999R0008005': '15',
            'TY9999D0010001': '10',
        }
    },
    '5000003081': { # 途游保皇
        'package':'com.tuyoo.baohuang.coolpad',
        'appId':'5000003081',
        'appKey':'f9cecbbcc40d4f1397becfc0cb7df60f',
        'publicKey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCZWXCbEYHbtGbxkuCMVFLyBEAa
41gxG1z06O7wYZeAbMv9uAwRjHGzGxf2OfT2Jq7abgoreg/GEM4fGlawfx6iVY9f
tfks30XyZ/WUUrBTPdjFuuneTdG4rimFg1V/c/clBkkFxyO5wWCiF/Ds29htkEv8
6q0aJl8petwXJzaCIwIDAQAB
-----END PUBLIC KEY-----''',
        'privateKey':'MIICXAIBAAKBgQCNCFkNMq6vnes9Y4geHI1Ije6gLNsnuWhhoJRekWMI1wp/9gMtyIOj7ifSKVuZL59V1J8BZLUXb2LBNLgA/j+j4WpnYbM6dG697smc/U6i981cxXLXguhbA1LnUShIlIPjxIDgoLVXqEM1fUepRhI8OtNG5ADFRbVrX+Q4fPRQrwIDAQABAoGAeSESWyOMpYkc4jz6S+J59jbxHOFp2VSFMlSZGiAEzzLi8cR6NnhhmAqUaQzcf1VHpJBZgPjeEKK6TvbYkwHL5cvbvhOqTMcgcpY8IJE4wddfsp5RTEfeEW/Xb9ezxossQVQPcJ6P8cxaOMNP24tKUjih2UD+MrFRiCSFVEFwwwECQQDZ9sXY1rrJcqudCJShjBWtc7c4Et0Q905Zxs4SNlcs+wKvLdDhAh0CqtPmaczlZoVrHTEGRHOPOg9fJEy9OHaVAkEApaTHA12WlWKO8QzmPfSHr8ha5pJJNjlpc6h61R+BDfGb86EMVnlgW5uPTJp7eM2itruuFc5r/AeKnr3qjcqtMwJBANiDjwMYQtHLi/fgxyw2aG41jWIxMtIgp/78QkXLHwu6iG8VtvFc1Q6KPRYcMQILtiqyA7nzE0vKY+yhtW0dgoUCQFh3ivrXLyeVvfYsB4QrZ5SQk0v18TgOra1h3EibTNffpIUYDHja1oXWrVAiabN5UF/8GNv4pV+zv2tMz0rvZlUCQFoBrGooLB7jboc5ssM8iIEk2CT7VVHGEuthVJ594HEvjGtNJy37tyw0R9/diFbMFSe9sWr1u4jYjisM0jAxKc8=',
        'products': {
            'TY9999R0050001': '1',
            'TY9999D0002001': '2',
            'TY9999D0005003': '3',
            'TY9999D0006016': '4',
            'TY9999D0008005': '5',
            'TY9999D0008027': '6',
            'TY9999D0010001': '7',
            'TY9999D0030001': '8',
            'TY9999D0050001': '9',
            'TY9999D0100001': '10',
            'TY9999D0300001': '11',
            'TY9999D1000001': '12',
            'TY9999R0000101': '13',
            'TY9999R0008005': '14',
            'TY9999R0100001': '15',
            'TY9999D0008026': '30',
            'TY9999D0050007': '19',
            'TY9999D0100011': '20',
            'TY9999D0001003': '21',
            'TY9999D0012003': '22',
            'TY9999D0008001': '28',
            'TY9999D0008025': '29',
            'TY9999D0030011': '17',
            'TY9999D0030012': '31',
            'TY9999D0100012': '33',
            'TY9999R0030001': '34',
        }
    },
})



"""
    聚乐(HTC) appKey配置
"""
add_global_item('jolo_keys', {
    # 平台公钥
    'publicKey':'''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDbRLzWfCD4pQb1mjeGLy6gw+Af
OKZ1dpNbMUyZml+p3stTSdTyHHpkuPPsaOqsT9gFDSmXz5KRBt4w6KCeLj/R61KA
5rmMJipDnSJV19kld0z6NW47kiEQHslaalDBCST94TUIcCzjhaiG3yTChDCTFo3v
47qyt6j3YvVpih8UNQIDAQAB
-----END PUBLIC KEY-----''',
    ####
    'com.tuyoo.tudoudizhu.htc': {
        'gameCode':'2913285111414',
        'gameName':'途游斗地主',
        'publicKey':'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHg6J7GnYor1w+tmL4+cV46e1od76w6HJkieI2AmLI8W3Qv0HuZ3Omw82n/a4cSE3y/XgpsTtzhAL9v+syajygL18Dn2SpFHMpjfcqZf+1IY6SmtKpAKbfNgsu6eS+d8+1zzdGD9tiUFULddkhe6N6AwyF9PNh8pDh+PsKG5TXRQIDAQAB',
        'privateKey':'MIICeQIBADANBgkqhkiG9w0BAQEFAASCAmMwggJfAgEAAoGBAMeDonsadiivXD62Yvj5xXjp7Wh3vrDocmSJ4jYCYsjxbdC/Qe5nc6bDzaf9rhxITfL9eCmxO3OEAv2/6zJqPKAvXwOfZKkUcymN9ypl/7UhjpKa0qkApt82Cy7p5L53z7XPN0YP22JQVQt12SF7o3oDDIX082HykOH4+woblNdFAgMBAAECgYEAsCJM0gMFZ1uQwyh+7bCLnfheh8iXB1TekFWN6AJpNV62hQAj85VO612W9ISnLf7DGg6dA6mcg5l6jovc1pAlXfFdE7MaLylxbRyM6s+11CcBSi9XffDvFuTDhbtvjldbA1O9+J0A5yunSJhu+SJsktirDODbgRbnGiNLJZVXjK0CQQDvkPVt9j8KyjsR/PYUUXq+7mF+tI5QfL8UMrNRBiFWQGCvgJJJLPwzoOTmXwiguK9kV/iglPSZQ37qNWP+xqtjAkEA1TNRo1ZBEQ9P86SvwbKry6hJx3hU3v/43jiYD7qleNgsYd7ZtY0KT3P6Yq7j3zuHH9zgWucG249s6ghSIkl3NwJBAJtrCp5lE68XVc0stCSoW56EnkGKN42l8HzVC5o0BOqk51TUb5MDmTaRWg7OdpV2W2sY21aqbCkGLc8aBh5imwsCQQCE/phknb/FFpo3UHpbCEvmpTow9j1rRp5GcWNaHIJwmdlFzDBe8naGDcEZoiN/87BdDfneetNqT1QPwdUKkm2NAkEA0JfaEXXlTCyYAKYyjVuKOMvTrZTf2/F14cKIlBbS2FFaFVzrlYAJfIb0t5KcZ0+X2fPkmDv57fi3jtjLNpjBQQ==',
    }

})


"""
 啪啪游戏大厅 appKey配置
"""
add_global_item('papa_keys', {
    '16000073': {
        'privateKey':'b47387d2b01c16b7',
        'secretKey':'3a0bbcfd94c0e7d821a3e041a2fc77cc1b95f46991dfbb1cdd2121358e5e0523',
    }
})


"""
 快玩 appKey配置
"""
add_global_item('kuaiwan_keys', {
    '284': {
        'appKey':'85bhsfofuxpwrvvhst4zv1ol764vt24f',
    }
})

"""
 快玩 appKey配置
"""
add_global_item('zplay_redirect_url', {
    '4': "https://itunes.apple.com/cn/app/id1090850101",
})

"""
 唱吧appkey配置
"""
add_global_item('changba_keys',{
    '3004578291': {
        'publicKey': '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDEfjMO0XZsHrnAQKECxYFc0FX3
wbz6cEDf5GUEbktaPOlcJJhuDrb1Tp8LtmZ/28i5ENkSFDE4d2bJV8Koj5E0y9XT
39NcV3XqzbNHNcGr73wpURkkPDzYIGaHYHSQha13FD8DdByDT34narPVlcxtTrWn
bj4Z+09EEgaCMUKWvwIDAQAB
-----END PUBLIC KEY-----'''
    }
})


"""
 热云上报数据
"""
add_global_item('reyun_config',{
    'IOS_3.765_tyGuest.weixin,appStore,alipay,alipaywap.0-hall6.appStore.single': {
        'appId': 'bf7f39d5122b65c4d4aea55b799f9968',
        'channelId':'_default_',
    }
})


"""
栗子支付 serverkey配置
"""
add_global_item('lizi_keys', {
    'AD945716C35CCAD961F7': {
        'serverKey': 'LNXCBSi6St5Xa4umwgzmxlXsfM3d9HUL'
    }
})

add_global_item('alibig_config', {
    'userList':[10129, 10145],
    'clientList':['Android_3.767_tyGuest.yisdkpay4.0-hall6.baidusearch.tu',],
    'prodId':'TY9999D0002001',
    'prodCount':2600,
    'prodPrice':0.1,
    'prodName':'5200万金币',
    'paymentName':'2千元购买5200万金币',
    'paymentTips':'买了不上当，买了不后悔',
    'limitCount': 7,
})

"""
努比亚 参数配置孙
"""
add_global_item('nubia_keys', {
    '408464': {
        'secret': 'DDDE8F75B2C2390275231CB53C63E921'
    },
    '455117': {
        'secret': '3D6589168AC18545C3706638ADE8DAC5'
    },
    '710010': {
        'secret': '1A40171D14C89612F1406D6F22CC3FFB'
    },
})


"""
应用宝YSDK
"""
add_global_item('ysdk_keys', {
    'sandbox_url': 'ysdktest.qq.com',
    'release_url': 'ysdk.qq.com',
    '1105251413': {
        #sandbox
        'sandbox_appKey': '5iTNpidxzGr3i2keKbgnyhIf1NUSc8I9',
        #现网
        'release_appKey': 'JJBDKkAAJsQkXIoBBsJzI9E2DES7F4gD',
        'qq_appId': '1105251413',
        'qq_appKey': 'lYpbE3SsEuBqFIke',
        'wx_appId': 'wx0a9188e66af5e1a0',
        'wx_appKey': '2290948173f5480489f13203b12dfcf1'
    },
    #优乐麻将的参数：
    '1105671996': {
        #sandbox
        'sandbox_appKey': 'oZJfoE06BYrmOSIyFX7dUg9We8AqfkJZ',
        #现网
        'release_appKey': 'u5rQsUba2mPwNJMH9QrRDZeqUqhKjVsH',
        'qq_appId': '1105671996',
        'qq_appKey': 'zJrsnxfpkNVEdO6F',
        'wx_appId': 'wxf9bf1f278b62ecb0',
        'wx_appKey': 'a7666c6ef841559038e22b6a3cbefa57'
    },
    #点点麻将ysdk参数：
    '1105600917': {
        #sandbox
        'sandbox_appKey': 'BmwMuKYoYlDLNH1zKAe1pPZqj1aDg7IM',
        #现网
        'release_appKey': 'XzStB9f6rxrUe6XQgDP40Xrm7IHbeqM4',
        'qq_appId': '1105600917',
        'qq_appKey': 'Mro7xnzT9QDjX9yG',
        'wx_appId': 'wx42dbe62e7cc9c504',
        'wx_appKey': 'a9480bae73a09bf357be594c7be7a02d'
    },
    #三缺一
    '1105671156': {
        #sandbox
        'sandbox_appKey': 'QpRzl8yH0XUpWobCkWb0pTcdTcbKw6JD',
        #现网
        'release_appKey': 'mEbreIMxoO0uHE9bnuTJZxGel8wPlqRN',
        'qq_appId': '1105671156',
        'qq_appKey': 'Deeu4bTqDPbHkvVb',
        'wx_appId': 'wx41789d3c7a8a6ad2',
        'wx_appKey': 'c9b1447884ed88a524679db05cb23fe7'
    },
    #经典途游德州
    '1105787022':{
        #sandbox
        'sandbox_appKey': 'uirfL1i2egGX7KgspfExbkExyNvIu59J',
        #现网
        'release_appKey': '84U37j5Ud9MyanevsYc0vojbdbu3xI2x',
        'qq_appId': '1105787022',
        'qq_appKey': 'fbDT6ECccXu8nPiU',
        'wx_appId': 'wxeff5dc920adba335',
        'wx_appKey': '7c1f203174d745d2946e1f50e989500b'
    },
})


"""
乐视tv
"""
add_global_item('letv_keys', {
    '250219': {
        'appid': '250219',
        'scrkey': '348d752288114394aa4e288a9f2ca4c8'
    },
    '215607': {
        'appid': '215607',
        'scrkey': '75e29985546f470ab715e89b6b4cfb10'
    },
    '231097': {
        'appid': '231097',
        'scrkey': '3fc04b297a2c4e22bfac4ffd718aee03'
    },
    '227354': {
        'appid': '227354',
        'scrkey': '00115b31caef4f80811083257481ed81'
    },
    '256983': {
        'appid': '256983',
        'scrkey': 'e1b0258af4ba46b2b8df6c817334494d'
    },
    '256913': {
        'appid': '256913',
        'scrkey': 'f2574dfcb1604cb0b74d21e4e551677d'
    },
})
"""
v4登陆控制
"""
add_global_item('login_strategy',{
    '9999':
        {
            'switch':'oni',
            '0':{
                'code':1,
                'info':'为了您的账户安全，请先绑定手机'
            },
        }
})

'''
微信公众号中使用的一些参数
'''
add_global_item('externalLogin',{
    '9999':{
        'appId':9999,
        'clientId':'Android_3.767_tyGuest.yisdkpay4.0-hall6.baidusearch.tu',#随便找的一个,
        'md5':'919981c74a064261ac044f0888cf8f75',
    }
})

'''
百度游戏 配置
'''
add_global_item('bdgame_keys', {
    '8169647': {
        'appId': '8169647',
        'secretKey': 'szwjleCzE2OytO5y0IOo1FEumPHVoG9R'
    }
})

'''
益玩配置
'''
add_global_item('yiwan_keys', {
    '104693': {
        'appId': '10469',
        'appKey': 'YuhSZlQrDC3Wq1cn'
    }
})

'''
JUSDK 配置
'''
add_global_item('jusdk_keys', {
    '202979001': {
        'appId': '202979001',
        'appKey': 'a0c50f346283879bbe4ef310d38db2d8'
    }
})

'''
v4 防爆卡控制
'''
add_global_item('smspay_strategy', {
    'out_limit_tips':"对不起，暂时无法支付，请稍后重试",
    'liantong.wo': {
        'limit_month': 290,
        'limit_day': 20,
        'min_interval':600
    },
    'ydjd': {
        'limit_month': 290,
        'limit_day': 20,
        'min_interval':600
    },
})

'''
 Mobvista 重定向URL設置
'''
add_global_item('mobvista_redirect_url', {
    'pwjtest2':"https://itunes.apple.com/cn/app/id1090850101",
    'ty_dzpk_cn_ios':"https://itunes.apple.com/cn/app/id1125917659?mt=8"
})


'''
 Appcoach 重定向URL設置
'''
add_global_item('appcoach_redirect_config', {
    'pwjtest2':"https://itunes.apple.com/cn/app/id1090850101",
    'redirect_url':"https://itunes.apple.com/cn/app/id1092491104?mt=8"#永恒手游
})

