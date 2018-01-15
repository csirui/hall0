# -*- coding=utf-8 -*-
from hashlib import md5

import datetime
import json

from tyframework.context import TyContext


class TuYouPayAiGame():
    XML_CHECK_RET = '''<?xml version="1.0" encoding="UTF-8"?>
<sms_pay_check_resp>
    <cp_order_id>%s</cp_order_id>
    <correlator>%s</correlator>
    <game_account>%s</game_account>
    <fee>%s</fee>
    <if_pay>%s</if_pay>
    <order_time>%s</order_time>
</sms_pay_check_resp>
'''
    XML_RET = '''<?xml version="1.0" encoding="UTF-8"?>
<cp_notify_resp>
    <h_ret>%s</h_ret>
    <cp_order_id>%s</cp_order_id>
</cp_notify_resp>
'''

    @classmethod
    def _get_order_info(self, orderPlatformId):
        appInfo = {}
        try:
            TyContext.RunMode.get_server_link(orderPlatformId)
            baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'PAY_STATE_IDEL')
            baseinfo = json.loads(baseinfo)
            if 'uid' in baseinfo and baseinfo['uid'] != None:
                appInfo['uid'] = baseinfo['uid']
            if 'orderPrice' in baseinfo and baseinfo['orderPrice'] != None:
                appInfo['orderPrice'] = baseinfo['orderPrice']
            if 'appId' in baseinfo and baseinfo['appId'] != None:
                appInfo['appId'] = baseinfo['appId']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doAiGameMsgCallback->_get_order_info error', 'orderPlatformId=', orderPlatformId)
            return appInfo

        # ftlog.info('doAiGameMsgCallback->_get_order_info', 'appInfo=',appInfo)
        return appInfo

    @classmethod
    def doAiGameMsgCallback(self, rpath):
        notifys = TyContext.RunHttp.convertArgsToDict()
        cpparam = notifys.get('cpparam', '')
        if not cpparam:
            appkeys = '62d55e5d5d47f5d0121d2049d6893bc1'
            return self._doAiGameMsgCallbackNew(appkeys, rpath)

        resultcode = notifys.get('resultCode', '')
        resultmsg = notifys.get('resultMsg', '')
        try:
            order_paytype = notifys['payType']
            del notifys['payType']
            notifys['sub_paytype'] = order_paytype
        except:
            order_paytype = ''
        validatecode = notifys.get('validatecode', '')

        # 限制ip请求
        # clientIp = TyContext.RunHttp.get_client_ip()
        # TyContext.ftlog.info('TuYouPayAiGame.doAiGameMsgCallback in clientIp=', clientIp)
        # iplist = clientIp.split('.')
        # if len(iplist) != 4 or iplist[0] != '202' or iplist[1] != '102' or iplist[2] != '39' :
        #    return cpparam

        if resultcode == '' or resultmsg == '' or cpparam == '' or order_paytype != 'isagSmsPay' or validatecode == '':
            return TuYouPayAiGame.XML_RET % ('1', cpparam)

        tSign = resultcode + cpparam
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if validatecode != vSign:
            TyContext.ftlog.info('TuYouPayAiGame.__doAiGameMsgCallbackOld__->ERROR, sign error !! sign=', validatecode,
                                 'vSign=', vSign)
            return TuYouPayAiGame.XML_RET % ('1', cpparam)

        # 解密得到原始游戏订单号
        orderPlatformId = cpparam
        TyContext.ftlog.info('TuYouPayAiGame.__doAiGameMsgCallbackOld__ orderPlatformId=', orderPlatformId)
        if resultcode == '00':
            from tysdk.entity.pay.pay import TuyouPay
            TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', notifys)

        return TuYouPayAiGame.XML_RET % ('0', cpparam)

    @classmethod
    def doAiGameCallbackDizhuHappy(self, rpath):
        appkeys = '89df51ef2ece07a06ed513d4c522266f'
        return self._doAiGameMsgCallbackNew(appkeys, rpath)

    '''
    @classmethod
    def doAiGameCallbackDizhuDanji(self, rpath):
        appkeys = '62d55e5d5d47f5d0121d2049d6893bc1'
        return self._doAiGameMsgCallbackNew(appkeys, rpath)
    '''

    @classmethod
    def doAiGameCallbackDizhuHuabei(self, rpath):
        appkeys = '6be1b0234b18b0e09188abb4e2429454'
        return self._doAiGameMsgCallbackNew(appkeys, rpath)

    @classmethod
    def doAiGameCallbackDizhuStarZszhWF(self, rpath):
        appkeys = '7978406bb21b362065e9588cecd5d8d1'
        return self._doAiGameMsgCallbackNew(appkeys, rpath)

    @classmethod
    def doAiGameCallbackDizhuStarZszhPT(self, rpath):
        appkeys = '9bff05ca361095c5727d7e7b2946b516'
        return self._doAiGameMsgCallbackNew(appkeys, rpath)

    @classmethod
    def _get_appkey(cls, gamecode):
        try:
            extdata = TyContext.PayType.get_pay_type_ext_datas('aigame')
            if extdata is not None:
                appkeys = extdata.get('appkeys', {})
                appkey = appkeys.get(gamecode, None)
                if appkey is not None:
                    return appkey
        except:
            TyContext.ftlog.exception()
            return None

    @classmethod
    def doAiGameAllCallback(cls, rpath):
        notifys = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('doAiGameAllCallback->param=', notifys)

        cpparam = notifys.get('cpparam', '')
        if cpparam:
            return cls.doAiGameMsgCallback(rpath)

        cp_order_id = notifys.get('cp_order_id', '')
        gamecode = notifys.get('game_code', '')
        appkey = cls._get_appkey(gamecode)
        if appkey is None:
            TyContext.ftlog.error('doAiGameAllCallback->no appkey configured'
                                  ' for game_code', gamecode)
            return TuYouPayAiGame.XML_RET % ('1', cp_order_id)
        return cls._do_all_callback(appkey, notifys)

    @classmethod
    def _doAiGameMsgCallbackNew(cls, appkey, rpath):
        notifys = TyContext.RunHttp.convertArgsToDict()
        return cls._do_all_callback(appkey, notifys)

    @classmethod
    def _do_all_callback(self, appkey, notifys):
        method = TyContext.RunHttp.getRequestParam('method', '')
        cp_order_id = TyContext.RunHttp.getRequestParam('cp_order_id', '')
        correlator = TyContext.RunHttp.getRequestParam('correlator', '')
        order_time = TyContext.RunHttp.getRequestParam('order_time', '')
        sign = TyContext.RunHttp.getRequestParam('sign', '')
        if method == 'check':
            # 订单效验接口
            game_account = ''
            game_fee = ''
            ct = datetime.datetime.now()
            order_current_time = ct.strftime('%Y%m%d%H%M%S')
            if cp_order_id == '' or sign == '':
                return TuYouPayAiGame.XML_CHECK_RET % (
                cp_order_id, correlator, game_account, game_fee, '1', order_current_time)

            orderPlatformId = cp_order_id
            appInfo = self._get_order_info(orderPlatformId)
            if 'uid' in appInfo and appInfo['uid'] != None:
                game_account = appInfo['uid']
            if 'orderPrice' in appInfo and appInfo['orderPrice'] != None:
                game_fee = appInfo['orderPrice']

            tSign = cp_order_id + str(correlator) + str(order_time) + method + appkey
            m = md5()
            m.update(tSign)
            vSign = m.hexdigest()
            if sign != vSign:
                TyContext.ftlog.info('TuYouPayAiGame._doAiGameMsgCallbackNew->ERROR, sign error !! sign=', sign,
                                     'vSign=', vSign)
                return TuYouPayAiGame.XML_CHECK_RET % (
                cp_order_id, correlator, game_account, game_fee, '1', order_current_time)

            return TuYouPayAiGame.XML_CHECK_RET % (
            cp_order_id, correlator, game_account, game_fee, '0', order_current_time)
        else:
            # 成功回调接口
            result_code = TyContext.RunHttp.getRequestParam('result_code', '')
            fee = TyContext.RunHttp.getRequestParam('fee', '')
            pay_type = TyContext.RunHttp.getRequestParam('pay_type', '')
            game_code = notifys.get('game_code')
            try:
                fee = int(fee)
            except:
                TyContext.ftlog.exception()
                fee = -1

            ct = datetime.datetime.now()
            order_current_time = ct.strftime('%Y%m%d%H%M%S')
            if cp_order_id == '' or sign == '' or method != 'callback':
                return TuYouPayAiGame.XML_RET % ('1', cp_order_id)

            orderPlatformId = cp_order_id
            tSign = cp_order_id + str(correlator) + str(result_code) + str(fee) + pay_type + method + appkey
            m = md5()
            m.update(tSign)
            vSign = m.hexdigest()
            if sign != vSign:
                TyContext.ftlog.info('TuYouPayAiGame._doAiGameMsgCallbackNew->ERROR, sign error !! sign=', sign,
                                     'vSign=', vSign)
                return TuYouPayAiGame.XML_RET % ('1', cp_order_id)

            if pay_type:
                notifys['sub_paytype'] = pay_type
            if correlator:
                notifys['third_orderid'] = correlator
            if game_code:
                notifys['pay_appid'] = game_code
            if str(result_code) == '00':
                from tysdk.entity.pay.pay import TuyouPay
                isOk = TuyouPay.doBuyChargeCallback(
                    orderPlatformId, fee, 'TRADE_FINISHED', notifys)
                if isOk:
                    retXml = TuYouPayAiGame.XML_RET % ('0', cp_order_id)
                else:
                    retXml = TuYouPayAiGame.XML_RET % ('1', cp_order_id)
            else:
                retXml = TuYouPayAiGame.XML_RET % ('1', cp_order_id)

            return retXml

    @classmethod
    def doAiGameCallback(self, rpath):

        serialno = TyContext.RunHttp.getRequestParam('serialno', '')
        resultcode = TyContext.RunHttp.getRequestParam('resultCode', '')
        resultmsg = TyContext.RunHttp.getRequestParam('resultMsg', '')
        gameUserId = TyContext.RunHttp.getRequestParam('gameUserId', '')
        # gameGold = TyContext.RunHttp.getRequestParam('gameGold', 0)
        order_paytype = TyContext.RunHttp.getRequestParam('payType', '')
        validatecode = TyContext.RunHttp.getRequestParam('validatecode', '')
        # requestTime = TyContext.RunHttp.getRequestParam('requestTime', '')

        # 限制ip请求
        # clientIp = TyContext.RunHttp.get_client_ip()
        # TyContext.ftlog.info('TuYouPayAiGame.doAiGameCallback in clientIp=', clientIp)
        # iplist = clientIp.split('.')
        # if len(iplist) != 4 or iplist[0] != '202' or iplist[1] != '102' or iplist[2] != '39' :
        #    return serialno

        if serialno == '' or resultcode == '' or resultmsg == '' or gameUserId == '' or order_paytype == '' or validatecode == '':
            return serialno

        tSign = serialno + gameUserId
        m = md5()
        m.update(tSign)
        vSign = m.hexdigest()
        if validatecode != vSign:
            TyContext.ftlog.info('TuYouPayAiGame.doAiGameCallback->ERROR, sign error !! sign=', validatecode, 'vSign=',
                                 vSign)
            return serialno

        # 解密得到原始游戏订单号
        orderPlatformId = gameUserId

        TyContext.ftlog.info('TuYouPayAiGame.doAiGameCallback orderPlatformId=', orderPlatformId)
        if resultcode == '120':
            #             if int(gameGold) == 0:
            #                 total_fee = -1
            #             else:
            #                 total_fee = int(gameGold)

            from tysdk.entity.pay.pay import TuyouPay
            TuyouPay.doBuyChargeCallback(orderPlatformId, -1, 'TRADE_FINISHED', TyContext.RunHttp.convertArgsToDict())

        return serialno
