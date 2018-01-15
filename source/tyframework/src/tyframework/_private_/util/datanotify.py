# -*- coding=utf-8 -*-


def notify_game_server_on_data_change(userId, args):
    '''
    新老服务交互时, SDK与游戏服务交互时, 
    由于hall37使用了进程内数据缓存, 那么通过redis的发布订阅, 
    得到用户数据发生变化, 进而进行用户数据缓存的清理操作
    当老服务hall0完全停止时, 此方法也应该废弃
    但是SDK的数据变化还是需要通知到hall37
    共分8个渠道进行发布
   '''
    from tyframework.context import TyContext
    try:
        send = 0
        if args == None:
            send = 1
        elif len(args) > 2:
            cmd = args[0].upper()
            if cmd == 'HSET' or cmd == 'HMSET' or cmd == 'HDEL' or cmd == 'HINCRBY' or cmd == 'HINCRBYFLOAT' or cmd == 'HSETNX' \
                    or cmd == 'EVAL' or cmd == 'EVALSHA' or cmd == 'LPOP' or cmd == 'LPUSH' or cmd == 'BLPOP' or cmd == 'BRPOP' \
                    or cmd == 'BRPOPLPUSH' or cmd == 'LINSERT' or cmd == 'LPUSHX' or cmd == 'LREM' or cmd == 'LSET' \
                    or cmd == 'LREM' or cmd == 'LTRIM' or cmd == 'RPOP' or cmd == 'RPOPLPUSH' or cmd == 'RPUSH' or cmd == 'RPUSHX' \
                    or cmd == 'DEL' or cmd == 'EXPIRE' or cmd == 'EXPIREAT' or cmd == 'MOVE' or cmd == 'MIGRATE' or cmd == 'PERSIST' \
                    or cmd == 'PEXPIRE' or cmd == 'PEXPIREAT' or cmd == 'RENAME' or cmd == 'RENAMENX' or cmd == 'RESTORE' \
                    or cmd == 'SADD' or cmd == 'SINTER' or cmd == 'SINTERSTORE' or cmd == 'SMOVE' or cmd == 'SPOP' or cmd == 'SREM' \
                    or cmd == 'SUNION' or cmd == 'SUNIONSTORE' or cmd == 'ZADD' or cmd == 'ZINCRBY' or cmd == 'ZINTERSTORE' \
                    or cmd == 'ZREM' or cmd == 'ZREMRANGEBYSCORE' or cmd == 'ZREMRANGEBYRANK' or cmd == 'ZREMRANGEBYLEX' \
                    or cmd == 'ZUNIONSTORE' or cmd == 'APPEND' or cmd == 'BITOP' or cmd == 'BITPOS' or cmd == 'DECR' or cmd == 'DECRBY' \
                    or cmd == 'GETSET' or cmd == 'INCR' or cmd == 'INCRBY' or cmd == 'INCRBYFLOAT' or cmd == 'MSET' or cmd == 'MSETNX' \
                    or cmd == 'PSETEX' or cmd == 'SET' or cmd == 'SETBIT' or cmd == 'SETEX' or cmd == 'SETNX' or cmd == 'SETRANGE' \
                    or cmd == 'SETBIT' or cmd == 'SETBIT':
                send = 1
        if send:
            TyContext.ftlog.debug('datachange->', userId)
            TyContext.RedisMix.sendcmd('PUBLISH', 'userdatachange_' + str(userId % 16), userId)
    except:
        TyContext.ftlog.error()
