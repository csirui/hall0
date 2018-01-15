# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class Fengkong(object):
    @classmethod
    def is_ip_limited(cls, clientip, clientid, paytype):
        TyContext.ftlog.debug('Fengkong is_ip_limited clientip', clientip,
                              'clientId', clientid, 'paytype', paytype)
        if not paytype or not clientid or not clientip:
            return False

        waivedlist = TyContext.Configure.get_global_item_json(
            'paytype.msg.speed.limited.waived.clientid.list', [])
        limit = TyContext.Configure.get_global_item_json(
            'single_ip_day_count_limit', {})
        limit = int(limit.get(paytype, -1))
        TyContext.ftlog.debug('Fengkong is_ip_limited', 'limit', limit,
                              'waivedlist', waivedlist)
        if limit <= 0 or not clientid or not waivedlist or clientid in waivedlist:
            return False

        count = TyContext.RedisPayData.execute(
            'HGET', 'paytype_ip_control:%s' % paytype, clientip)
        TyContext.ftlog.debug('Fengkong is_ip_limited count', count)
        if not count or count < limit:
            return False

        TyContext.ftlog.info(
            'paytype_ip_control clientip %s paytype %s exceed limit %d'
            % (clientip, paytype, limit))
        return True
