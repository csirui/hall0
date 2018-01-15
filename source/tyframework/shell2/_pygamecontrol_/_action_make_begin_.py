# -*- coding: utf-8 -*-

import datetime
from _main_helper_ import myhelper

def action_make_begin(actparams):
    '''
    开始进行有写操作的make命令集合
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0
    params['_make_time_'] = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

    return 1
