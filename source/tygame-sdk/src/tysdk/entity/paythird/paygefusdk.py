# -*- coding=utf-8 -*-

class TuYouGeFuSdk(object):
    thirdPartyId = '43'

    @classmethod
    def charge_data(cls, chargeinfo):
        orderNo = chargeinfo['platformOrderId']
        fee = int(chargeinfo['chargeTotal']) * 100
        prodcutName = '途游斗地主'
        productDesc = chargeinfo['buttonName']
        others = chargeinfo['platformOrderId']
        chargeinfo['chargeData'] = {'orderNo': orderNo, 'fee': fee,
                                    'productName': prodcutName, 'productDesc': productDesc,
                                    'productDesc': productDesc, 'others': others, 'thirdPartyId': cls.thirdPartyId}
