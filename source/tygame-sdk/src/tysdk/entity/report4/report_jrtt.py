#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class ReportJRTT:
    @classmethod
    def reportIDFA(cls, params):
        adid = params.get('adid', '')
        cid = params.get('cid', '')
        idfa = params.get('idfa', '')
        mac = params.get('mac', '')
        os = params.get('os', '')
        timestamp = params.get('timestamp', '')
        TyContext.ftlog.debug('ReportJRTT->reportJRTT', 'adid=%s cid=%s idfa=%s mac=%s os=%s timestamp=%s' % (
        adid, cid, idfa, mac, os, timestamp))
        TyContext.RedisPayData.execute('HMSET', 'jrtt:%s' % idfa,
                                       'idfa', idfa,
                                       'adid', adid,
                                       'cid', cid,
                                       'mac', mac,
                                       'os', os,
                                       'timestamp', timestamp)
        return 'success'

    @classmethod
    def feedbackIDFA(cls, userId, idfa):
        adid, cid, idfa, mac, os, timestamp = TyContext.RedisPayData.execute('HMGET', 'jrtt:%s' % idfa, 'adid', 'cid',
                                                                             'idfa', 'mac', 'os', 'timestamp')
        if adid and idfa and cid:
            # url = 'http://promote.zplay.cn/ad/postback/'
            # rparams = {
            #    'chn': adxid,
            #    'imp': imp_id,
            #    'did': did,
            # }
            # responseMsg, _ = TyContext.WebPage.webget(url, rparams, method_ = 'GET')
            TyContext.ftlog.debug('ReportJRTT->feedbackIDFA',
                                  'uid=%s adid=%s cid=%s idfa=%s mac=%s os=%s timestamp=%s' % (
                                      userId, adid, cid, idfa, mac, os, timestamp))
