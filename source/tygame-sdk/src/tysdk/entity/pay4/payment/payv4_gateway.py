#! encoding=utf-8
import hashlib

from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.payment.payv4_weixin import PayBaseV4

__author__ = 'yuejianqiang'


class PayGatewayV4(PayBaseV4):
    @classmethod
    def checkGatewaySign(cls, rparams):
        appId = rparams.get('appId')
        sign = rparams.get('sign')
        if not appId or not sign:
            return False
        appConfig = GameItemConfigure(appId).get_game_configure()
        appKey = appConfig['appKey']
        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        if sign != hashlib.md5('%s%s' % (text, appKey)).hexdigest():
            return False
        return True

    @classmethod
    def calcGatewaySign(cls, rparams):
        appId = rparams.get('appId')
        appConfig = GameItemConfigure(appId).get_game_configure()
        appKey = appConfig['appKey']
        params = filter(lambda x: x[0] != '' and x[0] != 'sign', rparams.items())
        params.sort(lambda x, y: cmp(x[0], y[0]))
        params = map(lambda x: '%s=%s' % x, params)
        text = '&'.join(params)
        return hashlib.md5('%s%s' % (text, appKey)).hexdigest()
