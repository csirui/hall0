# -*- coding=utf-8 -*-

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import rsaVerify


class TuyouPayOppo():
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        diamondId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('oppo_prodids', {})
        data = prodconfig[str(appId)].get(str(diamondId), None)

        if data:
            oppoCount = data['count']
            oppoProdName = data['name']
        else:
            raise Exception(
                'can not find oppo product define of buttonId=' + diamondId
                + ' clientId=' + chargeinfo['clientId'])
        chargeinfo['chargeData'] = {'oppoCount': oppoCount, 'oppoProdName': oppoProdName}

    @classmethod
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
        isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        if isOk:
            return 'result=OK&resultMsg=成功'
        else:
            return 'result=FAIL&resultMsg=发商品失败'

        pass
