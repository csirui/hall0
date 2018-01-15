# -*- coding=utf-8 -*-

# usage:
# $ export PYTHONPATH=$(pwd)/src:$(pwd)/test:$(pwd)/../tyframework/src
# $ python -m unittest -f test_channels.TestChannels

from datetime import datetime
from mock import Mock, MagicMock, patch
import unittest
import random
import json

from tysdk.entity.duandai.channels import Channels

def my_print(*args):
    for arg in args:
        print arg,
    print

class TestChannels(unittest.TestCase):

    @patch('tysdk.entity.duandai.channels.TyContext')
    def test_select_a_channel_case1(self, ctx):
        candidates = ['yipay']
        ctx.ftlog.debug = my_print
        ctx.Configure.get_global_item_json.return_value = ''
        ctx.RedisPayData.execute.return_value = ''
        c = Channels()
        c._drop_capped_paytypes = MagicMock()
        c._get_default_channels = MagicMock()
        with self.assertRaises(Exception) as e:
            c._drop_capped_paytypes.return_value = []
            c.select_a_channel(
                'chinaMobile', 51, 2, 'clientid', 10001, candidates)
        self.assertEqual(e.exception.message, 'can NOT select_a_channel from NULL candidates')

        c._drop_capped_paytypes.return_value = ['ydmm_123', 'ydjd_321']
        c._get_default_channels.return_value = [
            {"channel": "yipay", "share": 0, "precedence": 100 },
            {"channel": "linkyun.api", "share": 0, "precedence": 200 }, ]
        ctx.Configure.get_global_item_json.return_value = ''
        with self.assertRaises(Exception) as e:
            c.select_a_channel(
                'chinaMobile', 51, 2, 'clientid', 10001, candidates)
        self.assertEqual(e.exception.message, 'select_a_channel NO backups')

        c._drop_capped_paytypes.return_value = ['ydmm_123', 'ydjd_321',
                                                'yipay', 'linkyun.api']
        c._get_default_channels.return_value = [
            {"channel": "yipay", "share": 0, "precedence": 300 },
            {"channel": "linkyun.api", "share": 0, "precedence": 200 }, ]
        p = c.select_a_channel(
            'chinaMobile', 51, 2, 'clientid', 10001, candidates)
        self.assertEqual(p, 'linkyun.api')

    @patch('tysdk.entity.duandai.channels.TyContext')
    def test_select_a_channel_case2(self, ctx):
        candidates = ['yipay']
        ctx.ftlog.debug = my_print
        ctx.Configure.get_global_item_json.return_value = ''
        ctx.RedisPayData.execute.return_value = ''
        c = Channels()
        c._drop_capped_paytypes = MagicMock()
        c._drop_capped_paytypes.return_value = ['ydmm_123', 'ydjd_321',
                                                'yipay', 'linkyun.api']
        ctx.Configure.get_global_item_json.side_effect = [
            '',
            {"ydmm": {"appid": "123"} },
            [{"channel": "yipay", "share": 0, "precedence": 100 },
             {"channel": "linkyun.api", "share": 0, "precedence": 200 }, ],
        ]
        p = c.select_a_channel(
            'chinaMobile', 51, 2, 'clientid', 10001, candidates)
        self.assertEqual(p, 'ydmm_123')

    @patch('tysdk.entity.duandai.channels.TyContext')
    def test_select_a_channel_case3(self, ctx):
        candidates = ['yipay']
        ctx.ftlog.debug = my_print
        ctx.Configure.get_global_item_json.return_value = ''
        ctx.RedisPayData.execute.return_value = ''
        c = Channels()
        c._drop_capped_paytypes = MagicMock()
        c._drop_capped_paytypes.return_value = ['yipay1', 'llinkyun.api']
        channels = ""
        paycodes = ''
        backup_channels = [
            {"channel": "yipay", "share": 0, "precedence": 100 },
            {"channel": "linkyun.api", "share": 0, "precedence": 200 }, ]
        ctx.Configure.get_global_item_json.side_effect = [
            channels,
            paycodes,
            backup_channels,
        ]
        p = c.select_a_channel(
            'chinaMobile', 51, 2, 'clientid', 10026, candidates)
        self.assertEqual(p, 'yipay')

    @patch('tysdk.entity.duandai.channels.TyContext')
    def test_select_a_channel_case5(self, ctx):
        candidates = ['yipay']
        ctx.ftlog.debug = my_print
        ctx.Configure.get_global_item_json.return_value = ''
        ctx.RedisPayData.execute.return_value = ''
        c = Channels()
        c._drop_capped_paytypes = MagicMock()
        c._drop_capped_paytypes.return_value = ['yipay', 'linkyun.api']
        channels = {"chinaMobile": [
            {"channel": "ydmm_123", "share": 10, "precedence": 10 },
            {"channel": "ydjd_321", "share": 30, "precedence": 30 },
            {"channel": "yipay", "share": 0, "precedence": 300 },
            {"channel": "linkyun.api", "share": 0, "precedence": 200 },
        ]}
        ctx.Configure.get_global_item_json.side_effect = [
            channels,
        ]
        p = c.select_a_channel(
            'chinaMobile', 51, 2, 'clientid', 10026, candidates)
        self.assertEqual(p, 'linkyun.api')

    @patch('tysdk.entity.duandai.channels.TyContext')
    def test_select_a_channel_case4(self, ctx):
        candidates = ['yipay']
        ctx.ftlog.debug = my_print
        ctx.Configure.get_global_item_json.return_value = ''
        ctx.RedisPayData.execute.return_value = ''
        c = Channels()
        c._drop_capped_paytypes = MagicMock()
        c._drop_capped_paytypes.return_value = ['ydmm_123', 'ydjd_321',
                                                'yipay', 'linkyun.api']
        channels = {"chinaMobile": [
            {"channel": "ydmm_123", "share": 10, "precedence": 10 },
            {"channel": "ydjd_321", "share": 30, "precedence": 30 },
            {"channel": "yipay", "share": 0, "precedence": 100 },
            {"channel": "linkyun.api", "share": 0, "precedence": 200 },
        ]}
        ctx.Configure.get_global_item_json.side_effect = [
            channels,
        ]
        p = c.select_a_channel(
            'chinaMobile', 51, 2, 'clientid', 10026, candidates)
        self.assertEqual(p, 'ydjd_321')


class SequentialTestLoader(unittest.TestLoader):

    def __init__(self, testcls):
        self._testcls = testcls

    def sortTestMethodsUsing(self, a, b):
        #ln = lambda f: getattr(self._testcls, f).im_func.func_code.co_firstlineno
        #lncmp = lambda _, a, b: cmp(ln(a), ln(b))
        ln_a = getattr(self._testcls, a).im_func.func_code.co_firstlineno
        ln_b = getattr(self._testcls, b).im_func.func_code.co_firstlineno
        #print a, ln_a, b, ln_b
        return cmp(ln_a, ln_b)

def main():
    #use sequential loader and fail fast, to make sure some testcases passed
    #before other cases
    loader = SequentialTestLoader(TestChannels)
    unittest.main(testLoader=loader, failfast=True)
    #unittest.main(testLoader=loader, verbosity=2, failfast=True)


if __name__ == '__main__':
    main()

