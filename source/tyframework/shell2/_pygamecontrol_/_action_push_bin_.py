# -*- coding: utf-8 -*-

from _main_helper_ import myhelper
from _main_tarfile_ import DIR_ALL_MAKE
from _main_push_ import push_dirs_to_all_server

def action_push_bin(actparams):
    '''
    推动所有的编译输出文件到所有服务器，bin、script、webroot目录
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0
    return push_dirs_to_all_server(params, '推送编译代码', DIR_ALL_MAKE)
