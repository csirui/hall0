# -*- coding=utf-8 -*-
'''
Created on 2014-11-22

@author: Fan Zheng

使用说明:
    1.设置服务器地址host和端口号httpPort
    2.运行此脚本(python sdkmonitor.py)
    3.输入paytype(tuyooios, ydmm)
    5.测试成功支付输出O:Charge Success Test 证明购买测试成功
    6.测试成功支付输出X:Charge Success Test 证明购买测试失败
'''

import sys
import json
import zlib
import traceback
import socket
import datetime
import time
from urllib import urlopen
from hashlib import md5
import logging
from tycodec import TyCodec

my_logger = None
def logout(msg):
    #logging.basicConfig(filename='tmp/test.log', level=logging.INFO)
    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #logging.info(t + ' ' + msg)
    #print(t + ' ' + msg)

class PayTest(object):

    #"tuyou.ali" "ydmm" "liantong.wo" "aigame"
    def __init__(self, paytype):
        self.paytype = paytype
        self.clientId = "Android_3.33_newpay"
        self.gameId = "6"
        #self.host, self.httpPort = "open.touch4.me", 80
        #self.host, self.httpPort = "125.39.218.113", 80
        #self.host, self.httpPort = "42.62.53.180", 80
        self.host, self.httpPort = "125.39.218.101", 3002
        self.deviceId = "16"
        self.imei = "16"
        self.snsId = "kugou:1"
        self.userId = ""
        self.authorCode = ""
        self.authInfo = ""
        self.userEmail = ""
        self.tcpIp = ""
        self.tcpPort = ""
        self.prodId = "TY9999D0006001"
        self.prodName = "6元金币"
        self.prodPrice = "60"
        self.platformOrderId = ""
        self.start_chip = 0
        self.chip = 0
        self.last_chip = 0
        self.start_coin = 0
        self.coin = 0
        self.last_coin = 0
        self.msgordercode = "30000841069402"
        #self.phoneType = "chinaMobile"
        #self.phoneType = "chinaUnion"
        #self.phoneType = "chinaTelecom"
        self.phoneType = "other"
        self.ss = None
        self.android_diamonds = {'6':
                                    [
                                     {'tyid':'TY9999R0008001', 'count' : 80, 'price': 8, 'name':'钻石x80', 'icon' : ''},
                                     {'tyid':'TY9999R0050001', 'count' : 500, 'price': 50,   'name':'钻石x500',   'icon' : ''},
                                    ]
        }
        self.android_products = {'6':
                                    [
                                     {'tyid': 'TY9999D0006001', 'name':'60000金币', 'price':6},
                                     {'tyid': 'TY9999D0030001', 'name':'300000金币', 'price':300}
                                    ]
        }
        self.android_2_products = {'6':
                                    [
                                     {'tyid': 'VOICE100', 'name':'xiaolaba', 'price':1}
                                    ]
        }
        self.ios_diamonds = {'6':
                                [
                                 {'tyid': 'TY9999R0006001', 'name':'60钻石（可以用来兑换金币或购买道具）',
                                   'price':6, 'iosid': 'cn.com.doudizhu.happy.hall.7', },
                                ]
        }
        self.ios_products = {'6':
                                [
                                 {'tyid': 'TY9999D0006003', 'name':'6万金币', 'price':6,
                                          'iosid': 'cn.com.doudizhu.happy.1', },
                                ]
        }
    def dotest(self, appids, failcallback=False, newpay=True,
        clientids={'Android_3.37_tuyoo.weakChinaMobile.0-hall6.ydmm.happy'}):
        logout("start test")
        if self.__dologin():
            logout("login success")
            if newpay:
                if self.paytype == 'tuyooios':
                    self.doiostest(appids, failcallback)
                else:
                    self.doandroidtest(appids, failcallback, clientids)
            else:
                self.dopaytestv2(appids, failcallback)
        else:
            print "X:login failed"

    def doandroidtest(self, appids, failcallback, clientids):
        for clientid in clientids:
            self.clientId = clientid
            diamonds = self.android_diamonds
            products = self.android_products
            self.dothetest(appids, diamonds, products, failcallback)

    def doiostest(self, appids, failcallback):
        self.clientId = 'IOS_3.37_tuyoo.appStore.0-hall6.tuyoo.huanle'
        diamonds = self.ios_diamonds
        products = self.ios_products
        self.dothetest(appids, diamonds, products, failcallback)

    def dopaytestv2(self, appids, failcallback):
        self.clientId = 'Android_2.92_360'
        for prodinfo in self.android_2_products['6']:
            self.__straight(prodinfo)

    def dothetest(self, appids, diamonds, products, failcallback):
        for appid in diamonds.keys():
            if appid not in appids:
                continue
            self.gameId = appid
            for prodinfo in diamonds[appid]:
                self.buydiamond(prodinfo, failcallback)
        for appid in products.keys():
            if appid not in appids:
                continue
            self.gameId = appid
            for prodinfo in products[appid]:
                self.buychip(prodinfo, failcallback)

    def buydiamond(self, prodinfo, failcallback):
        self.__charge(prodinfo)

    def buychip(self, prodinfo, failcallback):
        self.__consume(prodinfo)

    def __md5_sign(self, param):
        param_str = '&'.join(k + "=" + param[k] for k in sorted(param.keys()))
        #logout("md5 sign str:" + param_str)
        des_str = TyCodec.des_encode(param_str)
        #logout("des encode str:" + des_str)
        digest = md5(des_str).hexdigest()
        return digest

    def __dologin(self):
        logout("start login")
        params = {}
        params['appId'] = self.gameId
        params['clientId'] = self.clientId
        params['deviceId'] = TyCodec.des_encode(self.deviceId)
        params['snsId'] = TyCodec.des_encode(self.snsId)
        params['imei'] = TyCodec.des_encode(self.imei)
        params['phoneType'] = self.phoneType
        
        sign = self.__md5_sign(params)
        params['code'] = sign
        param_str = '&'.join(k + "=" + params[k] for k in sorted(params.keys()))
        murl = 'http://%s:%d/open/v3/user/processSnsId?' % (self.host, self.httpPort) + param_str
        logout('HTTP Login Request:' + murl)
        webpage = urlopen(murl)
        response = webpage.read()
        logout('HTTP Login Response:' + response)
        webpage.close()
        msg = json.loads(response)
        self.userId = msg['result']['userId']
        self.authorCode = msg['result']['authorCode']
        self.userEmail = msg['result']['userEmail']
        self.authInfo = {'authcode':self.authorCode, 'account':self.userEmail, 'uid':self.userId }
        self.authInfo = json.dumps(self.authInfo)
        self.tcpIp = msg['result']['tcpsrv']['ip']
        self.tcpPort = int(msg['result']['tcpsrv']['port'])
        return True

    def __straight(self, prodinfo):
        cparams = {}
        cparams['userId'] = str(self.userId)
        cparams['appId'] = self.gameId
        cparams['authInfo'] = str(self.authInfo)
        cparams['clientId'] = self.clientId
        cparams['buttonId'] = prodinfo['tyid'] #self.prodId
        cparams['phonetype'] = '0'
        cparam_str = '&'.join(k + "=" + cparams[k] for k in sorted(cparams.keys()))
        curl = 'http://%s:%d/v1/pay/paytype/get?' % (self.host, self.httpPort) + cparam_str
        logout('HTTP Charge Request:' + curl)
        webpage = urlopen(curl)
        response = webpage.read()
        logout('HTTP Charge Response:' + response)
        webpage.close()
        msg = json.loads(response)
        if 'result' in msg and msg['result']['payType']:
            cparams = {}
            cparams['userId'] = str(self.userId)
            cparams['appId'] = self.gameId
            cparams['authInfo'] = str(self.authInfo)
            cparams['clientId'] = self.clientId
            cparams['buttonId'] = prodinfo['tyid'] #self.prodId
            cparams['phoneType'] = self.phoneType
            cparams['apiVer'] = '2'
            cparams['deviceId'] = self.deviceId
            cparams['v'] = '2'
            cparams['orderId'] = 'tuyootest123'
            cparams['orderPrice'] = str(msg['result']['price'])
            cparams['orderName'] = prodinfo['name']
            cparams['orderDesc'] = ''
            cparams['orderPicUrl'] = ''
            cparams['prodId'] = prodinfo['tyid'] #self.prodId
            cparams['phonenum'] = ''
            cparams['payType'] = msg['result']['payType']
            cparams['payChannel'] = 'tuyoo'
            cparam_str = '&'.join(k + "=" + cparams[k] for k in sorted(cparams.keys()))
            curl = 'http://%s:%d/v1/pay/straight?' % (self.host, self.httpPort) + cparam_str
            logout('HTTP Straight Request:' + curl)
            webpage = urlopen(curl)
            response = webpage.read()
            logout('HTTP Straight Response:' + response)
            webpage.close()
            msg = json.loads(response)
            if 'result' in msg and msg['result']['orderPlatformId']:
                print 'O:2.0 Straight Test', self.gameId+':'+self.clientId
            else:
                print 'X:2.0 Straight Test', self.gameId+':'+self.clientId, " buy prodId:" + prodinfo['tyid']
        else:
            print 'X:2.0 Straight Test', self.gameId+':'+self.clientId, " buy prodId:" + prodinfo['tyid']


    def __charge(self, prodinfo):
        cparams = {}
        cparams['userId'] = str(self.userId)
        cparams['appId'] = self.gameId
        cparams['authorCode'] = str(self.authorCode)
        cparams['clientId'] = self.clientId
        cparams['diamondId'] = prodinfo['tyid'] #self.prodId
        cparams['diamondName'] = prodinfo['name'] #self.prodName
        self.prodPrice = int(prodinfo['price'])
        cparams['diamondPrice'] = str(self.prodPrice) #self.prodPrice
        cparams['diamondCount'] = "1"
        cparams['prodOrderId'] = ""
        if self.clientId[0:3] == 'IOS':
            cparams['payType'] = "tuyooios"
        sign = self.__md5_sign(cparams)
        cparams['code'] = sign
        cparam_str = '&'.join(k + "=" + cparams[k] for k in sorted(cparams.keys()))
        curl = 'http://%s:%d/open/v3/pay/charge?' % (self.host, self.httpPort) + cparam_str
        logout('HTTP Charge Request:' + curl)
        webpage = urlopen(curl)
        response = webpage.read()
        logout('HTTP Charge Response:' + response)
        webpage.close()
        msg = json.loads(response)
        try:
            if msg['result']['platformOrderId']:
                if 'chargeCategories' in msg['result']:
                    paytype = 'chargeCategories'
                else:
                    paytype =  msg['result']['chargeType']
                print 'O:3.0 Charge  Test', self.gameId+':'+self.clientId, ' paytype:' + paytype
            else:
                print 'X:3.0 Charge  Test', self.gameId+':'+self.clientId, " buy prodId:" + prodinfo['tyid'], 'response', response
        except:
            print 'X:3.0 Charge  Test', self.gameId+':'+self.clientId, " buy prodId:" + prodinfo['tyid'], 'response', response


    def __consume(self, prodinfo, mustcharge='1'):
        cparams = {}
        cparams['userId'] = str(self.userId)
        cparams['appId'] = self.gameId
        cparams['authorCode'] = str(self.authorCode)
        cparams['clientId'] = self.clientId
        cparams['prodId'] = prodinfo['tyid'] #self.prodId
        cparams['prodName'] = prodinfo['name'] #self.prodName
        cparams['prodCount'] = "1"
        self.prodPrice = int(prodinfo['price'])
        cparams['prodPrice'] = str(self.prodPrice * 10) #self.prodPrice
        cparams['prodOrderId'] = ""
        if self.clientId[0:3] == 'IOS':
            cparams['payType'] = "tuyooios"
        #钻石直充
        cparams['mustcharge'] = mustcharge #'1'
        sign = self.__md5_sign(cparams)
        cparams['code'] = sign
        cparam_str = '&'.join(k + "=" + cparams[k] for k in sorted(cparams.keys()))
        curl = 'http://%s:%d/open/v3/pay/consume?' % (self.host, self.httpPort) + cparam_str
        logout('HTTP Consume Request:' + curl)
        webpage = urlopen(curl)
        response = webpage.read()
        logout('HTTP Consume Response:' + response)
        webpage.close()
        msg = json.loads(response)
        #if msg['cmd'] == 'charge':
        #    self.platformOrderId = msg['result']['platformOrderId']
        #elif msg['cmd'] == 'consume':
        #    self.platformOrderId = None
        #    orderId = msg['result']['orderId']
        try:
            if msg['result']['platformOrderId'] or msg['result']['orderId']:
                if 'chargeCategories' in msg['result']:
                    paytype = 'chargeCategories'
                else:
                    paytype =  msg['result']['chargeType']
                print 'O:3.0 Consume Test', self.gameId+':'+self.clientId, ' paytype:' + paytype
            else:
                print 'X:3.0 Consume Test', self.gameId+':'+self.clientId, " buy prodId:" + prodinfo['tyid'], 'response', response
        except:
            print 'X:3.0 Consume Test', self.gameId+':'+self.clientId, " buy prodId:" + prodinfo['tyid'], 'response', response


    def doTcpOpen(self):
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ss.settimeout(3000)
        logout('Connect tcp ' + self.tcpIp +  ':' + str(self.tcpPort))
        ss.connect((self.tcpIp, self.tcpPort))
        seads = ss.recv(4)
        self.session_seed = int(seads, 16)
        self.ss = ss
        self.__buffer = ''

    def doTcpClose(self):
        logout('Tcp closed')
        if self.ss :
            self.ss.close()
            self.ss = None

    def doTcpCommand(self, cmdDict, needCmd=None, needResponse=True) :
        self.doSendTcpCommand(cmdDict)
        if not needCmd:
            needCmd = cmdDict['cmd']
            logout("needCmd=None, needCmd:" + str(needCmd))
        if not needResponse :
            return None
        return self.doReceiveTcpCommand(needCmd)

    def ty_encode(self, srcstr):
        dlen = len(srcstr)
        tstr = '%04X' % dlen
        czstr = TyCodec.tycode(self.session_seed + dlen, srcstr)
        return tstr + czstr

    def ty_decode(self, dststr):
        ddstr = TyCodec.tycode(self.session_seed + int(dststr[:4], 16), dststr[4:])
        ddstr = zlib.decompress(ddstr)
        return ddstr

    def doSendTcpCommand(self, cmdDict) :
        requeststr = json.dumps(cmdDict) + '\r\n'
        requeststr = self.ty_encode(requeststr)
        self.ss.send(requeststr)
        #logout("Request, requeststr:" + str(requeststr))

    def doReceiveTcpCommand(self, needCmd=None) :
        stime = time.time()
        wait_time = 3
        if needCmd == "prod_delivery":
            wait_time = 3000
        while True :
            data = self.ss.recv(2048)
            #logout("receivedata, data:" + str(data))
            if data :
                response = self.dataReceived(data, needCmd)
                #logout("receivedata, response:" + str(response))
                if not response:
                    continue
                if response :
                    return response
            if time.time() - stime > time:
                return None
        return None

    def dataReceived(self, data, needCmd):
        self.__buffer = self.__buffer + data
        dlen = len(self.__buffer)
        while dlen > 4 :
            mlen = self.__buffer[0:4]
            try:
                mlen = int(mlen, 16)
            except:
                print 'ERROR ZIP HEAD LENGTH !', self, mlen
                self.doTcpClose()
                return

            if dlen < mlen + 4 :
                logout("dataReceived dlen:" + str(dlen) + " " + str(mlen))
                return False

            line = self.__buffer[:(mlen + 4)]
            if mlen + 4 == dlen :
                self.__buffer = ''
            else:
                self.__buffer = self.__buffer[(mlen + 4):]
            res = self.parseTcpLines(line, needCmd)
            if res:
                return res
            dlen = len(self.__buffer)
        return False

    def parseTcpLines(self, line, needCmd) :
        data = self.ty_decode(line)
        data = data.strip('\n\0')
        response = json.loads(data)
        if 'error' in response :
            return response
        resCmd = response['cmd']
        #logout("parseTcpLines response:" + str(response))
        if resCmd == needCmd :
            if self.userId > 0 and 'userId' in response['result']:
                if self.userId == response['result']['userId'] :
                    return response
                else:
                    return None
            else:
                return response
        return None

    def doTcpUserInfo(self):
        cmd = {'cmd':'user_info', 'params':{'userId':self.userId,
                                            'gameId':self.gameId ,
                                            'phoneType':'chinaMobile',
                                            'clientId':self.clientId,
                                            'authorCode':self.authorCode}}
        logout('TCP userinfo Request' + str(cmd))
        msg = self.doTcpCommand(cmd)
        logout('TCP userinfo Response' +  str(msg))
        uid = msg['result']['userId']
        if self.userId == uid :
            self.chip = msg['result']['udata']['chip']
            self.coin = msg['result']['udata']['diamond']
            return True
        return False


