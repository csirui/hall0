# -*- coding=utf-8 -*-

# Author:        zipxing@hotmail.com
# Company:       YouXia.Inc
# Created:       2012年04月08日 星期日 14时48分18秒
# FileName:      /home/zhoux/freetime2/src/freetime/util/msg.py

class MsgLine:
    UDPTARGET_SEPARATOR = '\20'
    UDPID_SEPARATOR = '\21'
    ucount = 0

    def __init__(self, udpId=0, targets=None, message=None):
        self.udpId = udpId
        self.message = message;
        self.targets = targets
        self.cmd = self._fastJosnStr(message, 'cmd')
        self.userId = -2
        self.gameId = -2
        self.roomId = -2
        self.clientId = ''
        if message and message.find('|OLDBRIDGE|') >= 0:
            # src, dst, queryid, userheader1, userheader2, message
            datas = message.split('|', 5)
            self.bridgeId = datas[0]
            self.udpId = datas[2]
            self.userId = int(datas[4])
            self.message = datas[5]

    def getUserId(self):
        if self.userId == -2:
            self.userId = self._fastJosnInt(self.message, 'userId')
        return self.userId

    def getGameId(self):
        if self.gameId == -2:
            self.gameId = self._fastJosnInt(self.message, 'gameId')
        return self.gameId

    def getRoomId(self):
        if self.roomId == -2:
            self.roomId = self._fastJosnInt(self.message, 'roomId')
        return self.roomId

    def getClientId(self):
        if self.clientId == '':
            self.clientId = self._fastJosnStr(self.message, 'clientId')
        return self.clientId

    def dumpMsg(self):
        return str(self.udpId) + '|' + str(self.userId) + '|' + str(self.targets) + \
               '|' + str(self.cmd) + '|' + self.message

    def pack(self):
        return MsgLine.packstr(self.udpId, self.targets, self.message)

    def _fastJosnStr(self, line, key):
        key = '"' + key + '":'
        i = line.find(key)
        if i > 0:
            x = line.find('"', i + len(key))
            y = line.find('"', x + 1)
            return line[x + 1:y]
        else:
            return ''

    def _fastJosnInt(self, src, key):
        pos = src.find('"' + key + '":')
        if pos == -1:
            return -1
        ls = src[pos + len(key) + 3:].strip()
        nums = ''
        for x in xrange(len(ls)):
            if ls[x] <= '9' and ls[x] >= '0':
                nums += ls[x]
            else:
                break
        if len(nums) == 0:
            return -1
        return int(nums)

    @classmethod
    def nextUdpId(self):
        udpId = self.ucount + 1
        if udpId > 2000000000:
            udpId = 1
        self.ucount = udpId
        return udpId

    @classmethod
    def getUdpId(self, data):
        i = data.find(self.UDPID_SEPARATOR, 0, 16)
        udpid = int(data[0:i])
        return udpid

    @classmethod
    def unpack(self, data):
        i = data.find(self.UDPID_SEPARATOR, 0, 16)
        if i > 0:
            udpid = int(data[0:i])

            j = data.find(self.UDPTARGET_SEPARATOR, i + 1)
            tstr = data[i + 1: j]
            targets = tstr.split(',')
            for x in xrange(len(targets)):
                targets[x] = int(targets[x])

            message = data[j + 1:]
        else:
            udpid = 0
            targets = [0]
            message = data
        return MsgLine(udpid, targets, message)

    @classmethod
    def packstr(self, udpId, targets, message):
        if udpId == None:
            udpId = self.nextUdpId()
        targets_ = None
        if targets == None:
            targets_ = '0'
        else:
            if type(targets) == int:
                targets_ = str(targets)
            else:
                targets_ = []
                for x in xrange(len(targets)):
                    targets_.append(str(targets[x]))
                targets_ = ','.join(targets_)

        return str(udpId) + self.UDPID_SEPARATOR + targets_ + self.UDPTARGET_SEPARATOR + message
