# -*- coding=utf-8 -*-
import os, base64, json

def to_string(obj):
    datas = []
    _makelines_(obj, datas, 1)
    strs = ''.join(datas)
    strs = strs.replace('\n', '\\n')
    strs = strs.replace('\d', '\\\\d')
    strs = strs.replace('\r', '')
    return strs

def _makelines_(obj, datas, flg=0):
    if isinstance(obj, unicode) :
        obj = obj.encode('utf-8')
        if flg :
            datas.append(obj)
        else:
            datas.append('"')
            datas.append(obj)
            datas.append('"')
    elif isinstance(obj, str) :
        if flg :
            datas.append(obj)
        else:
            datas.append('"')
            datas.append(obj)
            datas.append('"')
    elif isinstance(obj, (int , long, bool, float)):
        datas.append(str(obj))
    elif isinstance(obj, list)  :
        datas.append('[')
        i = 0
        for sobj in obj :
            if i > 0 :
                datas.append(', ')
            _makelines_(sobj, datas)
            i = 1
        datas.append(']')
    elif isinstance(obj, tuple) :
        datas.append('[')
        i = 0
        for sobj in obj :
            if i > 0 :
                datas.append(', ')
            _makelines_(sobj, datas)
            i = 1
        datas.append(']')
    elif isinstance(obj, dict) :
        datas.append('{')
        i = 0
        for k, v in obj.items() :
            if i > 0 :
                datas.append(', ')
            if isinstance(k, unicode) :
                k = k.encode('utf-8')
            else:
                k = str(k)
            datas.append('"')
            datas.append(k)
            datas.append('":')
            _makelines_(v, datas)
            i = 1
        datas.append('}')
    else :
        raise Exception

def decode_utf8_objs(datas):
    if isinstance(datas, dict) :
        ndatas = {}
        for key, val in datas.items() :
            if isinstance(key, unicode) :
                key = key.encode('utf-8')
            ndatas[key] = decode_utf8_objs(val)
        return ndatas
    if isinstance(datas, list) :
        ndatas = []
        for val in datas :
            ndatas.append(decode_utf8_objs(val))
        return ndatas
    if isinstance(datas, unicode) :
        return datas.encode('utf-8')
    return datas

def clone_object(objd):
    return decode_utf8_objs(json.loads(json.dumps(objd)))

def read_file(fpath, parsejson=False, needdecode=False):
    fp = open(fpath, 'r')
    if parsejson :
        datas = json.load(fp)
    else:
        datas = fp.read()
    if needdecode :
        datas = decode_utf8_objs(datas)
    fp.close()
    return datas

def write_file(fpath, content):
    if isinstance(content, (list, tuple, dict, set)) :
        content = json.dumps(content, sort_keys=True, indent=4, separators=(',', ':'))
    rfile = open(fpath, 'w')
    rfile.write(content)
    rfile.close()

service = None
outputs = None
outputsfile = None
SERVERIDS = None
ROOMS = None
ROOM_CHILDS = None
GAMES = None
ISSDK=0

def init_configure_env(issdk=0):
    global service, outputs, outputsfile, ISSDK
    ISSDK = issdk
    sfile = os.environ.get('CONFIGURE_SERVICE_FILE')
    service = read_file(sfile, True, True)

    outputsfile = os.environ.get('CONFIGURE_OUTPUTS_FILE')
    print 'outputsfile=', outputsfile
    outputs = read_file(outputsfile, True, True)
    
    if not 'configuredatas' in outputs :
        outputs['configuredatas'] = {}

    if not 'cmdkeys' in outputs :
        outputs['cmdkeys'] = {}
    
    if not 'ROOMS' in outputs :
        outputs['ROOMS'] = {}
    
    if not 'ROOM_CHILDS' in outputs :
        outputs['ROOM_CHILDS'] = {}

    if not 'GAMES' in outputs :
        outputs['GAMES'] = {}
    
    if not 'SERVERIDS' in outputs :
        outputs['SERVERIDS'] = {}
    
    global SERVERIDS, ROOMS, ROOM_CHILDS, GAMES
    SERVERIDS = outputs['SERVERIDS']
    ROOMS = outputs['ROOMS']
    ROOM_CHILDS = outputs['ROOM_CHILDS']
    GAMES = outputs['GAMES']

def finish_configure_env():
    global outputs, outputsfile
    write_file(outputsfile, outputs)

def get_service():
    return service

