# -*- coding=utf-8 -*-

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import rsaVerify
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuyouPayOppoV4(PayBaseV4):
    def check_charge_info(self, mi, chargeInfo):

        if not self.need_continue_changed_chargeinfo(mi, chargeInfo):
            return
        TyContext.ftlog.debug('need continue change chargeinfo !')
        appId = chargeInfo['appId']
        prodconfig = TyContext.Configure.get_global_item_json('oppo_prodids', {})
        opppProdDict = prodconfig.get(str(appId), {})
        buttonId = chargeInfo['buttonId']
        if not buttonId in opppProdDict:
            clientId = chargeInfo['clientId']
            diamondPrice = chargeInfo['diamondPrice']
            prodDict = ChargeConfigure.get_prod_dict(appId, clientId=clientId)
            prodList = []
            for id in opppProdDict:
                try:
                    prodInfo = prodDict[id]
                except KeyError:
                    continue
                if prodInfo.get('is_diamond') and prodInfo['price'] >= diamondPrice:
                    prodList.append(prodInfo)
            if prodList:
                prodList.sort(lambda x, y: cmp(x['price'], y['price']))
                prodInfo = prodList[0]
                chargeInfo['diamondId'] = prodInfo['id']
                chargeInfo['diamondName'] = prodInfo['name']
                chargeInfo['diamondPrice'] = prodInfo['price']
                chargeInfo['chargeTotal'] = prodInfo['price'] * chargeInfo['diamondCount']
                chargeInfo['chargeCoin'] = prodInfo['diamondPrice'] * chargeInfo['diamondCount']

    def need_continue_changed_chargeinfo(self, mi, chargeInfo):
        '''

        :param mi:
        :param chargeInfo:
        :return:
        '''
        appId = chargeInfo['appId']
        clientId = chargeInfo['clientId']
        mainchannel = chargeInfo['mainChannel']
        config = GameItemConfigure(appId).get_game_channel_configure_by_package('nearme', chargeInfo['packageName'],
                                                                                mainchannel)
        TyContext.ftlog.debug('oppo getSdkConfig-->', config)
        buttonId = chargeInfo['buttonId']
        prodconfig = config.get('products', {})
        diamondList = filter(lambda x: buttonId in x.values(), prodconfig)
        TyContext.ftlog.debug('oppo diamondList->', diamondList)
        if diamondList:
            return False
        idSet = set([])
        for v in prodconfig:
            idSet.add(v.get('diamondId'))
        # 配置为空，用其他方式修改 chargeinfo
        if not idSet:
            return True
        self.change_chargeinfo(idSet, chargeInfo)
        return False

    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        appId = chargeinfo['appId']
        diamondId = chargeinfo['diamondId']
        prodconfig = TyContext.Configure.get_global_item_json('oppo_prodids', {})
        try:
            data = prodconfig[str(appId)].get(str(diamondId), None)
        except:
            data = None
        if data:
            oppoCount = data['count']
            oppoProdName = data['name']
        else:
            config = GameItemConfigure(appId).get_game_channel_configure_by_package('nearme', chargeinfo['packageName'],
                                                                                    chargeinfo['mainChannel'])
            prodconfig = config.get('products')
            diamondList = filter(lambda x: diamondId in x.values(), prodconfig)
            diamondConfig = diamondList[0] if diamondList else {}
            if not diamondConfig:
                raise PayErrorV4(1,
                                 'can not find oppo product define of diamondId=' + diamondId
                                 + ' clientId=' + chargeinfo['clientId'])
            else:
                oppoCount = diamondConfig.get('count')
                oppoProdName = diamondConfig.get('name')
        chargeinfo['chargeData'] = {'oppoCount': oppoCount, 'oppoProdName': oppoProdName}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_order("nearme")
    def order_nearme(self, mi):
        return self.charge_data(mi)

    @payv4_order("nearme.ali")
    def order_nearme_ali(self, mi):
        return self.charge_data(mi)

    @payv4_order("nearme.wx")
    def order_nearme_wx(self, mi):
        return self.charge_data(mi)

    @payv4_callback('/open/ve/pay/oppo/callback')
    def doOppoCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        orderPlatformId = ''
        try:
            notifyId = rparam['notifyId']
            orderPlatformId = rparam['partnerOrder']

            productName = rparam['productName']
            productDesc = rparam['productDesc']
            price = rparam['price']
            count = rparam['count']
            attach = rparam['attach']
            sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doOppoCallback->ERROR, param error !! rparam=', rparam)
            return 'result=FAIL&resultMsg=参数错误'

        baseString = 'notifyId=' + notifyId + '&partnerOrder=' + orderPlatformId + '&productName=' + productName + '&productDesc=' + productDesc + '&price=' + str(
            price) + '&count=' + str(count) + '&attach=' + attach
        # 签名校验
        if not rsaVerify(baseString, sign, 'oppo'):
            TyContext.ftlog.error('TuyouPayOppo.doOppoCallback rsa verify error !!')
            return 'result=FAIL&resultMsg=签名验证失败'

        total_fee = float(price) / 100
        ChargeModel.save_third_pay_order_id(orderPlatformId, notifyId)
        isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'result=OK&resultMsg=成功'
        else:
            return 'result=FAIL&resultMsg=发商品失败'
