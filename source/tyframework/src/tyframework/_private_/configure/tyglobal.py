# -*- coding=utf-8 -*-

import copy
import os
import sys

from tyframework._private_.util.lockattr import LockAttr


class TYGlobal(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        self.newtcpbridge_connids = []
        self.__shell_ver__ = 0
        self.__servie__ = {}
        self.RUN_MODE_ONLINE = 1
        self.RUN_MODE_ONLINE_AUDIT = 2
        self.RUN_MODE_TEST_OUTSIDE = 3
        self.RUN_MODE_TEST_INSIDE = 4

        self.RUN_TYPE_CONN = 'conn'
        self.RUN_TYPE_HEARTBEAT = 'heart'
        self.RUN_TYPE_ROBOT = 'robot'
        self.RUN_TYPE_ACCOUNT = 'account'
        self.RUN_TYPE_HTTP = 'http'
        self.RUN_TYPE_GAME = 'game'
        self.RUN_TYPE_ENTITY = 'entity'
        self.RUN_TYPE_QUICKSTART = 'quick'

    def init_static_data(self):
        if len(self.__servie__) > 0:
            self.__ctx__.ftlog.error('ERROR, TYGlobal already init !!')
            return False

        path_script = os.environ.get('PATH_SCRIPT', './')

        jfile = path_script + '/control.json'
        jfile = self.__ctx__.fileutil.abspath(jfile)
        self.__ctx__.ftlog.info('TYGlobal.init_static_data->', jfile)
        datas = self.__ctx__.fileutil.read_json_file(jfile, True)
        self.__shell_ver__ = 2
        return self._init_static_data_(datas['service'])

    def _init_static_data_(self, service):
        if len(self.__servie__) > 0:
            self.__ctx__.ftlog.error('ERROR, TYGlobal already init !!')
            return False

        self.__servie__ = service

        self.__prockey__ = sys.argv[1]

        datas = self.__prockey__.split(':')
        self.__groupkey__ = datas[0] + ':' + datas[1] + ':' + datas[2]
        self.__log_file_name__ = datas[3] + '.log'

        datas = datas[3].split('-')
        self.__process_id__ = int(datas[3])

        srvs = self.__servie__['servers']
        srvsmap = {}
        for srv in srvs:
            srvsmap[srv['id']] = srv

        self.__run_server__ = None
        self.__run_process__ = None
        min_http_port = 65536
        for proc in self.__servie__['process']:
            if self.__process_id__ == proc['id']:
                self.__run_process__ = proc
                self.__run_server__ = srvsmap[proc['server']]
            if proc['type'] == 'http':
                min_http_port = min(min_http_port, proc['http'])

        self.__is_control_process__ = 0
        if min_http_port == self.__run_process__.get('http', 0):
            self.__is_control_process__ = 1

        tcpsrvids = []
        tcplist = []
        bridge_tcplist = []
        for proc in self.__servie__['process']:
            if proc.get('type', '') == 'conn' and proc.get('tcp', 0) > 0:
                srvid = proc['server']
                tcplist.append([srvsmap[srvid]['internet'], proc['tcp']])
                bridge_tcplist.append([srvsmap[srvid]['intrant'], proc['tcp'] + 1000])
                tcpsrvids.append(proc['id'])

        self.__conn_srv_ids__ = tcpsrvids
        self.__conn_ip_ports__ = tcplist
        self.__bridge_tcplist__ = bridge_tcplist
        self.__ctx__.ftlog.info('TYGlobal.newtcpbridge->', self.newtcpbridge())

        LockAttr.lock(self)
        return True

    def shell_ver(self):
        return self.__shell_ver__

    def prockey(self):
        return self.__prockey__

    def groupkey(self):
        return self.__groupkey__

    def log_file_name(self):
        return self.__log_file_name__

    def run_process(self):
        return self.__run_process__

    def run_process_type(self):
        return self.__run_process__['type']

    def run_process_id(self):
        return self.__run_process__['id']

    def run_server(self):
        return self.__run_server__

    def all_process(self):
        return self.__servie__['process']

    def all_service(self):
        return self.__servie__

    def is_control_process(self):
        return self.__is_control_process__

    def gameid(self):
        return self.__servie__['id']

    def name(self):
        return self.__servie__['name']

    def corporation(self):
        return self.__servie__.get('corporation', 'tuyoo')

    def encodepyc(self):
        return self.__servie__['encodepyc']

    def hook(self):
        return self.__servie__.get('hook', 'nohook')

    def http_download(self):
        return self.__servie__['http.download']

    def http_game(self):
        return self.__servie__['http.game']

    def http_sdk(self):
        return self.__servie__['http.sdk']

    def http_sdk_inner(self):
        return self.__servie__.get('http.sdk.inner', self.http_sdk())

    def newtcpbridge(self):
        return self.__servie__['newtcpbridge']

    def mode(self):
        return self.__servie__.get('mode', 0)

    def simulation(self):
        return self.__servie__.get('simulation', 0)

    def mysql(self, dbname):
        return self.__servie__['mysql'].get(dbname, None)

    def bicollect_server(self):
        return self.__servie__['bicollect.server']

    def path_backup(self):
        return self.__servie__['paths'].get('backup', self.path_log())

    def path_bin(self):
        return self.__servie__['paths']['bin']

    def path_bireport(self):
        return self.__servie__['paths']['bireport']

    def path_hotfix(self):
        return self.__servie__['paths'].get('hotfix', self.path_bin())

    def path_log(self):
        return self.__servie__['paths']['log']

    def path_script(self):
        return self.__servie__['paths']['script']

    def path_webroot(self):
        return self.__servie__['paths']['webroot']

    def redis_config(self):
        return self.__servie__['redis']['config']

    def redis_mix(self):
        return self.__servie__['redis'].get('mix', self.redis_config())

    def redis_bicount(self):
        return self.__servie__['redis'].get('bicount', self.redis_mix())

    def redis_forbidden(self):
        return self.__servie__['redis'].get('forbidden', self.redis_mix())

    def redis_friend(self):
        return self.__servie__['redis'].get('friend', self.redis_mix())

    def redis_online(self):
        return self.__servie__['redis'].get('online', self.redis_mix())

    def redis_onlinegeo(self):
        return self.__servie__['redis'].get('onlinegeo', self.redis_mix())

    #     def redis_onlinemix(self):
    #         return self.__servie__['redis'].get('onlinemix', self.redis_mix())

    def redis_paydata(self):
        return self.__servie__['redis'].get('paydata', self.redis_mix())

    def redis_userkeys(self):
        return self.__servie__['redis'].get('userkeys', self.redis_mix())

    def redis_avatar(self):
        return self.__servie__['redis'].get('avatar', self.redis_mix())

    def redis_datas(self):
        return self.__servie__['redis'].get('datas', [self.redis_mix()])

    def redis_table_datas(self):
        return self.__servie__['redis'].get('tabledatas', self.redis_datas())

    def redis_locker(self):
        return self.__servie__['redis'].get('locker', self.redis_mix())

    def file_configure(self):
        return self.__servie__.get('_configure_json_file_', 'none')

    def redis_pool_size(self):
        psize = int(self.__servie__.get('redis.pool.size', 0))
        if psize <= 0 or psize > 255:
            if self.mode() == 2:  # 审核服
                return 2
            else:
                return 16
        else:
            return psize

    def conn_ip_port_list(self):
        return self.__conn_ip_ports__

    def bridge_ip_port_list(self):
        return self.__bridge_tcplist__

    def conn_server_ids(self):
        return self.__conn_srv_ids__

    def http_global_sync_center(self):
        return self.__servie__.get('http.global.sync.center', 'http://10.3.0.3:6000')

    def http_global_api_server_online(self):
        return self.http_global_sync_center() + '/server_online'

    def http_global_api_sync_config(self):
        return self.http_global_sync_center() + '/sync_configure'

    def dump_static_info(self):
        lines = ['GLOBAL Setting Dump Begin\n']
        lines.append('GLOBAL gameid                  = %d\n' % (self.gameid()))
        lines.append('GLOBAL name                    = %s\n' % (self.name()))
        lines.append('GLOBAL mode                    = %d\n' % (self.mode()))
        lines.append('GLOBAL corporation             = %s\n' % (self.corporation()))
        lines.append('GLOBAL encodepyc               = %s\n' % (self.encodepyc()))
        lines.append('GLOBAL hook                    = %s\n' % (self.hook()))
        lines.append('GLOBAL groupkey                = %s\n' % (self.groupkey()))
        lines.append('GLOBAL prockey                 = %s\n' % (self.prockey()))
        lines.append('GLOBAL is_control_process      = %d\n' % (self.is_control_process()))
        lines.append('GLOBAL run_process_id          = %s\n' % (self.run_process_id()))
        lines.append('GLOBAL run_process_type        = %s\n' % (self.run_process_type()))
        run_process = copy.deepcopy(self.run_process())
        if 'key' in run_process:
            del run_process['key']
        lines.append('GLOBAL run_process             = %s\n' % (str(run_process)))
        run_server = self.run_server()
        if '_scripts_' in run_server:
            del run_server['_scripts_']
        if '_procids_' in run_server:
            del run_server['_procids_']
        if 'pwd' in run_server:
            del run_server['pwd']
        if 'user' in run_server:
            del run_server['user']
        lines.append('GLOBAL run_server              = %s\n' % (str(run_server)))
        lines.append('GLOBAL http_sdk                = %s\n' % (self.http_sdk()))
        lines.append('GLOBAL http_game               = %s\n' % (self.http_game()))
        lines.append('GLOBAL http_download           = %s\n' % (self.http_download()))
        lines.append('GLOBAL http_global_sync_center = %s\n' % (self.http_global_sync_center()))
        lines.append('GLOBAL log_file_name           = %s\n' % (self.log_file_name()))
        lines.append('GLOBAL path_backup             = %s\n' % (self.path_backup()))
        lines.append('GLOBAL path_bin                = %s\n' % (self.path_bin()))
        lines.append('GLOBAL path_bireport           = %s\n' % (self.path_bireport()))
        lines.append('GLOBAL path_hotfix             = %s\n' % (self.path_hotfix()))
        lines.append('GLOBAL path_log                = %s\n' % (self.path_log()))
        lines.append('GLOBAL path_script             = %s\n' % (self.path_script()))
        lines.append('GLOBAL path_webroot            = %s\n' % (self.path_webroot()))

        lines.append('GLOBAL redis_config            = %s\n' % (str(self.redis_config())))
        lines.append('GLOBAL redis_mix               = %s\n' % (str(self.redis_mix())))
        lines.append('GLOBAL redis_bicount           = %s\n' % (str(self.redis_bicount())))
        lines.append('GLOBAL redis_friend            = %s\n' % (str(self.redis_friend())))
        lines.append('GLOBAL redis_online            = %s\n' % (str(self.redis_online())))
        lines.append('GLOBAL redis_onlinegeo         = %s\n' % (str(self.redis_onlinegeo())))
        lines.append('GLOBAL redis_paydata           = %s\n' % (str(self.redis_paydata())))
        lines.append('GLOBAL redis_avatar            = %s\n' % (str(self.redis_avatar())))
        lines.append('GLOBAL redis_userkeys          = %s\n' % (str(self.redis_userkeys())))
        alist = self.redis_datas()
        for x in xrange(len(alist)):
            lines.append('GLOBAL redis_datas        [%02d] = %s\n' % (x, str(alist[x])))

        lines.append('GLOBAL file_configure          = %s\n' % (self.file_configure()))
        lines.append('GLOBAL redis_pool_size         = %d\n' % (self.redis_pool_size()))
        alist = self.conn_ip_port_list()
        for x in xrange(len(alist)):
            lines.append('GLOBAL conn_ip_port_list  [%02d] = %s\n' % (x, str(alist[x])))

        adict = self.__servie__['mysql']
        for k, v in adict.items():
            lines.append('GLOBAL mysql      [%-10s] = %s\n' % (k, str(v)))

        self.__ctx__.ftlog.info(''.join(lines))
        self.__ctx__.ftlog.info('GLOBAL Setting Dump End')


TYGlobal = TYGlobal()
