# coding: utf-8
# dingfu 2014/9/24

import os
from bisect import bisect

from ipaddr import IPAddress


class IPCarrier(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

    def _init_singleton_(self):
        filename = self.__ctx__.TYGlobal.path_webroot() + '/ip_carrier.txt'
        self.__ip_list_start = []
        self.__ip_list_end = []
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f:
                    if len(line) == 0 or line == '\n':
                        continue
                    start, end, carrier = line[:-1].split(' ')
                    self.__ip_list_start.append(int(start))
                    self.__ip_list_end.append((int(end), carrier))
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
            return self.__ip_list_end[pos][1]
        raise Exception(ipstr + " not found")


IPCarrier = IPCarrier()
