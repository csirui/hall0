# -*- coding=utf-8 -*-
import base64
import json

from tyframework.context import TyContext
from tysdk.entity.user.account import Account


class HttpUser(object):
    JSONPATHS = None
    HTMLPATHS = None

    @classmethod
    def getJsonPaths(cls):
        if not HttpUser.JSONPATHS:
            HttpUser.JSONPATHS = {
                '/open/v1/user/loginByAccount': cls.doLoginByAccount,
                '/open/v1/user/loginBySnsId': cls.doLoginBySnsId,
                '/open/v1/user/randomAccount': cls.doRandAccount,
                '/open/v1/user/registerByAccount': cls.doRegisterByAccount,
                '/open/v1/user/sms': cls.doUserSms,
                '/open/v1/user/registerByEmail': cls.doRegisterByEmail,
                '/open/v1/user/loginByEmail': cls.doLoginByEmail,
                '/open/v1/user/loginByMobile': cls.doLoginByMobile,
                '/open/v1/user/loginByGuest': cls.doLoginByGuest,
                '/open/v1/user/loginByTyId': cls.doLoginByTyId,
                '/open/v1/user/loginByTyId2': cls.doLoginByTyId2,
                '/open/v1/user/changePwd': cls.doChangePwd,
                '/open/v1/user/changeGuestPwd': cls.doChangeGuestPwd,
                '/open/v1/user/bindEmail': cls.doBindEmail,
                '/open/v1/user/bindMobile': cls.doBindMobile,
                '/open/v1/user/getAccountByDevId': cls.doGetAccountByDevId,
                '/open/v1/user/loginBySnsIdNew': cls.doLoginBySnsId2,
                '/open/v1/user/registerTyId': cls.doRegisterTyId,
                '/open/v1/api/getUserInfo': cls.doGetUserInfo,
                '/open/v3/user/reportLbs': cls.doReportLbs,
            }
        return HttpUser.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not HttpUser.HTMLPATHS:
            HttpUser.HTMLPATHS = {
                #                 '/open/v1/user/smsCallback': cls.doUserSmsCallback,
                '/open/va/user/smsCallback': cls.doUserSmsCallback,
            }
        return HttpUser.HTMLPATHS

    @classmethod
    def doRandAccount(cls, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        mo = TyContext.Cls_MsgPack()
        Account.doRandom(mo)
        return mo

    @classmethod
    def doUserSms(cls, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'userId', 'appId'])
        mo = TyContext.Cls_MsgPack()
        Account.doLoginSms(msg, mo)
        return mo

    @classmethod
    def doUserSmsCallback(cls, rpath):
        rparam = TyContext.RunHttp.convertArgsToDict()
        TyContext.ftlog.info('HttpUser.doUserSmsCallback->rparam=', rparam)
        if rparam['args'] != None:
            try:
                msg = TyContext.Cls_MsgPack()
                mobile = rparam['args'].split(',')[2]
                content = rparam['args'].split(',')[3]
                contentData = base64.decodestring(content.replace('%3d', '='))
                TyContext.ftlog.info('HttpUser.doUserSmsCallback->contentData=', contentData)
                params = contentData.split('|');
                userId = ''
                clientId = ''
                if len(params) == 2:
                    userId = params[0]
                    clientId = params[1]

                TyContext.RunHttp.set_request_arg('clientId', clientId)
                TyContext.RunHttp.set_request_arg('userId', userId)
                __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
                if __ret__ != False:
                    return __ret__

                msg.setParam('userId', userId)
                msg.setParam('clientId', clientId)
                msg.setParam('mobile', mobile)
                Account.doRegisterMobile(msg)
            except:
                TyContext.ftlog.exception()
                TyContext.ftlog.info('HttpUser.doUserSmsCallback->ERROR, get mobile error !! rparam=', rparam)
            return '0'

    @classmethod
    def doLoginByAccount(cls, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__
        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'appId', 'userAccount', 'userPwd'])
        mo = TyContext.Cls_MsgPack()
        Account.doLogin(msg, mo)
        return mo

    @classmethod
    def doLoginBySnsId(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'appId', 'snsId', 'snsToken'])
        mo = TyContext.Cls_MsgPack()
        Account.doLogin(msg, mo)
        return mo

    @classmethod
    def doLoginByEmail(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'email', 'userPwd', 'appId', 'phoneType'])
        mo = TyContext.Cls_MsgPack()
        Account.doLoginByEmail(msg, mo)
        return mo

    @classmethod
    def doLoginByMobile(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'mobile', 'userPwd', 'appId', 'phoneType'])
        mo = TyContext.Cls_MsgPack()
        Account.doLoginByMobile(msg, mo)
        return mo

    @classmethod
    def doLoginByGuest(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(
            ['deviceId', 'clientId', 'appId', 'userId', 'userPwd', 'phoneType', 'deviceName'])
        mo = TyContext.Cls_MsgPack()
        Account.doLoginByGuest(msg, mo)
        return mo

    @classmethod
    def doLoginByTyId(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'appId', 'userId', 'userPwd', 'phoneType'])
        mo = TyContext.Cls_MsgPack()
        Account.doLoginByTyId(msg, mo)
        return mo

    @classmethod
    def doLoginByTyId2(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'appId', 'userId', 'userPwd', 'phoneType'])
        msg.setParam('apiVer', 2)
        mo = TyContext.Cls_MsgPack()
        Account.doLoginByTyId(msg, mo)
        return mo

    @classmethod
    def doRegisterByAccount(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'appId', 'userAccount', 'userPwd'])
        mo = TyContext.Cls_MsgPack()
        Account.doRegister(msg, mo)
        return mo

    @classmethod
    def doRegisterByEmail(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['email', 'userPwd', 'deviceId', 'clientId', 'appId'])
        mo = TyContext.Cls_MsgPack()
        Account.doRegisterEmail(msg, mo)
        return mo

    @classmethod
    def doChangePwd(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['authInfo', 'oldPwd', 'newPwd'])
        mo = TyContext.Cls_MsgPack()
        Account.doChangePwd(msg, mo)
        return mo

    @classmethod
    def doChangeGuestPwd(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['authInfo', 'userPwd'])
        mo = TyContext.Cls_MsgPack()
        Account.doChangeGuestPwd(msg, mo)
        return mo

    @classmethod
    def doBindEmail(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['authInfo', 'userId', 'email', 'userPwd', 'appId', 'clientId'])
        mo = TyContext.Cls_MsgPack()
        Account.doBindByEmail(msg, mo)
        return mo

    @classmethod
    def doBindMobile(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['authInfo', 'userId', 'mobile'])
        mo = TyContext.Cls_MsgPack()
        Account.doBindByMobile(msg, mo)
        return mo

    @classmethod
    def doGetAccountByDevId(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'appId'])
        mo = TyContext.Cls_MsgPack()
        Account.getAccountByDevId(msg, mo)
        return mo

    @classmethod
    def doLoginBySnsId2(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'appId', 'snsId', 'snsToken', 'userId'])
        mo = TyContext.Cls_MsgPack()
        Account.doLoginBySnsId(msg, mo)
        return mo

    @classmethod
    def doGetUserInfo(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['userId', 'appId'])
        mo = TyContext.Cls_MsgPack()
        Account.doGetUserInfo(msg, mo)
        return mo

    @classmethod
    def doRegisterTyId(self, rpath):

        __ret__ = TyContext.ServerControl.checkLoginForbid(rpath)
        if __ret__ != False:
            return __ret__

        msg = TyContext.RunHttp.convertToMsgPack(['deviceId', 'clientId', 'appId', 'phoneType', 'deviceName'])
        mo = TyContext.Cls_MsgPack()
        Account.doRegisterTyId(msg, mo)
        return mo

    @classmethod
    def doReportLbs(cls, rpath):
        """ 处理客户端上报地理位置
        """

        response = TyContext.Cls_MsgPack()
        response.setCmd('reportLbs')
        user_id = TyContext.RunHttp.getRequestParamInt('userId')
        longitude = TyContext.RunHttp.getRequestParam('geoLon')
        lantitude = TyContext.RunHttp.getRequestParam('geoLat')
        TyContext.ftlog.debug('doReportLbs userid=', user_id, 'position:', longitude, lantitude)
        if not user_id or not longitude or not lantitude:
            TyContext.ftlog.error('doReportLbs parameter error: userid=', user_id,
                                  'position:', longitude, lantitude)
            response.setResult('code', 1)
            return response

        try:
            longitude = (float)(longitude)
            lantitude = (float)(lantitude)
        except:
            TyContext.ftlog.error('doReportLbs long/lant error: userid=', user_id,
                                  'position:', longitude, lantitude)
            response.setResult('code', 1)
            return response

        zip_code, name = TyContext.CityLocator.calculate_province_code_and_name(longitude,
                                                                                lantitude)
        city_code = [zip_code, name]
        TyContext.ftlog.info('doReportLbs userid=', user_id, 'calculated location:', city_code)
        TyContext.RedisUser.execute(user_id, 'hmset', 'user:' + str(user_id), 'city_code', json.dumps(city_code))

        response.setResult('code', 0)

        # set online_geo table
        game_id = TyContext.RunHttp.getRequestParamInt('appId')
        geohash_int = TyContext.GeoHash.encode(lantitude, longitude)
        if game_id and geohash_int:
            # first del it from offline_geo table
            TyContext.RedisOnlineGeo.execute('zrem', 'offline_geo:%d' % game_id, user_id)
            # add to online_geo table
            TyContext.RedisOnlineGeo.execute('zadd', 'online_geo:%d' % game_id, geohash_int, user_id)
        return response
