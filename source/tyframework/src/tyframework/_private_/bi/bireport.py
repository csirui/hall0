# -*- coding=utf-8 -*-
import struct
import time


class BiReport(object):
    def __call__(self, *args, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.CHIP_TYPE_CHIP = 1  # 金币
        self.CHIP_TYPE_TABLE_CHIP = 2  # TABLE_CHIP
        self.CHIP_TYPE_COIN = 3  # COIN
        self.CHIP_TYPE_DIAMOND = 4  # DIAMODN
        self.CHIP_TYPE_COUPON = 5  # COUPON
        self.__RLOGGER__ = None
        self.__PROCESSID__ = None
        self.__GAMENAME__ = None
        self.__GAME_ID__ = None
        self.__bicollects__ = {}
        self.__callbacks__ = {}

    def _init_singleton_(self):
        logoutfile = self.__ctx__.TYGlobal.path_bireport() + '/bi.' + self.__ctx__.TYGlobal.log_file_name()
        self.__ctx__.ftlog.info('open bi report file ->', logoutfile)
        self.__RLOGGER__ = self.__ctx__.ftlog.open_normal_logfile(logoutfile)
        self.__PROCESSID__ = int(self.__ctx__.TYGlobal.run_process_id())
        self.__GAMENAME__ = self.__ctx__.TYGlobal.name()
        self.__GAME_ID__ = int(self.__ctx__.TYGlobal.gameid())
        self.__report__(['open'], {})
        self.__bicollects__ = {}
        self._init_bicollects_()

    def __make_msg__(self, arglist, argdict):
        t = self.__ctx__.TimeStamp.format_time_ms()
        jsondata = [t, self.__GAME_ID__, self.__GAMENAME__, self.__PROCESSID__]
        jsondata.extend(arglist)
        jsondata.append(argdict)

        msg = self.__ctx__.strutil.dumps(jsondata)
        msg = msg.replace('\\n', '\\\\n')
        msg = msg.replace('\\r', '')
        msg = msg.replace('\\t', '')
        return msg

    def __report__(self, arglist, argdict):
        if self.__RLOGGER__ != None:
            msg = self.__make_msg__(arglist, argdict)
            self.__RLOGGER__.info(msg)
            try:
                if len(arglist) > 1 and isinstance(arglist[1], int):
                    callback = self.__callbacks__.get(arglist[1], None)
                    if callable(callback):
                        callback(arglist, argdict)
            except:
                self.__ctx__.ftlog.exception()

    def __get_current_day__(self):
        return self.__ctx__.TimeStamp.format_time_day_short()

    def register_game_callback(self, gameid, callback):
        self.__callbacks__[gameid] = callback

    def report(self, *arglist, **argdict):
        alist = ['report', 0]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def report_alive(self):
        self.__report__(['alive', 0], {})

    def __get_user_type_str__(self, userType):
        if userType == 0:
            return 'dev'
        if userType == 1:
            return 'mail'
        if userType == 2:
            return 'sns'
        if userType == 3:
            return 'mobile'
        return userType

    def user_register(self, gameId, userId, userType, clientId, clientIP, deviceId, *arglist, **argdict):
        userId = int(userId)
        if userId <= 10000:
            return

        key = 'count:user:new:' + self.__get_user_type_str__(userType) + ':' + str(
            gameId) + ':' + self.__get_current_day__()
        self.__ctx__.RedisBiCount.execute('SADD', key, userId)

        key = 'count:user:login:' + str(gameId) + ':' + self.__get_current_day__()
        self.__ctx__.RedisBiCount.execute('SADD', key, userId)

        alist = ['user_register', gameId, userId, userType, clientId, clientIP, deviceId]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def user_login(self, gameId, userId, userType, clientId, clientIP, deviceId, *arglist, **argdict):
        userId = int(userId)
        if userId <= 10000:
            return

        key = 'count:user:login:' + str(gameId) + ':' + self.__get_current_day__()
        self.__ctx__.RedisBiCount.execute('SADD', key, userId)

        alist = ['user_login', gameId, userId, userType, clientId, clientIP, deviceId]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def user_dev2reg(self, gameId, userId, clientId, clientIP, deviceId, *arglist, **argdict):
        userId = int(userId)
        if userId <= 10000:
            return

        key = 'count:user:dev2reg:' + str(gameId) + ':' + self.__get_current_day__()
        self.__ctx__.RedisBiCount.execute('SADD', key, userId)

        alist = ['user_dev2reg', gameId, userId, clientId, clientIP, deviceId]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def user_dev2sns(self, gameId, userId, clientId, clientIP, deviceId, *arglist, **argdict):
        userId = int(userId)
        if userId <= 10000:
            return

        key = 'count:user:dev2sns:' + str(gameId) + ':' + self.__get_current_day__()
        self.__ctx__.RedisBiCount.execute('SADD', key, userId)

        alist = ['user_dev2sns', gameId, userId, clientId, clientIP, deviceId]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def chip_update(self, gameId, userId, detalCount, finalCount, updateEventTag, *arglist, **argdict):
        alist = ['chip_update', gameId, userId, detalCount, finalCount, updateEventTag]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def tablechip_update(self, gameId, userId, detalCount, finalCount, updateEventTag, *arglist, **argdict):
        alist = ['tablechip_update', gameId, userId, detalCount, finalCount, updateEventTag]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def coupon_update(self, gameId, userId, detalCount, finalCount, updateEventTag, *arglist, **argdict):
        alist = ['coupon_update', gameId, userId, detalCount, finalCount, updateEventTag]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def coin_update(self, gameId, userId, detalCount, finalCount, updateEventTag, *arglist, **argdict):
        alist = ['coin_update', gameId, userId, detalCount, finalCount, updateEventTag]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def diamond_update(self, gameId, userId, detalCount, finalCount, updateEventTag, *arglist, **argdict):
        alist = ['diamond_update', gameId, userId, detalCount, finalCount, updateEventTag]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def item_update(self, gameId, userId, itemId, detalCount, finalCount, updateEventTag, *arglist, **argdict):
        alist = ['item_update', gameId, userId, itemId, detalCount, finalCount, updateEventTag]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def table_start(self, gameId, roomId, tableId, cardId, userIdList, *arglist, **argdict):
        alist = ['table_start', gameId, roomId, tableId, cardId, userIdList]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def table_card(self, gameId, roomId, tableId, cardId, userIdList, *arglist, **argdict):
        alist = ['table_card', gameId, roomId, tableId, cardId, userIdList]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def table_winlose(self, gameId, roomId, tableId, cardId, userIdList, *arglist, **argdict):
        alist = ['table_winlose', gameId, roomId, tableId, cardId, userIdList]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def tcp_user_online(self, userCount, *arglist, **argdict):

        rkey = self.__ctx__.GData.redis_fixhead_ + 'count:user:onlines'
        self.__ctx__.RedisBiCount.execute('HSET', rkey, str(self.__PROCESSID__), str(userCount))

        alist = ['tcp_user_online', 0, userCount]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def room_user_online(self, roomId, userCount, playTableCount, *arglist, **argdict):

        rkey = self.__ctx__.GData.redis_fixhead_ + 'count:room:onlines'
        self.__ctx__.RedisBiCount.execute('HSET', rkey, str(roomId), str(userCount) + '|' + str(playTableCount))

        alist = ['room_user_online', 0, roomId, userCount, playTableCount]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def gcoin(self, coinKey, gameId, detalCount, *arglist, **argdict):

        rkey = str(gameId) + ':' + self.__get_current_day__()
        leftCount = self.__ctx__.RedisBiCount.execute('HINCRBY', 'GCOIN:' + rkey, coinKey, detalCount)

        alist = ['gcoin', gameId, detalCount, leftCount, rkey, coinKey]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def creat_game_data(self, gameId, userId, clientId, dataKeys, dataValues, *arglist, **argdict):
        alist = ['creat_game_data', gameId, userId, clientId, dataKeys, dataValues]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def table_room_fee(self, gameId, fees, *arglist, **argdict):
        alist = ['table_room_fee', gameId, fees]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def user_bind_game(self, gameId, userId, clientId, *arglist, **argdict):
        alist = ['bind_game', gameId, userId, clientId]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def user_bind_user(self, gameId, userId, clientId, *arglist, **argdict):
        alist = ['bind_user', gameId, userId, clientId]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def table_event(self, gameId, roomId, tableId, event, *arglist, **argdict):
        alist = ['table_event', gameId, roomId, tableId, event]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def player_event(self, gameId, userId, roomId, tableId, event, *arglist, **argdict):
        alist = ['player_event', gameId, userId, roomId, tableId, event]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def match_start(self, gameId, roomId, matchId, matchName, *arglist, **argdict):
        alist = ['match_start', gameId, roomId, matchId, matchName]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def match_finish(self, gameId, roomId, matchId, matchName, *arglist, **argdict):
        alist = ['match_finish', gameId, roomId, matchId, matchName]
        alist.extend(arglist)
        self.__report__(alist, argdict)

    def _init_bicollects_(self):
        biservers = self.__ctx__.TYGlobal.bicollect_server()
        for key, val in biservers.items():
            master = val['master']
            slave = val.get('slave', None)
            bisrv = []
            bisrv.append({'host': master['host'], 'port': master['port'], 'cluster': master['cluster']})
            if slave:
                bisrv.append({'host': slave['host'], 'port': slave['port'], 'cluster': slave['cluster']})
            self.__bicollects__[key] = bisrv

    def get_bi_rec_id(self, user_id, rec_type):
        '''
        取得一个BI统计类型的唯一自增ID
        rec_type, 记录的大分类,目前已知有: chip_update, coin_update, diamond_update, login_update
        '''
        assert (isinstance(user_id, int) and user_id > 0)
        assert (rec_type in self.__bicollects__)
        cluster = self.__bicollects__[rec_type][0]['cluster']
        rkey = 'global.bicollect.%s.%d' % (rec_type, (user_id % cluster))
        recid = self.__ctx__.RedisBiCount.execute('INCR', rkey)
        return long(recid)

    def report_bi(self, user_id, rec_type, struct_fmt, *struct_args):
        '''
        发送BI消息到BICOLLECT服务
        user_id 消息产生的用户ID, 必须是有效的正整数
        rec_type 消息的基本大类型, 目前已知有: chip_update, coin_update, diamond_update, login_update
        struct_fmt 消息的具体格式, struct的格式化格式
        struct_args 消息的参数, 即:struct.pack使用的参数
        注意: 本函数自动会在struct_fmt之前添加基本消息头"4cqi", 即: "msg:",消息的系统唯一ID,当前的时间
        '''
        recid = self.get_bi_rec_id(user_id, rec_type)
        struct_fmt = '<QI' + struct_fmt
        #         self.__ctx__.ftlog.debug('send bi udp->[', struct_fmt, recid, int(time.time()), struct_args, ']')
        data = 'msg:' + struct.pack(struct_fmt, recid, int(time.time()), *struct_args)
        #         biservers = self.__bicollects__[rec_type]
        #         cluster = biservers[0]['cluster']
        #         transport = self.__ctx__.getTasklet().gdata.udpClient.transport
        #         for biserver in biservers :
        #             host = biserver['host']
        #             biport = biserver['port']
        #             port = biport + (user_id % cluster) * 100 + (user_id / cluster) % cluster
        #             self.__ctx__.ftlog.debug('send bi udp->', (host, port), '[', repr(data), ']')
        #             transport.write(data, (host, port))
        try:
            from tyframework._private_.bi import bireport_http
            bireport_http.report_bi_http(user_id, rec_type, data)
        except:
            self.__ctx__.ftlog.exception()

    def report_bi_chip_update(self, user_id, delta, trueDelta, final, eventId,
                              clientId, gameId, appId, eventParam, chipType):
        # fmt = "4c Q I I q q q I I H H I B"
        #         | | | | | | | | | | | | └-- chipType 金币类型 1 CHIP 2 TABLECHIP 3 COIN 4 DIAMOND 5 COUPON
        #         | | | | | | | | | | | └-- eventParam 事件的参数
        #         | | | | | | | | | | └- appId 客户端登录时产生的appId
        #         | | | | | | | | | └- gameId 后端服务操作时使用的gameId
        #         | | | | | | | | └- clientId 客户端终端的ID
        #         | | | | | | | └- eventId 事件ID
        #         | | | | | | └- final 最终的数量
        #         | | | | | └- trueDelta 实际变化的数量
        #         | | | | └- delta 期望发生的数量
        #         | | | └- userId 事件产生的用户
        #         | | └- eventTime 当前的记录时间
        #         | └- recid 当前的记录ID
        #         └- "msg:" (固定)
        self.__ctx__.ftlog.debug('report_bi_chip_update->', user_id, delta, trueDelta, final, eventId,
                                 clientId, gameId, appId, eventParam, chipType)
        _, clientId = self.__ctx__.BiUtils.getClientIdNum(clientId, None, gameId, user_id)
        assert (isinstance(user_id, (int, long)))
        assert (isinstance(delta, (int, long)))
        assert (isinstance(trueDelta, (int, long)))
        assert (isinstance(final, (int, long)))
        assert (isinstance(eventId, (int, long)))
        assert (isinstance(clientId, (int, long)))
        assert (isinstance(gameId, (int, long)))
        assert (isinstance(appId, (int, long)))
        assert (isinstance(eventParam, (int, long)))
        assert (isinstance(chipType, (int, long)))
        return self.report_bi(user_id, 'chip_update', 'IqqqIIHHIB',
                              user_id, delta, trueDelta, final, eventId,
                              clientId, gameId, appId, eventParam, chipType)

    '''
    字段定义：event_type(4)|tyid(4)|gameid(2)|appid(2)|clientid(4)|ipaddr(4)|devid(32)|bindid(40)|phonetype(1)|province(1)|fail_reason(2)|reserved(?)
    总长度：128字节 使用长度：112字节 预留长度：?字节
    '''

    def report_bi_sdk_login(self, eventId, user_id, appId, clientId, bindId, fail_reason, devId=None):
        # fmt = "I I H H I I 32s 40s B B H"
        #        | | | | | |   |   | | | └- fail_reason
        #        | | | | | |   |   | | └- province
        #        | | | | | |   |   | └- phonetype
        #        | | | | | |   |   └- bindid
        #        | | | | | |   └- devid
        #        | | | | | └- ipAddr
        #        | | | | └- clientId 客户端终端的ID
        #        | | | └- appId 客户端登录时产生的appId
        #        | | └- gameId 后端服务操作时使用的gameId
        #        | └- userId 事件产生的用户
        #        └- eventId 事件ID
        user_id = int(user_id)
        appId = int(appId)
        gameId = self.__ctx__.Const.SDK_GAMEID
        from tyframework.context import TyContext
        _, clientId = self.__ctx__.BiUtils.getClientIdNum(clientId, None, gameId, user_id)
        if user_id:
            if not devId:
                devId = TyContext.UserSession.get_session_deviceid(user_id)
            phoneType = TyContext.UserSession.get_session_phone_type(user_id)
        else:
            devId = ''
            phoneType = 3
        ipAddrs = TyContext.RunHttp.get_client_ip()
        prov, _ = TyContext.UserSession.get_session_zipcode(user_id, client_ip=ipAddrs)
        province = prov / 10000 if prov != 1 else prov
        ipAddr = TyContext.IPAddress(ipAddrs)._ip
        assert (isinstance(eventId, (int, long)))
        assert (isinstance(user_id, (int, long)))
        assert (isinstance(gameId, (int, long)))
        assert (isinstance(appId, (int, long)))
        assert (isinstance(clientId, (int, long)))
        assert (isinstance(ipAddr, (int, long)))
        assert (isinstance(devId, basestring))
        assert (isinstance(bindId, basestring))
        assert (isinstance(phoneType, (int, long)))
        assert (isinstance(province, (int, long)))
        assert (isinstance(fail_reason, (int, long)))
        self.__ctx__.ftlog.debug('report_bi_sdk_login->', eventId, user_id, gameId,
                                 appId, clientId, ipAddr, devId, bindId, phoneType,
                                 province, fail_reason)
        self.__ctx__.ftlog.info('sdk_login_userip', user_id, ipAddrs)
        return self.report_bi(user_id, 'sdk_login', 'IIHHII32s40sBBH', eventId,
                              user_id, gameId, appId, clientId, ipAddr,
                              devId, bindId, phoneType, province, fail_reason)

    def report_bi_sdk_buy(self, eventid, userid, appid, clientid,
                          orderid, shortid='', deliver_orderid='',
                          prodid=0, diamondid=0, sub_event=0, prod_price=0,
                          charge_price=0, succ_price=0, paytype=0, sub_paytype='',
                          third_prodid='', third_orderid='', third_appid='',
                          ipaddr=0, mobile='', phonetype=3, province=1):
        '''
        字段定义：
        eventid(4)|tyid(4)|gameid(2)|appid(2)|clientid(4)|
        orderid(14)|shortid(6)|deliver_orderid(25)|prodid(2)|diamondid(2)|
        sub_event(1)|prod_price(4)|charge_price(4)|succ_price(4)|
        paytype(2)|sub_paytype(10)|
        third_prodid(32)|third_orderid(32)|third_appid(32)|
        ipaddr(4)|mobile(11)|phonetype(1)|province(1)
        这些字段总长度：203字节
        各字段释义：
        event_type: 支付事件。与其他event统一编码，占4字节。
            CREATE
            CLIENT_FINISHED
            CLIENT_CANCELED
            REQUEST_OK
            REQUEST_RETRY
            REQUEST_ERROR
            CALLBACK_OK
            CALLBACK_FAIL
            DELIVER_OK
            DELIVER_FAIL
            INTERNAL_ERR
        tyid: userid
        gameid: gameid (998 for SDK)
        appid: application id (e.g. 6 for 地主)
        clientid: clientid as a number，统一编码为2 bytes整形
        orderid: platformOrderid, 支付订单后，14位长字符串
        shortid: 某些情况下由orderid转换而成的6位长的短订单号
        deliver_orderid: 由发货系统生成的发货单号
        prodid: 商品ID，统一编码
        diamondid: 钻石ID，与商品统一编码
        sub_event: 子事件。可有可无。有的时候表示对应event_type的子事件。
                如event_type为CLIENT_CANCEL时，它表示取消的具体原因。
                又如event_type为INTERNAL_ERR时，它表示错误的具体原因。
                具体编码数值待定。
        prod_price: 商品标价，单位：钻石数
        charge_price: 充值金额，单位：元
        succ_price: 成功金额，单位：元
        paytype: 支付方式。统一编码为2 bytes整形
        sub_paytype: 子支付类型。对应支付方式有子支付方式的情况。
                    如使用小米支付有银行卡、充值卡等不同的子支付方式。暂定10字节字符串。
        third_prodid: 第三方所定义的商品ID，暂定32位字符串。用于对账。
        third_orderid: 第三方流水号，暂定32位字符串。用于对账。
        third_appid: 第三方应用ID，暂定32位字符串。用于分应用统计与对账。
        ipaddr: 4位IP地址
        mobile: 11位手机号码
        phonetype: 1位运营商类别（0/1/2分别表示移动、联通、电信)
        province: 1位省份编码（邮政编码最高2位）
        '''
        # fmt = "I I H H I 14s 6s 25s H H B I f f H 10s 32s 32s 32s I 11s B B"
        #        | | | | | |   |   |  | | | | | | |   |   |   |   | |   | | |
        #        | | | | | |   |   |  | | | | | | |   |   |   |   | |   | | └- province
        #        | | | | | |   |   |  | | | | | | |   |   |   |   | |   | └- phonetype
        #        | | | | | |   |   |  | | | | | | |   |   |   |   | |   └- mobile
        #        | | | | | |   |   |  | | | | | | |   |   |   |   | └- ipaddr
        #        | | | | | |   |   |  | | | | | | |   |   |   |   └- third_appid
        #        | | | | | |   |   |  | | | | | | |   |   |   └- third_orderid
        #        | | | | | |   |   |  | | | | | | |   |   └- third_prodid
        #        | | | | | |   |   |  | | | | | | |   └- sub_paytype
        #        | | | | | |   |   |  | | | | | | └- paytype
        #        | | | | | |   |   |  | | | | | └- succ_price
        #        | | | | | |   |   |  | | | | └- charge_price
        #        | | | | | |   |   |  | | | └- prod_price
        #        | | | | | |   |   |  | | └- sub_event
        #        | | | | | |   |   |  | └- diamondid
        #        | | | | | |   |   |  └- prodid
        #        | | | | | |   |   └- deliver_orderid
        #        | | | | | |   └- shortid
        #        | | | | | └- orderid
        #        | | | | └- clientId 客户端终端的ID
        #        | | | └- appId 客户端登录时产生的appId
        #        | | └- gameId 后端服务操作时使用的gameId
        #        | └- userId 事件产生的用户
        #        └- eventId 事件ID
        self.__ctx__.ftlog.debug(
            'report_bi_sdk_buy->', eventid, userid, appid, clientid, orderid,
            shortid, deliver_orderid, prodid, diamondid, sub_event,
            prod_price, charge_price, succ_price, paytype, sub_paytype,
            third_prodid, third_orderid, third_appid,
            ipaddr, mobile, phonetype, province)
        userid = int(userid)
        appid = int(appid)
        gameid = self.__ctx__.Const.SDK_GAMEID
        from tyframework.context import TyContext
        _, clientid = self.__ctx__.BiUtils.getClientIdNum(clientid, None, appid, userid)
        ip = TyContext.IPAddress(ipaddr)._ip
        prov = province / 10000 if province != 1 else province
        if prodid:
            prodid = self.__ctx__.BiUtils.productIdToNumber(appid, prodid)
        else:
            prodid = 0
        if diamondid:
            diamondid = self.__ctx__.BiUtils.productIdToNumber(gameid, diamondid)
        else:
            diamondid = 0
        assert (isinstance(eventid, (int, long)))
        assert (isinstance(userid, (int, long)))
        assert (isinstance(gameid, (int, long)))
        assert (isinstance(appid, (int, long)))
        assert (isinstance(clientid, (int, long)))
        assert (isinstance(orderid, basestring))
        assert (isinstance(shortid, basestring))
        assert (isinstance(deliver_orderid, basestring))
        assert (isinstance(prodid, (int, long)))
        assert (isinstance(diamondid, (int, long)))
        assert (isinstance(sub_event, (int, long)))
        assert (isinstance(prod_price, (int, long)))
        assert (isinstance(charge_price, (float, int, long)))
        assert (isinstance(succ_price, (float, int, long)))
        assert (isinstance(paytype, (int, long)))
        assert (isinstance(sub_paytype, basestring))
        assert (isinstance(third_prodid, basestring))
        assert (isinstance(third_orderid, basestring))
        assert (isinstance(third_appid, basestring))
        assert (isinstance(ip, (int, long)))
        assert (isinstance(mobile, basestring))
        assert (isinstance(prov, (int, long)))
        assert (isinstance(phonetype, (int, long)))
        return self.report_bi(
            userid, 'sdk_buy', 'IIHHI14s6s25sHHBIffH10s32s32s32sI11sBB', eventid,
            userid, gameid, appid, clientid, orderid, shortid, deliver_orderid,
            prodid, diamondid, sub_event, prod_price, charge_price, succ_price,
            paytype, sub_paytype, third_prodid, third_orderid, third_appid,
            ip, mobile, phonetype, prov)

    def report_game_event(self, eventId, user_id, gameId, roomId, tableId, roundId, detalChip, state1, state2, cardlist,
                          clientId, finalTableChip=0, finalUserChip=0):
        # fmt = "I I H I Q Q I q q q B B 20B"
        #        | | | | | | | | | | | | | 
        #        | | | | | | | | | | | | └- cardlist 当前事件操作的牌, 数字(0~54), 0xFF为无效
        #        | | | | | | | | | | | └- state2 当前事件操作的状态2(例如:托管,超时)
        #        | | | | | | | | | | └- state1 当前事件操作的状态1(例如:托管,超时)
        #        | | | | | | | | | └- finalUserChip 当前事件用户的最终所有金币数量
        #        | | | | | | | | └- finalTableChip 当前事件用户的最终桌子金币数量 
        #        | | | | | | | └- detalChip 当前事件操作涉及的金币数量
        #        | | | | | | └- roundId 当前事件的游戏局ID(如果为比赛事件,即为比赛的ID, 如果为普通牌桌,即为牌局ID或时间戳) 
        #        | | | | | └- tableId 游戏事件发生的房间桌子ID
        #        | | | | └- roomId 游戏事件发生的房间
        #        | | | └- clientId 客户端的clientId
        #        | | └- gameId 后端服务操作时使用的gameId
        #        | └- userId 事件产生的用户
        #        └- eventId 事件ID
        user_id = int(user_id)
        gameId = int(gameId)
        _, clientId = self.__ctx__.BiUtils.getClientIdNum(clientId, None, gameId, user_id)
        assert (isinstance(eventId, (int, long)))
        assert (isinstance(user_id, (int, long)))
        assert (isinstance(gameId, (int, long)))
        assert (isinstance(roomId, (int, long)))
        assert (isinstance(tableId, (int, long)))
        assert (isinstance(roundId, (int, long)))
        assert (isinstance(detalChip, (int, long)))
        assert (isinstance(state1, (int, long)))
        assert (isinstance(state2, (int, long)))
        assert (isinstance(clientId, (int, long)))
        assert (isinstance(finalUserChip, (int, long)))
        assert (isinstance(finalTableChip, (int, long)))
        cards = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        if cardlist:
            for x in xrange(min(20, len(cardlist))):
                cards[x] = int(cardlist[x])
        if eventId == self.__ctx__.BIEventId.TABLE_CARD:
            targed = 'card'
        else:
            targed = 'game'
        self.__ctx__.ftlog.debug('report_game_evnet->', eventId, user_id, gameId, roomId, tableId, roundId, state1,
                                 state2, clientId, cards)
        return self.report_bi(user_id, targed, 'IIHIQQIqqq22B', eventId,
                              user_id, gameId, clientId, roomId,
                              tableId, roundId, detalChip, finalTableChip, finalUserChip, state1, state2, *cards)


BiReport = BiReport()
