#! encoding=utf-8
from tyframework.context import TyContext
from tysdk.entity.report4.report_appcoach import ReportAppcoach
from tysdk.entity.report4.report_gdt import ReportGDT
from tysdk.entity.report4.report_mobvista import ReportMobVista
from tysdk.entity.report4.report_zht import ReportZHT

__author__ = 'yuejianqiang'


class ReportIOS:
    def __init__(self):
        self.report_list = [ReportGDT(), ReportZHT(), ReportMobVista(), ReportAppcoach()]

    def on_user_create(self, userId, rparams):
        TyContext.ftlog.info('ReportIOS->on_user_create', 'userId', userId, 'rparams', rparams)
        if rparams:
            datas = reduce(tuple.__add__, rparams.items())
        else:
            datas = ('key', 'value')
        idfa = rparams.get('idfa', '')
        imei = rparams.get('imei', '')
        if idfa or imei:
            self.handle_register(userId, rparams)
        else:
            key = 'report:user:%s' % userId
            TyContext.RedisPayData.execute('HMSET', key, *datas)
            TyContext.RedisPayData.execute('EXPIRE', key, 60)

    def on_user_login(self, userId, rparams):
        TyContext.ftlog.info('ReportIOS->on_user_login', 'userId', userId, 'rparams', rparams)
        key = 'report:user:%s' % userId
        # 是否第一次注册
        if TyContext.RedisPayData.execute('DEL', key):
            TyContext.ftlog.info('ReportIOS->on_user_login', 'userId=%s' % userId, 'rparams', rparams)
            self.handle_register(userId, rparams)

    def handle_register(self, userId, rparams):
        TyContext.ftlog.info('ReportIOS->handle_register', 'userId', userId, 'rparams', rparams)
        for report in self.report_list:
            report.handle_register(userId, rparams)
