# -*- coding=utf-8 -*-

###########################################################################
# 所有Context当中的成员的接口定义
# 所有的实现类必须具有构造函数
# 
###########################################################################

class GData:
    redis_fixhead_ = ''  # 某些REDIS键值的业务区分头
    redis_pool = None  # 现在已经废弃，为了代码兼容而保留
    redis_pool_config__ = None
    redis_pool_mix__ = None
    redis_cluster__ = {}
    redis_cluster_len__ = 0

    # Readonly DataBase Data
    servers = []

    rooms = []
    room_robots = []
    tables = []
    table_configs = {}

    # 整理后的静态数据
    map_type_servers = {}  # key=<typeId> value=<[serverId1, serverId2, ...]>
    map_cmd_servers = {}  # key=<command> value=<[serverId1, serverId2, ...]>
    map_cmd_srvtypes = {}  # key=<command> value=<[serverTyp1, serverTyp2, ...]>
    map_room_servers = {}  # key=<roomId> value=<[serverId1, serverId2, ...]>
    map_game_servers = {}  # key=<gameId> value=<[serverId1, serverId2, ...]>
    map_gameid_roomids = {}  # key=<gameId> value=<[roomId1, roomId2, ...]>
    map_gameid_roomids_sort = {}  # key=<gameId> value=<[roomId1, roomId2, ...]>
    map_roomid_room = {}  # key=<roomId> value=<[roomId, roomName, ...]>
    map_roomid_table_config = {}  # key=<roomId> value=<item of self.table_configs>
    map_gameid_matchs = {}
    isshutdown = False

    robotclientmap = {}  # kye=<ip:port> value=<UDP Client>
    clientmap = {}  # kye=<serverid> value=<UDP Client>
    usermap = {}  # key=<userId> value=<ConnUser|User>
    new_protocols = {}  # item=<ConnTCPSrvProtocol=ConnTCPSrvProtocol>
    maproom = {}  # key=<roomId> value=<Room>

    # 每个房间可以配置不同的玩法,麻将引入
    # 比如四川麻将使用（701，702，703，704）
    # 国标麻将使用（711，712，713，714）
    map_playmode_roomids = {}
