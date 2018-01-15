# -*- coding: utf-8 -*-

import json
import urllib

from advertise import AdvertiseService, is_valid_mac, is_valid_idfa, is_valid_macmd5
from tyframework.context import TyContext


class AdsWanpu(object):
    @classmethod
    def get_spname(cls):
        return 'wanpu'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsWanpu.ads_clicked rparams:', rparams)

        try:
            appId = int(rparams['app'])
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
        note = '{"callbackurl":"' + rparams['callbackurl'] + '"}'
        AdvertiseService.record_click(ids, rparams['clkip'], cls.get_spname(), note)

        return '{"success":true,"message":"成功"}'

    @classmethod
    def user_activated(cls, params):
        if not params['note']:
            TyContext.ftlog.error('AdsWanpu.user_activated note is None, params:', params)
        note = json.loads(params['note'])
        url = urllib.unquote(note['callbackurl']).decode('utf8')
        response, final_url = TyContext.WebPage.webget(url, postdata_=None, method_='GET')
        response = json.loads(response)
        if not response['success'] or str(response['success']) != 'true':
            TyContext.ftlog.error('AdsWanpu.user_activated postback reponse', response)
        return 'thankyou'
