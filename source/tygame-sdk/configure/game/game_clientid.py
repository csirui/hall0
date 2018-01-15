# -*- coding: utf-8 -*-
from pyscript._helper_config_ import *

# 这个配置, 转移到配置中心进行同步, 目前只同步了线上服务 104 101 3个主要服务
# add_global_item('clientid.number.map', {})

add_game_item_old(9998, 'game.branch', [
    {
        'http_game': "http://${VIRTUAL_HOST}:8010",
        'clientIds': ['*']
    }
]
                  )

add_game_item_old(9998, 'game.forbid.clientids', ["Android_2.1_tuyoo.tuyou.0.qq.hdanji",
                                                  "Android_2.0_tuyoo.tuyou.0.qq.hdanji"])

add_game_item_old(9998, 'game.forbid.msg', '您的客户端版本过低,请升级到最新版本.')

add_game_item_old(9998, 'http_gateway', {'default': 'http://125.39.220.70'
                                         })

add_game_item_old(9998, 'clientip_restricted_white', ['192.168.10.98',
                                                      ])
