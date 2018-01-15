# -*- coding: utf-8 -*-

from advertise import AdvertiseService
from tyframework.context import TyContext


class AdsQianjia(object):
    @classmethod
    def get_spname(cls):
        return 'qianjia'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsQianjia.ads_clicked rparams:', rparams)

        try:
            clickIp = rparams['ip']
            idfa = rparams['idfa']
            appid = rparams['appid']
        except Exception as e:
            TyContext.ftlog.error('AdsQianjia->ads_clicked ERROR: ', e)
            return 0

        ids = {}
        ids['iosappid'] = appid
        ids['idfa'] = idfa.lower()
        AdvertiseService.record_click(ids, clickIp, cls.get_spname())

        return 200

    @classmethod
    def user_activated(cls, params):
        return 'thankyou'
