# coding: utf-8
# dingfu 2014/9/24

import os
from bisect import bisect

from ipaddr import IPAddress


class IPLoc(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def _init_singleton_(self):
        self.prov2pc_map = {
            '北京': 10,
            '上海': 20,
            '天津': 30,
            '重庆': 40,
            '内蒙古': 1,
            '山西': 3,
            '河北': 5,
            '辽宁': 11,
            '吉林': 13,
            '黑龙江': 15,
            '江苏': 21,
            '安徽': 23,
            '山东': 25,
            '浙江': 31,
            '江西': 33,
            '福建': 35,
            '湖南': 41,
            '湖北': 43,
            '河南': 45,
            '广东': 51,
            '广西': 53,
            '贵州': 55,
            '海南': 57,
            '四川': 61,
            '云南': 65,
            '陕西': 71,
            '甘肃': 73,
            '宁夏': 75,
            '青海': 81,
            '新疆': 83,
            '西藏': 85,
            '香港': -1,
            '澳门': -1,
            '台湾': -1,
            # '香港' : 999077,
            # '澳门' : 999078,
            # '台湾' : 86,
        }
        filename = self.__ctx__.TYGlobal.path_webroot() + '/ip_prov.txt'
        self.__ip_list_start = []
        self.__ip_list_end = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f:
                    if len(line) == 0 or line == '\n':
                        continue
                    start, end, provname = line[:-1].split(' ')
                    self.__ip_list_start.append(int(start))
                    self.__ip_list_end.append((int(end), self.prov2pc_map[provname]))
        else:
            self.__ctx__.ftlog.error('ERROR, the resource file not found !', filename)

    def __binary_search(self, x, lo=0, hi=None):
        if hi is None:
            hi = len(self.__ip_list_start)
        pos = bisect(self.__ip_list_start, x, lo, hi)
        if pos == 0:
            return -1
        return pos - 1

    def find(self, ipstr):
        ''' return postcode of the province in which the ip addr reside '''
        ip = IPAddress(ipstr)
        pos = self.__binary_search(ip._ip)
        ip_start = IPAddress(self.__ip_list_start[pos])
        ip_end = IPAddress(self.__ip_list_end[pos][0])
        if ip > ip_start and ip < ip_end:
            if self.__ip_list_end[pos][1] < 0:
                raise Exception(ipstr + " not found")
            return self.__ip_list_end[pos][1]
        raise Exception(ipstr + " not found")


IPLoc = IPLoc()