def db_command(rkey, data):
    outputs['configuredatas'][rkey] = clone_object(data)

def db_rpush(rkey, data):
    rkey = 'configitems:global:'  + rkey
    outputs['cmdkeys'][rkey] = 1
    if rkey in outputs['configuredatas'] :
        vlist = outputs['configuredatas'][rkey]
        vlist.append(data)
    else:
        vlist = [data]
    outputs['configuredatas'][rkey] = clone_object(vlist)

def db_set(rkey, data):
    if rkey in outputs['cmdkeys'] :
        if data != outputs['configuredatas'][rkey] :
            print ISSDK, 'the new value is->', data
            print ISSDK, 'the old value is->', outputs['configuredatas'][rkey]
            if not ISSDK :
                raise Exception('the key already exits !' + rkey)
    outputs['cmdkeys'][rkey] = 1
    outputs['configuredatas'][rkey] = clone_object(data)

def add_global_item(key, data):
    db_set('configitems:global:' + str(key), data)

def add_game_item(key, data):
    db_set('configitems:game:%d:%s' % (service['id'], key), data)

def add_game_item_old(gameId, key, data):
    db_set('configitems:game:%s:%s' % (str(gameId), key), data)

def add_room_item(gameId, roomId, key, data):
    db_set('configitems:room:%d:%d:%s' % (gameId, roomId, key), data)

def add_client_item(key, clientId, templateid):
    db_set('configitems:gameclient:%d:%s:%s' % (service['id'], key, clientId), templateid)

def del_client_item_old(gameId, key, clientId):
    db_set('configitems:gameclient:%s:%s:%s' % (str(gameId), key, clientId))

def add_client_item_old(gameId, key, clientId, templateid):
    db_set('configitems:gameclient:%s:%s:%s' % (str(gameId), key, clientId), templateid)

def add_template_item(templateid, datas):
    db_set('configitems:template:%s' % (str(templateid)), datas)

def add_server_type(typeId, typeName, cmds):
    db_rpush('server_type', [typeId, typeName, cmds])

def _find_server_def_by_id_(sid):
    serverlist = service['servers']
    for x in xrange(len(serverlist)) :
        if serverlist[x]['id'] == sid :
            return serverlist[x]
    return None

def _find_process_def_by_type_(stype):
    plist = []
    plistids = []
    processlist = service['process']
    for x in xrange(len(processlist)) :
        if processlist[x]['type'] == stype :
            plist.append(processlist[x])
            plistids.append(processlist[x]['id'])
    return plistids, plist

def _get_type_id_by_name_(stype):
    datas = { 'conn' :1, 'account' : 2, 'entity': 3, 'game' : 4,
          'quick' : 5, 'heart' : 6, 'robot' :-1, 'http' :-2}
    return datas[stype]

def add_servers():
    processlist = service['process']
    for x in xrange(len(processlist)) :
        proc = processlist[x]
        serverId = proc['id']
        SERVERIDS[serverId] = 1
        typeId = _get_type_id_by_name_(proc['type'])
        srvdef = _find_server_def_by_id_(proc['server'])
        if 'ssl' in proc :
            tcp = proc['ssl']
            tcptype = 1
        elif 'tcp' in proc :
            tcp = proc['tcp']
            tcptype = 2
        elif 'http' in proc :
            tcp = proc['http']
            tcptype = 3
        else:
            tcp = 0
            tcptype = 0
        udp = 0
        if 'udp' in proc :
            udp = proc['udp']

        data = [serverId, typeId, srvdef['internet'], tcp, srvdef['intrant'], udp, tcptype]
        db_rpush('servers', data)

