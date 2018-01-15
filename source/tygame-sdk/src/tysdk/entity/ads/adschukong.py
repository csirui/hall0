# -*- coding: utf-8 -*-

import json

from advertise import AdvertiseService, is_valid_mac, is_valid_idfa, is_valid_macmd5
from tyframework.context import TyContext


class AdsChukong(object):
    @classmethod
    def get_spname(cls):
        return 'chukong'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsChukong.ads_clicked rparams:', rparams)
        try:
            idfa = rparams['idfa']
            if not is_valid_idfa(idfa):
                idfa = ''
        except:
            idfa = ''
        try:
            mac = rparams['mac']
        except:
            mac = ''
        try:
            appId = int(rparams['appId'])
        except:
            appId = 0
        macmd5 = ''
        if is_valid_macmd5(mac):
            macmd5 = mac
            mac = ''
        elif not is_valid_mac(mac):
            mac = ''
        if 'callback' not in rparams:
            rparams['callback'] = 'http://stats.cocounion.com/event/chukong/546bfa980efa549b77000011'

        ids = {}
        ids['iosappid'] = appId
        ids['mac'] = mac.lower()
        ids['macmd5'] = macmd5.lower()
        ids['idfa'] = idfa.lower()
        note = '{"os":"' + rparams['os'] + '","callback":"' + rparams['callback'] + '"}'
        AdvertiseService.record_click(ids, rparams['clkip'], cls.get_spname(), note)

        return 'success'

    @classmethod
    def user_activated(cls, params):
        del params['iosappid']
        if 'idfa' in params:
            params['idfa'] = params['idfa'].upper()
        if 'mac' in params:
            params['mac'] = params['mac'].upper()
        if not params['note']:
            TyContext.ftlog.error('AdsChukong.user_activated note is None, params:', params)
        note = json.loads(params['note'])
        url = note['callback']
        params['os'] = note['os']
        del params['clkip']
        del params['acttime']
        del params['clktime']
        del params['ip']
        del params['note']
        try:
            response, final_url = TyContext.WebPage.webget(url, postdata_=params, method_='GET')
        except:
            TyContext.ftlog.exception()
        return 'thankyou'
