#-*- coding=utf-8 -*-
'''
初始化paytype数据
支付方式：tuyooios
针对版本：AppStore上的IOS版本

注意：
   所有商品都以人民币定价
'''
import os
import sys
import redis

host = '127.0.0.1'
port = '6379'
db = '1'

#redis_cli = "/Library/redis/redis-2.8.17/src/redis-cli -h %s -p %s -n %s " %(host, port, db) #local
#redis_cli = "redis-cli -h %s -p %s -n %s " %(host, port, db)  #test_server
redis_cli = "/usr/local/redis/redis-cli -h %s -p %s -n %s " %(host, port, db) #online_server

def redis_get_pipe(cmd):
    return os.popen(redis_cli + cmd)

def redis_get_text(cmd):
    res = redis_get_pipe(cmd).read()
    return res  

def init_setname(rkey, gameId, clientIds):
       setname =[]
       for x in xrange(len(clientIds)):
           sname = ''
           #print x,':',clientIds[x]
           sname = rkey + ':' + str(gameId) + ':' + clientIds[x]
           setname.append(sname)
       return setname

def init_paytype_products(sname, products, unlimits, phonetypes, paytypes):
     for x in xrange(len(products)):
         product = products[x]
         prodId = product['tyid']
         prodPrice = product['price']
         
         for  y in xrange(len(unlimits)):
             unlimit = unlimits[y]
             
             for z in xrange(len(phonetypes)):
                 phonetype = phonetypes[z]
                 k = prodId + '_' + unlimit + '_' + phonetype
                 
                 for t in xrange( len( paytypes ) ):
                     type = paytypes[t]
                     v = '"{\\"paytype\\":\\"' + str( type ) + '\\",\\"price\\":\\"' + str( prodPrice ) + '\\"}"'

                     for s in xrange(len(sname)):
                         sn = sname[s]
                         ret = redis_get_text('hmset %s %s %s ' % (sn, k, v))
                         print sn, k, v, ret, '\n'


def init_paytype_diamonds(sname, diamonds, unlimits, phonetypes, paytypes):
     for x in xrange(len(diamonds)):
         diamond = diamonds[x]
         diamondId = diamond['id']
         diamondPrice = diamond['price']
         
         for  y in xrange(len(unlimits)):
             unlimit = unlimits[y]
             
             for z in xrange(len(phonetypes)):
                 phonetype = phonetypes[z]
                 k = diamondId + '_' + unlimit + '_' + phonetype

                 for t in xrange( len( paytypes ) ):
                     type = paytypes[t]
                     v = '"{\\"paytype\\":\\"' + str( type ) + '\\",\\"price\\":\\"' + str( diamondPrice ) + '\\"}"'
                 
                     for s in xrange( len( sname ) ):
                         sn = sname[s]
                         ret = redis_get_text( 'hmset %s %s %s ' % ( sn, k, v ) )
                         print sn, k, v, ret, '\n'

                     
#---------------------------套餐0------------------------------------                 
def do_init_products0():
    rkey = 'paytype'
    paytypes = ['tuyooios']
    unlimits = ['0', '1']
    phonetypes = ['0','1','2','3']
    gameId = 12
    clientIds = ['IOS_1.1_facebook.forrest.0.forrest.forrest',
                 'IOS_1.1_facebook.tuyooios.0.forrest.forrest',
                 'IOS_1.11337_tuyoo.tuyooios.0.appstore.appstore'
                 ]
    
    products = [
                # 套餐0 美元 转换为人民币定价
                {'tyid':'products0_sea_texas_chip_1', 'price': 1},
                {'tyid':'products0_sea_texas_chip_2', 'price': 5},
                {'tyid':'products0_sea_texas_chip_3', 'price': 20},
                {'tyid':'products0_sea_texas_chip_4', 'price': 50},
                {'tyid':'products0_sea_texas_chip_5', 'price': 100},
                {'tyid':'products0_sea_texas_chip_6', 'price': 200},

                {'tyid':'products0_sea_texas_coin_1', 'price': 1 },
                {'tyid':'products0_sea_texas_coin_2', 'price': 5 },
                {'tyid':'products0_sea_texas_coin_3', 'price': 20 },
                {'tyid':'products0_sea_texas_coin_4', 'price': 50 },
                {'tyid':'products0_sea_texas_coin_5', 'price': 100 },
                {'tyid':'products0_sea_texas_coin_6', 'price': 200 },
              ]
    
    sname = init_setname(rkey, gameId, clientIds)
    init_paytype_products(sname, products, unlimits, phonetypes, paytypes)
    
