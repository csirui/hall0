# -*- coding: utf-8 -*-

import json

from advertise import AdvertiseService, is_valid_mac, is_valid_idfa, is_valid_macmd5
from tyframework.context import TyContext


class AdsDianru(object):
    @classmethod
    def get_spname(cls):
        return 'dianru'

    @classmethod
    def get_activate_callback_url(cls):
        return 'http://api.mobile.dianru.com/callback/index.do'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsDianru.ads_clicked rparams:', rparams)
        try:
            appId = int(rparams['appId'])
        except:
            appId = 0

        try:
            idfa = rparams['drkey'][32:]
            if not is_valid_idfa(idfa):
                idfa = ''
        except:
            idfa = ''

        try:
            mac = rparams['drkey'][32:]
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
        note = '{"drkey":"' + rparams['drkey'] + '"}'
        AdvertiseService.record_click(ids, rparams['clkip'], cls.get_spname(), note)

        return 'success'

    @classmethod
    def user_activated(cls, params):
        postparams = {}
        if not params['note']:
            TyContext.ftlog.error('AdsDianru.user_activated note is None, params:', params)
        note = json.loads(params['note'])
        url = cls.get_activate_callback_url()
        postparams['drkey'] = note['drkey']
        if 'ip' in params:
            postparams['ip'] = params['ip']
        else:
            postparams['ip'] = params['clkip']
        response, final_url = TyContext.WebPage.webget(url, postparams)
        response = json.loads(response)
        if not response['status']:
            TyContext.ftlog.error('AdsDianru.user_activated postback reponse', response)
        return 'thankyou'
