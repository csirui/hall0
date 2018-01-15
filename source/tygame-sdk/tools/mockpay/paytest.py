# -*- coding=utf-8 -*-
'''
Created on 2014-11-22

@author: Fan Zheng

使用说明:
    1.设置服务器地址host和端口号httpPort
    2.运行此脚本(python mockpay.py)
    3.输入paytype(tuyou.ali, ydmm, liantong.wo, aigame)
    4.输入failcallback, 表示失败回调.
    5.测试成功支付输出Buy Success Text:0 证明购买成功测试成功
    6.测试失败支付输出Buy Failure Text:0 证明购买失败测试成功
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
from products import Product
from tycodec import TyCodec

my_logger = None
def logout(msg):
    logging.basicConfig(filename='tmp/test.log', level=logging.INFO)
    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logging.info(t + ' ' + msg)
    #print(t + ' ' + msg)

class PayTest(object):

    #"tuyou.ali" "ydmm" "liantong.wo" "aigame"
    def __init__(self, paytype):
        self.paytype = paytype
        self.clientId = "Android_3.33_newpay"
        self.gameId = "6"
        self.host, self.httpPort = "125.39.218.101", 80
        #self.host, self.httpPort = "125.39.218.113", 80
        #self.host, self.httpPort = "42.62.53.180", 10000
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
        self.phoneType = "chinaUnion" #"chinaMobile"
        self.ss = None

    def dotest(self, appids, failcallback=False, newpay=True):
        logout("start test")
        if self.__dologin():
            logout("login success")
            self.doTcpOpen()
            ret = self.doTcpUserInfo()
            self.start_chip = self.chip
            self.start_coin = self.coin
            if newpay:
                if self.paytype == 'tuyooios':
                    self.doiostest(appids, failcallback)
                else:
                    self.doandroidtest(appids, failcallback)
                self.doTcpClose()

    def doandroidtest(self, appids, failcallback):
        self.clientId = 'Android_3.33_newpay'
        diamonds = Product.getProducts('android_diamonds_1')
        products = Product.getProducts('android_products_1')
        self.dothetest(appids, diamonds, products, failcallback)

    def doiostest(self, appids, failcallback):
        self.clientId = 'IOS_3.33_newpay'
        diamonds = Product.getProducts('ios_diamonds_1')
        products = Product.getProducts('ios_products_1')
        self.dothetest(appids, diamonds, products, failcallback)

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
        ret = self.doTcpUserInfo()
        self.start_chip = self.chip
        self.start_coin = self.coin
        success_str, fail_str = self.getResultStr(prodinfo, failcallback)
        if self.__charge(prodinfo):
            self.__mock_callback(failcallback)
            ret = self.doTcpUserInfo()
            self.last_coin = self.coin - self.start_coin
            logout(self.paytype + " buy " + prodinfo['tyid'] +  " success chip:" + str(self.last_chip) + " coin:" + str(self.last_coin))
            if self.last_coin == (self.prodPrice * 10):
                #print  "success:", self.gameId+':'+self.clientId, self.paytype, "buy diamondId:" + prodinfo['tyid']
                print success_str
            else:
                print fail_str

    def buychip(self, prodinfo, failcallback):
        ret = self.doTcpUserInfo()
        self.start_chip = self.chip
        self.start_coin = self.coin
        success_str, fail_str = self.getResultStr(prodinfo, failcallback)
        if self.__consume(prodinfo):
            if self.platformOrderId:
                self.__mock_callback(failcallback)
            time.sleep(0.07)
            ret = self.doTcpUserInfo()
            self.last_coin = self.coin - self.start_coin
            self.last_chip = self.chip - self.start_chip
            logout(self.paytype + " buy " + prodinfo['tyid'] +  " success chip:" + str(self.last_chip) + " coin:" + str(self.last_coin))
            if self.last_chip > 0:
                print success_str
            else:
                print fail_str

    def getResultStr(self, prodinfo, failcallback):
        if failcallback:
            success_str = 'Buy Failure Test:X' + " paytpe:" + self.paytype + " " + self.gameId+':'+self.clientId, " buy prodId:" + prodinfo['tyid']
            fail_str = 'Buy Failure Test:0' + " paytpe:" + self.paytype
        else:
            success_str = 'Buy Success Test:O' + " paytpe:" + self.paytype
            fail_str = 'Buy Success Test:X' + " paytpe:" + self.paytype + " " + self.gameId+':'+self.clientId, " buy prodId:" + prodinfo['tyid']
        return success_str, fail_str

    def __md5_sign(self, param):
        param_str = '&'.join(k + "=" + param[k] for k in sorted(param.keys()))
        logout("md5 sign str:" + param_str)
        des_str = TyCodec.des_encode(param_str)
        logout("des encode str:" + des_str)
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
        self.platformOrderId = msg['result']['platformOrderId']
        return True

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
        if msg['cmd'] == 'charge':
            self.platformOrderId = msg['result']['platformOrderId']
        elif msg['cmd'] == 'consume':
            self.platformOrderId = None
            orderId = msg['result']['orderId']
        #self.msgordercode = msg['result']['chargeData']['msgOrderCode']

        return True

    def __mock_callback(self, failcallback):
        cparams = {}
        if failcallback:
            cparams['failcallback'] = str(failcallback)
        cparams['userId'] = str(self.userId)
        cparams['appId'] = self.gameId
        cparams['authorCode'] = str(self.authorCode)
        cparams['clientId'] = self.clientId
        cparams['paytype'] = self.paytype
        cparams['platformOrderId'] = str(self.platformOrderId)
        #ydmm 600 liantongwo 600
        if self.paytype in ['ydmm', 'youku', 'yee2.card']:
            cparams['price'] = str(self.prodPrice * 100) #'600'
        elif self.paytype == 'liantong.wo':
            cparams['price'] = str(self.prodPrice * 100) #'600'
            self.msgordercode = '140808049867'
        else:
            cparams['price'] = str(self.prodPrice)#'6.00'

        cparams['smstext'] = self.msgordercode
        cparams['payCode'] = self.msgordercode
        sign = self.__md5_sign(cparams)
        cparams['code'] = sign
        cparam_str = '&'.join(k + "=" + cparams[k] for k in sorted(cparams.keys()))
        curl = 'http://%s:%d/open/v3/pay/mockpay?' % (self.host, self.httpPort) + cparam_str
        logout('HTTP Mockpay Request:' + curl)
        webpage = urlopen(curl)
        response = webpage.read()
        logout('HTTP Mockpay Response:' + response)
        webpage.close()
        #msg = json.loads(response)

        return True


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



#paytypes = ['tuyou.ali', 'ydmm', 'liantong.wo', 'aigame', 'tuyooios', 'yee.card', 'youku', 'zhangyue', 'yee2.card']
#appids = ['10', '6', '8', ]
paytypes = ['yee2.card']
appids = ['6']
#paytypes = ['tuyou.ali']
#paytype = str(raw_input("Please enter one paytype(tuyou.ali, ydmm, liantong.wo, aigame):"))
for paytype in paytypes:
    paytest = PayTest(paytype)
    paytest.dotest(appids)
    paytest.dotest(appids, True)

#print(Product.getProducts('ios_products_1'))


