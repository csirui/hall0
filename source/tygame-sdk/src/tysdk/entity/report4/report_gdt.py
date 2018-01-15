#! encoding=utf-8
import base64
import hashlib
import time
import urllib

from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class ReportGDT:
    def __init__(self):
        # self.sign_key = 'b45c095c5419e693'
        # self.encrypt_key = 'BAAAAAAAAAAAESMp'
        self.sign_key = '8664b9b95623ed82'
        self.encrypt_key = 'BAAAAAAAAAAAFhJI'

    @classmethod
    def handle_click(self, rparams):
        muid = rparams.get('muid', '')
        # advertiser_id = rparams.get('advertiser_id', '')
        # appid = rparams.get('appid' ,'')
        # app_type = rparams.get('app_type', '')
        # click_id = rparams.get('click_id', '')
        # click_time = rparams.get('click_time', '')
        key = 'report:gdt:%s' % muid
        if rparams:
            datas = reduce(tuple.__add__, rparams.items())
        else:
            datas = ('key', 'value')
        TyContext.RedisPayData.execute('HMSET', key, *datas)
        TyContext.RedisPayData.execute('EXPIRE', key, 3600)

        TyContext.ftlog.info("UNIVERSAL_LOG_GDT", 'gdt_params=', rparams)

        return '{"ret": 0, "msg": "success"}'

    def handle_register(self, userId, rparams):
        clientId = rparams.get('clientId', '')
        if clientId.startswith('IOS_'):
            self.handle_register_ios(userId, rparams)
        elif clientId.startswith('Android_'):
            self.handle_register_android(userId, rparams)

    def handle_register_ios(self, userId, rparams):
        idfa = rparams.get('idfa', '').upper()
        muid = hashlib.md5(idfa).hexdigest()
        self.handle_regiester_common(muid, rparams)

    def handle_register_android(self, userId, rparams):
        idfa = rparams.get('imei', '').lower()
        muid = hashlib.md5(idfa).hexdigest()
        self.handle_regiester_common(muid, rparams)

    def handle_regiester_common(self, muid, rparams):
        key = 'report:gdt:%s' % muid
        click_id, appid, app_type, advertiser_id = TyContext.RedisPayData.execute('HMGET', key, 'click_id', 'appid',
                                                                                  'app_type', 'advertiser_id')
        if appid and app_type and advertiser_id:
            query_string = 'click_id=%s&muid=%s&conv_time=%s' % (click_id, muid, int(time.time()))
            page = 'http://t.gdt.qq.com/conv/app/%s/conv?%s' % (appid, query_string)
            encode_page = urllib.quote(page)
            property = '%s&GET&%s' % (self.sign_key, encode_page)
            signature = hashlib.md5(property).hexdigest()
            base_data = '%s&sign=%s' % (query_string, signature)
            data = base64.b64encode(self.simple_xor(base_data, self.encrypt_key))
            url = 'http://t.gdt.qq.com/conv/app/%(appid)s/conv?v=%(data)s&conv_type=MOBILEAPP_ACTIVITE&app_type=%(app_type)s&advertiser_id=%(advertiser_id)s' % {
                'appid': appid,
                'app_type': app_type,
                'advertiser_id': advertiser_id,
                'data': data,
            }
            response, _ = TyContext.WebPage.webget(url)
            TyContext.ftlog.info('ReportGDT->handle_regiester_common', 'request url', url, 'response', response)

    def simple_xor(self, source, key):
        retval = ''
        j = 0
        for ch in source:
            retval = retval + chr(ord(ch) ^ ord(key[j]))
            j = j + 1
            j = j % (len(key))
        return retval
