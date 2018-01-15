# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''
import json

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import _verify_with_publickey_pycrypto
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayLenovoV4(PayBaseV4):
    @payv4_order("lenovo")
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        appId = chargeinfo['appId']
        if 'payInfo' in chargeinfo and chargeinfo['payInfo']:
            payInfo = chargeinfo['payInfo']
            if 'appid' in payInfo and payInfo['appid']['lenovo']:
                appId = payInfo['appid']['lenovo']
        diamondId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('lenovo_prodids', {})
        try:
            data = prodconfig[str(appId)].get(str(diamondId), {})
            payCode = data['feecode']
        except KeyError:
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('lenovo',
                                                                                                  chargeinfo[
                                                                                                      'packageName'],
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])
            prodconfig = config.get('products', {})
            diamondList = filter(lambda x: diamondId in x.values(), prodconfig)
            diamondConfig = diamondList[0]
            payCode = diamondConfig['code']

        chargeinfo['chargeData'] = {'msgOrderCode': payCode,
                                    'waresid': payCode,
                                    'cpprivateinfo': chargeinfo['platformOrderId'],
                                    'notifyUrl': PayHelper.getSdkDomain() + '/open/ve/pay/lenovo/callback'}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    def need_continue_change_charge_info(self, chargeinfo):
        diamondId = chargeinfo['buttonId']
        config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('lenovo',
                                                                                              chargeinfo['packageName'],
                                                                                              chargeinfo['mainChannel'])
        prodConfig = config.get('products', {})
        diamondList = filter(lambda x: diamondId in x.values(), prodConfig)
        if diamondList:
            return False
        idSet = set([])
        for v in prodConfig:
            idSet.add(v.get('diamondId'))
        # 配置为空，用其他方式修改 chargeinfo
        if not idSet:
            return True
        self.change_chargeinfo(idSet, chargeinfo)
        return False

    def check_charge_info(self, mi, chargeInfo):
        if not self.need_continue_change_charge_info(chargeInfo):
            return
        appId = chargeInfo['appId']
        # packageName = chargeInfo['packageName']
        diamondId = chargeInfo['diamondId']
        prodConfig = TyContext.Configure.get_global_item_json('lenovo_prodids', {})
        thirdDict = prodConfig[appId]
        if not diamondId in thirdDict:
            clientId = chargeInfo['clientId']
            diamondPrice = chargeInfo['diamondPrice']
            prodDict = ChargeConfigure.get_prod_dict(appId, clientId=clientId)
            prodList = []
            for id in thirdDict:
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

    @payv4_callback('/open/ve/pay/lenovo/callback')
    def doLenovoCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        TyContext.ftlog.info('doLenovoCallback->rparam=', rparam)
        transdata = rparam['transdata']

        try:
            datas = json.loads(transdata)
            appId = datas['appid']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doLenovoCallback->ERROR, sign error !! transdata=', transdata)
            return 'ERROR'
        orderPlatformId = datas['exorderno']
        ChargeModel.save_third_pay_order_id(orderPlatformId, datas.get('transid', ''))
        appkeyconfig = TyContext.Configure.get_global_item_json('lenovo_appkeys', {})
        try:
            appKey = appkeyconfig[str(appId)]
        except KeyError:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'lenovo')
            appKey = config.get('lenovo_appKey')
        sign = rparam['sign']
        if self.verifySign(transdata, sign, appKey) != True:
            TyContext.ftlog.info('doLenovoCallback->ERROR, sign error !! transdata=', transdata, 'sign=', sign)
            return 'ERROR'
        total_fee = float(datas['money']) / 100
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'SUCCESS'
        else:
            return 'ERROR'

    def verifySign(self, transdata, sign, appKey):
        privateKey = self.loadRsaPrivateKey(appKey)
        return _verify_with_publickey_pycrypto(transdata, sign, privateKey)
