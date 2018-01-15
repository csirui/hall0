#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class ReportAndroid:
    @classmethod
    def onClick(cls, params):
        TyContext.ftlog.debug('ReportAndroid->onClick params=', params)
        return 'success'
