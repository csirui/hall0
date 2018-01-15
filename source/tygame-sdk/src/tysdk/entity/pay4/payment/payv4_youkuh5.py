# -*- coding=utf-8 -*-

import json
import urllib

from tyframework.context import TyContext
from tysdk.entity.pay3.constants import PayConst
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.paythird.helper import PayHelper


class TuYouPayYouKuH5V4(PayBaseV4):
    @payv4_order('h5.youku')
    def charge_data(self, mi):
        chargeinfo = self.get_charge_info(mi)
        buttonId = chargeinfo['buttonId']
        amount = str(int(float(chargeinfo['chargeTotal']) * 100))
        prodName = chargeinfo['buttonName']
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/youku/callback'
        chargeinfo['chargeData'] = {'amount': amount, 'productId': buttonId,
                                    'productName': prodName, 'notifyUrl': notifyurl}
        return self.return_mo(0, chargeInfo=chargeinfo)

    @classmethod
    def doPayRequest(self, chargeInfo, mi, mo):
        return PayConst.CHARGE_STATE_REQUEST

    @payv4_callback('/open/ve/pay/youkuh5/callback')
    def doYouKuCallback(cls, rpath):
        """
        qid=50469470&order_amount=10&order_id=youkutest1011&server_id=S1&sign=7439fb6fa5f82104c107648e9ac77d76
        sign=md5( qid + order_amount + order_id + server_id + ext + paykey );
        :param rpath:
        :return:
        """
        cb_rsp = {}
        rparam = TyContext.RunHttp.convertArgsToDict()

        try:
            ext = rparam['ext']
            extjson = json.loads(ext)
            ty_order_id = str(extjson.get('ty_order_id'))

            order_id = rparam['order_id']
            order_amount = rparam['order_amount']
            qid = rparam['qid']
            server_id = rparam['server_id']
            sign = rparam['sign']

            # youku_appId = rparam['passthrough']
        except:
            TyContext.ftlog.exception()
            TyContext.ftlog.info('doYouKuH5Callback->ERROR, param error !! rparam=', rparam)
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '参数错误'
            # return json.dumps(cb_rsp)
            return 0

        config = TyContext.Configure.get_global_item_json('youkuh5_config', {})
        paykey = config.get('payKey')
        if not paykey:
            TyContext.ftlog.error('_check_session not paykey ', paykey)
            return 0

        sign_str = qid + order_amount + order_id + server_id + ext + paykey
        from hashlib import md5

        m = md5()
        m.update(sign_str)
        my_sign = m.hexdigest()

        # 签名校验
        if my_sign != sign:
            TyContext.ftlog.error('TuYouPayYouKu sign verify error !!', my_sign, sign)
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '签名验证失败'
            # return json.dumps(cb_rsp)
            return 0

        total_fee = 0
        rparam['chargeType'] = 'h5.youku'
        isOk = PayHelper.callback_ok(ty_order_id, total_fee, rparam)
        if isOk:
            cb_rsp['status'] = 'success'
            cb_rsp['desc'] = '发货成功'
            # return json.dumps(cb_rsp)
            return 1
        else:
            cb_rsp['status'] = 'failed'
            cb_rsp['desc'] = '发货失败'
            # return json.dumps(cb_rsp)
            return 0

    @payv4_callback('/open/ve/pay/youkuh5/vip_callback')
    def doYoukuVipCallback(cls, rpath):
        mo = TyContext.Cls_MsgPack()

        config = TyContext.Configure.get_global_item_json('youkuh5_config', {})
        paykey = config.get('payKey')
        # qid=50469470&grade=1&vip_center_id=youkutest1011&sign=7439fb6fa5f82104c107648e9ac77d76

        qid = TyContext.RunHttp.getRequestParam('qid', '')
        grade = TyContext.RunHttp.getRequestParam('grade', '')
        vip_center_id = TyContext.RunHttp.getRequestParam('vip_center_id', '')
        sign = TyContext.RunHttp.getRequestParam('sign', '')
        if qid == '' or grade == '' or vip_center_id == '':
            return 0

        TyContext.ftlog.info('youku_vip_charge_callback', qid, grade, vip_center_id, sign)

        sign_str = "%s%s%s%s" % (qid, grade, vip_center_id, paykey)
        from hashlib import md5
        m = md5()
        m.update(sign_str)
        my_sign = m.hexdigest()
        TyContext.ftlog.debug('youku_vip_charge_callback my_sign', my_sign, sign)

        if not my_sign or my_sign != sign:
            mo.setResult('code', 1)
            mo.setResult('info', 'sign error')
            return 0

        sns_id = 'youkuh5:' + str(qid)
        uid = TyContext.RedisUserKeys.execute('GET', 'snsidmap:' + sns_id)

        cls.notify_game_server_on_vip_change(uid, vip_center_id, grade)
        return 1

    @classmethod
    def notify_game_server_on_vip_change(cls, uid, vip_center_id, grade):
        TyContext.ftlog.info('youku_vip_charge_notify', uid, grade, vip_center_id)
        appId = 6
        clientId = 'H5_3.7_youku.youku.0-hall6.youku.tu'
        params = {'vip_center_id': vip_center_id, 'grade': grade, 'uid': uid, 'appId': appId, 'clientId': clientId}
        control = TyContext.ServerControl.findServerControl(
            appId, clientId)
        if not control:
            TyContext.ftlog.error('notify_game_server_on_vip_change can not'
                                  ' find server control, params', params)
            return
        notifyUrl = str(control['http'] + '/v2/game/h5/dizhu/youku/vip_notify?' + urllib.urlencode(params))
        TyContext.ftlog.debug('notify_game_server_on_vip_change'
                              ' arguments', params, 'notifyUrl', notifyUrl)
        try:
            from twisted.web import client
            d = client.getPage(notifyUrl, method='GET')
        except Exception as e:
            TyContext.ftlog.error('notify_game_server_on_vip_change error', e,
                                  'notifyUrl', notifyUrl)

        def ok_callback(response):
            TyContext.ftlog.info('notify_game_server_on_vip_change response', response)

        def err_callback(error):
            TyContext.ftlog.error('notify_game_server_on_vip_change error', error)

        d.addCallbacks(ok_callback, err_callback)
