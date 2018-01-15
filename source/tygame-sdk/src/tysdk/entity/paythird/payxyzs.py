# -*- coding=utf-8 -*-

import json
from hashlib import md5

from helper import PayHelper
from tyframework.context import TyContext


######################################################################
# XY助手平台获取订单和支付结果回掉的主要逻辑实现
# 目前接入的游戏有途游斗地主、单机斗地主
# Created by Zhangshibo at 2015/08/15
# version: v2.0.3
######################################################################

class TuYouPayXYZS(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}

    @classmethod
    def doXYZSPayCallback(cls, rpath):
        # 获取XY助手途游斗地主的appkey和paykey
        rparam = TyContext.RunHttp.convertArgsToDict()
        try:
            appid = rparam['orderid'].split('_')[0]
            keyvalue = TyContext.Configure.get_global_item_json('XYSdk_config', {})
            if keyvalue and appid in keyvalue:
                appkey = keyvalue[appid]['appkey']
                paykey = keyvalue[appid]['paykey']
            else:
                TyContext.ftlog.error('TuYouPayXYZS->doXYZSPayCallback get appkey and paykey ERROR')
                return cls._response_result(8)
        except:
            TyContext.ftlog.error('TuYouPayXYZS->doXYZSPayCallback get appkey and paykey ERROR')
            return cls._response_result(8)
        TyContext.ftlog.debug(
            'TuYouPayXYZS->doXYZSPayCallback rparam: [%s], appid: [%s], appkey: [%s], paykey: [%s]' % (
            rparam, appid, appkey, paykey))
        return cls._docallback(appkey, paykey)

    @classmethod
    def doXYZSDJPayCallback(cls, rpath):
        # 获取XY助手单机斗地主的appkey和paykey
        rparam = TyContext.RunHttp.convertArgsToDict()
        try:
            appid = rparam['orderid'].split('_')[0]
            keyvalue = TyContext.Configure.get_global_item_json('XYDJSdk_config', {})
            if keyvalue and appid in keyvalue:
                appkey = keyvalue[appid]['appkey']
                paykey = keyvalue[appid]['paykey']
            else:
                TyContext.ftlog.error('TuYouPayXYZS->doXYZSDJPayCallback get appkey and paykey ERROR')
                return cls._response_result(8)
        except:
            TyContext.ftlog.error('TuYouPayXYZS->doXYZSDJPayCallback get appkey and paykey ERROR')
            return cls._response_result(8)
        TyContext.ftlog.debug(
            'TuYouPayXYZS->doXYZSDJPayCallback rparam: [%s], appid: [%s], appkey: [%s], paykey: [%s]' % (
            rparam, appid, appkey, paykey))
        return cls._docallback(appkey, paykey)

    @classmethod
    def _docallback(cls, appkey, paykey):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayXYZS->_docallback rparam is : ', rparam)

        # 验签
        safeSign = cls._gen_safe_sign(rparam, appkey)
        if safeSign != rparam['sign']:
            TyContext.ftlog.error('TuYouPayXYZS->_docallback sign verify failed, '
                                  'sign is [', safeSign, '],  rparam["sign"] is [', rparam['sign'], ']')
            return cls._response_result(6)
        if rparam['sig']:
            safeSign = cls._gen_safe_sign(rparam, paykey)
            if safeSign != rparam['sig']:
                TyContext.ftlog.error('TuYouPayXYZS->_docallback sign verify failed.'
                                      'sig is [', safeSign, '],  rparam["sig"] is [', rparam['sig'], ']')
                return cls._response_result(6)

        # 开始发货
        orderPlatformId = rparam["extra"]
        total_fee = float(rparam["amount"])
        PayHelper.callback_ok(orderPlatformId, total_fee, rparam)
        TyContext.ftlog.debug('TuYouPayXYZS->_docallback deliver goods successed.')

        return cls._response_result(0)

    # 签名方法
    @classmethod
    def _gen_safe_sign(cls, rparam, appkey):
        queryStr = appkey + '&'.join([k + '=' + rparam[k] for k in sorted(rparam.keys()) if k != 'sign' and k != 'sig'])
        TyContext.ftlog.debug('TuYouPayXYZS->_gen_safe_sign queryStr befor sign is : ', queryStr)
        sign = md5(queryStr).hexdigest()
        TyContext.ftlog.debug('TuYouPayXYZS->_gen_safe_sign queryStr after sign is : ', sign)
        return sign

    # 相应结果
    @classmethod
    def _response_result(cls, code):
        message = {
            0: '回调成功',
            1: '参数错误',
            2: '玩家不存在',
            3: '游戏服不存在',
            4: '订单已存在',
            5: '透传信息错误',
            6: '签名校验错误',
            7: '数据库错误',
            8: '其它错误'
        }
        return json.dumps({'ret': code, 'msg': message[code]})
