# -*- coding: utf-8 -*-

from _main_hot_cmd_ import execute_hot_cmd

def action_configure_update(actparams):
    '''
    执行当前的配置装载脚本，更新所有运行服务的配置内容
    '''
    return execute_hot_cmd(actparams, '更新配置文件', 'reload_configure_json')
