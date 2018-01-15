# -*- coding=utf-8 -*-

import json
from hashlib import md5
from urllib import quote, urlencode

from tyframework.context import TyContext
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.pay4.payment.payv4_callback import TuyouPayCallBackV4


class PayHelperV4:
    TRADE_FINISHED = 'TRADE_FINISHED'
    TRADE_FINISHED_ERROR = 'TRADE_FINISHED_ERROR'

    @classmethod
    def set_order_mobile(self, orderPlatformId, mobile, version='v3'):
        if not mobile:
            return
        if version == 'v2':
            orderkey = 'platformOrder:' + str(orderPlatformId)
            field = 'PAY_STATE_CHARGE'
        else:
            orderkey = 'sdk.charge:' + str(orderPlatformId)
            field = 'charge'
        TyContext.RunMode.get_server_link(orderPlatformId)
        chargeinfo = TyContext.RedisPayData.execute('HGET', orderkey, field)
        try:
            chargeinfo = json.loads(chargeinfo)
            chargeinfo['vouchMobile'] = mobile
        except Exception as e:
            TyContext.ftlog.info('PayHelper->set mobile exception', e,
                                 'orderPlatformId=', orderPlatformId, 'mobile=', mobile)
            return
        TyContext.RedisPayData.execute('HSET', orderkey, field, json.dumps(chargeinfo))

    @classmethod
    def callback_ok(cls, platformOrderId, total_fee, rparam):
        total_fee = float(total_fee)
        TyContext.RunMode.get_server_link(platformOrderId)
        ret = TuyouPayCallBackV4.callback(platformOrderId, total_fee, PayConst.CHARGE_STATE_CALLBACK_OK, rparam, '')
        TyContext.RunMode.del_server_link(platformOrderId)
        return ret

    @classmethod
    def callback_error(cls, platformOrderId, errorInfo, rparam):
        TyContext.RunMode.get_server_link(platformOrderId)
        ret = TuyouPayCallBackV4.callback(platformOrderId, 0, PayConst.CHARGE_STATE_ERROR_CALLBACK, rparam, errorInfo)
        TyContext.RunMode.del_server_link(platformOrderId)
        return ret

    @classmethod
    def notify_game_server_on_diamond_change(cls, params):
        control = TyContext.ServerControl.findServerControl(
            params['appId'], params['clientId'])
        if not control:
            TyContext.ftlog.error('notify_game_server_on_diamond_change can not'
                                  ' find server control, params', params)
            return
        notifyUrl = str(control['http'] + '/v2/game/charge/notify?' + urlencode(params))
        TyContext.ftlog.debug('notify_game_server_on_diamond_change'
                              ' arguments', params, 'notifyUrl', notifyUrl)
        try:
            from twisted.web import client
            d = client.getPage(notifyUrl, method='GET')
        except Exception as e:
            TyContext.ftlog.error('notify_game_server_on_diamond_change error', e,
                                  'notifyUrl', notifyUrl)

        def ok_callback(response):
            TyContext.ftlog.info('notify_game_server_on_diamond_change response', response)

        def err_callback(error):
            TyContext.ftlog.error('notify_game_server_on_diamond_change error', error)

        d.addCallbacks(ok_callback, err_callback)

    @classmethod
    def incr_paycount(cls, userId, count=1):
        script = '''
local ok, val = pcall(redis.call, 'hincrby', KEYS[1], KEYS[2], ARGV[1])
if ok then
  return val
else
  redis.call('hset', KEYS[1], KEYS[2], ARGV[1])
  return 'reset'
end
        '''
        userKey = 'user:' + str(userId)
        info = TyContext.RedisUser.execute(userId, 'EVAL', script, 2, userKey, 'payCount', count)
        if info == 'reset':
            TyContext.ftlog.error('incr_paycount for user', userId,
                                  'payCount error, reset to', count)

    @classmethod
    def getSdkDomain(cls):
        return TyContext.TYGlobal.http_sdk()

    @classmethod
    def getArgsDict(cls):
        return TyContext.RunHttp.convertArgsToDict()

    @classmethod
    def md5(cls, mstr):
        m = md5()
        m.update(mstr)
        md5str = m.hexdigest()
        return md5str

    @classmethod
    def md5hexdigest(cls, *args):
        mstr = []
        for argv in args:
            mstr.append(str(argv))
        mstr = ''.join(mstr)
        return cls.md5(mstr)

    @classmethod
    def verify_md5(cls, chekDigest, *args):
        mstr = []
        for argv in args:
            mstr.append(str(argv))
        mstr = ''.join(mstr)
        inputDigest = cls.md5(mstr)
        if chekDigest.upper() == inputDigest.upper():
            return True
        return False

    @classmethod
    def createLinkString(cls, rparam):
        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            ret = ret + str(k) + '=' + str(rparam[k]) + '&'
        return ret[:-1]

    @classmethod
    def createLinkString4Get(cls, rparam):
        sk = rparam.keys()
        sk.sort()
        ret = ""
        for k in sk:
            ret = ret + str(k) + '=' + quote(str(rparam[k]), '') + '&'
        return ret[:-1]

    @classmethod
    def checkCardParam(cls, mi, mo):

        card_amount = mi.getParamInt('card_amount', 0)
        if card_amount <= 0:
            mo.setError(1, '卡面额不正确')
            return False

        card_number = mi.getParamStr('card_number', '')
        if len(card_number) <= 0:
            mo.setError(1, '卡号不正确')
            return False

        card_pwd = mi.getParamStr('card_pwd', '')
        if len(card_pwd) <= 0:
            mo.setError(1, '卡密码不正确')
            return False
        return True

    __operator_dict = {
        '130': 'chinaunicom',
        '131': 'chinaunicom',
        '132': 'chinaunicom',
        '133': 'chinatelecom',
        '134': 'chinamobile',
        '135': 'chinamobile',
        '136': 'chinamobile',
        '137': 'chinamobile',
        '138': 'chinamobile',
        '139': 'chinamobile',
        '145': 'chinaunicom',
        '147': 'chinamobile',
        '150': 'chinamobile',
        '151': 'chinamobile',
        '152': 'chinamobile',
        '153': 'chinatelecom',
        '155': 'chinaunicom',
        '156': 'chinaunicom',
        '157': 'chinamobile',
        '158': 'chinamobile',
        '159': 'chinamobile',
        '1700': 'chinatelecom',
        '1705': 'chinamobile',
        '1709': 'chinaunicom',
        '176': 'chinaunicom',
        '177': 'chinatelecom',
        '178': 'chinamobile',
        '180': 'chinatelecom',
        '181': 'chinatelecom',
        '182': 'chinamobile',
        '183': 'chinamobile',
        '184': 'chinamobile',
        '185': 'chinaunicom',
        '186': 'chinaunicom',
        '187': 'chinamobile',
        '188': 'chinamobile',
        '189': 'chinatelecom'
    }

    @classmethod
    def get_mobile_operator(cls, mobile):
        if mobile[:3] == '170':
            key = mobile[:4]
        else:
            key = mobile[:3]
        try:
            return cls.__operator_dict[key]
        except:
            return 'unknown'


def get_default_paytype(clientid):
    operator_paytyes = 'weakChinaMobile,woStoreNew,woStore,aigame,YDJD'
    real_paytype = {'mi': 'xiaomi.common',
                    'midanji': 'xiaomi.danji',
                    'huabeidianhua': 'aigame',
                    'oppo': 'nearme',
                    'YDJDDanji': 'ydjd',
                    }
    fs = clientid.split('.')
    paytypes = fs[2].split(',')
    paytypes = [p for p in paytypes if p not in operator_paytyes]
    if paytypes:
        return real_paytype.get(paytypes[0], paytypes[0])
    default = fs[1].split('_')[-1]
    default_paytype = {'YDJD': 'ydjd', }
    return default_paytype.get(default, default)
