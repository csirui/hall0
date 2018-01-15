# -*- coding: utf-8 -*-

from _main_helper_ import myfiles, mylog, myhelper

def action_load_service(params):
    '''
    装载并检测服务启动配置文件
    '''
    # 取得当前文件的路径，添加到PYTHONPATH当中
    servicefile = myfiles.normpath(params['servicefile'])
    mylog.log('装载配置文件 :', servicefile)
    service = myfiles.read_json_file(servicefile, True)

    if not __check_basic_info__(params, service, servicefile) :
        return 0
    
    if not __check_projects_paths__(params, service) :
        return 0

    if not __check_configure_for_servers__(params, service) :
        return 0

    if not __check_configure_default_value__(params, service) :
        return 0
    
    if not __check_configure_for_process__(service) :
        return 0

    if not __check_service_url__(service, 'http.game') :
        return 0

    if not __check_service_url__(service, 'http.download') :
        return 0

    if not __check_service_url__(service, 'http.sdk') :
        return 0

    encodepyc = service.get('encodepyc')
    if not encodepyc in (0, 1):
        return mylog.error('配置文件 : encodepyc 是否使用加密pyc错误，0或1')
    
    # pypy = service.get('pypy')
    # if not isinstance(pypy, str) :
    #     return mylog.error('配置文件 : pypy命令执行值错误')
    # if pypy[0] != '/' :
    #     pypy = '/bin/' + pypy
    # if not myfiles.file_exists(pypy) :
    #     return mylog.error('配置文件 : pypy可执行命令丢失 ' + pypy)

    params['service'] = service
    __print_service_content__(params)
    return 1

def __check_service_url__(service , ukey):
    http = service[ukey]
    if not isinstance(http, str) or  http.find('http://') != 0 or http[-1] == '/' :
        return mylog.error('配置文件 : ' + ukey + '必须以http开头，不能以/结尾')
    return 1

def __check_basic_info__(params, service, servicefile):
    if not isinstance(service, dict) :
        return mylog.error('配置文件 : 格式错误，必须为dict')

    gameId = service.get('id')
    if not isinstance(gameId, int) or gameId <= 0 or gameId >= 10000 :
        return mylog.error('配置文件 : id值错误')

    gameName = service.get('name')
    if not isinstance(gameName, (str, unicode)) or len(gameName) <= 0 :
        return mylog.error('配置文件 : name值错误')
    if gameName.find('-') >= 0 :
        return mylog.error('配置文件 : name值错误,不能包含字符"-"')

    mode = service.get('mode')
    if mode not in (1, 2, 3, 4) :
        return mylog.error('配置文件 : mode值错误,一定是数字 1,2,3,4')

    simulation = service.get('simulation', 0)
    if simulation not in (0, 1) :
        return mylog.error('配置文件 : simulation值错误,一定是数字 0,1')
    service['simulation'] = simulation

    tcpbridge = service.get('newtcpbridge', '')
    if tcpbridge :
        if not __check_service_url__(service, 'newtcpbridge') :
            return 0
    service['newtcpbridge'] = tcpbridge

    if servicefile[0] != '/' :
        servicefile = myfiles.get_pwd() + '/' + servicefile
    
    servicefile = myfiles.abspath(servicefile)
    service['_servicefile_'] = servicefile
    return 1

