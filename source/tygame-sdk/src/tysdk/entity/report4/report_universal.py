#! encoding=utf-8


import json

from tysdk.entity.report4.report_model import ReportModel

__author__ = 'yuejianqiang'


class ReportUniversal(object):
    @classmethod
    def checkOnline(self, rparams, mo):
        appId = rparams['appId']
        userId = rparams['userId']
        # clientId = rparams.get('clientId')
        if int(appId) != 9999:
            ReportModel().checkOnline(appId, userId)
        mo.setResult('code', 0)
        mo.setResult('info', '')

    @classmethod
    def queryOnline(self, params):
        return json.dumps(ReportModel().queryOnline(params['appId'], params['userId']))
