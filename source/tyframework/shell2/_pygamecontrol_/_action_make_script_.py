# -*- coding: utf-8 -*-

import commands, json
from _main_helper_ import myfiles, mylog, myhelper

def action_make_script(actparams):
    '''
    生成所有的进程启动脚本
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0
    service = params['service']
    # 生成启动脚本

    process = service['process']
    srvids = {}
    for proc in process :
        if not proc['server'] in srvids :
            srvids[proc['server']] = []
        srvids[proc['server']].append(proc)

    servermap = {}
    servers = service['servers']
    for srv in servers :
        servermap[srv['id']] = srv
    
    allprocids = []
    for srvid in srvids :
        server = servermap[srvid]
        process = srvids[srvid]
        servershnames = []
        serverprocid = []
        if not __make_output_script__(params, service, server, process, servershnames, serverprocid) :
            return 0
        server['_scripts_'] = servershnames
        server['_procids_'] = serverprocid
        allprocids.extend(serverprocid)

    service['_allprocids_'] = allprocids
    commands.getoutput('chmod -R +x %s/*' % (service['paths']['script']))

    return 1

def __make_output_script__(params, service, server, process, servershnames, serverprocid):

    def _sort_process_(p1, p2):
        vs = {'game':1, 'account':2, 'entity' : 3, 'heart': 4, 'quick': 5, 'conn': 6, 'http': 7, 'robot' : 8, }
        t1 = vs[p1['type']]
        t2 = vs[p2['type']]
        if t1 == t2 :
            return 0
        if t1 > t2 :
            return 1
        return -1
    process.sort(_sort_process_)

    sshhost = server['sshhost']
    psidbase = service['prockey']
    
    mylog.log('生成服务器脚本 :', sshhost)

    basepath = service['paths']['script']
    basepath = basepath + '/' + sshhost
    myfiles.make_path(basepath, True)

    shnames = []
    myprocids = []
    cpucount = server.get('cpucount', 0)
    if cpucount > 1 :
        cpucount = cpucount - 1  #  cpu0始终不进行绑定，留给系统进行处理信息
    
    binpath = service['paths']['bin']
    mainpy = 'tyframework/service.py'
    if not myfiles.file_exists(binpath + '/' + mainpy) :
        mainpy = 'tyframework/server.py'
    
    if myfiles.file_exists(binpath + '/' + mainpy + 'c') :
        mainpy += 'c'
    
    for x in xrange(len(process)) :
        proce = process[x]
        ptype = proce['type'][0:4]

        if cpucount > 0 :
            taskset = ' taskset -c %d ' % ((x % cpucount) + 1)
        else:
            taskset = ''

        basefilename = ptype + '-' + service['name'] + '-' + str(service['id']) + '-' + '%05d' % (proce['id'])
        prockey = psidbase + basefilename
        proce['key'] = prockey

        serverprocid.append(prockey)
        myprocids.append(prockey)
        
        shname = basefilename + '.sh'
        shnames.append(shname)
        shscript = '''
#!/bin/bash
# SERVICE FILE=%s
export MAKE_TIME='%s'
export PYPY='%s'
export PATH_SCRIPT='%s'
export PATH_LOG='%s'
export PATH_WEBROOT='%s'
export PYTHONPATH='%s'
export PROCKEY='%s'
export PROCCLASS='%s'
export PROCLOG='%s'
export HOOKPROCESS='%s'
export TASKSET='%s'
sh ${PATH_SCRIPT}/shscript/_start_.sh
''' % (
        service['_servicefile_'],
        params['_make_time_'],
        service['pypy'],
        service['paths']['script'],
        service['paths']['log'],
        service['paths']['webroot'],
        service['paths']['bin'],
        prockey ,
        mainpy,
        basefilename + '.log',
        service['hook'],
        taskset
    )
        
        myfiles.write_file(basepath, shname, shscript)
        servershnames.append(shname)

    # 生成获取状态的脚本
    allname = service['name'] + '-all.sh'
    
    shcontent = '''
#!/bin/bash
# SERVICE FILE=%s
export MAKE_TIME='%s'
export PYPY='%s'
export PATH_SCRIPT='%s'
export PATH_LOG='%s'
export PROCKEYS='%s'
sh ${PATH_SCRIPT}/shscript/_status_.sh "$@"
''' % (
        service['_servicefile_'],
        params['_make_time_'],
        service['pypy'],
        service['paths']['script'],
        service['paths']['log'],
        json.dumps(serverprocid)
    )
    shname = 'status-' + allname
    myfiles.write_file(basepath, shname, shcontent)
    servershnames.append(shname)

    # 生成停止全部的脚本
    allname = service['name'] + '-all.sh'
    
    shcontent = '''
#!/bin/bash
# SERVICE FILE=%s
export MAKE_TIME='%s'
export PYPY='%s'
export PATH_SCRIPT='%s'
export PATH_LOG='%s'
export PROCKEY='%s'
sh ${PATH_SCRIPT}/shscript/_stop_.sh
''' % (
        service['_servicefile_'],
        params['_make_time_'],
        service['pypy'],
        service['paths']['script'],
        service['paths']['log'],
        psidbase
    )
    shname = 'kill-' + allname
    myfiles.write_file(basepath, shname, shcontent)
    servershnames.append(shname)
    
    # 生成启动全部的脚本
    lines_remote = []
    lines_local = []
    for shname in shnames :
        lines_remote.append('nohup ${SHELL_FOLDER}/%s >>/tmp/_start_$$.log 2>&1 &' % (shname))
        lines_local.append('${SHELL_FOLDER}/%s' % (shname))

    shcontent = '''
#!/bin/bash
# SERVICE FILE=%s
export MAKE_TIME='%s'
export PYPY='%s'
export SHELL_FOLDER=$(cd `dirname ${0}`; pwd)
export PATH_SCRIPT='%s'
export PATH_LOG='%s'
export PROCKEY='%s'
export ALLNOHUP=${1}
if [ "${ALLNOHUP}" = "allnohup" ] 
then
export ALL_PROCKEYS='%s'
%s
sh ${PATH_SCRIPT}/shscript/_check_while1_.sh
else
%s
fi
''' % (
        service['_servicefile_'],
        params['_make_time_'],
        service['pypy'],
        service['paths']['script'],
        service['paths']['log'],
        psidbase,
        '|'.join(myprocids),
        '\n'.join(lines_remote),
        '\n'.join(lines_local)
    )
    shname = 'start-' + allname
    myfiles.write_file(basepath, shname, shcontent)
    servershnames.append(shname)

    return 1

