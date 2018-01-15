# -*- coding: utf-8 -*-

import os
import sys
import time


def useage():
    print '''
TuYoo Game Server Controler V1.1

用法:game.sh -m [服务定义文件]   以服务定义文件为基础编译整个游戏工程
  或:game.sh -a start            使用最后一次成功编译的内容，启动所有服务进程
  或:game.sh -a stop             使用最后一次成功编译的内容，停止所有服务进程
  或:game.sh -a configure        重新编译游戏配置文件REDIS内容，并通知所有服务重新加载游戏配置
  或:game.sh -a webroot          重新拷贝所有工程的webroot内容，进行压缩处理后，推送到所有服务器
  或:game.sh -a push             重新推送最后一次编译的内容到所有服务器
  或:game.sh -a clean            删除本机最后一次编译的所有内容
  或:game.sh -a clean_all        删除所有机器上的编译结果或日志输出
  或:game.sh -a backup           备份本机最后一次编译的内容
  或:game.sh -hotfix <filename>  推送hotfix目录下的所有文件到各个服务器,并在各个服务器执行给出的文件           
  或:game.sh -h                  打印帮助(本信息)并退出
   
其他参数:
   -noback     在进行操作时，不进行自动的备份操作,缺省情况下-m -a start configure webroot命令会自动进行备份操作

'''
    return 0


def parse_cmd_lines():
    params = {'autobackup': True}
    for x in xrange(1, len(sys.argv)):
        flg = sys.argv[x]
        if flg == '-m':
            params['servicefile'] = sys.argv[x + 1]
            x = x + 1

        if flg == '-hotfix':
            params['hotfix'] = sys.argv[x + 1]
            x = x + 1

        if flg == '-a':
            params['action'] = sys.argv[x + 1]
            x = x + 1

        if flg == '-noback':
            params['autobackup'] = False

    mfileroot = os.path.abspath(__file__)
    if 'PATCH_PYSCRIPT_PATH' in os.environ:
        mfileroot = os.environ['PATCH_PYSCRIPT_PATH']
    mfileroot = os.path.dirname(mfileroot)
    mfileroot = os.path.dirname(mfileroot)

    os.sys.path.insert(0, mfileroot)

    params['__pyscript_path__'] = mfileroot
    params['__source_path__'] = os.path.dirname(os.path.dirname(mfileroot))

    return params


tasks = []


def add_tasks(task):
    global tasks
    tasks.append(task)


def main():
    params = parse_cmd_lines()

    needenv = False
    try:
        import redis
    except:
        needenv = True
        print 'ERROR !! python的运行环境缺少redis模块'
    try:
        import paramiko
    except:
        needenv = True
        print 'ERROR !! python的运行环境缺少paramiko模块'

    if needenv:
        print '请以root用户执行以下命令安装缺少模块:'
        print ''
        print 'sh ' + params['__pyscript_path__'] + '/shscript/install-env.sh'
        print ''
        return

    global tasks

    autobackup = params['autobackup']
    if 'servicefile' in params:
        add_tasks('action_load_service')
        add_tasks('action_make_begin')
        add_tasks('action_clean_bin')
        add_tasks('action_make_copy_source')
        add_tasks('action_make_compile_pyc')
        add_tasks('action_make_configure')
        add_tasks('action_make_script')
        add_tasks('action_make_webroot')
        add_tasks('action_make_encrypt_pyc')
        add_tasks('action_make_end')

    action = params.get('action', '')

    if action == 'prepare':
        add_tasks('action_push_bin')
        add_tasks('action_stop')
        add_tasks('action_configure_install')

    if action == 'start':
        add_tasks('action_push_bin')
        add_tasks('action_stop')
        add_tasks('action_configure_install')
        add_tasks('action_start')

    if action == 'stop':
        add_tasks('action_stop')

    if action == 'clean':
        add_tasks('action_clean_log')
        add_tasks('action_clean_bin')

    if action == 'clean_all':
        add_tasks('action_clean_all')

    if len(tasks) == 0:
        return useage()
    ct = time.time()
    from _main_helper_ import mylog
    try:
        roopath = os.path.dirname(params['__source_path__'])
        mylog.open_log_file(roopath)
        mylog.log('操作根目录 :', roopath)
        mylog.log('======================================================================')
        mylog.log('任务列表 :', tasks)
        mylog.log('======================================================================')
        for x in xrange(len(tasks)):
            task = tasks[x]
            mylog.log(mylog.wrap_color_cyan('执行任务 [%d/%d] : %s' % (x + 1, len(tasks), task)))
            tfun = None
            taskstr = 'from _%s_ import %s as tfun' % (task, task)
            exec taskstr
            if tfun(params) != 1:
                return 1
        mylog.log('')
        mylog.log('完成. 使用时间 %0.2f 秒' % (time.time() - ct))
        mylog.log('========================== done ============================================')
        return 0
    finally:
        try:
            mylog.close_log_file()
        except:
            pass


if __name__ == '__main__':
    main()