def __check_projects_paths__(params, service):
    servicefile_path = myfiles.get_parent_dir(service['_servicefile_'])
    
    projects = service.get('projects')
    if not isinstance(projects, list) :
        return mylog.error('配置文件 : 格式错误，projects必须为list')

    for project in projects :
        if not isinstance(project, dict) :
            return mylog.error('配置文件 : 格式错误，projects的每一项必须为dict')
        projectpath = project.get('path')
        if not projectpath or not isinstance(projectpath, (str, unicode)) :
            return mylog.error('配置文件 : 格式错误，projects的path必须定义为字符串')
        projectpath = projectpath.strip()
        if projectpath[0] != '/' :
            projectpath = servicefile_path + '/' + projectpath
        projectpath = myfiles.abspath(projectpath)
        if not myfiles.dir_exists(projectpath) :
            mylog.error('配置文件 : 工程路径不存在' , projectpath)
            return mylog.error('工程路径需为 相对与配置文件的相对路径 或 绝对路径')
        project['path'] = projectpath

        configure_py = project.get('configure_py', None)
        if configure_py and not isinstance(configure_py, (str, unicode)) :
            return mylog.error('配置文件 : 格式错误，projects的configure_py配置指向必须定义为字符串')

        if not configure_py :
            configure_py = projectpath + '/configure/game/_default_.py'
        if configure_py[0] != '/' :
            configure_py = servicefile_path + '/' + configure_py
        
        if not myfiles.file_exists(configure_py) :
            mylog.error('配置文件 : 游戏配置py文件不存在' , configure_py)
            return mylog.error('游戏配置py文件需为 相对与配置文件的相对路径 或 绝对路径 或 缺省使用工程目录下/configure/game/_default_.py')
        project['configure_py'] = myfiles.abspath(configure_py)

        configure_json = project.get('configure_json', None)
        if configure_json and not isinstance(configure_json, (str, unicode)) :
            return mylog.error('配置文件 : 格式错误，projects的configure_json配置指向必须定义为字符串')

        if not configure_json :
            configure_json = projectpath + '/configure_json/configurescripts/_default_.py'
        if configure_json[0] != '/' :
            configure_json = servicefile_path + '/' + configure_json
        
        if not myfiles.file_exists(configure_json) :
            mylog.error('配置文件 : 游戏配置json文件不存在' , configure_json)
            return mylog.error('游戏配置json文件需为 相对与配置文件的相对路径 或 绝对路径 或 缺省使用工程目录下/configure_json/configurescripts/_default_.py')
        project['configure_json'] = myfiles.abspath(configure_json)

    return 1

def __check_configure_default_value__(params, service):

    srv0 = service['servers'][0]
    internet = srv0['internet']
    intrant = srv0.get('intrant', internet) 

    redis_host = service.get('redis.host', intrant)
    redis_port = int(service.get('redis.port', 6379))
    redis_dbid = int(service.get('redis.dbid', 0))

    service['configuer.redis.host'] = redis_host
    service['configuer.redis.port'] = redis_port
    service['configuer.redis.dbid'] = redis_dbid

    if not 'corporation' in service:
        service['corporation'] = 'tuyoo'

    corporation = service['corporation']
    corporationdefault = None
    mylog.log('当前定义的公司为 :', corporation)
    try:
        make_default_setting = None
        exec('from _corporation_.%s import make_default_setting' % (corporation))
        corporationdefault = make_default_setting(service)
    except:
        return mylog.error('配置文件 : servers中公司的定义不在控制范围内 ' + corporation)
    
    from _corporation_.tester import make_tester_default_setting
    testerdefault = make_tester_default_setting(service)
    
    mode = service['mode']    
    if mode in (1, 2) and not 'redis.fixhead' in service:
        service['redis.fixhead'] = service['name'] + '.'
    
    if 'redis.fixhead' in service :
        if service['redis.fixhead'][-1] != '.' :
            service['redis.fixhead'] = service['redis.fixhead'] + '.'
 
    if not 'encodepyc' in service:
        service['encodepyc'] = 0

    if len(str(service.get('pypy', ''))) <= 0: 
        if not service['encodepyc'] :
            service['pypy'] = 'pypy'
        else:
            service['pypy'] = 'pypy-enc'

    if not 'mysql' in service :
        if mode in (1, 2) :
            service['mysql'] = corporationdefault['mysql']
        else:
            service['mysql'] = testerdefault['mysql']

    if not 'redis' in service:
        if mode in (1, 2) :
            service['redis'] = corporationdefault['redis']
        else:
            service['redis' ] = testerdefault['redis']

    root_path = params['__source_path__']
    service['paths'] = {
            'bin'  : myfiles.normpath(root_path + '/../bin'),
            'log' : myfiles.normpath(root_path + '/../logs'),
            'bireport' : myfiles.normpath(root_path + '/../bireport'),
            'script' : myfiles.normpath(root_path + '/../script'),
            'webroot' : myfiles.normpath(root_path + '/../webroot'),
            'backup' : myfiles.normpath(root_path + '/../backup'),
            'hotfix' : myfiles.normpath(root_path + '/../hotfix'),
    }

    if service.get('sharelog', 0) :
        service['paths']['log'] = '/home/share/logs_' + str(service['id'])
        service['paths']['bireport'] = '/home/share/bireport_' + str(service['id'])

    if not 'process' in service :
        service['process'] = testerdefault['process']

    httpport = service.get('http.port', redis_port + 2)
    firsthttpproc = None
    httpcount = 0
    process = service['process']
    for proc in process :
        if proc['type'] == 'http' :
            if proc.get('http', 0) <= 0 :
                proc['http'] = httpport
                httpport += 1
                httpcount += 1
            if firsthttpproc == None:
                firsthttpproc = proc
    
    connport = service.get('tcp.port', httpport)
    for proc in process :
        if proc['type'] == 'conn' :
            if proc['id'] == 10 :  # 机器人接入,机器人服务修改后，需要去掉此处特殊处理
                proc['ssl'] = connport
            else:
                proc['tcp'] = connport
            connport += 1

    udpport = service.get('udp.port', connport)
    if udpport % 2 != 0 :  # UDP端口，偶数为接收，奇数为发送
        udpport += 1
    for proc in process :
        proc['udp'] = udpport
        udpport += 2

    if not 'config' in service :
        service['config'] = 'game/default.py'

    if not firsthttpproc :
        return mylog.error('配置文件 : 必须定义至少一个HTTP进程')

    http_srv = None
    for srv in service['servers'] :
        if srv['id'] == firsthttpproc['server'] :
            http_srv = srv
            break
    http_internet = http_srv['internet']
    http_port = firsthttpproc['http']

    if not 'http.game' in service :
        if mode == 1:
            service['http.game'] = 'http://%s' % (http_internet)
        else:
            if httpcount == 1 :
                service['http.game'] = 'http://%s:%d' % (http_internet, http_port)
            else:
                service['http.game'] = 'http://%s' % (http_internet)

    if not 'http.download' in service :
        if mode == 1:
            service['http.download'] = 'http://%s' % (http_internet)
        else:
            if httpcount == 1 :
                service['http.download'] = 'http://%s:%d' % (http_internet, http_port)
            else:
                service['http.download'] = 'http://%s' % (http_internet)

    if not 'http.sdk' in service :
        if mode in (1, 2):
            service['http.sdk'] = corporationdefault['http.sdk']
        else:
            service['http.sdk'] = service['http.game']

    rconf = service['redis']['config']
    service['prockey'] = '%s:%d:%d:' % (rconf['host'], rconf['port'], rconf['dbid'])

    hook_process = service.get('hook', service['mode'] in (1, 2))
    if hook_process :
        hook_process = 'hook'
    else:
        hook_process = 'nohook'
    service['hook'] = hook_process


    if not 'bicollect.server' in service :
        if mode in (1, 2):
            service['bicollect.server'] = corporationdefault['bicollect.server']
        else:
            service['bicollect.server'] = testerdefault['bicollect.server']

    return 1

