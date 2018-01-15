# -*- coding=utf-8 -*-


from tyframework.context import TyContext

'''
交叉推广模块

'''


class Cross():
    # Android_2.63_360.360.0.360.1

    @classmethod
    def getAppList(cls, appId, clientId):
        config = TyContext.Configure.get_global_item_json('cross.config.applist')

        appId = str(appId)
        clientIdParts = clientId.split('_')
        channel = clientIdParts[2]
        channel_list = channel.split('.')
        if len(channel_list) > 3:
            main_channel = channel_list[-2]
        else:
            main_channel = channel
        # config = Cross.config
        applist = []
        if not config.has_key(appId):
            return applist
        appconfig_list = config[appId]
        for channel_config in reversed(appconfig_list):
            conf_channel = channel_config[0]
            conf_applist = channel_config[1]
            if main_channel == conf_channel or channel.endswith(conf_channel):
                applist = conf_applist
                break
        return applist

    @classmethod
    # cross:user_id -> target_app_id:source_app_id
    def downapp(cls, appId, down_app_id, clientId, userId, pkg, url):
        key = 'cross:' + str(userId)
        exist = TyContext.RedisUser.execute(userId, 'hget', key, str(down_app_id))
        if not exist:
            TyContext.RedisUser.execute(userId, 'hset', key, str(down_app_id), str(appId))
        TyContext.ftlog.info('[cross down]', 'appId=', appId, 'userId=', userId,
                             'clientId=', clientId, 'down_app_id=', down_app_id, 'pkg=', pkg, 'url=', url)

    @classmethod
    def reward(cls, userId, appId):
        key = 'cross:' + str(userId)
        source_app_id = TyContext.RedisUser.execute(userId, 'hget', key, str(appId))
        TyContext.ftlog.debug('source_app_id', source_app_id)
        if not source_app_id:
            return False
        source_app_id = str(source_app_id)
        key = 'cross_reward:' + str(userId)
        field = str(appId) + '-' + source_app_id
        is_reward = TyContext.RedisUser.execute(userId, 'hget', key, field)

        config_reward = TyContext.Configure.get_global_item_json('cross.config.reward')
        if is_reward or not config_reward.has_key(source_app_id):
            return False

        TyContext.RedisUser.execute(userId, 'hset', key, field, 1)
        chips = config_reward[source_app_id]
        TyContext.UserProps.incr_chip2(userId, source_app_id, chips, TyContext.ChipNotEnoughOpMode.NOOP,
                                       TyContext.BIEventId.UNKNOWN)
        TyContext.BiReport.gcoin('in.chip.smsinvite', appId, chips)

# Report.recoderGcoin( 'in.chip.smsinvite', appId, chips)
