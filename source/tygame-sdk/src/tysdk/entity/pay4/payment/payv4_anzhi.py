# -*- coding=utf-8 -*-

#################################################
# 安智app获取订单和支付结果回掉的主要逻辑实现
# 目前接入的游戏有中国象棋
# Created by Zhang Shibo at 2015/10/10
# version: 3.2
#################################################

import base64
import json
import time
from base64 import b64encode
from hashlib import md5
from urllib import unquote

from payv4_helper import PayHelperV4
from tyframework.context import TyContext
from tysdk.configure.game_item import GameItemConfigure
from tysdk.entity.pay4.charge_model import ChargeModel
from tysdk.entity.pay4.decorator.payv4_callback import payv4_callback
from tysdk.entity.pay4.decorator.payv4_order import payv4_order
from tysdk.entity.pay4.payment.payv4_base import PayBaseV4
from tysdk.entity.pay4.payment.payv4_error import PayErrorV4
from tysdk.utils.pyDes201.pyDes import triple_des, ECB, PAD_NORMAL, PAD_PKCS5


class TuYouPayAnZhiV4(PayBaseV4):
    @payv4_order('anzhi')
    def charge_data(cls, mi):
        chargeinfo = cls.get_charge_info(mi)
        config = GameItemConfigure(chargeinfo['appId']).get_game_channel_configure_by_package('anzhi',
                                                                                              chargeinfo['packageName'],
                                                                                              chargeinfo['mainChannel'])
        if not config:
            TyContext.ftlog.error('Anzhi,get sdkconfig error,cannot save orderinfo berforpay!')
        anzhiAppId = config.get('anzhi_appKey', "")
        anzhi_appSecret = config.get('anzhi_appSecret', "")
        charge_key = 'sdk.charge:anzhi:%s' % anzhiAppId
        TyContext.RedisPayData.execute('HSET', charge_key, 'appSecret', anzhi_appSecret)
        TyContext.ftlog.debug('TuYouAiDongManPay charge_data chargeinfo', chargeinfo)

        anzhiconfig = TyContext.Configure.get_global_item_json('anzhi_config', {})
        desKey = ''
        azsrt = ''
        azappKey = mi.getParamStr('anzhi_appKey')

        if anzhiconfig:
            for item in anzhiconfig:
                if 0 == cmp(item['appId'], azappKey):
                    TyContext.ftlog.debug('TuyouPayAnzhiv4 -> azappKey ->', azappKey, item['appId'])
                    azsrt = item['appsecret']
                    desKey = item.get('3desKey', '')
                    break
        TyContext.ftlog.debug('TuYouanzhi 3desKey=%s,sct=%s' % (azsrt, desKey))
        if not azsrt:
            azsrt = config.get('anzhi_appSecret', '')
            desKey = config.get('anzhi_3desKey', '')
            if not azsrt:
                raise PayErrorV4(1, '找不到安智的配置%s' % azappKey)
        chargeinfo['chargeData'] = {'platformOrderId': chargeinfo['platformOrderId']}

        if desKey:
            price = chargeinfo['diamondPrice']

            data = {
                'cpOrderId': chargeinfo['platformOrderId'],
                'cpOrderTime': int(time.time()),
                'amount': int(price * 100),
                'cpCustomInfo': chargeinfo['platformOrderId'],
                'productName': chargeinfo['diamondName'],
                'productCode': chargeinfo['diamondId'],
            }

            tripelDes = triple_des(desKey.encode('ascii'), mode=ECB, padmode=PAD_NORMAL)
            data_json = json.dumps(data)
            des_3_data = b64encode(tripelDes.encrypt(data_json, padmode=PAD_PKCS5))
            TyContext.ftlog.debug('TuYouPayAnZhiV4 data_json=%s,key=%s,3des=%s', data_json, desKey, des_3_data)
            chargeinfo['chargeData']['secretMD5'] = md5(desKey).hexdigest()
            chargeinfo['chargeData']['order_data'] = des_3_data

        return cls.return_mo(0, chargeInfo=chargeinfo)

    @payv4_callback('/open/ve/pay/anzhi/callback')
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
        encryptKey = ""
        if anzhiconfig:
            for item in anzhiconfig:
                if 0 == cmp(item['appId'], appId):
                    encryptKey = item['appsecret']
                    break
            else:
                TyContext.ftlog.error('TuYouPayAnZhi->doAnZhiCallback ERROR Cann\'t find appsecert, appId is: ', appId)
        else:
            TyContext.ftlog.error('TuYouPayAnZhi->doAnZhiCallback ERROR cann\'t find anzhi_config.')
        if not encryptKey:
            charge_key = 'sdk.charge:anzhi:%s' % appId
            encryptKey = TyContext.RedisPayData.execute('HGET', charge_key, 'appSecret')
            TyContext.ftlog.debug('get sdk config from redis,', encryptKey)
        try:
            # 先用base64解码，再采用3des解密
            tripelDes = triple_des(encryptKey.encode('ascii'), mode=ECB, padmode=PAD_NORMAL)
            data = tripelDes.decrypt(base64.b64decode(data))
            data = "".join([data.rsplit("}", 1)[0], "}"])
            TyContext.ftlog.debug('TuYouPayAnZhi->doAnZhiCallback Data is: ', data)
            params = json.loads(data)
            params['third_orderid'] = params['orderId']  # 三方订单号
            orderPlatformId = params['cpInfo']  # 途游订单号
            orderAmount = params['orderAmount']  # 商品金额(分)
            redBagMoney = params['redBagMoney']
            code = int(params['code'])  # 订单状态 成功:1
            ChargeModel.save_third_pay_order_id(orderPlatformId, params['orderId'])
            TyContext.ftlog.info('TuYouPayAnZhi->doAnZhiCallback params: ', params, ' orderPlatformId is: ',
                                 orderPlatformId)
        except Exception as e:
            TyContext.ftlog.error('TuYouPayAnZhi->doAnZhiCallback ERROR: ', e)
            return 'success'

        # 安智的同事说，只会出现code==1的情况，这里只是为了以防万一
        if 1 != code:
            TyContext.ftlog.error()
            errinfo = '安智支付失败'
            PayHelperV4.callback_error(orderPlatformId, errinfo, params)

        # 2) orderAmount+redBagMoney 应等于道具金额,金额验证异常请返回”money_error”。
        chargeKey = 'sdk.charge:' + orderPlatformId
        chargeTotal = TyContext.RedisPayData.execute('HGET', chargeKey, 'chargeTotal')

        anzhiTotal = (float(orderAmount) + float(redBagMoney)) / 100

        if float(chargeTotal) != anzhiTotal:
            return 'money_error'

        PayHelperV4.callback_ok(orderPlatformId, anzhiTotal, params)
        return 'success'
