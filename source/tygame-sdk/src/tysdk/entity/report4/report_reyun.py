#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'
import json


class ReportReyun:
    report_url = 'http://log.reyun.com'

    def handleRegister(self, **kwargs):
        clientId = kwargs.get('clientId', '')
        reyun_config = TyContext.Configure.get_global_item_json('reyun_config', {})
        if not clientId in reyun_config:
            return
        userId = kwargs.get('uid', kwargs.get('userId', 0))
        if not kwargs.get('idfa') and not kwargs.get('imei'):
            TyContext.RedisUserKeys.execute('SADD', 'ReyunUsers', str(userId))
        else:
            self.reportInstall(**kwargs)
            self.reportStartup(**kwargs)
            self.reportRegister(**kwargs)

    def reportInstall(self, **kwargs):
        clientId = kwargs.get('clientId', '')
        reyun_config = TyContext.Configure.get_global_item_json('reyun_config', {})
        if not clientId in reyun_config:
            return
        appId = reyun_config[clientId]['appId']
        channelId = reyun_config[clientId].get('channelId', '_default_')
        if clientId.startswith('Android_'):
            context = {'deviceid': kwargs.get('imei', ''),
                       'channelid': channelId,
                       'imei': kwargs.get('imei', ''),
                       'ip': kwargs.get('ip', '')}
        elif clientId.startswith('IOS_'):
            context = {'deviceid': kwargs.get('idfa', ''),
                       'channelid': channelId,
                       'idfa': kwargs.get('idfa', ''),
                       'idfv': kwargs.get('idfv', ''),
                       'ip': kwargs.get('ip', '')}
        else:
            return
        try:
            responseMsg, _ = TyContext.WebPage.webget('%s/receive/track/install' % self.report_url,
                                                      postdata_=json.dumps({'appid': appId, 'context': context}),
                                                      method_='POST',
                                                      headers_={'Content-Type': 'application/json'})
        except:
            TyContext.ftlog.exception()

    def reportStartup(self, **kwargs):
        clientId = kwargs.get('clientId', '')
        reyun_config = TyContext.Configure.get_global_item_json('reyun_config', {})
        if not clientId in reyun_config:
            return
        appId = reyun_config[clientId]['appId']
        channelId = reyun_config[clientId].get('channelId', '_default_')
        if clientId.startswith('Android_'):
            context = {'deviceid': kwargs.get('imei', ''),
                       'channelid': channelId,
                       'imei': kwargs.get('imei', ''),
                       'ip': kwargs.get('ip', '')}
        elif clientId.startswith('IOS_'):
            context = {'deviceid': kwargs.get('idfa', ''),
                       'channelid': channelId,
                       'idfa': kwargs.get('idfa', ''),
                       'idfv': kwargs.get('idfv', ''),
                       'ip': kwargs.get('ip', '')}
        else:
            return
        try:
            responseMsg, _ = TyContext.WebPage.webget('%s/receive/track/startup' % self.report_url,
                                                      postdata_=json.dumps({'appid': appId, 'context': context}),
                                                      method_='POST',
                                                      headers_={'Content-Type': 'application/json'})
        except:
            TyContext.ftlog.exception()

    def reportRegister(self, **kwargs):
        clientId = kwargs.get('clientId', '')
        userId = kwargs.get('uid', kwargs.get('userId', 0))
        reyun_config = TyContext.Configure.get_global_item_json('reyun_config', {})
        if not clientId in reyun_config:
            return
        appId = reyun_config[clientId]['appId']
        channelId = reyun_config[clientId].get('channelId', '_default_')
        if clientId.startswith('Android_'):
            context = {'deviceid': kwargs.get('imei', ''),
                       'channelid': channelId,
                       'imei': kwargs.get('imei', ''),
                       'ip': kwargs.get('ip', '')}
        elif clientId.startswith('IOS_'):
            context = {'deviceid': kwargs.get('idfa', ''),
                       'channelid': channelId,
                       'idfa': kwargs.get('idfa', ''),
                       'idfv': kwargs.get('idfv', ''),
                       'ip': kwargs.get('ip', '')}
        else:
            return
        try:
            responseMsg, _ = TyContext.WebPage.webget('%s/receive/track/register' % self.report_url,
                                                      postdata_=json.dumps(
                                                          {'appid': appId, 'who': userId, 'context': context}),
                                                      method_='POST',
                                                      headers_={'Content-Type': 'application/json'})
        except:
            TyContext.ftlog.exception()

    def reportLogin(self, **kwargs):
        clientId = kwargs.get('clientId', '')
        userId = kwargs.get('uid', kwargs.get('userId', 0))
        reyun_config = TyContext.Configure.get_global_item_json('reyun_config', {})
        if not clientId in reyun_config:
            return
        if TyContext.RedisUserKeys.execute('SREM', 'ReyunUsers', str(userId)):
            # TyContext.RedisUserKeys.execute('SREM', 'ReyunUsers', str(userId))
            self.reportInstall(**kwargs)
            self.reportStartup(**kwargs)
            self.reportRegister(**kwargs)
        appId = reyun_config[clientId]['appId']
        channelId = reyun_config[clientId].get('channelId', '_default_')
        if clientId.startswith('Android_'):
            context = {'deviceid': kwargs.get('imei', ''),
                       'channelid': channelId,
                       'imei': kwargs.get('imei', ''),
                       'ip': kwargs.get('ip', '')}
        elif clientId.startswith('IOS_'):
            context = {'deviceid': kwargs.get('idfa', ''),
                       'channelid': channelId,
                       'idfa': kwargs.get('idfa', ''),
                       'idfv': kwargs.get('idfv', ''),
                       'ip': kwargs.get('ip', '')}
        else:
            return
        try:
            responseMsg, _ = TyContext.WebPage.webget('%s/receive/track/loggedin' % self.report_url,
                                                      postdata_=json.dumps(
                                                          {'appid': appId, 'who': userId, 'context': context}),
                                                      method_='POST',
                                                      headers_={'Content-Type': 'application/json'})
        except:
            TyContext.ftlog.exception()

    def reportPayment(self, **kwargs):
        userId = kwargs.get('uid', kwargs.get('userId', 0))
        clientId = kwargs.get('clientId')
        idfa, ip, idfv, imei = TyContext.RedisUser.execute(userId, "HMGET", 'user:%s' % userId, 'idfa',
                                                           'sessionClientIP', 'idfv', 'imei')
        if idfa:
            kwargs['idfa'] = idfa
        if ip:
            kwargs['ip'] = ip
        if idfv:
            kwargs['idfv'] = idfv
        if imei:
            kwargs['imei'] = imei
        reyun_config = TyContext.Configure.get_global_item_json('reyun_config', {})
        if not clientId in reyun_config:
            return
        appId = reyun_config[clientId]['appId']
        channelId = reyun_config[clientId].get('channelId', '_default_')
        if clientId.startswith('Android_'):
            context = {'deviceid': kwargs.get('imei', ''),
                       'channelid': channelId,
                       'imei': kwargs.get('imei', ''),
                       'ip': kwargs.get('ip', '')}
        elif clientId.startswith('IOS_'):
            context = {'deviceid': kwargs.get('idfa', ''),
                       'channelid': channelId,
                       'idfa': kwargs.get('idfa', ''),
                       'idfv': kwargs.get('idfv', ''),
                       'ip': kwargs.get('ip', '')}
        else:
            return
        context['transactionid'] = kwargs.get('platformOrderId', '')
        context['paymenttype'] = kwargs.get('chargeType', '')
        context['currencytype'] = 'CNY'
        context['currencyamount'] = kwargs.get('chargedRmbs', 0.0)
        try:
            responseMsg, _ = TyContext.WebPage.webget('%s/receive/track/payment' % self.report_url,
                                                      postdata_=json.dumps(
                                                          {'appid': appId, 'who': userId, 'context': context}),
                                                      method_='POST',
                                                      headers_={'Content-Type': 'application/json'})
        except:
            TyContext.ftlog.exception()
