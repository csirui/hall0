# -*- coding: utf-8 -*-

from _main_helper_ import mylog, myhelper
from _main_tarfile_ import tar_gzip_folders, DIR_ALL, PACK_TYPE_TAR_GZIP

def action_backup(actparams):
    '''
    备份当前的所有内容、工程文件、编译输出文件，测试模式不进行任何备份
    '''
    mylog.log('备份全部代码')
    params = myhelper.action_common_init(actparams, True)
    if not params :
        mylog.log('找不到上次的编译结果，无法备份')
        return 1
    
    backfile = tar_gzip_folders(params, PACK_TYPE_TAR_GZIP, DIR_ALL)
    if not backfile :
        mylog.error('备份失败')
        return 0
    mylog.log('备份成功')
    return 1

