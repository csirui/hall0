# -*- coding: utf-8 -*-

import commands
import json
import os
import socket
import sys
import threading
import traceback
import uuid

import datetime
import paramiko
import redis


class mylog(object):
    def __init__(self):
        self._logfile_ = None
        self._RED = '\033[1;31;40m'
        self._YELLOW = '\033[1;33;40m'
        self._CYAN = '\033[1;35;40m'
        self._BLUE = '\033[1;36;40m'
        self._RECOVERY = '\033[0m'
        self.colors = [
            self._RED,
            self._YELLOW,
            self._CYAN,
            self._BLUE,
            self._RECOVERY
        ]

    def open_log_file(self, logpath):
        if self._logfile_ == None:
            actuuid = os.environ.get('WEB_SHELL_ACTION_UUID', None)
            if actuuid:
                self._logfile_ = open(logpath + '/webshelllog/act-' + actuuid + '.log', 'a')
            else:
                self._logfile_ = open(logpath + '/action.log', 'a')

    def close_log_file(self):
        if self._logfile_:
            self._logfile_.close()
            self._logfile_ = None

    def __make_row__(self, params):
        line = []
        for v in params:
            try:
                if isinstance(v, unicode):
                    v = v.encode('utf-8')
                elif isinstance(v, (list, tuple, dict)):
                    v = repr(v)
                else:
                    v = str(v)
                line.append(v)
            except:
                line.append(repr(v))
        line = ' '.join(line)
        return line

    def __make_line__(self, params):
        ct = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
        line = [ct, '|', self.__make_row__(params), '\n']
        line = ' '.join(line)
        return line

    def uncolormsg(self, msg):
        for c in self.colors:
            msg = msg.replace(c, '')
        return msg

    def log(self, *params):
        line = self.__make_line__(params)
        sys.stdout.write(line)
        sys.stdout.flush()
        if self._logfile_:
            line = self.uncolormsg(line)
            self._logfile_.write(line)
            self._logfile_.flush()

    def write(self, msg):
        if self._logfile_:
            msg = self.uncolormsg(msg)
            self._logfile_.write(msg)
            self._logfile_.flush()

    def exception(self, *params):
        self.log('************************************************************')
        self.log(*params)
        traceback.print_exc()
        self.log('************************************************************')

    def error(self, *msg):
        params = ['ERROR !!']
        params.extend(msg)
        line = self.__make_row__(params)
        self.log(self.wrap_color_red(line))
        return 0

    def wrap_color_red(self, *params):
        line = self.__make_row__(params)
        return "%s%s%s" % (self._RED, line, self._RECOVERY)

    def wrap_color_yellowd(self, *params):
        line = self.__make_row__(params)
        return "%s%s%s" % (self._YELLOW, line, self._RECOVERY)

    def wrap_color_blue(self, *params):
        line = self.__make_row__(params)
        return "%s%s%s" % (self._BLUE, line, self._RECOVERY)

    def wrap_color_cyan(self, *params):
        line = self.__make_row__(params)
        return "%s%s%s" % (self._CYAN, line, self._RECOVERY)


mylog = mylog()


