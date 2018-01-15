# -*- coding=utf-8 -*-

'''
全局锁的decorating
说明:
    全局锁,即系统内的唯一锁,跨越进程和物理机
使用方法示例:
    @global_lock_method(lock_name_head="global.user.modify_item", lock_name_tails=["gameid", "userid", "itemid"])
    def modify_item(self, gameid, userid, itemid, count, state):
        pass
    示例说明:
    lock_name_head : 全局锁的名字的开头, 以便区分不同的全局锁
    lock_name_tails : 全局的后缀的组成内容
    当调用时: modify_item(6, 10001, 20, 10, 1)时,
    实例中使用的全局锁为"global.user.modify_item:6:10001:20"
'''
from tyframework._private_.util.globallocker import global_lock_method

global_lock_method = global_lock_method
