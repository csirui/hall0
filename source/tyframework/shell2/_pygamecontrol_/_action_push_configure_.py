# -*- coding: utf-8 -*-

from _main_helper_ import myhelper
from _main_tarfile_ import DIR_MAKE_SCRIPT
from _main_push_ import push_dirs_to_all_server

def action_push_configure(actparams):
    '''
    推送编译输出的游戏配置文件到所有服务器，script目录
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0
    return push_dirs_to_all_server(params, '推送配置代码', DIR_MAKE_SCRIPT)
