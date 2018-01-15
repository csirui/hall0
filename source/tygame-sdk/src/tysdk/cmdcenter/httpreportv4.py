#! encoding=utf-8
from tysdk.entity.report4.report_android import ReportAndroid
from tysdk.entity.report4.report_appcoach import ReportAppcoach
from tysdk.entity.report4.report_gdt import ReportGDT
from tysdk.entity.report4.report_jrtt import ReportJRTT
from tysdk.entity.report4.report_mobvista import ReportMobVista
from tysdk.entity.report4.report_universal import ReportUniversal
from tysdk.entity.report4.report_zht import ReportZHT
from tysdk.entity.report4.report_zplay import ReportZPlay

__author__ = 'yuejianqiang'

from tyframework.context import TyContext
from tysdk.entity.user3.account_check import AccountCheck

__author__ = 'yuejianqiang'


class HttpReportV4(object):
    JSONPATHS = None
    HTMLPATHS = None
    error_sing = None

    @classmethod
    def getJsonPaths(cls):
        if not cls.JSONPATHS:
            cls.JSONPATHS = {
                '/v4/report/online/check': cls.checkOnline,  # 报告游戏在线时间queryOneline
            }
        return cls.JSONPATHS

    @classmethod
    def getHtmlPaths(cls):
        if not cls.HTMLPATHS:
            cls.HTMLPATHS = {
                '/v4/report/online/query': cls.queryOnline,
                '/v4/report/zplay/idfa': cls.reportZPlay,  # ZPlay上报平台
                '/v4/report/zplay/idfa2': cls.reportZPlay2,  # ZPlay上报平台
                '/v4/report/jrtt/idfa': cls.reportJRTT,  # 今日头条上报IDFA
                '/v4/report/android/click': cls.reportAndroidClick,  # 广告平台上报
                '/v4/report/gdt/click': cls.reportGDTClick,  # 广告平台上报
                '/v4/report/zht/click': cls.reportZhtClick,  # 智慧推广告平台
                '/v4/report/mobvista/click': cls.reportMobVista,  # MobVista
                '/v4/report/appcoach/click': cls.reportAppcoach,  # Appcoach
            }
        return cls.HTMLPATHS

    @classmethod
    def checkOnline(cls, rpath):
        isReturn, params = AccountCheck.check_userv4(rpath)
        if isReturn:
            return params
        mo = TyContext.Cls_MsgPack()
        ReportUniversal.checkOnline(params, mo)
        return mo

    @classmethod
    def queryOnline(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        return ReportUniversal.queryOnline(params)

    @classmethod
    def reportZPlay(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        return ReportZPlay.reportZPlay(params)

    @classmethod
    def reportZPlay2(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        return ReportZPlay.reportZPlay2(params)

    @classmethod
    def reportJRTT(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        return ReportJRTT.reportIDFA(params)

    @classmethod
    def reportAndroidClick(cls, rpath):
        params = TyContext.RunHttp.convertArgsToDict()
        return ReportAndroid.onClick(params)

    @classmethod
    def reportGDTClick(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        return ReportGDT.handle_click(rparams)

    @classmethod
    def reportZhtClick(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        return ReportZHT.handle_click(rparams)

    @classmethod
    def reportMobVista(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        return ReportMobVista.reportMobiVista(rparams)

    @classmethod
    def reportAppcoach(cls, rpath):
        rparams = TyContext.RunHttp.convertArgsToDict()
        return ReportAppcoach.reportAppcoach(rparams)
