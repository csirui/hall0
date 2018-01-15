# -*- coding=utf-8 -*-

import json

import datetime

from constants import PayConst
from tyframework.context import TyContext
from tysdk.entity.duandai.paycodes import PayCodes
from tysdk.entity.duandai.riskcontrol import RiskControl
from tysdk.entity.pay.shortidmapping import ShortOrderIdMap
from tysdk.entity.pay3.query_conf import TuyouPayQueryConf
from tysdk.entity.pay_common.clientrevision import ClientRevision
from tysdk.entity.pay_common.orderlog import Order


class TuyouPayQuery(object):
    __query_ext_status_funs__ = {}

    @classmethod
    def status(cls, mi):

        platformOrderId = mi.getParamStr('platformOrderId')
        platformOrderId = ShortOrderIdMap.get_long_order_id(platformOrderId)
        querynums = mi.getParamInt('querynums')
        appId = mi.getParamInt('appId')
        userId = mi.getParamInt('userId')
        clientId = mi.getParamStr('clientId', 'na')
        paytype = mi.getParamStr('payType', 'na')

        mo = TyContext.Cls_MsgPack()
        mo.setCmd('status')

        chargeKey = 'sdk.charge:' + platformOrderId
        state, chargeInfo, consumemo, errorInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'state', 'charge',
                                                                                 'consume:mo', 'errorInfo')
        if state == None or chargeInfo == None:
            mo.setError(1, 'platformOrderId参数错误')
            return mo

        chargeInfo = json.loads(chargeInfo)
        if paytype != 'na':
            chargeInfo['chargeType'] = paytype
        isOK = cls.__query_ext_status__(chargeInfo)
        if isOK:
            state, consumemo, errorInfo = TyContext.RedisPayData.execute('HMGET', chargeKey, 'state', 'consume:mo',
                                                                         'errorInfo')

        if state < PayConst.CHARGE_STATE_CLIENT_PAY_DONE:
            TyContext.RedisPayData.execute('HMSET', chargeKey, 'state', PayConst.CHARGE_STATE_CLIENT_PAY_DONE)
            Order.log(platformOrderId, Order.CLIENT_FINISHED, userId, appId,
                      clientId, paytype=paytype,
                      diamondid=chargeInfo.get('diamondId', 'na'),
                      charge_price=chargeInfo.get('chargeTotal', 'na'),
                      )
            # 对完成客户端请求的订单进行风控，之前在callback里进行风控效果不好,这里把total_fee=0
            # appids -> {"paytype": "appid"}
            appids = PayCodes(clientId).appids
            duandais = TyContext.Configure.get_global_item_json('all_duandai_paytypes', {})
            if paytype in appids.keys() and paytype in duandais:
                paytype = '_'.join([paytype, appids[paytype]])
                RiskControl(userId).record_usage(paytype, 0)

        # 充值中
        if state < PayConst.CHARGE_STATE_DONE:
            return cls.__get_query_mo(mo, state, 'process', chargeInfo, paytype, querynums)

        # 购买成功
        if state == PayConst.CHARGE_STATE_DONE:
            return cls.__get_query_mo(mo, state, 'success', chargeInfo, paytype, querynums)

        # 充值成功
        if state == PayConst.CHARGE_STATE_DONE_CONSUME:
            return cls.__get_query_mo(mo, state, 'success', chargeInfo, paytype, querynums)

        # 发货失败
        if state == PayConst.CHARGE_STATE_ERROR_CONSUME:
            return cls.__get_query_mo(mo, state, 'bug', chargeInfo, paytype, querynums)

        # 支付失败
        if state == PayConst.CHARGE_STATE_ERROR_CALLBACK:
            # 支付失败返回更多支付方式
            failreturnconfig = TyContext.Configure.get_global_item_json('payfail_returnconfig', {})
            payconfig = TyContext.Configure.get_global_item_json('store_payment', clientid=clientId)
            if payconfig and 'payment' in payconfig and 'more_categories' in payconfig['payment']:
                TyContext.ftlog.debug('CHARGE_STATE_ERROR_CALLBACK', payconfig['payment']['more_categories'],
                                      'diamondId', chargeInfo['diamondId'])
                if payconfig['payment']['more_categories'] in failreturnconfig and chargeInfo[
                    'diamondId'] in failreturnconfig:
                    mo.setResult('des', failreturnconfig[chargeInfo['diamondId']]['des'])

                    paytemplate = failreturnconfig[payconfig['payment']['more_categories']]
                    paytemplateconfig = TyContext.Configure.get_global_item_json(paytemplate)
                    mo.setResult('morepaytype', paytemplateconfig)
                    mo.setResult('priority', paytemplateconfig[0]['paytype'])
            return cls.__get_query_mo(mo, state, 'fail', chargeInfo, paytype, querynums)

        # 充值失败
        if errorInfo == None:
            errorInfo = ''
        else:
            errorInfo = u'充值失败原因:' + unicode(errorInfo)

        # 支付失败返回更多支付方式
        failreturnconfig = TyContext.Configure.get_global_item_json('payfail_returnconfig', {})
        payconfig = TyContext.Configure.get_global_item_json('store_payment', clientid=clientId)
        if payconfig and 'payment' in payconfig and 'more_categories' in payconfig['payment']:
            TyContext.ftlog.debug('CHARGE_STATE_ERROR_CALLBACK', payconfig['payment']['more_categories'], 'diamondId',
                                  chargeInfo['diamondId'])
            if payconfig['payment']['more_categories'] in failreturnconfig and chargeInfo[
                'diamondId'] in failreturnconfig:
                mo.setResult('des', failreturnconfig[chargeInfo['diamondId']]['des'])

                paytemplate = failreturnconfig[payconfig['payment']['more_categories']]
                paytemplateconfig = TyContext.Configure.get_global_item_json(paytemplate)
                mo.setResult('morepaytype', paytemplateconfig)
                mo.setResult('priority', paytemplateconfig[0]['paytype'])
        return cls.__get_query_mo(mo, state, 'fail', chargeInfo, paytype, querynums, errorInfo)

    @classmethod
    def __get_query_mo(cls, mo, state, action, chargeInfo, paytype, querynums, errorInfo=''):
        querystatus_config = TyContext.Configure.get_global_item_json('querystatus_config', decodeutf8=True)
        if action == 'fail':
            baseinfo = querystatus_config['failinfo']
        elif action == 'bug':
            baseinfo = ''
        elif action == 'timeout':
            baseinfo = querystatus_config['timeoutinfo']
        else:
            baseinfo = querystatus_config['processinfo']
        querymaxnums = int(querystatus_config['querymaxnums'])
        if action == 'process' and querynums > querymaxnums:
            action = 'timeout'
            mo.setResult('stopquery', 1)
        if ClientRevision(chargeInfo['uid']).support_querystatus_rsp_action_parameter:
            mo.setResult('status', state)
            mo.setResult('action', action)
        else:
            mo.setResult('action', action)
            mo.setResult('status', state)
        info = querystatus_config[action]['info']
        tips = querystatus_config[action]['tips']
        binfo = ''
        if baseinfo:
            for key in baseinfo.keys():
                if paytype in key:
                    binfo = baseinfo[key]
                    break
            if not binfo:
                binfo = baseinfo['thirdpay']
        infotemplate = querystatus_config[action]['content']
        if action == 'success':
            content = infotemplate.format(
                time=datetime.datetime.now().strftime('%H点%M分%S秒'),
                prodname=chargeInfo['diamondName'].encode('utf8')
            )
        elif action == 'bug':
            content = infotemplate
        elif action == 'fail':
            content = infotemplate.format(
                info=binfo + '\n' + errorInfo.encode('utf8'),
            )
        else:
            content = infotemplate.format(
                info=binfo,
            )
        mo.setResult('info', info)
        mo.setResult('content', content)
        mo.setResult('tips', tips)
        return mo

    @classmethod
    def __query_ext_status__(cls, chargeInfo):
        # for charge categories, no need to query external status
        if 'chargeType' not in chargeInfo:
            return
        chargeType = chargeInfo['chargeType']
        cfun = None
        TyContext.ftlog.debug('__query_ext_status__ ', chargeInfo)
        if chargeType in cls.__query_ext_status_funs__:
            cfun = cls.__query_ext_status_funs__[chargeType]
        else:
            if chargeType in TuyouPayQueryConf.QUERY_DATA:
                cpath = TuyouPayQueryConf.QUERY_DATA[chargeType]
                tks = cpath.split('.')
                mpackage = '.'.join(tks[0:-1])
                clsName = tks[-1]
                clazz = None
                exec 'from %s import %s as clazz' % (mpackage, clsName)
                cfun = getattr(clazz, 'query_ext_status')
                cls.__query_ext_status_funs__[chargeType] = cfun
            else:
                cls.__query_ext_status_funs__[chargeType] = None
        isOK = False
        if cfun:
            try:
                isOK = cfun(chargeInfo)
            except:
                TyContext.ftlog.exception()
        TyContext.ftlog.debug('__query_ext_status__', isOK, cfun)
        return isOK
