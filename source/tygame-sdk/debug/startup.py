#! encoding=utf-8

__author__ = 'yuejianqiang'

"""
python startup.py 172.16.8.166:6379:0:http-local_test-9998-0
work_dir=./debug
"""


import init_env
import sys
import os
from tyframework import server
import traceback

def main():
    #prockey = '172.16.0.243:6379:0:game-hall_test_intranet-9999-1'
    #procclass = ''
    os.environ['PATH_SCRIPT'] = '../script'
    os.environ['PATH_LOG'] = '../logs'
    os.environ['PATH_WEBROOT'] = '../tygame-hall/webroot'
    if not os.path.isdir('../logs'):
        os.makedirs('../logs')
    if not os.path.isdir('../bireport'):
        os.makedirs('../bireport')
    server.main()

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
        print 'byebye'
