# -*- coding: utf-8 -*-

from _main_helper_ import myhelper, myfiles


def action_make_copy_source(actparams):
    '''
    拷贝源代码工程的etc、src、src-robot、webroot到编译输出目录，按照配置文件的工程列表进行顺序覆盖拷贝
    '''
    params = myhelper.action_common_init(actparams)
    if not params:
        return 0
    service = params['service']

    # 创建所有的路径
    allpaths = service['paths']
    for mp in allpaths:
        if not myfiles.make_path(allpaths[mp]):
            return 0

    # 拷贝源文件到bin的install路径
    compilepath = service['paths']['bin']
    webroot = service['paths']['webroot']

    cpfpaths = ['%s/shscript' % (params['__pyscript_path__'])]
    cptpaths = [service['paths']['script'] + '/shscript']

    for proj in service['projects']:
        projpath = proj['path']
        cpfpaths.append('%s/etc' % (projpath))
        cpfpaths.append('%s/src' % (projpath))
        cpfpaths.append('%s/src-robot' % (projpath))
        cpfpaths.append('%s/webroot' % (projpath))

        cptpaths.append(compilepath)
        cptpaths.append(compilepath)
        cptpaths.append(compilepath)
        cptpaths.append(webroot)

    if not myfiles.link_files_all(cpfpaths, cptpaths):
        return 0
    if service['corporation'] == 'momo':
        myfiles.delete_path(webroot + '/8')
        myfiles.delete_path(webroot + '/block')
        myfiles.delete_path(webroot + '/chinesechess')
        myfiles.delete_path(webroot + '/dizhu')
        myfiles.delete_path(webroot + '/dizhu2')
        myfiles.delete_path(webroot + '/douniu')
        myfiles.delete_path(webroot + '/douniu2')
        myfiles.delete_path(webroot + '/gomoku')
        myfiles.delete_path(webroot + '/scmahjong')
        myfiles.delete_path(webroot + '/scmahjong2')
        myfiles.delete_path(webroot + '/sdk')
        myfiles.delete_path(webroot + '/t3card2')
        myfiles.delete_path(webroot + '/t3flush')
        myfiles.delete_path(webroot + '/texas')
        myfiles.delete_path(webroot + '/hall6')

    return 1
