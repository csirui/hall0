#! encoding=utf-8
import time

from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class UniversalUser:
    def increase_user_charge_data(self, userId, appId, clientId, amount, chargeType):
        """
        增加用户的充值数据
        :param userId: 平台用户Id
        :param appId: 平台应用Id
        :param amount: 充值金额（单位元）
        :return: None
        """
        try:
            charge_amount, charge_count = self.get_user_charge_data(userId, appId)
            charge_amount = charge_amount + amount if charge_amount else amount
            charge_count = charge_count + 1 if charge_count else 1
            TyContext.RedisUser.execute(userId, 'HMSET', 'universal_user:%s' % userId,
                                        'charge_amount_%s' % appId, int(charge_amount),
                                        'charge_count_%s' % appId, int(charge_count))
        except:
            TyContext.ftlog.exception()
        try:
            self.increase_client_charge_total_daily(clientId, amount, chargeType)
        except:
            TyContext.ftlog.exception()

    def get_user_charge_data(self, userId, appId):
        """
        获取用户在某个饮应用中充值信息
        :param userId:
        :param appId:
        :return: 总充值钻石数量，总充值次数
        """
        universal_key = 'universal_user:%s' % userId
        charge_amount, charge_count = TyContext.RedisUser.execute(userId, 'HMGET', universal_key,
                                                                  'charge_amount_%s' % appId,
                                                                  'charge_count_%s' % appId)
        if not charge_amount:
            charge_amount = 0
        if not charge_count:
            charge_count = 0
        return float(charge_amount), float(charge_count)

    def get_user_charge_amount(self, userId, appId):
        return self.get_user_charge_data(userId, appId)[0]

    def get_user_charge_count(self, userId, appId):
        return self.get_user_charge_data(userId, appId)[1]

    def get_client_charge_total_daily(self, clientId, chargeType):
        """
        增加clientId的充值金额记录
        :param clientId:
        :param chargeType:
        :return:
        """
        format = '%Y%m%d'
        day = time.strftime(format, time.localtime(time.time()))
        key = 'client_charge_daily:%s:%s' % (clientId, day)
        sum0, sum1 = TyContext.RedisPayData.execute('HMGET', key, chargeType, 'all')
        return sum0 if sum0 else 0, sum1 if sum1 else 0

    def increase_client_charge_total_daily(self, clientId, amount, chargeType):
        """
        增加clientId的充值金额记录
        :param clientId:
        :param amount:
        :param chargeType:
        :return:
        """
        format = '%Y%m%d'
        day = time.strftime(format, time.localtime(time.time()))
        key = 'client_charge_daily:%s:%s' % (clientId, day)
        sum0, sum1 = self.get_client_charge_total_daily(clientId, chargeType)
        TyContext.RedisPayData.execute('HMSET', key, chargeType, sum0 + amount, 'all', sum1 + amount)
        TyContext.RedisPayData.execute('EXPIRE', key, 86400)