class myfiles(object):
    def __init__(self):
        self.path_pwd = None

    def make_dirs(self, checkdir):
        if os.path.exists(checkdir) == False:
            os.makedirs(checkdir)

    def write_file(self, fpath, fname, content):
        if isinstance(content, (list, tuple, dict, set)):
            content = json.dumps(content, sort_keys=True, indent=4, separators=(',', ':'))
        if (fpath != None and len(fpath) > 0):
            fullpath = fpath + '/' + fname
        else:
            fullpath = fname
        rfile = open(fullpath, 'w')
        rfile.write(content)
        rfile.close()

    def read_file(self, fpath):
        try:
            if os.path.isfile(fpath):
                f = open(fpath, 'rb')
                c = f.read()
                f.close()
                return c
        except:
            pass
        return None

    def read_json_file(self, fpath, needdecode=False):
        fp = open(fpath, 'r')
        datas = json.load(fp)
        if needdecode:
            datas = self.decode_objs_utf8(datas)
        fp.close()
        return datas

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

    def copy_file(self, fromFile, toFile):
        from shutil import copyfile as copyfile2
        copyfile2(fromFile, toFile)

    def delete_file(self, fromFile):
        os.remove(fromFile)

    def copy_files(self, cfrom, cto):
        if os.path.exists(cfrom) and os.path.exists(cto) and cfrom != cto:
            mylog.log('拷贝源文件 : %s/* -> %s' % (cfrom, cto))
            cmd = 'cp -fr %s/* %s' % (cfrom, cto)
            status, output = commands.getstatusoutput(cmd)
            if status != 0:
                mylog.log('ERRROR !!', '文件拷贝失败:', cfrom, cto, output)
                return 0
        return 1

    def link_files_all(self, fpaths, tpaths):
        for fpath, tpath in zip(fpaths, tpaths):
            msg = '链接目录 : %s -> %s\n' % (fpath, tpath)
            sys.stdout.write(msg)
            mylog.write(msg)
            if not os.path.exists(fpath):
                continue
            if not os.path.exists(tpath):
                os.makedirs(tpath)
            for each in os.listdir(fpath):
                source = os.path.realpath(os.path.join(fpath, each))
                target = os.path.join(tpath, each)
                if os.path.exists(target):
                    if os.path.realpath(target) == source:
                        continue
                    else:
                        os.remove(target)
                os.symlink(os.path.realpath(source), target)
        return 1

    def copy_files_all(self, fpaths, tpaths):
        outfiles = []
        copyed = set()
        mpaths = set()
        for x in xrange(len(fpaths)):
            fpath = fpaths[x]
            tpath = tpaths[x]

            msg = '拷贝目录 : %s -> %s\n' % (fpath, tpath)
            sys.stdout.write(msg)
            mylog.write(msg)

            mlen = 0
            fpath = self.abspath(fpath)
            ffiles = []
            outfiles.append(ffiles)
            cutlen = len(fpath)
            for parent, _, filenames in os.walk(fpath):
                for filename in filenames:
                    filename = parent + '/' + filename
                    if filename.find('.svn') < 0:
                        ffiles.append(filename)
                        mlen = max(len(filename), mlen)
            mlen += 4

            lformat = '拷贝 : [%d/' + str(len(ffiles)) + '] %-' + str(mlen) + 's'
            for x in xrange(len(ffiles)):
                fname = ffiles[x]
                if fname in copyed:
                    continue
                copyed.add(fname)
                cpto = tpath + fname[cutlen:]
                cpdir = os.path.dirname(cpto)
                if cpdir not in mpaths:
                    if not os.path.isdir(cpdir):
                        os.makedirs(cpdir)
                        if not os.path.isdir(cpdir):
                            mylog.log('ERRROR !!', '无法建立目录:', cpdir)
                            return 0
                    mpaths.add(cpdir)

                msg = lformat % (x + 1, fname[cutlen:])
                sys.stdout.write('\r')
                sys.stdout.write(msg)

                with open(fname, 'rb') as fsrc:
                    with open(cpto, 'wb') as fdst:
                        while 1:
                            buf = fsrc.read(1024 * 64)
                            if not buf:
                                break
                            fdst.write(buf)
            msg = '拷贝 %d 文件%s\n' % (len(ffiles), ' ' * mlen)
            sys.stdout.write('\r')
            sys.stdout.write(msg)
            mylog.write(msg)
        return 1

    def find_py_files(self, srcpath, extname='.py', converttoimport=False):
        pyfiles = []
        srcpath = self.abspath(srcpath)
        cutlen = len(srcpath) + 1
        extlen = len(extname)
        for root, _, files in os.walk(srcpath, True, followlinks=True):
            for name in files:
                fpath = os.path.join(root, name)
                fpath = fpath[cutlen:]
                if fpath.find('-') < 0 \
                        and fpath.find('dyn_') < 0 \
                        and fpath.find('/dyn/') < 0 \
                        and fpath.find('dynamic') < 0 \
                        and fpath.find('/tools/') < 0 \
                        and fpath[-extlen:] == extname \
                        and fpath.lower().find('test') < 0 \
                        and fpath.find('script/') != 0:

                    if converttoimport:
                        fpath = fpath[0:-extlen]
                        fpath = fpath.replace('/', '.')
                        fpath = 'import ' + fpath
                    pyfiles.append(fpath)
        return pyfiles

    def make_path(self, mpath, clear=False):
        if os.path.exists(mpath):
            if clear:
                mylog.log('清空目录 :', mpath)
                status, output = commands.getstatusoutput('rm -fr %s/*' % (mpath))
                if status != 0:
                    mylog.log('ERRROR !!', '无法删除目录:', mpath, output)
                    return None
        else:
            os.mkdir(mpath)
        if not os.path.exists(mpath):
            mylog.log('ERRROR !!', '无法建立目录:', mpath)
            return None
        return mpath

    def delete_path(self, mpath):
        if os.path.exists(mpath):
            mylog.log('删除目录 :', mpath)
            status, output = commands.getstatusoutput('rm -fr %s' % (mpath))
            if status != 0:
                mylog.log('ERRROR !!', '无法删除目录:', mpath, output)
                return None
        return mpath

    def normpath(self, apath):
        return os.path.normpath(apath)

    def abspath(self, apath):
        return os.path.abspath(apath)

    def get_parent_dir(self, apath, level=1):
        for _ in xrange(level):
            apath = os.path.dirname(apath)
        return apath

    def file_exists(self, afile):
        return os.path.isfile(afile)

    def dir_exists(self, afile):
        return os.path.isdir(afile)

    def get_pwd(self):
        if self.path_pwd == None:
            self.path_pwd = commands.getoutput('pwd')
        return self.path_pwd


