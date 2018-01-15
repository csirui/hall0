# -*- coding=utf-8 -*-
#################################################
# 联想单机获取支付方式和支付结果回掉的主要逻辑实现
# Created by Zhang Shibo at 2015/11/12
# Version: v1.8
#################################################
import base64
import json

from OpenSSL.crypto import load_privatekey, FILETYPE_PEM, sign

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYouPayLenovoDanjiV4(PayBaseV4):
    @payv4_order('lenovodj')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        appId = mi.getParamStr('lenovodj_openId', None)
        if not appId:
            raise PayErrorV4(1, '请检查一下是否有联想单机的openId')

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
            # raise PayErrorV4(1,'【联想单机】openId[%s]对应的参数没有找到！' % appId)

        # 前端不要private key开头和结尾的字符
        appKey = appKey.replace('-----BEGIN PRIVATE KEY-----\n', '').replace('\n-----END PRIVATE KEY-----', '')
        if data:
            payCode = data['feecode']
        if not payCode or not appKey:
            config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('lenovodj',
                                                                                                  chargeinfo[
                                                                                                      'packageName'],
                                                                                                  chargeinfo[
                                                                                                      'mainChannel'])
            prodconfig = config.get('products', {})
            diamondList = filter(lambda x: diamondId in x.values(), prodconfig)
            diamondConfig = diamondList[0] if diamondList else {}
            payCode = diamondConfig.get('code', '')
            appKey = config.get('lenovo_appKey', '')
            if not payCode or not appKey:
                raise PayErrorV4(1, '【联想单机】没有找到计费点！');
        chargeinfo['chargeData'] = {'msgOrderCode': payCode, 'appKey': appKey}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/lenovodj/callback')
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
            ChargeModel.save_third_pay_order_id(orderPlatformId, transdata.get('transid'))
        except Exception as e:
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback ERROR:', e)
            return 'FAILURE'

        if '0' != str(result):
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback ERROR, sign error !! rparam=', rparam,
                                  'sign=', sign)
            PayHelperV4.callback_error(orderPlatformId, '支付失败', transdata)
            return 'FAILURE'

        appkeyconfig = TyContext.Configure.get_global_item_json('lenovodanji_config', {})
        if not appkeyconfig:
            TyContext.ftlog.error(
                'TuYouPayLenovoDanji->doLenovoDanjiCallback Doesn\'t find appkeyconfig by lenovodanji_config')

        for item in appkeyconfig:
            if 0 == cmp(appid, item['appId']):
                lenovodanji_prikey_str = item['appKey']
                break
        else:
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback Doesn\'t find appkey by appid:', appid)
            config = GameItemConfigure.get_game_channel_configure_by_orderId(orderPlatformId, 'lenovodj')
            lenovodanji_prikey_str = cls.loadRsaPrivateKey(config.get('lenovo_appKey', ""))

        if not cls.verifySign(lenovodanji_prikey_str, verifyData, signStr):
            TyContext.ftlog.error('TuYouPayLenovoDanji->doLenovoDanjiCallback ERROR, sign error')
            return 'FAILURE'

        transdata['sub_paytype'] = paytype
        PayHelperV4.callback_ok(orderPlatformId, float(total_fee) / 100, transdata)
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
