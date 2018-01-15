# -*- coding=utf-8 -*-

import json

from tyframework.context import TyContext


class PlatformOrder(object):
    def __init__(self, orderid):
        self._orderid = orderid
        self._order = {}
        TyContext.RunMode.get_server_link(orderid)
        chargeKey = 'sdk.charge:' + orderid
        ret = TyContext.RedisPayData.execute('HGETALL', chargeKey)
        TyContext.ftlog.debug('PlatformOrder(%s) hgetall' % orderid, chargeKey, ret)
        if ret:
            for i in xrange(len(ret) / 2):
                self._order[ret[2 * i]] = ret[2 * i + 1]
        TyContext.ftlog.debug('PlatformOrder(%s) __init__ to' % orderid,
                              self._order)

    @property
    def state(self):
        try:
            return self._order['state']
        except Exception as e:
            TyContext.ftlog.error('PlatformOrder(%s)' % self._orderid, self._order, e)
            return None

    @property
    def userid(self):
        try:
            return self.chargeinfo['uid']
        except Exception as e:
            TyContext.ftlog.error('PlatformOrder(%s)' % self._orderid, self._order, e)
            return None

    @property
    def clientid(self):
        try:
            return self.chargeinfo['clientId']
        except Exception as e:
            TyContext.ftlog.error('PlatformOrder(%s)' % self._orderid, self._order, e)
            return None

    @property
    def buttonid(self):
        try:
            return self.chargeinfo['buttonId']
        except Exception as e:
            TyContext.ftlog.error('PlatformOrder(%s)' % self._orderid, self._order, e)
            return None

    @property
    def chargeinfo(self):
        try:
            if isinstance(self._order['charge'], basestring):
                self._order['charge'] = json.loads(self._order['charge'])
            return self._order['charge']
        except Exception as e:
            TyContext.ftlog.error('PlatformOrder(%s)' % self._orderid, self._order, e)
            return None
