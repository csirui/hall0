#! encoding=utf-8
from twisted.web.util import redirectTo

from tyframework.context import TyContext

__author__ = 'yuejianqiang'

import time


class ReportAppcoach:
    @classmethod
    def reportAppcoach(cls, params):
        sub_Publisher = params.get('sub_Publisher', "")
        click_id = params.get('click_id', '')
        android_id = params.get('android_id', '')
        google_aid = params.get('google_aid', "")
        ios_Idfa = params.get('ios_Idfa', "")
        mid = android_id if android_id else ios_Idfa.upper()
        if not mid:
            TyContext.ftlog.debug("ReportAppcoach,error,cannot find a key for redis")
            return
        rkey = 'appcoach:%s' % mid
        TyContext.ftlog.info("UNIVERSAL_LOG_APPCOACH", 'appcoach_params=', params)
        TyContext.RedisPayData.execute('HMSET', rkey,
                                       'sub_Publisher', sub_Publisher,
                                       'android_id', android_id,
                                       'google_aid', google_aid,
                                       'click_id', click_id,
                                       'ts', int(time.time()))
        httpreq = TyContext.RunHttp.get_request()
        appcoach_redirect_url = TyContext.Configure.get_global_item_json('appcoach_redirect_config', {})
        red_addr = appcoach_redirect_url.get("redirect_url", "https://itunes.apple.com/cn/app/id1090850101")
        if isinstance(red_addr, unicode):
            red_addr = red_addr.encode('utf-8')
        return redirectTo(red_addr, httpreq)

    def handle_register(self, userId, rparams):

        clientId = rparams.get('clientId', "")
        if clientId.startswith('IOS_'):
            mid = rparams.get('idfa', '')
        elif clientId.startswith('Android_'):
            mid = rparams.get('deviceId', '')
        else:
            return
        rkey = 'appcoach:%s' % mid
        click_id, sub_Publisher = TyContext.RedisPayData.execute('HMGET', rkey, 'click_id', 'sub_Publisher')
        if not click_id:
            TyContext.ftlog.error("ReportAppcoach,not the user from MobVista")
            return
        appcoach_redirect_url = TyContext.Configure.get_global_item_json('appcoach_redirect_config', {})
        source = appcoach_redirect_url.get("source", "tuyoo")
        utrack_token = appcoach_redirect_url.get("utrack-token", "9b89643544514af1af0f4fb159bb66cb")
        params = {
            'tid': click_id,
            'utrack-token': utrack_token,
            'source': source
        }
        TyContext.ftlog.info("ReportAppcoach,feedback_params=", params, 'regist_channel=', sub_Publisher,
                             "regist_uid=", userId)
        url = "http://ut.appcoachs.net/conversion"
        try:
            responseMsg, _ = TyContext.WebPage.webget(url, params, method_='GET')
            TyContext.ftlog.debug('ReportAppcoach feedback message', responseMsg)
        except Exception, e:
            TyContext.ftlog.debug("ReportAppcoach,feedback_exception=", e)