def do_init_diamonds0():
    rkey = 'paytype'
    paytypes = ['tuyooios']
    unlimits = ['0', '1']
    phonetypes = ['0','1','2','3']
    gameId = 12
    clientIds = ['IOS_1.1_facebook.forrest.0.forrest.forrest',
                 'IOS_1.1_facebook.tuyooios.0.forrest.forrest',
                 'IOS_1.11337_tuyoo.tuyooios.0.appstore.appstore'
                ]
    
    diamonds = [
                {'id':'DG100',   'count' : 100,   'price': 1,   'name':'钻石x100',   'icon' : ''},
                {'id':'DG500',   'count' : 500,   'price': 5,   'name':'钻石x500',   'icon' : ''},
                {'id':'DG2000',  'count' : 2000,  'price': 20,  'name':'钻石x2000',  'icon' : ''},
                {'id':'DG5000',  'count' : 5000,  'price': 50 , 'name':'钻石x5000',  'icon' : ''},
                {'id':'DG10000', 'count' : 10000, 'price': 100, 'name':'钻石x10000', 'icon' : ''},
                {'id':'DG20000', 'count' : 20000, 'price': 200, 'name':'钻石x20000', 'icon' : ''},
               ]
    
    sname = init_setname(rkey, gameId, clientIds)
    init_paytype_diamonds(sname, diamonds, unlimits, phonetypes, paytypes)
#---------------------------套餐0------------------------------------       

#---------------------------套餐4------------------------------------                 
def do_init_products4():
    rkey = 'paytype'
    paytypes = ['tuyooios']
    unlimits = ['0', '1']
    phonetypes = ['0','1','2','3']
    gameId = 12
    clientIds = ['IOS_1.1_facebook.forrest.0.forrest.forrest',
                 'IOS_1.1_facebook.tuyooios.0.forrest.forrest',
                 'IOS_1.11337_tuyoo.tuyooios.0.appstore.appstore',
                 'IOS_1.12337_tuyoo.tuyooios.0.appstore.appstore'
                ]
    
    products = [
                # 套餐4 人民币
                {'tyid':'products4_sea_texas_chip_1', 'price': 6},
                {'tyid':'products4_sea_texas_chip_2', 'price': 30},
                {'tyid':'products4_sea_texas_chip_3', 'price': 60},
                {'tyid':'products4_sea_texas_chip_4', 'price': 128},
                {'tyid':'products4_sea_texas_chip_5', 'price': 328},
                {'tyid':'products4_sea_texas_chip_6', 'price': 648},

                {'tyid':'products4_sea_texas_coin_1', 'price': 6 },
                {'tyid':'products4_sea_texas_coin_2', 'price': 30 },
                {'tyid':'products4_sea_texas_coin_3', 'price': 60 },
                {'tyid':'products4_sea_texas_coin_4', 'price': 128 },
                {'tyid':'products4_sea_texas_coin_5', 'price': 328 },
                {'tyid':'products4_sea_texas_coin_6', 'price': 648 },
              ]
    
    sname = init_setname(rkey, gameId, clientIds)
    init_paytype_products(sname, products, unlimits, phonetypes, paytypes)
    
def do_init_diamonds4():
    rkey = 'paytype'
    paytypes = ['tuyooios']
    unlimits = ['0', '1']
    phonetypes = ['0','1','2','3']
    gameId = 12
    clientIds = ['IOS_1.1_facebook.forrest.0.forrest.forrest',
                 'IOS_1.1_facebook.tuyooios.0.forrest.forrest',
                 'IOS_1.11337_tuyoo.tuyooios.0.appstore.appstore',
                 'IOS_1.12337_tuyoo.tuyooios.0.appstore.appstore'
                ]
    
    diamonds = [            
                {'id':'DG60',   'count' : 60,   'price': 6,    'name':'钻石x60',   'icon' : ''},
                {'id':'DG300',  'count' : 300,  'price': 30,   'name':'钻石x300',  'icon' : ''},
                {'id':'DG600',  'count' : 600,  'price': 60,   'name':'钻石x600',  'icon' : ''},
                {'id':'DG1280', 'count' : 1280, 'price': 128 , 'name':'钻石x1280', 'icon' : ''},
                {'id':'DG3280', 'count' : 3280, 'price': 328,  'name':'钻石x3280', 'icon' : ''},
                {'id':'DG6480', 'count' : 6480, 'price': 648,  'name':'钻石x6480', 'icon' : ''},
               ]
    
    sname = init_setname(rkey, gameId, clientIds)
    init_paytype_diamonds(sname, diamonds, unlimits, phonetypes, paytypes)
#---------------------------套餐4------------------------------------  


if __name__=='__main__':
#   do_init_products0()
#   do_init_diamonds0()
   do_init_products4()
   do_init_diamonds4()
