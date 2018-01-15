# -*- coding=utf-8 -*-

import json
import time
from hashlib import md5

from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.sns4.decorator.snsv4_base import SnsV4Base
from tysdk.entity.sns4.decorator.snsv4_login import snsv4_login


class AccountUCV4(SnsV4Base):
    @snsv4_login('ucsid')
    def doGetUserInfo(cls, params, snsId):
        sid = snsId[6:].strip()
        if len(sid) <= 0:
            return False
        return cls.__get_userid(params, sid)

    @classmethod
    def __get_userid(cls, params, sid):
        uc_config = TyContext.Configure.get_global_item_json('uc_config', {})
        gameId = params['snsAppId']
        try:
            apiKey = uc_config[gameId]['apiKey']
        except KeyError:
            mainchannel = params['clientId'].split('.')[-2]
            config = GameItemConfigure(params['appId']).get_game_channel_configure_by_package('uc', 'uc_appId', gameId,
                                                                                              mainchannel)
            if not config:
                TyContext.ftlog.error('AccountUC __get_userid not uc apiKey the gameId=' + gameId)
            # 补丁 按照包名+主渠道 读取参数
            if not config:
                config = GameItemConfigure(params['appId']).get_game_channel_configure_by_package('uc', params.get(
                    'packageName'),
                                                                                                  mainchannel)
                if not config:
                    return False
            apiKey = config.get('apiKey')
        postparam = {}
        postparam['id'] = str(int(time.time()))
        data = {}
        data['sid'] = sid
        game = {}
        game['gameId'] = int(gameId)
        postparam['data'] = data
        postparam['game'] = game
        postparam['sign'] = cls.__cal_sign(sid, apiKey)

        getidurl = 'http://sdk.g.uc.cn/cp/account.verifySession'
        TyContext.ftlog.debug('AccountUC->access url->', getidurl, 'param:', postparam)
        response, tokenurl = TyContext.WebPage.webget(getidurl, postdata_=json.dumps(postparam))

        try:
            datas = json.loads(response)
            ucid = datas['data']['accountId']
            params['snsId'] = 'uc:' + ucid
        except:
            TyContext.ftlog.error('AccountUC->get userid url return ERROR, response=', response)
            return False
        return True

    @classmethod
    def __cal_sign(cls, sid, apiKey):
        check_str = 'sid=' + sid + apiKey
        m = md5()
        m.update(check_str)
        digest = m.hexdigest()
        return digest
