#! encoding=utf-8
from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay3.charge_conf import TuyouPayChargeConf
from tysdk.entity.pay3.consume import TuyouPayConsume
from tysdk.entity.pay3.diamondlist import TuyouPayDiamondList
from tysdk.entity.pay4.charge_configure import ChargeConfigure
from tysdk.entity.pay4.payment import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4

__author__ = 'yuejianqiang'


class ChargeV3Delegator(PayBaseV4):
    def make_order_id(self, userId, appId, clientId):
        return TyContext.ServerControl.makeChargeOrderIdV3(userId, appId, clientId)

    def order(self, mi):
        mo = TyContext.Cls_MsgPack()
        TyContext.ftlog.info('ChargeV3Delegator', 'order mi', mi)
        userId = mi.getParamInt('userId', 0)
        # authorCode = mi.getParamStr('authorCode')
        appId = mi.getParamStr('appId', '9999')
        appInfo = mi.getParamStr('appInfo', '')
        clientId = mi.getParamStr('clientId')
        tyChannelName = mi.getParamStr('tyChannelName')
        chargeType = mi.getParamStr('chargeType')
        prodId = mi.getParamStr('prodId')
        # 检查支持的支付列表
        store_payment = ChargeConfigure.get_store_payment(prodId, appId, clientId=clientId)
        if not store_payment:
            mo.setResult('code', 1)
            mo.setResult('info', '支付类型未配置')
            return mo
        # 获取对应的支付类型
        payInfo = filter(lambda x: x['paytype'] == chargeType, store_payment)
        if not payInfo:
            mo.setResult('code', 1)
            mo.setResult('info', '支付类型无效')
            return mo
        # 获取商品信息
        prod_info = ChargeConfigure.get_prod_info(appId, prodId, clientId=clientId)
        if not prod_info:
            mo.setResult('code', 1)
            mo.setResult('info', '未找到对应的商品')
            return mo
        try:
            chargeInfo = self.get_charge_info(mi)
        except TyContext.FreetimeException as e:
            TyContext.ftlog.error('_charge_begin_w_new_categories exception', e)
            mo.setError(e.errorCode, e.message)
            return mo
        # chargeinfo_dump = json.dumps(chargeInfo)
        # datas = ['state', PayConst.CHARGE_STATE_BEGIN,
        #         'charge', chargeinfo_dump,
        #         'createTime', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
        #
        # TyContext.RedisPayData.execute('HMSET', 'sdk.charge:' + orderId, *datas)
        # ChargeModel.save_order(prodOrderId, *datas)
        # 返回数据
        mo.setResult('code', 0)
        mo.setResult('chargeInfo', chargeInfo)
        return mo

    def check_charge_info(self, mi, chargeInfo):
        appId = chargeInfo['appId']
        clientId = chargeInfo['clientId']
        diamondId = chargeInfo['diamondId']
        # prodPrice = chargeInfo['diamondPrice']
        prodCount = chargeInfo['diamondCount']
        mustcharge = int(chargeInfo.get('mustcharge', 0))
        diamondlist = TuyouPayDiamondList.diamondlist2(appId, clientId)
        prodInfo = ChargeConfigure.get_prod_info(appId, diamondId, clientId=clientId)
        # 非钻石商品需要先购买钻石
        if not prodInfo.get('is_diamond', 0):
            # 消耗的钻石数量
            consumeCoin = int(prodInfo['diamondPrice'] * prodCount)
            if not diamondlist:
                TyContext.ftlog.error('__consume_charge__ diamondlist ERROR', appId, clientId)
                raise PayErrorV4(6, '钻石列表配置错误')
                return True
            ios_patch = TyContext.Configure.get_global_item_int('patch_ios_bug_TY9999R0003001', 1)
            if ios_patch:
                diamondlist = TuyouPayConsume._patch_ios_client_bug(clientId, diamondlist)
            for diamond in diamondlist:
                count = diamond['count']
                if count >= consumeCoin:
                    break
            else:
                TyContext.ftlog.error('__consume_charge__ find charge diamond ERROR', appId, clientId, consumeCoin,
                                      diamondlist)
                raise PayErrorV4(7, '钻石项目取得失败')
            chargeInfo['diamondId'] = diamond['id']
            chargeInfo['diamondPrice'] = diamond['price']
            chargeInfo['chargeTotal'] = diamond['price'] * chargeInfo['diamondCount']
            if mustcharge or True:
                chargeInfo['diamondName'] = diamond['name']
                chargeInfo['buttonId'] = chargeInfo['diamondId']
                chargeInfo['buttonName'] = chargeInfo['diamondName']
        try:
            self.get_charge_data(chargeInfo)
        except TyContext.FreetimeException as e:
            TyContext.ftlog.error('_charge_begin_w_new_categories exception', e)
            # mo.setError(e.errorCode, e.message)
            # return mo
            raise (e.errorCode, e.message)

    @classmethod
    def get_charge_data(cls, chargeinfo):
        ''' delegate to charge_data func of thirdpay '''
        cfun = TuyouPayChargeConf.get_charge_data_func(chargeinfo['chargeType'])
        try:
            cfun(chargeinfo)
        except TyContext.FreetimeException as e:
            raise
        except Exception as e:
            TyContext.ftlog.exception()
            return

        if 'chargeData' not in chargeinfo and 'chargeCategories' not in chargeinfo:
            raise Exception('neither chargeData nor chargeCategories in chargeinfo')

        try:
            if chargeinfo['chargeData'].get('need_short_order_id', 0):
                chargeinfo['shortDiamondOrderId'] = ShortOrderIdMap.get_short_order_id(
                    chargeinfo['platformOrderId'])
        except:
            pass
