# -*- coding=utf-8 -*-

import json

from Crypto.PublicKey import RSA

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto_md5
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYooIappayV4(PayBaseV4):
    @payv4_order('iappay')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        appid = mi.getParamStr('iappay_appid', None)
        if not appid:
            raise PayErrorV4(1, "爱贝支付ID不存在")
        iappayConfig = TyContext.Configure.get_global_item_json('iappay_config', {})
        appKey = iappayConfig.get(appid)['appkey'] if iappayConfig.get(appid) else ""
        if not appKey:
            chargeType = chargeinfo['chargeType']
            sdk = chargeType.split('.')[0]
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package(sdk,
                                                                                                  chargeinfo[
                                                                                                      'packageName'],
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])

            prodConfig = config.get('products', {})
            diamondList = filter(lambda x: chargeinfo['diamondId'] in x.values(), prodConfig)
            diamondConfig = diamondList[0] if diamondList else {}
            if not diamondConfig:
                raise PayErrorV4(1, '【爱贝】没有对应的计费点代码！')
            chargeinfo['chargeData'] = {'waresid': diamondConfig.get("feecode"), 'appKey': config.get('iappay_appKey')}
            return self.return_mo(0, chargeInfo=chargeinfo)
        try:
            # if 'prodId' in chargeinfo:
            #    waresid = iappayConfig[appid]['payConfig'][chargeinfo['prodId']]
            # if 'buttonId' in chargeinfo:
            #     waresid = iappayConfig[appid]['payConfig'][chargeinfo['buttonId']]
            # elif 'diamondId' in chargeinfo:
            waresid = iappayConfig[appid]['payConfig'][chargeinfo['diamondId']]
            # else:
            #    waresid = None
        except:
            waresid = None
        if not waresid:
            raise PayErrorV4(1, '【爱贝】没有对应的计费点代码！')
        if not appKey:
            TyContext.ftlog.error('TuYooIappay this id has no key , id ', appid)
            raise PayErrorV4(1, '爱贝ID [%s] 没有找到对应的参数' % appid)
        if not waresid:
            TyContext.ftlog.error('TuYooIappay this prodId has no waresid , chargeinfo ', chargeinfo)
        chargeinfo['chargeData'] = {'waresid': waresid, 'appKey': appKey}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_order('lenovodanji.iappay')
    def chare_data_lenovo(self, mi):
        return self.charge_data(mi)

    @payv4_order('samsung.iappay')
    def chare_data_samsung(self, mi):
        return self.charge_data(mi)

    def need_continue_change_chargeinfo(self, chargeinfo):
        '''
            检查 ID是否配置，未配置 就进行配置
            :param chargeinfo:
            :return:
        '''
        chargeType = chargeinfo['chargeType']
        sdk = chargeType.split('.')[0]
        config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package(sdk,
                                                                                              chargeinfo['packageName'],
                                                                                              chargeinfo['mainChannel'])
        diamondId = chargeinfo['diamondId']
        prodConfig = config.get('products', {})
        diamondList = filter(lambda x: diamondId in x.values(), prodConfig)
        diamondConfig = diamondList[0] if diamondList else {}
        if diamondConfig:
            return False
        idSet = set([])
        for v in prodConfig:
            idSet.add(v.get('prodId'))  # 叫这个名字!!!
        # 配置为空，用其他方式修改 chargeinfo
        if not idSet:
            return True
        self.change_chargeinfo(idSet, chargeinfo)
        return False

    def check_charge_info(self, mi, chargeInfo):
        if not self.need_continue_change_chargeinfo(chargeInfo):
            return
        iappay_appid = mi.getParamStr('iappay_appid', None)
        iappayConfig = TyContext.Configure.get_global_item_json('iappay_config', {})
        payConfig = iappayConfig[iappay_appid]['payConfig']
        appId = chargeInfo['appId']
        diamondId = chargeInfo['diamondId']
        if not diamondId in payConfig:
            clientId = chargeInfo['clientId']
            diamondPrice = chargeInfo['diamondPrice']
            prodDict = ChargeConfigure.get_prod_dict(appId, clientId=clientId)
            prodList = []
            for id in payConfig:
                # 单机商品过滤掉
                if id.endswith('DJ'):
                    continue
                try:
                    prodInfo = prodDict[id]
                except KeyError:
                    continue
                if int(prodInfo.get('is_diamond', 0)) and prodInfo['price'] >= diamondPrice:
                    prodList.append(prodInfo)
            if prodList:
                prodList.sort(lambda x, y: cmp(x['price'], y['price']))
                prodInfo = prodList[0]
                chargeInfo['diamondId'] = prodInfo['id']
                chargeInfo['diamondName'] = prodInfo['name']
                chargeInfo['buttonName'] = prodInfo['name']
                chargeInfo['diamondPrice'] = prodInfo['price']
                chargeInfo['chargeTotal'] = prodInfo['price'] * chargeInfo['diamondCount']
                chargeInfo['chargeCoin'] = prodInfo['diamondPrice'] * chargeInfo['diamondCount']

    @payv4_callback('/open/ve/pay/iappay/callback')
    def doIappayPayCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        transdata = rparam['transdata']
        transdata = json.loads(transdata)
        sign = rparam['sign']
        appid = transdata['appid']
        signtype = rparam['signtype']
        iappayConfig = TyContext.Configure.get_global_item_json('iappay_config', {})
        try:
            pubkey = iappayConfig.get(appid)['pubkey'] if iappayConfig.get(appid) else ""
            orderPlatformId = transdata['cporderid']
            total_fee = transdata['money']
            result = transdata['result']
            ChargeModel.save_third_pay_order_id(orderPlatformId, transdata.get('transid'))
        except Exception as e:
            TyContext.ftlog.error('doIappayPayCallback->ERROR, exception', e, 'rparam', transdata)
            return 'error'
        if not pubkey:
            chargeKey = 'sdk.charge:' + orderPlatformId
            chargeInfo = TyContext.RedisPayData.execute('HGET', chargeKey, 'charge')
            if chargeInfo:
                chargeInfo = TyContext.strutil.loads(chargeInfo, decodeutf8=True)
            else:
                return 'failed'
            chargeType = chargeInfo['chargeType']
            sdk = chargeType.split('.')[0]
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, sdk)
            pubkey = config.get('iappay_pubKey')
            if not pubkey:
                TyContext.ftlog.error('doIappayPayCallback->ERROR,cannot get sdkconfig for', appid)
                return 'failed'
            pubkey = cls.loadRsaPublicKey(pubkey)
        if not cls._verify_sign(rparam, sign, pubkey):
            errinfo = '支付失败'
            PayHelperV4.callback_error(orderPlatformId, errinfo, rparam)
            return 'failed'

        if result != 0:
            errinfo = '支付失败'
            TyContext.ftlog.error('doIappayPayCallback->ERROR, exception, result not 0')
            PayHelperV4.callback_error(orderPlatformId, errinfo, rparam)
            return 'failed'
        PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        return 'success'

    @classmethod
    def _verify_sign(cls, rparam, sign, pubkey):
        # data = "&".join(k + "=" + str(rparam[k]) for k in rparam.keys())
        data = str(rparam['transdata'])
        key = RSA.importKey(pubkey)
        TyContext.ftlog.error('doIappayPayCallback->ERROR, exception', data, sign, key)
        return _verify_with_publickey_pycrypto_md5(data, sign, key)
