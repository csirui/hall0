# -*- coding: utf-8 -*-

import commands
from _main_helper_ import mylog, myhelper, myssh
from _main_thread_ import mutil_thread_server_action

def action_stop(actparams):
    '''
    服务整体全部停止服务
    '''
    mylog.log(mylog.wrap_color_cyan('开始停止服务'))
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0

    haserror = mutil_thread_server_action(params, thread_action_stop)
    if haserror :
        mylog.error('停止服务失败 !!')
        return 0

    mylog.log('停止服务完成')
    return 1

def thread_action_stop(controls):
    '''
    这个方法运行再多线程当中
    '''
    result = 0
    outputs = ''
    try:
        server = controls['server']
        service = controls['service']
        stopsh = server['_scripts_'][-2]
        scriptpath = service['paths']['script']
        cmd = '%s/%s/%s' % (scriptpath, server['sshhost'], stopsh)
        # 停止时，停3次
        for _ in (2, 1, 0) :
            try:
                if server.get('localhost', 0) == 1 :
                    status, outputs = commands.getstatusoutput(cmd)
                else:
                    ip = server['sshhost']
                    myssh.connect(ip, server['user'], server['pwd'], server['port'])
                    status, outputs = myssh.executecmds(ip, cmd)
                
                if status == 0 :  # KILL成功
                    result = 1
                    break
            except:
                mylog.exception()

        if status != 0 :  # 停止失败
            result = 2           

    except:
        result = 3  # 代码异常
        mylog.exception()

    controls['done'] = 1
    controls['result'] = result
    controls['outputs'] = outputs
