# -*- coding: utf-8 -*-

import json
import urllib

from advertise import AdvertiseService, is_valid_mac, is_valid_idfa, is_valid_macmd5
from tyframework.context import TyContext


class AdsOmygreen(object):
    @classmethod
    def get_spname(cls):
        return 'omygreen'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsOmygreen.ads_clicked rparams:', rparams)
        try:
            appId = int(rparams['appid'])
        except:
            appId = 0
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
        macmd5 = ''
        if is_valid_macmd5(mac):
            macmd5 = mac
            mac = ''
        elif not is_valid_mac(mac):
            mac = ''

        ids = {}
        ids['iosappid'] = appId
        ids['mac'] = mac.lower()
        ids['macmd5'] = macmd5.lower()
        ids['idfa'] = idfa.lower()
        note = '{"callback_url":"' + rparams['callback'] + '"}'
        AdvertiseService.record_click(ids, rparams['clkip'], cls.get_spname(), note)

        return 'success'

    @classmethod
    def user_activated(cls, params):
        TyContext.ftlog.info('AdsOmygreen.user_activated, params:', params)
        try:
            if not params['note']:
                TyContext.ftlog.error('AdsOmygreen.user_activated note is None, params:', params)
            note = json.loads(params['note'])
            url = urllib.unquote(note['callback_url']).decode('utf8')
            response, final_url = TyContext.WebPage.webget(url, postdata_=None, method_='GET')
            TyContext.ftlog.info('AdsOmygreen.user_activated response:', response, url)
            response_json = json.loads(response)
            if int(response_json['code']) != 0:
                TyContext.ftlog.error('AdsOmygreen.user_activated postback reponse', response)
            return 'thankyou'
        except:
            TyContext.ftlog.exception('AdsOmygreen.user_activated ERROR')
            return 'AdsOmygreen.error'
