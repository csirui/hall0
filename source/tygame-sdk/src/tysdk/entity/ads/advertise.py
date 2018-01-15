# -*- coding: utf-8 -*-

import json
import re
import time
import urllib
from hashlib import md5

from twisted.web import client

from tyframework.context import TyContext
from tysdk.entity.user_common.constants import AccountConst


def is_valid_imei(imei):
    return re.match('^[0-9]{15}$', imei)


def is_valid_macmd5(macmd5):
    return re.match('^[0-9a-fA-F]{32}$', macmd5)


def is_valid_mac(mac):
    if not re.match('^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$', mac):
        return False
    _mac = mac.lower()
    if _mac == AccountConst.MAC_00 or _mac == AccountConst.MAC_02:
        return False
    return True


def is_valid_idfa(idfa):
    return re.match('^[0-9a-fA-F]{8}-([0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}$', idfa)


MYSQL_ADS_NAME = 'advertise'


class AdsServiceDao(object):
    def load(self, userId):
        raise NotImplemented()

    def save(self, status):
        raise NotImplemented()

    def record(self, id_name, id_val, spname, clkip, note=None, clktime=None):
        raise NotImplemented()

    def query(self, id_name, id_val):
        raise NotImplemented()


class AdsServiceMysqlImpl(AdsServiceDao):
    def record(self, iosappid, id_name, id_val, spname, clkip, note=None, clktime=None):
        if not clktime:
            clktime = int(time.time())
            # clktime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        sqlstr = 'INSERT INTO clicks (iosappid, spname, ' + id_name + ', clkip, clktime, clicks, note)' \
                                                                      ' VALUES(%s,%s,%s,%s,%s,1,%s) ON DUPLICATE KEY UPDATE clicks=clicks+1'
        values = TyContext.DbMySql.query(MYSQL_ADS_NAME, sqlstr,
                                         [iosappid, spname, id_val, clkip, clktime, note])
        TyContext.ftlog.debug('AdsServiceMysqlImpl.record',
                              sqlstr % (iosappid, spname, id_val, clkip, clktime, note),
                              'returns', values)

    def query(self, id_name, id_val):
        sqlstr = 'SELECT iosappid, mac, idfa, userid, clkip, clktime, spname, note FROM clicks WHERE ' + id_name + '=%s limit 1'
        values = TyContext.DbMySql.query(MYSQL_ADS_NAME, sqlstr, [id_val])
        TyContext.ftlog.debug('AdsServiceMysqlImpl.query', sqlstr % id_val, 'returns', values)
        if not values or len(values) <= 0:
            return None
        return values[0][0], values[0][1], values[0][2], values[0][3], \
               values[0][4], values[0][5], values[0][6], values[0][7]

    def query_by_idfa(self, appid, idfa, spname=None):
        if spname != None:
            sqlstr = 'SELECT count(*) as num FROM clicks WHERE iosappid=%s AND idfa=%s AND spname=%s AND userid !=""'
            values = TyContext.DbMySql.query(MYSQL_ADS_NAME, sqlstr, [appid, idfa, spname])
            TyContext.ftlog.debug('AdsServiceMysqlImpl.query_click_by_idfa', sqlstr % (appid, idfa, spname), 'returns',
                                  values)
        else:
            sqlstr = 'SELECT count(*) as num FROM clicks WHERE iosappid=%s AND idfa=%s AND userid !=""'
            values = TyContext.DbMySql.query(MYSQL_ADS_NAME, sqlstr, [appid, idfa])
            TyContext.ftlog.debug('AdsServiceMysqlImpl.query_click_by_idfa', sqlstr % (appid, idfa), 'returns', values)
        if not values or len(values) <= 0:
            return 0
        return values[0][0]

    def update_on_creation(self, userid, crttime, spname, id_name, id_val):
        sqlstr = 'UPDATE clicks SET userid=%s, crttime=%s WHERE ' \
                 + id_name + '=%s AND spname=%s limit 1'
        values = TyContext.DbMySql.query(MYSQL_ADS_NAME, sqlstr, [userid, crttime, id_val, spname])
        TyContext.ftlog.debug('AdsServiceMysqlImpl.update_on_creation',
                              sqlstr % (userid, crttime, id_val, spname),
                              'returns', values)

    def update_on_activation(self, userid, acttime, actip):
        sqlstr = 'UPDATE clicks SET acttime=%s, actip=%s WHERE userid=%s limit 1'
        values = TyContext.DbMySql.query(MYSQL_ADS_NAME, sqlstr,
                                         [acttime, actip, userid])
        TyContext.ftlog.debug('AdsServiceMysqlImpl.update_on_activation',
                              sqlstr % (acttime, actip, userid),
                              'returns', values)


