# -*- coding=utf-8 -*-

import urllib
from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper


class TuyouPayMo9pay(object):
    pay_url = 'https://www.mo9.com/gateway/mobile.shtml?m=mobile&'
    return_url = 'http://www.tuyoo.com/mo9/success'

    @classmethod
    def doPayRequestMo9(cls, params):
        mo = TyContext.Cls_MsgPack()
        mo9appId = params['mo9appId']
        mo9config = TyContext.Configure.get_global_item_json('mo9_config', {})
        config = mo9config.get(str(mo9appId), None)
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/mo9/callback'
        if config:
            mo9account = str(config['account'])
            mo9key = str(config['paykey'])
        else:
            raise Exception('can not find mo9pay config info define of mo9appId=' + str(mo9appId))
        paydata = {'pay_to_email': mo9account,
                   'version': '2.1',
                   'return_url': cls.return_url,
                   'notify_url': notifyurl,
                   'invoice': params['orderPlatformId'],
                   'payer_id': str(params['userId']),
                   'lc': 'CN',
                   'amount': str(float(params['orderPrice'])),
                   'currency': 'CNY',
                   'item_name': params['orderName'],
                   'app_id': mo9appId,
                   }
        paydata['sign'] = cls.__cal_sign(paydata, mo9key)
        urlparams = '&'.join(k + "=" + urllib.quote(paydata[k].encode('utf-8')) for k in sorted(paydata.keys()))
        openUrl = cls.pay_url + urlparams
        payData = {'openurl': openUrl}

        mo.setResult('code', 0)
        mo.setResult('payData', payData)
        return mo

    @classmethod
    def doMo9payCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuyouPayMo9pay.doMo9payCallbackin rparam=', rparam)

        try:
            mo9appId = str(rparam['app_id'])
            orderPlatformId = rparam['invoice']
            mo9config = TyContext.Configure.get_global_item_json('mo9_config', {})
            config = mo9config.get(mo9appId, None)
            mo9paykey = str(config['paykey'])
            sign = rparam['sign']
        except:
            TyContext.ftlog.info('doMo9payCallback->ERROR, param error !! rparam=', rparam)
            TyContext.ftlog.exception()
            return "error"

        # 签名校验
        if not cls.__verify_sign(rparam, mo9paykey, sign):
            TyContext.ftlog.error('TuyouPayMo9pay.doMo9payCallback verify error !!')
            return "ILLEGAL SIGN"

        from tysdk.entity.pay.pay import TuyouPay
        trade_status = 'TRADE_FINISHED'
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)
        if isOk:
            return "OK"
        else:
            return "error"

    @classmethod
    def __cal_sign(cls, rparam, key):
        check_str = '&'.join(k + "=" + rparam[k] for k in sorted(rparam.keys()) if k != 'sign') \
                    + key
        m = md5()
        m.update(check_str.encode('utf-8'))
        digest = m.hexdigest().upper()
        return digest

    @classmethod
    def __verify_sign(cls, rparam, key, sign):
        check_str = '&'.join(k + "=" + rparam[k] for k in sorted(rparam.keys()) if k != 'sign') \
                    + key
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().upper()
        if digest != sign:
            TyContext.ftlog.error('TuyouPayMo9pay verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
