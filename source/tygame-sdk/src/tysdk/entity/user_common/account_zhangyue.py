# -*- coding=utf-8 -*-

import json
import time

from OpenSSL.crypto import load_privatekey, FILETYPE_PEM

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay.rsacrypto import _sign_with_privatekey_openssl


class AccountZhangyue():
    VALIDATE_URL = 'https://uc.ireader.com/open/token/check'

    @classmethod
    def doGetUserInfo(cls, params, snsId):
        app_id = params['zhangyue_appId']
        uid = params['zhangyue_uid']
        token = params["zhangyue_token"]

        if uid.startswith('gameyk_'):
            return True

        mainChannel = params['clientId'].split('.')[-2]
        config = GameItemConfigure(params['appId']).get_game_channel_configure_by_primarykey('zhangyue',
                                                                                             'zhangyue_appId',
                                                                                             app_id,
                                                                                             mainChannel)
        rsa_key = config["zhangyue_rsa_key"]
        wrap_rsa_key = cls.loadRsaKey(rsa_key, '-----BEGIN RSA PRIVATE KEY-----', '-----END RSA PRIVATE KEY-----')
        TyContext.ftlog.debug('AccountZhangyue -> wrap rsa key ->', wrap_rsa_key)
        privateKey = load_privatekey(FILETYPE_PEM, wrap_rsa_key)

        rparams = {
            "app_id": app_id,
            "open_uid": uid,
            "access_token": token,
            "timestamp": int(time.time()),
            "sign_type": "RSA",
            "version": '"1.0'
        }

        data = '&'.join(['%s=%s' % (k, v) for k, v in sorted(rparams.items()) if v])
        sign = _sign_with_privatekey_openssl(data, privateKey)
        rparams["sign"] = sign
        response_msg, _ = TyContext.WebPage.webget(cls.VALIDATE_URL, rparams, method_='GET')
        TyContext.ftlog.debug('AccountZhangyue -> response ->', response_msg)
        resp = json.loads(response_msg)
        if int(resp['code']) == 0:
            return True
        else:
            return False

    @classmethod
    def loadRsaKey(cls, key, prefix, suffix):
        key = key.replace('\r', '')
        key = key.replace('\n', '')
        if key.find(prefix) >= 0:
            key = key[len(prefix):]
        if key.find(suffix) >= 0:
            key = key[:-len(suffix)]
        data = [prefix, ]
        for i in range(0, len(key), 64):
            data.append(key[i:i + 64])
        data.append(suffix)
        return '\n'.join(data)
