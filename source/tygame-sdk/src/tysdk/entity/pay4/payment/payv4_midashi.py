# -*- coding=utf-8 -*-

import binascii
import hashlib
import hmac
import json
import urllib

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


######################################################################
# 米大师获取订单和支付结果回掉的主要逻辑实现
# Created by Zhangshibo at 2015/11/03
# version: v1.5
######################################################################

class TuYouPayMiDaShiV4(PayBaseV4):
    @payv4_order('midashi')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/midashi/callback')
    def doMiDaShiPayCallback(cls, rpath):
        # 由于设计到路径和请求方法，验签放到httpgateway里做了，这里只负责发货
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayMiDaShi->doMiDaShiPayCallback rparam: ', rparam)
        if 'payitem' in rparam:
            payitem = rparam['payitem']
            appmeta = payitem.split('*')[0]
            platformOrderId = appmeta
        else:
            return cls.getReturnContent(4, 'payitem')

        if 'appmeta' in rparam:
            appmeta = rparam['appmeta']
            if '*' in appmeta:
                appmeta = appmeta.split('*')[1]
            thirdPayType = appmeta
        else:
            return cls.getReturnContent(4, 'appmeta')

        if 'amt' in rparam:
            total_fee = float(rparam['amt'])
        else:
            return cls.getReturnContent(4, 'amt')

        rparam['sub_paytype'] = thirdPayType
        PayHelperV4.callback_ok(platformOrderId, -1, rparam)
        return cls.getReturnContent(0)

    @classmethod
    def getReturnContent(cls, code, info=None):
        errMap = {
            '0': '成功',
            '1': '系统繁忙',
            '2': 'token已过期',
            '3': 'token不存在',
            '4': '请求参数错误:',
        }
        if not info:
            retStr = {"ret": int(code), "msg": errMap[str(code)]}
        else:
            retStr = {"ret": int(code), "msg": errMap[str(code)] + '(' + info + ')'}
        retStr = json.dumps(retStr)
        return retStr

    @classmethod
    def verifySign(cls, params):
        rpath = TyContext.RunHttp.get_request_path()
        TyContext.ftlog.debug('TuYouPayMiDaShi->verifySign rpath: ', rpath)
        rawData = TyContext.RunHttp.get_request_raw_data()
        if len(rawData) == 0:
            TyContext.ftlog.error('TuYouPayMiDaShi->verifySign Get Raw Data ERROR!')
            return False

        rMethod = rawData[rawData.index('METHOD') + 1]
        TyContext.ftlog.debug('TuYouPayMiDaShi->verifySign rMethod: ', rMethod)
        appid = params['appid']
        sign = params['sig']
        midashiConfig = TyContext.Configure.get_global_item_json('midashi_sdk_config', {})
        for item in midashiConfig:
            if item['appid'] == appid:
                appkey = item['appkey']
                break
        else:
            TyContext.ftlog.error('TuYouPayMiDaShi->verifySign Get AppKey ERROR! appid is:[%s]' % appid)
            return False
        calcSign = cls._hmac_sha1_sig(rMethod, rpath, params, appkey + '&')
        if 0 != cmp(sign, calcSign):
            TyContext.ftlog.error(
                'TuYouPayMiDaShi->verifySign sign error. expected sign:[%s], calculate sign:[%s]' % (sign, calcSign))
            return False
        return True

    @classmethod
    def __mk_source(cls, method, url_path, params):
        for item in params.keys():
            params[item] = params[item].replace(".", "%2E")
            params[item] = params[item].replace("-", "%2D")
            params[item] = params[item].replace("_", "%5F")
        str_params = urllib.quote(
            "&".join(k + "=" + str(params[k]) for k in sorted(params.keys()) if k != 'sig' and k != 'cee_extend'),
            '')
        source = '%s&%s&%s' % (method.upper(), urllib.quote(url_path, ''),
                               str_params)
        return str(source)

    @classmethod
    def _hmac_sha1_sig(cls, method, url_path, params, secret):
        source = cls.__mk_source(method, url_path, params)
        TyContext.ftlog.debug('TuYouPayMiDaShi->_hmac_sha1_sig before sign:', source)
        hashed = hmac.new(str(secret), source, hashlib.sha1)
        decryptStr = binascii.b2a_base64(hashed.digest())[:-1]
        TyContext.ftlog.debug('TuYouPayMiDaShi->_hmac_sha1_sig after sign:', source)
        return decryptStr
