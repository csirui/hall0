# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap


class TuYouPayZhangQu():
    # 订单签名验证key
    sign_skey = 'zhangqutuyou'

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        prodId = params['prodId']

        payCode = ''
        orderPhone = ''
        if prodId == 'T20K' or prodId == 'CARDMATCH10' or prodId == 'MOONKEY' or prodId == 'TGBOX1' or prodId == 'T3_NS_COIN_2' or prodId == 'COIN8' or prodId == 'TEXAS_COIN1' or prodId == 'C2':
            payCode = 'YY,11,10026'
            orderPhone = '10658035616002'

        sortOrderId = ShortOrderIdMap.get_short_order_id(params['orderPlatformId'])
        payData = {'msgOrderCode': payCode, 'orderPhone': orderPhone, 'sortOrderId': sortOrderId}
        params['payData'] = payData
        mo.setResult('payData', payData)

        pass

    @classmethod
    def __set_order_mobile__(self, orderPlatformId, mobile):
        try:
            if mobile != '':
                baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId),
                                                          'PAY_STATE_CHARGE')
                baseinfo = json.loads(baseinfo)
                baseinfo['vouchMobile'] = mobile
                TyContext.RedisPayData.execute('HSET', 'platformOrder:' + str(orderPlatformId), 'PAY_STATE_CHARGE',
                                               json.dumps(baseinfo))
        except:
            TyContext.ftlog.info('doZhangQuCallback->set mobile error', 'orderPlatformId=', orderPlatformId, 'mobile=',
                                 mobile)

    @classmethod
    def doZhangQuCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()

        sortOrderId = ''
        linkid = ''
        feecode = 0
        try:
            mobileId = rparam['mobile']
            productCode = rparam['code']
            region = rparam['region']
            feecode = rparam['feecode']
            linkid = rparam['linkid']
            goodsInf = rparam['p']
            sortOrderId = str(goodsInf)[-6:]
            sign = rparam['sign']
            desc = rparam['desc']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doZhangQuCallback->ERROR, param error !! rparam=', rparam)
            return 'param error'

        # 效验sign
        tSign = str(mobileId) + str(linkid) + str(productCode) + TuYouPayZhangQu.sign_skey
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if sign != vSign:
            TyContext.ftlog.info('doZhangQuCallback->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return 'sign error'
        if sortOrderId == '':
            TyContext.ftlog.info('doZhangQuCallback->ERROR, orderPlatformId error !! sortOrderId=', sortOrderId,
                                 'goodsInf=', goodsInf)
            return 'orderPlatformId error'

        orderPlatformId = ShortOrderIdMap.get_long_order_id(sortOrderId)
        if len(orderPlatformId) != 14:
            TyContext.ftlog.info('doZhangQuCallback->ERROR, orderPlatformId error !! sortOrderId=', sortOrderId,
                                 'goodsInf=', goodsInf, 'orderPlatformId=', orderPlatformId)
            return 'orderPlatformId error'

        TyContext.RunMode.get_server_link(orderPlatformId)

        # 把手机号补充到订单信息里
        self.__set_order_mobile__(orderPlatformId, mobileId)

        if str(productCode) == '21000':
            from tysdk.entity.pay.pay import TuyouPay
            trade_status = 'TRADE_FINISHED'
            total_fee = int(int(feecode) / 100)

            isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
            if isOk:
                return linkid
            else:
                return 'charge fail'

        return 'charge fail'

        pass
