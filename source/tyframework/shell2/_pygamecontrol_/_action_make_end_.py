# -*- coding: utf-8 -*-

from _main_helper_ import myhelper

def action_make_end(actparams):
    '''
    结束进行有写操作的make命令集合
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0

    myhelper.save_last_output(params)
    return 1
