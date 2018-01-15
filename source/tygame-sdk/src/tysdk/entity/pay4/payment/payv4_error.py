#! encoding=utf-8
from tyframework.context import TyContext

__author__ = 'yuejianqiang'


class PayErrorV4(Exception):
    def __init__(self, code, info):
        self.code = code
        self.info = info

    def mo(self):
        mo = TyContext.Cls_MsgPack()
        mo.setResult('code', self.code)
        mo.setResult('info', self.info)
        return mo
