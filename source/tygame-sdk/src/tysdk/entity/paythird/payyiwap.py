# -*- coding=utf-8 -*-

import json
import time
from hashlib import md5

import datetime

from constants import PHONETYPE_CHINAMOBILE, PHONETYPE_CHINAUNION
from helper import PayHelper
from tyframework.context import TyContext
from tysdk.entity.pay3.consume import TuyouPayConsume

create_errmsg = {
    '10000': '系统异常',
    '10002': '请求参数异常',
    '10005': '未知数据异常',
    '20901': '请求运营商返回无效结果',
    '20902': '短信验证码错误',
    '20903': '手机号被运营商锁定',
    '20904': '发送验证码失败',
    '20905': '手机号超过日消费限额',
    '20906': '手机号超过月消费限额',
    '20907': '用户名超过日消费限额',
    '20908': '用户名超过月消费限额',
    '20909': '同一设备为不同账号充值超过上限',
    '20910': '同一手机号为不同用户充值超过上限',
    '20911': '同一个手机号为不同用户充值超过上限',
    '20912': '手机号余额不足',
    '20913': 'MD5签名校验失败',
    '20915': '黑名单用户',
}


class TuYouPayYiWap(object):
    # merc_id = '2000024'
    # yipay_appid = '5969fac8a69c11e49758c6a10b512583'
    # yipay_key = 'fda8c042c87f2fdb031110c9eadc8dec'
    # createorder_url = 'http://fee.aiyuedu.cn:23000/sdkfee/api2/create_order'

    @classmethod
    def charge_data(cls, chargeinfo):
        chargeinfo = TyContext.RunHttp.convertArgsToDict()
        clientId = chargeinfo.get('clientId', 'Android_3.501_tuyoo.yisdkpay.0-hall6.youyifu.happy')
        TyContext.ftlog.debug('TuYouPayYiWap->charge_data chargeinfo', chargeinfo)
        yiconfig = TyContext.Configure.get_global_item_json('yipaywap_config:%s' % clientId, {})
        cls.merc_id = str(yiconfig['merc_id'])
        cls.yipay_appid = str(yiconfig['app_id'])
        cls.yipay_key = str(yiconfig['yipay_key'])
        cls.createorder_url = str(yiconfig['createorder_url'])

        # 此处为了兼容js跨域问题jsonp,官网展示
        if 'callback' in chargeinfo:
            adaptJsonp = 1
            adaptString = chargeinfo['callback']
        else:
            adaptJsonp = 0
        if 'uid' in chargeinfo:
            userId = str(chargeinfo['uid'])
        else:
            chargeinfo['chargeData'] = {'code': 1, 'info': '缺失参数 uid'}
            return chargeinfo['chargeData']
        appId = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'appId')

        if appId is None:
            appId = '6'

        if 'phoneNum' in chargeinfo:
            bindMobile = str(chargeinfo['phoneNum'])
        else:
            chargeinfo['chargeData'] = {'code': 1, 'info': '缺失参数 bindMobile'}
            return chargeinfo['chargeData']

        if 'phoneType' in chargeinfo:
            phoneType = str(chargeinfo['phoneType'])
        else:
            chargeinfo['chargeData'] = {'code': 1, 'info': '缺失参数 phoneType'}
            return chargeinfo['chargeData']
        phoneType = TyContext.UserSession.get_phone_type_name(phoneType)

        ''' 
        authInfo = chargeinfo['authInfo'] 
        authUid, _, _ = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        if not authUid:
            chargeinfo['chargeData'] = {'code':1, 'info':'用户登录信息超时'}              
        '''

        if 'prodId' in chargeinfo:
            buttonId = chargeinfo['prodId']
        else:
            chargeinfo['chargeData'] = {'code': 1, 'info': '缺失参数 buttonId'}
            return chargeinfo['chargeData']

        yipaywapconfig = yiconfig  # TyContext.Configure.get_global_item_json('yipaywap_config', {})
        diamonds = yipaywapconfig[buttonId]

        price = int(diamonds['price']) * 10

        clientId = yipaywapconfig['clientId']
        platformOrderId = TyContext.ServerControl.makeChargeOrderIdV3(userId, appId, clientId)
        # yipaywapconfig = TyContext.Configure.get_global_item_json('yipaywap_config', {})
        if yipaywapconfig:
            diamond = yipaywapconfig[buttonId]

        chargeinfo = {
            'uid': userId,
            'appId': appId,
            'appInfo': '',
            'clientId': clientId,
            'diamondId': buttonId,
            'diamondPrice': int(diamond['price']) / 10,
            'diamondCount': 1,
            'diamondsPerUnit': diamond['price'],
            'diamondName': diamond['des'],
            'chargeTotal': int(diamond['price']) / 10,
            'platformOrderId': platformOrderId,
            'phoneType': TyContext.UserSession.get_session_phone_type(userId),
            'payInfo': '',
            'buttonId': buttonId,
            'buttonName': diamond['des'],
        }
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        chargeinfo['chargeType'] = 'CAT_THIRDPAY'
        chargeinfo_dump = json.dumps(chargeinfo)
        datas = ['state', 0, 'charge', chargeinfo_dump, 'createTime', timestamp]
        mo = TyContext.Cls_MsgPack()
        mo.setCmd('consume')
        prodOrderId = ''
        ###
        if 'R' in buttonId:
            fail, prodOrderId = False, TyContext.ServerControl.makeChargeOrderIdV3(userId, appId, clientId)
        else:
            fail, prodOrderId = TuyouPayConsume._create_consume_transaction(appId, '', clientId, userId,
                                                                            int(diamond['price']), buttonId,
                                                                            diamond['price'], 1, diamond['des'],
                                                                            prodOrderId, mo)
            if fail:
                return mo

        if 'D' in buttonId:
            consumeInfo = {}
            consumeInfo['prodId'] = buttonId
            consumeInfo['consumeCoin'] = int(diamond['price'])
            consumeInfo['appId'] = appId
            consumeInfo['appInfo'] = ''
            consumeInfo['clientId'] = clientId
            consumeInfo['userId'] = userId
            consumeInfo['prodPrice'] = diamond['price']
            consumeInfo['prodCount'] = 1
            consumeInfo['prodName'] = diamond['des']
            consumeInfo['prodOrderId'] = prodOrderId
            datas.append('consume')
            datas.append(json.dumps(consumeInfo))
        TyContext.RedisPayData.execute('HMSET', 'sdk.charge:' + platformOrderId, *datas)
        TyContext.ftlog.debug('TuYouPayYiWap->charge_data chargeinfo', chargeinfo)

        if buttonId in yiconfig['monthly_prods']:
            is_monthly = '2'
        else:
            is_monthly = '0'
        response = cls.__create_order(phoneType, userId, price, platformOrderId, is_monthly, bindMobile,
                                      diamonds['feecode'], diamonds.get('scheme', 1))
        status = response['status']
        msg = create_errmsg.get(status, response['msg'])
        if int(status) != 0:
            TyContext.ftlog.error('TuYouPayYiWap create_order failed for user', userId,
                                  'orderid', platformOrderId, 'status', status, 'msg', msg)
            chargeinfo['chargeData'] = {'code': 1, 'info': msg}
            if 1 == adaptJsonp:
                ret = {}
                ret['code'] = 1
                ret['info'] = msg
                chargeinfo['chargeData'] = adaptString + '(' + json.dumps(ret) + ')'

            return chargeinfo['chargeData']

        # 此处为了兼容js跨域问题,官网展示
        if 1 == adaptJsonp:
            # chargeinfo['chargeData'] = {'code':0, 'orderid': response['res']['orderid'] }
            ret = {}
            ret['code'] = 0
            ret['orderid'] = response['res']['orderid']
            try:
                ret['fee_url'] = response['res']['fee_url']
            except KeyError:
                pass
            chargeinfo['chargeData'] = adaptString + '(' + json.dumps(ret) + ')'
            # chargeinfo['chargeData'] = adaptString + '([' + '{code:0,orderid:'+ str(response['res']['orderid']) + '}])'
            TyContext.ftlog.debug('TuYouPayYiWap chargeinfo[chargeData]', chargeinfo['chargeData'])
        else:
            chargeinfo['chargeData'] = {'code': 0, 'orderid': response['res']['orderid'],
                                        'fee_url': response['res'].get('fee_url', '')}
        return chargeinfo['chargeData']

    @classmethod
    def __create_order(cls, phoneType, userId, amount, orderPlatformId, is_monthly, bindMobile, paycode, scheme):
        # yiconfig = TyContext.Configure.get_global_item_json('yipaywap_config', {})
        iccid = TyContext.UserSession.get_session_iccid(userId)
        imei = TyContext.UserSession.get_session_imei(userId)
        params = {}
        if phoneType == PHONETYPE_CHINAMOBILE:
            params['corp_type'] = '1'
        elif phoneType == PHONETYPE_CHINAUNION:
            params['corp_type'] = '2'
        else:
            params['corp_type'] = '3'

        params['merc_id'] = cls.merc_id
        params['amount'] = str(amount)
        if iccid:
            params['iccid'] = iccid
        if imei:
            params['imei'] = imei
        params['user_id'] = userId
        params['app_id'] = cls.yipay_appid
        params['site_type'] = '1'
        params['scheme'] = '%s' % scheme
        params['ver'] = '2.0'

        params['pay_code'] = paycode  # yiconfig['paycode_config'][str(amount/100)]
        # 0非包月, 2包月
        params['is_monthly'] = is_monthly
        params['phone'] = bindMobile
        notifyurl = PayHelper.getSdkDomain() + '/v1/pay/yipay/callback'
        params['app_orderid'] = orderPlatformId
        params['ip'] = TyContext.RunHttp.get_client_ip()
        params['ret_url'] = notifyurl
        params['noti_url'] = notifyurl
        params['time'] = str(int(time.time()))
        params['sign'] = cls._cal_sign(params)
        response_msg, final_url = TyContext.WebPage.webget(cls.createorder_url, params)

        TyContext.ftlog.debug('TuYouPayYiWap->charge_data createorder_url', cls.createorder_url, 'params', params,
                              'response_msg', response_msg)
        response = json.loads(response_msg)
        return response

    @classmethod
    def _cal_sign(cls, params):
        params['merc_key'] = cls.yipay_key
        check_str = '&'.join(k + "=" + str(params[k]) for k in sorted(params.keys()) if k != 'sign')
        m = md5()
        m.update(check_str)
        digest = m.hexdigest().lower()
        del params['merc_key']
        return digest

    @classmethod
    def verify_receipt(cls, receiptinfo):
        receiptinfo = TyContext.RunHttp.convertArgsToDict()

        TyContext.ftlog.debug('TuYouPayYiWap->verify_receipt receiptinfo', receiptinfo)
        orderid = receiptinfo['orderid']
        verify_code = receiptinfo['verify_code']
        # 短验目前只有音乐基地
        clientId = receiptinfo.get('clientId', 'Android_3.501_tuyoo.yisdkpay.0-hall6.youyifu.happy')
        yiconfig = TyContext.Configure.get_global_item_json('yipaywap_config:%s' % clientId, {})
        cls.merc_id = str(yiconfig['merc_id'])
        cls.yipay_appid = str(yiconfig['app_id'])
        cls.yipay_key = str(yiconfig['yipay_key'])

        # 此处为了兼容js跨域问题jsonp,官网展示
        if 'callback' in receiptinfo:
            adaptJsonp = 1
            adaptString = receiptinfo['callback']
        else:
            adaptJsonp = 0

        params = {}
        params['merc_id'] = cls.merc_id
        params['app_id'] = cls.yipay_appid
        params['orderid'] = orderid
        params['verify_code'] = verify_code
        params['ver'] = '2.0'

        params['sign'] = cls._cal_sign(params)

        yipaywapconfig = yiconfig  # TyContext.Configure.get_global_item_json('yipaywap_config', {})
        if yipaywapconfig:
            cls.verconfirm_url = yipaywapconfig['verconfirmurl']

        response_msg, final_url = TyContext.WebPage.webget(cls.verconfirm_url, params)

        response = json.loads(response_msg)
        TyContext.ftlog.debug('TuYouPayYiWap->verify_receipt response', response)

        verifyinfo = {}
        if response['res']['code'] in ('0', '200'):
            response['res']['code'] = 0
        verifyinfo['chargeData'] = {'code': response['res']['code'], 'orderid': response['res']['msg']}

        if 1 == adaptJsonp:
            ret = {}
            ret['code'] = response['res']['code']
            ret['orderid'] = response['res']['msg']
            verifyinfo['chargeData'] = adaptString + '(' + json.dumps(ret) + ')'
            TyContext.ftlog.debug('TuYouPayYiWap chargeinfo[chargeData]', verifyinfo['chargeData'])
        return verifyinfo['chargeData']

    @classmethod
    def padding_phonenumber(cls, paddinginfo):
        paddinginfo = TyContext.RunHttp.convertArgsToDict()
        ''' 
        authInfo = paddinginfo['authInfo']
        authUid, _, _ = TyContext.AuthorCode.checkUserAuthorInfo(authInfo)
        if not authUid:
            chargeinfo['chargeData'] = {'code':1, 'info':'用户登录信息超时'} 
        '''
        if 'uid' in paddinginfo:
            userId = str(paddinginfo['uid'])
        else:
            paddinginfo['data'] = {'code': 2, 'info': '参数缺失 uid'}
            return paddinginfo['data']

        bindMobile = TyContext.RedisUser.execute(userId, 'HGET', 'user:' + str(userId), 'bindMobile')

        if bindMobile:
            paddinginfo['data'] = {'code': 0, 'bindMobile': bindMobile}
            return paddinginfo['data']
        else:
            paddinginfo['data'] = {'code': 2, 'info': '取不到用户手机号'}
            return paddinginfo['data']
