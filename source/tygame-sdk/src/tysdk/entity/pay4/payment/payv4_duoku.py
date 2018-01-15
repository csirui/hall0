# -*- coding=utf-8 -*-

from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.entity.pay4.payment.payv4_helper import PayHelperV4


class TuYouPayDuoKuV4(PayBaseV4):
    @payv4_order('duoku')
    def charge_data(cls, mi):

        chargeinfo = cls.get_charge_info(mi)

        packageName = chargeinfo['packageName']

        appId = chargeinfo['appId']
        buttonId = chargeinfo['diamondId']
        clientId = chargeinfo['clientId']
        # 先取多appId对应的支付配置
        payData = None
        duokuAppId = mi.getParamStr('dksdk_appid', "")
        config = GameItemConfigure(appId).get_game_channel_configure_by_primarykey('duoku', 'dksdk_appid', duokuAppId,
                                                                                   chargeinfo['mainChannel'])
        if config:
            prodconfig = config.get('products', {})
            diamondList = filter(lambda x: buttonId in x.values(), prodconfig)
            payData = diamondList[0] if diamondList else {}
            if payData:
                orderPlatformId = chargeinfo['platformOrderId']
                shortOrderPlatformId = ShortOrderIdMap.get_short_order_id(orderPlatformId)
                payData['orderPlatformId'] = shortOrderPlatformId
                chargeinfo['chargeData'] = payData
                return cls.return_mo(0, chargeInfo=chargeinfo)
        prodconfig = TyContext.Configure.get_global_item_json('duoku_prodids')
        if duokuAppId:
            config = prodconfig.get(duokuAppId, None)
            if config:
                payData = config.get(buttonId, None)
        if not payData:
            if packageName:
                try:
                    appconfig = prodconfig[packageName]
                    payData = appconfig[buttonId]
                except:
                    TyContext.ftlog.exception()
                    raise PayErrorV4(1, '【百度】找不到这个商品[%s]配置！' % buttonId)
            else:
                try:
                    appconfig = prodconfig[str(appId)]
                    payData = appconfig[buttonId]
                except Exception as e:
                    TyContext.ftlog.exception()
                    raise PayErrorV4(1, '【百度】找不到这个商品[%s]配置！' % buttonId)
        orderPlatformId = chargeinfo['platformOrderId']
        shortOrderPlatformId = ShortOrderIdMap.get_short_order_id(orderPlatformId)
        payData['orderPlatformId'] = shortOrderPlatformId
        chargeinfo['chargeData'] = payData
        return cls.return_mo(0, chargeInfo=chargeinfo)

    def need_continue_change_chargeinfo(self, chargeinfo):
        '''
        检查 ID是否配置，未配置 就进行配置
        :param chargeinfo:
        :return:
        '''
        config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('duoku',
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
            idSet.add(v.get('diamondId'))
        # 配置为空，用其他方式修改 chargeinfo
        if not idSet:
            return True
        self.change_chargeinfo(idSet, chargeinfo)
        return False

    def check_charge_info(self, mi, chargeInfo):
        if not self.need_continue_change_chargeinfo(chargeInfo):
            return
        appId = chargeInfo['appId']
        packageName = chargeInfo['packageName']
        diamondId = chargeInfo['diamondId']
        prodConfig = TyContext.Configure.get_global_item_json('duoku_prodids', {})
        thirdDict = prodConfig[packageName]
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

    @payv4_callback('/open/ve/pay/duoku/msg/callback')
    def doDuoKuCallback(cls, rpath):
        TyContext.ftlog.info('doDuoKuCallback start')
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            shortOrderPlatformId = rparam['cpdefinepart']
            orderPlatformId = ShortOrderIdMap.get_long_order_id(shortOrderPlatformId)
            appId = rparam['appid']
            sign = rparam['sign']
            unit = rparam['unit']
            amount = rparam['amount']
            status = rparam['status']
            mobileId = rparam.get('phone', '')
        except:
            TyContext.ftlog.info('doDuoKuCallback->ERROR, param error !! rparam=', rparam)
            TyContext.ftlog.exception()
            return 'failure'
        if status != 'success':
            PayHelperV4.callback_error(orderPlatformId, 'pay fail', rparam)
            return 'failure'
        paykey_dict = TyContext.Configure.get_global_item_json('duoku_paykeys', {})
        paykey = paykey_dict.get(appId, "")
        if not paykey:
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId)
            paykey = config.get('dksdk_appsecret', "")
            if not paykey:
                TyContext.ftlog.error("doDuokuCallback", "cannot get %s sdkconfig" % appId)
        # 签名校验
        if not cls.__verify_sign(rparam, paykey, sign):
            return 'failure'

        if unit == 'fen':
            total_fee = float(amount) / 100
        else:
            total_fee = float(amount)
        ChargeModel.save_third_pay_order_id(orderPlatformId, rparam.get('orderid'))
        rparam['chargeType'] = 'duoku'
        rparam['third_orderid'] = rparam['orderid']
        PayHelperV4.set_order_mobile(orderPlatformId, mobileId)
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'success'
        else:
            return 'failure'

    @classmethod
    def __verify_sign(cls, rparam, paykey, sign):
        check_str = (rparam['appid']
                     + rparam['orderid']
                     + rparam['amount']
                     + rparam['unit']
                     + rparam['status']
                     + rparam['paychannel']
                     + paykey)
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayDuoKu verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
