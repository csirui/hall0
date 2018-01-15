# -*- coding=utf-8 -*-

# usage:
# $ export PYTHONPATH=$(pwd)/src:$(pwd)/test:$(pwd)/../tyframework/src
# $ python -m unittest -f test_riskcontrol.TestRiskControl

from datetime import datetime
from mock import Mock, patch
import unittest
import random
import json

from tysdk.entity.duandai.riskcontrol import RiskControl


class TestRiskControl(unittest.TestCase):

    @patch('tysdk.entity.duandai.riskcontrol.TyContext')
    def test_is_device_volume_capped(self, ctx):
        userid = 10001
        riskcontrol = RiskControl(userid)
        now = datetime.now()
        yymmdd = now.strftime('%Y%m%d')
        ctx.RedisPayData.execute.return_value = ''
        paytype = 'ydmm'
        self.assertFalse(riskcontrol._is_device_volume_capped(paytype, 100, 50))
        ctx.RedisPayData.execute.return_value = json.dumps(
            {'yyyymmdd': yymmdd, 'dcount': 19, 'mcount': 29})
        self.assertFalse(riskcontrol._is_device_volume_capped(paytype, 100, 50))
        ctx.RedisPayData.execute.return_value = json.dumps(
            {'yyyymmdd': yymmdd, 'dcount': 69, 'mcount': 29})
        self.assertTrue(riskcontrol._is_device_volume_capped(paytype, 100, 50))


    @patch('tysdk.entity.duandai.riskcontrol.TyContext')
    def test_is_user_volume_capped(self, ctx):
        userid = 10001
        riskcontrol = RiskControl(userid)
        now = datetime.now()
        yymmdd = now.strftime('%Y%m%d')
        riskcontrol._user_quota = ''
        paytype = 'ydmm'
        self.assertFalse(riskcontrol._is_user_volume_capped(paytype, 100, 50))
        riskcontrol._user_quota = json.dumps({
            'ydmm': {'yyyymmdd': yymmdd, 'dcount': 19, 'mcount': 29}})
        self.assertFalse(riskcontrol._is_user_volume_capped(paytype, 100, 50))


    @patch('tysdk.entity.duandai.riskcontrol.TyContext')
    def test_is_volume_capped(self, ctx):
        userid = 10001
        riskcontrol = RiskControl(userid)
        now = datetime.now()
        yymm = now.strftime('%Y%m')
        yymmdd = now.strftime('%Y%m%d')
        other_yyMMdd = '%s%02d%s' % (yymmdd[0:4], (int(yymmdd[4:6])+1)%12, yymmdd[7:])
        other_yymmDD = yymmdd[:7] + str(random.choice(
            [i for i in xrange(10) if i != int(yymmdd[7])]))
        self.assertEqual(riskcontrol._month, yymm)
        self.assertEqual(riskcontrol._day, yymmdd)

        quota = None
        self.assertFalse(riskcontrol._is_volume_capped(quota, 0, 0))
        quota = {'yyyymmdd': yymmdd, 'dcount': 19, 'mcount': 29}
        self.assertFalse(riskcontrol._is_volume_capped(quota, 100, 50))
        quota = {'yyyymmdd': yymmdd, 'dcount': 119, 'mcount': 229}
        self.assertFalse(riskcontrol._is_volume_capped(quota, -1, -1))
        quota = {'yyyymmdd': yymmdd, 'dcount': 69, 'mcount': 89}
        self.assertTrue(riskcontrol._is_volume_capped(quota, -1, 50))
        quota = {'yyyymmdd': yymmdd, 'dcount': 69, 'mcount': 89}
        self.assertTrue(riskcontrol._is_volume_capped(quota, 100, 50))
        quota = {'yyyymmdd': yymmdd, 'dcount': 119, 'mcount': 229}
        self.assertTrue(riskcontrol._is_volume_capped(quota, 100, 50))

        quota = {'yyyymmdd': other_yymmDD, 'dcount': 69, 'mcount': 89}
        self.assertFalse(riskcontrol._is_volume_capped(quota, 100, 50))
        quota = {'yyyymmdd': other_yymmDD, 'dcount': 69, 'mcount': 189}
        self.assertTrue(riskcontrol._is_volume_capped(quota, 100, 50))

        quota = {'yyyymmdd': other_yyMMdd, 'dcount': 69, 'mcount': 189}
        self.assertFalse(riskcontrol._is_volume_capped(quota, 100, 50))


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
    loader = SequentialTestLoader(TestRiskControl)
    unittest.main(testLoader=loader, failfast=True)
    #unittest.main(testLoader=loader, verbosity=2, failfast=True)


if __name__ == '__main__':
    main()

