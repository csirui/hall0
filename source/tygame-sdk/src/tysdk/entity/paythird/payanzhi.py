# -*- coding=utf-8 -*-

#################################################
# 安智app获取订单和支付结果回掉的主要逻辑实现
# 目前接入的游戏有中国象棋
# Created by Zhang Shibo at 2015/10/10
# version: 3.2
#################################################

import base64
import json
from urllib import unquote

from helper import PayHelper
from tyframework.context import TyContext
from tysdk.utils.pyDes201.pyDes import triple_des, ECB, PAD_NORMAL


class TuYouPayAnZhi(object):
    @classmethod
    def charge_data(cls, chargeinfo):
        TyContext.ftlog.debug('TuYouAiDongManPay charge_data chargeinfo', chargeinfo)
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}

    @classmethod
    def doAnZhiCallback(cls, rpath):
        postData = TyContext.RunHttp.get_body_content()
        TyContext.ftlog.debug('TuYouPayAnZhi->doAnZhiCallback original postData is:', postData)

        paramslist = postData.split('&')
        rparam = {}
        for k in paramslist:
            paramdata = k.split('=')
            rparam[paramdata[0]] = paramdata[1]
        TyContext.ftlog.debug('TuYouPayAnZhi->doAnZhiCallback parame list(Before urldecode) is: ', rparam)

        for k in rparam.keys():
            rparam[k] = unquote(rparam[k])
        TyContext.ftlog.debug('TuYouPayAnZhi->doAnZhiCallback parame list(After urldecode) is: ', rparam)

        if 'data' in rparam and 'appId' in rparam:
            data = rparam['data']
            appId = rparam['appId']
        else:
            TyContext.ftlog.error('TuYouPayAnZhi->doAnZhiCallback ERROR There doesn\'t has data or appId in post data.')
            return 'failed'

        anzhiconfig = TyContext.Configure.get_global_item_json('anzhi_config', {})
        if anzhiconfig:
            for item in anzhiconfig:
                if 0 == cmp(item['appId'], appId):
                    cls.encryptKey = item['appsecret']
                    break
            else:
                TyContext.ftlog.error('TuYouPayAnZhi->doAnZhiCallback ERROR Cann\'t find appsecert, appId is: ', appId)
                return 'success'
        else:
            TyContext.ftlog.error('TuYouPayAnZhi->doAnZhiCallback ERROR cann\'t find anzhi_config.')
            return 'success'

        try:
            # 先用base64解码，再采用3des解密
            tripelDes = triple_des(cls.encryptKey.encode('ascii'), mode=ECB, padmode=PAD_NORMAL)
            data = tripelDes.decrypt(base64.b64decode(data))
            data = "".join([data.rsplit("}", 1)[0], "}"])
            TyContext.ftlog.debug('TuYouPayAnZhi->doAnZhiCallback Data is: ', data)
            params = json.loads(data)
            params['third_orderid'] = params['orderId']  # 三方订单号
            orderPlatformId = params['cpInfo']  # 途游订单号
            orderAmount = params['orderAmount']  # 商品金额(分)
            code = int(params['code'])  # 订单状态 成功:1
            TyContext.ftlog.info('TuYouPayAnZhi->doAnZhiCallback params: ', params, ' orderPlatformId is: ',
                                 orderPlatformId)
        except Exception as e:
            TyContext.ftlog.error('TuYouPayAnZhi->doAnZhiCallback ERROR: ', e)
            return 'success'

        # 安智的同事说，只会出现code==1的情况，这里只是为了以防万一
        if 1 != code:
            TyContext.ftlog.error()
            errinfo = '安智支付失败'
            PayHelper.callback_error(orderPlatformId, errinfo, params)

        PayHelper.callback_ok(orderPlatformId, float(orderAmount) / 100, params)
        return 'success'
