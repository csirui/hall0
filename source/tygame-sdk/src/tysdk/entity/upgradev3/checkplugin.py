# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class TuYouCheckPlugin(object):
    @classmethod
    def plugin_info(cls, pluginInfo):
        pluginInfo = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouCheckPlugin->plugin_info', pluginInfo)

        if 'clientId' in pluginInfo and pluginInfo['clientId']:
            pluginConfig = TyContext.Configure.get_global_item_json(pluginInfo['clientId'], {})
        else:
            TyContext.ftlog.error('TuYouCheckPlugin->plugin_info no params clientId')
            return 'fail'

        if pluginConfig:
            return pluginConfig
        else:
            TyContext.ftlog.error('TuYouCheckPlugin->plugin_info no pluginConfig')
            return 'fail'
