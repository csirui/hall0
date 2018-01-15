# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class PayCodes(object):
    def __init__(self, clientid):
        self._paycodes = TyContext.Configure.get_global_item_json(
            'paycodes', clientid=clientid)
        TyContext.ftlog.debug('PayCodes(%s) __init__ to' % clientid,
                              self._paycodes)
        if not self._paycodes:
            TyContext.ftlog.error('PayCodes(%s) can not get config' % clientid)
            self._paycodes = {}

    @property
    def appids(self):
        appids = {}
        for paytype in self._paycodes:
            appids[paytype] = self._paycodes[paytype]['appid']
        return appids

    def get_appkey(self, paytype):
        try:
            return self._paycodes[paytype]['appkey']
        except:
            return ''
