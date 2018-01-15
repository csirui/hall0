# -*- coding=utf-8 -*-

import json
from hashlib import md5

from tyframework.context import TyContext


class TuYouPay360SNS():
    URL_ACCSEE_360PAY = 'https://openapi.360.cn/oauth2/access_token?grant_type=authorization_code' + \
                        '&code=%s&client_id=%s&client_secret=%s&redirect_uri=oob&scope=pay'

    @classmethod
    def get_360_app_info(cls, appId, clientId):
        client_ids = TyContext.Configure.get_game_item_json(appId, 'account.360.client.version', {})
        clientver = ''
        if clientId in client_ids:
            clientver = str(client_ids[clientId])
        client_id = TyContext.Configure.get_game_item_str(appId, 'account.360.client.id' + clientver)
        client_secret = TyContext.Configure.get_game_item(appId, 'account.360.client.id.' + clientver)
        return client_id, client_secret

    @classmethod
    def doBuyStraight(self, userId, params, mo):
        TyContext.RunHttp.getRequestParamJs(params, '360snscode', '')
        snscode = params['360snscode']
        clientId = params['clientId']
        appId = params['appId']
        client_id, client_secret = self.get_360_app_info(appId, clientId)

        TyContext.ftlog.info('TuYouPay360SNS->doBuyStraight appId=', appId, 'clientId=', clientId,
                             'snscode=', snscode, 'app_client_id=', client_id, 'app_client_secret', client_secret)

        tokenurl = self.URL_ACCSEE_360PAY % (snscode, client_id, client_secret)
        response, tokenurl = TyContext.WebPage.webget(tokenurl)
        TyContext.ftlog.info('TuYouPay360SNS->doBuyStraight->snscode=', snscode, 'response=', response)

        error_info = None
        response_json = None
        try:
            response_json = json.loads(response)
        except:
            response_json = {}
            error_info = {'error_code': -1, 'error_msg': "360返回值错误", 'content': str(response)}

        access_token = response_json.get('access_token', '')
        expires_in = response_json.get('expires_in', '')
        scope = response_json.get('scope', '')
        refresh_token = response_json.get('refresh_token', '')

        if access_token == '':
            if error_info == None:
                error_info = response_json

        if error_info == None:
            error_info = {'error_code': 0, 'error_msg': "OK"}

        from tysdk.entity.paythird.helper import PayHelper
        notify_uri = PayHelper.getSdkDomain() + '/v1/pay/360sns/callback'
        payData = {'access_token': access_token,
                   'expires_in': expires_in,
                   'scope': scope,
                   'refresh_token': refresh_token,
                   'error_info': error_info,
                   'notify_uri': notify_uri}

        params['payData'] = payData
        mo.setResult('payData', payData)
        pass

    @classmethod
    def verify_sign(self, app_secret):

        rparam = TyContext.RunHttp.convertArgsToDict()

        sk = rparam.keys()
        sk.sort()
        sings = []
        sign = ''
        for k in sk:
            v = str(rparam[k])
            if k == 'sign':
                sign = v.lower()
            elif k != 'sign_return' and len(v) > 0:
                sings.append(v)
        sings.append(app_secret)
        rstr = '#'.join(sings)
        m = md5()
        m.update(rstr)
        mysign = m.hexdigest().lower()
        TyContext.ftlog.debug('do360CallbackSNS->buildMySign->', sign, mysign, rstr)
        if mysign == sign:
            return True, rparam
        return False, rparam

    @classmethod
    def do360CallbackSNS(self, rpath):

        orderPlatformId = TyContext.RunHttp.getRequestParam('app_order_id', '')
        TyContext.RunMode.get_server_link(orderPlatformId)

        baseinfo = TyContext.RedisPayData.execute('HGET', 'platformOrder:' + str(orderPlatformId), 'PAY_STATE_IDEL')
        baseinfo = json.loads(baseinfo)
        appId = int(baseinfo.get('appId', 0))
        clientId = baseinfo.get('clientId', '')
        client_id, client_secret = self.get_360_app_info(appId, clientId)
        TyContext.ftlog.info('do360CallbackSNS->orderPlatformId=', orderPlatformId,
                             'appId=', appId, 'clientId=', clientId,
                             'client_id=', client_id, 'client_secret=', client_secret)
        isOK, rparam = self.verify_sign(client_secret)
        if isOK != True:
            TyContext.ftlog.info('do360CallbackSNS->ERROR, sign error !! ')
            return 'error-sign-verify-false'

        from tysdk.entity.pay.pay import TuyouPay
        if rparam.get('gateway_flag') != 'success':
            # 长连接通知，客户端支付失败
            TyContext.ftlog.error('do360CallbackSNS error, charge return error !!!')
            TuyouPay.deliveryChargeError(orderPlatformId, rparam, u'360SNS支付失败', 1)
            return 'ok'

        trade_status = 'TRADE_FINISHED'
        total_fee = float(rparam.get('amount', -1))
        if total_fee > 0:
            total_fee = total_fee / 100
        isOk = TuyouPay.doBuyChargeCallback(orderPlatformId, total_fee, trade_status, rparam)
        if isOk:
            return 'ok'
        else:
            return 'error-game-chanrge-exception'
        pass
