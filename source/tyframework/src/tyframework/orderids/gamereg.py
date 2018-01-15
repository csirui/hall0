'''
Created on 2014年6月23日

@author: zjgzzz@126.com
'''
from tyframework._private_.msg.msg import MsgPack
from tyframework.orderids import gaofangip

_RKEY = 'hall:map.game.servers'


class sdkconf(object):
    @classmethod
    def getFirstLoginForbid(cls, clientId):
        from tyframework.context import TyContext
        confs = TyContext.Configure.get_game_item_json(9998, 'game.forbid.clientids', [])
        if clientId in confs:
            return True
        return False

    @classmethod
    def getFirstLoginForbidMsg(cls):
        from tyframework.context import TyContext
        return TyContext.Configure.get_game_item_str(9998, 'game.forbid.msg', '')

    @classmethod
    def getHttpGameDomain(cls, clientId):
        from tyframework.context import TyContext
        confs = TyContext.Configure.get_game_item_json(9998, 'game.branch', {})
        httpgame = None
        for conf in confs:
            cids = conf['clientIds']
            if TyContext.strutil.reg_matchlist(cids, clientId):
                httpgame = conf['http_game']
                break
        if not httpgame:
            httpgame = 'http://10.3.0.18'
        return httpgame


def _loadRegGames():
    from tyframework.context import TyContext
    jsonstr = TyContext.RedisMix.execute('GET', _RKEY)
    return TyContext.strutil.loads(jsonstr, False, True, {})


def _saveRegGames(games):
    from tyframework.context import TyContext
    TyContext.RedisMix.execute('SET', _RKEY, TyContext.strutil.dumps(games))
    # 通知所有进程, 重新装载配置


#     configure.notifyConfigureChanged([_RKEY], ['global'])


def registerServer(http_game, mode, name, conns, rtime):
    from tyframework.context import TyContext
    if TyContext.TYGlobal.mode() in (1, 2):
        if mode not in (1, 2):
            return False, 'error, online sdk must be with online or audit servers !!'

    games = _loadRegGames()

    if conns:
        games[http_game] = {'http_game': http_game,
                            'mode': mode,
                            'name': name,
                            'conns': conns,
                            'time': rtime
                            }
        _saveRegGames(games)

    return True, games


def unRegisterServer(http_game):
    games = _loadRegGames()
    if http_game in games:
        del games[http_game]
        _saveRegGames(games)
    return True, games


def listRegisterServer():
    gamesDb = _loadRegGames()
    return gamesDb, gamesDb


def _findRegGame(clientId):
    from tyframework.context import TyContext
    games = _loadRegGames()
    http_game = sdkconf.getHttpGameDomain(clientId)
    game = games.get(http_game, None)
    TyContext.ftlog.debug('findUserTcpAddress->', http_game, games)
    if not game and len(games) == 1:
        game = games.values()[0]
    if not game:
        vals = games.values()
        for g in vals:
            if g['mode'] == 1:
                game = g
                break
    if not game and len(games) > 0:
        game = games.values()[0]
    #     if not game :
    #         raise Exception('can not find the conns of : clientId=' + str(clientId))
    return game


def findUserTcpAddress(userId, clientId):
    from tyframework.context import TyContext
    ip, port = gaofangip.getGaoFangIp2(userId, clientId)
    if ip:
        ipport = [ip, port]
    else:
        game = _findRegGame(clientId)
        if not game:
            return ['1.1.1.1', 1]  # 新的hall5不再SDK进行注册，tcp连接信息需要前端二次请求hall5的API获取
        conns = game['conns']
        ipport = conns[userId % len(conns)]
        ip, port = gaofangip.getGaoFangIp(clientId, ipport[0], ipport[1])
        ipport = [ip, port]
    TyContext.ftlog.info('tcp ipport=', ipport, 'userId=', userId, 'clientId=', clientId)
    return ipport


def findHttpGameByClientId(clientId):
    game = _findRegGame(clientId)
    return game['http_game']


def findGameModeByClientId(clientId):
    game = _findRegGame(clientId)
    return game['mode']


def findGameModeHttpByClientId(clientId):
    game = _findRegGame(clientId)
    return game['mode'], game['http_game']


def checkLoginForbid():
    '''
    检查是否被禁止登陆
    '''
    from tyframework.context import TyContext
    try:
        userId = 0
        try:
            if TyContext.RunHttp.is_current_http():
                userId = TyContext.RunHttp.getRequestParamInt('userId', 0)
            else:
                msg = TyContext.getTasklet().getMsg()
                userId = msg.getParam('userId')
        except:
            pass
        clientId, _ = TyContext.BiUtils.getClientIdNum(None, None, 9998, userId)
        forbid = sdkconf.getFirstLoginForbid(clientId)
        if forbid:
            mo = MsgPack()
            mo.setResult('code', 10)
            mo.setResult('info', sdkconf.getFirstLoginForbidMsg())
            return mo
    except:
        TyContext.ftlog.error()
    return False