myfiles = myfiles()


class myhelper(object):
    def __init__(self):
        self.__ifconfig__ = None
        self.__whoami__ = None
        self.__pings__ = {}

    def is_local_ip(self, ip):
        if self.__ifconfig__ == None:
            self.ifconfig = commands.getoutput('ifconfig')
        if self.ifconfig and self.ifconfig.find('command not found') >= 0:
            self.ifconfig = commands.getoutput('/sbin/ifconfig')
        if self.ifconfig.find('addr:' + ip + ' ') < 0:
            if self.ifconfig.find('inet ' + ip + ' ') < 0:
                return False
        return True

    def whoami(self):
        if self.__whoami__ == None:
            self.__whoami__ = commands.getoutput('whoami')
        return self.__whoami__

    def ping_host(self, ip):
        if ip in self.__pings__:
            return self.__pings__[ip]
        # ping 1秒钟超时
        if os.sys.platform == 'darwin':  # MacOs
            sts, _ = commands.getstatusoutput('ping -t 1 ' + ip)
        else:
            sts, _ = commands.getstatusoutput('ping -w 1 ' + ip)
        self.__pings__[ip] = sts
        if sts == 0:
            return True
        return False

    def check_ssh_port(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((host, 22))
            s.close();
        except:
            return False
        return True

    def get_redis_pipe(self, redisdef):
        rconn = redis.StrictRedis(host=redisdef['host'], port=redisdef['port'], db=redisdef['dbid'])
        rpipe = rconn.pipeline()
        return rpipe

    def load_py_configures(self, pyfilepath, returnKey, envdict=None):
        try:
            if envdict == None:
                envdict = {}
            envdict['__env__'] = envdict
            execfile(pyfilepath, envdict, envdict)
            if returnKey:
                return envdict[returnKey]
            return True
        except:
            mylog.exception()
        return None

    def get_env(self, ekey, defaultval):
        return os.environ.get(ekey, defaultval)

    def save_last_output(self, params):
        allfile = params['service']['paths']['script'] + '/control.json'
        mylog.log('输出控制文件 :', allfile)
        myfiles.write_file('', allfile, params)

    def load_last_output(self, params):
        controlfile = params['__source_path__'] + '/../script/control.json'
        controlfile = myfiles.abspath(controlfile)
        if not os.path.exists(controlfile):
            return None
        mylog.log('装载控制文件 :', controlfile)
        datas = myfiles.read_json_file(controlfile, True)
        return datas

    def action_common_init(self, actparams, can_not_found=False):
        if 'service' in actparams:
            return actparams
        params = self.load_last_output(actparams)
        if not params:
            if not can_not_found:
                mylog.log('找不到上次编译的结果control.json 无法进行后续操作')
            return None
        actparams.update(params)
        return params

    def cread_thread(self, fun_run, *params):
        t = threading.Thread(target=fun_run, args=params)
        t.start()
        return t


myhelper = myhelper()


class myssh(object):
    def __init__(self):
        self.sshsavepath = os.path.expanduser('~') + '/.ssh'
        self.__SSH_CLIENT__ = {}
        self.__SFTP_CLIENT__ = {}

    def connect(self, ip, user, password, port=22, reconnect=False):
        try:
            if reconnect:
                if ip in self.__SFTP_CLIENT__:
                    try:
                        self.__SFTP_CLIENT__[ip].close()
                    except:
                        pass
                    del self.__SFTP_CLIENT__[ip]
                if ip in self.__SSH_CLIENT__:
                    try:
                        self.__SSH_CLIENT__[ip].close()
                    except:
                        pass
                    del self.__SSH_CLIENT__[ip]

            if not ip in self.__SFTP_CLIENT__:
                s = paramiko.SSHClient()

                if password and len(password) > 0:
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    s.connect(ip, port, user, password, timeout=15)
                else:
                    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    hpath = os.path.expanduser('~')
                    key = paramiko.RSAKey.from_private_key_file(hpath + '/.ssh/id_rsa')
                    s.load_system_host_keys()
                    s.connect(ip, port, user, pkey=key)

                self.__SSH_CLIENT__[ip] = s
                self.get_sftp(ip)

        except Exception, e:
            mylog.log('SSH连接', user, '@', ip, '失败')
            raise e

    def get_ssh(self, ip):
        return self.__SSH_CLIENT__[ip]

    def get_sftp(self, ip):
        sftp = self.__SFTP_CLIENT__.get(ip, None)
        if sftp == None:
            sftp = self.__SSH_CLIENT__[ip].open_sftp()
            self.__SFTP_CLIENT__[ip] = sftp
        return sftp

    def release_all(self):
        for s in self.__SFTP_CLIENT__.values():
            try:
                s.close()
            except:
                pass
        for s in self.__SSH_CLIENT__.values():
            try:
                s.close()
            except:
                pass
        self.__SSH_CLIENT__ = {}
        self.__SFTP_CLIENT__ = {}

    def __write_remote_tmp_sh__(self, ip, lines):

        checkret = '''
TY_REMOTE_SSH_EXEC_RESULT_=$?
if [ ${TY_REMOTE_SSH_EXEC_RESULT_} -ne 0 ]
then
echo "TY_REMOTE_SSH_EXEC_RESULT_=${TY_REMOTE_SSH_EXEC_RESULT_}"
exit ${TY_REMOTE_SSH_EXEC_RESULT_}
fi
'''
        sftp = self.get_sftp(ip)
        remotepath = '/tmp/' + str(uuid.uuid1())
        fo = sftp.open(remotepath, 'w')
        for line in lines:
            fo.write(line)
            fo.write('\n')
        fo.write('\n\n')
        fo.write(checkret)
        fo.write('\n\n')
        fo.write('rm -fr ' + remotepath)
        fo.write('\n\n')
        fo.flush()
        fo.close()
        return remotepath

    def executecmds(self, ip, cmdlist):
        if isinstance(cmdlist, (str, unicode)):
            cmdlist = [cmdlist]
        cmd = self.__write_remote_tmp_sh__(ip, cmdlist)
        sclient = self.get_ssh(ip)
        ret = 0
        _, stdout, stderr = sclient.exec_command('sh ' + cmd, get_pty=True)
        lines = []
        for line in stdout:
            line = line.strip()
            lines.append(line)
            if line.find('TY_REMOTE_SSH_EXEC_RESULT_') >= 0:
                ret = int(line.split('=')[1])
        for line in stderr:
            lines.append(line.strip())
            if ret == 0:
                ret = 1
        sclient.exec_command('rm -fr ' + cmd, get_pty=True)
        return ret, '\n'.join(lines)

    def mkdirs(self, ip, mpath):
        if isinstance(mpath, (str, unicode)):
            mpath = [mpath]
        lines = []
        for p in mpath:
            p = os.path.abspath(p)
            cmd = '''if [ ! -d  '%s' ] \n then \n mkdir -p '%s' \n fi\n''' % (p, p)
            lines.append(cmd)
        ret = self.executecmds(ip, lines)
        return ret

    def __file_callback__(self, size, filesize):
        pass

    def put_file(self, ip, localpath, remotepath, fun_callback):
        if not fun_callback:
            fun_callback = self.__file_callback__
        sftp = self.get_sftp(ip)
        attrs = sftp.put(localpath, remotepath, callback=fun_callback)
        return attrs.st_size

    def get_file(self, ip, remotepath, localpath, fun_callback):
        if not fun_callback:
            fun_callback = self.__file_callback__
        sftp = self.get_sftp(ip)
        attrs = sftp.get(remotepath, localpath, callback=fun_callback)
        return attrs.st_size


myssh = myssh()


def localrun(cmdline):
    """Return (status, output) of executing cmd in a shell."""
    import subprocess
    p = subprocess.Popen(cmdline, shell=True, close_fds=True, bufsize=-1, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    outs = p.stdout.readlines()
    sts = p.wait()
    text = ''.join(outs)
    return sts, text
