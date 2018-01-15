# -*- coding: utf-8 -*-

import commands, json, os, urllib, urllib2
from redis.client import StrictRedis

def get_psef_pid_list(cmdline):
    lines = commands.getoutput(cmdline)
    pidstrs = lines.strip().split('\n')
    pids = []
    for x in pidstrs :
        x = x.strip()
        if len(x) > 0 :
            pids.append(str(int(x)))
    return pids

def get_redis_conn(redisdef):
    if isinstance(redisdef, dict) :
        host = redisdef['host']
        port = int(redisdef['port'])
        dbid = int(redisdef['dbid'])
    elif isinstance(redisdef, (list, tuple)) :
        host = redisdef[0]
        port = int(redisdef[1])
        dbid = int(redisdef[2])
    else:
        datas = redisdef.split(':')
        host = datas[0]
        port = int(datas[1])
        dbid = int(datas[2])
    for x in (6, 5, 4, 3, 2, 1) :
        try:
            rconn = StrictRedis(host=host, port=port, db=dbid)
            return rconn
        except Exception, e:
            if x == 1 :
                raise e

def execute_redis_cmd_safe(redisdef, cmd, *params):
    for x in (6, 5, 4, 3, 2, 1) :
        try:
            conn = get_redis_conn(redisdef)
            fun = getattr(conn, cmd)
            datas = fun(*params)
            del conn
            return datas
        except Exception, e:
            if x == 1 :
                raise e

def get_redis_pipe(redisdef):
    return get_redis_conn(redisdef).pipeline()

def read_json_file(fpath, needdecode=False):
    fp = open(fpath, 'r')
    datas = json.load(fp)
    if needdecode :
        datas = decode_objs_utf8(datas)
    fp.close()
    return datas

def decode_objs_utf8(datas):
    if isinstance(datas, dict) :
        ndatas = {}
        for key, val in datas.items() :
            if isinstance(key, unicode) :
                key = key.encode('utf-8')
            ndatas[key] = decode_objs_utf8(val)
        return ndatas
    if isinstance(datas, list) :
        ndatas = []
        for val in datas :
            ndatas.append(decode_objs_utf8(val))
        return ndatas
    if isinstance(datas, unicode) :
        return datas.encode('utf-8')
    return datas

def load_control_datas() :
    spath = os.environ['PATH_SCRIPT']
    controlfile = spath + '/control.json'
    print 'Load Control File :', controlfile
    datas = read_json_file(controlfile, True)
    return datas

def webget(self, posturl, pdatas, parsejson=False):
    Headers = {'Content-type': 'application/x-www-form-urlencoded'}
    postData = urllib.urlencode(pdatas)
    request = urllib2.Request(url=posturl, data=postData, headers=Headers)
    response = urllib2.urlopen(request)
    retstr = response.read()
    if parsejson :
        retstr = json.loads(retstr)
    return retstr