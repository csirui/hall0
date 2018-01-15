# -*- coding=utf-8 -*-

import copy

from tyframework.context import TyContext


class ClientRevision(object):
    @classmethod
    def get_client_sdk_revision(cls, svninfo):
        TyContext.ftlog.debug('get_client_sdk_revision svninfo=', svninfo)
        try:
            return int(svninfo.split(' ')[2])
        except:
            return 0

    def __init__(self, userid):
        self._userid = userid
        self._client_sdk_rev = TyContext.UserSession.get_session_client_sdk_revision(userid)

    @property
    def support_querystatus_rsp_action_parameter(self):
        min_rev = TyContext.Configure.get_global_item_int(
            'min_revision_supporting_querystatus_action_flag_parameter', 3184)
        return self._client_sdk_rev >= min_rev

    @property
    def support_type0_smspayinfo(self):
        min_rev = TyContext.Configure.get_global_item_int(
            'min_revision_supporting_type0_smspayinfo', 3350)
        return self._client_sdk_rev >= min_rev

    def get_builtin_paytypes(self, operator):
        paytypes = copy.deepcopy(_basic_builtin_paytypes[operator])
        if self._client_sdk_rev >= TyContext.Configure.get_global_item_int(
                'min_revision_supporting_yipay', 3250):
            paytypes.append('yipay')
            paytypes.append('gefu')
        if self._client_sdk_rev >= TyContext.Configure.get_global_item_int(
                'min_revision_supporting_eftapi', 3550) \
                and (operator == 'chinaUnion' or operator == 'chinaTelecom'):
            paytypes.append('EFT.api')
        return paytypes


_basic_builtin_paytypes = {
    'chinaMobile': ['linkyun', ],
    'chinaUnion': ['EFTChinaUnion.msg', ],
    'chinaTelecom': ['EFTChinaTelecom.msg', ],
    'other': [],
}
