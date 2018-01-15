# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月08日 星期日 14时48分18秒
# FileName:      /home/zhoux/freetime2/src/freetime/util/msg.py

import base64
import json
import types


class MsgPack:
    def __init__(self, jsonstr=None):
        if jsonstr != None:
            self._ht = json.loads(jsonstr)
        else:
            self._ht = {}

    def __str__(self):
        return str(self._ht)

    def __repr__(self):
        return self.__str__()

    def setKey(self, key, value):
        self._ht[key] = value

    def getKey(self, key):
        if self._ht.has_key(key):
            return self._ht[key]
        return None

    def rmKey(self, key):
        if self._ht.has_key(key):
            del self._ht[key]

    def setCmd(self, cmd):
        self._ht['cmd'] = cmd

    def getCmd(self):
        if self._ht.has_key('cmd'):
            return self._ht['cmd']
        return None

    def setActCmd(self, cmd):
        self.setCmd('table_call')
        self.setResult('action', cmd)

    def getActCmd(self):
        return self.getResultStr('action', '')

    def setParam(self, pkey, pvalue):
        if not self._ht.has_key('params'):
            self._ht['params'] = {}
        reqht = self._ht['params']
        reqht[pkey] = pvalue

    def getParam(self, pkey):
        if self._ht.has_key('params'):
            reqht = self._ht['params']
            if reqht.has_key(pkey):
                return reqht[pkey]
        return None

    def setResult(self, pkey, pvalue):
        if not self._ht.has_key('result'):
            self._ht['result'] = {}
        reqht = self._ht['result']
        reqht[pkey] = pvalue

    def getResult(self, pkey):
        if self._ht.has_key('result'):
            reqht = self._ht['result']
            if reqht.has_key(pkey):
                return reqht[pkey]
        return None

    def isError(self):
        if self._ht.has_key('error'):
            return True
        else:
            return False

    def setError(self, code, info):
        errht = {}
        errht['code'] = code
        errht['info'] = info
        self._ht['error'] = errht

    def getErrorInfo(self):
        if self._ht.has_key('error'):
            errht = self._ht['error']
            if errht.has_key('info'):
                return errht['info']
        return None

    def getErrorCode(self):
        if self._ht.has_key('error'):
            errht = self._ht['error']
            if errht.has_key('code'):
                return errht['code']
        return None

    def unpack(self, sin):
        jstr = sin.strip('\r\n\0 ')
        self._ht = json.loads(jstr)

    def pack(self):
        return json.dumps(self._ht, separators=(',', ':')) + '\n\0'

    def packJson(self):
        return json.dumps(self._ht, separators=(',', ':'))

    def getParamStr(self, pkey, dValue=''):
        value = self.getParam(pkey)
        if value == None:
            value = str(dValue)
        return value

    def getParamInt(self, pkey, dValue=0):
        try:
            value = int(self.getParam(pkey))
        except:
            value = dValue
        return value

    def getParamFloat(self, pkey, dValue=0.0):
        try:
            value = float(self.getParam(pkey))
        except:
            value = dValue
        return value

    def rmResult(self, *pkeys):
        if self._ht.has_key('result'):
            reqht = self._ht['result']
            for pkey in pkeys:
                if reqht.has_key(pkey):
                    del reqht[pkey]

    def getResultStr(self, pkey, dValue=''):
        value = self.getResult(pkey)
        if value == None:
            value = str(dValue)
        return value

    def getResultInt(self, pkey, dValue=0):
        try:
            value = int(self.getResult(pkey))
        except:
            value = dValue
        return value

    def getResultFloat(self, pkey, dValue=0.0):
        try:
            value = float(self.getResult(pkey))
        except:
            value = dValue
        return value

    # Get base params from client msg...
    def getBaseParams(self, gdata):
        #        cmd = self.getCmd()
        #        cid = self.getKey('cmdId')
        try:
            uid = int(self.getParam('userId'))
        except:
            uid = 0
        try:
            rid = int(self.getParam('roomId'))
        except:
            rid = 0
        try:
            tid = int(self.getParam('tableId'))
        except:
            tid = 0
        try:
            sid = int(self.getParam('seatId'))
        except:
            sid = 0
        try:
            gid = int(self.getParam('gameId'))
        except:
            gid = 0

        room = None
        if rid in gdata.maproom:
            room = gdata.maproom[rid]

        table = None
        if room and tid in room.maptable:
            table = room.maptable[tid]

        user = None
        if uid in gdata.usermap:
            user = gdata.usermap[uid]

        return (gid, uid, rid, tid, sid, user, room, table)

    def getOutMsgPack(self):
        mo = MsgPack()
        mo.setCmd(self.getCmd())
        return mo

    @classmethod
    def makeErrorPack(cls, errstring):
        mo = MsgPack()
        mo.setKey('RESULT', 'ERROR')
        mo.setKey('REASON', errstring)
        return mo

    @classmethod
    def makeErrorString(cls, errstring):
        return MsgPack.makeErrorPack(errstring).pack()

    @classmethod
    def pstruct(cls, idata):
        try:
            odata = idata.encode('utf-8')
        except:
            odata = idata
        return odata

    @classmethod
    def b64encode(cls, data):
        pt = type(data)
        if pt == types.UnicodeType:
            pass
        elif pt == types.StringType:
            data = unicode(data)
        else:
            data = unicode(str(data))
        data = data.encode('utf-8')
        data = base64.b64encode(data)
        return data

    def getParams(self, *keys):
        return map(self._ht.get('params', {}).get, keys)

    def getResults(self, *keys):
        return map(self._ht.get('result', {}).get, keys)
