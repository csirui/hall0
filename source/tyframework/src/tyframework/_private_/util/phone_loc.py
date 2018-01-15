# coding: utf-8
# dingfu 2014/9/17
#
import os

# province name to postcode
prov2pc_map = {
    '北京': 10,
    '上海': 20,
    '天津': 30,
    '重庆': 40,
    '内蒙古': 01,
    '山西': 03,
    '河北': 05,
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
    '香港': 99,
}

# postcode to province name
pc2prov_map = {
    10: '北京',
    20: '上海',
    30: '天津',
    40: '重庆',
    01: '内蒙古',
    03: '山西',
    05: '河北',
    11: '辽宁',
    13: '吉林',
    15: '黑龙江',
    21: '江苏',
    23: '安徽',
    25: '山东',
    31: '浙江',
    33: '江西',
    35: '福建',
    41: '湖南',
    43: '湖北',
    45: '河南',
    51: '广东',
    53: '广西',
    55: '贵州',
    57: '海南',
    61: '四川',
    65: '云南',
    71: '陕西',
    73: '甘肃',
    75: '宁夏',
    81: '青海',
    83: '新疆',
    85: '西藏',
    99: '香港',
}


# postcode to zipcode: pc*10000


class ContradictError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class CoarseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class PhoneTrie(object):
    @property
    def triedict(self):
        return self.__trie

    def __str__(self):
        return str(self.__trie)

    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.__trie = {}

    def _init_singleton_(self):
        filename = self.__ctx__.TYGlobal.path_webroot() + '/phone_prefix.txt'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                for line in f:
                    tp = line[:-1].split(' ')
                    self.insert((tp[0], prov2pc_map[tp[1]]))
        else:
            self.__ctx__.ftlog.error('ERROR, the resource file not found !', filename)
        deredundant(self.__trie)

    def find(self, phonestr):
        m = self.__trie
        for d in phonestr:
            if d not in m:
                raise Exception(phonestr + " not found")
            if isinstance(m[d], tuple):
                return m[d][1]
            if isinstance(m[d], dict):
                m = m[d]
                continue
            raise Exception(phonestr + " not found")

    def insert(self, t):
        prefix, prov = t
        d = self.__trie
        for i in xrange(len(prefix)):
            p = prefix[i]
            if p not in d:
                d[p] = [prefix], prov
                return
            o = d[p]
            if isinstance(o, tuple):
                if prefix in o[0]:
                    if o[1] != prov:
                        raise ContradictError("")
                    return
                if prov == o[1]:
                    o[0].append(prefix)
                    return
                if i >= len(prefix) - 1:
                    raise CoarseError("")
                d[p] = {prefix[i + 1]: ([prefix], prov)}
                for pre in o[0]:
                    self.insert((pre, o[1]))
                return
            if isinstance(o, dict):
                d = o
                continue
            raise Exception('inserting ' + str(t) + ' into ' + str(self.__trie))


def deredundant(triedict):
    for s in triedict:
        if isinstance(triedict[s], tuple):
            del triedict[s][0][:]
        elif isinstance(triedict[s], dict):
            deredundant(triedict[s])
        else:
            raise Exception("")


def common(prefix, triedict):
    for s in triedict:
        if isinstance(triedict[s], tuple):
            print prefix + s, triedict[s][1]
        elif isinstance(triedict[s], dict):
            common(prefix + s, triedict[s])
        else:
            raise Exception("")


PhoneTrie = PhoneTrie()
