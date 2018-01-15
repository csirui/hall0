# -*- coding=utf-8 -*-

from pyscript._helper_config_ import add_global_item

cross_config = dict()

cross_config['6'] = [  # 从主渠道 到 细化渠道, 优先检查后缀为360.1的渠道
    [ 'tuyou', [
            {
                'title': u'天天德州',
                'pkg': 'com.tuyoo.dezhoupoker.main',
                'url': 'http://apk.dl.tuyoo.com/down/dezhou/tuyoo_android_poker.apk',
                'icon': 'dezhou_icon.jpg',
                'desc': '天天德州，加入新的玩法',
                'appid': 8
            },
            {
                'title': u'疯狂斗牛',
                'pkg': 'com.tuyoo.douniu.main',
                'appid': 5,
                'url': 'http://apk.dl.tuyoo.com/down/douniu/tuyoo_android_douniu.apk',
                'icon': 'douniu_icon.jpg',
                'desc': '疯狂斗牛，加入新的玩法',
            },
            {
                'title': u'疯狂麻将',
                'pkg': 'com.mahjong.kuaile',
                'appid': 7,
                'url': 'http://apk.dl.tuyoo.com/down/majiang/tuyoo_android_majiang.apk',
                'icon': 'majiang_icon.jpg',
                'desc': '途游麻将，加入新的玩法',
            }
        ]
    ],
    [ '360', [
            {
                'title': u'天天德州',
                'pkg': 'com.tuyoo.dezhoupoker.main',
                'url': 'http://apk.dl.tuyoo.com/down/dezhou/tuyoo_android_poker.apk',
                'icon': 'dezhou_icon.jpg',
                'desc': '天天德州，加入新的玩法',
                'appid': 8
            },
            {
                'title': u'疯狂斗牛',
                'pkg': 'com.tuyoo.douniu.main',
                'appid': 5,
                'url': 'http://apk.dl.tuyoo.com/down/douniu/tuyoo_android_douniu.apk',
                'icon': 'douniu_icon.jpg',
                'desc': '疯狂斗牛，加入新的玩法',
            },
            {
                'title': u'途游麻将',
                'pkg': 'com.tuyoo.majiang.kuaile',
                'appid': 7,
                'url': 'http://apk.dl.tuyoo.com/down/majiang/tuyoo_android_majiang.apk',
                'icon': 'dizhu_icon.jpg',
                'desc': '途游麻将，加入新的玩法',
            }
        ]
    ],
    [ '360.1', [
            {
                'title': u'欢乐德州',
                'pkg': 'com.tuyoo.dezhou.main',
                'url': 'http://apk.dl.tuyoo.com/down/dezhou/tuyoo_android_poker.apk',
                'appid': 8,
                'icon': '/open/img/dizhu_icon.jpg',
                'desc': '欢乐德州，加入新的玩法',
            },
            {
                'title': u'疯狂斗牛',
                'pkg': 'com.tuyoo.douniu.main',
                'appid': 5,
                'url': 'http://apk.dl.tuyoo.com/down/douniu/tuyoo_android_douniu.apk',
                'icon': '/open/img/dizhu_icon.jpg',
                'desc': '欢乐德州，加入新的玩法',
            }
        ]
    ]
]

add_global_item('cross.config.applist', cross_config)

add_global_item('cross.config.reward', {
        '6': 20000,
})
