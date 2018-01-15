#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class GameItemConfigure:
    def __init__(self, appId):
        self.appId = appId

    def get_game_configure(self):
        return TyContext.Configure.get_game_item_json(self.appId, 'game')

    def get_game_sdk_configure(self, sdk_name):
        appConfig = self.get_game_configure()
        return appConfig.get(sdk_name)

    def get_sdk_configure(self, channelName, packageName, sdkName):
        config = TyContext.Configure.get_game_item_json(self.appId, channelName)
        return config.get(packageName, {}).get(sdkName, {})

    def get_game_channel_configure(self, channelName):
        config = TyContext.Configure.get_game_item_json(self.appId, channelName)
        TyContext.ftlog.debug('GameItemConfigure,get config by channel', config)
        if not config:
            config = {}
        return config

    def get_game_channel_configure_by_package(self, sdk, package, channle=""):
        if not channle:
            channle = sdk
        config = self.get_game_channel_configure(channle) or {}
        return config.get(package).get(sdk) if config.get(package) else {}

    def get_game_channel_configure_by_primarykey(self, sdk, primaryKey, primaryValue, channel=""):
        if not channel:
            channle = sdk
        config = self.get_game_channel_configure(channel)
        for packageConfig in config.values():
            for package in packageConfig.values():
                TyContext.ftlog.debug('GameItemConfigure get sdkconfig', package)
                if package.get(primaryKey) == primaryValue:
                    return package
        return {}

    @classmethod
    def get_game_channel_configure_by_orderId(cls, platformOrderId, sdk=""):
        chargeKey = 'sdk.charge:' + platformOrderId
        chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
        if chargeInfo:
            chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
        if not chargeInfo:
            return {}
        appId = chargeInfo['appId']
        package = chargeInfo['packageName']
        chargeType = sdk if sdk else chargeInfo['chargeType']
        mainchannel = chargeInfo['clientId'].split('.')[-2] if chargeInfo['clientId'].split('.') else ""
        TyContext.ftlog.debug('GameItemConfigure,appId, package,mainchannel,chargetype', appId, package, mainchannel,
                              chargeType)
        return GameItemConfigure(appId).get_game_channel_configure_by_package(chargeType, package, mainchannel)
