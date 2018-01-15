# -*- coding=utf-8 -*-
''' 广告 '''

from tysdk.entity.ads.advertise import AdvertiseService
from tysdk.entity.user3.account_check import AccountCheck


class HttpAds(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
            }
            AccountCheck.__init_checker__()
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                '/open/v3/adsclicked/duomeng': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/chukong': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/limei': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/youmi': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/dianru': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/wanpu': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/omygreen': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/juzhuanqian': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/gdt': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/quzhuan': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/qianjia': AdvertiseService.ads_clicked,
                '/open/v3/adsclicked/shike': AdvertiseService.ads_clicked,
                '/open/v3/user/adnotifycallback': AdvertiseService.user_activated,
                '/open/v3/user/created': AdvertiseService.user_created,
                '/open/v3/adsclicked/checkidfa': AdvertiseService.check_idfas,
            }
            AccountCheck.__init_checker__()
        return cls.HTMLPATHS
