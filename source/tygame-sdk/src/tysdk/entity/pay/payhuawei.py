# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''

from tyframework.context import TyContext
from tysdk.entity.pay.pay import TuyouPay
from tysdk.entity.pay.rsacrypto import _import_rsa_key_, \
    _sign_with_privatekey_pycrypto, _verify_with_publickey_pycrypto
from tysdk.entity.paythird.helper import PayHelper


class TuyouPayHuaWei(object):
    pub_key_1 = '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALajjeAqG8xbEW9dLSdLLhN0dhgFm4eW
YHYxwCki/FXc9uDuq31lcEnleRQEEW/mV/P/5ML271kjP+JPlsvE8+sCAwEAAQ==
-----END PUBLIC KEY-----'''
    prv_key_1 = '''-----BEGIN RSA PRIVATE KEY-----
MIIBVwIBADANBgkqhkiG9w0BAQEFAASCAUEwggE9AgEAAkEAtqON4CobzFsRb10t
J0suE3R2GAWbh5ZgdjHAKSL8Vdz24O6rfWVwSeV5FAQRb+ZX8//kwvbvWSM/4k+W
y8Tz6wIDAQABAkEAo2g6K/IA5Rolw0nOeHWfR/DPKDb8LJeyvo1MrIGM2xRRMI97
FvQVUNOrYgNvZyVJGkOMD6atqnuj3A3wBQWhgQIhANiY9LkJ/Px6blln3sZmIWRb
CKZ1TF/p8BGotpDg9CFRAiEA190hc5EMJ9tfCleKEd5IIzkR5nbwPA7G+53ZTnu9
UnsCIQCoXxZ1tQb9OSsIww7RCVlRytZJl4s8T/03rP/mVYhRUQIhAJdRryJpGmFS
OWRxixsNe/odBnxNAgjHvxshQvTubv/DAiEApTdN5GR9+culN9SGX+h65UJ45xmW
gM3nmzXEXBITsjk=
-----END RSA PRIVATE KEY-----'''

    pub_key_2 = '''-----BEGIN PUBLIC KEY-----
MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJQNHmiSC2cyVzo3zY0WfjQcn5nPl+uk
AjXo0syHc+T2okBrub619vHfe1xa5Zru01nbi/PLUONh51dMQwIWmnkCAwEAAQ==
-----END PUBLIC KEY-----'''
    prv_key_2 = '''-----BEGIN RSA PRIVATE KEY-----
MIIBVQIBADANBgkqhkiG9w0BAQEFAASCAT8wggE7AgEAAkEAlA0eaJILZzJXOjfN
jRZ+NByfmc+X66QCNejSzIdz5PaiQGu5vrX28d97XFrlmu7TWduL88tQ42HnV0xD
AhaaeQIDAQABAkA8vcUkEgcrp7Ox5wMmR3wv1S6F5G3n97oQdB1IXKpn3UiIpMiV
Hyz9inlztjeNYjVD2WnAJzkNwDjgLglEJAABAiEAygq1kdbVgNJhJyhxWwQnoJvm
hmyXiR2YA3psVppdrAECIQC7lyfc3MIz42b0eiRjVAnR4ARHK3ypVZTQb6kRoWhO
eQIgUAQLwrVlmv42sc5njldH5mi31Hb/ULNit8XtUCMUhAECIQCC2Bvl4dVTe/oD
7G4VGjj/OtHBEoQRWLBD8p5qvbqTgQIhALHzMHK8iBKLYlvrSNKWPZGQt8ohWe6U
5+hSNc9aosOM
-----END RSA PRIVATE KEY-----'''

    HWAPPS = {
        # 疯狂AAA
        '1': {'userName': 'tuyou',
              'hw_appid': '10157894',
              'pay_id': '900086000020107980',
              'pay_ras_pub_key': pub_key_1,
              'pay_ras_privat_key': prv_key_1
              },
        # 疯狂斗牛
        '10': {'userName': 'tuyou',
               'hw_appid': '10157900',
               'pay_id': '900086000020107980',
               'pay_ras_pub_key': pub_key_1,
               'pay_ras_privat_key': prv_key_1
               },
        # 疯狂麻将
        '7': {'userName': 'tuyou',
              'hw_appid': '10157898',
              'pay_id': '900086000020107980',
              'pay_ras_pub_key': pub_key_1,
              'pay_ras_privat_key': prv_key_1
              },
        # 疯狂德州
        '8': {'userName': 'tuyou',
              'hw_appid': '10157896',
              'pay_id': '900086000020107980',
              'pay_ras_pub_key': pub_key_1,
              'pay_ras_privat_key': prv_key_1
              },
        # 斗地主
        '6': {'userName': 'tuyou',
              'hw_appid': '10161280',
              'pay_id': '10086000000680944',
              'pay_ras_pub_key': pub_key_2,
              'pay_ras_privat_key': prv_key_2
              },
    }

    @classmethod
    def doBuyStraight(cls, userId, params, mo):
        appId = str(params['appId'])
        hwapps = TuyouPayHuaWei.HWAPPS[appId]

        userName = hwapps['userName']  # 必填 不参与签名
        userID = hwapps['pay_id']  # String    支付ID。 在开发者联盟上获取的支付 ID    必填
        applicationID = hwapps['hw_appid']  # String    应用ID。 在开发者联盟上获取的APP ID    必填
        amount = '%d.00' % int(
            params['orderPrice'])  # String    商品所要支付金额。格式为：元.角分，最小金额为分，保留到小数点后两位。例如：20.00，此金额将会在支付时显示给用户确认)，     必填
        productName = params['orderName']  # String(50)    商品名称。此名称将会在支付时显示给用户确认   必填
        requestId = params['orderPlatformId']  # String(30)    开发者支付订单号。注：最长30字节。其值由开发者定义生成，用于标识一次支付请求，每次请求需唯一，不可重复。
        productDesc = params['orderName']  # String(100)    商户对商品的自定义描述 。 必填，不能为空

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
        mo.setResult('payData', rparam)
        pass

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
                TyContext.ftlog.debug('k====>', k, 'v====>', v, 'ret==>', ret)
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
            appId = TyContext.ServerControl.get_appid_frm_order_id(orderPlatformId)
            hwapps = TuyouPayHuaWei.HWAPPS[str(appId)]
            isOk = self.__check_ras_code__(hwapps, rparam, False)
            if isOk:
                total_fee = int(float(rparam['amount']))
                try:
                    # huawei sdk also use payType, which is tuyou's sub_paytype
                    rparam['sub_paytype'] = rparam['payType']
                    del rparam['payType']
                except:
                    pass
                isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, 'TRADE_FINISHED', rparam)
                if isOk:
                    return '{"result":0}'
                else:
                    return '{"result":3}'
            else:
                return '{"result":1}'
        except:
            TyContext.ftlog.exception()
            return '{"result":94}'
