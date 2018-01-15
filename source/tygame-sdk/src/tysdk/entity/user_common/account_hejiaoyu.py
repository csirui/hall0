# -*- coding=utf-8 -*-

class AccountHejiaoyu():
    @classmethod
    def doGetUserInfo(cls, params, snsId):
        name = params['hejiaoyu_name']

        if name:
            params['deviceName'] = name
            params['name'] = '和-' + name

        return True
