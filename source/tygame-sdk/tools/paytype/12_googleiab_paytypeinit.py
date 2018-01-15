#-*- coding=utf-8 -*-
'''
初始化paytype数据
支付方式：googleiab
针对版本：GooglePlay上的Android版本


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

                     

#-----------------------------------------------套餐1 初始化--------------------------------------------------
def do_init_products1():
    rkey = 'paytype'
    paytypes = ['googleiab']
    unlimits = ['0', '1']
    phonetypes = ['0','1','2','3']
    gameId = 12
    clientIds = ['Android_1.1_facebook.forrest.0.forrest.forrest',
                 'Android_1.1_facebook.googleiab.0.forrest.forrest',
                 'Android_1.11337_facebook.googleiab.0.googleplay.googleplay',
                 'Android_1.11337_facebook.googleiab.0.googleplay.tss'
                 ]
    
    products = [
                # Google支付 套餐1  美元 转换为人民币定价
                {'tyid':'products1_sea_texas_chip_1', 'price': 6 },
                {'tyid':'products1_sea_texas_chip_2', 'price': 30 },
                {'tyid':'products1_sea_texas_chip_3', 'price': 120 },
                {'tyid':'products1_sea_texas_chip_4', 'price': 300 },
                {'tyid':'products1_sea_texas_chip_5', 'price': 600 },
#                {'tyid':'products1_sea_texas_chip_6', 'price': 1200 },
                {'tyid':'products1_sea_texas_chip_7', 'price': 60 },

                {'tyid':'products1_sea_texas_coin_1', 'price': 6 },
                {'tyid':'products1_sea_texas_coin_2', 'price': 30 },
                {'tyid':'products1_sea_texas_coin_3', 'price': 120 },
                {'tyid':'products1_sea_texas_coin_4', 'price': 300 },
                {'tyid':'products1_sea_texas_coin_5', 'price': 600 },
#                {'tyid':'products1_sea_texas_coin_6', 'price': 1200 },
                {'tyid':'products1_sea_texas_coin_7', 'price': 60 },
              ]
    
    sname = init_setname(rkey, gameId, clientIds)
    init_paytype_products(sname, products, unlimits, phonetypes, paytypes)
    
def do_init_diamonds1():
    rkey = 'paytype'
    paytypes = ['googleiab']
    unlimits = ['0', '1']
    phonetypes = ['0','1','2','3']
    gameId = 12
    clientIds = ['Android_1.1_facebook.forrest.0.forrest.forrest',
                 'Android_1.1_facebook.googleiab.0.forrest.forrest',
                 'Android_1.11337_facebook.googleiab.0.googleplay.googleplay',
                 'Android_1.11337_facebook.googleiab.0.googleplay.tss'
                ]
    
    diamonds = [
                #套餐1
                {'id':'DG60',    'count' : 60,    'price': 6,   'name':'钻石x60',   'icon' : ''},
                {'id':'DG300',   'count' : 300,   'price': 30,   'name':'钻石x300',  'icon' : ''},
                {'id':'DG600',   'count' : 600,   'price': 60,  'name':'钻石x600',  'icon' : ''},
                {'id':'DG1200',  'count' : 1200,  'price': 120,  'name':'钻石x1200', 'icon' : ''},
                {'id':'DG3000',  'count' : 3000,  'price': 300,  'name':'钻石x3000', 'icon' : ''},
                {'id':'DG6000',  'count' : 6000,  'price': 600, 'name':'钻石x6000', 'icon' : ''},
               ]
    
    sname = init_setname(rkey, gameId, clientIds)
    init_paytype_diamonds(sname, diamonds, unlimits, phonetypes, paytypes)
    
#-----------------------------------------------套餐2 初始化--------------------------------------------------
def do_init_products2():
    rkey = 'paytype'
    paytypes = ['googleiab']
    unlimits = ['0', '1']
    phonetypes = ['0','1','2','3']
    gameId = 12
    clientIds = [
                 'Android_1.12337_facebook.googleiab.0.googleplay.vnpt'
                 ]
    
    products = [
                # Google支付 套餐2  越南盾 : 人民币 = 20000 : 6
                {'tyid':'products2_sea_texas_chip_1', 'price': 6 }, #₫20000
                {'tyid':'products2_sea_texas_chip_2', 'price': 30 }, #₫100000
                {'tyid':'products2_sea_texas_chip_3', 'price': 60 }, #₫200000
                {'tyid':'products2_sea_texas_chip_4', 'price': 150 }, #₫500000
                {'tyid':'products2_sea_texas_chip_5', 'price': 300 }, #₫1000000
                {'tyid':'products1_sea_texas_chip_6', 'price': 600 }, #₫2000000

                {'tyid':'products2_sea_texas_coin_1', 'price': 6 }, #₫20000
                {'tyid':'products2_sea_texas_coin_2', 'price': 30 }, #₫100000
                {'tyid':'products2_sea_texas_coin_3', 'price': 60 }, #₫200000
                {'tyid':'products2_sea_texas_coin_4', 'price': 150 }, #₫500000
                {'tyid':'products2_sea_texas_coin_5', 'price': 300 }, #₫1000000
                {'tyid':'products1_sea_texas_coin_6', 'price': 600 }, #₫2000000
              ]
    
    sname = init_setname(rkey, gameId, clientIds)
    init_paytype_products(sname, products, unlimits, phonetypes, paytypes)
    
def do_init_diamonds2():
    rkey = 'paytype'
    paytypes = ['googleiab']
    unlimits = ['0', '1']
    phonetypes = ['0','1','2','3']
    gameId = 12
    clientIds = [
                 'Android_1.12337_facebook.googleiab.0.googleplay.vnpt'
                ]
    
    diamonds = [
                #套餐2
                {'id':'DG60',   'count' : 60,   'price': 6,    'name':'钻石x60',   'icon' : ''},
                {'id':'DG300',  'count' : 300,  'price': 30,   'name':'钻石x300',  'icon' : ''},
                {'id':'DG600',  'count' : 600,  'price': 60,   'name':'钻石x600',  'icon' : ''},
                {'id':'DG1500', 'count' : 1500, 'price': 150,  'name':'钻石x1500', 'icon' : ''},
                {'id':'DG3000', 'count' : 3000, 'price': 300 , 'name':'钻石x3000', 'icon' : ''},
                {'id':'DG6000', 'count' : 6000, 'price': 600,  'name':'钻石x6000', 'icon' : ''},
               ]
    
    sname = init_setname(rkey, gameId, clientIds)
    init_paytype_diamonds(sname, diamonds, unlimits, phonetypes, paytypes)
    

if __name__=='__main__':
   do_init_products1()
   do_init_diamonds1()
   
   do_init_products2()
   do_init_diamonds2()
