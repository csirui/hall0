# -*- coding=utf-8 -*-

from tyframework.context import TyContext
from tysdk.entity.duandai.channels import Channels
from tysdk.entity.duandai.paycodes import PayCodes
from tysdk.entity.duandai.riskcontrol import RiskControl
from tysdk.entity.pay3.charge_conf import TuyouPayChargeConf
from tysdk.entity.pay_common.clientrevision import ClientRevision


class TuYouPayDuandai(object):
    @classmethod
    def _choose_a_paytype(cls, userid, supported_paytypes, operator, price,
                          buttonid, clientid):
        TyContext.ftlog.debug('TuYouPayDuandai _choose_a_paytype userid,'
                              ' supported_paytypes, operator, price, buttonid, clientid',
                              userid, supported_paytypes, operator, price, buttonid, clientid)

        clientip = TyContext.UserSession.get_session_client_ip(userid)
        provid, _ = TyContext.UserSession.get_session_zipcode(userid)
        provid /= 10000
        channel = Channels()
        alls = channel.get_all_supported_channels(operator, price, provid)
        alls = channel.risk_control(alls, clientid, clientip)
        supports = set(supported_paytypes)
        candidates = alls & supports
        TyContext.ftlog.debug('TuYouPayDuandai _choose_a_paytype alls', alls,
                              'supports', supports, 'make candidates', candidates)

        user_control = RiskControl(userid)
        avails = list()
        for p in candidates:
            if user_control.is_limited(p):
                break
            support_this = TuyouPayChargeConf.get_support_this_func(p.split('_')[0])
            if support_this(p, clientid, buttonid):
                avails.append(p)
        TyContext.ftlog.debug('TuYouPayDuandai _choose_a_paytype avails', avails,
                              'from candidates', candidates)
        return channel.select_a_channel(operator, provid, price, clientid,
                                        userid, avails)

    @classmethod
    def charge_data(cls, chargeinfo):
        try:
            cls._charge_data_for_duandai(chargeinfo)

        except Exception as e:
            TyContext.ftlog.debug('TuYouPayDuandai charge_data exception', e)
            # TyContext.ftlog.exception()
            clientId = chargeinfo['clientId']
            payconfig = TyContext.Configure.get_global_item_json(
                'store_payment', clientid=clientId)
            try:
                more_cats = payconfig['payment']['more_categories']
            except:
                TyContext.ftlog.error('TuYouPayDuandai charge_data clientid',
                                      clientId, 'payconfig error', payconfig)
                return
            if 'CAT_' in more_cats:
                chargeType = more_cats.lower()
            else:
                chargeinfo['chargeType'] = chargeType = more_cats
            cfun = TuyouPayChargeConf.get_charge_data_func(chargeType)
            cfun(chargeinfo)

    @classmethod
    def _charge_data_for_duandai(cls, chargeinfo):
        buttonId = chargeinfo['buttonId']
        clientId = chargeinfo['clientId']
        price = chargeinfo['chargeTotal']
        userid = chargeinfo['uid']

        phone_type = TyContext.UserSession.get_session_phone_type(userid)
        operator = TyContext.UserSession.get_phone_type_name(phone_type)
        if operator == TyContext.UserSession.PHONETYPE_OTHER_STR:
            raise Exception('phone_type other has no duandai')

        builtin_paytypes = ClientRevision(userid).get_builtin_paytypes(operator)

        # appids -> {"paytype": "appid"}
        appids = PayCodes(clientId).appids
        TyContext.ftlog.debug('TuYouPayDuandai _charge_data_for_duandai '
                              'appids', appids, 'chargeinfo', chargeinfo)

        all_duandai_paytypes = TyContext.Configure.get_global_item_json("all_duandai_paytypes")
        supported_paytypes = ['_'.join([k, appids[k]])
                              for k in appids.keys()
                              if k in all_duandai_paytypes]

        supported_paytypes.extend(builtin_paytypes)

        paytype = cls._choose_a_paytype(userid, supported_paytypes, operator,
                                        price, buttonId, clientId)
        TyContext.ftlog.debug('TuYouPayDuandai charge_data got paytpe', paytype)
        chargeType = paytype.split('_')[0]
        cfun = TuyouPayChargeConf.get_charge_data_func(chargeType)
        chargeinfo['chargeType'] = chargeType
        cfun(chargeinfo)
        if 'chargeData' not in chargeinfo or not chargeinfo['chargeData']:
            raise Exception('got null paydata for paytype %s' % chargeType)
        chargeinfo['chargeData']['issms'] = 1