paytypes = ['tuyooios','ydmm']
#paytypes = ['tuyooios']
appids = ['6']
clientids = ['Android_3.363_oppo.oppo,weakChinaMobile,woStore.0-hall6.oppo.dj',
             'Android_3.363_huawei.huawei,weakChinaMobile,woStore.0-hall6.huawei.dj',
             'Android_3.363_pps.pps,weakChinaMobile,woStore,aigame.0-hall6.pps.dj',
             'Android_3.363_tuyoo.lenovo,weakChinaMobile,woStore,aigame.0-hall6.lenovo.dj',
             'Android_3.363_vivo.vivo,weakChinaMobile,woStore,aigame.0-hall6.vivo.dj',
             'Android_3.363_zhangyue.zhangyue,weakChinaMobile,woStore,aigame.0-hall6.zhangyue.dj',
             'Android_3.363_midanji.midanji,weakChinaMobile,woStore,aigame.0-hall6.mi.midanji',
             'Android_3.363_youku.youku,weakChinaMobile,aigame.0-hall6.youku.happy',
             'Android_3.37_360.360.0-hall6.360.day',
             'Android_3.363_tuyoo.weakChinaMobile.0-hall6.wandou.happy',
             'Android_3.37_tuyoo.YDJD.0-hall6.ydjd.dj',
             'Android_3.37_mi.mi,weakChinaMobile,woStore,aigame.0-hall6.mi.dj',
             'Android_3.37_tuyoo.yisdkpay.0-hall6.youyifu.happy',
             'Android_3.37_tuyoo.lenovodj.0-hall6.lianxiangyouxi.dj',
             'Android_3.37_uc.uc.0-hall6.uc.dj',
             'Android_3.37_tuyoo.duoku.0-hall6.baidu.dj',
            ]
for paytype in paytypes:
    paytest = PayTest(paytype)
    paytest.dotest(appids, clientids=clientids)

paytest = PayTest('ydmm')
paytest.dotest(appids, newpay=False)