def __check_configure_for_servers__(params, service):
    ids = {}
    internets = {}
    intrants = {}

    if not 'servers' in service :
        return mylog.error('配置文件 : 必须定义servers')

    servers = service['servers']
    if not isinstance(servers, list) or len(servers) <= 0 :
        return mylog.error('配置文件 : servers定义为空或非数组')

    for x in xrange(len(servers)) :
        server = servers[x]

        if 'internet' not in server :
            return mylog.error('配置文件 : servers[' , x, ']的对外定义internet丢失')
        
        if server['internet'] not in internets :
            internets[server['internet']] = 1
        else:
            return mylog.error('配置文件 : servers[', x, ']的internet [' , server['internet'], '] 重复')

        if 'intrant' not in server :
            server['intrant'] = server['internet']

        if server['intrant'] not in intrants :
            intrants[server['intrant']] = 1
        else:
            return mylog.error('配置文件 : servers[', x, ']的intrant [' , server['intrant'] , '] 重复')

        if 'id' not in server :
            return mylog.error('配置文件 : servers[', x, ']的id丢失')
        if server['id'] not in ids :
            ids[server['id']] = 1
        else:
            return mylog.error('配置文件 : servers[', x, ']的id [' , server['id'] , '] 重复')

        server['user'] = myhelper.whoami()
        
        if 'pwd' not in server :
            server['pwd'] = ''
        if not 'port' in server:
            server['port'] = 22
        if not 'cpucount' in server:
            server['cpucount'] = 0
        
        if not isinstance(server['port'], int) or server['port'] < 0 :
            return mylog.error('配置文件 : servers[', x, ']的SSH登录端口不正确')

        if not isinstance(server['cpucount'], int) or server['cpucount'] < 0 :
            return mylog.error('配置文件 : servers[', x, ']的CUP数量定义不正确')

        if not isinstance(server['user'], (str, unicode)) :
            return mylog.error('配置文件 : servers[', x, ']的登陆用户名定义不正确')

        if not isinstance(server['pwd'], (str, unicode)) :
            return mylog.error('配置文件 : servers[', x, ']的登陆密码定义不正确')

        if not isinstance(server['id'], (str, unicode)) :
            return mylog.error('配置文件 : servers[', x, ']的服务器ID定义不正确')

        if not isinstance(server['intrant'], (str, unicode)) :
            return mylog.error('配置文件 : servers[', x, ']的内网地址定义不正确')

        if not isinstance(server['internet'], (str, unicode)) :
            return mylog.error('配置文件 : servers[', x, ']的对外地址定义不正确')

        islocalhost0 = myhelper.is_local_ip(server['internet'])
        islocalhost1 = myhelper.is_local_ip(server['intrant'])
        
        if islocalhost0 or islocalhost1 :
            server['sshhost'] = server['intrant']
            server['localhost'] = 1
        else:
            if myhelper.check_ssh_port(server['intrant'], server['port']) :
                server['sshhost'] = server['intrant']
            else:
                if myhelper.check_ssh_port(server['internet'], server['port']) :
                    server['sshhost'] = server['internet']
                else:
                    return mylog.error('配置文件 : servers[', x, ']SSH端口检测失败')
        mylog.log('检查服务器SSH : %02d/%02d %-16s %s' % (x, len(servers), server['id'], server['sshhost']))
        
    return 1

