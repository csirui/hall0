# -*- coding: utf-8 -*-

from _main_helper_ import myhelper, myfiles

def action_clean_log(actparams):
    '''
    清空运行期的所有目录log、bireport
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0

    service = params['service']
    allpaths = [
                service['paths']['log'],
                service['paths']['bireport'],
    ]
    for mp in allpaths:
        if not myfiles.delete_path(mp) :
            return 0
    return 1
