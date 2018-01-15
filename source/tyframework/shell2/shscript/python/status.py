# -*- coding: utf-8 -*-

import os, json
from _helper_ import get_psef_pid_list, execute_redis_cmd_safe

def get_process_pid(prockey):
    cmd = 'ps -ef | grep "%s" | grep -v "grep" | grep -v "_stop_" | grep -v "_while1_" | awk \'{print $2}\'' % (prockey)
    pids = get_psef_pid_list(cmd)
    if len(pids) == 1 :
        return int(pids[0])
    return 0

def get_all_stimes(prockeys):
    prockey0 = prockeys[0]
    datas = prockey0.split(':')
    mkey = 'script.' + ':'.join(datas[0:3])
    stimes = execute_redis_cmd_safe(datas, 'hmget', mkey, prockeys)
    for x in xrange(len(stimes)) :
        st = stimes[x]
        if st != None:
            st = int(st)
        else:
            st = 0
        stimes[x] = st
    return stimes

def clean_all_startup_status(prockeys):
    prockey0 = prockeys[0]
    datas = prockey0.split(':')
    mkey = 'script.' + ':'.join(datas[0:3])
    execute_redis_cmd_safe(datas, 'delete', mkey)
    return 0

def get_startup_status(prockeys):    
    stimes = get_all_stimes(prockeys)
    status = []
    for x in xrange(len(prockeys)):
        prockey = prockeys[x]
        st = stimes[x]
        pid = get_process_pid(prockey)
        status.append([prockey, st, pid])

    return status

if __name__ == '__main__':
    action = os.sys.argv[1]
    prockeys = os.environ.get('PROCKEYS')
    prockeys = json.loads(prockeys)
    status = {}
    result = None
    if action == 'startup' :
        result = get_startup_status(prockeys)
    elif action == 'cleanall' :
        result = clean_all_startup_status(prockeys)

    status['action'] = action
    status['result'] = result
    status = json.dumps(status)
    print 'RESPONSE_JSON=' + status