def __check_configure_for_process__(service):
    srvmap = {}
    servers = service['servers']
    for x in xrange(len(servers)) :
        srv = servers[x]
        srvmap[srv['id']] = srv
        srv['proccount'] = 0

    ids = {}
    ports = {}
    if 'process' not in service or len(service['process']) == 0 :
        return mylog.error('配置文件 : process定义丢失')
    
    http_count = 0
    process = service['process']
    for x in xrange(len(process)) :
        proc = process[x]
        uhead = '配置文件 : process[', x, ']'
        if 'type' not in proc :
            return mylog.error(uhead + '的type丢失')
        if 'id' not in proc :
            return mylog.error(uhead + '的id丢失')
        if 'server' not in proc :
            return mylog.error(uhead + '的server丢失')
        
        ptype = proc['type']
        if ptype not in ('robot', 'http', 'conn', 'entity', 'account', 'quick', 'heart', 'game') :
            return mylog.error(uhead + ' process type' + proc['type'] + '定义错误')
        
        uhead = '配置文件:process[' + str(x) + '][' + str(ptype) + '][' + str(proc['id']) + ']'

        pid = proc['id']
        if not isinstance(pid, int) or pid < 0:
            return mylog.error(uhead + ' process id ', proc['id'], '为非正整数')
        if pid in ids :
            return mylog.error(uhead + ' process id ', proc['id'], '重复定义')
        ids[pid] = [pid]
        
        if proc['server'] not in srvmap :
            return mylog.error(uhead + '的server值[' + proc['server'] + ']未在servers当中定义')
        else:
            proc['internet'] = srvmap[proc['server']]['internet']
            proc['intrant'] = srvmap[proc['server']]['intrant']
            srvmap[proc['server']]['proccount'] += 1

        if 'udp' not in proc :
            return mylog.error(uhead + '的udp丢失')
        udp = proc['udp']

        if ptype in ('http') :
            http_count += 1

            if 'http' not in proc :
                return mylog.error(uhead + '的http端口定义丢失')
            if not isinstance(proc['http'], int) or proc['http'] <= 0:
                return mylog.error(uhead + ' http端口为非大于零的整形数字')

            if proc['http'] not in ports :
                ports[proc['http']] = proc['http']
            else:
                return mylog.error(uhead + ' http端口已经被使用')

        if ptype in ('conn') :
            if not 'ssl' in proc and not 'tcp' in proc:
                return mylog.error(uhead + ' 必须定义ssl或tcp端口')
            if 'ssl' in proc and 'tcp' in proc:
                return mylog.error(uhead + ' ssl或tcp端口只能定义一个')

            if 'ssl' in proc :
                if not isinstance(proc['ssl'], int) or proc['ssl'] <= 0:
                    return mylog.error(uhead + ' ssl端口为非大于零的整形数字')
                if proc['ssl'] not in ports :
                    ports[proc['ssl']] = proc['ssl']
                else:
                    return mylog.error(uhead + ' ssl端口已经被使用')

            if 'tcp' in proc :
                if not isinstance(proc['tcp'], int) or proc['tcp'] <= 0:
                    return mylog.error(uhead + ' tcp端口为非大于零的整形数字')
    
                if proc['tcp'] not in ports :
                    ports[proc['tcp']] = proc['tcp']
                else:
                    return mylog.error(uhead + ' tcp端口已经被使用')

        if udp != None :
            if not isinstance(udp, int) or udp <= 0:
                return mylog.error(uhead , ' udp端口为非大于零的整形数字 udp=', udp)
            if udp % 2 != 0 :
                return mylog.error(uhead , ' udp端口必须为偶数 udp=', udp)
            if udp not in ports :
                ports[udp] = udp
            else:
                return mylog.error(uhead, ' udp端口已经被使用udp=', udp)
            
    return 1

