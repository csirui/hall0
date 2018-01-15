# -*- coding: utf-8 -*-

import json, time, sys, commands
from _main_helper_ import myhelper, mylog, myfiles, myssh

def mutil_thread_server_action(params, fun_thread_main):
    stime = time.time()
    threads = []
    serivce = params['service']
    for server in serivce['servers'] :
        # done 0 - 线程运行中 1 － 线程结束
        # result 0 - 操作进行中 1 － 正常结束 2 － 异常结束
        controls = {'params' : params, 'service' : serivce, 'server' : server, 'done' : 0, 'result' : 0}
        t = myhelper.cread_thread(fun_thread_main, controls)
        controls['thread'] = t
        threads.append(controls)

    runchars = ['*', '-', '\\', '|', '/']
    isdoneall = 0
    resultall = 0
    wcount = 0

    while 1 :
        slines = []
        isdoneall = 0
        resultall = 0
        for worker in threads :
            srv = worker['server']
            isdone = worker.get('done', 0)
            result = worker.get('result', 0)
            percent = worker.get('percent', None)
            isdoneall += isdone
            resultall += result
            
            if result == 0:
                st = mylog.wrap_color_yellowd(runchars[wcount % len(runchars)])
            elif result == 1 :
                st = mylog.wrap_color_blue('O')
            else :
                st = mylog.wrap_color_red('E')

            if percent != None :
                if result == 0:
                    st = mylog.wrap_color_yellowd(percent) + st
                elif result == 1 :
                    st = mylog.wrap_color_blue(percent) + st
                else :
                    st = mylog.wrap_color_red(percent) + st

            slines.append(st + ' ')
        
        ptime = mylog.wrap_color_yellowd('%03d' % (time.time() - stime))
        lmsg = mylog.wrap_color_blue('PROGRESS       : ') + ptime + ' ' + ''.join(slines)
        sys.stdout.write('\r')
        sys.stdout.write(lmsg)
        if isdoneall == len(threads) :
            break
        time.sleep(0.2)
        wcount += 1

    sys.stdout.write('\n')
    
    haserror = 0
    for worker in threads :
        srv = worker['server']
        ip = srv['sshhost']
        result = worker.get('result', 0)
        if result == 1 :
            resultstr = 'OK'
        else:
            resultstr = 'ERROR'
            haserror = 1

        msg = '服务器 : %-16s : %s' % (ip, resultstr)
        if result == 1 :
            mylog.log(mylog.wrap_color_blue(msg))
        else:
            outputs = worker.get('outputs', '')
            mylog.error(msg, outputs)

        finalstatus = worker.get('finalstatus', None)
        if finalstatus :
            for line in finalstatus :
                mylog.log(line)
        
    return haserror

def get_status_json_datas(outputs):
    statusjson = None
    lines = outputs.split('\n')
    for line in lines :
#         mylog.log('line->', line)
        if line.find('RESPONSE_JSON=') >= 0 :
            statusjson = line[len('RESPONSE_JSON='):].strip()
            break
    datas = json.loads(statusjson)
    datas = myfiles.decode_objs_utf8(datas)
    return datas

def exec_index_script_on_first_server(params, script, script_param):
    service = params['service']
    servers = service['servers']
    server = None
    for s in servers :
        if s.get('localhost', 0) == 1 :
            server = s
            break
    if server == None :
        server = servers[0]

    scriptpath = service['paths']['script']
    if isinstance(script, int) :
        statussh = server['_scripts_'][script]
        cmd = '%s/%s/%s %s' % (scriptpath, server['sshhost'], statussh, script_param)
    else:
        cmd = '%s/%s %s' % (scriptpath, script, script_param)
    if server.get('localhost', 0) == 1 :
        status, outputs = commands.getstatusoutput(cmd)
    else:
        ip = server['sshhost']
        myssh.connect(ip, server['user'], server['pwd'], server['port'])
        status, outputs = myssh.executecmds(ip, cmd)
    return status, outputs
