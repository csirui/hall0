# -*- coding=utf-8 -*-

from tyframework.context import TyContext


class HotCmdHandler(object):
    def __init__(self, params=None):
        self.cmdname = '_server_hot_cmd_'
        self.errmsg1 = '{"cmd":"%s","err"}'
        self.handlers = {}
        self.handlers['reload_configure_json'] = self.__handle_action_reload_configure_json__
        self.handlers['exec_hotfix_py'] = self.__handle_action_exec_hotfix_py__

    def __call__(self, *args, **argds):
        return self

    def handel_msg(self, tasklet, msg):
        mo = TyContext.MsgPack()
        mo.setCmd(self.cmdname)
        try:
            action = msg.getParam('action')
            mo.setResult('action', action)
            handler = self.handlers.get(action)
            if handler:
                handler(msg, mo)
            else:
                mo.setError(1, 'action not found !')
        except:
            TyContext.ftlog.exception()
            mo.setError(1, TyContext.ftlog.format_exc())

        mo.setKey('prockey', TyContext.TYGlobal.prockey())

        TyContext.ftlog.info('_server_hot_cmd_ response :', mo)

        if tasklet.protocol and msg.getParam('noresponse') != 1:
            # 这里出异常会把整个进程卡死，为了安全，多加点异常处理
            try:
                data = TyContext.MsgLine.packstr(tasklet.msgline.udpId, 0, mo.pack())
                tasklet.protocol.writeMessage(data, tasklet.udpaddress)
            except:
                TyContext.ftlog.exception()
                try:
                    mo.setError(1, TyContext.ftlog.format_exc())
                    data = TyContext.MsgLine.packstr(tasklet.msgline.udpId, 0, mo.pack())
                    tasklet.protocol.writeMessage(data, tasklet.udpaddress)
                except:
                    TyContext.ftlog.exception()

    def __handle_action_exec_hotfix_py__(self, mi, mo):
        """
        用 execfile 动态执行 udp 消息中指定的脚本文件，来实现动态的调试、
        更新、 bug修复、数据调整等
        """
        pyfile = mi.getParam('pyfile')
        TyContext.ftlog.info('_server_hot_cmd_ exec_hotfix_py :', pyfile)
        execfile_result = {}
        execfile_globals = {
            'TyContext': TyContext,
            'exec_tasklet': TyContext.getTasklet(),
            'exec_result': execfile_result,
        }
        try:
            execfile(pyfile, execfile_globals, execfile_globals)
            mo.setResult('execfile_result', execfile_result)
            mo.setResult('ok', 1)
        except:
            mo.setError(1, TyContext.ftlog.format_exc())
            TyContext.ftlog.exception()

    def __handle_action_reload_configure_json__(self, mi, mo):
        TyContext.ftlog.info('_server_hot_cmd_ reload_configure_json')
        try:
            changedlist = mi.getParam('changedlist')
            if isinstance(changedlist, list) and len(changedlist) > 0:
                #                 TyContext.Configure.reload(10, True) # 只更新变化的缓存键值
                TyContext.Configure.reload_cache_keys(changedlist)
            mo.setResult('ok', 1)
        except:
            mo.setError(1, TyContext.ftlog.format_exc())
            TyContext.ftlog.exception()


HotCmdHandler = HotCmdHandler()
