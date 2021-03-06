# -*- coding=utf-8 -*-
'''
Created on 2014-12-05

@author: Fan Zheng
'''

from tyframework.context import TyContext
from tysdk.entity.pay.rsacrypto import _import_rsa_key_, \
    _sign_with_privatekey_pycrypto, _verify_with_publickey_pycrypto
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayHuaWei(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = str(chargeinfo['appId'])
        clientId = str(chargeinfo['clientId'])
        if 'payInfo' in chargeinfo and chargeinfo['payInfo']:
            payInfo = chargeinfo['payInfo']
            if 'appid' in payInfo and payInfo['appid']['huawei']:
                clientId = payInfo['appid']['huawei']
        huawei_config = TyContext.Configure.get_global_item_json('huawei_config', {})
        hwapps = huawei_config.get(clientId, None)
        if hwapps:
            userName = hwapps['userName']  # 必填 不参与签名
            userID = hwapps['pay_id']  # String    支付ID。 在开发者联盟上获取的支付 ID    必填
            applicationID = hwapps['hw_appid']  # String    应用ID。 在开发者联盟上获取的APP ID    必填
        else:
            raise Exception('TuYouPayHuaWei can not find huawei config of clientId=' + clientId)
        amount = '%.2f' % float(chargeinfo[
                                    'chargeTotal'])  # String    商品所要支付金额。格式为：元.角分，最小金额为分，保留到小数点后两位。例如：20.00，此金额将会在支付时显示给用户确认)，     必填
        productName = chargeinfo['diamondName']  # String(50)    商品名称。此名称将会在支付时显示给用户确认   必填
        requestId = chargeinfo['platformOrderId']  # String(30)    开发者支付订单号。注：最长30字节。其值由开发者定义生成，用于标识一次支付请求，每次请求需唯一，不可重复。
        productDesc = chargeinfo['diamondName']  # String(100)    商户对商品的自定义描述 。 必填，不能为空

        rparam = {'userID': userID,
                  'applicationID': applicationID,
                  'amount': amount,
                  'productName': productName,
                  'requestId': requestId,
                  'productDesc': productDesc,
                  }
        sign = cls.__check_ras_code__(hwapps, rparam, True)
        rparam['sign'] = sign
        rparam['userName'] = userName
        rparam['notifyUrl'] = PayHelper.getSdkDomain() + '/v1/pay/huawei/callback'
        chargeinfo['chargeData'] = rparam

    @classmethod
    def __check_ras_code__(cls, hwapps, rparam, issign):
        TyContext.ftlog.debug('__check_ras_code__->', rparam, issign, hwapps)
        sk = rparam.keys()
        sk.sort()
        ret = ""
        sign = ''
        for k in sk:
            if k == 'sign':
                sign = rparam[k]
            else:
                v = rparam[k]
                if isinstance(v, unicode):
                    v = v.encode('utf-8')
                else:
                    v = str(v)
                # TyContext.ftlog.debug('k====>', k, 'v====>', v, 'ret==>', ret)
                ret = ret + str(k) + '=' + v + '&'
        sigdata = ret[:-1]

        if issign:
            private_key = hwapps.get('_pay_ras_privat_key_', None)
            if not private_key:
                private_key = _import_rsa_key_(hwapps['pay_ras_privat_key'])
                hwapps['_pay_ras_privat_key_'] = private_key
            TyContext.ftlog.debug('__check_ras_code__ sign code ', sign, sigdata, private_key)
            b = _sign_with_privatekey_pycrypto(sigdata, private_key)
            return b
        else:
            public_key = hwapps.get('_pay_ras_pub_key_', None)
            if not public_key:
                public_key = _import_rsa_key_(hwapps['pay_ras_pub_key'])
                hwapps['_pay_ras_pub_key_'] = public_key
            TyContext.ftlog.debug('__check_ras_code__ verify ', sign, sigdata, public_key)
            isOk = _verify_with_publickey_pycrypto(sigdata, sign, public_key)
            return isOk

    @classmethod
    def doHuaWeiCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doHuaWeiCallback->rparam=', rparam)
        try:
            orderPlatformId = rparam['requestId']
            clientId = rparam['extReserved']
            huawei_config = TyContext.Configure.get_global_item_json('huawei_config', {})
            hwapps = huawei_config.get(clientId, None)
            isOk = self.__check_ras_code__(hwapps, rparam, False)
            if isOk:
                total_fee = float(rparam['amount'])
                try:
                    # huawei sdk also use payType, which is tuyou's sub_paytype
                    rparam['sub_paytype'] = rparam['payType']
                    del rparam['payType']
                except:
                    pass
                isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
                if isOk:
                    return '{"result":0}'
                else:
                    return '{"result":3}'
            else:
                return '{"result":1}'
        except:
            TyContext.ftlog.exception()
            return '{"result":94}'
