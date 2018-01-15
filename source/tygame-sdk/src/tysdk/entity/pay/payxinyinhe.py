# -*- coding=utf-8 -*-
'''
Created on 2013-3-18

@author: Administrator
'''

from tyframework.context import TyContext


class TuYouPayXinYinHe(object):
    @classmethod
    def doXinYinHeCallback(self, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('doXinYinHeCallback->rparam=', rparam)

        orderPlatformId = ''
        try:
            result = rparam['result']
            payMoney = rparam['payMoney']
            orderPlatformId = rparam['orderno']
            merId = rparam['merId']
            verifyType = rparam['verifyType']
            # sign = rparam['sign']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doXinYinHeCallback->ERROR, param error !! rparam=', rparam)
            return 'fail'

        # 效验sign
        '''
        tSign = str(result)+str(payMoney)+str(orderPlatformId)+str(merId)+str(verifyType)
        m = md5()  
        m.update(tSign)  
        vSign = m.hexdigest() 
        if sign != vSign :
            TyContext.ftlog.info('doXinYinHeCallback->ERROR, sign error !! sign=', sign, 'vSign=', vSign)
            return 'fail'
        '''
        if orderPlatformId == '':
            TyContext.ftlog.info('doXinYinHeCallback->ERROR, orderPlatformId error !! orderPlatformId=',
                                 orderPlatformId)
            return 'fail'

        TyContext.RunMode.get_server_link(orderPlatformId)

        if int(result) == 1 or int(result) == 2:
            trade_status = 'TRADE_FINISHED'
            # total_fee = int(float(payMoney) / 100)
            from tysdk.entity.pay.pay import TuyouPay
            TuyouPay.doBuyChargeCallback(orderPlatformId, -1, trade_status, rparam)

        return 'success'
