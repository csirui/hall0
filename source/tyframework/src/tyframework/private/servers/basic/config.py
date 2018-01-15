# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月06日 星期五 10时40分52秒
# FileName:      config.py

# from freetime.util.constants import CONF_ID
# from freetime.util.constants import CONF_SERVER_ID
# from freetime.util.constants import CONF_SERVER_MSG_TYPE
# from freetime.util.constants import CONF_MSG_TYPE_ID
# from freetime.util.constants import CONF_MSG_TYPE_LIST
# from freetime.util.constants import CONF_ROOM_ID
# from freetime.util.constants import CONF_ROOM_GAMESVR_ID
# from freetime.util.constants import CONF_ROOM_GAME_ID
# from freetime.util.constants import CONF_ROOM_DESC_DICT

CONF_ID = 0
CONF_SERVER_ID = CONF_ID
CONF_SERVER_MSG_TYPE = 1
CONF_MSG_TYPE_ID = CONF_ID
CONF_MSG_TYPE_LIST = 2
CONF_ROOM_ID = CONF_ID
CONF_ROOM_GAMESVR_ID = 2
CONF_ROOM_GAME_ID = 3
CONF_ROOM_DESC_DICT = 7


class Config:
    def __init__(self):
        self.redis_pool = None  # 现在已经废弃，为了代码兼容而保留
        self.redis_pool_config__ = None
        self.redis_pool_mix__ = None
        self.redis_cluster__ = {}
        self.redis_cluster_len__ = 0

        # Readonly DataBase Data
        self.server_type = []

        self.rooms = []
        self.room_robots = []
        self.tables = []
        self.table_configs = {}

        # 整理后的静态数据
        self.map_type_servers = {}  # key=<typeId> value=<[serverId1, serverId2, ...]>
        self.map_cmd_servers = {}  # key=<command> value=<[serverId1, serverId2, ...]>
        self.map_cmd_srvtypes = {}  # key=<command> value=<[serverTyp1, serverTyp2, ...]>
        self.map_room_servers = {}  # key=<roomId> value=<[serverId1, serverId2, ...]>
        self.map_game_servers = {}  # key=<gameId> value=<[serverId1, serverId2, ...]>
        self.map_gameid_roomids = {}  # key=<gameId> value=<[roomId1, roomId2, ...]>
        self.map_gameid_roomids_sort = {}  # key=<gameId> value=<[roomId1, roomId2, ...]>
        self.map_roomid_room = {}  # key=<roomId> value=<[roomId, roomName, ...]>
        self.map_gameid_matchs = {}
        self.map_roomid_table_config = {}  # key=<roomId> value=<item of self.table_configs>
        self.isshutdown = False

        # 每个房间可以配置不同的玩法,麻将引入
        # 比如四川麻将使用（701，702，703，704）
        # 国标麻将使用（711，712，713，714）
        self.map_playmode_roomids = {}

        # for pineapple
        self.map_playarea_servers = {}
        self.map_playarea_roomids = {}

    def initData(self, tasklet, redis_pool):
        from tyframework.context import TyContext

        self.redis_pool = redis_pool
        self.redis_pool_config__ = redis_pool
        TyContext.ftlog.info('initData->', self, self.redis_pool_config__)

        TyContext.ftlog.info('load server_type...')
        self.server_type = TyContext.Configure.get_global_item_json('server_type', [], None, True)
        self.server_type.sort(key=lambda x: x[CONF_ID])

        if TyContext.TYGlobal.gameid() == TyContext.Const.SDK_GAMEID:
            self.__init_global_user_id__()
            return

        TyContext.ftlog.info('load rooms...')
        self.rooms = TyContext.Configure.get_global_item_json('rooms', [])
        for room in self.rooms:
            TyContext.ftlog.info('load rooms...', room)
            self.map_roomid_room[room[0]] = room

            room_desc = room[len(room) - 1]
            play_mode = 'default'
            if 'play_mode' in room_desc:
                play_mode = room_desc['play_mode']
            if not play_mode in self.map_playmode_roomids:
                self.map_playmode_roomids[play_mode] = []
            self.map_playmode_roomids[play_mode].append(room[0])

        TyContext.ftlog.info('load room_robots...')
        self.room_robots = TyContext.Configure.get_global_item_json('room_robots', [])
        for rr in self.room_robots:
            TyContext.ftlog.info('load room_robots...', rr)

        sortrooms = []
        for room in self.rooms:
            if 'minCoin' in room[CONF_ROOM_DESC_DICT]:
                sortrooms.append([room[CONF_ROOM_GAME_ID], room[CONF_ID], room[CONF_ROOM_DESC_DICT]['minCoin']])
            else:
                sortrooms.append([room[CONF_ROOM_GAME_ID], room[CONF_ID], room[CONF_ID]])
            self._appendListItem2Map(self.map_gameid_roomids, room[CONF_ROOM_GAME_ID], room[CONF_ID])

        sortrooms.sort(key=lambda x: x[2], reverse=True)
        for rooms in sortrooms:
            self._appendListItem2Map(self.map_gameid_roomids_sort, rooms[0], rooms[1])

        TyContext.ftlog.info('map_gameid_roomids=', self.map_gameid_roomids)
        TyContext.ftlog.info('map_gameid_roomids_sort=', self.map_gameid_roomids_sort)

        TyContext.ftlog.info('load tables...')

        self.tables = TyContext.Configure.get_global_item_json('tables', [])
        for x in xrange(len(self.tables)):
            TyContext.ftlog.info('load tables...', self.tables[x])

        TyContext.ftlog.info('load table_config ...')
        tlist = TyContext.Configure.get_global_item_json('table_config', [])
        for t in tlist:
            self.table_configs[t[CONF_ID]] = t
            self.map_roomid_table_config[t[CONF_ROOM_ID]] = t
            TyContext.ftlog.info('load table_config ...', t)

        srvtypenamemap = {'conn': 1, 'account': 2, 'entity': 3, 'game': 4,
                          'quick': 5, 'heart': 6, 'robot': -1, 'http': -2}
        TyContext.ftlog.info('creat map_type_servers ...')
        for server in TyContext.TYGlobal.all_process():
            serverId = server['id']
            typeId = srvtypenamemap[server['type']]
            self._appendListItem2Map(self.map_type_servers, typeId, serverId)
        TyContext.ftlog.info('map_type_servers = ', self.map_type_servers)

        TyContext.ftlog.info('creat map_cmd_servers ...')
        for serverType in self.server_type:
            serverTypeId = serverType[CONF_MSG_TYPE_ID]
            TyContext.ftlog.info('map_cmd_servers', serverTypeId, serverType[CONF_MSG_TYPE_LIST])
            for serverMsg in serverType[CONF_MSG_TYPE_LIST]:
                TyContext.ftlog.info('map_cmd_servers', serverTypeId, serverMsg)
                self.map_cmd_servers[serverMsg] = self.map_type_servers[serverTypeId]
                self._appendListItem2Map(self.map_cmd_srvtypes, serverMsg, serverTypeId)

        TyContext.ftlog.info('map_cmd_servers = ', self.map_cmd_servers)
        TyContext.ftlog.info('map_cmd_srvtypes = ', self.map_cmd_srvtypes)

        TyContext.ftlog.info('creat map_room_servers map_game_servers ...')
        for room in self.rooms:
            roomId = room[CONF_ROOM_ID]
            serverId = room[CONF_ROOM_GAMESVR_ID]
            gameId = room[CONF_ROOM_GAME_ID]

            TyContext.ftlog.debug('room->', room)
            if isinstance(serverId, int):
                serverId = [serverId]
            for v in serverId:
                self._appendListItem2Map(self.map_room_servers, roomId, v)
                self._appendListItem2Map(self.map_game_servers, gameId, v)

            category = room[CONF_ROOM_DESC_DICT].get('category')
            if category == 'match' or category == 'bigmatch':
                if not gameId in self.map_gameid_matchs:
                    self.map_gameid_matchs[gameId] = {'roomIds': [], 'serverIds': [], 'servers': set()}
                matchs = self.map_gameid_matchs[gameId]
                matchs['roomIds'].append(roomId)
                matchs['serverIds'].append(serverId)
                for v in serverId:
                    matchs['servers'].add(v)

        TyContext.ftlog.info('map_gameid_matchs = ', self.map_gameid_matchs)
        TyContext.ftlog.info('map_room_servers = ', self.map_room_servers)
        TyContext.ftlog.info('map_game_servers = ', self.map_game_servers)

        self.redis_pool_mix__ = TyContext.RedisMix.__db__.__redisPool__
        TyContext.ftlog.info('redis.mix.id=', id(self.redis_pool_mix__))

        for i in xrange(len(TyContext.RedisUser.__dbs__)):
            rpool = TyContext.RedisUser.__dbs__[i].__redisPool__
            TyContext.ftlog.info('redis.cluster.id=', id(rpool))
            self.redis_cluster__[i] = rpool

        self.redis_cluster_len__ = len(self.redis_cluster__)
        self.__init_global_user_id__()

    def __init_global_user_id__(self):
        from tyframework.context import TyContext
        self.redis_fixhead_ = self.gameName + '.' + str(self.gameId) + '.'

        globalUserId = TyContext.RedisMix.execute('GET', 'global.userid')
        if globalUserId == None or int(globalUserId) < 10000:
            TyContext.RedisMix.execute('SET', 'global.userid', 10000)
        TyContext.ftlog.info('globalUserId = ', globalUserId)

    def _appendListItem2Map(self, datamap, itemKey, itemValue):
        values = None
        if datamap.has_key(itemKey):
            values = datamap[itemKey]
        else:
            values = []
            datamap[itemKey] = values
        if not (itemValue in values):
            values.append(itemValue)

    def updateConfig(self, tasklet):
        try:
            from freetime.games import gameClass
        except:
            return
        from tyframework.context import TyContext

        TyContext.ftlog.info('**** UPDATE CONFIGER !!!!! begin')
        TyContext.ftlog.info('updateConfig rooms...')
        rooms = TyContext.Configure.get_global_item_json('rooms', [])
        tlist = TyContext.Configure.get_global_item_json('table_config', [])

        self.rooms = rooms
        for room in self.rooms:
            TyContext.ftlog.info('updateConfig rooms...', room)
            self.map_roomid_room[room[0]] = room

        sortrooms = []
        for room in self.rooms:
            if 'minCoin' in room[CONF_ROOM_DESC_DICT]:
                sortrooms.append([room[CONF_ROOM_GAME_ID], room[CONF_ID], room[CONF_ROOM_DESC_DICT]['minCoin']])
            else:
                sortrooms.append([room[CONF_ROOM_GAME_ID], room[CONF_ID], room[CONF_ID]])

        sortrooms.sort(key=lambda x: x[2], reverse=True)
        for rooms in sortrooms:
            self._appendListItem2Map(self.map_gameid_roomids_sort, rooms[0], rooms[1])
        TyContext.ftlog.info('updateConfig map_gameid_roomids_sort=', self.map_gameid_roomids_sort)

        TyContext.ftlog.info('updateConfig table_config ...')
        for t in tlist:
            self.table_configs[t[CONF_ID]] = t
            TyContext.ftlog.info('load table_config ...', t)

        ptype = TyContext.TYGlobal.run_process_type()
        if ptype == TyContext.TYGlobal.RUN_TYPE_GAME:
            TyContext.ftlog.info('updateConfig call room reload')
            for roominfo in self.rooms:
                if roominfo[CONF_ROOM_GAMESVR_ID] == self.serverId:
                    TyContext.ftlog.info('updateConfig call room reload', roominfo)
                    roomid = roominfo[CONF_ROOM_ID]
                    room = self.maproom[roomid]
                    room.on_reload_conf(roominfo, self)

        from freetime.games import gameClass
        for _, game in gameClass.items():
            if isinstance(game, dict):
                gameins = game.get('game', None)
                if gameins:
                    try:
                        gameins.on_reload_conf()
                    except:
                        TyContext.ftlog.exception()

        TyContext.ftlog.info('**** UPDATE CONFIGER !!!!! done')

    def getServerIdByMsg(self, cmd):
        if self.map_cmd_servers.has_key(cmd):
            sids = self.map_cmd_servers[cmd]
            return sids
        return None

    def getServerIdByRoomId(self, roomId):
        if self.map_room_servers.has_key(roomId):
            return self.map_room_servers[roomId]
        return None

    def getServerIdByGameId(self, gameId):
        if self.map_game_servers.has_key(gameId):
            sids = self.map_game_servers[gameId]
            return sids
        return None

    def initVarDatas(self):
        pass
