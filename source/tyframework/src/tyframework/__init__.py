# -*- coding=utf-8 -*-

def tycontext_init(params):
    from context import TyContext
    TyContext.ftlog.info('tycontext_init in')

    TyContext.ftlog.open_stdout_logfile(TyContext.TYGlobal.path_log() + '/' + TyContext.TYGlobal.log_file_name())

    from tyframework._private_.dbredis.db_redis import DbRedis
    from tyframework._private_.dbredis.db_single import RedisSingle
    from tyframework._private_.dbredis.db_cluster import RedisCluster

    # 配置数据库
    redisParamsConfig = params['redis.config']
    TyContext.RedisConfig = RedisSingle(redisParamsConfig)

    # 配置中心
    #     TyContext.Configure.reload(10, False) # 有ftlog自身的_init_singleton_带动进行debug界别设定

    TyContext.RedisMix = RedisSingle(TyContext.TYGlobal.redis_mix(), 'redis.mix')
    TyContext.RedisLocker = RedisSingle(TyContext.TYGlobal.redis_locker(), 'redis.locker')
    TyContext.RedisAvatar = RedisSingle(TyContext.TYGlobal.redis_avatar(), 'redis.avatar')
    TyContext.RedisOnline = RedisCluster(TyContext.TYGlobal.redis_online(), 'redis.online')
    TyContext.RedisOnlineGeo = RedisSingle(TyContext.TYGlobal.redis_onlinegeo(), 'redis.onlinegeo')
    TyContext.RedisFriendMix = RedisSingle(TyContext.TYGlobal.redis_friend(), 'redis.friend')
    TyContext.RedisBiCount = RedisSingle(TyContext.TYGlobal.redis_bicount(), 'redis.bicount')
    TyContext.RedisForbidden = RedisSingle(TyContext.TYGlobal.redis_forbidden(), 'redis.forbidden')
    TyContext.RedisUserKeys = RedisSingle(TyContext.TYGlobal.redis_userkeys(), 'redis.userkeys')
    TyContext.RedisPayData = RedisSingle(TyContext.TYGlobal.redis_paydata(), 'redis.paydata')
    TyContext.RedisUser = RedisCluster(TyContext.TYGlobal.redis_datas(), 'redis.cluster')
    TyContext.RedisGame = TyContext.RedisUser
    TyContext.RedisUser.notifycahnged = 1
    TyContext.RedisTableData = RedisCluster(TyContext.TYGlobal.redis_table_datas(), 'redis.tabledatas')
    #     TyContext.RedisOnLineMix = RedisSingle(TyContext.TYGlobal.redis_onlinemix(), 'redis.onlinemix')

    TyContext.GData = params['gdata']

    TyContext._init_singleton_()

    TyContext.ftlog.info('tycontext_init out')
