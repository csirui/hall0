# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class TuYouPayJinri(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        appId = chargeinfo['appId']
        buttonId = chargeinfo['buttonId']
        prodconfig = TyContext.Configure.get_global_item_json('jinri_prodids', {})
        data = prodconfig[str(appId)].get(str(buttonId), None)

        if data:
            payCode = data['feecode']
        else:
            raise Exception(
                'can not find jinri product define of buttonId=' + buttonId
                + ' clientId=' + chargeinfo['clientId'])

        chargeinfo['chargeData'] = {'msgOrderCode': payCode}

    @classmethod
    def doJinriCallback(cls, rpath):
        from payyi import TuYouPayYi
        return TuYouPayYi.do_yipay_callback('jinri')
