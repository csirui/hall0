# -*- coding: utf-8 -*-

import commands, json
from _main_helper_ import myfiles, mylog, myhelper

def action_make_configure(actparams, pypath=None):
    '''
    读取本地当前的配置文件内容，生成配置JSON文件，生成配置装载的脚本
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0

    service = params['service']

    # 每次执行配置文件时，使用__service__.json和__outputs__.json进行数据交换
    compilepath = service['paths']['bin']
    sfile = compilepath + '/__service__.json'
    myfiles.write_file('', sfile, json.dumps(service))
    
    ofile = compilepath + '/__outputs__.json'
    myfiles.write_file('', ofile, json.dumps({}))

    i = 1
    mcount = len(service['projects']) * 2
    for proj in service['projects'] :
        pyfile = proj['configure_py']
        mylog.log('装载游戏配置 [%d/%d] :' % (i, mcount), pyfile)
        i += 1
        basepy = myfiles.get_parent_dir(service['projects'][0]['configure_py'])
        if not __execute_game_config_py__(service, basepy, pyfile, sfile, ofile, pypath) :
            return 0

        pyfile = proj['configure_json']
        mylog.log('装载游戏配置 [%d/%d] :' % (i, mcount), pyfile)
        i += 1
        basepy = myfiles.get_parent_dir(service['projects'][0]['configure_json'])
        if not __execute_game_config_py__(service, basepy, pyfile, sfile, ofile, pypath) :
            return 0
    
    patchpy = myfiles.get_parent_dir(compilepath) + '/patch_config.py'
    if myfiles.file_exists(patchpy) :
        cmd = 'pypy ' + patchpy + ' ' + ofile
        mylog.log('执行游戏配置文件补丁:', cmd)
        status, output = commands.getstatusoutput(cmd)
        for l in output.split('\n'):
            mylog.log(l)
        if status != 0 :
            mylog.error('游戏配置文件补丁失败:', patchpy)
            mylog.error(status, output)
            return 0

    outputs = myfiles.read_json_file(ofile)
    cmdlist = []
    configuredatas = outputs.get('configuredatas', {})
    for k, v in configuredatas.items() :
        cmdlist.append(['set', k, v])

    if not __write_redis_config_script__(params, service, cmdlist) :
        return 0

    commands.getstatusoutput('rm -fr ' + sfile)
    commands.getstatusoutput('rm -fr ' + ofile)
    return 1

def __execute_game_config_py__(service, basepy, gamefile, sfile, ofile, extrapath=None):
    
    compilepath = service['paths']['bin']
    shtemplate = '''
#!/bin/bash
cd %s
pwd
export CONFIGURE_SERVICE_FILE=%s
export CONFIGURE_OUTPUTS_FILE=%s
export PYTHONPATH=%s:${PYTHONPATH}
export PYPY=%s
${PYPY} %s
exit $?
'''
    pypath = '%s:%s:%s' % (compilepath,
                           basepy,
                           myfiles.get_parent_dir(gamefile))
    if extrapath:
        pypath = '%s:%s' % (pypath, ':'.join(extrapath))
    content = shtemplate % (compilepath,
                            sfile,
                            ofile,
                            pypath,
                            myhelper.get_env('PYPY_COMPILE', service['pypy']),
                            gamefile
                            )
    shfile = compilepath + '/_temp_.sh'
    myfiles.write_file('', shfile, content)
    status, output = commands.getstatusoutput('sh ' + shfile)
    if status != 0 :
        mylog.error('游戏配置文件读取、运行失败:', gamefile)
        mylog.error(status, output)
        return 0
    commands.getstatusoutput('rm -fr ' + shfile)
    return 1

def __write_redis_config_script__(params, service, configuredata):

    redisfile = 'configure.json'
    mylog.log('保存游戏配置 :', redisfile)
    myfiles.write_file(service['paths']['script'], redisfile, configuredata)
    service['_configure_json_file_'] = redisfile

    _sh_template_ = '''
#!/bin/bash
export MAKE_TIME='%s'
export PATH_SCRIPT='%s'
export PATH_LOG='%s'
sh ${PATH_SCRIPT}/shscript/_hotcmd_.sh "$@"
exit $?
'''
    content = _sh_template_ % (params['_make_time_'],
                               service['paths']['script'],
                               service['paths']['log']
                               )
    outfile = 'hotcmd.sh'
    mylog.log('生成游戏热更新脚本 :' , outfile)
    myfiles.write_file(service['paths']['script'], outfile, content)
    service['_script_hotcmd_'] = outfile

    return 1
