# -*- coding=utf-8 -*-

# Author:        zhaoqinghui@hoolai.com
# Company:       Hoolai.Inc
# Created:       2013年01月25日 星期六 00时34分53秒
# FileName:      account.py
# Class:         Account

import json

from tyframework.context import TyContext


######################################################################
# 360登录过程的主要逻辑实现
#
######################################################################
class Account360():
    sexMem = repr('男').replace('\\', '').replace('\'', '')

    @classmethod
    def isDefault360Username(cls, username):
        if not isinstance(username, unicode):
            username = str(username)
        return username and username.startswith('360U')

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        ret = cls._doGetUserInfo(params, snsId)
        TyContext.ftlog.info('doGetUserInfo360 ret', ret, 'params', params)
        return ret

    @classmethod
    def _doGetUserInfo(cls, params, snsId):
        if snsId.startswith('360token:'):
            access_token = snsId[9:]
            if access_token == 'null' or access_token == 'undefined' or len(access_token) <= 0:
                return False

            return cls._get_userinfo_by_token(params, access_token)
        elif snsId.startswith('360kp:'):
            '''
            qid, auth_key = snsId[6:].split('_')
            return cls._get_userinfo_from_kaiping(params, qid, auth_key)
            '''
            qid, auth_key = snsId[6:].split('_')
            params['snsId'] = '360:' + str(qid)
            try:
                userid = cls._find_userid_by_qid('360:%s' % qid)
                session_key = 'kp_login:%s' % qid
                vip360 = TyContext.RedisMix.execute('HGET', session_key, 'vip360')
                if userid > 0 and vip360:
                    TyContext.RedisUser.execute(userid, 'HSET', 'user:%s' % userid, '360.vip', vip360)
                    TyContext.ftlog.info('Account360 set_360_vip success', 'user_id', userid, '360.vip', vip360)
                if vip360 != None:
                    params['vip360'] = vip360
            except:
                pass
            return True
        elif snsId.startswith('360qt:'):
            q, t = snsId[6:].split('&')
            return cls._get_userinfo_by_qt(params, q, t)
        else:
            code = snsId[4:].strip()
            if code == 'null' or code == 'undefined' or len(code) <= 0:
                return False

            if len(code) < 20:
                return True

            access_token = cls._get_accesstoken(params, code)
            if access_token:
                return cls._get_userinfo_by_token(params, access_token)

    @classmethod
    def _get_accesstoken(cls, params, code):
        appId = params['appId']
        clientId = params['clientId']
        client_ids = TyContext.Configure.get_game_item_json(appId, 'account.360.client.version', {})
        clientver = ''
        if clientId in client_ids:
            clientver = str(client_ids[clientId])
        client_id = TyContext.Configure.get_game_item_str(appId, 'account.360.client.id' + clientver)
        client_secret = TyContext.Configure.get_game_item_str(appId, 'account.360.client.secret' + clientver)

        if not client_id or not client_secret:
            TyContext.ftlog.error('Account360 the appinfo of appId %d is not found !' % (appId))
            return None

        tokenurl = 'https://openapi.360.cn/oauth2/access_token?grant_type=authorization_code&' + \
                   'client_id=%s&client_secret=%s&redirect_uri=oob&code=%s' % (client_id, client_secret, code)
        tokenurl = tokenurl.encode('ascii')
        TyContext.ftlog.debug('Account360->access token url->', tokenurl)
        try:
            response, tokenurl = TyContext.WebPage.webget(tokenurl)
        except Exception as e:
            TyContext.ftlog.error('Account360->access token url ERROR', e)
            return None
        accessToken = None
        try:
            datas = json.loads(response)
            accessToken = datas['access_token']
        except:
            TyContext.ftlog.error('Account360->access token url return ERROR, response=', response)
        return accessToken

    @classmethod
    def _get_userinfo_from_kaiping(cls, params, qid, auth_key):
        session_key = 'kp_login:%s' % qid
        auth_key, access_token = TyContext.RedisMix.execute(
            'HMGET', session_key, 'auth_key', 'access_token')
        TyContext.ftlog.debug('Account360->_get_userinfo_from_kaiping session_key:',
                              session_key, 'auth_key', auth_key,
                              'access_token', access_token)
        if not auth_key or not access_token:
            TyContext.ftlog.error('Account360->_get_userinfo_from_kaiping'
                                  ' session missing:', session_key, auth_key,
                                  access_token)
            return False

        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'access_token': access_token}
        infourl = 'http://g.360-api.cn/user/show?uid=%s' % qid
        try:
            response, _ = TyContext.WebPage.webget(infourl, method_='GET', headers_=headers)
        except Exception as e:
            TyContext.ftlog.error('Account360->_get_userinfo_from_kaiping ERROR', e)
            return False
        TyContext.ftlog.debug('Account360->_get_userinfo_from_kaiping response', response)

        try:
            infos = json.loads(response)
        except Exception:
            TyContext.ftlog.error('Account360->_get_userinfo_from_kaiping json parse ERROR, response=', response)
            return False

        TyContext.ftlog.info('Account360->_get_userinfo_from_kaiping response=', infos)
        if not infos or int(infos['errno']) != 0:
            TyContext.ftlog.error('Account360->_get_userinfo_from_kaiping return ERROR, infos', infos)
            return False

        data = infos['data']
        params['snsId'] = '360:' + str(data['uid'])
        params['name'] = data.get('uname')
        try:
            params['purl'] = data['avatar']['big']
        except:
            TyContext.ftlog.error('Account360->_get_userinfo_from_kaiping no purl present')
        return True

    @classmethod
    def _get_userinfo_by_qt(cls, params, q, t):
        # q, t should be already urlencoded
        qtverify_proxy = TyContext.Configure.get_global_item_str('winpc_360qt_verify_proxy')
        if qtverify_proxy:
            infourl = qtverify_proxy % (q, t)
        else:
            # test server
            infourl = 'http://101.199.99.156:20001/api.php?head_size=100_100&Q=%s&T=%s' % (q, t)
        try:
            response, infourl = TyContext.WebPage.webget(infourl)
        except Exception as e:
            TyContext.ftlog.error('Account360->_get_userinfo_by_qt ERROR', e)
            return False
        try:
            # jisheng use trunked encoding in his proxy, so the response consists
            # of a trunk-size and the corresponding trunk-data, separated by \r\n
            infos = json.loads(response.split('\r\n')[1])
        except Exception:
            TyContext.ftlog.error('Account360->_get_userinfo_by_qt return ERROR, response=', response)
            return False

        TyContext.ftlog.debug('Account360->_get_userinfo_by_qt response=', infos)
        if not infos or infos['errno'] != '0':
            TyContext.ftlog.error('Account360->_get_userinfo_by_qt return ERROR, infos', infos)
            return False

        infos = infos['data']
        params['snsId'] = '360:' + str(infos['qid'])
        nickname = infos.get('nickName')
        if not nickname:
            nickname = infos['userName']
        params['name'] = nickname
        params['snsinfo'] = infos['userName']
        params['purl'] = infos['imageUrl']
        return True

    @classmethod
    def _get_userinfo_by_token(cls, params, access_token):
        if access_token is None or len(access_token) < 20:
            TyContext.ftlog.error('Account360->_get_userinfo_by_token token error', access_token)
            return False
        appId = params['appId']
        infourl = 'https://openapi.360.cn/user/me.json?fields=id,name,nick,' \
                  'avatar,sex,area&access_token=' + access_token
        infourl = infourl.encode('ascii')
        try:
            response, infourl = TyContext.WebPage.webget(infourl)
        except Exception as e:
            TyContext.ftlog.error('Account360->open userinfo url ERROR', e)
            return False
        try:
            infos = json.loads(response)
        except Exception:
            TyContext.ftlog.error('Account360->user info url return ERROR, response=', response)
            return False

        if infos:
            params['snsId'] = '360:' + str(infos['id'])
            nickname = infos.get('nick')
            if not nickname:
                nickname = infos['name']
            params['snsinfo'] = infos['name']
            # params['purl'] = infos['avatar']
            params['address'] = infos['area']
            no_sync_360_appids = TyContext.Configure.get_global_item_json('no_sync_360_info_appid', [9999, 8, 21])
            if not appId in no_sync_360_appids:
                sex360 = repr(infos['sex']).replace('\\', '').replace('\'', '')
                sex = 0
                if sex360.find(cls.sexMem) >= 0:
                    sex = 1
                params['sex'] = sex
                params['name'] = nickname
            return True
        return False

    @classmethod
    def _find_userid_by_qid(cls, qid):
        uid = TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + str(qid))
        if not uid or uid <= 0:
            return 0
        try:
            from tysdk.entity.user_common.account_helper import AccountHelper
            TyContext.MySqlSwap.checkUserDate(uid)
            AccountHelper.restore_avatar_verify_set(uid)
            return uid
        except:
            TyContext.ftlog.error('Account360 _find_userid_by_qid can not find'
                                  ' user for qid', qid)
            return 0
