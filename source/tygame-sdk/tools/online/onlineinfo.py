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

def show_room_infos():
    fp = get_redis_pipe('10.3.0.8:6379:2')
#      {1 : 't3card', 6 : 'tyddz', 7 : 'majiang', 8 : 'texas', 10 : 'dn'}
    gameids = [1, 6, 7, 8, 10]

    fp.hgetall('tyhall.1.count:room:onlines')
    fp.hgetall('tyhall.6.count:room:onlines')
    fp.hgetall('majiang.7.count:room:onlines')
    fp.hgetall('texas.8.count:room:onlines')
    fp.hgetall('tyhall.10.count:room:onlines')
    datas = fp.execute()
#    print datas
    for x in xrange(len(gameids)):
        gid = gameids[x]
        data = datas[x]
        infos = {}
        all = 0        
        for roomid, value in data.items() :
            if gid != 10 :
                roomid = str(roomid)[0:3]
            else:
                roomid = str(roomid)

            try:
                value = int(value.split('|')[0])
#                print gid, roomid, value
                all += value
                if roomid in infos :
                    infos[roomid] += value
                else:
                    infos[roomid] = value
            except:
                pass
        print gid, all, infos

if __name__ == '__main__':
    show_room_infos()
    
