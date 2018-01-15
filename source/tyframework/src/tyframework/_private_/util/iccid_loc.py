# coding: utf-8
# fanzheng 2014/9/27

import re


# 因为目前只是对中国移动的手机有按省份切换支付方式的需求，
# 这里只提供移动的ICCID的省份转换

class IccidLoc(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.iccid2prov_map = {
            '01': 10,
            '09': 20,
            '02': 30,
            '31': 40,
            '05': 01,
            '04': 03,
            '03': 05,
            '06': 11,
            '07': 13,
            '08': 15,
            '10': 21,
            '12': 23,
            '15': 25,
            '11': 31,
            '14': 33,
            '13': 35,
            '18': 41,
            '17': 43,
            '16': 45,
            '19': 51,
            '20': 53,
            '23': 55,
            '21': 57,
            '22': 61,
            '24': 65,
            '26': 71,
            '27': 73,
            '29': 75,
            '28': 81,
            '30': 83,
            '25': 85,
        }

    def get_provid(self, iccid):
        if not iccid or not re.match('^[0-9]{10,20}$', iccid):
            return -2
        operator = iccid[4:6]
        if operator == '00':  # CMCC
            provid = iccid[8:10]
            try:
                return self.iccid2prov_map[provid]
            except:
                return -1
        return -2


IccidLoc = IccidLoc()
