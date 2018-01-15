# -*- coding=utf-8 -*-

# import re
from tyframework.orderids import gamereg, orderid

'''
服务器的定义控制器
主要为了登陆的控制、API的转发控制
'''


class ServerControl(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        # 2014/12/2 对于113sdk，会把这个版本号转为大写
        self.orderIdVer1 = 'a'  # Decimal62.tostr62(10, 1)  # a
        self.consumeOrderIdVer1 = 'b'  # Decimal62.tostr62(11, 1)  # b

        self.orderIdVer3 = 'c'  # Decimal62.tostr62(12, 1)  # c
        self.consumeOrderIdVer3 = 'd'  # Decimal62.tostr62(13, 1)  # d
        self.danjiOrderIdVer3 = 'f'  # Decimal62.tostr62(15, 1)  # f
        self.smsBindOrderIdVer3 = 's'  # Decimal62.tostr62(13, 1)  # d
        self.changTianYouOrderIdVer3 = 'y'  # Decimal62.tostr62(13, 1)  # d

    def is_valid_orderid_str(self, orderId):
        return orderid.is_valid_orderid_str(orderId)

    #         return re.match(r'^[a-zA-Z0-9]{14}', orderid)


    #     def __is_match_ids__(self, clientId, clientIds):
    #         for cid in clientIds :
    #             if self.__ctx__.strutil.reg_match(cid, clientId) :
    #                 return True
    #         return False

    #     def get_control_all(self, appId):
    #         controlall = self.__ctx__.Configure.get_configure_json('sdk.server.control.' + str(appId))
    #         return controlall

    #     def findServerControlByHttp(self, appId, httpgame):
    #         controlall = self.get_control_all(appId)
    #         if controlall :
    #             for x in xrange(len(controlall) - 1, -1, -1):
    #                 control = controlall[x]
    #                 if httpgame == control['http'] :
    #                     return control
    #         return None

    def findServerControl(self, appId, clientId):
        mode, httpgame = gamereg.findGameModeHttpByClientId(clientId)
        return {'http': httpgame, 'mode': mode}

    #         curdomain = None
    #         try:
    #             control = self.__ctx__.RunMode.get_server_control()
    #             if control != None :
    #                 return control
    #
    #             if int(appId) >= 10000 :
    #                 return None
    #
    #             curdomain = self.__ctx__.TYGlobal.http_sdk()
    #             controlall = self.get_control_all(appId)
    #             serverControl = None
    #             if controlall :
    #                 # 只有接入的SDK地址和当前的SDK地址一致时，才进行检测
    #                 for x in xrange(len(controlall) - 1, -1, -1):
    #                     control = controlall[x]
    #                     if curdomain == control['http.sdk'] :
    #                         if self.__is_match_ids__(clientId, control['ids']) :
    #                             serverControl = control
    #                             break
    #             if not serverControl and self.__ctx__.TYGlobal.mode() != 1 :
    #                 for x in xrange(len(controlall) - 1, -1, -1):
    #                     control = controlall[x]
    #                     if curdomain == control['http.sdk'] and control['http'] == self.__ctx__.TYGlobal.http_game():
    #                         serverControl = control
    #                         break
    #             if not serverControl :
    #                 raise Exception('ServerControl not found appId=' + str(appId) + ' clientId=' + str(clientId) + ' curdomain=' + str(curdomain))
    #             return serverControl
    #         except :
    #             self.__ctx__.ftlog.exception('ServerControl->findServerControl ERROR ->', clientId, appId, curdomain)
    #         return None

    #     def findServerControlByOrderId(self, orderId):
    #         appId = self.__ctx__.strutil.toint10(orderId[1:4])
    #         tag = self.__ctx__.strutil.toint10(orderId[4:5])
    #         return self.findServerControlByTag(appId, tag)

    #     def findServerControlByTag(self, appId, tag):
    #         try:
    #             control = self.__ctx__.RunMode.get_server_control()
    #             if control != None :
    #                 self.__ctx__.ftlog.debug('ServerControl->findServerControlByTag found test link server !')
    #                 if tag == control['tag'] :
    #                     return control
    #                 self.__ctx__.ftlog.error('ServerControl->findServerControlByTag found test link server ! tag not equal ! ', tag , control)
    #                 return control
    #
    #             if int(appId) >= 10000 :
    #                 return None
    #
    #             controlall = self.get_control_all(appId)
    #             serverControl = None
    #             if controlall :
    #                 for x in xrange(len(controlall) - 1, -1, -1):
    #                     control = controlall[x]
    #                     if tag == control['tag'] :
    #                         serverControl = control
    #                         break
    #             self.__ctx__.ftlog.debug('ServerControl->findServerControlByTag->', tag, appId, serverControl)
    #             return serverControl
    #         except :
    #             self.__ctx__.ftlog.exception()
    #         return None

    def findUserTcpAddress(self, appId, clientId, userId):
        return gamereg.findUserTcpAddress(userId, clientId)

    #         try:
    #             if int(appId) >= 10000 :
    #                 return None, None
    #
    #             tip, tport = self.__ctx__.RunMode.get_user_tcp_address(userId)
    #             if tip != None and tport != None :
    #                 return tip, tport
    #
    #             serverControl = self.findServerControl(appId, clientId)
    #             if serverControl and 'tcpsrv' in serverControl:
    #                 if '_tcpsrv_' in serverControl :
    #                     tcplist = serverControl['_tcpsrv_']
    #                 else:
    #                     tcplist = []
    #                     serverControl['_tcpsrv_'] = tcplist
    #                     tlist = serverControl['tcpsrv']
    #                     for tcp in tlist :
    #                         tcpip = tcp[0]
    #                         tcpport = tcp[1]
    #                         if isinstance(tcpport , (list, tuple)) :
    #                             for x in xrange(tcpport[0], tcpport[1] + 1):
    #                                 tcplist.append([tcpip, x])
    #                         elif isinstance(tcpport, int):
    #                             tcplist.append([tcpip, tcpport])
    # #                 ftlog.info('ServerControl->findUserTcpAddress->', appId, clientId, userId, tcplist)
    #                 if len(tcplist) > 0 :
    #                     tcpitem = tcplist[userId % len(tcplist)]
    # #                     ftlog.info('ServerControl->findUserTcpAddress->', appId, clientId, userId, tcpitem)
    #                     return tcpitem[0], tcpitem[1]
    #         except :
    #             self.__ctx__.ftlog.exception()
    #         self.__ctx__.ftlog.info('ServerControl->findUserTcpAddress ERROR->', appId, clientId, userId)
    #         return None, None


    #     def __make_order_id__(self, appId, clientId, orderIdVer62):
    #         try:
    #             appId = int(appId)
    #             control = self.findServerControl(appId, clientId)
    #             seqNum = int(self.__ctx__.RedisMix.execute('INCR', 'global.orderid.seq.' + orderIdVer62))
    #             otime = self.__ctx__.TimeStamp.get_current_timestamp()
    #             if control :
    #                 srvTag = control['tag']
    #             else:
    #                 srvTag = 0
    #             # orderId构成:<1位API版本号>+<3位APPID>+<1位服务器标记>+<6位时间戳>+<3位序号>，共14位
    #             oid = orderIdVer62 + self.__ctx__.strutil.tostr62(appId, 3) + \
    #                   self.__ctx__.strutil.tostr62(srvTag, 1) + self.__ctx__.strutil.tostr62(otime, 6) + \
    #                   self.__ctx__.strutil.tostr62(seqNum, 3)
    #
    #             self.__ctx__.RunMode.set_server_link(oid)
    #
    #             return oid
    #         except :
    #             self.__ctx__.ftlog.exception('__make_order_id__ ERROR ->', appId, orderIdVer62, clientId)
    #         return None

    def get_appid_frm_order_id(self, orderId):
        return orderid.get_appid_frm_order_id(orderId)

    #         # a00111x54Lq00l
    #         # apiVer, appId, tag, otime, seq
    #         _, appId, _, _, _ = self.get_order_id_info(orderId)
    #         return appId

    #     def get_order_id_info(self, orderId):
    #         # a00111x54Lq00l
    #         apiVer, appId, tag, otime, seq = 0 , 0, 0, 0 , 0
    #         if len(orderId) == 14 :
    #             apiVer = self.__ctx__.strutil.toint10(orderId[0])
    #             appId = self.__ctx__.strutil.toint10(orderId[1:4])
    #             tag = self.__ctx__.strutil.toint10(orderId[4])
    #             otime = self.__ctx__.strutil.toint10(orderId[5:11])
    #             seq = self.__ctx__.strutil.toint10(orderId[11:14])
    #         return apiVer, appId, tag, otime, seq

    def makeConsumeOrderIdV3(self, userId, appId, clientId):
        return orderid.makeConsumeOrderIdV3(userId, appId, clientId)

    #         return self.__make_order_id__(appId, clientId, self.consumeOrderIdVer3)

    def makeChargeOrderIdV3(self, userId, appId, clientId):
        return orderid.makeChargeOrderIdV3(userId, appId, clientId)

    #         return self.__make_order_id__(appId, clientId, self.orderIdVer3)

    def makeChargeOrderIdV4(self, userId, appId, clientId):
        return orderid.makeChargeOrderIdV4(userId, appId, clientId)

    #         return self.__make_order_id__(appId, clientId, self.orderIdVer3)


    def makeSmsBindOrderIdV3(self, userId, appId, clientId):
        return orderid.makeSmsBindOrderIdV3(userId, appId, clientId)

    #         return self.__make_order_id__(appId, clientId, self.smsBindOrderIdVer3)

    def makeChangTianYouOrderIdV3(self, userId, appId, clientId):
        return orderid.makeChangTianYouOrderIdV3(userId, appId, clientId)

    #         return self.__make_order_id__(appId, clientId, self.changTianYouOrderIdVer3)

    def makePlatformOrderIdV1(self, userId, params):
        return orderid.makePlatformOrderIdV1(userId, params)

    #         appId = int(params['appId'])
    #         clientId = params['clientId']
    #         return self.__make_order_id__(appId, clientId, self.orderIdVer1)

    def makeGameOrderIdV1(self, userId, params):
        return orderid.makeGameOrderIdV1(userId, params)

    #         appId = int(params['appId'])
    #         clientId = params['clientId']
    #         return self.__make_order_id__(appId, clientId, self.consumeOrderIdVer1)

    def checkLoginForbid(self, rpath, postData=''):
        '''
        检查是否被禁止登陆
        '''
        return gamereg.checkLoginForbid()


# try:
#             clientId = self.__ctx__.RunHttp.getRequestParam('clientId', '')
#             appId = self.__ctx__.RunHttp.getRequestParamInt('appId', -1)
#             if appId < 0 :
#                 appId = self.__ctx__.RunHttp.getRequestParamInt('gameId', -1)
#                 if appId < 0 :
#                     userId = self.__ctx__.RunHttp.getRequestParamInt('userId', -1)
#                     if userId > 0 :
#                         appId = self.__ctx__.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'sessionAppId')
#                         if appId == None :
#                             appId = -1
#             if appId >= 0 and appId < 10000 :
#                 control = self.findServerControl(appId, clientId)
#                 if control and 'nologin' in control :
#                     if self.__is_match_ids__(clientId, control['nologin']) :
#                         self.__ctx__.ftlog.debug('ServerControl->checkLoginForbid->', appId, clientId, 'login foribidden !')
#                         mo = self.__ctx__.MsgPack()
#                         mo.setResult('code', 10)
#                         mo.setResult('info', control['nologinmsg'])
#                         return mo
#         except :
#             self.__ctx__.ftlog.exception()
#         return False

ServerControl = ServerControl()
