# -*- coding: utf-8 -*-

import json
import os


class fileutil(object):
    def __call__(self, *argl, **argd):
        return self

    def _init_ctx_(self):
        from tyframework.context import TyContext
        self.__ctx__ = TyContext

    def __init__(self):
        pass

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
            datas = self.__ctx__.strutil.decode_objs_utf8(datas)
        fp.close()
        return datas

    def copy_file(self, fromFile, toFile):
        from shutil import copyfile as copyfile2
        copyfile2(fromFile, toFile)

    def delete_file(self, fromFile):
        os.remove(fromFile)

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


fileutil = fileutil()
