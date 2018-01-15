# -*- coding: utf-8 -*-

import time, commands, sys
from _main_helper_ import mylog, myhelper, myssh, localrun
from _main_thread_ import mutil_thread_server_action
from _main_thread_ import exec_index_script_on_first_server
from _main_thread_ import get_status_json_datas

def action_start(actparams):
    '''
    服务整体全部重新启动
    '''
    mylog.log('准备启动服务')
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0
    
    if __action_start_clean_status__(params) :
        return 0

    mylog.log(mylog.wrap_color_cyan('开始启动服务'))

    haserror = mutil_thread_server_action(params, __thread_action_start__)
    if haserror :
        mylog.error('启动服务失败 !!')
        return 0

    mylog.log('启动服务完成')
    return 1

def __action_start_clean_status__(params):
    mylog.log('清除启动状态标志')
    status, outputs = exec_index_script_on_first_server(params, -3, 'cleanall')
    if status == 0 :
        datas = get_status_json_datas(outputs)
        if datas['result'] == 0 :
            mylog.log('清除启动状态标志成功')
            return 0
    mylog.error('清除启动状态标志失败 !!')
    mylog.error(outputs)
    return 1
    
def __thread_action_start__(controls):
    '''
    这个方法运行再多线程当中
    '''
    result = 0
    outputs = ''
    try:
        status, outputs = __thread_action_start_server__(controls)
        # print status, outputs
        if status == 0 :  # 启动成功
            result = 1
    except:
        result = 2  # 代码异常
        mylog.exception()

    controls['done'] = 1
    controls['result'] = result
    controls['outputs'] = outputs

def __thread_action_start_server__(controls):

    server = controls['server']
    service = controls['service']
    statussh = server['_scripts_'][-3]
    startsh = server['_scripts_'][-1]
    scriptpath = service['paths']['script']
    islocalhost = server.get('localhost', 0)
    controls['percent'] = '---%'

    ip = server['sshhost']
    if not islocalhost :
        myssh.connect(ip, server['user'], server['pwd'], server['port'])

    controls['percent'] = '--+%'

    stime = int(time.time())
    cmd = '%s/%s/%s allnohup > /tmp/popen_$$.log 2>&1 ' % (scriptpath, server['sshhost'], startsh)

    if islocalhost :
        status, outputs = localrun(cmd)
    else:
        status, outputs = myssh.executecmds(ip, cmd)
    if status != 0 :
        return 2, outputs
    
    controls['percent'] = '-++%'

    # 查询数据库中，各个进程的状态
    okcount = 0
    cmd = '%s/%s/%s startup' % (scriptpath, server['sshhost'], statussh)
    finalstatus = []
    errors = {}
    while 1 :
        if islocalhost :
            status, outputs = localrun(cmd)
        else:
            status, outputs = myssh.executecmds(ip, cmd)
        if status != 0 :
            return 2, outputs

        status = get_status_json_datas(outputs)

        process = status['result']
        finalstatus = []
        stop = 0
        okcount = 0
        errcount = 0
        for proc in process :
            prockey = proc[0]
            ptime = int(proc[1])
            pid = proc[2]
            if int(pid) > 0 :
                if ptime <= stime :
                    finalstatus.append(mylog.wrap_color_red('启动超时 ' + prockey))
                else:
                    okcount += 1
                    finalstatus.append(mylog.wrap_color_blue('启动成功 ' + prockey + ' ' + str(ptime - stime) + '秒'))
            else:
                errcount += 1
                msg = mylog.wrap_color_red('进程消失 ' + prockey)
                if prockey not in errors :
                    errors[prockey] = 1
                    sys.stdout.write('\n' + msg + '\n')
                finalstatus.append(msg)

        donecount = okcount + errcount
        if donecount != len(process) :
            p = int(float(okcount) / float(len(process)) * 100)
        else:
            p = 100
        controls['percent'] = '% 3d' % (p) + '%'
        
        # print ip, okcount, len(process), stime, stop
        if int(time.time()) - stime >= 240 :
            stop = 2

        if donecount == len(process) :
            if errcount > 0 :
                stop = 1
            else:
                stop = 10
            break
        
        if stop > 0 : 
            break

        time.sleep(0.2)

    controls['finalstatus'] = finalstatus

    if stop == 1 :
        return 2, '启动失败'
    
    if stop == 2 :
        return 3, '进程超时'

    controls['percent'] = '++++'
    return 0, '启动成功'
