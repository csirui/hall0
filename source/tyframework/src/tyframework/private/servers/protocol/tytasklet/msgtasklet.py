# -*- coding=utf-8 -*-

from simpletasklet import SimpleTasklet
from tyframework.context import TyContext


class MsgTasklet(SimpleTasklet):
    def handle(self):
        funs = None
        cmd = None
        old_freetime4 = False
        try:
            cmd = getattr(self.msgline, 'cmd', None)
            if cmd != None:
                old_freetime4 = True
                TyContext.ftlog.debug('MsgTasklet->cmd=[', cmd, ']', self.msgline.dumpMsg())
            else:
                cmd = self.msgline.getCmd()
                TyContext.ftlog.debug('MsgTasklet->cmd=[', cmd, ']', self.msgline.pack())
            commands = self.getCommands()
            if cmd in commands:
                funs = commands[cmd]
            elif '_default_' in commands:
                funs = commands['_default_']
        except Exception, e:
            TyContext.ftlog.exception(cmd, e)
            return

        if funs:
            try:
                self.__cmd__ = cmd
                funs(self.msgline)
            except Exception, e:
                TyContext.ftlog.exception(cmd, e)
            return

        TyContext.ftlog.error('the msg is not in process cmd=', cmd, old_freetime4)

    def sendResponse(self, msg, userId=None):
        raise NotImplementedError

    def getCommands(self):
        raise NotImplementedError

    def getActionCommands(self):
        raise NotImplementedError
