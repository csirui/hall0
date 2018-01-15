# -*- coding: utf-8 -*-

import commands
from _main_helper_ import myfiles, mylog, myhelper

def action_make_encrypt_pyc(actparams):
    '''
    将pyc进行途游方式的加密处理，加密后必须使用途游的pypy-enc进行运行
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0
    service = params['service']

    # 加密处理
    if service['encodepyc'] :
        mylog.log('加密运行处理')
        compilepath = service['paths']['bin']
        cmd = 'find %s -name "*.py" | xargs rm -fr' % (compilepath)
        status, output = commands.getstatusoutput(cmd)
        if status != 0 :
            mylog.log('ERRROR !!', '加密模式，游戏工程py文件删除失败:', compilepath)
            mylog.log(status, output)
            return 0
        pycfiles = myfiles.find_py_files(compilepath, '.pyc', False)
        for pycfile in pycfiles :
            __tuyoo_enc_pyc_file__('%s/%s' % (compilepath, pycfile))
        mylog.log('加密运行处理完成')

    return 1

'''
Encode pyc file for protect source code, this pyc can load only by pypy-enc.
zhouxin.
'''

def __tuyoo_zxor__(sbuf):
    sestr = '3243243243201013812039291074083725638295840918037128964732657947591783291738291738921748932758932758924760926639173892173921'
    dbuf = ''
    for x in xrange(len(sbuf)):
        dbuf = dbuf + chr(ord(sbuf[x]) ^ ord(sestr[x % (len(sestr))]))
    return dbuf

def __tuyoo_enc_pyc_file__(pycfile):
    ff = open(pycfile, 'rb')
    fbuf = ff.read()
    abuf = fbuf[:8]
    abuf = abuf + __tuyoo_zxor__(fbuf[8:])
    ff.close()
    fw = open(pycfile, 'wb')
    fw.write(abuf)
    fw.close()
