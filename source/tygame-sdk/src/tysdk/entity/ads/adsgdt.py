import base64
import hashlib
import json
import time
import urllib

from advertise import AdvertiseService
from tyframework.context import TyContext


class AdsGdt(object):
    @classmethod
    def get_spname(cls):
        return 'gdt'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsGdt.ads_clicked rparams:', rparams)
        try:
            idfa = rparams['muid']
        except:
            idfa = ''
        try:
            appId = int(rparams['appid'])
        except:
            appId = 0

        if 'callback' not in rparams:
            rparams['callback'] = 'http://t.gdt.qq.com/conv/app/' + str(appId) + '/conv?'

        # clktime = rparams['click_time']
        ids = {}
        ids['iosappid'] = appId
        ids['mac'] = ''
        ids['macmd5'] = ''
        ids['idfa'] = idfa.lower()

        note = {'callback': rparams['callback'], 'clickId': rparams['click_id'],
                'advertiserId': rparams['advertiser_id']}
        strNote = ''.join(['"' + k + '"' + ':' + '"' + str(note[k]) + '"' + ',' for k in note.keys()])

        strNote = '{' + strNote[0:-1] + '}'

        AdvertiseService.record_click(ids, rparams['clkip'], cls.get_spname(), strNote)
        TyContext.ftlog.debug('AdsGdt.ads_clicked ids:', ids, 'strNote', strNote)

        return '{"ret":0,"msg":"成功"}'

    '''
    http://t.gdt.qq.com/conv/app/{appid}/conv?v={data}&conv_type={conv_type}&app_type={ app_type}&advertiser_id={uid}
    '''

    @classmethod
    def user_activated(cls, params):
        TyContext.ftlog.debug('AdsGdt.user_activate ids:params', params)
        if 'idfa' in params:
            params['idfa'] = params['idfa'].upper()
        if not params['note']:
            TyContext.ftlog.error('AdsGdt.user_activated note is None, params:', params)
        note = json.loads(params['note'])

        clickId = note['clickId']
        muid = params['idfa']
        convTime = int(time.time())
        clientIp = params['ip']

        queryString = 'muid' + '=' + muid + '&' + 'click_id' + '=' + clickId + '&' + 'conv_time' + '=' + str(
            convTime) + '&' + 'client_ip' + '=' + clientIp
        urlPage = note['callback'] + queryString
        signKey = '6bcd7d94072202a9'
        signature = cls.ConvSign(urlPage, signKey, 'GET')

        TyContext.ftlog.debug('AdsGdt.user_activated ---- step1: urlPage', urlPage, 'signature', signature)

        queryString += '&sign=' + urllib.quote_plus(signature)
        encryptKey = 'd17d39b532f924e3'
        data = cls.ConvEncrypt(queryString, encryptKey)

        TyContext.ftlog.debug('AdsGdt.user_activated ---- step2: queryString', queryString, 'data', data)

        conv_type = 'MOBILEAPP_ACTIVITE'
        app_type = 'IOS'
        advertiser_id = note['advertiserId']
        attachment = 'conv_type' + '=' + conv_type + '&' + 'app_type' + '=' + app_type + '&' + 'advertiser_id' + '=' + advertiser_id
        requestUrl = note['callback'] + 'v' + '=' + urllib.quote_plus(data) + '&' + attachment

        TyContext.ftlog.debug('AdsGdt.user_activated ---- step3: requestUrl', requestUrl)

        del params['clkip']
        del params['acttime']
        del params['clktime']
        del params['ip']
        del params['note']

        try:
            response, _ = TyContext.WebPage.webget(requestUrl, postdata_=params, method_='GET')
            ponse = json.loads(response)
            msg = '{' + 'ret:' + str(ponse['ret']) + ',' + 'msg:' + ponse['msg'] + '}'
        except Exception, e:
            TyContext.ftlog.exception()
            msg = '{' + 'ret:－1,' + 'msg:' + str(e) + '}'
        return msg

    @classmethod
    def SimpleXor(cls, source, key):
        retval = ''
        j = 0
        for ch in source:
            retval = retval + chr(ord(ch) ^ ord(key[j]))
            j = j + 1
            j = j % (len(key))
        return retval

    @classmethod
    def ConvSign(cls, page, key, method='GET'):
        encode_page = urllib.quote_plus(page)
        conv_property = key + '&' + method + '&' + encode_page
        signature = hashlib.md5(conv_property).hexdigest()
        return signature

    @classmethod
    def ConvEncrypt(cls, query_string, key):
        retval = base64.encodestring(cls.SimpleXor(query_string, key)).replace('\n', '')
        return retval
