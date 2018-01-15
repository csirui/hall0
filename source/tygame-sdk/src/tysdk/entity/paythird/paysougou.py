#! encoding=utf-8

__author__ = 'yuejianqiang'

import hashlib

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPaySougou(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId'], }
        # m4399_keys = TyContext.Configure.get_global_item_json('m4399_keys', {})
        # packageName = chargeinfo['packageName']
        # appInfo = m4399_keys[packageName]
        # appKey = appInfo['appKey']
        # appSecret = appInfo['appSecret']
        # chargeKey = 'sdk.charge:m4399:%s' % chargeinfo['platformOrderId']
        # TyContext.RedisPayData.execute('HMSET', chargeKey, 'appKey', appKey, 'appSecret', appSecret)

    @classmethod
    def doCallback(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPaySougou->doCallback, rparams=', rparams)
        platformOrderId = rparams['appdata']
        amount1 = rparams['amount1']
        if not cls.check_sign(rparams):
            TyContext.ftlog.error('TuYouPaySougou.doCallback->ERROR, sign error !! rparam=', rparams)
            return 'ERR_200'
        isOk = PayHelper.callback_ok(platformOrderId, -1, rparams)
        if isOk:
            return 'OK'
        else:
            return 'ERR_500'

    @classmethod
    def check_sign(self, rparams):
        gid = rparams['gid']
        sougou_keys = TyContext.Configure.get_global_item_json('sougou_keys', {})
        paySecret = sougou_keys[gid]['paySecret']
        text = filter(lambda x: x[0] != 'auth', rparams.items())
        text.sort(lambda x, y: cmp(x[0], y[0]))
        text = ['%s=%s' % x for x in text]
        text.append(paySecret)
        myauth = hashlib.md5('&'.join(text)).hexdigest()
        if rparams['auth'] == myauth:
            return True
        return False
