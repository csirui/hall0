# -*- coding=utf-8 -*-

import hashlib
import hmac
import json
import md5
import time
import uuid
from urllib import urlencode, quote

from datetime import datetime

from dedup import Deduplicates
from tyframework.context import TyContext
from tysdk.entity.paythird.helper import PayHelper
from tysdk.entity.user_common.account_helper import AccountHelper


class Transaction(object):
    ''' make sure a transactionid is globally unique in a peroid '''

    def __init__(self, name, expire=60 * 60 * 24 * 30):
        self.__txnname = name
        self.__expire = expire

    def check(self, transaction_id):
        if not transaction_id:
            return False
        ret = TyContext.RedisMix.execute('SADD', self.__txnname, transaction_id)
        if ret == 0:
            return False
        ttl = TyContext.RedisMix.execute('TTL', self.__txnname)
        if ttl < 0:
            ttl = self.__expire
            TyContext.RedisMix.execute('EXPIRE', self.__txnname, ttl)
        TyContext.ftlog.debug('__mark_transaction_as_delivered add transaction_id:',
                              transaction_id, 'key', self.__txnname, 'ttl:', ttl)
        return True


class TuYouSLL(object):
    '''
    TuYouSLL (SLL=San Liu Ling :-) defines all the http api for 360.
    '''

    @classmethod
    def __calc_sign(cls, appkey, params):
        sign_str = '&'.join(['%s=%s' % (k, params[k]) for k in sorted(params.keys())])
        sign = hmac.new(appkey, sign_str, hashlib.sha1).hexdigest()
        TyContext.ftlog.debug('TuYouSLL __calc_sign appkey', appkey,
                              'sign_str', sign_str, 'sign', sign)
        return sign

    @classmethod
    def __check_sign(cls, appkey, params):
        try:
            if not appkey:
                TyContext.ftlog.error('TuYouSLL __check_sign error appkey null')
                return False
            sign = params['sign']
            del params['sign']
            expected = cls.__calc_sign(appkey, params)
            if sign != expected:
                TyContext.ftlog.error('TuYouSLL __check_sign error sign', sign,
                                      'expected', expected)
                return False
            return True
        except:
            TyContext.ftlog.error('TuYouSLL __check_sign error')
            TyContext.ftlog.exception()
            return False

    @classmethod
    def get_chip(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouSLL get_chip params', params)
        ok, ret = cls.__common_check(params, do_create=True)
        if not ok:
            return ret
        userid = ret
        chip = TyContext.RedisUser.execute(userid, 'HGET', 'user:%s' % userid, 'chip')
        ret = {}
        ret['code'] = 0
        ret['userid'] = userid
        ret['curr_chip'] = chip
        ret['sign'] = cls.__calc_sign(cls.appkey, ret)
        TyContext.ftlog.debug('TuYouSLL get_chip ret', ret)
        return json.dumps(ret)

    @classmethod
    def incr_chip(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouSLL incr_chip params', params)
        ok, ret = cls.__common_check(params, do_create=True)
        if not ok:
            return ret
        userid = ret
        gameid = int(params['appid'])
        transactionid = params.get('transactionid', '')
        if not transactionid or \
                not Transaction('delivered_tu360_transactions_%s' % gameid).check(transactionid):
            return cls.__build_error_ret(1, 'transactionid missing or already used', transactionid)
        count = int(params['count'])
        eventid = int(params.get('eventid', 0))
        delta, chip = TyContext.UserProps.incr_chip2(
            userid, gameid, count, TyContext.ChipNotEnoughOpMode.NOOP, eventid)
        ret = {}
        if delta != count:
            ret['code'] = 2
            ret['msg'] = 'no enough chip'
        else:
            ret['code'] = 0
        ret['userid'] = userid
        ret['add_chip'] = delta
        ret['final_chip'] = chip
        ret['transactionid'] = transactionid
        ret['sign'] = cls.__calc_sign(cls.appkey, ret)
        TyContext.ftlog.debug('TuYouSLL incr_chip ret', ret)
        return json.dumps(ret)

    # 1元=100金豆。1金豆=0.1钻石=100金币
    @classmethod
    def exchange_bean(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouSLL exchange_bean params', params)
        ok, ret = cls.__common_check(params, do_create=True)
        if not ok:
            return ret
        userid = ret
        transactionid = params.get('transactionid', '')
        gameid = int(params['appid'])
        if not transactionid or \
                not Transaction('delivered_tu360_transactions_%s' % gameid).check(transactionid):
            return cls.__build_error_ret(1, 'transactionid missing or already used', transactionid)
        count = int(params['count'])
        if count < 0:
            return cls.__build_error_ret(1, 'wrong count value', transactionid)
        forwhat = params['for']
        eventid = int(params.get('eventid', 0))
        ret = {}
        if forwhat == 'diamond':
            # 兑换钻石时，只接受金豆数为10的倍数
            exchange_rate_diamond = 0.1
            count = int(exchange_rate_diamond * count)
            delta, final = TyContext.UserProps.incr_diamond(
                userid, gameid, count, TyContext.ChipNotEnoughOpMode.NOOP, eventid)
            ret['code'] = 0
            ret['userid'] = userid
            ret['snsid'] = params['snsid']
            ret['add_diamond'] = delta
            ret['final_diamond'] = final
            ret['transactionid'] = transactionid
            ret['sign'] = cls.__calc_sign(cls.appkey, ret)
            TyContext.ftlog.debug('TuYouSLL exchange_bean ret', ret)
            return json.dumps(ret)
        elif forwhat == 'chip':
            exchange_rate_chip = 100
            count = int(exchange_rate_chip * count)
            delta, final = TyContext.UserProps.incr_chip2(
                userid, gameid, count, TyContext.ChipNotEnoughOpMode.NOOP, eventid)
            ret['code'] = 0
            ret['userid'] = userid
            ret['snsid'] = params['snsid']
            ret['add_chip'] = delta
            ret['final_chip'] = final
            ret['transactionid'] = transactionid
            ret['sign'] = cls.__calc_sign(cls.appkey, ret)
            TyContext.ftlog.debug('TuYouSLL exchange_bean ret', ret)
            return json.dumps(ret)
        else:
            return cls.__build_error_ret(1, 'for parameter value error', transactionid)

    @classmethod
    def __build_error_ret(cls, code, msg, transaction_id=None):
        ret = {}
        ret['code'] = code
        ret['msg'] = msg
        if transaction_id:
            ret['transactionid'] = transaction_id
        ret['sign'] = cls.__calc_sign(cls.appkey, ret)
        TyContext.ftlog.debug('TuYouSLL __build_error_ret ret', ret)
        return json.dumps(ret)

    @classmethod
    def _find_userid_by_qid(cls, qid):
        uid = TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + str(qid))
        if not uid or uid <= 0:
            return 0
        try:
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('TuYouSLL _find_userid_by_qid can not find'
                                  ' user for qid', qid)
            return 0

    @classmethod
    def __merge_balance(cls, qid, userid, appid):
        balance = TyContext.RedisMix.execute('HGET', 'qid.balance', qid)
        if balance:
            chip = TyContext.RedisUser.execute(userid, 'HGET', 'user:%s' % userid, 'chip')
            if chip:
                eventid = 20000
                delta, final = TyContext.UserProps.incr_chip2(
                    userid, int(appid), balance, TyContext.ChipNotEnoughOpMode.NOOP, eventid)
                TyContext.ftlog.info('TuYouSLL __merge_balance qid', qid,
                                     'uid', userid, 'merge', balance, 'balance', 'final', final)
            TyContext.RedisMix.execute('HDEL', 'qid.balance', qid)

    @classmethod
    def __common_check(cls, params, do_create=False):
        ''' do common check like sign check, snsid chek.

        return ok flag and an extra parameter. if ok flag is false, the extra
        parameter is the error ret msg. if true, the extra parameter is the
        userid bound with the qid. '''

        appid = params['appid']
        qid = params['snsid']
        gid = params.get('guestid')
        cls.appkey = str(TyContext.Configure.get_game_item_str(appid, 'appKey', ''))
        if not cls.__check_sign(cls.appkey, params):
            return False, cls.__build_error_ret(1, 'sign error')
        if not qid.startswith('360:'):
            return False, cls.__build_error_ret(1, 'wrong snsid')
        if not gid:
            userid = cls._find_userid_by_qid(qid)
            if userid:
                cls.__merge_balance(qid, userid, appid)
                return True, userid
            if not do_create:
                return False, cls.__build_error_ret(2, 'snsid not registered')
            userid = cls.__create_user(appid, qid)
            if not userid:
                return False, cls.__build_error_ret(1, 'user create failed')
            return True, userid
        if not gid.startswith('360:'):
            return False, cls.__build_error_ret(1, 'wrong guestid')
        userid = cls._find_userid_by_qid(gid)
        if userid:
            cls.__merge_balance(gid, userid, appid)
            return True, userid
        return False, cls.__build_error_ret(1, 'guestid not registered')

    @classmethod
    def revoke_qid(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouSLL revoke_qid params', params)
        ok, ret = cls.__common_check(params)
        if not ok:
            # clear the corresponding qid.balance item
            if json.loads(ret)['code'] == 2:
                qid = params['snsid']
                balance = TyContext.RedisMix.execute('HGET', 'qid.balance', qid)
                if balance:
                    TyContext.RedisMix.execute('HDEL', 'qid.balance', qid)
                    ret = {}
                    ret['code'] = 0
                    ret['snsid'] = qid
                    ret['sign'] = cls.__calc_sign(cls.appkey, ret)
                    TyContext.ftlog.info('TuYouSLL revoke_qid qid', qid,
                                         'relinquish', balance, 'balance')
                    return json.dumps(ret)
            return ret
        userid = ret
        qid = params['snsid']
        userid = TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + qid)
        TyContext.RedisUserKeys.execute('DEL', 'snsidmap:' + qid)
        chip = TyContext.RedisUser.execute(userid, 'HGET', 'user:%s' % userid, 'chip')
        if chip:
            gameid = int(params['appid'])
            eventid = 20011
            delta, final = TyContext.UserProps.incr_chip2(
                userid, gameid, -chip, TyContext.ChipNotEnoughOpMode.NOOP, eventid)
            TyContext.ftlog.info('TuYouSLL revoke_qid qid', qid, 'userid', userid,
                                 'relinquish', delta, 'chips')
        TyContext.RedisUser.execute(userid, 'DEL', 'user:%s' % userid)
        ret = {}
        ret['code'] = 0
        ret['snsid'] = qid
        ret['userid'] = userid
        ret['sign'] = cls.__calc_sign(cls.appkey, ret)
        TyContext.ftlog.debug('TuYouSLL revoke_qid ret', ret)
        return json.dumps(ret)

    @classmethod
    def gid2qid(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouSLL gid2qid params', params)
        ok, ret = cls.__common_check(params)
        if not ok:
            return ret
        userid = ret
        qid = params['snsid']
        gid = params['guestid']
        # XXX how if qid already mapped to a user?!
        TyContext.RedisUserKeys.execute('SET', 'snsidmap:' + qid, userid)
        TyContext.RedisUserKeys.execute('DEL', 'snsidmap:' + gid)
        TyContext.ftlog.info('TuYouSLL gid2qid for userid', userid,
                             'gid', gid, 'qid', qid)
        ret = {}
        ret['code'] = 0
        ret['snsid'] = qid
        ret['guestid'] = gid
        ret['userid'] = userid
        ret['sign'] = cls.__calc_sign(cls.appkey, ret)
        TyContext.ftlog.debug('TuYouSLL gid2qid ret', ret)
        return json.dumps(ret)

    @classmethod
    def __create_user(cls, appId, qid):
        # get balance first
        balance = TyContext.RedisMix.execute('HGET', 'qid.balance', qid)
        if balance is None:
            balance = 0
        uid = TyContext.RedisMix.execute('INCR', 'global.userid')
        if uid <= 0:
            return 0
        # XXX clientid for 360pc qipai
        clientId = 'pc_1.0_qid'
        from tysdk.entity.user_common.constants import AccountConst
        datas = {'isbind': AccountConst.USER_TYPE_SNS,
                 'snsId': qid,
                 'createTime': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                 'clientId': clientId,
                 'appId': appId,
                 'userId': uid,
                 }
        udkv = []
        for k, v in datas.items():
            udkv.append(k)
            udkv.append(v)
        TyContext.RedisUser.execute(uid, 'HMSET', 'user:%s' % uid, *udkv)
        TyContext.MySqlSwap.updateUserDataAliveTime(uid)
        TyContext.UserProps.incr_chip2(
            uid, int(appId), balance, TyContext.ChipNotEnoughOpMode.NOOP,
            20000, clientId=clientId)
        TyContext.UserProps.incr_coin(
            uid, int(appId), 0, TyContext.ChipNotEnoughOpMode.NOOP,
            TyContext.BIEventId.UNKNOWN, clientId=clientId)
        TyContext.UserProps.incr_diamond(
            uid, int(appId), 0, TyContext.ChipNotEnoughOpMode.NOOP,
            TyContext.BIEventId.UNKNOWN, clientId=clientId)
        TyContext.RedisUserKeys.execute('SET', 'snsidmap:' + qid, uid)
        TyContext.RedisMix.execute('HDEL', 'qid.balance', qid)
        TyContext.ftlog.info('TuYouSLL __create_user for qid', qid,
                             'userid', uid, 'balance', balance)
        return uid

    @classmethod
    def _qipai_check_sign(cls, order_id, sign):
        key = TyContext.Configure.get_global_item_str('qipai_sign_key')
        mysign = hashlib.md5(order_id + key).hexdigest()
        if mysign != sign:
            TyContext.ftlog.error('TuYouSLL _qipai_check_sign failed: mysign', mysign,
                                  'order_id', order_id, 'sign', sign)
            return False
        return True

    @classmethod
    def _qipai_ipauth(cls):
        qipai_srvip = TyContext.RunHttp.get_client_ip()
        valid_ips = TyContext.Configure.get_global_item_json('qipai_servers_ip', [])
        if qipai_srvip not in valid_ips:
            TyContext.ftlog.error('TuYouSLL _qipai_ipauth failed:', qipai_srvip,
                                  'not in', valid_ips)
            ipauth = TyContext.Configure.get_global_item_int('qipai_ipauth')
            if ipauth:
                return False
        return True

    @classmethod
    def qipai_addchip(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouSLL qipai_addchip params', params)

        if not cls._qipai_ipauth():
            return 'invalid source ip'

        trans_id = params['trans_id']
        dedup = Deduplicates('pc_qipai_delivered_transids')
        if dedup.is_key_duplicated(trans_id):
            TyContext.ftlog.error('TuYouSLL qipai_addchip trans_id', trans_id,
                                  'already delivered. params', params)
            return 'trans_id already delivered'

        sign = params['sign']
        if not cls._qipai_check_sign(trans_id, sign):
            return 'sign wrong'

        qid = params['qid']
        userid = cls._find_userid_by_qid('360:' + params['qid'])
        if not userid:
            return 'tuyoo user not found for qid %s' % qid

        game_code = params['game_code']
        gameid_dict = TyContext.Configure.get_global_item_json('qipai_gamecode2gameid', {})
        gameid = int(gameid_dict.get(game_code, 6))
        count = int(params['chip_count'])
        delta, chip = TyContext.UserProps.incr_chip2(
            userid, gameid, count, TyContext.ChipNotEnoughOpMode.NOOP,
            TyContext.BIEventId.BUY_PRODUCT)

        dedup.mark_key_exists(trans_id)

        product_name = params['product_name']
        cls._record_charge_event(gameid, userid, delta, 0, trans_id,
                                 '360PC_' + product_name, '360pc')
        cls._notify_game_server({'appId': gameid, 'userId': userid,
                                 'delta_chip': delta})

        TyContext.ftlog.info('TuYouSLL qipai_addchip add', count, 'chips for user',
                             userid, 'final chip', chip)
        # 0 for success, other for failure
        return '0'

    @classmethod
    def _notify_game_server(cls, params):
        clientId = TyContext.UserSession.get_session_clientid(params['userId'])
        control = TyContext.ServerControl.findServerControl(params['appId'], clientId)
        if not control:
            TyContext.ftlog.error('_notify_game_server can not find'
                                  ' server control, params', params)
            return
        notifyUrl = str(control['http'] + '/v2/game/charge/qipainotify?' + urlencode(params))
        TyContext.ftlog.debug('_notify_game_server'
                              ' arguments', params, 'notifyUrl', notifyUrl)
        # 通知游戏服务端进行vip等级的更新
        rmbs = 0.0
        diamonds = 0
        if 'delta_chip' in params:
            rmbs += params['delta_chip'] / 10000.0
            diamonds += int(params['delta_chip'] / 1000)
        if 'delta_diamond' in params:
            rmbs += params['delta_diamond'] / 10.0
            diamonds += int(params['delta_diamond'])
        PayHelper.notify_game_server_on_diamond_change(
            {'appId': params['appId'], 'clientId': clientId, 'buttonId': '360KP_PROD',
             'userId': params['userId'], 'diamonds': diamonds, 'rmbs': rmbs})

        from twisted.web import client
        d = client.getPage(notifyUrl, method='GET')

        def ok_callback(response):
            TyContext.ftlog.info('_notify_game_server response', response)

        def err_callback(error):
            TyContext.ftlog.error('_notify_game_server error', error)

        d.addCallbacks(ok_callback, err_callback)

    @classmethod
    def _record_charge_event(cls, appId, userId, chip_count, diamond_count,
                             trans_id, product_name, paytype):
        clientId = TyContext.UserSession.get_session_clientid(userId)
        total_fee = chip_count / 10000.0 + diamond_count / 10.0

        # fake platform order, for gdss' sake
        ts = int(time.time())
        seqNum = int(TyContext.RedisMix.execute('INCR', 'global.orderid.seq.a'))
        fake_order = paytype + TyContext.strutil.tostr62(ts, 6) + \
                     TyContext.strutil.tostr62(seqNum, 3)

        ct = datetime.now()
        paykey = ct.strftime('pay:%Y%m%d')
        name = u'%d钻石' % diamond_count if diamond_count else u'%d金币' % chip_count
        payinfo = {'time': ct.strftime('%Y%m%d%H%M%S'),
                   'uid': userId,
                   'appId': appId,
                   'name': name,
                   'fee': total_fee,
                   'type': paytype,
                   'clientId': clientId,
                   'tyOrderId': fake_order,
                   'appOrderId': trans_id,
                   'prodId': product_name,
                   }
        TyContext.RedisPayData.execute('LPUSH', paykey, json.dumps(payinfo))
        # XXX 这里payCount加1不严格，但为了首充礼包，先加上。暂时无副作用
        PayHelper.incr_paycount(userId)
        TyContext.RedisUser.execute(userId, 'HINCRBYFLOAT', 'user:' + str(userId), 'chargeTotal', total_fee)

    @classmethod
    def qipai_getchip(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouSLL qipai_getchip params', params)

        qid = params.get('qid', '')
        userid = cls._find_userid_by_qid('360:' + qid)
        if not userid:
            TyContext.ftlog.error('TuYouSLL qipai_getchip: tuyoo user not found for qid %s' % qid)
            return 0
        chip = TyContext.RedisUser.execute(userid, 'HGET', 'user:%s' % userid, 'chip')
        TyContext.ftlog.info('TuYouSLL qipai_getchip for qid %s: %d chips for user %d' % (qid, chip, userid))
        return chip

    '''
    @classmethod
    def kp_login(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouSLL kp_login params', params)

        qid = params.get('uid', '')
        gkey = params.get('gkey', '')
        if not qid or not gkey:
            TyContext.ftlog.error('TuYouSLL kp_login no uid or gkey')
            return 'no uid or gkey'

        session_key = 'kp_login:%s' % qid
        TyContext.RedisMix.execute('HSET', session_key, 'gkey', gkey)
        TyContext.RedisMix.execute('EXPIRE', session_key, 600)
        TyContext.ftlog.debug('kp_login HSET session_key', session_key,
                              'gkey', gkey)

        code_uri = quote('http://s1.%s.g.360-g.net/open/v3/user/kaiping/code' % gkey)
        location = 'http://oauth.open.wan.360.cn/access_appcode_get?' \
            'client_id=%s&redirect_uri=%s' % (gkey, code_uri)
        try:
            TyContext.RunHttp.redirect(location)
        except Exception as e:
            TyContext.ftlog.error('kp_login redirect ERROR', e)
            return 'redirect fail'
        TyContext.ftlog.info('kp_login redirected to', location)

    '''

    @classmethod
    def kp_code(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouSLL kp_code params', params)

        qid = params.get('uid', '')
        code = params.get('code', '')
        if not qid or not code:
            TyContext.ftlog.error('kp_code no uid or code')
            return 'no uid or code'

        ret = {'errno': 0, 'errmsg': 'success'}

        session_key = 'kp_login:%s' % qid
        client_id = TyContext.RedisMix.execute('HGET', session_key, 'gkey')
        TyContext.ftlog.debug('kp_login HGET session_key', session_key,
                              'gkey', client_id)
        configs = TyContext.Configure.get_global_item_json(
            'kaiping_configs', {})
        client_secret = configs.get(client_id, (0, 0, 0))[0]
        if not client_id or not client_secret:
            TyContext.ftlog.error('kp_code error: no client_id or client_secret')
            return 'no client_id or client_secret'

        code_uri = quote('http://s1.%s.g.360-g.net/open/v3/user/kaiping/code' % client_id)
        location = 'http://oauth.open.wan.360.cn/access_token?' \
                   'grant_type=authorization_code&' \
                   'code=%s&client_secret=%s&client_id=%s&redirect_uri=%s' \
                   % (code, client_secret, client_id, code_uri)
        try:
            response, _ = TyContext.WebPage.webget(location)
        except Exception as e:
            TyContext.ftlog.error('kp_code get access_token ERROR', e)
            ret['errno'] = -1
            ret['errmsg'] = str(e)
            return json.dumps(ret)
        TyContext.ftlog.info('kp_code get access_token response', response)

        try:
            res = json.loads(response)
            errno = res['errno']
            errmsg = res['errmsg']
            data = res['data']
            access_token = data['access_token']
        except Exception as e:
            TyContext.ftlog.error('kp_code json error for access_token', e)
            ret['errno'] = -1
            ret['errmsg'] = str(e)
            return json.dumps(ret)

        data = {'auth_key': '', 'zone': 0}  # , 'extraInfo': ''}
        auth_key = str(uuid.uuid4()).replace('-', '')
        TyContext.RedisMix.execute('HMSET', session_key, 'auth_key', auth_key,
                                   'access_token', access_token)
        data['auth_key'] = auth_key
        ret['data'] = data
        TyContext.ftlog.info('kp_code return', ret)
        return json.dumps(ret)

    @classmethod
    def kp_login(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouSLL kp_login params', params)

        qid = params.get('uid', '')
        gkey = params.get('gkey', '')
        # 兼容360比赛登录请求，该模式需要返回jsonp格式
        callback_fun = params.get('callback', '')
        matchid = params.get('matchid', '')
        if not qid or not gkey:
            TyContext.ftlog.error('TuYouSLL kp_login no uid or gkey')
            return 'no uid or gkey'

        # 获取360vip值
        vip360 = cls.get_360_vip(qid, gkey)
        userid = cls._find_userid_by_qid('360:%s' % qid)
        if userid:
            TyContext.RedisUser.execute(userid, 'HSET', 'user:%s' % userid, '360.vip', vip360)
            TyContext.ftlog.info('TuYouSLL kp_login set_360_vip success', 'user_id', userid, '360.vip', vip360)
        else:
            TyContext.ftlog.info('TuYouSLL kp_login set_360_vip error', 'snsid', '360:%s' % qid, 'userid', userid)

        session_key = 'kp_login:%s' % qid
        TyContext.RedisMix.execute('HMSET', session_key, 'gkey', gkey, 'callback_fun', callback_fun, 'matchid', matchid,
                                   'vip360', vip360)
        TyContext.RedisMix.execute('EXPIRE', session_key, 600)
        TyContext.ftlog.debug('kp_login HMSET session_key', session_key,
                              'gkey', gkey, 'callback_fun', callback_fun, 'matchid', matchid)

        ret = {'errno': 0, 'errmsg': 'success'}
        data = {'auth_key': '', 'zone': 0, 'extraInfo': ''}
        auth_key = str(uuid.uuid4()).replace('-', '')
        TyContext.RedisMix.execute('HMSET', session_key, 'auth_key', auth_key)
        extraInfo = ''
        if matchid != None and matchid != '':
            extraInfo = "matchid=" + str(matchid)

        data['extraInfo'] = extraInfo
        data['auth_key'] = auth_key
        ret['data'] = data
        TyContext.ftlog.info('kp_code return', ret)
        # 如果callback_fun存在，返回jsonp格式
        if callback_fun != None and callback_fun != '':
            return str(callback_fun) + '(' + json.dumps(ret) + ')'
        else:
            return json.dumps(ret)

    @classmethod
    def kp_login_new(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouSLL kp_login_new params', params)

        qid = params.get('uid', '')
        gkey = params.get('gkey', '')
        # 兼容360比赛登录请求，该模式需要返回jsonp格式
        callback_fun = params.get('callback', '')
        matchid = params.get('matchid', '')
        if not qid or not gkey:
            TyContext.ftlog.error('TuYouSLL kp_login_new no uid or gkey')
            return 'no uid or gkey'

        # 获取360vip值
        vip360 = cls.get_360_vip(qid, gkey)
        userid = cls._find_userid_by_qid('360:%s' % qid)
        if userid:
            TyContext.RedisUser.execute(userid, 'HSET', 'user:%s' % userid, '360.vip', vip360)
            TyContext.ftlog.info('TuYouSLL kp_login_new set_360_vip success', 'user_id', userid, '360.vip', vip360)
        else:
            TyContext.ftlog.info('TuYouSLL kp_login_new set_360_vip error', 'snsid', '360:%s' % qid, 'userid', userid)

        session_key = 'kp_login:%s' % qid
        TyContext.RedisMix.execute('HMSET', session_key, 'gkey', gkey, 'callback_fun', callback_fun, 'matchid', matchid)
        TyContext.RedisMix.execute('EXPIRE', session_key, 600)
        TyContext.ftlog.debug('kp_login_new HMSET session_key', session_key,
                              'gkey', gkey, 'callback_fun', callback_fun, 'matchid', matchid)

        code_uri = quote('http://s1.%s.g.360-g.net/open/v3/user/kaiping/code' % gkey)
        location = 'http://oauth.open.wan.360.cn/access_appcode_get?' \
                   'client_id=%s&redirect_uri=%s' % (gkey, code_uri)
        try:
            TyContext.RunHttp.redirect(location)
        except Exception as e:
            TyContext.ftlog.error('kp_login_new redirect ERROR', e)
            return 'redirect fail'
        TyContext.ftlog.info('kp_login_new redirected to', location)

    @classmethod
    def kp_code_new(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('TuYouSLL kp_code params', params)

        qid = params.get('uid', '')
        code = params.get('code', '')
        if not qid or not code:
            TyContext.ftlog.error('kp_code no uid or code')
            return 'no uid or code'

        ret = {'errno': 0, 'errmsg': 'success'}

        session_key = 'kp_login:%s' % qid
        client_id, callback_fun, matchid = TyContext.RedisMix.execute('HMGET', session_key, 'gkey', 'callback_fun',
                                                                      'matchid')
        TyContext.ftlog.debug('kp_login HMGET session_key', session_key,
                              'gkey', client_id, 'callback_fun', callback_fun, 'matchid', matchid)
        configs = TyContext.Configure.get_global_item_json(
            'kaiping_configs', {})
        client_secret = configs.get(client_id, (0, 0, 0))[0]
        if not client_id or not client_secret:
            TyContext.ftlog.error('kp_code error: no client_id or client_secret')
            return 'no client_id or client_secret'

        code_uri = quote('http://s1.%s.g.360-g.net/open/v3/user/kaiping/code' % client_id)
        location = 'http://oauth.open.wan.360.cn/access_token?' \
                   'grant_type=authorization_code&' \
                   'code=%s&client_secret=%s&client_id=%s&redirect_uri=%s' \
                   % (code, client_secret, client_id, code_uri)
        try:
            response, _ = TyContext.WebPage.webget(location)
        except Exception as e:
            TyContext.ftlog.error('kp_code get access_token ERROR', e)
            ret['errno'] = -1
            ret['errmsg'] = str(e)
            return json.dumps(ret)
        TyContext.ftlog.info('kp_code get access_token response', response)

        try:
            res = json.loads(response)
            errno = res['errno']
            errmsg = res['errmsg']
            data = res['data']
            access_token = data['access_token']
        except Exception as e:
            TyContext.ftlog.error('kp_code json error for access_token', e)
            ret['errno'] = -1
            ret['errmsg'] = str(e)
            return json.dumps(ret)

        data = {'auth_key': '', 'zone': 0, 'extraInfo': ''}
        auth_key = str(uuid.uuid4()).replace('-', '')
        TyContext.RedisMix.execute('HMSET', session_key, 'auth_key', auth_key,
                                   'access_token', access_token)
        extraInfo = ''
        if matchid != None and matchid != '':
            extraInfo = "matchid=" + str(matchid)

        data['extraInfo'] = extraInfo
        data['auth_key'] = auth_key
        ret['data'] = data
        TyContext.ftlog.info('kp_code_new return', ret)
        # 如果callback_fun存在，返回jsonp格式
        if callback_fun != None and callback_fun != '':
            return str(callback_fun) + '(' + json.dumps(ret) + ')'
        else:
            return json.dumps(ret)

    @classmethod
    def get_360_vip(cls, qid, gkey):

        if not qid or not gkey:
            TyContext.ftlog.error('get_360_vip no uid or gkey')
            return 0

        configs = TyContext.Configure.get_global_item_json(
            'kaiping_configs', {})
        lkey = configs.get(gkey, (0, 0, 0))[2]
        if not gkey or not lkey:
            TyContext.ftlog.error('get_360_vip error: no gkey or lkey')
            return 0

        # 签名: md5($gkey.$uid.$time.$lkey)
        # ($lkey为登陆密钥，注：uid为urldecode之后的值，“.”为连接符)
        ts = int(time.time())
        sign_str = str(gkey) + str(qid) + str(ts) + str(lkey)
        sign = hashlib.md5(sign_str).hexdigest().lower()
        version = '3.0'

        location = 'http://rcapi.360-g.net/vplan_wan?' \
                   'uid=%s&gkey=%s&time=%s&sign=%s&version=%s' \
                   % (qid, gkey, ts, sign, version)
        try:
            response, _ = TyContext.WebPage.webget(location)
        except Exception as e:
            TyContext.ftlog.error('get_360_vip ERROR', e)
            return 0
        TyContext.ftlog.info('get_360_vip response', response)

        try:
            res = json.loads(response)
            if res and res['errno'] == 0 and res['data']:
                user_360_type = res['data']['type']
            else:
                user_360_type = 'N'
        except Exception as e:
            TyContext.ftlog.error('get_360_vip json error for level', e)
            return 0

        # N是非会员 E是过期会员 Y是年费  M是月费
        if user_360_type == 'Y' or user_360_type == 'M':
            return 1
        else:
            return 0

    @classmethod
    def kp_checkuser(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('kp_checkuser params', params)

        try:
            qid = params['uid']
            platform = params['platform']
            gkey = params['gkey']
            skey = params['skey']
            ts = params['time']
            sign = params['sign']
        except Exception as e:
            ret = {'errno': -2, 'errmsg': str(e)}
            TyContext.ftlog.error('kp_checkuser error:', e)
            return json.dumps(ret)

        configs = TyContext.Configure.get_global_item_json(
            'kaiping_configs', {})
        config = configs.get(gkey)
        if not config or not config[2]:
            ret = {'errno': -5, 'errmsg': 'lkey not configured'}
            TyContext.ftlog.error('kp_checkuser error:', ret)
            return json.dumps(ret)

        # 签名: md5($uid.$platform.$gkey.$skey.$time.'#'.$lkey)
        # ($lkey为登陆密钥，注：uid为urldecode之后的值，“.”为连接符)
        lkey = config[2]
        sign_str = ''.join((qid, platform, gkey, skey, ts)) + '#' + lkey
        if md5.new(sign_str).hexdigest() != sign.lower():
            ret = {'errno': -2, 'errmsg': 'sign error'}
            TyContext.ftlog.error('kp_checkuser error:', ret)
            return json.dumps(ret)

        userid = cls._find_userid_by_qid('360:' + qid)
        if not userid:
            ret = {'errno': -1, 'errmsg': 'no user'}
            TyContext.ftlog.error('kp_checkuser error:', ret)
            return json.dumps(ret)
        data = []
        userinfo = {}
        nickname = TyContext.RedisUser.execute(userid, 'HGET', 'user:%s' % userid, 'name')
        if nickname:
            userinfo['nickname'] = nickname
        else:
            userinfo['nickname'] = ''
        data.append(userinfo)
        ret = {'errno': 0, 'errmsg': 'success', 'data': data}
        TyContext.ftlog.info('kp_checkuser success:', ret)
        return json.dumps(ret)

    @classmethod
    def kp_exchange(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('kp_exchange params', params)

        try:
            qid = params['uid']
            platform = params['platform']
            gkey = params['gkey']
            skey = params['skey']
            ts = params['time']
            order_id = params['order_id']
            coins = params['coins']
            moneys = params['moneys']
            sign = params['sign']
        except Exception as e:
            ret = {'errno': -1, 'errmsg': str(e)}
            TyContext.ftlog.error('kp_exchange error:', e)
            return json.dumps(ret)

        configs = TyContext.Configure.get_global_item_json(
            'kaiping_configs', {})
        config = configs.get(gkey)
        if not config:
            ret = {'errno': -5, 'errmsg': 'gkey not configured'}
            TyContext.ftlog.error('kp_exchange error:', ret)
            return json.dumps(ret)

        _, pkey, _, gameid = config
        TyContext.ftlog.debug('kp_exchange client_id', gkey, 'pay_key', pkey)
        if not pkey:
            ret = {'errno': -5, 'errmsg': 'pay_key null'}
            TyContext.ftlog.error('kp_exchange error:', ret)
            return json.dumps(ret)

        # md5($uid.$platform.$gkey.$skey.$time.$order_id.$coins.$moneys'#'.$pkey)
        sign_str = ''.join((qid, platform, gkey, skey, ts, order_id, coins,
                            moneys)) + '#' + pkey
        if md5.new(sign_str).hexdigest() != sign.lower():
            ret = {'errno': -2, 'errmsg': 'sign error'}
            TyContext.ftlog.error('kp_exchange error:', ret)
            return json.dumps(ret)

        userid = cls._find_userid_by_qid('360:' + qid)
        if not userid:
            ret = {'errno': -3, 'errmsg': 'no user'}
            return json.dumps(ret)

        dedup = Deduplicates('pc_kaiping_delivered_order_ids')
        if dedup.is_key_duplicated(order_id):
            ret = {'errno': 1, 'errmsg': 'duplicate order_id'}
            TyContext.ftlog.error('kp_exchange error:', ret)
            return json.dumps(ret)

        count = int(coins)
        delta, _ = TyContext.UserProps.incr_diamond(
            userid, gameid, count, TyContext.ChipNotEnoughOpMode.NOOP,
            TyContext.BIEventId.BUY_PRODUCT)

        dedup.mark_key_exists(order_id)

        cls._record_charge_event(gameid, userid, 0, delta, order_id,
                                 '360KP_PROD', '360kp')
        cls._notify_game_server({'appId': gameid, 'userId': userid,
                                 'delta_chip': 0, 'delta_diamond': delta})
        data = {'order_id': order_id, 'uid': qid, 'role_id': userid,
                'role_name': '', 'platform': platform, 'gkey': gkey,
                'skey': skey, 'coins': coins, 'moneys': moneys,
                'time': int(time.time())}
        ret = {'errno': 0, 'errmsg': 'success', 'data': data}
        TyContext.ftlog.info('kp_exchange success:', ret)
        return json.dumps(ret)
