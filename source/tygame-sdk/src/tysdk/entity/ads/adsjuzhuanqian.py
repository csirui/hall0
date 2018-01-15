# -*- coding: utf-8 -*-

import json

from advertise import AdvertiseService, is_valid_idfa
from tyframework.context import TyContext


class AdsJuzhuanqian(object):
    @classmethod
    def get_spname(cls):
        return 'juzhuanqian'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsJuzhuanqian.ads_clicked rparams:', rparams)
        try:
            idfa = rparams['idfa']

            if not is_valid_idfa(idfa):
                idfa = ''
        except Exception as e:
            TyContext.ftlog.error('AdsJuzhuanqian.ads_clicked idfa err', e)
            idfa = ''
        try:
            appId = int(rparams['app_id'])
        except Exception as e:
            TyContext.ftlog.error('AdsJuzhuanqian.ads_clicked appId err', e)
            appId = 0
        try:
            appSerect = rparams['app_secret']
        except Exception as e:
            TyContext.ftlog.error('AdsJuzhuanqian.ads_clicked appId err', e)
            appSerect = ''
        if not idfa and not appId and not appSerect:
            return 'fail'
        ids = {}
        ids['iosappid'] = appId
        ids['idfa'] = idfa.lower()
        if 'callback' not in rparams:
            callback = 'http://prd.51remai.cn/api/partner/notify'
        note = '{"callback":"' + callback + '","appSerect":"' + appSerect + '"}'
        AdvertiseService.record_click(ids, rparams['clkip'], cls.get_spname(), note)
        return 'success'

    @classmethod
    def user_activated(cls, params):
        if not params['note']:
            TyContext.ftlog.error('AdsJuzhuanqian.user_activated note is None, params:', params)
        note = json.loads(params['note'])
        url = note['callback']
        post_param = {}
        post_param['app_id'] = params['iosappid']
        post_param['app_secret'] = note['appSerect']
        post_param['idfa'] = params['idfa'].upper()
        try:
            response, final_url = TyContext.WebPage.webget(url, querys=post_param, method_='GET')
        except:
            TyContext.ftlog.exception()
        return 'thankyou'
