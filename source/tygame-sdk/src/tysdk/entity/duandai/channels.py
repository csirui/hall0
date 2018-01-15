# -*- coding=utf-8 -*-

import json
import time
from operator import itemgetter

from datetime import datetime

from tyframework.context import TyContext

prov2zc_dict = {
    # '全国' :  0,
    u'北京': 10,
    u'上海': 20,
    u'天津': 30,
    u'重庆': 40,
    u'内蒙古': 1,
    u'山西': 3,
    u'河北': 5,
    u'辽宁': 11,
    u'吉林': 13,
    u'黑龙江': 15,
    u'江苏': 21,
    u'安徽': 23,
    u'山东': 25,
    u'浙江': 31,
    u'江西': 33,
    u'福建': 35,
    u'湖南': 41,
    u'湖北': 43,
    u'河南': 45,
    u'广东': 51,
    u'广西': 53,
    u'贵州': 55,
    u'海南': 57,
    u'四川': 61,
    u'云南': 65,
    u'陕西': 71,
    u'甘肃': 73,
    u'宁夏': 75,
    u'青海': 81,
    u'新疆': 83,
    u'西藏': 85,
    u'香港': -1,
    u'澳门': -1,
    u'台湾': -1,
    # u'香港' : 999077,
    # u'澳门' : 999078,
    # u'台湾' : 86,
}


