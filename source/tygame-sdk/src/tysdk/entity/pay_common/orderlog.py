# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class Order(object):
    CREATE = 'CREATE'
    CLIENT_FINISHED = 'CLIENT_FINISHED'
    CLIENT_CANCELED = 'CLIENT_CANCELED'
    REQUEST_OK = 'REQUEST_OK'
    REQUEST_RETRY = 'REQUEST_RETRY'
    REQUEST_ERROR = 'REQUEST_ERROR'
    CALLBACK_OK = 'CALLBACK_OK'
    CALLBACK_FAIL = 'CALLBACK_FAIL'
    DELIVER_OK = 'DELIVER_OK'
    DELIVER_FAIL = 'DELIVER_FAIL'
    INTERNAL_ERR = 'INTERNAL_ERR'
    SUBSCRIBE = 'SUBSCRIBE'
    UNSUBSCRIBE = 'UNSUBSCRIBE'
    UNSUBSCRIBE_TMP = 'UNSUBSCRIBE_TMP'
    RENEW_SUBSCRIBE = 'RENEW_SUBSCRIBE'
    OUTOFSERVICE = 'OUTOFSERVICE'

    eventid = {
        CREATE: TyContext.BIEventId.SDK_BUY_CREATE,
        CLIENT_FINISHED: TyContext.BIEventId.SDK_BUY_CLIENT_FINISHED,
        CLIENT_CANCELED: TyContext.BIEventId.SDK_BUY_CLIENT_CANCELED,
        REQUEST_OK: TyContext.BIEventId.SDK_BUY_REQUEST_OK,
        REQUEST_RETRY: TyContext.BIEventId.SDK_BUY_REQUEST_RETRY,
        REQUEST_ERROR: TyContext.BIEventId.SDK_BUY_REQUEST_ERROR,
        CALLBACK_OK: TyContext.BIEventId.SDK_BUY_CALLBACK_OK,
        CALLBACK_FAIL: TyContext.BIEventId.SDK_BUY_CALLBACK_FAIL,
        DELIVER_OK: TyContext.BIEventId.SDK_BUY_DELIVER_OK,
        DELIVER_FAIL: TyContext.BIEventId.SDK_BUY_DELIVER_FAIL,
        INTERNAL_ERR: TyContext.BIEventId.SDK_BUY_INTERNAL_ERR,
        SUBSCRIBE: TyContext.BIEventId.SDK_SUBSCRIBE_MONTHLY_VIP,
        UNSUBSCRIBE_TMP: TyContext.BIEventId.SDK_UNSUBSCRIBE_MONTHLY_VIP_TEMP,
        UNSUBSCRIBE: TyContext.BIEventId.SDK_UNSUBSCRIBE_MONTHLY_VIP,
        RENEW_SUBSCRIBE: TyContext.BIEventId.SDK_RENEW_SUBSCRIBE_MONTHLY_VIP,
        OUTOFSERVICE: TyContext.BIEventId.SDK_MOBILE_OUT_OF_SERVEICE,
    }

    @classmethod
    def log(cls, platformOrderId, event, userId, gameId, clientId,
            info='na', subevent='na',
            shortId='na', prodOrderId='na', prodid='na', diamondid='na',
            prod_price='na', charge_price='na', succ_price='na',
            paytype='na', sub_paytype='na', third_prodid='na', third_orderid='na',
            pay_appid='na', mobile='na', third_userid='na', third_provid='na'):
        '''前五个为positional argument，必须带
        后面的为keyword argument，可选，不带时缺省值是na
        prod_price 商品价格，单位：钻石
        charge_price 充值金额，单位：元
        succ_price 成功支付金额。单位：元。如果三方回调里没有带此参数，其值为-1
        '''
        phonetype = TyContext.UserSession.get_session_phone_type(userId)
        # mobile = TyContext.UserSession.get_session_mobile(userId)
        # if not mobile:
        #    mobile = 'na'
        iccid = TyContext.UserSession.get_session_iccid(userId)
        if not iccid:
            iccid = 'na'
        lbs = TyContext.UserSession.get_session_city_zip(userId)
        ip = TyContext.UserSession.get_session_client_ip(userId)
        if not ip:
            ip = 'na'
        # sometimes ip got 'ip port'
        ip = ip.split(' ')[0]
        zipcode, by = TyContext.UserSession.get_session_zipcode(userId)
        if isinstance(info, basestring):
            try:
                info = info.encode('utf-8')
            except:
                info = repr(info)
        # 去掉字符串中的换行和空格
        info = '#'.join([f.strip() for f in info.splitlines()])
        info = info.replace(' ', '_')
        clientId = '#'.join([f.strip() for f in clientId.splitlines()])
        clientId = clientId.replace(' ', '_')
        if not prodid:
            prodid = 'na'
        if not paytype:
            paytype = 'na'
        # 参数顺序固定，不允许变化，如需加入新参数，都往后加
        TyContext.ftlog.info(
            'OrderLog', platformOrderId, event, userId, gameId, clientId, info,
            shortId, prodOrderId, prodid, diamondid,
            phonetype, mobile, iccid, lbs, ip, zipcode, by,
            prod_price, charge_price, succ_price, paytype, sub_paytype,
            third_prodid, third_orderid, subevent, pay_appid,
            third_provid, third_userid)

        try:
            cls._bi_log(platformOrderId, event, userId, gameId, clientId,
                        info, subevent, mobile, phonetype, zipcode, ip,
                        shortId, prodOrderId, prodid, diamondid,
                        prod_price, charge_price, succ_price,
                        paytype, sub_paytype, third_prodid, third_orderid,
                        pay_appid)
        except:
            TyContext.ftlog.exception()

    @classmethod
    def _bi_log(cls, platformOrderId, event, userId, gameId, clientId,
                info, subevent, mobile, phonetype, zipcode, ip,
                shortId, prodOrderId, prodid, diamondid,
                prod_price, charge_price, succ_price,
                paytype, sub_paytype, third_prodid, third_orderid,
                pay_appid):
        if gameId == 'na':
            gameId = 0
        # if int(gameId) > 10000:
        #     return
        paytype_codes = TyContext.Configure.get_global_item_json('paytype.number.map')
        try:
            paytype_code = paytype_codes[paytype]
        except:
            TyContext.ftlog.exception()
            paytype_code = 0

        shortId = '' if shortId == 'na' else shortId
        prodOrderId = '' if prodOrderId == 'na' else prodOrderId
        subevent = 0 if subevent == 'na' else int(subevent)
        sub_paytype = '' if sub_paytype == 'na' else str(sub_paytype)
        prod_price = 0 if prod_price == 'na' else int(float(prod_price))
        charge_price = 0.0 if charge_price == 'na' else float(charge_price)
        succ_price = 0.0 if succ_price == 'na' else float(succ_price)
        third_prodid = '' if third_prodid == 'na' else third_prodid
        third_orderid = '' if third_orderid == 'na' else third_orderid
        pay_appid = '' if pay_appid == 'na' else pay_appid
        ip = 0 if ip == 'na' else ip
        mobile = '' if mobile == 'na' else mobile
        phonetype = 0 if phonetype == 'na' else phonetype
        zipcode = 0 if zipcode == 'na' else zipcode
        diamondid = diamondid if diamondid != 'na' else None
        prodid = prodid if prodid != 'na' else None

        TyContext.BiReport.report_bi_sdk_buy(
            Order.eventid[event], userId, gameId, clientId,
            platformOrderId, shortId, prodOrderId,
            prodid, diamondid, subevent,
            prod_price, charge_price, succ_price,
            paytype_code, sub_paytype,
            third_prodid, third_orderid, pay_appid,
            ip, mobile, phonetype, zipcode)

    @classmethod
    def get_pay_appid(cls, paytype, payinfo, clientId):
        TyContext.ftlog.debug('get_pay_appid args', paytype, payinfo, clientId)
        try:
            return payinfo['appid'][paytype]
        except:
            pass
        pay_appid_config = TyContext.Configure.get_global_item_json('pay_appid_config')
        TyContext.ftlog.debug('get_pay_appid pay_appid_config', pay_appid_config)
        try:
            return pay_appid_config[clientId][paytype]
        except:
            pass
        return 'na'
