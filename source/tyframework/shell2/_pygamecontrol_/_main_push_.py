# -*- coding: utf-8 -*-

import os
from _main_helper_ import mylog, myfiles, myssh
from _main_thread_ import mutil_thread_server_action
from _main_tarfile_ import tar_gzip_folders, PACK_TYPE_TGZ

def push_dirs_to_all_server(params, actname, push_dirs):

    service = params['service']
    servers = service['servers']
    if len(servers) == 1 :
        if servers[0].get('localhost', 0) == 1:
            mylog.log(actname, ':', '本机运行,无需推送')
            return 1

    pushfile = tar_gzip_folders(params, PACK_TYPE_TGZ, push_dirs)
    if pushfile == None :
        return 0
    params['pushfile'] = pushfile

    mylog.log(mylog.wrap_color_cyan(actname))

    haserror = mutil_thread_server_action(params, __thread_action_push__)
    if haserror :
        mylog.error(actname, ':', '失败 !!')
        return 0

    mylog.log(actname + '完成')
    return 1

def __thread_action_push__(controls):

    '''
    这个方法运行再多线程当中
    '''
    result = 0
    outputs = ''
    try:
        if controls['server'].get('localhost', 0) == 1 :
            controls['percent'] = '+++%'
            result = 1
        else:
            result, outputs = __thread_action_push_ssh__(controls)
    except:
        result = 2  # 代码异常
        mylog.exception()

    controls['done'] = 1
    controls['result'] = result
    controls['outputs'] = outputs

def __thread_action_push_ssh__(controls):
    
    controls['percent'] = '---%'
    
    params = controls['params']
    service = controls['service']
    server = controls['server']
    pushfile = params['pushfile']
    pushpath = myfiles.get_parent_dir(pushfile)
    
    ip = server['sshhost']
    myssh.connect(ip, server['user'], server['pwd'], server['port'])
    paths = [pushpath]
    paths.extend(service['paths'].values())
    
    controls['percent'] = '--+%'
    
    status, outputs = myssh.mkdirs(ip, paths)
    if status != 0 :
        return 2, '远程目录建立失败\n' + myfiles.decode_objs_utf8(outputs)

    controls['percent'] = '-++%'
    
    controls['percent'] = '000%'
    localfilesize = os.path.getsize(pushfile)
    
    def update_send_size(sendsize_, allsize_):
        if sendsize_ == allsize_ :
            p = 100
        else:
            p = int((float(sendsize_) / float(allsize_)) * 100)
        controls['percent'] = '% 3d' % (p) + '%'

    putsize = myssh.put_file(ip, pushfile, pushfile, update_send_size)
    if int(putsize) != localfilesize :
        return 2, 'SSH推送失败'

    cmdlist = ['cd %s' % (os.path.dirname(pushpath)),
               'tar xf %s' % (pushfile),
               ]
    controls['percent'] = '+++%'
    status, outputs = myssh.executecmds(ip, cmdlist)
    if status != 0 :
        return 2, '解压缩失败\n' + myfiles.decode_objs_utf8(outputs)

    controls['percent'] = '++++'
    return 1, ''

