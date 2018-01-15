# -*- coding: utf-8 -*-

import os, json, time, uuid
from _helper_ import get_redis_pipe, get_redis_conn, decode_objs_utf8

def dump_datas(data):
    if data == None :
        return 'none'
    if isinstance(data, (list, tuple, dict)) :
        return json.dumps(data, separators=(',', ':'))
    elif isinstance(data, (int, float, bool)) :
        return str(data)
    elif isinstance(data, (str, unicode)) :
        return data
    else:
        print  'Un Support Value Data Type !! type(data)=' + str(type(data))
        print  'data=' + repr(data)
        raise Exception('Un Support Value Data Type !! type(data)=' + str(type(data)))
    
def load_redis_file(redisaddr, cmdfile):
    
    print 'Load Redis Json File：', redisaddr, cmdfile
    
    jsonf = open(cmdfile)
    datas = json.load(jsonf)
    jsonf.close()
    
    delkeys = set()
    rpipe = get_redis_pipe(redisaddr)
    for data in datas :
        cmd = data[0].lower()
        if cmd == 'del' :
            cmd = 'delete'
        fun = getattr(rpipe, cmd)
        if cmd == 'delete' :
            fun(dump_datas(data[1]))
        elif cmd == 'set' :
            fun(dump_datas(data[1]), dump_datas(data[2]))
        elif cmd == 'hset' :
            fun(dump_datas(data[1]), dump_datas(data[2]), dump_datas(data[3]))
        elif cmd == 'hmset' :
            vdict = {}
            for k, v in data[2].items() :
                k = dump_datas(k)
                v = dump_datas(v)
                vdict[k] = v
            fun(dump_datas(data[1]), vdict)
        elif cmd == 'lpush' or cmd == 'rpush' :
            rkey = dump_datas(data[1])
            if rkey not in delkeys :
                delkeys.add(rkey)
                rpipe.delete(rkey)
            fun(rkey, dump_datas(data[2]))
        else:
            raise Exception('Un Support Redis Command ：' + cmd)

    t1 = time.time()
    rpipe.set('configitems.update.time', t1)
    datas = rpipe.execute()
    ut = int((time.time() - t1) * 1000)
    print 'Load Redis Json File OK ', ut , 'ms'


def load_redis_file_by_diff(redisaddr, cmdfile):
    print 'Load Redis Json File：', redisaddr, cmdfile
    
    # 取得当前的数据库数据
    rconn = get_redis_conn(redisaddr)
    oldkeys = []
    olddatas = {}
    cur = 0
    while cur >= 0 :
        datas = rconn.scan(cur, 'configitems:*', 999)
        cur = datas[0]
        ckeys = datas[1]
        if ckeys :
            oldkeys.extend(ckeys)
            oldvalues = rconn.mget(ckeys)

            for x in xrange(len(ckeys)) :
                print 'old->', ckeys[x], '=[', oldvalues[x], ']'
                olddatas[ckeys[x]] = oldvalues[x]

        if cur <= 0 :
            break
    
    # 取得要更新的配置文件数据
    newdatas = {}
    jsonf = open(cmdfile)
    datas = json.load(jsonf)
    jsonf.close()
    datas = decode_objs_utf8(datas)
    for data in datas :
        cmd = data[0].lower()
        if cmd == 'set' :
            newdatas[dump_datas(data[1])] = dump_datas(data[2])
        else:
            raise Exception('Un Support Redis Command ：' + repr(data))

    # REDIS中有, 配置文件中没有, 为要删除的键值
    delkeys = set(oldkeys) - set(newdatas.keys())
    for k in delkeys :
        if k.find('.number.map') > 0 :
            continue
        print 'del->', k
    # 检查要更新的键值
    updatas = {}
    for key, newvalue in newdatas.items() :
        oldvalue = olddatas.get(key, None)
        if newvalue != oldvalue :
            updatas[key] = newvalue
            #print 'update->', key, 'new=[', newvalue, '] old=[', oldvalue, ']'
    
    print 'redis update begin !!'
    rpipe = get_redis_pipe(redisaddr)
    for k in delkeys :
        if k.find('.number.map') > 0 :
            continue
        rpipe.delete(k)
    n = 0
    for k, v in updatas.items() :
        #print 'redis-set->', k, v
        rpipe.set(k, v)
        if n % 20 == 0 :
            rpipe.execute()
        n = n + 1
        pass
    rpipe.set('configitems:__uuid__', str(uuid.uuid4()).replace('-', ''))
    rpipe.execute()
    print 'redis update done !!'

    changekeys = set(delkeys)
    changekeys.update(set(updatas.keys()))
    changekeys.add('configitems:__uuid__')
    for k in changekeys :
        print 'changed->', k
#     raise Exception('test')
    cks = list(changekeys)
    return cks

if __name__ == '__main__':
    redisaddr = os.environ['CONFIGURE_RDIS_HOST']
    cmdfile = os.environ['CONFIGURE_JSON_FILE']
    load_redis_file(redisaddr, cmdfile)
