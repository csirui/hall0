# -*- coding: utf-8 -*-

def make_default_setting(service):
    intrant = service['configuer.redis.host']
    portredis = service['configuer.redis.port']
    dbidredis = service['configuer.redis.dbid']
    return {
        'http.sdk' : 'http://123.206.34.124',
        'mysql' : {
            'beauty' : {'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'beauty', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'advertise' : {'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'ads', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
#             'tyuser'     : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tyuser', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata0'    : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tydata0', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata1'    : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tydata1', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata2'    : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tydata2', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata3'    : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tydata3', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata4'    : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tydata4', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata5'    : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tydata5', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata6'    : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tydata6', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
            'tydata7'    : { 'host' : '10.141.87.65', 'port' : 3306, 'dbname' : 'tydata7', 'user' : 'tuyoogame', 'pwd' : 'tuyoogame' },
        },
        'redis' : {
                    'config'   : { 'host' : intrant, 'port' : portredis, 'dbid' : dbidredis },
                    'mix'      : { 'host' : '10.141.87.65', 'port' : 6507, 'dbid' : 0 },
                    'friend'   : { 'host' : '10.141.87.65', 'port' : 6503, 'dbid' : 0 },
                    'paydata'  : { 'host' : '10.141.87.65', 'port' : 6509, 'dbid' : 0 },
                    'bicount'  : { 'host' : '10.141.87.65', 'port' : 6502, 'dbid' : 0 },
                    'userkeys' : { 'host' : '10.141.87.65', 'port' : 6505, 'dbid' : 0 },
                    'onlinegeo': { 'host' : '10.141.87.65', 'port' : 6504, 'dbid' : 0 },
                    'avatar'   : { 'host' : '10.141.87.65', 'port' : 6501, 'dbid' : 0 },
                    'locker'   : { 'host' : '10.141.87.65', 'port' : 6506, 'dbid' : 0 },
#                     'tabledatas'   : [
#                                  { 'useridmod' : 0, 'host' : '10.141.87.65', 'port' : 6410, 'dbid' : 0 },
#                                  { 'useridmod' : 1, 'host' : '10.141.87.65', 'port' : 6411, 'dbid' : 0 },
#                               ],
                    'online' : [
                                 { 'useridmod' : 0, 'host' : '10.141.87.65', 'port' : 6508, 'dbid' : 0 }
                              ],
                    'datas' : [
                                 { 'useridmod' : 0, 'host' : '10.141.87.65', 'port' : 6380, 'dbid' : 0 },
                                 { 'useridmod' : 1, 'host' : '10.141.87.65', 'port' : 6381, 'dbid' : 0 },
                                 { 'useridmod' : 2, 'host' : '10.141.87.65', 'port' : 6382, 'dbid' : 0 },
                                 { 'useridmod' : 3, 'host' : '10.141.87.65', 'port' : 6383, 'dbid' : 0 },
                                 { 'useridmod' : 4, 'host' : '10.141.87.65', 'port' : 6384, 'dbid' : 0 },
                                 { 'useridmod' : 5, 'host' : '10.141.87.65', 'port' : 6385, 'dbid' : 0 },
                                 { 'useridmod' : 6, 'host' : '10.141.87.65', 'port' : 6386, 'dbid' : 0 },
                                 { 'useridmod' : 7, 'host' : '10.141.87.65', 'port' : 6387, 'dbid' : 0 },
                              ]
        },
        'bicollect.server' : {
            'chip_update' : {
                'master' : {'host' : '127.0.0.1', 'port' : 3000, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 3000, 'cluster' : 4},
                },
            'sdk_login' : {
                'master' : {'host' : '127.0.0.1', 'port' : 3010, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 3010, 'cluster' : 4},
                },
            'client_event' : {
                'master' : {'host' : '127.0.0.1', 'port' : 3020, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 3020, 'cluster' : 4},
                },
            'sdk_buy' : {
                'master' : {'host' : '127.0.0.1', 'port' : 3030, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 3030, 'cluster' : 4},
                },
            'game' : {
                'master' : {'host' : '127.0.0.1', 'port' : 3040, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 3040, 'cluster' : 4},
                },
            'card' : {
                'master' : {'host' : '127.0.0.1', 'port' : 3050, 'cluster' : 4},
                'slave'  : {'host' : '127.0.0.1', 'port' : 3050, 'cluster' : 4},
                }
         },
    }
