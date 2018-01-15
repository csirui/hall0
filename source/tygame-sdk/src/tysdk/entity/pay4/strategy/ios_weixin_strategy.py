#! encoding=utf-8
from tyframework.context import TyContext
from tysdk.entity.user3.account_game_data import AccountGameData
from tysdk.entity.user4.universal_user import UniversalUser

__author__ = 'yuejianqiang'


class TuYooIOSPayWeixinStrategy:
    def __init__(self, strategy_name, charge_type=None):
        self.strategy_name = strategy_name
        self.charge_type = charge_type

    def __call__(self, **kwds):
        appId = kwds['appId']
        userId = kwds['userId']
        clientId = kwds['clientId']
        ios_control = TyContext.Configure.get_global_item_json('ios_weinxin_pay_control', {})
        if self.strategy_name:
            strategy_control = ios_control.get(self.strategy_name, {})
            # 策略名称错误返回失败
            if not strategy_control:
                return False
            #####################################################
            #  充值金额限制
            #####################################################
            charge_limit = strategy_control.get('charge_limit', {})
            if charge_limit:
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'charge_limit=%s' % charge_limit)
                # 充值次数
                charge_amount_threshold = charge_limit.get('charge_amount', 0)
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'user_charge_amount=%s' % UniversalUser().get_user_charge_amount(userId, appId))
                if charge_amount_threshold > 0 and UniversalUser().get_user_charge_amount(userId,
                                                                                          appId) < charge_amount_threshold:
                    return False
                # 充值金额
                charge_count_threshold = charge_limit.get('charge_count', 0)
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'user_charge_count=%s' % UniversalUser().get_user_charge_count(userId, appId))
                if charge_count_threshold > 0 and UniversalUser().get_user_charge_count(userId,
                                                                                        appId) < charge_count_threshold:
                    return False
                # 此包的总充值金额限制
                charge_type_amount, charge_type_total = UniversalUser().get_client_charge_total_daily(clientId,
                                                                                                      self.charge_type)
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'charge_type=%s charge_type_amount=%s charge_type_total=%s' % (
                #    self.charge_type, charge_type_amount, charge_type_total))
                if self.charge_type not in charge_limit:
                    return False
                # 充值类型限额为百分比
                if charge_type_total > 0 and charge_type_amount * 100 > charge_type_total * charge_limit[
                    self.charge_type]:
                    return False
            ####################################################
            # 充值时间限制
            #####################################################
            # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'strategy_control=%s' % strategy_control)
            # 当天时间阈值
            today_threshold = strategy_control.get('today', 0)
            # 累计时间阈值
            total_threshold = strategy_control.get('total', 0)
            # 3天时间阈值
            day3_threshold = strategy_control.get('day3', 0)
            # 7天时间阈值
            day7_threshold = strategy_control.get('day7', 0)
            # vip阈值
            vip_threshold = strategy_control.get('vip', 0)
            # 合并规则
            operator = strategy_control.get('operator', 'and')
            flag_list = []
            if int(today_threshold):
                today_time = AccountGameData.get_user_today_time(appId, userId)
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'today_time=%s' % today_time)
                flag_list.append(int(today_time) > today_threshold)
            if int(total_threshold):
                total_time = AccountGameData.get_user_total_time(appId, userId)
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'total_time=%s' % total_time)
                flag_list.append(int(total_time) > total_threshold)
            if int(vip_threshold):
                vip = AccountGameData.get_user_vip(appId, userId)
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'vip=%s' % vip)
                flag_list.append(int(vip) > int(vip_threshold))
            if int(day3_threshold):
                day3_total = AccountGameData.get_user_day3_time(appId, userId)
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'day3_total=%s' % day3_total)
                flag_list.append(day3_total > day3_threshold)
            if int(day7_threshold):
                day7_total = AccountGameData.get_user_day7_time(appId, userId)
                # TyContext.ftlog.info('TuYooIOSPayWeixinStrategy', 'day7_total=%s' % day7_total)
                flag_list.append(day7_total > day7_threshold)
            if operator.lower() == 'and':
                test_flag = reduce(lambda x, y: x and y, flag_list, True)
            else:
                test_flag = reduce(lambda x, y: x or y, flag_list, False)
        else:
            test_flag = False
        return test_flag
