# -*- coding=utf-8 -*-

import inspect, json
import os
from codecs import BOM_UTF8

class ConfigureHelper(object):

    def __init__(self):
        self._sync_domain_ = 'http://10.3.0.3:6000'
        self._workpath_ = None  # 工作路径 由tygame_manager进程进行初始化
        self._svnrootpath_ = None  # SVN路径 由tygame_manager进程进行初始化
        self._ctx_ = None  # SSContext 由tygame_manager进程进行初始化
        self._svn_ = None  # SvnMgr 由tygame_manager进程进行初始化

    def debug(self, *msg):
        if self._ctx_ :
            self._ctx_.log.debug(*msg)
        else:
            print msg

    def error(self, *msg):
        if self._ctx_ :
            self._ctx_.log.error(*msg)
        else:
            print msg

    def trim_bom(self, strdata, bom=BOM_UTF8):
        if strdata.startswith(bom):
            return strdata[len(bom):]
        else:
            return strdata

    def clone_data(self, data):
        return json.loads(json.dumps(data))

    def get_sync_domain(self, syncapi):
        return self._sync_domain_ + syncapi

    def sync_webget_json(self, posturl, postdatas):
        return self._ctx_.WebPage.sync_webget_json(posturl, postdatas)

    def get_relative_data_path(self, model):
        '''
        取得当前模块的数据相对路径
        例如: 如果PY文件为: gdata/gameids.py
        那么返回: gdata/gameids
        '''
        if getattr(model, '_relative_data_path_', None) == None :
            pyfile = inspect.getabsfile(model.__class__)
            model._relative_data_path_ = pyfile[len(os.path.normpath(self._workpath_)) + 1:-3]
        return model._relative_data_path_

    def get_redid_data_key(self, model):
        '''
        取得当前模块的REDIS数据键值
        例如: 如果PY文件为: gdata/gameids.py
        那么返回: 'gdata:gameids'
        '''
        keypath = self.get_relative_data_path(model)
        keypath = keypath.replace('/', ':')
        return keypath

    def get_json_data_file_path(self, model, svntag, clientid):
        p = self._svnrootpath_ + '/' + svntag + '/' + self.get_relative_data_path(model) + '/' + clientid + '.json'
        p = os.path.abspath(p)
        return p

    def find_sub_files(self, srcpath, extname='.json'):
        pyfiles = []
        srcpath = os.path.abspath(srcpath)
        cutlen = len(srcpath) + 1
        _extname = '_' + extname
        for root, _, files in os.walk(srcpath, True):
            for name in files:
                fpath = os.path.join(root, name)
                fpath = fpath[cutlen:]
                if fpath.endswith(extname) \
                    and (not fpath.endswith(_extname)) \
                    and (not fpath.split('/')[-1][0] in ('_', '.')) :
                    pyfiles.append(os.path.normpath(fpath))
        return pyfiles

    def add_json_data_file(self, svntag, clientid, jsonfile):
        self.write_json_data_file(jsonfile, None)
        self._svn_.svnadd(jsonfile)

    def write_json_data_file(self, jsonfile, datas):
        fp = None
        try:
            fp = open(jsonfile, 'w')
            if not isinstance(datas, (str, unicode)) :
                wdata = json.dumps(datas, sort_keys=True, indent=4, separators=(',', ':'))
            else:
                wdata = datas
            fp.write(wdata)
            fp.close()
        except Exception, e:
            raise e
        finally:
            try:
                fp.close()
            except:
                pass
        
    def read_json_data_file(self, jsonfile, needException=False):
        fp, datas = None, None
        try:
            self.debug('read_json_data_file----->>>>>>', jsonfile)
            fp = open(jsonfile)
            datas = json.loads( self.trim_bom(fp.read()) )
            fp.close()
        except Exception, e:
            if needException :
                raise e
            else:
                self.error(e)
        finally:
            try:
                fp.close()
            except:
                pass
        return datas        

    def decode_utf8_objs(self, datas):
        if isinstance(datas, dict) :
            ndatas = {}
            for key, val in datas.items() :
                if isinstance(key, unicode) :
                    key = key.encode('utf-8')
                ndatas[key] = self.decode_utf8_objs(val)
            return ndatas
        if isinstance(datas, list) :
            ndatas = []
            for val in datas :
                ndatas.append(self.decode_utf8_objs(val))
            return ndatas
        if isinstance(datas, unicode) :
            return datas.encode('utf-8')
        return datas

    def load_all_models(self, workpath, svnrootpath, _ctx_, _svn_):
        # 初始化ConfigureHelper
        if os.sys.path[0] != workpath :
            os.sys.path.insert(0, workpath)
        self._workpath_ = workpath
        self._svnrootpath_ = svnrootpath
        self._ctx_ = _ctx_
        self._svn_ = _svn_

        self.CACHE = {}
        self.INFODICT = {}
        pyfiles = self.find_sub_files(workpath, '.py')
        for pyfile in pyfiles :
            model = self.__new_model__(workpath, pyfile)
            info = model.get_info()
            dstyle = model.get_data_style()
            svnpath = self.get_relative_data_path(model)
            modelinfo = {'name' : info['name'],
                         'svnpath' : svnpath,
                         'catalog' : dstyle,
                         'instance' : model
                         }
            self.CACHE[svnpath] = modelinfo
            if not dstyle in self.INFODICT :
                self.INFODICT[dstyle] = []
            self.INFODICT[dstyle].append({'name':info['name'], 'svnpath': svnpath})

        for _, x in self.INFODICT.items() :
            x.sort(key=lambda x: x['name'])
        pass

    def __new_model__(self, basepath, pyfile):
        self.debug('__new_model__->', basepath, '->', pyfile)
        pypkg = pyfile.replace('/', '.')[0:-3]
        if pypkg[0] == '.' :
            pypkg = pypkg[1:]
        self.debug('__new_model__ pkg->', pypkg)
        control = None
        execstr = '''
from %s import ConfigureData
control = ConfigureData()
        ''' % (pypkg)
        exec(execstr)
        return control

ConfigureHelper = ConfigureHelper()
