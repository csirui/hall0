# -*- coding=utf-8 -*-
import zlib


class TySync(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.SYNC_KEY = 'configitems.sync.uuids'
        self.__sync_global_buffer__ = {}

    def __decode_sync_datas__(self, b64str):
        b64str = self.__ctx__.strutil.b64decode(b64str)
        b64str = zlib.decompress(b64str)
        newobj = self.__ctx__.strutil.loads(b64str)
        return newobj

    def sync_global_configure(self, hc):
        '''
        每个游戏服务只需要第一个进程进行同步即可
        每10秒同步一次,本次和下一个10秒进行配置的强制更新
        '''
        try:
            if self.__ctx__.TYGlobal.is_control_process() and hc % 10 == 0:
                self._sync_global_configure_()
        except Exception as e:
            self.__ctx__.ftlog.exception(e)

    def _sync_global_configure_(self):
        # PATCH:不再同步数据了
        return
        # syncurl = self.__ctx__.TYGlobal.http_global_api_sync_config()
        # sync_uuids = self.__ctx__.RedisConfig.execute('GET', self.SYNC_KEY)
        # sync_uuids = self.__ctx__.strutil.loads(sync_uuids, False, True, {})
        #
        # datas, syncurl = self.__ctx__.WebPage.webget_json(syncurl, sync_uuids)
        # if not datas:
        #     self.__ctx__.ftlog.error('ERROR sync_global_configure')
        #     return
        #
        # result = datas.get('result', {})
        # code = result.get('code', -1)
        # self.__ctx__.ftlog.debug('sync_global_configure code=', code)
        # if code != 200:
        #     return
        #
        # confall = result['datas']
        # if len(confall) > 0:
        #     ct = self.__ctx__.TimeStamp.get_current_timestamp()
        #     self.__ctx__.ftlog.info('sync_global_configure start set data')
        #     changedlist = []
        #     for conf_name in confall:
        #         confs = confall[conf_name]
        #         sync_uuids[conf_name] = confs['uuid']
        #         cmds = confs['cmds']
        #         cmds = self.__ctx__.strutil.b64decode(cmds)
        #         cmds = zlib.decompress(cmds)
        #         cmds = self.__ctx__.strutil.loads(cmds)
        #         for rcmd in cmds:
        #             changedlist.append(rcmd[1])
        #             self.__ctx__.RedisConfig.sendcmd(*rcmd)
        #
        #     et = self.__ctx__.TimeStamp.get_current_timestamp()
        #     if len(changedlist) > 0:
        #         self.__ctx__.RedisConfig.execute('SET', self.SYNC_KEY, self.__ctx__.strutil.dumps(sync_uuids))
        #         # TODO 这个位置, 需要通知所有的进程, 配置发生了变化, 如果webshell启动, 那么此处的同步可以通过webshell进行??
        #         msg = self.__ctx__.MsgPack()
        #         msg.setCmd('_server_hot_cmd_')
        #         msg.setParam('action', 'reload_configure_json')
        #         msg.setParam('changedlist', changedlist)
        #         msg.setParam('noresponse', 1)
        #         tasklet = self.__ctx__.getTasklet()
        #         for client in tasklet.gdata.clientmap.values():
        #             client.sendMessage(msg)
        #
        #     self.__ctx__.ftlog.info('check_global_config end set data, seconds=', (et - ct))


TySync = TySync()
