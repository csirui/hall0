# -*- coding=utf-8 -*-

import base64
import inspect
import json
import re
import struct
import urllib
import uuid
from hashlib import md5


class strutil(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.CLIENT_SYS_ANDROID = 'Android'
        self.CLIENT_SYS_IOS = 'IOS'

        self.__buffered_reg__ = {}
        int62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.__int62dictint__ = {}
        self.__int62dictstr__ = {}
        for x in xrange(len(int62)):
            self.__int62dictint__[x] = int62[x]
            self.__int62dictstr__[int62[x]] = x

    def _init_singleton_(self):
        self.fwlibc, self.fwffi = self.__ctx__.CffiLoader.load_framework_cffi()
        self.ffi_des_str = self.fwffi.new("unsigned char[]", 65536)
        self.ffi_code_str = self.fwffi.new("char[]", 65536)

    def tycode(self, seed, datas):
        self.fwlibc.tycode(seed, datas, len(datas), self.ffi_code_str)
        return self.fwffi.buffer(self.ffi_code_str, len(datas))[:]

    def uuid(self):
        return str(uuid.uuid4()).replace('-', '')

    def dumps(self, obj):
        return json.dumps(obj, separators=(',', ':'))

    def dumpsbase64(self, obj):
        jstr = json.dumps(obj, separators=(',', ':'))
        return base64.b64encode(jstr)

    def loadsbase64(self, base64jsonstr, decodeutf8=False):
        jsonstr = self.b64decode(base64jsonstr)
        datas = json.loads(jsonstr)
        if decodeutf8:
            datas = self.decode_objs_utf8(datas)
        return datas

    def loads(self, jsonstr, decodeutf8=False, ignoreException=False, execptionValue=None):
        if ignoreException:
            try:
                datas = json.loads(jsonstr)
            except:
                datas = execptionValue
        else:
            datas = json.loads(jsonstr)
        if datas and decodeutf8:
            datas = self.decode_objs_utf8(datas)
        return datas

    def b64decode(self, base64str):
        base64str = base64str.replace(' ', '+')
        return base64.b64decode(base64str)

    def b64encode(self, normalstr):
        return base64.b64encode(normalstr)

    def md5digest(self, md5str):
        m = md5()
        m.update(md5str)
        md5code = m.hexdigest()
        return md5code.lower()

    def urlencode(self, params):
        return urllib.urlencode(params)

    def reg_match(self, regExp, checkStr):
        if regExp == '*':
            return True
        if regExp in self.__buffered_reg__:
            breg = self.__buffered_reg__[regExp]
        else:
            breg = re.compile(regExp)
            self.__buffered_reg__[regExp] = breg
        if breg.match(checkStr):
            return True
        return False

    def reg_matchlist(self, regExpList, checkStr):
        for regExp in regExpList:
            if self.reg_match(regExp, checkStr):
                return True
        return False

    def tostr62(self, int10, slenfix=0):
        if int10 <= 0:
            s62 = '0'
        else:
            s62 = ''
            while int10 > 0:
                c = self.__int62dictint__[int10 % 62]
                int10 = int10 / 62
                s62 = c + s62

        if slenfix > 0:
            while len(s62) < slenfix:
                s62 = '0' + s62
            if len(s62) > slenfix:
                s62 = s62[-slenfix:]
        return s62

    def toint10(self, str62):
        int10 = 0
        slen = len(str62)
        for x in xrange(slen):
            m = self.__int62dictstr__[str62[x]]
            if m > 0:
                for _ in xrange(slen - x - 1):
                    m = m * 62
            int10 = m + int10
        return int10

    def parse_client_id(self, clientId):
        if isinstance(clientId, (str, unicode)):
            infos = clientId.split('_', 2)
            if len(infos) == 3:
                try:
                    clientsys = infos[0][0]
                    if clientsys == 'I' or clientsys == 'i':
                        clientsys = self.CLIENT_SYS_IOS
                    else:
                        clientsys = self.CLIENT_SYS_ANDROID
                    return clientsys, self.__ctx__.ClientUtils.getVersionFromClientId(clientId), infos[2]
                except:
                    pass
        return 'error', 0, 'error'

    def get_json_str(self, jsonstr, key, defaultVal=''):
        key = '"' + key + '":'
        i = jsonstr.find(key)
        if i > 0:
            x = jsonstr.find('"', i + len(key))
            y = jsonstr.find('"', x + 1)
            return jsonstr[x + 1:y]
        else:
            return defaultVal

    def get_json_int(self, jsonstr, key, defaluVal=0):
        key = '"' + key + '":'
        i = jsonstr.find(key)
        if i > 0:
            linelen = len(jsonstr)
            i = i + len(key)
            value = 0
            flg = 0
            while i < linelen:
                c = jsonstr[i]
                if c == '0':
                    value = value * 10
                    flg = 1
                elif c == '1':
                    value = value * 10 + 1
                    flg = 1
                elif c == '2':
                    value = value * 10 + 2
                    flg = 1
                elif c == '3':
                    value = value * 10 + 3
                    flg = 1
                elif c == '4':
                    value = value * 10 + 4
                    flg = 1
                elif c == '5':
                    value = value * 10 + 5
                    flg = 1
                elif c == '6':
                    value = value * 10 + 6
                    flg = 1
                elif c == '7':
                    value = value * 10 + 7
                    flg = 1
                elif c == '8':
                    value = value * 10 + 8
                    flg = 1
                elif c == '9':
                    value = value * 10 + 9
                    flg = 1
                elif c == ' ' or c == '"':
                    pass
                else:
                    break
                i += 1
            if flg == 1:
                return value
        return defaluVal

    def des_encrypt(self, deskey, desstr):
        deslen = len(desstr)
        if deslen > 65000:
            raise Exception('the desstr length too long !! 65000 limited !!')
        outlen = self.fwlibc.des_encrypt(desstr, deslen, deskey, self.ffi_des_str)
        return self.fwffi.buffer(self.ffi_des_str, outlen)[:]

    def des_decrypt(self, deskey, desstr):
        deslen = len(desstr)
        if deslen > 65000:
            raise Exception('the desstr length too long !! 65000 limited !!')
        outlen = self.fwlibc.des_decrypt(desstr, deslen, deskey, self.ffi_des_str)
        return self.fwffi.buffer(self.ffi_des_str, outlen)[:]

    def tydes_encode(self, desstr):
        desstr = 'TUYOO~' + desstr + '~POKER201309031548'
        desstr = self.des_encrypt('tuyoocom', desstr)
        desstr = base64.b64encode(desstr)
        return desstr

    def tydes_decode(self, desstr):
        desstr = self.b64decode(desstr)
        desstr = self.des_decrypt('tuyoocom', desstr)
        postail = desstr.find('~POKER201309031548')
        poshead = desstr.find('TUYOO~')
        if poshead == 0 and postail > 6:
            desstr = desstr[6:postail]
            return desstr
        return None

    def to_string(self, obj, maxlen=0, needeascp=False):
        datas = []
        self.__makelines__(obj, datas, maxlen, 1)
        str1 = ''.join(datas)
        if needeascp:
            str1 = str1.replace('\n', '\\n')
            str1 = str1.replace('\d', '\\\\d')
            str1 = str1.replace('\r', '')
        return str1

    def __makelines__(self, obj, datas, maxlen, flg=0):
        dtype = type(obj)
        if dtype == unicode:
            obj = obj.encode('utf-8')
            if maxlen > 0 and len(obj) > maxlen:
                obj = obj[0:maxlen] + '......'
            if flg:
                datas.append(obj)
            else:
                datas.append('"')
                datas.append(obj)
                datas.append('"')

        elif dtype == str:
            if maxlen > 0 and len(obj) > maxlen:
                obj = obj[0:maxlen] + '......'
            if flg:
                datas.append(obj)
            else:
                datas.append('"')
                datas.append(obj)
                datas.append('"')

        elif dtype == int or dtype == long or dtype == bool or dtype == float:
            datas.append(str(obj))

        elif dtype == list:
            datas.append('[')
            i = 0
            for sobj in obj:
                if i > 0:
                    datas.append(', ')
                self.__makelines__(sobj, datas, maxlen)
                i = 1
            datas.append(']')

        elif dtype == tuple:
            datas.append('(')
            i = 0
            for sobj in obj:
                if i > 0:
                    datas.append(', ')
                self.__makelines__(sobj, datas, maxlen)
                i = 1
            datas.append(')')

        elif dtype == dict:
            datas.append('{')
            i = 0
            for k, v in obj.items():
                if i > 0:
                    datas.append(', ')
                if isinstance(k, unicode):
                    k = k.encode('utf-8')
                else:
                    k = str(k)
                datas.append('"')
                datas.append(k)
                datas.append('":')
                self.__makelines__(v, datas, maxlen)
                i = 1
            datas.append('}')

        else:
            obj = str(obj)
            if maxlen > 0 and len(obj) > maxlen:
                obj = obj[0:maxlen] + '......'
            if flg:
                datas.append(obj)
            else:
                datas.append('"')
                datas.append(obj)
                datas.append('"')

    def unicode_2_ascii(self, idata):
        if isinstance(idata, unicode):
            idata = idata.encode('utf-8')
        else:
            idata = str(idata)
        return idata

    def pack(self, struct_fmt, *datas):
        return struct.pack(struct_fmt, *datas)

    def unpack(self, struct_fmt, datas):
        return struct.unpack(struct_fmt, self.unicode_2_ascii(datas))

    def pack1iB(self, int1, int2):
        return struct.pack("iB", int1, int2)

    def unpack1iB(self, int12):
        return struct.unpack("iB", self.unicode_2_ascii(int12))

    def pack2iB(self, int1, int2, int3):
        return struct.pack("2iB", int1, int2, int3)

    def unpack2iB(self, int123):
        return struct.unpack("2iB", self.unicode_2_ascii(int123))

    def pack3iB(self, int1, int2, int3, int4):
        return struct.pack("3iB", int1, int2, int3, int4)

    def unpack3iB(self, int1234):
        return struct.unpack("3iB", self.unicode_2_ascii(int1234))

    def decode_objs_utf8(self, datas):
        if isinstance(datas, dict):
            ndatas = {}
            for key, val in datas.items():
                if isinstance(key, unicode):
                    key = key.encode('utf-8')
                ndatas[key] = self.decode_objs_utf8(val)
            return ndatas
        if isinstance(datas, list):
            ndatas = []
            for val in datas:
                ndatas.append(self.decode_objs_utf8(val))
            return ndatas
        if isinstance(datas, unicode):
            return datas.encode('utf-8')
        return datas

    def decode_objs_utf8_fast(self, datas):
        dtype = type(datas)
        if dtype == dict:
            ndatas = {}
            for key, val in datas.items():
                key = key.encode('utf-8')
                ndatas[key] = self.decode_objs_utf8_fast(val)
            return ndatas
        if dtype == list:
            ndatas = []
            for val in datas:
                ndatas.append(self.decode_objs_utf8_fast(val))
            return ndatas
        if dtype == unicode:
            return datas.encode('utf-8')
        return datas

    def get_object_functions(self, obj, funhead, funargc):
        funs = {}
        for key in dir(obj):
            if key.find(funhead) == 0:
                try:
                    methodfun = getattr(obj, key)
                    if inspect.ismethod(methodfun) and len(inspect.getargspec(methodfun)[0]) == funargc:
                        key = key[len(funhead):]
                        funs[key] = methodfun
                except AttributeError:
                    continue
        return funs


strutil = strutil()
