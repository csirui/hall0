#! encoding=utf-8

__author__ = 'yuejianqiang'


"""
python reload_configure.py install_configure_json
work_dir = ./debug
"""

import os
import sys
import init_env
sys.path.append('/Users/yuejianqiang/workspace/tuyoo/newsvn/freetime4/trunk/tyframework/shell2/shscript/python')

os.environ['PATH_SCRIPT'] = '../script'
os.environ['PATH_LOG'] = '../logs'
os.environ['PATH_WEBROOT'] = '../game-sdk/webroot'

from hotcmd import main


# pypy load_configure.py
main()