def add_room(roomId, serverIds, roomName, desc, ismajiang=False, gameId=-1):
    
    plistids, plist = _find_process_def_by_type_('game')
    if not serverIds[0] in plistids :
        serverIds[0] = int(plistids[0])

    global ROOMS, ROOM_CHILDS
    if gameId == -1 :
        gameId = service['id']
    maxUser = 10000000
    picUrl = ''
    picMd5 = ''
    isMatch = 0
    if 'category' in desc and desc['category'] == 'match' :
        isMatch = 1
    if isMatch :
        desc['matchId'] = roomId
    else:
        desc['matchId'] = 0
    datas = [roomId, roomName, serverIds[0], gameId, maxUser, picUrl, picMd5, desc]
    ROOMS[roomId] = desc
    
    if ismajiang :  # 麻将特殊处理
        if service['mode'] != 1 :
            serverIds = [serverIds[0]]
        datas = [roomId, roomName, serverIds, gameId, maxUser, picUrl, picMd5, desc]
        db_rpush('rooms', datas)
        ROOM_CHILDS[roomId] = []
        return

    db_rpush('rooms', datas)
    ROOM_CHILDS[roomId] = []
    if service['mode'] == 1 :
        for x in xrange(1, len(serverIds)) :
            serverId = serverIds[x]
            childRoomId = serverId
            ROOM_CHILDS[roomId].append(childRoomId)
            desc['parentRoom'] = roomId
            if isMatch :
                desc['matchId'] = childRoomId
            else:
                desc['matchId'] = 0
            datas = [childRoomId, roomName, serverId, gameId, maxUser, picUrl, picMd5, desc]
            db_rpush('rooms', datas)

def add_table_config(configId, configList):
    datas = [configId]
    datas.extend(configList)
    db_rpush('table_config', datas)

def add_table(roomId, tableConfigId, count, serverIds=[]):
    if service['mode'] in (2, 3) :
        # 测试、审核服自动消减桌子数量和房间配置
        if count > 100 :
            count = min(15, count)
        serverIds = []

    data = [count, "", roomId, "", 0, tableConfigId]
    db_rpush ('tables', data)
    if serverIds :
        for x  in xrange(1, len(serverIds)) :
            childRoomId = serverIds[x]
            data = [count, "", childRoomId, "", 0, tableConfigId]
            db_rpush ('tables', data)

def append_chid_room_dict(datas):
    global ROOM_CHILDS
    for roomid in datas.keys() :
        childs = []
        if int(roomid) in ROOM_CHILDS :
            childs = ROOM_CHILDS[int(roomid)]
        for childid in childs :
            value = datas[roomid]
            if isinstance(roomid, (str, unicode)) :
                childid = str(childid)
            datas[childid] = value
    return datas

def _find_process_by_robot_id_(robotid):
    host, port = None, None
    process = None
    processlist = service['process']
    for x in xrange(len(processlist)) :
        if processlist[x]['type'] == 'robot' and processlist[x]['id'] == robotid:
            process = processlist[x]
            port = process['udp']
            break
    if not process :
        return host, port
    server = process['server']
    serverlist = service['servers']
    for x in xrange(len(serverlist)) :
        if serverlist[x]['id'] == server :
            host = serverlist[x]['intrant']
            break
    return host, port

def add_robot(robotId, *roomids):
    global ROOMS, ROOM_CHILDS
    for roomId in roomids :
        if roomId in ROOMS :
            host, port = _find_process_by_robot_id_(robotId)
            if host and port :
                rids = [roomId]
                rids.extend(ROOM_CHILDS[roomId])
                db_rpush('room_robots', [host, port, rids])

def build_pic_url(picName, gameId):
    return '%s/%d/%s' % (service['http.download'], gameId, picName)

def get_http_download():
    return service['http.download']

def get_http_game():
    return service['http.game']

def format_xml(xmlstr):
    xmls = xmlstr.split('\n')
    for x in xrange(len(xmls)) :
        xmls[x] = xmls[x].strip('\r\n ')
        if xmls[x][0:4] == '<!--' and xmls[x][-3:] == '-->':
            xmls[x] = ''
    xmlstr = ''.join(xmls)
    return xmlstr

def make_client_action(module, action, params=None, isb64=True):
    if params :
        data = {"module":module, "cmd":{"action":action, "params":params}}
    else:
        data = {"module":module, "cmd":{"action":action}}
    data = to_string(data)
    if isb64 :
        data = base64.b64encode(data)
    return data

def get_act_show_room(index):
    return make_client_action('rooms', 'ShowRoomList', {"index":index}, True)

def get_act_quit():
    return make_client_action('common', 'Quit', None, True)

def get_act_close_wnd():
    return make_client_action('common', 'CloseWindow', None, True)

def get_act_open_wnd(wnd, index=0, args=""):
    return make_client_action('common', 'OpenWindow',
                           {'style' : 0,
                            'title' : '',
                            'wnd':wnd,
                            'index':index,
                            "args": args,
                            }, True)

def get_act_open_activity(index=0, args="tab_=13.html"):
    return get_act_open_wnd('activity', index, args) 

def get_act_open_shop(index=0, args=""):
    return get_act_open_wnd('shop', index, args) 
