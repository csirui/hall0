# -*- coding: utf-8 -*-

import os, json, time, socket
from _helper_ import load_control_datas, get_redis_pipe
from _configure_ import *

class UdpSender(object):
    
    def __init__(self):
        rsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rsock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        rsock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65536)
        rsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
        rsock.settimeout(0.01)
        self.rsock = rsock
        self.dlist = []

    def send_udp(self, message, ip, port):
        self.rsock.sendto(message, (ip, port))
        self.recvdata()

    def recvdata(self):
        try:
            datas = self.rsock.recv(4096)
            if datas.find('{') >= 0 :
                datas = datas[datas.find('{'):]
                while datas[-1] == '\x00' or  datas[-1] == '\n' or  datas[-1] == '\r':
                    datas = datas[:-1]
            print int(time.time()), 'hotcmd recvdata', datas
            data = json.loads(datas)
            self.dlist.append(data)
        except Exception, e:
            print e
        return None

def query_hotcmd_on_all_server(params, cmdparams):

    servers = {}
    for srv in params['service']['servers'] :
        servers[srv['id']] = srv

    results = {}
    request = {}
    udp = UdpSender()
    ct = int(time.time())
    message = {'cmd':'_server_hot_cmd_', 'ct' : ct, 'params' : cmdparams}
    message = json.dumps(message, separators=(',', ':'))

    for proc in params['service']['process'] :
        ip = servers[proc['server']]['intrant']
        udp.send_udp(message, ip, proc['udp'])
        request[proc['key']] = 1
    print int(time.time()), 'keys :', request

    while len(request) > len(udp.dlist) and time.time() - ct < 60 :  # 60秒超时
        for _ in xrange(len(request) - len(udp.dlist)) :
            udp.recvdata()

    for datas in udp.dlist :
        prockey = datas.get('prockey', '')
        if prockey in request :
            del request[prockey]
            results[prockey] = datas

    for prockey in request :
        results[prockey] = {'result' : {'ok' : 0},
                            'error' : { 'info' : 'HotCmd Execute TimeOut 60s !!', 'code' : 1}}
    return results

def reset_service_configure(redisaddr, service):
    rpipe = get_redis_pipe(redisaddr)
    srvkey = 'service.configure.' + str(service['name']) + '.' + str(service['id'])
    rpipe.set(srvkey, json.dumps(service))
    rpipe.execute()

def main():
    action = os.sys.argv[1]
    actparams = {'action' : action}
    srvresults = None
    result = 0

    params = load_control_datas()
    service = params['service']
    if action == 'reload_configure_json' :
        redisaddr = service['redis']['config']
        redisfile = service['paths']['script'] + '/' + service['_configure_json_file_']
        changedlist = load_redis_file_by_diff(redisaddr, redisfile)
        actparams['changedlist'] = changedlist
        srvresults = query_hotcmd_on_all_server(params, actparams)
        reset_service_configure(redisaddr, service)

    elif action == 'install_configure_json' :
        redisaddr = service['redis']['config']
        redisfile = service['paths']['script'] + '/' + service['_configure_json_file_']
        load_redis_file_by_diff(redisaddr, redisfile)
        reset_service_configure(redisaddr, service)
        srvresults = {}

    elif action == 'exec_hotfix_py' :
        pyfile = os.sys.argv[2]
        actparams['pyfile'] = pyfile
        srvresults = query_hotcmd_on_all_server(params, actparams)

    else:
        result = 1
    outputs = {'result' : 0, 'process' : srvresults}
    outputs = json.dumps(outputs)
    print 'RESPONSE_JSON=' + outputs

if __name__ == '__main__':
    main()
