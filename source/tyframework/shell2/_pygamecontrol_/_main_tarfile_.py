# -*- coding: utf-8 -*-

import os, commands, datetime
from _main_helper_ import mylog, myfiles

DIR_MAKE_BIN = 1
DIR_MAKE_SCRIPT = 1 << 1
DIR_MAKE_WEBROOT = 1 << 2
DIR_SOURCE = 1 << 3
DIR_HOTFIX = 1 << 4
DIR_ALL_MAKE = DIR_MAKE_BIN | DIR_MAKE_SCRIPT | DIR_MAKE_WEBROOT
DIR_ALL = DIR_ALL_MAKE | DIR_SOURCE

PACK_TYPE_TGZ = 1
PACK_TYPE_TAR = 2
PACK_TYPE_TAR_GZIP = 3

def tar_gzip_folders(params, pack_type, tar_dirs):

    service = params['service']
    root_path = myfiles.get_parent_dir(params['__source_path__'])

    tar_paths = []
    tar_prefix = 0
    if tar_dirs & DIR_MAKE_BIN :
        tar_prefix |= DIR_MAKE_BIN
        tar_paths.append(service['paths']['bin'])
    
    if tar_dirs & DIR_MAKE_SCRIPT :
        tar_prefix |= DIR_MAKE_SCRIPT
        tar_paths.append(service['paths']['script'])
    
    if tar_dirs & DIR_MAKE_WEBROOT :
        tar_prefix |= DIR_MAKE_WEBROOT
        tar_paths.append(service['paths']['webroot'])
    
    if tar_dirs & DIR_SOURCE :
        tar_prefix |= DIR_SOURCE
        projs = service['projects']
        for proj in projs :
            tar_paths.append(proj['path'])
        tar_paths.append(myfiles.get_parent_dir(params['__pyscript_path__']))

    if tar_dirs & DIR_HOTFIX :
        tar_prefix |= DIR_MAKE_WEBROOT
        tar_paths.append(service['paths']['hotfix'])

    if len(tar_paths) == 0 :
        raise Exception('没有指定要打包的目录!')

    if PACK_TYPE_TAR == pack_type or PACK_TYPE_TAR_GZIP == pack_type:
        ext_name = '.tar'
    elif PACK_TYPE_TGZ == pack_type :
        ext_name = '.tgz'
    else:
        raise Exception('打包类型错误')
    tartime = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    tgzfile = str(tar_prefix) + '-' + tartime + ext_name
    backpath = service['paths']['backup']
    myfiles.make_dirs(backpath)
    tgzfile = backpath + '/' + tgzfile
    if os.path.isfile(tgzfile) or os.path.isfile(tgzfile + '.gz'):
        mylog.log('打包成功 :' , tgzfile)
        return tgzfile

    allpaths = []
    for x in xrange(len(tar_paths)) :
        p = tar_paths[x]
        p = p.replace(root_path, '.')
        if p[0] == '/' :
            mylog.log('打包失败，原路径与当前路径不一致', tar_paths[x], root_path)
            return None
        allpaths.append(p)
    tarpath = ' '.join(allpaths)

    if PACK_TYPE_TAR == pack_type or PACK_TYPE_TAR_GZIP == pack_type :
        cmd = 'tar cf %s %s' % (tgzfile, tarpath)
    elif PACK_TYPE_TGZ == pack_type :
        cmd = 'tar cfz %s %s' % (tgzfile, tarpath)

    cmd = 'cd %s; %s' % (root_path, cmd)
    commands.getstatusoutput('rm -fr %s' % (tgzfile))
    status, output = commands.getstatusoutput(cmd)
    if status != 0 :
        mylog.error('打包失败!!', output)
        return None

    if not os.path.isfile(tgzfile) :
        mylog.error('打包失败!! 找不到文件 :' , tgzfile)
        return None
    
    if PACK_TYPE_TAR_GZIP == pack_type :
        commands.getstatusoutput('rm -fr %s.gz' % (tgzfile))
        cmd = 'nohup gzip %s >/dev/null 2>&1 &' % (tgzfile)
        os.popen(cmd)
        tgzfile += '.gz'

    mylog.log('打包成功 :', tgzfile)
    return tgzfile