class Channels(object):
    # XXX make this called when config changed
    @classmethod
    def init(cls):
        cls._duandai_channels = {
            'chinaMobile': {
                # price -> {provid -> [paytype list]}
            },
            'chinaUnion': {},
            'chinaTelecom': {},
        }

        global prov2zc_dict
        channels_config = TyContext.Configure.get_global_item_json('channels_config', [])
        for channel_config in channels_config:
            paytype = channel_config['paytype']
            for operator_config in channel_config['availability']:
                operator = operator_config['operator']
                operator_control = cls._duandai_channels[operator]
                for price_config in operator_config['price_list']:
                    price = price_config['price']
                    try:
                        price_control = operator_control[price]
                    except:
                        price_control = {}
                        operator_control[price] = price_control

                    if 0 == price_config['control'][0]['on']:
                        for control in price_config['control'][1:]:
                            provid = control['prov']
                            provid = prov2zc_dict[provid]
                            try:
                                price_control[provid].remove(paytype)
                            except KeyError:
                                price_control[provid] = []
                            except ValueError:
                                pass
                            try:
                                price_control[0].remove(paytype)
                            except KeyError:
                                price_control[0] = []
                            except ValueError:
                                pass
                        continue

                    for control in price_config['control'][1:]:
                        provid = control['prov']
                        provid = prov2zc_dict[provid]
                        if 1 == control['on']:
                            try:
                                if paytype not in price_control[provid]:
                                    price_control[provid].append(paytype)
                            except KeyError:
                                price_control[provid] = [paytype]
                            try:
                                if paytype not in price_control[0]:
                                    price_control[0].append(paytype)
                            except KeyError:
                                price_control[0] = [paytype]
                        else:
                            try:
                                price_control[provid].remove(paytype)
                            except KeyError:
                                price_control[provid] = []
                            except ValueError:
                                pass

        TyContext.ftlog.info('Channels init get', cls._duandai_channels)

    def __init__(self):
        self._channels_volume_control = TyContext.Configure.get_global_item_json(
            'channels_volume_control')
        self._channels_volume = TyContext.RedisPayData.execute('GET', 'channels_volume')
        if self._channels_volume:
            self._channels_volume = json.loads(self._channels_volume)
        TyContext.ftlog.debug('Channels channels_volume_control',
                              self._channels_volume_control, self._channels_volume)

    def _drop_capped_paytypes(self, operator, province, candidates):

        def _capped(paytype):
            cfg_by_op = self._channels_volume_control[operator]
            try:
                cfg_by_prov = cfg_by_op[province]
            except:
                cfg_by_prov = cfg_by_op['0']
            try:
                cap = cfg_by_prov[paytype]['day_max']
            except:
                cap = -1
            try:
                volume = self._channels_volume[operator][paytype]
            except:
                volume = 0
            if cap >= 0 and volume >= cap:
                TyContext.ftlog.info('_drop_capped_paytypes drop', paytype,
                                     'whose cap is', cap)
                return True
            return False

        TyContext.ftlog.debug('_drop_capped_paytypes before', candidates)
        can = [paytype for paytype in candidates if not _capped(paytype)]
        TyContext.ftlog.debug('_drop_capped_paytypes after', can)
        return can

    def _get_default_channels(self, clientid, operator, province=None):
        paycodes = TyContext.Configure.get_global_item_json('paycodes',
                                                            clientid=clientid)
        channels = []
        paytypes_by_op = {"chinaMobile": ['ydjd', 'ydmm'],
                          "chinaUnion": ['liantong.wo'],
                          "chinaTelecom": ['aigame']}
        # 根据省判断ydmm、ydjd的先后顺序
        if province and operator == 'chinaMobile':
            global prov2zc_dict
            channels_defalut_config = TyContext.Configure.get_global_item_json('channels_defalut_config', {})
            if 'ydmm' in channels_defalut_config and channels_defalut_config['ydmm']:
                for prov in channels_defalut_config['ydmm']:
                    provid = prov2zc_dict[prov]
                    if provid == int(province):
                        paytypes_by_op['chinaMobile'] = ['ydmm', 'ydjd']
                        break

        precedence_base = 10
        share = 100
        for paytype in paytypes_by_op[operator]:
            try:
                appid = paycodes[paytype]['appid']
            except:
                pass
            else:
                channel_main = {"channel": "_".join([paytype, appid]),
                                "share": share, "precedence": precedence_base}
                channels.append(channel_main)
                precedence_base += 10
                share = 0

        backup_channels = TyContext.Configure.get_global_item_json(
            'backup_channels',
            [{"channel": "yipay", "share": 0, "precedence": precedence_base},
             {"channel": "gefu", "share": 0, "precedence": precedence_base + 10},
             {"channel": "linkyun.api", "share": 0, "precedence": precedence_base + 20}, ])
        channels.extend(backup_channels)
        TyContext.ftlog.debug('_get_default_channels', channels)
        return channels

    @classmethod
    def risk_control(cls, candidates, clientid, clientip):
        TyContext.ftlog.debug('Channels->risk_control', 'candidates=', candidates, 'ip=', clientip)
        avail = []
        for p in candidates:
            pmain = p.split('_')[0]
            from tysdk.entity.pay_common.fengkong import Fengkong
            if Fengkong.is_ip_limited(clientip, clientid, pmain):
                continue
            avail.append(p)
        return set(avail)

    def select_a_channel(self, operator, province, price, clientid, userid, candidates):
        candidates = self._drop_capped_paytypes(operator, province, candidates)
        if not candidates:
            raise Exception('can NOT select_a_channel from NULL candidates')

        channels = TyContext.Configure.get_global_item_json('channels',
                                                            clientid=clientid)
        try:
            channels = channels[operator]
        except:
            channels = self._get_default_channels(clientid, operator, province)
        TyContext.ftlog.debug('select_a_channel channels', channels,
                              'candidates', candidates)
        sum_share = 0.0
        final_channels = {}
        for channel in channels:
            if channel['channel'] in candidates:
                final_channels[channel['channel']] = channel
                sum_share += channel['share']
        TyContext.ftlog.debug('select_a_channel final_channels', final_channels,
                              'sum_share', sum_share)
        # redistribute the share
        if sum_share:
            sum_share /= 100
            for paytype in final_channels:
                final_channels[paytype]['share'] = int(final_channels[paytype]['share'] / sum_share)
            shares = [[paytype,
                       final_channels[paytype]['share'],
                       final_channels[paytype]['precedence']]
                      for paytype in final_channels
                      if final_channels[paytype]['share'] > 0]
            shares.sort(key=itemgetter(2))
            TyContext.ftlog.debug('select_a_channel uid', userid, 'shares', shares)
            share = 0
            for item in shares:
                item[1] += share
                share = item[1]
            point = userid % 100
            TyContext.ftlog.debug('select_a_channel uid', userid, 'point', point, 'shares', share)
            for item in shares:
                if point <= item[1]:
                    return item[0]

        # choose from backups
        backups = [[paytype,
                    final_channels[paytype]['precedence']]
                   for paytype in final_channels
                   if final_channels[paytype]['share'] == 0]
        if not backups:
            raise Exception(
                'select_a_channel NO channel for operator %s, province %s,'
                ' price %s, clientid %s, userid %s, in candidates %s' % (
                    operator, province, price, clientid, userid, candidates))

        backups.sort(key=itemgetter(1))
        TyContext.ftlog.debug('select_a_channel backups', backups)
        return backups[0][0]

    @classmethod
    def incr_ip_count(cls, paytype, ip):
        if not ip:
            return
        paytype = paytype.split('_')[0]
        ret = TyContext.RedisPayData.execute('HINCRBY', 'paytype_ip_control:%s' % paytype, ip, 1)
        key = 'paytype_ip_control:%s' % paytype
        TyContext.ftlog.debug('Channels->risk_control', 'key=', key, 'ip=', ip, 'ret=', ret)
        ttl = TyContext.RedisPayData.execute('TTL', 'paytype_ip_control:%s' % paytype)
        if ttl == -1:
            # set expire
            nt = time.localtime()
            expire = 86400 - nt[3] * 3600 + nt[4] * 60 + nt[5]
            TyContext.RedisPayData.execute('EXPIRE', 'paytype_ip_control:%s' % paytype, expire)

    @classmethod
    def incr_volume(cls, operator, paytype, amount):
        today = datetime.now().strftime('%Y%m%d')
        channels_volume = TyContext.RedisPayData.execute('GET', 'channels_volume')
        if not channels_volume:
            channels_volume = {'timestamp': today}
        else:
            channels_volume = json.loads(channels_volume)
            if today != channels_volume['timestamp']:
                TyContext.ftlog.info('Channels incr_volume purge channels_volume',
                                     channels_volume)
                channels_volume = {'timestamp': today}
        if operator not in channels_volume:
            channels_volume[operator] = {}
        try:
            channels_volume[operator][paytype] += amount
        except:
            channels_volume[operator][paytype] = amount
        channels_volume = json.dumps(channels_volume)
        TyContext.RedisPayData.execute('SET', 'channels_volume', channels_volume)
        TyContext.ftlog.info('Channels incr_volume operator', operator,
                             'paytype', paytype, 'amount', amount,
                             'final channels_volume', channels_volume)

    @classmethod
    def get_all_supported_channels(cls, operator, price, provid):
        return set(cls._duandai_channels[operator][str(price)][provid])

    @classmethod
    def get_min_interval(cls, paytype):
        channels = TyContext.Configure.get_global_item_json('channels_config', [])
        interval = 0
        for channel in channels:
            if channel['paytype'] == paytype:
                interval = int(channel.get('min_interval', 0))
                break
        TyContext.ftlog.debug('Channels get_min_interval', interval, 'paytype', paytype)
        return interval

    @classmethod
    def get_personal_monthly_cap(cls, paytype):
        channels = TyContext.Configure.get_global_item_json('channels_config', [])
        cap = 0
        for channel in channels:
            if channel['paytype'] == paytype:
                cap = int(channel.get('personal_monthly_cap', -1))
                break
        TyContext.ftlog.debug('Channels get_personal_monthly_cap', cap, 'paytype', paytype)
        return cap

    @classmethod
    def get_personal_daily_cap(cls, paytype):
        channels = TyContext.Configure.get_global_item_json('channels_config', [])
        cap = 0
        for channel in channels:
            if channel['paytype'] == paytype:
                cap = int(channel.get('personal_daily_cap', -1))
                break
        TyContext.ftlog.debug('Channels get_personal_daily_cap', cap, 'paytype', paytype)
        return cap
