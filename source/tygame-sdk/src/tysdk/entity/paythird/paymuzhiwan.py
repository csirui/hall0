# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class TuYouPayMuzhiwan(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        buttonId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('muzhiwan_prodids', {})
        data = prodconfig[str(appId)].get(str(buttonId), None)

        if data:
            payCode = data['feecode']
        else:
            raise Exception('can not find muzhiwan product define of buttonId=' + buttonId)

        chargeinfo['chargeData'] = {'msgOrderCode': payCode}

    @classmethod
    def doMuzhiwanCallback(cls, rpath):
        from payyi import TuYouPayYi
        return TuYouPayYi.do_yipay_callback('muzhiwan')
