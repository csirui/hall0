# -*- coding=utf-8 -*-

def is_test_sdk_server():
    import os
    ret = 'TEST_SDK_SERVER' in os.environ
    from tyframework.context import TyContext
    TyContext.ftlog.info('TEST_SDK_SERVER', ret)
    return ret


def tygame_init():
    '''
    TyContext初始化完毕，网络监听之前，进行游戏的初始化(注意:此时无法进行网络通讯)
    '''
    from tyframework.context import TyContext
    TyContext.ftlog.info('tygame_init tysdk in')

    ptype = TyContext.TYGlobal.run_process_type()
    if ptype == TyContext.TYGlobal.RUN_TYPE_HTTP:
        sdkmode = TyContext.TYGlobal.run_process().get('subtype')
        if sdkmode == 'gateway':
            game_gateway_init()
        elif sdkmode == 'sdk':
            game_sdk_init()
        else:
            game_gateway_init()
            game_sdk_init()
    else:
        TyContext.ftlog.error('ERROR !! not know server process type !! ', ptype)

    TyContext.ftlog.info('tygame_init tysdk out')
    return [TyContext.TYGlobal.gameid()]


def game_gateway_init():
    from tyframework.context import TyContext
    TyContext.ftlog.info('game_gateway_init in')

    #     from tysdk.cmdcenter.httptimer import HttpSdkTimer
    #     TyContext.Cmds.add_timer(HttpSdkTimer)

    from tysdk.cmdcenter.httpgateway import HttpGateWay
    TyContext.RunHttp.add_executer(HttpGateWay)
    TyContext.ftlog.info('game_gateway_init out')


def init_subscription():
    from tyframework._private_.dbredis import txredisapi as redis
    class RedisListenerProtocol(redis.SubscriberProtocol):
        @classmethod
        def init_subscription(cls):
            # already connected or on connecting
            # if RedisListenerProtocol.connection_status != 0:
            #    return
            # start connection
            from tyframework.context import TyContext
            from twisted.internet.protocol import ClientCreator
            from twisted.internet import reactor
            params = TyContext.RedisConfig.address
            # RedisListenerProtocol.connection_status = 1
            TyContext.ftlog.debug("RedisListenerProtocol",
                                  'try to connect to redis server (%s:%s)' % (params['host'], params['port']))
            defer = ClientCreator(reactor, RedisListenerProtocol).connectTCP(params['host'], params['port'])
            defer.addErrback(lambda reason: reactor.callLater(5000, RedisListenerProtocol.init_subscription))

        def connectionMade(self):
            from tyframework.context import TyContext
            TyContext.ftlog.debug("RedisListenerProtocol", 'connection made')
            self.subscribe("configure")

        def messageReceived(self, pattern, channel, message):
            from tyframework.context import TyContext
            # print "pattern=%s, channel=%s message=%s" %(pattern, channel, message)
            TyContext.ftlog.debug("RedisListenerProtocol", 'reload configure [%s]' % message)
            TyContext.Configure.reload_cache_keys([message])

        def connectionLost(self, reason):
            # defer = ClientCreator(reactor, RedisListenerProtocol).connectTCP(params['host'], params['port'])
            # init_configure_subscription()
            # RedisListenerProtocol.connection_status = 0
            from tyframework.context import TyContext
            TyContext.ftlog.debug("RedisListenerProtocol", 'connection lost')
            RedisListenerProtocol.init_subscription()

    RedisListenerProtocol.init_subscription()


def game_sdk_init():
    from tyframework.context import TyContext

    TyContext.ftlog.info('game_sdk_init in')

    #     from tysdk.cmdcenter.httptimer import HttpSdkTimer
    #     TyContext.Cmds.add_timer(HttpSdkTimer)

    from tysdk.cmdcenter.httpuser import HttpUser
    TyContext.RunHttp.add_executer(HttpUser)

    from tysdk.cmdcenter.httpuserv3 import HttpUserV3
    TyContext.RunHttp.add_executer(HttpUserV3)

    from tysdk.cmdcenter.httpuserv4 import HttpUserV4
    TyContext.RunHttp.add_executer(HttpUserV4)

    from tysdk.cmdcenter.httpreportv4 import HttpReportV4
    TyContext.RunHttp.add_executer(HttpReportV4)

    from tysdk.cmdcenter.httpuserh5v3 import HttpUserH5V3
    TyContext.RunHttp.add_executer(HttpUserH5V3)

    from tysdk.cmdcenter.httppayh5v3 import HttpPayH5V3
    TyContext.RunHttp.add_executer(HttpPayH5V3)

    from tysdk.cmdcenter.httppayv1 import HttpPay
    TyContext.RunHttp.add_executer(HttpPay)

    from tysdk.cmdcenter.httppayv3 import HttpPayV3
    TyContext.RunHttp.add_executer(HttpPayV3)

    from tysdk.cmdcenter.httppayv4 import HttpPayV4
    TyContext.RunHttp.add_executer(HttpPayV4)

    from tysdk.cmdcenter.httpuserphotov3 import HttpUserPhotov3
    TyContext.RunHttp.add_executer(HttpUserPhotov3)

    from tysdk.cmdcenter.httpbeautycertifyv3 import HttpBeautyCertifyv3
    TyContext.RunHttp.add_executer(HttpBeautyCertifyv3)

    from tysdk.cmdcenter.httpavatarverifyv3 import HttpAvatarVerifyv3
    TyContext.RunHttp.add_executer(HttpAvatarVerifyv3)

    from tysdk.cmdcenter.httpsnsv3 import HttpSnsV3
    TyContext.RunHttp.add_executer(HttpSnsV3)

    from tysdk.cmdcenter.httpfriendv3 import HttpFriendV3
    TyContext.RunHttp.add_executer(HttpFriendV3)

    from tysdk.cmdcenter.httpupgradev3 import HttpUpgradev3
    TyContext.RunHttp.add_executer(HttpUpgradev3)

    from tysdk.cmdcenter.httppushv3 import HttpPushV3
    TyContext.RunHttp.add_executer(HttpPushV3)

    from tysdk.cmdcenter.httpmanagement import HttpManagement
    TyContext.RunHttp.add_executer(HttpManagement)

    from tysdk.cmdcenter.httpads import HttpAds
    TyContext.RunHttp.add_executer(HttpAds)

    from tysdk.cmdcenter.gamereg import HttpGameRegister
    TyContext.RunHttp.add_executer(HttpGameRegister)

    from tysdk.cmdcenter.testorder import HttpTestOrder
    TyContext.RunHttp.add_executer(HttpTestOrder)

    from tysdk.cmdcenter.httphello import HttpHello
    TyContext.RunHttp.add_executer(HttpHello)

    from tysdk.entity.ads.advertise import AdvertiseService
    AdvertiseService.on_init()

    from tysdk.entity.beautycertify3.beautycertify import BeautyCertifyService
    BeautyCertifyService.onInit()

    from tysdk.entity.beautycertify3.avatarverify import AvatarVerifyService
    AvatarVerifyService.onInit()

    from tysdk.entity.upgradev3.versionmanagerv3 import GameIncUpdateConfiger
    GameIncUpdateConfiger.instance()

    from tysdk.entity.upgradev3.versionmanagerv3 import GameIncUpdate
    GameIncUpdate.instance()

    from tysdk.entity.user_common.username import UsernameGenerator
    UsernameGenerator.createInstance()

    from tysdk.entity.duandai.channels import Channels
    Channels.init()

    init_subscription()

    TyContext.ftlog.info('game_sdk_init out')
