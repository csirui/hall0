# -*- coding: utf-8 -*-
'''
Created on 2014年2月20日

@author: zjgzzz@126.com
'''
import re


class UserSession(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.KEY_USER_SESSION = '_user_session_values_'
        self.PHONETYPE_CHINAMOBILE_STR = "chinaMobile"
        self.PHONETYPE_CHINAUNION_STR = "chinaUnion"
        self.PHONETYPE_CHINATELECOM_STR = "chinaTelecom"
        self.PHONETYPE_OTHER_STR = "other"

        self.PHONETYPE_CHINAMOBILE = 0
        self.PHONETYPE_CHINAUNION = 1
        self.PHONETYPE_CHINATELECOM = 2
        self.PHONETYPE_OTHER = 3
        self.__get_zipcode_cnt = {'all': 0,
                                  'mobile': 0,
                                  'iccid': 0,
                                  'lbs': 0,
                                  'ip': 0,
                                  'missed': 0}

    def __get_session_values__(self, userId):
        extdatas = self.__ctx__.TYRun.get_tasklet_ext_datas()
        key = self.KEY_USER_SESSION + str(userId)
        datas = extdatas.get(key, {})
        if len(datas) == 0:
            gameid, devid, clientid, phoneType, client_ip, city_code, bindMobile, \
            vouchMobile, detect_phonenumber, idfa, iccid, imei, imsi, clientSdkRev = \
                self.__ctx__.RedisUser.execute(userId, 'HMGET', 'user:' + str(userId),
                                               'sessionAppId', 'sessionDevId',
                                               'sessionClientId', 'sessionPhoneType',
                                               'sessionClientIP', 'city_code',
                                               'bindMobile', 'vouchMobile',
                                               'detect_phonenumber', 'sessionIdfa',
                                               'sessionIccid', 'imei', 'imsi', 'sessionClientSdkRev')

            if phoneType == self.PHONETYPE_CHINAMOBILE or phoneType == self.PHONETYPE_CHINAMOBILE_STR:
                phoneType = self.PHONETYPE_CHINAMOBILE
            elif phoneType == self.PHONETYPE_CHINAUNION or phoneType == self.PHONETYPE_CHINAUNION_STR:
                phoneType = self.PHONETYPE_CHINAUNION
            elif phoneType == self.PHONETYPE_CHINATELECOM or phoneType == self.PHONETYPE_CHINATELECOM_STR:
                phoneType = self.PHONETYPE_CHINATELECOM
            else:
                phoneType = self.PHONETYPE_OTHER

            if devid == None:
                devid = ''
            if clientid == None:
                clientid = ''
            client_sys, client_ver, client_chanel = self.__ctx__.strutil.parse_client_id(clientid)

            try:
                city_code = self.__ctx__.strutil.loads(city_code)
            except:
                city_code = self.__ctx__.CityLocator.DEFAULT_LOCATION

            if bindMobile == None:
                bindMobile = ''
            if vouchMobile == None:
                vouchMobile = ''
            if detect_phonenumber == None:
                detect_phonenumber = ''
            if iccid is None:
                iccid = ''
            if imei is None:
                imei = ''
            if idfa is None:
                idfa = ''
            if gameid == None:
                gameid = 0
            datas['gameid'] = int(gameid)
            datas['devid'] = str(devid)
            datas['clientid'] = clientid
            datas['client_ip'] = client_ip if client_ip else ''
            datas['client_sys'] = client_sys
            datas['client_ver'] = client_ver
            datas['client_chanel'] = client_chanel
            datas['phone_type'] = phoneType
            datas['city_code_zip'] = city_code[0]
            datas['city_code_name'] = city_code[1]
            datas['bindMobile'] = bindMobile
            datas['vouchMobile'] = vouchMobile
            datas['detect_phonenumber'] = detect_phonenumber
            datas['idfa'] = idfa
            datas['iccid'] = str(iccid)
            datas['imei'] = str(imei)
            datas['imsi'] = str(imsi)
            datas['client_sdk_revision'] = clientSdkRev
            extdatas[key] = datas
        return datas

    def get_session_gameid(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['gameid']

    def get_session_clientid(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['clientid']

    def get_session_client_ip(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['client_ip']

    def get_session_deviceid(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['devid']

    def get_session_idfa(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['idfa']

    def get_session_iccid(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['iccid']

    def get_session_imei(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['imei']

    def get_session_imsi(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['imsi']

    def get_session_client_sys(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['client_sys']

    def get_session_client_ver(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['client_ver']

    def get_session_client_sdk_revision(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['client_sdk_revision']

    def get_session_client_chanel(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['client_chanel']

    def get_session_phone_type(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['phone_type']

    def get_session_city_zip(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['city_code_zip']

    def get_session_city_name(self, userId):
        datas = self.__get_session_values__(userId)
        return datas['city_code_name']

    def get_session_zipcode(self, userId, client_ip=None):
        ''' return tuple(zipcode, bywhich) '''

        if not userId and client_ip:
            return self.__get_ip_address_zipcode(client_ip), 'ip'

        precedence = self.__ctx__.Configure.get_global_item_json(
            'get_session_zipcode_precedence', ['mobile', 'iccid', 'lbs', 'ip'])
        datas = self.__get_session_values__(userId)
        bindMobile, vouchMobile, detectMobile, iccid = \
            datas['bindMobile'], datas['vouchMobile'], \
            datas['detect_phonenumber'], datas['iccid']
        if not client_ip:
            client_ip = datas['client_ip']
        self.__ctx__.ftlog.debug('get_session_zipcode bindMobile', bindMobile,
                                 'vouchMobile', vouchMobile, 'detectMobile', detectMobile,
                                 'client_ip', client_ip, 'iccid', iccid)

        self.__get_zipcode_cnt['all'] += 1
        for p in precedence:
            if p == 'mobile':
                z = self.__get_session_zipcode_by_mobile(bindMobile, vouchMobile,
                                                         detectMobile)
            elif p == 'iccid':
                z = self.__ctx__.IccidLoc.get_provid(iccid)
                if z > 0:
                    z *= 10000
                else:
                    z = 1
            elif p == 'lbs':
                z = self.get_session_city_zip(userId)
            elif p == 'ip':
                z = self.__get_ip_address_zipcode(client_ip)
            if z > 1:
                self.__get_zipcode_cnt[p] += 1
                self.__ctx__.ftlog.debug('get_session_zipcode', z, 'by', p,
                                         '__get_zipcode_cnt', self.__get_zipcode_cnt)
                return z, p
        self.__get_zipcode_cnt['missed'] += 1
        self.__ctx__.ftlog.debug('get_session_zipcode missed, __get_zipcode_cnt',
                                 self.__get_zipcode_cnt)
        return 1, 'missed'

    def get_session_province(self, userId):
        zipcode, _ = self.get_session_zipcode(userId)
        province = self.__ctx__.Const.PROVINCE_MAP.get(str(zipcode), '')
        return province

    def get_session_mobile(self, userId):
        datas = self.__get_session_values__(userId)
        bindMobile = self.__get_valid_phonenumber(datas['bindMobile'])
        vouchMobile = self.__get_valid_phonenumber(datas['vouchMobile'])
        detectMobile = self.__get_valid_phonenumber(datas['detect_phonenumber'])
        if bindMobile:
            return bindMobile
        if vouchMobile:
            return vouchMobile
        if detectMobile:
            return detectMobile
        return ''

    def __get_valid_phonenumber(self, phone):
        if not phone:
            return None
        phone = re.sub('[^0-9]', '', str(phone))
        phonenumber = None
        result = re.search('1[0-9]{10}$', phone)
        if result:
            phonenumber = result.group(0)
        return phonenumber

    def __get_session_zipcode_by_mobile(self, bindMobile, vouchMobile, detectMobile):
        if bindMobile != '':
            zipcode = self.__get_phone_home_location_zipcode(bindMobile)
            if zipcode != 1:
                return zipcode
        if vouchMobile != '':
            zipcode = self.__get_phone_home_location_zipcode(vouchMobile)
            if zipcode != 1:
                return zipcode
        if detectMobile != '':
            zipcode = self.__get_phone_home_location_zipcode(detectMobile)
            if zipcode != 1:
                return zipcode

    def get_phone_type_name(self, phone_type_code):
        if phone_type_code == self.PHONETYPE_CHINAMOBILE or phone_type_code == self.PHONETYPE_CHINAMOBILE_STR:
            return self.PHONETYPE_CHINAMOBILE_STR
        elif phone_type_code == self.PHONETYPE_CHINAUNION or phone_type_code == self.PHONETYPE_CHINAUNION_STR:
            return self.PHONETYPE_CHINAUNION_STR
        elif phone_type_code == self.PHONETYPE_CHINATELECOM or phone_type_code == self.PHONETYPE_CHINATELECOM_STR:
            return self.PHONETYPE_CHINATELECOM_STR
        else:
            return self.PHONETYPE_OTHER_STR

    def get_phone_type_code(self, phone_type_name):
        phone_type_name = str(phone_type_name)
        if phone_type_name == str(self.PHONETYPE_CHINAMOBILE) or phone_type_name == self.PHONETYPE_CHINAMOBILE_STR:
            return self.PHONETYPE_CHINAMOBILE
        elif phone_type_name == str(self.PHONETYPE_CHINAUNION) or phone_type_name == self.PHONETYPE_CHINAUNION_STR:
            return self.PHONETYPE_CHINAUNION
        elif phone_type_name == str(self.PHONETYPE_CHINATELECOM) or phone_type_name == self.PHONETYPE_CHINATELECOM_STR:
            return self.PHONETYPE_CHINATELECOM
        else:
            return self.PHONETYPE_OTHER

    def __get_phone_home_location_zipcode(self, phonenumber):
        phonenumber = str(phonenumber)
        if phonenumber[0] == '+':
            phonenumber = phonenumber[-11:]
        if len(phonenumber) != 11:
            return 1
        self.__ctx__.ftlog.debug('__get_phone_home_location_zipcode phonenumber', phonenumber)
        try:
            pc = self.__ctx__.PhoneTrie.find(phonenumber)
            self.__ctx__.ftlog.debug('__get_phone_home_location_zipcode return', pc * 10000)
            return pc * 10000

        except Exception, e:
            # self.__ctx__.ftlog.exception()
            self.__ctx__.ftlog.error('__get_phone_home_location_zipcode error', str(e))
            return 1  # 全国

    def __get_ip_address_zipcode(self, ipstr):
        try:
            pc = self.__ctx__.IPLoc.find(ipstr)
            return pc * 10000
        except Exception, e:
            # self.__ctx__.ftlog.exception()
            self.__ctx__.ftlog.error('__get_ip_address_zipcode error', str(e))
            return 1  # 全国


UserSession = UserSession()
