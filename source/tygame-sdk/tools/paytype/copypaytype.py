# -*- coding: utf-8 -*-

import sys, redis, time
import os

def get_redis_pipe(redisdef):
    if isinstance(redisdef, dict) :
        host = redisdef['host']
        port = int(redisdef['port'])
        dbid = int(redisdef['dbid'])
    else:
        datas = redisdef.split(':')
        host = datas[0]
        port = int(datas[1])
        dbid = int(datas[2])
        
    rconn = redis.StrictRedis(host=host, port=port, db=dbid)
    rpipe = rconn.pipeline()
    return rpipe

def copy_pay_type(fromredis, toredis):
    print 'copy_pay_type fromredis=', fromredis
    fp = get_redis_pipe(fromredis)
    print 'copy_pay_type toredis=', toredis
    tp = get_redis_pipe(toredis)
    fp.keys('paytype:*')
    pkeys = fp.execute()[0]
    datas = {}
    for pkey in pkeys :
        print 'pay key->', pkey
        fp.hgetall(pkey)
        pdatas = fp.execute()[0]
        datas[pkey] = pdatas
        tp.hmset(pkey, pdatas)
        tp.execute()

if __name__ == '__main__':
    fromredis = sys.argv[1]
    toredis = sys.argv[2]
    copy_pay_type(fromredis, toredis)
    