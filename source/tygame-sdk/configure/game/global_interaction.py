# -*- coding: utf-8 -*-

from pyscript._helper_config_ import add_global_item

add_global_item('beauty.certify.margin', {
                '6':{
                     'collect':'http://10.3.0.3/v1/dizhu/beautycert/deduct',
                     'back':'http://10.3.0.3/v1/dizhu/beautycert/return',
                     'reward':'http://10.3.0.3/v1/dizhu/beautycert/reward',
                },
                '8':{
                     'collect':'http://10.3.0.3/v1/texaspoker/beautycert/deduct',
                     'back':'http://10.3.0.3/v1/texaspoker/beautycert/return',
                     'reward':'http://10.3.0.3/v1/texaspoker/beautycert/reward',
                },
                })

add_global_item('newsnsid.reward.callback', {
#                 '6': 'http://10.3.0.3/v1/game/newsnsid',
                '7': 'http://10.3.0.3/v1/game/newsnsid',
                })
add_global_item('bindsnsid.reward.callback', {
                '6': 'http://10.3.0.3/v1/game/bindsnsid',
                '7': 'http://10.3.0.3/v1/game/bindsnsid',
                '8': 'http://10.3.0.3/v1/game/bindsnsid',
                '12': 'http://mania.shediao.com/v1/game/bindsnsid'
                })

add_global_item('bindphone.reward.callback', {
                '6': 'http://10.3.0.3/v1/dizhu/bindphone',
                })

add_global_item('forbidden.login.callback', {
                '6': 'http://10.3.0.18/v2/game/user/forcelogout',
                '7': 'http://10.3.0.3/v2/game/user/forcelogout',
                '8': 'http://10.3.0.18/v2/game/user/forcelogout',
                '12': 'http://mania.shediao.com/v2/game/user/forcelogout'
                })

add_global_item('push.server', 'http://10.3.13.16:8888')
add_global_item('push.server.new', 'http://121.201.7.106')