def __print_service_content__(params):
    service = params['service']
    mylog.log('================================================================================')
    mylog.log('Service Configer :', params['servicefile'])
    mylog.log('Python Exec      :', service['pypy'])
    mylog.log('--------------------------------------------------------------------------------')
    mylog.log('Run Mode         :', service['mode'])
    mylog.log('Simulation       :', service['simulation'])
    mylog.log('Game Name        :', service['name'])
    mylog.log('Bin Path         :', service['paths']['bin'])
    mylog.log('Log Path         :', service['paths']['log'])
    mylog.log('BiReport Path    :', service['paths']['bireport'])
    mylog.log('WebRoot Path     :', service['paths']['webroot'])
    mylog.log('Script Path      :', service['paths']['script'])
    mylog.log('Http Game        :', service['http.game'])
    mylog.log('Http Download    :', service['http.download'])
    mylog.log('Http SDK         :', service['http.sdk'])

    mylog.log('--------------------------------------------------------------------------------')
    bireports = service.get('bireport.server', None)
    if bireports :
        for k, v in bireports.items() :
            mylog.log('BiReport         : ', k, '->', v)
    else:
        mylog.log('BiReport         : Use Log File')

    mylog.log('--------------------------------------------------------------------------------')
    projects = service.get('projects')
    for x in xrange(len(projects)):
        proj = projects[x]
        mylog.log('Project Path           : %s' % (proj['path']))
        mylog.log('Project Configure PY   : %s' % (proj['configure_py']))
        mylog.log('Project Configure JSON : %s' % (proj['configure_json']))
        mylog.log('--------------------------------------------------------------------------------')

    mkeys = service['mysql'].keys()
    mkeys.sort()
    for dbalias in mkeys :
        mysql = service['mysql'][dbalias]
        slen = '%s@%s:%d/%s' % (mysql['user'], mysql['host'], mysql['port'], mysql['dbname'])
        mylog.log('MySql For %-10s :' % (dbalias), slen)

    mylog.log('--------------------------------------------------------------------------------')
    mkeys = service['redis'].keys()
    mkeys.sort()
    for dbalias in mkeys :
        rd = service['redis'][dbalias]
        if isinstance(rd, dict):
            slen = '%s:%d:%d' % (rd['host'], rd['port'], rd['dbid'])
            mylog.log('Redis For %-14s :' % (dbalias), slen)

    mylog.log('--------------------------------------------------------------------------------')
    for dbalias in mkeys :
        rdatas = service['redis'][dbalias]
        if isinstance(rdatas, list):
            for x in xrange(len(rdatas)) :
                rd = rdatas[x]
                slen = '%s:%d:%d  %d' % (rd['host'], rd['port'], rd['dbid'], rd['useridmod'])
                mylog.log('Redis For %-14s %d/%d  :' % (dbalias, x, len(rdatas)), slen)

    mylog.log('--------------------------------------------------------------------------------')
    mylog.log('Servers  N/C  : PC :        INTERNET :         INTRANT :             SSH : ID ')
    servers = service['servers']
    for x in xrange(len(servers)) :
        slen = '%02d : %15s : %15s : %15s : %s' % (servers[x]['proccount'], servers[x]['internet'], servers[x]['intrant'], servers[x]['sshhost'], servers[x]['id'])
        mylog.log('Servers %02d/%02d :' % (x, len(servers)), slen)
    
    mylog.log('--------------------------------------------------------------------------------')
    mylog.log('Process   N/C    :   UDP :   TCP :   HTTP :    ID :     TYPE : SERVER')
    process = service['process']
    for x in xrange(len(process)) :
        proc = process[x]
        udp = 0
        if 'udp' in proc :
            udp = proc['udp']
        tcp = 0
        if 'tcp' in proc :
            tcp = proc['tcp']
        if 'ssl' in proc :
            tcp = proc['ssl']
        http = 0
        if 'http' in proc :
            http = proc['http']

        slen = '%5d : %5d : %5d : %5d : %8s : %s' % (udp, tcp, http, proc['id'], proc['type'], proc['server'])
        
        mylog.log('Process %03d/%03d  :' % (x, len(process)), slen)

    mylog.log('================================================================================')
