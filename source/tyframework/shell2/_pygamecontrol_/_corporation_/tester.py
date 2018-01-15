# -*- coding: utf-8 -*-

def make_tester_default_setting(service):
    intrant = service['configuer.redis.host']
    portredis = service['configuer.redis.port']
    serverid = service['servers'][0]['id']
    mode = service['mode']
    if mode == 4 :
        httpsdk = 'http://192.168.10.16'
    else:
        if service.get('isnetwork42', 0) :
            httpsdk = 'http://42.62.53.180'
        else:
            httpsdk = 'http://125.39.218.101'

    return {
        'http.sdk' : httpsdk,
        'mysql' : {
            'beauty' : {'host' : intrant, 'port' : 3306, 'dbname' : 'beauty', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'advertise' : {'host' : intrant, 'port' : 3306, 'dbname' : 'ads', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata0'    : { 'host' : intrant, 'port' : 3306, 'dbname' : 'tydata0', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata1'    : { 'host' : intrant, 'port' : 3306, 'dbname' : 'tydata1', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata2'    : { 'host' : intrant, 'port' : 3306, 'dbname' : 'tydata2', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata3'    : { 'host' : intrant, 'port' : 3306, 'dbname' : 'tydata3', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata4'    : { 'host' : intrant, 'port' : 3306, 'dbname' : 'tydata4', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata5'    : { 'host' : intrant, 'port' : 3306, 'dbname' : 'tydata5', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata6'    : { 'host' : intrant, 'port' : 3306, 'dbname' : 'tydata6', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata7'    : { 'host' : intrant, 'port' : 3306, 'dbname' : 'tydata7', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
        },
        'redis' : {
                    'config'   : { 'host' : intrant, 'port' : portredis, 'dbid' : 0 },
                    'mix'      : { 'host' : intrant, 'port' : portredis, 'dbid' : 1 },
                    'friend'   : { 'host' : intrant, 'port' : portredis, 'dbid' : 2 },
                    'paydata'  : { 'host' : intrant, 'port' : portredis, 'dbid' : 3 },
                    'bicount'  : { 'host' : intrant, 'port' : portredis, 'dbid' : 4 },
                    'userkeys' : { 'host' : intrant, 'port' : portredis, 'dbid' : 5 },
                    'online'   : { 'host' : intrant, 'port' : portredis, 'dbid' : 6 },
                    'avatar'   : { 'host' : intrant, 'port' : portredis, 'dbid' : 9 },
                    'locker'   : { 'host' : intrant, 'port' : portredis, 'dbid' : 10 },
                    'tabledatas'   : [
                                 { 'useridmod' : 0, 'host' : intrant, 'port' : portredis, 'dbid' : 11 },
                                 { 'useridmod' : 1, 'host' : intrant, 'port' : portredis, 'dbid' : 12 },
                              ],
                    'datas' : [
                                 { 'useridmod' : 0, 'host' : intrant, 'port' : portredis, 'dbid' : 7 },
                                 { 'useridmod' : 1, 'host' : intrant, 'port' : portredis, 'dbid' : 8 },
                              ]
        },
        'bicollect.server' : {
            'chip_update' : {
                'master' : {'host' : '127.0.0.1', 'port' : 13000, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 23000, 'cluster' : 4},
                },
            'sdk_login' : {
                'master' : {'host' : '127.0.0.1', 'port' : 13010, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 23010, 'cluster' : 4},
                },
            'client_event' : {
                'master' : {'host' : '127.0.0.1', 'port' : 13020, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 23020, 'cluster' : 4},
                },
            'sdk_buy' : {
                'master' : {'host' : '127.0.0.1', 'port' : 3030, 'cluster' : 4},
#                 'slave'  : {'host' : '127.0.0.1', 'port' : 3030, 'cluster' : 4},
                },
            'game' : {
                'master' : {'host' : '127.0.0.1', 'port' : 13040, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 23040, 'cluster' : 4},
                },
            'card' : {
                'master' : {'host' : '127.0.0.1', 'port' : 13050, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 23050, 'cluster' : 4},
                }
        },
        'process' : [
              { 'type' : 'robot', 'id' : 0, 'server' : serverid},
              { 'type' : 'robot', 'id' : 1, 'server' : serverid},
              { 'type' : 'http', 'id' : 2, 'server' : serverid},
              { 'type' : 'conn', 'id' : 10, 'server' : serverid},
              { 'type' : 'conn', 'id' : 11, 'server' : serverid},
              { 'type' : 'entity', 'id' : 30, 'server' : serverid},
              { 'type' : 'account', 'id' : 50, 'server' : serverid},
              { 'type' : 'quick', 'id' : 98, 'server' : serverid},
              { 'type' : 'heart', 'id' : 99, 'server' : serverid},
              { 'type' : 'game', 'id' : 10000, 'server' : serverid},
           ]
    }
