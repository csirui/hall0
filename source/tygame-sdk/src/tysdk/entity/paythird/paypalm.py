# -*- coding=utf-8 -*-

import urllib
from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayPalm():
    @classmethod
    def doPayRequestCard(cls, chargeinfo, mi, mo):
        userId = chargeinfo['uid']
        platformOrderId = chargeinfo['platformOrderId']
        price = int(float(chargeinfo['chargeTotal'])) * 100
        prodname = unicode(chargeinfo['diamondName'])
        payurl = cls.__create_order(userId, price, platformOrderId, prodname)
        if not payurl:
            mo.setError('code', 1)
            mo.setError('info', error)
            return PayConst.CHARGE_STATE_ERROR_REQUEST
        payData = {'openurl': payurl}
        mo.setResult('payData', payData)
        return PayConst.CHARGE_STATE_REQUEST

    @classmethod
    def __create_order(cls, userId, amount, orderPlatformId, prodname):
        palmconfig = TyContext.Configure.get_global_item_json('palm_config', {})
        createorder_url = palmconfig['createorder_url']
        payurl = None
        key = palmconfig['key']
        merc_id = palmconfig['merc_id']
        params = {}
        params['opCode'] = '33A11H'
        params['payAmt'] = str(amount)
        params['merUserId'] = userId
        params['productId'] = '100001'
        params['orderType'] = 'collect'
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/palm/callback'
        returnurl = PayHelper.getSdkDomain() + '/v1/pay/palm/closeview/callback?orderid=' + orderPlatformId
        params['notifyUrl'] = notifyurl
        params['returnUrl'] = returnurl
        params['merOrderNo'] = orderPlatformId
        params['merId'] = merc_id
        params['orderDesc'] = prodname
        params['userId'] = ''
        params['sign'] = cls.__cal_sign(params, key)
        response_msg, final_url = TyContext.WebPage.webget(createorder_url, postdata_=params)
        response = response_msg.split('&')
        for value in response:
            param = value.split('=')
            if 'tranResult' in param and str(param[1]) != '000000':
                TyContext.ftlog.error('TuYouPayPalm createorder ERROR! params=',
                                      params, ' response=', response)
                return None
            if 'orderNo' in param:
                params = {}
                params['opCode'] = '33A12H'
                params['merId'] = merc_id
                params['orderNo'] = param[1]
                params['sign'] = cls.__cal_sign(params, key)
                payurl = createorder_url + '?' + urllib.urlencode(params)
        return payurl

    @classmethod
    def doPalmCallback(cls, rpath):
        palmconfig = TyContext.Configure.get_global_item_json('palm_config', {})
        key = palmconfig['key']
        rparam = TyContext.RunHttp.convertArgsToDict()
        try:
            orderPlatformId = rparam['merOrderNo']
            sign = rparam['sign']
            status = int(rparam['tranResult'])
        except Exception as e:
            TyContext.ftlog.error('doPalmCallback->ERROR, exception', e, 'rparam', rparam)
            return 'error'

        # 签名校验
        if not cls.__verify_sign(rparam, sign, key):
            return 'error'

        total_fee = float(rparam.get('payAmt', -1)) / 100
        rparam['third_orderid'] = rparam['orderNo']
        rparam['chargeType'] = 'palm.card'
        if status != '000000':
            isOk = PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        else:
            PayHelper.callback_error(orderPlatformId, str(rparam['resultInfo']), rparam)
        return 'success'

    @classmethod
    def doPalmCloseCallback(cls, rpath):
        return TyContext.CloseWebView.getCloseHtml()

    @classmethod
    def __cal_sign(cls, params, key):
        check_str = '&'.join(k + "=" + str(params[k]) for k in sorted(params.keys()) if k != 'sign')
        check_str += key
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        return digest

    @classmethod
    def __verify_sign(cls, rparam, sign, key):
        check_str = '&'.join(k + "=" + str(rparam[k]) for k in sorted(rparam.keys()) if k != 'sign' and k != 'remark')
        check_str += key
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        if digest != sign:
            TyContext.ftlog.error('TuYouPayPalm.doPalmCallback verify sign failed: expected sign', sign,
                                  'calculated', digest, 'rparam', rparam, 'check_str', check_str)
            return False
        return True
