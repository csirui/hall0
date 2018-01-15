#! encoding=utf-8
from twisted.web.util import redirectTo

from tyframework.context import TyContext

__author__ = 'yuejianqiang'

import time


class ReportMobVista:
    @classmethod
    def reportMobiVista(cls, params):
        uuid = params.get('uuid', "")
        clickid = params.get('clickid', '')
        subchannel = params.get('subchannel', '')
        ip = params.get('ip', "")
        rkey = 'mobvista:%s' % ip
        if not uuid or not clickid:
            TyContext.ftlog.debug("ReportMobVista,params not correct!")
            return
        TyContext.ftlog.info("UNIVERSAL_LOG_MOBVISTA", 'mobivista_params=', params)
        TyContext.RedisPayData.execute('HMSET', rkey,
                                       'subchannel', subchannel,
                                       'clickid', clickid,
                                       'uuid', uuid,
                                       'ts', int(time.time()))

        httpreq = TyContext.RunHttp.get_request()
        mobvista_redirect_url = TyContext.Configure.get_global_item_json('mobvista_redirect_url', {})
        red_addr = mobvista_redirect_url.get(uuid, "https://itunes.apple.com/cn/app/id1090850101")
        if isinstance(red_addr, unicode):
            red_addr = red_addr.encode('utf-8')
        return redirectTo(red_addr, httpreq)

    def handle_register(self, userId, rparams):
        clientId = rparams.get('clientId', "")
        if clientId.startswith('IOS_'):
            platform = "ios"
        else:
            TyContext.ftlog.debug("ReportMobVista,platform is not IOS!")
            return
        clientIp = TyContext.RunHttp.get_client_ip()
        rkey = 'mobvista:%s' % clientIp
        subchannel, clickid, uuid = TyContext.RedisPayData.execute('HMGET', rkey,
                                                                   'subchannel',
                                                                   'clickid',
                                                                   'uuid')
        if not subchannel or not clickid or not uuid:
            TyContext.ftlog.debug("ReportMobVista,not the user from MobVista,clientIp->", clientIp)
            return
        params = {
            'mobvista_pl': platform,
            'mobvista_campuuid': uuid,
            'mobvista_ip': clientIp,
            'mobvista_clickid': clickid,
            'mobvista_gaid': rparams.get('idfa', ''),
            'mobvista_devid': rparams.get('idfa', '')
        }
        TyContext.ftlog.info("feedback_params=", params, "regist_channel=", subchannel,
                             'regist_uid=', userId)
        url = "http://stat.mobvista.com/install?"
        responseMsg, _ = TyContext.WebPage.webget(url, params, method_='GET')
        TyContext.ftlog.debug('ReportMobVista feedback message', responseMsg)
