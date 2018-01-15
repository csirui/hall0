# -*- coding: utf-8 -*-
# 2014-060-03 18:00同步
from pyscript._helper_config_ import *

init_configure_env(1)

add_global_item('client.connect.timeouts', 35) # GAME和SDK定义重复
add_global_item('client.heart.beat.times', 6) # GAME和SDK定义重复
add_global_item('coupon.auto.confirm', 1)

add_global_item('login.forbidden.chip', 99999999999999)
add_global_item('login.forbidden.days', 7)
add_global_item('is_data_hall_mode' ,1)
add_global_item('clientid.waived.confirm', 0) #登录效验clientid白名单开关
add_global_item('client.log.report.confirm', 0) #客户端实时汇报开关
add_global_item('client.log.report.list', ['Android_3.73','Winpc_3.60','Winpc_3.601']) #按版本打开客户端上报

# 服务器log打印级别 2-debug 1-info （serve.serverId.debuglevel）
# 服务器是否打印网络的传输消息，只有在对应的打印级别为debug时才有效 0 -- 不打印  1 --- 打印
add_global_item('game_names', {
        '1' : u"扎金花",
        '2' : u"俄罗斯方块",
        '3' : u"象棋",
        '5' : u"斗牛",
        '6' : u"斗地主",
        '7' : u"麻将",
        '8' : u"德州",
        '9' : u"跑得快",
        '10' : u"斗牛",
        '12' : u"海外德州",
        '16' : u"百人牛牛",
        '17' : u"途游保皇",
        '18' : u"途游金三顺",
        '19' : u"跑狗",
        '20' : u"途游五子棋",
        '21' : u"途游跑胡子",
        '9996' : u"全局配置中心",
        '9998' : u"SDK及网关",
        '9999' : u"途游斗地主大厅",
})

from game_third import *
from game_tuyoo import *
from global_avatar import *
from global_cross import *
from global_friend import *
from global_interaction import *
from global_v3_products import *
from global_bugfix import *
from global_paytype import *
from global_thirdpay import *
from global_upgrade import *
from global_duandai import *
from global_misc import *
from global_tmp import *
from game_clientid import *
from global_paymentv4 import *

# db_set('poker:map.gaofangip', {
#     "policy": "none",
#     "namespace": {
#         "ip": "域名"
#     }
# })

finish_configure_env()
