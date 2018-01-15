# -*- coding=utf-8 -*-

import json
from hashlib import md5

import datetime

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.duandai.paycodes import PayCodes


class TuYouPayAiGame():
    resultcode_msg = {
        '00': '订购成功',
        '01': '短代格式错误',
        '02': '合作方代码错误',
        '03': '订购产品代码错误',
        '04': '合作方游戏用户格式错误',
        '05': '合作方游戏流水号格式错误',
        '06': '接入码扩展位数值与实际道具金额不符',
        '07': '短代限额约束:详情说明',
        '08': '发送短信失败/订购失败',
        '09': '服务异常',
    }

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
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}

    @classmethod
    def _get_order_info(self, orderPlatformId):
        appInfo = {}
        try:
            TyContext.RunMode.get_server_link(orderPlatformId)
            baseinfo = TyContext.RedisPayData.execute('HGET', 'sdk.charge:' + str(orderPlatformId), 'charge')
            baseinfo = json.loads(baseinfo)
            appInfo['clientId'] = baseinfo['clientId']
            # if 'uid' in baseinfo and baseinfo['uid'] is not None:
            #    appInfo['uid'] = baseinfo['uid']
            # if 'orderPrice' in baseinfo and baseinfo['orderPrice'] is not None:
            #    appInfo['orderPrice'] = baseinfo['orderPrice']
            # if 'appId' in baseinfo and baseinfo['appId'] is not None:
            #    appInfo['appId'] = baseinfo['appId']
        except Exception as e:
            TyContext.ftlog.error('TuYouPayAiGame._get_order_info exception', e,
                                  'orderPlatformId', orderPlatformId)

        TyContext.ftlog.debug('doAiGameMsgCallback->_get_order_info appInfo',
                              appInfo)
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
            TyContext.ftlog.info('doAiGameMsgCallback->ERROR, sign error !! sign=', validatecode, 'vSign=', vSign)
            return TuYouPayAiGame.XML_RET % ('1', cpparam)

        # 解密得到原始游戏订单号
        orderPlatformId = cpparam
        TyContext.ftlog.info('doAiGameMsgCallback orderPlatformId=', orderPlatformId)
        notifys['chargeType'] = 'aigame.msg'
        if resultcode == '00':
            PayHelper.callback_ok(orderPlatformId, -1, notifys)
        else:
            PayHelper.callback_error(orderPlatformId, 'resultCode(%s) not 0' % resultcode, notifys)
        return TuYouPayAiGame.XML_RET % ('0', cpparam)

    @classmethod
    def doAiGameCallbackDizhuHappy(self, rpath):
        appkey = '89df51ef2ece07a06ed513d4c522266f'
        return self._doAiGameMsgCallbackNew(appkey, rpath)

    '''
    @classmethod
    def doAiGameCallbackDizhuDanji(self, rpath):
        appkey = '62d55e5d5d47f5d0121d2049d6893bc1'
        return self._doAiGameMsgCallbackNew(appkey, rpath)
    '''

    @classmethod
    def doAiGameCallbackDizhuHuabei(self, rpath):
        appkey = '6be1b0234b18b0e09188abb4e2429454'
        return self._doAiGameMsgCallbackNew(appkey, rpath)

    @classmethod
    def doAiGameCallbackDizhuStarZszhWF(self, rpath):
        appkey = '7978406bb21b362065e9588cecd5d8d1'
        return self._doAiGameMsgCallbackNew(appkey, rpath)

    @classmethod
    def doAiGameCallbackDizhuStarZszhPT(self, rpath):
        appkey = '9bff05ca361095c5727d7e7b2946b516'
        return self._doAiGameMsgCallbackNew(appkey, rpath)

    # added by zhangshibo at 2015-09-11
    # gamename:单机斗地主（欢乐版）
    # version:4.1.2
    @classmethod
    def doAiGameCallbackDizhuHappyDj(self, rpath):
        appkey = 'fe6a5fe5ed6193ee88bc19457b8bf6d7'
        return self._doAiGameMsgCallbackNew(appkey, rpath)

    # end added

    @classmethod
    def _get_appkey(cls, gamecode, clientid):
        paycodes = PayCodes(clientid)
        appkey = paycodes.get_appkey('aigame')
        if appkey:
            TyContext.ftlog.debug('TuYouPayAiGame _get_app_key from paycodes'
                                  ' config', appkey)
            return appkey

        appkey = ''
        try:
            extdata = TyContext.PayType.get_pay_type_ext_datas('aigame')
            appkey = extdata['appkeys'][gamecode]
        except Exception as e:
            TyContext.ftlog.error('TuYouPayAiGame _get_app_key exception', e)

        return appkey

    @classmethod
    def doAiGameAllCallback(cls, rpath):
        notifys = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('doAiGameAllCallback->param=', notifys)

        cpparam = notifys.get('cpparam', '')
        if cpparam:
            return cls.doAiGameMsgCallback(rpath)

        cp_order_id = notifys.get('cp_order_id', '')
        clientid = cls._get_order_info(cp_order_id).get('clientId', '')
        gamecode = notifys.get('game_code', '')
        appkey = cls._get_appkey(gamecode, clientid)
        if not appkey:
            TyContext.ftlog.error('doAiGameAllCallback->no appkey configured'
                                  ' for game_code', gamecode)
        return cls._do_all_callback(appkey, notifys)

    @classmethod
    def _doAiGameMsgCallbackNew(cls, appkey, rpath):
        notifys = TyContext.RunHttp.convertArgsToDict()
        return cls._do_all_callback(appkey, notifys)

    @classmethod
    def _do_all_callback(self, appkey, notifys):
        method = notifys.get('method', '')
        cp_order_id = notifys.get('cp_order_id', '')
        correlator = notifys.get('correlator', '')
        order_time = notifys.get('order_time', '')
        sign = notifys.get('sign', '')

        if method == 'check':  # 订单效验接口
            game_account = ''
            game_fee = ''
            ct = datetime.datetime.now()
            order_current_time = ct.strftime('%Y%m%d%H%M%S')
            if cp_order_id == '' or sign == '':
                return TuYouPayAiGame.XML_CHECK_RET % (
                cp_order_id, correlator, game_account, game_fee, '1', order_current_time)

            orderPlatformId = cp_order_id
            appInfo = self._get_order_info(orderPlatformId)
            if 'uid' in appInfo and appInfo['uid'] is not None:
                game_account = appInfo['uid']
            if 'orderPrice' in appInfo and appInfo['orderPrice'] is not None:
                game_fee = appInfo['orderPrice']

            tSign = cp_order_id + str(correlator) + str(order_time) + method + appkey
            m = md5()
            m.update(tSign)
            vSign = m.hexdigest()
            if sign != vSign:
                TyContext.ftlog.info('TuYouPayAiGame._do_all_callback->ERROR, sign error !! sign=', sign, 'vSign=',
                                     vSign)
                return TuYouPayAiGame.XML_CHECK_RET % (
                cp_order_id, correlator, game_account, game_fee, '1', order_current_time)

            return TuYouPayAiGame.XML_CHECK_RET % (
            cp_order_id, correlator, game_account, game_fee, '0', order_current_time)

        elif method == 'callback':  # 成功回调接口
            result_code = notifys.get('result_code', '')
            fee = notifys.get('fee', '-1')  # 单位：元
            try:
                fee = float(fee)
            except:
                TyContext.ftlog.error('TuYouPayAiGame._do_all_callback->ERROR, fee format error !! fee=', fee)
                fee = -1
            pay_type = notifys.get('pay_type', 'na')

            ct = datetime.datetime.now()
            order_current_time = ct.strftime('%Y%m%d%H%M%S')
            if cp_order_id == '' or sign == '' or method != 'callback':
                return TuYouPayAiGame.XML_RET % ('1', cp_order_id)

            orderPlatformId = cp_order_id
            if appkey:
                tSign = cp_order_id + str(correlator) + str(result_code) + str(int(fee)) + pay_type + method + appkey
                m = md5()
                m.update(tSign)
                vSign = m.hexdigest()
                if sign != vSign:
                    TyContext.ftlog.info('TuYouPayAiGame._do_all_callback->ERROR,'
                                         ' sign error !! sign=', sign, 'vSign=', vSign)
                    return TuYouPayAiGame.XML_RET % ('1', cp_order_id)

            notifys['chargeType'] = 'aigame'
            notifys['sub_paytype'] = pay_type
            notifys['third_orderid'] = correlator
            notifys['pay_appid'] = notifys.get('game_code', 'na')
            if str(result_code) == '00':
                isOk = PayHelper.callback_ok(orderPlatformId, -1, notifys)
                if not isOk:
                    TyContext.ftlog.error('TuYouPayAiGame._do_all_callback->callback failed',
                                          'order', orderPlatformId)
                retXml = TuYouPayAiGame.XML_RET % ('0', cp_order_id)
            else:
                errinfo = TuYouPayAiGame.resultcode_msg.get(
                    result_code, 'result_code(%s) is not 00' % result_code)
                TyContext.ftlog.error('TuYouPayAiGame._do_all_callback error',
                                      errinfo, 'for order', orderPlatformId)
                PayHelper.callback_error(orderPlatformId, errinfo, notifys)
                retXml = TuYouPayAiGame.XML_RET % ('0', cp_order_id)

            return retXml

    @classmethod
    def doAiGameCallback(self, rpath):
        notifys = TyContext.RunHttp.convertArgsToDict()
        serialno = notifys.get('serialno', '')
        resultcode = notifys.get('resultCode', '')
        resultmsg = notifys.get('resultMsg', '')
        gameUserId = notifys.get('gameUserId', '')
        order_paytype = notifys.get('payType', '')
        validatecode = notifys.get('validatecode', '')

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

            notifys['chargeType'] = 'aigame'
            PayHelper.callback_ok(orderPlatformId, -1, notifys)

        return serialno
