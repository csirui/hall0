# -*- coding: utf-8 -*-

import os, time, commands
from _helper_ import get_psef_pid_list, execute_redis_cmd_safe

def kill_process_(key1, key2):
    count = 1
    while 1 :
        cmd = 'ps -ef | grep "%s" | grep "%s" | grep -v "grep" | grep -v "_stop_" | grep -v "stop" | awk \'{print $2}\'' % (key1, key2)
        pids = get_psef_pid_list(cmd)
        if pids :
            print len(pids),
            if count > 40 :
                print 'Error !!'
                return 1
            force = ''
            if count > 20 :
                force = ' -9 '
            cmd = 'kill ' + force + ' '.join(pids)
            sts, outs = commands.getstatusoutput(cmd)
            print sts, outs
            time.sleep(0.1)
            count += 1
        else:
            return 0

def remove_run_status(prockey):
    datas = prockey.split(':')
    if len(datas) > 3 and len(datas[3]) > 0 :
        mkey = 'script.' + ''.join(datas[0:3])
        execute_redis_cmd_safe(datas, 'hdel', mkey, prockey)

def stop_process(prockey):
    print 'Kill  :', prockey

    # 先切掉while1守护进程
    if kill_process_(prockey, '_while1_') != 0 :
        raise Exception('Kill while1 process ERROR ' + prockey)
    
    # 先切掉pypy进程
    if kill_process_(prockey, prockey) != 0 :
        raise Exception('Kill pypy process ERROR ' + prockey)
    
    remove_run_status(prockey)
    print 'OK'

if __name__ == '__main__':
    prockey = os.environ.get('PROCKEY')
    stop_process(prockey)
