# -*- coding: utf-8 -*-

import json
import urllib

from advertise import AdvertiseService, is_valid_mac, is_valid_idfa, is_valid_macmd5
from tyframework.context import TyContext


class AdsShike(object):
    @classmethod
    def get_spname(cls):
        return 'shike'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsShike.ads_clicked rparams:', rparams)
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
            ip = rparams['ip']
        except:
            ip = rparams['clkip']
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
        if 'callback' in rparams and rparams['callback'] != '':
            note = '{"callback_url":"' + rparams['callback'] + '"}'
            AdvertiseService.record_click(ids, ip, cls.get_spname(), note)
        else:
            AdvertiseService.record_click(ids, ip, cls.get_spname())

        return 200

    @classmethod
    def user_activated(cls, params):
        TyContext.ftlog.info('AdsShike.user_activated, params:', params)
        try:
            if not params['note']:
                TyContext.ftlog.error('AdsShike.user_activated note is None, params:', params)
            note = json.loads(params['note'])
            url = urllib.unquote(note['callback_url']).decode('utf8')
            response, final_url = TyContext.WebPage.webget(url, postdata_=None, method_='GET')
            TyContext.ftlog.info('AdsShike.user_activated response:', response, url)
            response_json = json.loads(response)
            if response_json['message'] != 'ok':
                TyContext.ftlog.error('AdsShike.user_activated postback reponse', response)
            return 'thankyou'
        except:
            TyContext.ftlog.exception('AdsShike.user_activated ERROR')
            return 'AdsShike.error'
