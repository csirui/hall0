# -*- coding: utf-8 -*-

import os, time
from _helper_ import get_psef_pid_list, get_redis_conn

last_check_pid = None
def is_process_alive(prockey):
    global last_check_pid
    cmd = 'ps -ef | grep "%s" | grep -v "grep" | grep -v "_stop_" | grep -v "_while1_" | awk \'{print $2}\'' % (prockey)
    pids = get_psef_pid_list(cmd)
    print 'is_process_alive', prockey, pids
    if len(pids) == 1 :
        pid = pids[0]
        if last_check_pid == None :
            last_check_pid = pid
            return 1
        else:
            if last_check_pid != pid :
                return 0
            else:
                return 1
    return 0

def get_process_status(prockey, ctime, timeouts):
    datas = prockey.split(':')
    if len(datas) > 3 and len(datas[3]) > 0 :
        mkey = 'script.' + ':'.join(datas[0:3])
        rconn = get_redis_conn(datas)
        while 1 :
            stime = rconn.hget(mkey, prockey)
            if stime and int(stime) > ctime :
                print 'Check Start Up OK !!', prockey
                return 0
            else:
                if is_process_alive(prockey) :
                    if time.time() - ctime > timeouts :  # 超时
                        raise Exception('Error, Time Out.')
                    time.sleep(0.2)
                else:
                    raise Exception('Error, Process Missing.')
    else:
        raise Exception('Error, PROCKEY format error.')
    
if __name__ == '__main__':
    prockey = os.environ.get('PROCKEY')
    ctime = int(os.environ.get('SHELL_START_TIME'))
    timeouts = int(os.environ.get('ACTION_TIME_OUT'))
    get_process_status(prockey, ctime, timeouts)
