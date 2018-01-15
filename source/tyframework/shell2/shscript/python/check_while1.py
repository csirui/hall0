# -*- coding: utf-8 -*-

import os, time
from _helper_ import get_psef_pid_list

def is_while1_alive(prockey):
    global last_check_pid
    cmd = 'ps -ef | grep "%s" | grep "_while1_" | grep -v "grep" | grep -v "_stop_" | grep -v "check_while1" | awk \'{print $2}\'' % (prockey)
    pids = get_psef_pid_list(cmd)
    print 'is_while1_alive', prockey, pids
    if len(pids) == 1 :
        return 1
    return 0

def get_process_status(allprockeys, timeouts):
    ct = int(time.time())
    while 1 :
        wcount = 0
        for prockey in allprockeys : 
            if is_while1_alive(prockey) :
                wcount += 1
        if wcount == len(allprockeys) :
            return 0
        else:
            if int(time.time()) - ct > timeouts :
                raise Exception('Check while1 process timeouts !')
        time.sleep(0.2)

if __name__ == '__main__':
    ct = int(time.time())
    print 'is_while1_alive begin', ct
    allprockeys = os.environ.get('ALL_PROCKEYS')
    allprockeys = allprockeys.split('|')
    timeouts = int(os.environ.get('ACTION_TIME_OUT'))
    get_process_status(allprockeys, timeouts)
    print 'is_while1_alive done', (int(time.time()) - ct)
