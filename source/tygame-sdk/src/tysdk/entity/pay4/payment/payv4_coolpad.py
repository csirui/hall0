#! encoding=utf-8
from Crypto.PublicKey import RSA

from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto_md5
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
import json
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayCoolpadV4(PayBaseV4):
    ORDER_URL = 'http://pay.coolyun.com:6988/payapi/order'

    @payv4_order("coolpad")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        cls.check_charge_info(mi, chargeinfo)
        packageName = chargeinfo['packageName']
        userId = int(chargeinfo['uid'])
        snsId, snsinfo = TyContext.RedisUser.execute(userId, 'HMGET', 'user:%s' % userId, 'snsId', 'snsinfo')
        coolpad_keys = TyContext.Configure.get_global_item_json('coolpad_keys', {})
        for appId, appInfo in coolpad_keys.items():
            if appId == 'publicKey':
                continue
            if isinstance(appInfo, dict) and appInfo.get('package') == packageName:
                break
        else:
            TyContext.ftlog.error('TuYouPayCoolpad package not found ', packageName)
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('coolpad',
                                                                                                  chargeinfo[
                                                                                                      'packageName'],
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])
            if not config:
                raise PayErrorV4(1, 'TuYouPayCoolpad package not found %s' % packageName)
            else:
                appInfo = {
                    'appId': config.get('coolpad_appId'),
                    'appKey': config.get('coolpad_appKey'),
                }
            prodConfig = config.get('products', {})
            diamondId = chargeinfo['diamondId']
            diamondList = filter(lambda x: diamondId in x.values(), prodConfig)
            diamondConfig = {}
            if diamondList:
                diamondConfig = diamondList[0]
            waresid = diamondConfig.get('code', '')
            if not waresid:
                raise PayErrorV4(1, "找不到计费点 ")
            chargeinfo['chargeData'] = {'callback': 'http://open.touch4.me/v1/pay/coolpad/callback', 'waresid': waresid,
                                        'appKey': appInfo['appKey'], 'openID': snsId[len('coolpad:'):],
                                        'authToken': snsinfo}
            return cls.return_mo(0, chargeInfo=chargeinfo)
        appId = appInfo['appId']
        appKey = appInfo['appKey']
        try:
            if 'diamondId' in chargeinfo:
                waresid = chargeinfo['diamondId']
            elif 'buttonId' in chargeinfo:
                waresid = chargeinfo['buttonId']
            elif 'prodId' in chargeinfo:
                waresid = chargeinfo['prodId']
            else:
                waresid = None
            waresid = appInfo['products'][waresid]
        except:
            TyContext.ftlog.error('TuYouPayCoolpad product not found ', chargeinfo)
            raise PayErrorV4(1, "找不到计费点 ")
        if not appKey:
            TyContext.ftlog.error('TuYooIappay this id has no key , id ', appId)

        if not waresid:
            TyContext.ftlog.error('TuYooIappay this prodId has no waresid , chargeinfo ', chargeinfo)
            raise PayErrorV4(1, "找不到计费点 ")
        chargeinfo['chargeData'] = {'callback': 'http://open.touch4.me/v1/pay/coolpad/callback', 'waresid': waresid,
                                    'appKey': appKey, 'openID': snsId[len('coolpad:'):], 'authToken': snsinfo}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    def check_charge_info(self, mi, chargeinfo):
        '''
        检查计费点有没有配置，
        没有：找所有产品里面不小于当前计费点价格的最小钻石替换充值信息
        :param chargeinfo:
        :return:
        '''
        config = GameItemConfigure.get_game_channel_configure_by_orderId(chargeinfo['platformOrderId'])
        diamondId = chargeinfo['diamondId']
        prodConfig = config.get('products', {})
        diamondList = filter(lambda x: diamondId in x.values(), prodConfig)
        diamondConfig = diamondList[0] if diamondList else {}
        if diamondConfig:
            return
        idSet = set([])
        for v in prodConfig:
            id = v.get('diamondId')
            if id:
                idSet.add(id)
        # 配置为空，用其他方式修改 chargeinfo
        if not idSet:
            return
        self.change_chargeinfo(idSet, chargeinfo)

    @payv4_callback("/open/ve/pay/coolpad/callback")
    def doCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        transdata = rparam['transdata']
        transdata = json.loads(transdata)
        sign = rparam['sign']
        appid = transdata['appid']
        signtype = rparam['signtype']
        orderPlatformId = transdata['cporderid']
        try:
            coolpad_keys = TyContext.Configure.get_global_item_json('coolpad_keys', {})
            pubkey = coolpad_keys[appid]['publicKey']
        except:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'coolpad')
            pubkey = config.get('coolpad_appPubKey', '')
            if not pubkey:
                TyContext.ftlog.debug("doCoolpadCallback,cannot find coolpad sdkconfig for", appid)
                return 'error'
            pubkey = self.loadRsaPublicKey(pubkey)
        try:
            # total_fee = transdata['money']
            result = transdata['result']
        except Exception as e:
            TyContext.ftlog.error('doCoolpadPayCallback->ERROR, exception', e, 'rparam', transdata)
            return 'error'
        if not self._verify_sign(rparam, sign, pubkey):
            errinfo = '支付失败'
            ChargeModel.save_third_pay_order_id(orderPlatformId, transdata.get('transid', ''))
            PayHelperV4.callback_error(orderPlatformId, errinfo, rparam)
            return 'failed'
        if result != 0:
            errinfo = '支付失败'
            TyContext.ftlog.error('doCoolpadPayCallback->ERROR, exception, result not 0')
            PayHelperV4.callback_error(orderPlatformId, errinfo, rparam)
            return 'failed'
        PayHelperV4.callback_ok(orderPlatformId, -1, rparam)
        return 'success'

    @classmethod
    def _verify_sign(cls, rparam, sign, pubkey):
        # data = "&".join(k + "=" + str(rparam[k]) for k in rparam.keys())
        data = str(rparam['transdata'])
        key = RSA.importKey(pubkey)
        TyContext.ftlog.error('doCoolpadPayCallback->ERROR, exception', data, sign, key)
        return _verify_with_publickey_pycrypto_md5(data, sign, key)