class AdvertiseService(object):
    __ads_dao = AdsServiceMysqlImpl()
    __ads_class = {}

    @classmethod
    def on_init(cls):
        dbconf = TyContext.TYGlobal.mysql(MYSQL_ADS_NAME)
        TyContext.ftlog.debug('AdvertiseService.on_init dbconf=', dbconf)
        TyContext.DbMySql.connect(MYSQL_ADS_NAME, dbconf)

    @classmethod
    def query_click(cls, id_name, id_val):
        return cls.__ads_dao.query(id_name, id_val)

    @classmethod
    def query_click_by_idfa(cls, appid, idfa, spname=None):
        return cls.__ads_dao.query_by_idfa(appid, idfa, spname=None)

    @classmethod
    def update_clicks_on_creation(cls, userid, crttime, spname, id_name, id_val):
        return cls.__ads_dao.update_on_creation(userid, crttime, spname, id_name, id_val)

    @classmethod
    def update_clicks_on_activation(cls, userid, acttime, actip):
        return cls.__ads_dao.update_on_activation(userid, acttime, actip)

    @classmethod
    def record_click(cls, ids, clkip, spname, note=None):
        TyContext.ftlog.debug('AdvertiseService.record_click ids:', ids, 'spname:', spname)
        if len(spname) <= 0:
            TyContext.ftlog.error('AdvertiseService.record_click wrong spname:', spname)
            return
        iosappid = ids.get('iosappid', 0)
        if iosappid <= 0:
            TyContext.ftlog.error('AdvertiseService.record_click wrong iosappid:', iosappid)
            return
        if len(ids.get('mac', '')) > 0:
            cls.__ads_dao.record(iosappid, 'mac', ids['mac'], spname, clkip, note)
            return
        elif len(ids.get('idfa', '')) > 0:
            cls.__ads_dao.record(iosappid, 'idfa', ids['idfa'], spname, clkip, note)
            return
        TyContext.ftlog.error('AdvertiseService.record_click no valid ids:', ids)

    @classmethod
    def ads_clicked(cls, rpath):
        sp = rpath.split('/')[-1]
        try:
            spcls = cls.__ads_class[sp]
        except:
            try:
                clsname = 'Ads' + sp[0].upper() + sp[1:].lower()
                importstr = 'from ads%s import %s as spcls' % (sp, clsname)
                TyContext.ftlog.debug('ads_clicked load ads class:', importstr)
                exec importstr
                cls.__ads_class[sp] = spcls
            except:
                TyContext.ftlog.exception()
                return 'system error'

        rparams = TyContext.RunHttp.convertArgsToDict()
        if 'clkip' not in rparams:
            rparams['clkip'] = TyContext.RunHttp.get_client_ip()
        TyContext.ftlog.debug('AdvertiseService.ads_clicked rparams=', rparams)
        return spcls.ads_clicked(rparams)

    @classmethod
    def on_user_created(cls, userid):
        ''' call the api asynchronously '''
        try:
            httpdomain = None
            sc = TyContext.RunMode.get_server_control()
            TyContext.ftlog.debug('on_user_created get_server_control', sc)
            if sc:
                httpdomain = TyContext.RunMode.get_server_control()['http']
            if not httpdomain:
                httpdomain = TyContext.TYGlobal.http_game()
            url = str(httpdomain) + '/open/v3/user/created?' + urllib.urlencode({'userId': userid})
            TyContext.ftlog.debug('AdvertiseService.on_user_created getPage url=', url)
            d = client.getPage(url)
            TyContext.TyDeffer.add_default_callback(d, __file__, 'on_user_created', url)
        except Exception, e:
            TyContext.ftlog.error('AdvertiseService.on_user_created error=', e)
            # TyContext.ftlog.exception()

    @classmethod
    def user_created(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('AdvertiseService.user_created rparam=', rparams)
        userid = int(rparams['userId'])

        mac = TyContext.RedisUser.execute(userid, 'HGET', 'user:%d' % userid, 'mac')
        # mac is in '010203040506' format in user table,
        # convert it to '01:02:03:04:05:06' format first
        if mac:
            # if there is only digits in mac, it will be converted to an int, so
            # convert it back to str here.
            if isinstance(mac, int):
                mac = '%012d' % mac
            mac = ':'.join([mac[2 * i:2 * i + 2] for i in xrange(6)])
        else:
            mac = ''
        TyContext.ftlog.debug('AdvertiseService.user_created userid', userid, 'mac', mac)
        crttime = int(time.time())

        if is_valid_mac(mac):
            ret = AdvertiseService.query_click('mac', mac)
            if ret:
                iosappid, _, _, _, _, _, sp, _ = ret
                AdvertiseService.update_clicks_on_creation(userid, crttime, sp, 'mac', mac)
            return 'should be successful, but who knows'

        idfa = TyContext.UserSession.get_session_idfa(userid)
        TyContext.ftlog.debug('AdvertiseService.user_created userid', userid, 'idfa', idfa)
        if is_valid_idfa(idfa):
            ret = AdvertiseService.query_click('idfa', idfa)
            if ret:
                iosappid, _, _, _, _, _, sp, _ = ret
                AdvertiseService.update_clicks_on_creation(userid, crttime, sp, 'idfa', idfa)
            else:
                m = md5()
                m.update(idfa)
                digest = m.hexdigest().lower()
                ret = AdvertiseService.query_click('idfa', digest)
                if ret:
                    iosappid, _, _, _, _, _, sp, _ = ret
                    AdvertiseService.update_clicks_on_creation(userid, crttime, sp, 'idfa', digest)
            cls.notifyQuzhuanUserCreated(userid)
            return 'should be successful, but who knows'

        TyContext.ftlog.error('AdvertiseService.user_created no valid '
                              'mac (%s) or idfa (%s)' % (mac, idfa))
        return 'should be successful, but who knows'

    @classmethod
    def user_activated(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('AdvertiseService.user_activated rparam=', rparams)
        userid = int(rparams['userId'])
        # gameid = rparams['appId']
        params = {}
        ip = TyContext.UserSession.get_session_client_ip(userid)
        acttime = int(time.time())
        result = AdvertiseService.query_click('userid', userid)
        if not result:
            return 'not advertise user'
        iosappid, mac, idfa, _, clkip, clktime, sp, note = result
        AdvertiseService.update_clicks_on_activation(userid, acttime, ip)
        TyContext.ftlog.info('AdvertiseService.user_activated mac', mac, 'idfa', idfa, 'ip', type(ip), 'acttime',
                             acttime, 'userid', userid, 'sp=', sp)
        params['userId'] = userid
        params['iosappid'] = iosappid
        params['clkip'] = clkip
        if idfa:
            params['idfa'] = idfa
        if mac:
            params['mac'] = mac
        params['clktime'] = clktime
        params['acttime'] = acttime
        if ip:
            params['ip'] = ip
        params['note'] = note
        TyContext.ftlog.debug('AdvertiseService.user_activated param=', params)
        try:
            spcls = cls.__ads_class[sp]
        except:
            try:
                clsname = 'Ads' + sp[0].upper() + sp[1:].lower()
                importstr = 'from ads%s import %s as spcls' % (sp, clsname)
                TyContext.ftlog.debug('user_activated load ads class:', importstr)
                exec importstr
                cls.__ads_class[sp] = spcls
            except:
                TyContext.ftlog.exception()
                return 'iamsorry'
        return spcls.user_activated(params)

    @classmethod
    def notifyQuzhuanUserCreated(cls, userId):
        result = AdvertiseService.query_click('userid', userId)
        if not result:
            TyContext.ftlog.info(
                'AdvertiseService->notifyQuzhuanUserCreated {userId} not advertise user'.format(userId=userId))
            return 'not advertise user'
        iosappid, mac, idfa, _, clkip, clktime, sp, note = result
        if sp != 'quzhuan':
            TyContext.ftlog.info(
                'AdvertiseService->notifyQuzhuanUserCreated {userId} not quzhuan advertise user'.format(userId=userId))
            return 'not quzhuan advertise user'
        params = {}
        params['userId'] = userId
        params['iosappid'] = iosappid
        params['clkip'] = clkip
        if idfa:
            params['idfa'] = idfa
        if mac:
            params['mac'] = mac
        params['clktime'] = clktime
        acttime = int(time.time())
        params['acttime'] = acttime
        ip = TyContext.UserSession.get_session_client_ip(userId)
        if ip:
            params['ip'] = ip
        params['note'] = note
        from adsquzhuan import AdsQuzhuan
        ret = AdsQuzhuan.user_created(params)
        TyContext.ftlog.info('AdvertiseService->notifyQuzhuanUserCreated notify quzhuan result.', ret)

    @classmethod
    def check_idfas(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('AdvertiseService.check_idfas rparams:', rparams)
        ret = {}
        try:
            checkidfas = rparams['idfa']
            appid = rparams['appid']
        except Exception as e:
            TyContext.ftlog.error('AdvertiseService->check_idfas ERROR: ', e)
            return json.dumps(ret)
        idfas = []
        idfas = checkidfas.split(',')
        if len(idfas) > 0:
            for idfa in idfas:
                if idfa == '':
                    continue
                ret[idfa] = 0
                low_idfa = str(idfa).lower()
                num = AdvertiseService.query_click_by_idfa(appid, low_idfa)
                if int(num) > 0:
                    ret[idfa] = 1
                else:
                    m = md5()
                    m.update(low_idfa)
                    digest = m.hexdigest().lower()
                    num = AdvertiseService.query_click_by_idfa(appid, digest)
                    if int(num) > 0:
                        ret[idfa] = 1

        return json.dumps(ret)
