# -*- coding=utf-8 -*-

from collections import OrderedDict
from hashlib import md5
from urllib import unquote
from urllib import urlencode

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4


######################################################################
# 海马玩获取订单和支付结果回掉的主要逻辑实现
# Created by Zhangshibo at 2015/08/18
######################################################################
class TuYouPayHaiMaWanV4(PayBaseV4):
    @payv4_order('haimawan')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}
        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/haimawan/callback')
    def doPayHaiMaWanCallback(cls, rpath):
        message = {
            0: '订单未支付',
            1: '订单支付成功',
            2: '请求订单失败',
            3: '订单签名失败',
            4: '订单支付失败',
            5: '其他失败',
        }
        rparam = OrderedDict()
        params = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.debug('TuYouPayHaiMaWan->doHaiMaWanPayCallback params in Requrest is: ', params)

        # 获取回掉参数
        try:
            rparam['notify_time'] = params['notify_time']
            rparam['appid'] = params['appid']
            rparam['out_trade_no'] = params['out_trade_no']
            rparam['total_fee'] = params['total_fee']
            rparam['subject'] = params['subject']
            rparam['body'] = params['body']
            rparam['trade_status'] = params['trade_status']
            strSign = unquote(params['sign'])
        except Exception, e:
            TyContext.ftlog.error('TuYouPayHaiMaWan->doHaiMaWanPayCallback get callback param ERROR!', e)
            return 'fail'

        # 判断支付状态
        status = int(params['trade_status'])
        if status not in message or 1 != status:
            TyContext.ftlog.error('TuYouPayHaiMaWan->doHaiMaWanPayCallback pay failed, status is: ', message[status])
            PayHelperV4.callback_error(params["out_trade_no"], message[status], rparam)
            return 'fail'

        # 验证签名
        keyvalue = TyContext.Configure.get_global_item_json('haimawan_config', {})  # 获取海马玩的appkey
        for value in keyvalue:
            if 0 == cmp(value['appid'], params['appid']):
                appkey = value['appkey']
                break
        else:
            TyContext.ftlog.error('uYouPayHaiMaWan->doHaiMaWanPayCallback get appkey ERROR')
            return 'fail'

        rparam['trade_status'] = rparam['trade_status'] + appkey
        strBeforeSign = urlencode(rparam)
        strAfterSign = md5(strBeforeSign).hexdigest()
        TyContext.ftlog.debug('TuYouPayHaiMaWan->doHaiMaWanPayCallback Before sign: [', strBeforeSign, '] '
                                                                                                       'After sign: [',
                              strAfterSign, ']')
        if 0 != cmp(strSign, strAfterSign):
            TyContext.ftlog.error('TuYouPayHaiMaWan->doHaiMaWanPayCallback veriry sign failed')
            return 'fail'

        # 发货并返回结果
        orderPlatformId = params["out_trade_no"]
        total_fee = float(params["total_fee"])
        PayHelperV4.callback_ok(orderPlatformId, total_fee, rparam)
        TyContext.ftlog.debug('TuYouPayHaiMaWan->doHaiMaWanPayCallback deliver goods successed.')
        return 'success'
