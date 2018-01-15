# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext


######################################################################
# YoukuSDK登录过程的主要逻辑实现
#
######################################################################
class AccountYouku():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        accountId = snsId[6:].strip()
        if not accountId:
            return False
        return cls._check_session(params, accountId)

    @classmethod
    def _check_session(cls, params, accountId):
        # qid=$qid&time=$time&server_id=$server_id$loginkey
        snsInfo = params['snsInfo']
        if not snsInfo:
            return False

        try:
            snsInfo = json.loads(snsInfo)
        except:
            pass
            return False
        qid = snsInfo.get('qid')
        param_time = snsInfo.get('time')
        server_id = snsInfo.get('server_id')
        sign = snsInfo.get('sign')
        name = snsInfo.get('name')

        config = TyContext.Configure.get_global_item_json('youkuh5_config', {})
        loginkey = config.get('loginKey')
        gkey = config.get('gkey')
        if not loginkey:
            TyContext.ftlog.error('AccountYouku _check_session not loginkey ', loginkey)
            return False

        check_str = 'qid=%s&time=%s&server_id=%s%s' % (qid, param_time, server_id, loginkey)
        m = md5()
        m.update(check_str)
        my_sign = m.hexdigest()
        if sign != my_sign:
            TyContext.ftlog.error(
                'AccountYouku _check_session check=%s sign=%s mysign=%s ' % (check_str, sign, my_sign))
            return False

        if name:
            params['name'] = name

        # get user info
        cls._get_userinfo(qid, gkey, loginkey, params)
        return True

    @classmethod
    def _get_userinfo(cls, qid, gkey, loginkey, params):
        # ?userid=28318249&gkey=xxx&time=1311111103&sign=90852a3c4819dbc28b20a02d300b2c9d
        import time
        time_str = str(int(round(time.time())))
        url = "http://api.wan.youku.com/tp/member/getinfo"
        check_str = '%s%s%s%s' % (qid, gkey, time_str, loginkey)
        m = md5()
        m.update(check_str)
        sign = m.hexdigest()
        url += "?userid=%s&gkey=%s&time=%s&sign=%s" % (qid, gkey, time_str, sign)
        try:
            TyContext.ftlog.debug('url', url)
            response, infourl = TyContext.WebPage.webget(url, method_='GET')
        except Exception as e:
            TyContext.ftlog.error('AccountYouku->open userinfo url ERROR', e)
            return False
        try:
            infos = json.loads(response)
        except Exception:
            TyContext.ftlog.error('AccountYouku->user info url return ERROR, response=', response)
            return False

        vip = 0
        snsinfo = {}
        if infos:
            errno = infos.get('errno', 0)
            if errno == 0:
                data = infos.get('data')
                youku_vip = data.get('vip')
                youku_name = data.get('name')
                if youku_vip:
                    snsinfo['vip'] = 1
                    # params['name'] = youku_name

        snsinfo['vip'] = vip
        # snsinfo['vip'] = 1  # todo h5
        params['snsinfo'] = json.dumps(snsinfo)
