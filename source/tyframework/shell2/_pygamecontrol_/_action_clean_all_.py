# -*- coding: utf-8 -*-

from _main_helper_ import myhelper, mylog, myssh
from _main_thread_ import mutil_thread_server_action
import commands

def action_clean_all(actparams):
    '''
    清空运行期的所有目录log、bireport
    '''
    mylog.log(mylog.wrap_color_cyan('清除所有机器的编译、日志内容'))
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0

    haserror = mutil_thread_server_action(params, thread_action_clean_all)
    if haserror :
        mylog.error('清除所有机器的编译、日志内容失败 !!')
        return 0

    mylog.log(mylog.wrap_color_cyan('清除所有机器的编译、日志内容完成'))
    return 1

def thread_action_clean_all(controls):
    '''
    这个方法运行再多线程当中
    '''
    result = 0
    outputs = ''
    try:
        server = controls['server']
        service = controls['service']
#         bufwebroot = service['paths']['webroot'].replace('/webroot', '/.webroot')
        allpaths = [
                    service['paths']['log'],
                    service['paths']['bireport'],
                    service['paths']['bin'],
                    service['paths']['script'],
                    service['paths']['webroot'],
                    service['paths']['backup'],
                    service['paths']['hotfix'],
#                     bufwebroot
        ]
        cmd = 'rm -fr ' + ' '.join(allpaths)
        
        # 停止时，停3次
        try:
            if server.get('localhost', 0) == 1 :
                status, outputs = commands.getstatusoutput(cmd)
            else:
                ip = server['sshhost']
                myssh.connect(ip, server['user'], server['pwd'], server['port'])
                status, outputs = myssh.executecmds(ip, cmd)
            
            if status == 0 :  # 成功
                result = 1
        except:
            mylog.exception()

        if status != 0 :  # 失败
            result = 2           

    except:
        result = 3  # 代码异常
        mylog.exception()

    controls['done'] = 1
    controls['result'] = result
    controls['outputs'] = outputs
