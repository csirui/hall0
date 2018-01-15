# -*- coding=utf-8 -*-

import json

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4


class TuYouPay360V4(PayBaseV4):
    __name__ = "TuYouPay360V4"
    # 商户id和密钥，由360提供
    merchant_code = "3337100050"
    merchant_security_code = "53c3985592a0dced717c014092d7718b"

    # 360支付url
    pay_request_url = "https://mpay.360.cn/gateway/do?"
    query_request_url = "http://query.mpay.360.cn/trans/get?"
    no_notify_url = "http://mpay.360.cn/noReturn/notify"

    notify_url = "/v1/pay/360/callback"

    bank_code = ['MOBILE_ZFB', 'SZX_CARD', 'LT_CARD', 'DX_CARD', 'JCARD', 'QIHU_CARD']
    bank_code2charge_type_dict = {'MOBILE_ZFB': '360.ali',
                                  'SZX_CARD': '360.card.yd',
                                  'LT_CARD': '360.card.lt',
                                  'DX_CARD': '360.card.dx',
                                  'JCARD': None,
                                  'QIHU_CARD': None}
    trans_service = 'direct_pay'
    input_cha = 'UTF-8'
    sign_type = 'MD5'

    reqSeq = 0

    @payv4_order('360.ali')
    def handle_order(self, mi):
        chargeInfo = self.get_charge_info(mi)
        mo = TyContext.Cls_MsgPack()
        try:
            self.doPayRequestAli(chargeInfo, mi, mo)
        except:
            raise PayErrorV4(1, "阿里支付请求错误")
        paydata = mo.getResult("payData")
        payData = {}
        payData['360ali_config'] = paydata
        return self.return_mo(0, chargeInfo=chargeInfo, payData=payData)

    @classmethod
    def doPayRequestAli(cls, chargeInfo, mi, mo):
        return cls._pay_request(chargeInfo, mi, mo, 0)

    @classmethod
    def doPayRequestCardYd(cls, chargeInfo, mi, mo):
        return cls._pay_request(chargeInfo, mi, mo, 1)

    @classmethod
    def doPayRequestCardLt(cls, chargeInfo, mi, mo):
        return cls._pay_request(chargeInfo, mi, mo, 2)

    @classmethod
    def doPayRequestCardDx(cls, chargeInfo, mi, mo):
        return cls._pay_request(chargeInfo, mi, mo, 3)

    @classmethod
    def _pay_request(cls, chargeInfo, mi, mo, bankIndex):

        rparam = cls._get_pay_requset_params(chargeInfo, mi, mo, bankIndex)
        if not rparam:
            return PayConst.CHARGE_STATE_REQUEST_RETRY

        purl = cls.pay_request_url + PayHelperV4.createLinkString4Get(rparam)

        TyContext.ftlog.info(cls.__name__, '_pay_request->return bankIndex=', bankIndex, 'purl=', purl)
        response, purl = TyContext.WebPage.webget(purl)
        TyContext.ftlog.info(cls.__name__, '_pay_request->return bankIndex=', bankIndex, 'purl=', purl, 'response=',
                             response)

        if response == None:
            response = ''
        else:
            response = response.strip()

        mo.setResult('payData', '')
        if response[0:7] == 'success':
            return PayConst.CHARGE_STATE_REQUEST
        elif response[0] == '{':
            try:
                jsondatas = json.loads(response)
                if jsondatas['code'] == 'success':
                    mo.setResult('payData', jsondatas['paydata'])
                else:
                    if 'info' in jsondatas:
                        errInfo = jsondatas['info']
                        mo.setResult('info', jsondatas['info'])
                    else:
                        errInfo = '360充值请求错误'
                        raise PayErrorV4(1, errInfo)
                    mo.setError(1, errInfo)
                return PayConst.CHARGE_STATE_REQUEST
            except:
                pass

        i = response.find('<h2>[')
        if i > 0:
            j = response.find('</h2>', i)
            errInfo = response[i + 4: j]
            errInfo = errInfo.decode('gb2312')
            mo.setError(1, errInfo)
            return PayConst.CHARGE_STATE_REQUEST_IGNORE
        else:
            try:
                errInfo = response.decode('gb2312')
            except:
                errInfo = response
            if errInfo.find('failed:') == 0:
                errInfo = errInfo[7:]
                raise PayErrorV4(1, errInfo)
            mo.setError(1, errInfo)
            return PayConst.CHARGE_STATE_ERROR_REQUEST

    @classmethod
    def _get_pay_requset_params(cls, chargeInfo, mi, mo, bankIndex):
        cls.reqSeq += 1
        rparam = {}
        # 如果同一个事务，发送第一次请求，失败，360认为此事务已被占用，必须使用不同的事务ID
        rparam['mer_trade_code'] = chargeInfo['platformOrderId'] + '-' + str(cls.reqSeq)
        rparam['rec_amount'] = float(chargeInfo['chargeTotal'])
        rparam['product_name'] = chargeInfo['buttonName']
        rparam['mer_code'] = cls.merchant_code
        rparam['trans_service'] = cls.trans_service
        rparam['input_cha'] = cls.input_cha
        rparam['sign_type'] = cls.sign_type
        rparam['notify_url'] = PayHelperV4.getSdkDomain() + cls.notify_url
        rparam['return_url'] = cls.no_notify_url
        rparam['bank_code'] = cls.bank_code[bankIndex]
        if bankIndex in (1, 2, 3):
            if not PayHelperV4.checkCardParam(mi, mo):
                return None
            rparam['card_amount'] = mi.getParamInt('card_amount')
            rparam['card_number'] = mi.getParamStr('card_number')
            rparam['card_pwd'] = mi.getParamStr('card_pwd')
        rparam['sign'] = cls.__build_my_sign__(rparam)
        return rparam

    @classmethod
    def __build_my_sign__(cls, rparam):
        rstr = PayHelperV4.createLinkString(rparam) + cls.merchant_security_code
        ret = PayHelperV4.md5(rstr)
        return ret

    @payv4_callback('/open/ve/pay/360/callback')
    def callback(cls, rpath):
        try:
            rparam = PayHelperV4.getArgsDict()
            TyContext.ftlog.info(cls.__name__, 'callback->rparam=', rparam)

            orderPlatformId = rparam['mer_trade_code']
            if orderPlatformId.find('-') > 0:
                orderPlatformId = orderPlatformId[0:orderPlatformId.find('-')]

            mer_code = rparam['mer_code']
            bank_pay_flag = rparam['bank_pay_flag']
            sign = rparam['sign']
            total_fee = rparam.get('pay_amount', rparam.get('rec_amount', -1))
            try:
                total_fee = float(total_fee)
            except:
                TyContext.ftlog.error(cls.__name__, 'callback fee error. total_fee', total_fee)
                total_fee = -1

            del rparam['sign']

            vSign = cls.__build_my_sign__(rparam)
            if sign != vSign:
                raise Exception('sign not equal')

            rparam['sign'] = sign

            if mer_code != cls.merchant_code:
                raise Exception('mer_code is not me !!!')

            rparam['third_orderid'] = rparam['gateway_trade_code']
            if bank_pay_flag == 'success':
                chargeType = cls.bank_code2charge_type_dict.get(rparam.get('bank_code', ''), None)
                if chargeType:
                    rparam['chargeType'] = chargeType

                isOk = PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
            else:
                bank_pay_flag = bank_pay_flag.decode('utf-8')
                isOk = PayHelperV4.callback_error(orderPlatformId, bank_pay_flag, rparam)
            if isOk:
                return 'success'
        except:
            TyContext.ftlog.exception()

        return 'error'
