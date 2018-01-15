# -*- coding=utf-8 -*-

import base64
from binascii import unhexlify
from collections import OrderedDict
from xml.etree import ElementTree

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.duandai.smspayinfo import SmsPayInfo
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.utils.pyDes201.pyDes import triple_des, CBC, PAD_NORMAL


class TuYouPayAiDongManV4(PayBaseV4):
    createorderUrl = ''

    @payv4_order('aidongman')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        TyContext.ftlog.debug('TuYouAiDongManPay charge_data chargeinfo', chargeinfo)

        phonenum = chargeinfo.get('phone', '')
        appId = chargeinfo['appId']
        prodId = chargeinfo['diamondId']
        orderId = chargeinfo['platformOrderId']

        aidongmanConfig = TyContext.Configure.get_global_item_json('aidongmanpay_config', {})
        if aidongmanConfig:
            self.createorderUrl = aidongmanConfig['createorderUrl']

        aidongmanProdIds = TyContext.Configure.get_global_item_json('aidongmanpay_prodids', {})
        TyContext.ftlog.info('TuYouAiDongManPay charge_data aidongmanProdIds', aidongmanProdIds)
        try:
            payCode = aidongmanProdIds[str(appId)]
        except Exception as e:
            mainchannel = chargeinfo['clientId'].split('.')[-2] if chargeinfo['clientId'].split('.') else ""
            config = GameItemConfigure(appId).get_game_channel_configure_by_package('aidongman',
                                                                                    chargeinfo['packageName'],
                                                                                    mainchannel)
            productConfig = config.get('products')
            if productConfig:
                finalConfig = filter(lambda x: prodId in x.values(), productConfig)
                finalConfig = finalConfig[0] if finalConfig else []

        # 采短透传方式,短信内容(23位) + 订单信息. callback字段 Extension 返回订单信息
        paymessages = payCode[prodId]['smscodes'] + orderId

        messages = [(payCode[prodId]['smsports'], paymessages, 0)]
        no_hint = chargeinfo.get('nohint', None)
        payinfo = SmsPayInfo.build_sms_payinfo(messages, nohint=no_hint)
        SmsPayInfo.fill_in_dialog_text(
            payinfo, chargeinfo['buttonName'], chargeinfo['diamondPrice'])
        chargeinfo['chargeData'] = {'smsPayinfo': payinfo}

        return self.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/aidongman/callback')
    def doAiDongManCallback(cls, rpath):
        xmlData = TyContext.RunHttp.getRequestParam('requestData', '')
        xmlroot = ElementTree.fromstring(xmlData)
        TyContext.ftlog.info('doAiDongManCallback rparam xmlData', xmlData)

        params = OrderedDict()

        params['Behavior'] = xmlroot.find('Behavior').text
        params['Trade_status'] = xmlroot.find('Trade_status').text
        params['Trade_no'] = xmlroot.find('Trade_no').text
        params['Buyer_id'] = xmlroot.find('Buyer_id').text
        params['Extension'] = xmlroot.find('Extension').text

        sign = params['Behavior'] + params['Trade_status'] + params['Trade_no'] + params['Buyer_id'] + params[
            'Extension']

        params['Product_id'] = xmlroot.find('Product_id').text
        params['Product_name'] = xmlroot.find('Product_name').text
        params['Price'] = int(float(xmlroot.find('Price').text))
        params['App_id'] = xmlroot.find('App_id').text
        params['sign'] = xmlroot.find('Sign').text.replace(' ', '+')
        params['sign'] = ''.join(params['sign'].split())

        TyContext.ftlog.info('doAiDongManCallback params', params)

        aidongmanconfig = TyContext.Configure.get_global_item_json('aidongmanpay_config', {})
        if aidongmanconfig:
            cls.encryptKey = aidongmanconfig['3des']['encryptKey']

        # 采用3des加密
        padByte = chr(int(8 - len(sign) % 8))
        ivBytes = ''
        ivSource = aidongmanconfig['3des']['iv']
        for i in ivSource:
            ivBytes = ivBytes + chr(int(i))

        tripelDes = triple_des(unhexlify(cls.encryptKey), mode=CBC, pad=padByte, IV=ivBytes, padmode=PAD_NORMAL)
        sign = tripelDes.encrypt(sign)
        sign = base64.b64encode(sign)

        plantformId = params['Extension'][23:]
        TradeNo = xmlroot.find('Trade_no').text

        params['chargeType'] = 'aidongman'
        params['third_orderid'] = params['Trade_no']

        PayHelperV4.set_order_mobile(plantformId, params['Buyer_id'])

        TyContext.ftlog.info('doAiDongManCallback sign', sign, 'params[sign]', params['sign'])

        ResponseBody = ElementTree.Element('ResponseBody')
        Trade_no = ElementTree.SubElement(ResponseBody, 'Trade_no')
        Status = ElementTree.SubElement(ResponseBody, 'Status')
        Trade_no.text = str(TradeNo)
        Status.text = '1'
        mo = ElementTree.tostring(ResponseBody)
        if sign == params['sign']:
            if int(params['Trade_status']) == 0 or int(params['Trade_status']) == 1:
                PayHelperV4.callback_ok(plantformId, float(params['Price']), params)
                Status.text = '0'
                mo = ElementTree.tostring(ResponseBody)
                TyContext.ftlog.info('doAiDongManCallback->SUCCESS rparams', params, 'mo', mo)
                return mo
            else:
                errinfo = '爱动漫支付失败'
                PayHelperV4.callback_error(plantformId, errinfo, params)
                TyContext.ftlog.error('doAiDongManCallback->ERROR, failDesc', errinfo, 'rparams', params, 'mo', mo)
                return mo
        else:
            errinfo = '签名校验失败'
            PayHelperV4.callback_error(plantformId, errinfo, params)
            TyContext.ftlog.error('doAiDongManCallback->ERROR, failDesc', errinfo, 'rparams', params)

        return mo
