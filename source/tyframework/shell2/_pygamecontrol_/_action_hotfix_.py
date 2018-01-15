# -*- coding: utf-8 -*-

from _main_helper_ import myhelper, myfiles, mylog
from _main_tarfile_ import DIR_HOTFIX
from _main_push_ import push_dirs_to_all_server
from _main_hot_cmd_ import execute_hot_cmd

def action_hotfix(actparams):
    '''
    推送hotfix目录下的所有文件到各个服务器,并在各个服务器执行给出的文件
    '''
    mylog.log('准备HOTFIX')
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0
    service = params['service']

    # 创建所有的路径
    hotfixdir = service['paths']['hotfix']
    if not myfiles.make_path(hotfixdir) :
        return 0

    # 拷贝源文件到bin的install路径
    cpfpaths = []
    cptpaths = []
    for proj in service['projects'] :
        projpath = proj['path']
        cpfpaths.append('%s/hotfix' % (projpath))
        cptpaths.append(hotfixdir)
    
    if not myfiles.copy_files_all(cpfpaths, cptpaths) :
        return 0
    
    hotfixpy = actparams['hotfix']
    hotfixpy = hotfixdir + '/' + hotfixpy
    if not myfiles.file_exists(hotfixpy):
        mylog.error('没有找到HOTFIX文件', hotfixpy)
        return 0

    if not push_dirs_to_all_server(params, '推送HOTFIX代码', DIR_HOTFIX) :
        return 0

    return execute_hot_cmd(actparams, 'HOTFIX', 'exec_hotfix_py ' + hotfixpy)
