#! encoding=utf-8
from twisted.web.util import redirectTo

from tyframework.context import TyContext

__author__ = 'yuejianqiang'

import time


class ReportZPlay:
    @classmethod
    def reportZPlay2(cls, params):
        TyContext.ftlog.debug('ReportZPlay->reportZPlay2', '%s' % params)
        return 'success'

    @classmethod
    def reportZPlay(cls, params):
        adxid = params.get('adxid', '')
        imp_id = params.get('imp_id', '')
        did = params.get('did', '')
        appid = params.get('appid', '')
        TyContext.ftlog.debug('ReportZPlay->reportZPlay',
                              'adxid=%s imp_id=%s did=%s appid=%s' % (adxid, imp_id, did, appid))
        TyContext.RedisPayData.execute('HMSET', 'zplay:%s' % did,
                                       'adxid', adxid,
                                       'imp_id', imp_id,
                                       'did', did,
                                       'appid', appid,
                                       'ts', int(time.time()))

        httpreq = TyContext.RunHttp.get_request()
        zplay_redirect_url = TyContext.Configure.get_global_item_json('zplay_redirect_url', {})
        red_addr = zplay_redirect_url.get(appid, "https://itunes.apple.com/cn/app/id1090850101")
        if isinstance(red_addr, unicode):
            red_addr = red_addr.encode('utf-8')
        return redirectTo(red_addr, httpreq)
        # httpreq.redirect(red_addr.decode('utf-8'))
        # httpreq.finish()
        # hack: return 'redirected' so that execHtml will not handle the request
        # return 'redirected'

    @classmethod
    def feedbackZPlay(cls, userId, idfa):
        adxid, imp_id, did = TyContext.RedisPayData.execute('HMGET', 'zplay:%s' % idfa, 'adxid', 'imp_id', 'did')
        if adxid and imp_id and did:
            url = 'http://promote.zplay.cn/ad/postback/'
            rparams = {
                'chn': adxid,
                'imp': imp_id,
                'did': did,
            }
            responseMsg, _ = TyContext.WebPage.webget(url, rparams, method_='GET')
            TyContext.ftlog.debug('ReportZPlay->feedbackZPlay', 'uid=%s adxid=%s imp_id=%s did=%s response=%s' % (
            userId, adxid, imp_id, did, responseMsg))
