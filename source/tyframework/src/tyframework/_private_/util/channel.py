# -*- coding=utf-8 -*-
from tyframework._private_.util.initreactor import tychannel, tybomb


class NWChannel(tychannel):
    def send_nowait(self, v):
        if self.balance == 0:
            self.value = v
        else:
            self.send(v)

    def send_exception_nowait(self, ntype, value):
        if self.balance == 0:
            self.exc = (ntype, value)
        else:
            if isinstance(value, ntype):
                self.send(tybomb(ntype, value))
            else:
                self.send_exception(ntype, value)

    def receive(self):
        if hasattr(self, 'value'):
            v = self.value
            del self.value
            return v
        if hasattr(self, 'exc'):
            ntype, value = self.exc
            del self.exc
            raise ntype, value
        return tychannel.receive(self)
