# -*- coding: utf-8 -*-

import os, sys
from _main_helper_ import myhelper, mylog, myfiles

def action_make_webroot(actparams):
    '''
    压缩处理当前的编译输出路径的webroot中的js、html文件
    '''
    params = myhelper.action_common_init(actparams)
    if not params :
        return 0

    # 压缩webroot
    __mini_webroot__(params)

    return 1

def __mini_webroot__(params):
    wwwroot = params['service']['paths']['webroot']
    jarpath = params['__pyscript_path__']

    mylog.log('压缩WEBROOT :', wwwroot)
    
    basename = os.path.basename(wwwroot)

    htmlfiles = []
    for parent, _, filenames in os.walk(wwwroot):
        if parent.find('.svn') < 0 and parent.find('configure') < 0 :
            for filename in filenames:
                if filename.find('.svn') < 0 :
                    fnames = filename.split('.')
                    ext = fnames[-1]
#                     if ext == 'html' : # 某些情况下, 编码错乱, 不进行压缩处理了
#                         htmlfiles.append(('html', parent, filename))
                    if ext == 'js' or ext == 'css':
                        if not 'min' in fnames :
                            htmlfiles.append(('java', parent, filename))

    count = len(htmlfiles)
    maxlen = 0
    for x in xrange(count):
        mtype, parent, filename = htmlfiles[x]
        maxlen = max(maxlen, len(parent + '/' + htmlfiles[x][2]))
    maxlen += 10

    for x in xrange(count):
        htmlfile = htmlfiles[x]
        mtype, parent, filename = htmlfile
        fullpath = parent + '/' + filename
        
        logoutpath = fullpath
        while len(logoutpath) < maxlen :
            logoutpath = logoutpath + ' '
        sys.stdout.write('\r')
        sys.stdout.write('min web file [%d/%d] %s' % (x + 1, count, logoutpath))

        if mtype == 'html' :
            content = __execute_html__(fullpath)
        else:
            buffilepath = fullpath.replace('/' + basename + '/', '/.' + basename + '/')
            bufcontent = myfiles.read_file(buffilepath)
            newcontent = myfiles.read_file(fullpath)
            if bufcontent == newcontent :
                content = myfiles.read_file(buffilepath + '.mindata_')
            else:
                fnames = filename.split('.')
                content = __execute_java__(jarpath, fnames[-1], fullpath)
                myfiles.make_dirs(os.path.dirname(buffilepath))
                myfiles.write_file('', buffilepath, newcontent)
                myfiles.write_file('', buffilepath + '.mindata_', content)
        myfiles.write_file('', fullpath, content)
    sys.stdout.write('\rmin web file %d done.%s\n' % (count, ' ' * maxlen))

def __execute_java__(jarpath, ext, fromFile):
    import subprocess
    cmd = 'java -jar %s/shscript/yui.jar --type %s --charset utf-8 %s'
    cmd = cmd % (jarpath, ext, fromFile)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in p.stdout.readlines():
        lines.append(line)
    p.wait()
    out = ''.join(lines)
    return out

def __execute_html__(fullpath):
    lines = []
    nfile = open(fullpath)
    for line in nfile.readlines():
        line = line.strip()
        if len(line) > 0 :
            lines.append(line)
    nfile.close()
    html = '\n'.join(lines)
    return html
