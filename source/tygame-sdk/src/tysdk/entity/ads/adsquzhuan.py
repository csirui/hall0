# -*- coding: utf-8 -*-

import json
from hashlib import md5

from advertise import AdvertiseService
from tyframework.context import TyContext


class AdsQuzhuan(object):
    serverKey = '123456'

    @classmethod
    def get_spname(cls):
        return 'quzhuan'

    @classmethod
    def ads_clicked(cls, rparams):
        TyContext.ftlog.debug('AdsQuzhuan->ads_clicked:', rparams)
        try:
            clickIp = rparams['clickIp']
            mac = rparams['mac']
            idfa = rparams['idfa']
            appId = rparams['appId']
            token = rparams['token']
            callbackUrl = rparams['callBackUrl']
        except Exception as e:
            TyContext.ftlog.error('AdsQuzhuan->ads_clicked ERROR: ', e)
            return cls.resultThirdMessage(1, str(e))

        signStr = cls.serverKey + clickIp + idfa + mac
        signature = md5(signStr).hexdigest()
        TyContext.ftlog.debug(
            'AdsQuzhuan->user_activated sign string is: [%s], signature is: [%s]' % (signStr, signature))

        if 0 != cmp(token, signature):
            TyContext.ftlog.error(
                'AdsQuzhuan->ads_clicked signature Error: excepted sign is: [%s], calculate sign is:[%s]'
                % (token, signature))
            return cls.resultThirdMessage(2, 'sign error')

        ids = {}
        ids['iosappid'] = appId
        ids['mac'] = ''
        ids['macmd5'] = ''
        ids['idfa'] = idfa.lower()
        strNote = json.dumps({'callback': callbackUrl})
        AdvertiseService.record_click(ids, clickIp, cls.get_spname(), strNote)
        TyContext.ftlog.debug('AdsQuzhuan.ads_clicked ids:', ids, 'strNote', strNote)
        return cls.resultThirdMessage()

    @classmethod
    def user_created(cls, params):
        try:
            iosappid = params['iosappid']
            acttime = params['acttime']
            noteStr = params['note']
            noteJson = json.loads(noteStr)
            notifyUrl = noteJson['callback']
        except Exception as e:
            TyContext.ftlog.error('AdsQuzhuan->user_activated ERROR:', e)
            return cls.returnSelfMessage(-1, str(e))
        ip = params.get('ip', 'null')
        userId = params.get('userId', 'null')

        signStr = str(iosappid) + str(acttime) + str(ip) + str(cls.serverKey)
        signature = md5(signStr).hexdigest()
        TyContext.ftlog.debug(
            'AdsQuzhuan->user_activated sign string is: [%s], signature is: [%s]' % (signStr, signature))

        requestParamAdd = '&wifiMac={wifiMac}&sign={sign}&acttime={acttime}&ip={ip}&appVersion={appVersion}&appUserId={appUserId}'
        requestParamAdd = requestParamAdd.format(wifiMac='null', sign=signature, acttime=acttime, ip=ip,
                                                 appVersion='null', appUserId=userId)
        requestUrl = 'http://' + notifyUrl + requestParamAdd
        TyContext.ftlog.debug('AdsQuzhuan->user_activated requestUrl:', requestUrl)
        try:
            response, _ = TyContext.WebPage.webget(requestUrl, method_='GET')
            ponse = json.loads(response)
            msg = cls.returnSelfMessage(ponse['code'], ponse['msg'])
            TyContext.ftlog.debug('AdsQuzhuan->user_activated request relult:', msg)
        except Exception, e:
            TyContext.ftlog.error('AdsQuzhuan->user_activated ERROR:', e)
            return cls.returnSelfMessage(-1, str(e))
        return msg

    '''
    http://42.62.53.158.1:8080/renwuke/api/adCallBack/ios/auto?
    appId={appId}&wifiMac={wifiMac}&mac={mac}&idfa={idfa}&sign={sign}
    &clktime={clktime}&acttime={acttime}&clkip={clkip}&ip={ip}&appVersion={appVersion}&appUserId={appUserId}
    '''

    @classmethod
    def user_activated(cls, params):
        userId = params.get('userId', 'null')
        idfa = params.get('idfa', 'null')
        TyContext.ftlog.info(
            'AdsQuzhuan->user_activated user {userId} from {platName} which phone idfa is {idfa} has actived'.format(
                userId=userId,
                platName=cls.get_spname(),
                idfa=idfa
            ))
        return cls.returnSelfMessage(0, 'success')

    @classmethod
    def resultThirdMessage(cls, code=0, errmsg='success'):
        msg = {}
        msg['code'] = code
        msg['msg'] = errmsg
        return json.dumps(msg)

    @classmethod
    def returnSelfMessage(cls, code, errmsg):
        msg = {}
        msg['ret'] = code
        msg['msg'] = errmsg
        return json.dumps(msg)
