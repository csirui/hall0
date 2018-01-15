# -*- coding: utf-8 -*-

from _main_helper_ import myhelper, myfiles

def action_clean_bin(actparams):
    '''
    清空编译输出的所有目录bin、script、webroot
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0

    service = params['service']
    allpaths = [
                service['paths']['bin'],
                service['paths']['script'],
#                 service['paths']['webroot'],
                service['paths']['hotfix'],
    ]
    for mp in allpaths:
        if not myfiles.delete_path(mp) :
            return 0
    return 1
