# -*- coding: utf-8 -*-

import hashlib
import json

from advertise import AdvertiseService, is_valid_mac, is_valid_idfa, is_valid_macmd5
from tyframework.context import TyContext


class AdsDuomeng(object):
    @classmethod
    def get_spname(cls):
        return 'duomeng'

    @classmethod
    def get_activate_callback_url(cls):
        return 'http://e.domob.cn/track/ow/api/postback'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsDuomeng.ads_clicked rparams:', rparams)
        try:
            idfa = rparams['ifa']
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

        ids = {}
        ids['iosappid'] = appId
        ids['mac'] = mac.lower()
        ids['macmd5'] = macmd5.lower()
        ids['idfa'] = idfa.lower()
        AdvertiseService.record_click(ids, rparams['clkip'], cls.get_spname())

        httpreq = TyContext.RunHttp.get_request()
        red_addr = cls.__get_redirect_address(appId)
        httpreq.redirect(red_addr)
        httpreq.finish()
        # hack: return 'redirected' so that execHtml will not handle the request
        return 'redirected'

    __appkeys = {
        830490089: '6c579e68fc80c85a04623edfde6184f2',
    }
    __iosappid_url = {
        830490089: 'https://itunes.apple.com/cn/app/tu-you-huan-le-dou-de-zhu/id830490089?l=zh&ls=1&mt=8',
    }

    @classmethod
    def __get_redirect_address(cls, iosappid):
        try:
            return cls.__iosappid_url[iosappid]
        except:
            TyContext.ftlog.error('AdsDuomeng __get_redirect_address missing url for iosappid', iosappid)
            return 'https://itunes.apple.com/cn/app/tu-you-huan-le-dou-de-zhu/id830490089?l=zh&ls=1&mt=8'

    @classmethod
    def __calc_sign(cls, params):
        appid = params['appId']
        udid = params.get('udid', '')
        ma = ''
        ifa = params.get('ifa', '')
        oid = ''
        key = cls.__appkeys[appid]
        return hashlib.md5('%s,%s,%s,%s,%s,%s' % (appid, udid, ma, ifa, oid, key)).hexdigest()

    @classmethod
    def user_activated(cls, params):
        params['appId'] = params['iosappid']
        del params['iosappid']
        del params['note']
        if 'idfa' in params:
            params['ifa'] = params['idfa'].upper()
            del params['idfa']
        if 'mac' in params:
            params['udid'] = params['mac'].upper()
            del params['mac']
        params['sign'] = cls.__calc_sign(params)
        url = cls.get_activate_callback_url()
        response, final_url = TyContext.WebPage.webget(url, params, method_='GET')
        response = json.loads(response)
        if not response['success']:
            TyContext.ftlog.error('AdsDuomeng.user_activated postback reponse', response)
        TyContext.ftlog.info('AdsDuomeng.user_activated reponse', response)
        return 'thankyou'
