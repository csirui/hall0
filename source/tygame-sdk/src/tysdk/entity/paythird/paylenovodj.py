# -*- coding=utf-8 -*-
#################################################
# 联想单机获取支付方式和支付结果回掉的主要逻辑实现
# Created by Zhang Shibo at 2015/11/12
# Version: v1.8
#################################################
import base64
import json

from OpenSSL.crypto import load_privatekey, FILETYPE_PEM, sign

from helper import PayHelper
from tyframework.context import TyContext


class TuYouPayLenovoDanji(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        if 'payInfo' in chargeinfo and chargeinfo['payInfo']:
            payInfo = chargeinfo['payInfo']
            if 'appid' in payInfo and payInfo['appid']['lenovodj']:
                appId = payInfo['appid']['lenovodj']
        diamondId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('lenovodanji_prodids', {})
        data = None
        payCode = None
        bgname = None
        try:
            data = prodconfig[str(appId)].get(str(diamondId), None)
        except Exception as e:
            TyContext.ftlog.info('doLenovoDanji old app requested!, ', e)
        appKey = ''
        appConfig = TyContext.Configure.get_global_item_json('lenovodanji_config', {})
        for item in appConfig:
            if 0 == cmp(str(appId), item['appId']):
                appKey = item['appKey']
                break
        else:
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback Doesn\'t find appkey by appid:', appId)

        # 前端不要private key开头和结尾的字符
        appKey = appKey.replace('-----BEGIN PRIVATE KEY-----\n', '').replace('\n-----END PRIVATE KEY-----', '')
        if data:
            payCode = data['feecode']
        chargeinfo['chargeData'] = {'msgOrderCode': payCode, 'appKey': appKey}

    @classmethod
    def doLenovoDanjiCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doLenovoDanjiCallback->rparam=', rparam)
        try:
            transdata = rparam['transdata']
            verifyData = transdata
            signStr = rparam['sign']
            transdata = json.loads(transdata)
            TyContext.ftlog.debug('TuYouPayLenovoDanji->doLenovoDanjiCallback transdata: ', transdata)
            orderPlatformId = transdata['cpprivate']
            appid = transdata['appid']
            total_fee = transdata['money']
            result = transdata['result']
            paytype = transdata['paytype']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback ERROR:', e)
            return 'FAILURE'

        if '0' != str(result):
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback ERROR, sign error !! rparam=', rparam,
                                  'sign=', sign)
            PayHelper.callback_error(orderPlatformId, '支付失败', transdata)
            return 'FAILURE'

        appkeyconfig = TyContext.Configure.get_global_item_json('lenovodanji_config', {})
        if not appkeyconfig:
            TyContext.ftlog.error(
                'TuYouPayLenovoDanji->doLenovoDanjiCallback Doesn\'t find appkeyconfig by lenovodanji_config')
            return 'FAILURE'

        for item in appkeyconfig:
            if 0 == cmp(appid, item['appId']):
                lenovodanji_prikey_str = item['appKey']
                break
        else:
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback Doesn\'t find appkey by appid:', appid)
            return 'FAILURE'

        if not cls.verifySign(lenovodanji_prikey_str, verifyData, signStr):
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback ERROR, sign error')
            return 'FAILURE'

        transdata['sub_paytype'] = paytype
        PayHelper.callback_ok(orderPlatformId, float(total_fee) / 100, transdata)
        return 'SUCCESS'

    @classmethod
    def verifySign(cls, priKey, data, exceptedSign):
        TyContext.ftlog.debug('TuYouPayLenovoDanji->verifySign data: {data}, exceptsign: {excepted}'.format(
            data=data,
            excepted=exceptedSign
        ))
        key = load_privatekey(FILETYPE_PEM, priKey)
        calcSign = base64.b64encode(sign(key, data, 'sha1'))
        if 0 == cmp(calcSign, exceptedSign):
            TyContext.ftlog.debug('TuYouPayLenovoDanji->verifySign accept!')
            return True
        else:
            TyContext.ftlog.error(
                'TuYouPayLenovoDanji->verifySign excepted sign: {excepted}, calculate sign: {calculate}'.format(
                    excepted=exceptedSign,
                    calculate=calcSign
                ))
            return False
