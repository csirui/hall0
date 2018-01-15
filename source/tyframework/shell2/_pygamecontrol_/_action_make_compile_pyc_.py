# -*- coding: utf-8 -*-

import commands
from _main_helper_ import myfiles, mylog, myhelper

def action_make_compile_pyc(actparams):
    '''
    预编译所有的py文件到pyc，以便发现语法错误
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0
    service = params['service']

    # 编译文件
    mylog.log('开始预编译PY文件')
    compilepath = service['paths']['bin']

    makesosh = myfiles.find_py_files(compilepath, 'makeso.sh')
    for msh in makesosh :
        cmd = 'sh %s/%s' %(compilepath, msh)
        mylog.log('编译SO文件 :', msh)
        status, output = commands.getstatusoutput(cmd)
        if status != 0 :
            mylog.log('ERRROR !!', '工程so文件编译失败:', compilepath)
            mylog.log(output)
            return 0

    mylog.log('编译PY文件 :', compilepath)
    pyfiles = myfiles.find_py_files(compilepath, '.py', True)
    content = '\n'.join(pyfiles)
    # 生成编译文件
    cfilepath = '%s/c.py' % (compilepath)
    myfiles.write_file('', cfilepath, content)
    
    pypy = myhelper.get_env('PYPY_COMPILE', service['pypy'])
    cmd = 'export PYTHONPATH=%s; %s -tt %s' % (compilepath, pypy, cfilepath)
    status, output = commands.getstatusoutput(cmd)
    if status != 0 :
        mylog.log('ERRROR !!', '工程py文件编译失败:', compilepath)
        mylog.log(output)
        return 0
    commands.getstatusoutput('rm -fr ' + cfilepath)
    mylog.log('预编译PY文件成功！')
    return 1
