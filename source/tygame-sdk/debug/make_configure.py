#! encoding=utf-8

__author__ = 'JQ'

"""
python make_configure.py -m test_intranet_tg.json -a configure
work_dir=./
"""


import init_env
import sys
sys.path.append('/Users/yuejianqiang/workspace/tuyoo/newsvn/freetime4/tags/tyframework-tag-release-20150910/shell2')
#sys.path.append('../tyframework/src')
#sys.path.append('../game-sdk/src')
from _pygamecontrol_._action_load_service_ import action_load_service
from _pygamecontrol_._action_make_begin_ import action_make_begin
from _pygamecontrol_._action_make_configure_ import action_make_configure
from _pygamecontrol_._action_make_end_ import action_make_end



def main():
    params = {
        'action': 'configure',
        'servicefile': './local_test.json',
        '__pyscript_path__':  './',
        '__source_path__':  './',
        'autobackup':True,
        'CONFIGURE_SERVICE_FILE': '../bin/__service__.json',
        'CONFIGURE_OUTPUTS_FILE': '../bin/__outputs__.json',
    }

    action_load_service(params)
    action_make_begin(params)
    action_make_configure(params, ['../tyframework/src', '../game-sdk/src'])
    action_make_end(params)

if __name__ == '__main__':
    main()