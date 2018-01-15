# -*- coding=utf-8 -*-

class PayType(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def __bug_paytypeinfo_patch__(self, datas):
        if datas:
            if 'paytype' in datas:
                datas['payType'] = datas['paytype']
            elif 'payType' in datas:
                datas['paytype'] = datas['payType']
        return datas

    def __get_client_game_item_json__(self, gid, key, clientid, defaultVal=None):
        templateid = self.__ctx__.Configure.get_configure_str(
            'configitems:gameclient:' + str(gid) + ':' + key + ':' + clientid, None)
        if templateid:
            return self.__ctx__.Configure.get_configure_json('configitems:template:' + templateid, defaultVal)
        return defaultVal

    def __get_pay_info__(self, appId, clientid, buttonId, unlimit, phonetype, citycode):
        paytype = None
        price = None
        phonetype = self.__ctx__.UserSession.get_phone_type_code(phonetype)
        paychanneldict, gamepayitem = self.__get_pay_info_new__(appId, clientid, buttonId, unlimit, phonetype, citycode)
        if paychanneldict and gamepayitem:
            paytype = paychanneldict['paytype']
            price = gamepayitem['rmb']
        else:
            paytype, price = self.__get_pay_info_old__(appId, clientid, buttonId, unlimit, phonetype, citycode)
        if paytype == None or price == None:
            self.__ctx__.ftlog.error('__get_pay_info__ error,', appId, clientid, buttonId, unlimit, phonetype, citycode)
        return paytype, price

    def __get_pay_info_old__(self, appId, clientid, buttonId, unlimit, phonetype, citycode):
        self.__ctx__.ftlog.debug('__get_pay_info_old__ !', appId, clientid, buttonId, unlimit, phonetype, citycode)
        rkey = "paytype:" + str(appId) + ":" + clientid
        rsubkey = str(buttonId) + '_' + str(unlimit) + '_' + str(phonetype)
        # TODO 过渡期代码，线上的paytype存放于mix库，新的策略为存放于configer库 
        paytypeinfo = self.__ctx__.RedisMix.execute('HGET', rkey, rsubkey)
        if paytypeinfo is None:
            paytypeinfo = self.__ctx__.RedisConfig.execute('HGET', rkey, rsubkey)
        if paytypeinfo is None:
            self.__ctx__.ftlog.error('__get_pay_info_old__', rsubkey, 'missing in paytype', rkey)
            return None, None
        try:
            data = self.__ctx__.strutil.loads(paytypeinfo)
            data = self.__bug_paytypeinfo_patch__(data)
            self.__ctx__.ftlog.debug('__get_pay_info_old__ get paytype', data['paytype'], 'price', data['price'])
            return data['paytype'], data['price']
        except:
            self.__ctx__.ftlog.exception()
        return None, None

    def __get_pay_info_new__(self, appId, clientid, buttonId, unlimit, phonetype, citycode):

        self.__ctx__.ftlog.debug('__get_pay_info_new__ !', appId, clientid, buttonId, unlimit, phonetype, citycode)

        # 找到对应的clientId的1级支付模板内容
        citydict = self.__get_client_game_item_json__(appId, 'paytype', clientid)
        if not citydict:
            self.__ctx__.ftlog.error('__get_pay_info_new__ can not find citydict !',
                                     appId, clientid, buttonId, unlimit, phonetype, citycode)
            return None, None

        templateid2 = citydict.get(str(citycode), None)
        if not templateid2:
            citycode_all = self.__ctx__.CityLocator.DEFAULT_LOCATION[0]
            templateid2 = citydict.get(str(citycode_all), None)
        if not templateid2:
            self.__ctx__.ftlog.error('__get_pay_info_new__ can not find templateid2 !',
                                     appId, clientid, buttonId, unlimit, phonetype, citycode, citydict)
            return None, None

        itemdict = self.__ctx__.Configure.get_template_item_json(templateid2)
        if not itemdict:
            self.__ctx__.ftlog.error('__get_pay_info_new__ can not find itemdict !',
                                     appId, clientid, buttonId, unlimit, phonetype, citycode, citydict,
                                     templateid2)
            return None, None

        limitdict = itemdict.get(str(buttonId), None)
        if not limitdict:
            self.__ctx__.ftlog.error('__get_pay_info_new__ can not find limitdict !',
                                     appId, clientid, buttonId, unlimit, phonetype, citycode, citydict,
                                     templateid2, itemdict)
            return None, None

        phonedict = limitdict.get(str(unlimit), None)
        if not phonedict:
            self.__ctx__.ftlog.error('__get_pay_info_new__ can not find phonedict !',
                                     appId, clientid, buttonId, unlimit, phonetype, citycode, citydict,
                                     templateid2, itemdict, limitdict)
            return None, None

        paychannelid = phonedict.get(str(phonetype), None)
        if not paychannelid:
            self.__ctx__.ftlog.error('__get_pay_info_new__ can not find paychannelid !',
                                     appId, clientid, buttonId, unlimit, phonetype, citycode, citydict,
                                     templateid2, itemdict, limitdict, phonedict)
            return None, None

        paychanneldict, gamepayitem = self.get_pay_type_item_datas(paychannelid, appId, buttonId)
        if not paychanneldict or not gamepayitem:
            self.__ctx__.ftlog.error('__get_pay_info_new__ can not find paychanneldict !',
                                     appId, clientid, buttonId, unlimit, phonetype, citycode, citydict,
                                     templateid2, itemdict, limitdict, phonedict, paychannelid)
            return None, None

        rmb = gamepayitem.get('rmb', None)
        if not rmb or rmb <= 0:
            self.__ctx__.ftlog.error('__get_pay_info_new__ can not find rmb !',
                                     appId, clientid, buttonId, unlimit, phonetype, citycode, citydict,
                                     templateid2, itemdict, limitdict, phonedict, paychannelid,
                                     paychanneldict, gamepayitem)
            return None, None

        return paychanneldict, gamepayitem

    def get_pay_type_item_datas(self, paychannelid, appId, buttonId):
        paychanneldict = self.__ctx__.Configure.get_global_item_json('paychannel:' + paychannelid)
        if not paychanneldict:
            self.__ctx__.ftlog.error('get_pay_type_item_datas can not find paychanneldict !',
                                     paychannelid, appId, buttonId)
            return None, None

        channelitems = paychanneldict.get('items', None)
        if not channelitems:
            self.__ctx__.ftlog.error('get_pay_type_item_datas can not find channelitems !',
                                     paychannelid, appId, buttonId,
                                     paychanneldict)
            return None, None

        payitem = channelitems.get(str(appId), None)
        if not payitem:
            self.__ctx__.ftlog.error('get_pay_type_item_datas can not find payitem !',
                                     paychannelid, appId, buttonId,
                                     paychanneldict, channelitems)
            return None, None

        gamepayitem = payitem.get(buttonId, None)
        if not gamepayitem:
            self.__ctx__.ftlog.error('get_pay_type_item_datas can not find gamepayitem !',
                                     paychannelid, appId, buttonId,
                                     paychanneldict, channelitems, payitem)
            return None, None
        return paychanneldict, gamepayitem

    def get_pay_type_ext_datas(self, paytype):
        extdatas = self.__ctx__.Configure.get_global_item_json('payextdata:' + paytype)
        if not extdatas:
            self.__ctx__.ftlog.error('get_pay_type_ext_datas can not find payextdata !',
                                     paytype)
            return None
        return extdatas

    def append_pay_type_info(self, appId, clientId, buttonId, unlimit, phonetype, citycode, userId, mo):
        payType, price = self.__get_pay_info__(appId, clientId, buttonId, unlimit, phonetype, citycode)
        if payType is None or price is None:
            mo.setResult('code', '2')
            mo.setResult('info', 'paytye configure error!')
            return

        is_prefer_alipay, alipaytype = self.__prefer_alipay_once_used(clientId, userId)
        if is_prefer_alipay:
            mo.setResult('code', '0')
            mo.setResult('payType', alipaytype)
            mo.setResult('price', price)
            return

        if payType == 'linkyun':
            payType = self.__linkyun_switch_patch(citycode, clientId, buttonId)
            self.__ctx__.ftlog.debug('append_pay_type_info linkyun switch return', payType)
        elif payType == 'huafubao':
            payType = self.__huafubao_switch_patch(citycode, clientId, buttonId)
            self.__ctx__.ftlog.debug('append_pay_type_info huafubao switch return', payType)

        mo.setResult('code', '0')
        mo.setResult('payType', payType)
        mo.setResult('price', price)

    def __prefer_alipay_once_used(self, clientId, userId):
        if 0 == self.__ctx__.Configure.get_global_item_int('prefer_alipay_once_used'):
            return False, None
        used = self.__ctx__.RedisUser.execute(userId, 'HGET', 'user:%d' % userId, 'used_alipay')
        if used is None or used == 0:
            return False, None
        clientid_dict = self.__ctx__.Configure.get_global_item_json('prefer_alipay_clientids', {})
        if clientId not in clientid_dict:
            return False, None
        # return True, clientid_dict[clientId]
        return True, 'tuyoo'

    def get_pay_type_by_user(self, userId, buttonId, clientId=None):
        appId = self.__ctx__.UserSession.get_session_gameid(userId)
        return self.get_paytype_by_user(appId, userId, buttonId, clientId)

    def get_paytype_by_user(self, appId, userId, buttonId, clientId=None):
        phonetype = self.__ctx__.UserSession.get_session_phone_type(userId)
        citycode, _ = self.__ctx__.UserSession.get_session_zipcode(userId)
        unlimit = self.__ctx__.SmsPayCheck.is_sms_pay_limited(userId)
        if not clientId:
            clientId = self.__ctx__.UserSession.get_session_clientid(userId)
        payType, _ = self.__get_pay_info__(appId, clientId, buttonId, unlimit, phonetype, citycode)
        if payType != None:
            if payType == 'linkyun':
                payType = self.__linkyun_switch_patch(citycode, clientId, buttonId)
                self.__ctx__.ftlog.debug('append_pay_type_info linkyun switch return', payType)
            elif payType == 'huafubao':
                payType = self.__huafubao_switch_patch(citycode, clientId, buttonId)
                self.__ctx__.ftlog.debug('append_pay_type_info huafubao switch return', payType)
            return payType
        else:
            if clientId.find('IOS_') >= 0:
                if clientId.find('yueyu') > 0:
                    return 'tuyoo'
                return 'tuyooios'
            # 缺省都走tuyoo
            return 'tuyoo'

    def get_pay_data_by_user(self, userId, buttonId, clientId=None):
        appId = self.__ctx__.UserSession.get_session_gameid(userId)
        return self.get_paydata_by_user(appId, userId, buttonId, clientId)

    def get_paydata_by_user(self, appId, userId, buttonId, clientId=None):
        phonetype = self.__ctx__.UserSession.get_session_phone_type(userId)
        unlimit = self.__ctx__.SmsPayCheck.is_sms_pay_limited(userId)
        if not clientId:
            clientId = self.__ctx__.UserSession.get_session_clientid(userId)
        # citycode = self.__ctx__.UserSession.get_session_city_zip(userId)
        citycode, _ = self.__ctx__.UserSession.get_session_zipcode(userId)
        return self.get_pay_type_info(appId, clientId, buttonId, unlimit, phonetype, citycode)

    def get_paydata_by_clientid(self, appId, clientId, buttonId, phonetype, citycode):
        channel_dict, gamepayitem = self.__get_pay_info_new__(appId, clientId, buttonId, '0', phonetype, citycode)
        if not channel_dict or 'paytype' not in channel_dict \
                or not gamepayitem or 'paydata' not in gamepayitem:
            return None, None
        return channel_dict['paytype'], gamepayitem['paydata']

    def get_pay_type_info(self, appId, clientId, buttonId, unlimit, phonetype, citycode):
        paychanneldict, gamepayitem = self.__get_pay_info_new__(appId, clientId, buttonId, unlimit, phonetype, citycode)
        return paychanneldict, gamepayitem

    prodids_8_yuan = {'C8': None, 'C8_LUCKY': None, 'C8_QUICK': None,
                      'C8_RAFFLE': None, 'RAFFLE_8': None, 'RAFFLE_NEW': None,
                      'T80K': None, 'TEXAS_COIN_LUCKY_R8': None, 'TEXAS_COIN_R8': None,
                      'TGBOX9': None, 'ZHUANYUN_8': None, 'ZHUANYUN_MEZZO': None, }

    def __linkyun_switch_patch(self, citycode, clientid, prodid):
        citycode = str(citycode)
        provs = self.__ctx__.Configure.get_global_item_json('linkyun_supported_provs', {})
        citycodes = [str(int(p) * 10000) for p in provs.keys()]
        # 河北没有开通8元
        if citycode == '50000' and prodid not in PayType.prodids_8_yuan:
            return 'linkyun'
        if citycode in citycodes:
            return 'linkyun'
        return 'tuyoo'
        # clientid_type = self.__ctx__.Configure.get_global_item_json(
        #    '360_or_tuyoo_per_clientid', {'tuyoo':{}, '360':{}})
        # self.__ctx__.ftlog.debug('linkyun switch', citycode, clientid, prodid, citycodes, clientid_type)
        # if clientid in clientid_type['360']:
        #    return '360'
        # if clientid in clientid_type['tuyoo']:
        #    return 'tuyoo'

    prodids_10_yuan = {'C10': None, 'C10_LUCKY': None, 'T100K': None, 'TEXAS_COIN2': None, }

    def __huafubao_switch_patch(self, citycode, clientid, prodid):
        citycode = str(citycode)
        provs = self.__ctx__.Configure.get_global_item_json('huafubao_supported_provs', {})
        citycodes = [str(int(p) * 10000) for p in provs.keys()]
        # 江西只开了10元
        if citycode == '330000' and prodid in PayType.prodids_10_yuan:
            return 'huafubao'
        if citycode in citycodes:
            return 'huafubao'
        return 'tuyoo'
        # clientid_type = self.__ctx__.Configure.get_global_item_json(
        #    '360_or_tuyoo_per_clientid', {'tuyoo':{}, '360':{}})
        # if clientid in clientid_type['360']:
        #    return '360'
        # if clientid in clientid_type['tuyoo']:
        #    return 'tuyoo'


PayType = PayType()
